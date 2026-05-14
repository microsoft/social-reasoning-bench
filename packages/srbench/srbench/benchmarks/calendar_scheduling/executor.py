"""Canonical execution entry point for calendar scheduling (agent-driven loop).

The executor:

1. Sets up the env + per-agent resources.
2. Drives the counterparty's forced opening: asks it to compose the meeting-
   request message body via :meth:`CounterpartyAgent.generate_text`, executes
   the deterministic ``RequestMeeting`` action against the env, and records
   the result on the requestor's transcript via ``add_forced_action``.
3. Spawns both agents' ``run`` loops concurrently. The agents drive their own
   action loops via the ``invoke_tool`` callback (bound to
   ``resources.execute``). The executor waits for the first of:
   - either agent's ``run`` to return,
   - ``env.end_event`` to fire (``EndConversation`` was executed),
   - the wall-clock timeout to elapse,
   - the externally-supplied ``cancel_event`` to fire.
4. Cancels the remaining tasks and harvests state into a
   ``CalendarExecutionResult``.
"""

from __future__ import annotations

import asyncio
import logging
import traceback

from srbench_llm import SRBenchModelClient

from ...shared.logging import BenchmarkLogger, VerboseLogger
from .agents.assistant import CalendarAssistantAgent
from .agents.calendar_requestor import CalendarRequestorAgent
from .environment import (
    AgentResources,
    CalendarSchedulingEnvironment,
)
from .environment.actions import RequestMeeting
from .types import (
    CalendarExecutionResult,
    CalendarTask,
    Meeting,
    Tool,
)

# v2: CalendarTask has hash built in, no separate HashedCalendarTask
HashedCalendarTask = CalendarTask

logger = logging.getLogger(__name__)


async def _force_initial_request(
    requestor_agent: CalendarRequestorAgent,
    requestor_resources: AgentResources,
    task: CalendarTask,
    assistant_email: str,
) -> Tool:
    """Drive the deterministic opening RequestMeeting from the requestor.

    The requestor agent composes the natural-language body of the message via
    its ``generate_text`` capability, the harness wraps it in a
    ``RequestMeeting`` with predetermined uid/date/time fields, executes it
    against the env, and records the forced action on the requestor's
    transcript.
    """
    requested_meeting = task.requestor.requested_meeting

    message = await requestor_agent.generate_text(
        f"Generate a plain text message to accompany the following meeting "
        f"request:\n\n```json\n{requested_meeting.model_dump_json()}\n```\n\n"
        f"RESPOND WITH TEXT ONLY. DO NOT CALL ANY TOOLS."
    )
    if not message:
        logger.warning(
            "CalendarRequestorAgent failed to generate an opening message. "
            "Sending RequestMeeting with no body."
        )

    request_action = RequestMeeting(
        message=message,
        uid=requested_meeting.uid,
        title=requested_meeting.title,
        description=requested_meeting.description,
        organizer=task.requestor.email,
        date=requested_meeting.date,
        start=requested_meeting.start_time,
        end=requested_meeting.end_time,
        attendees=[assistant_email],
    )

    result = await requestor_resources.execute(request_action)
    requestor_agent.add_forced_action(request_action, result)
    return request_action


async def execute_task(
    task: HashedCalendarTask,
    assistant_model: str,
    assistant_client: SRBenchModelClient,
    requestor_model: str,
    requestor_client: SRBenchModelClient,
    system_prompt: str | None,
    assistant_explicit_cot: bool,
    requestor_explicit_cot: bool,
    expose_preferences: bool,
    max_actions_per_agent: int = 50,
    max_wall_time_seconds: float | None = None,
    cancel_event: asyncio.Event | None = None,
    benchmark_logger: BenchmarkLogger | None = None,
) -> CalendarExecutionResult:
    """Execute a single calendar scheduling task."""
    if benchmark_logger is None:
        benchmark_logger = VerboseLogger(logger)

    environment = CalendarSchedulingEnvironment()

    assistant_email = task.assistant.email
    requestor_email = task.requestor.email

    assistant_initial_meetings = [
        Meeting(
            uid=m.uid,
            title=m.title,
            description=m.description,
            organizer=m.organizer,
            date=m.date,
            start_time=m.start_time,
            end_time=m.end_time,
            attendees=list(m.attendees),
        )
        for m in task.assistant.calendar
    ]
    assistant_resources = environment.create_agent_resources(
        owner=assistant_email,
        initial_meetings=assistant_initial_meetings,
        contacts=task.assistant.contacts,
        allowed_date=task.requestor.requested_meeting.date,
    )

    requestor_initial_meetings = [
        Meeting(
            uid=m.uid,
            title=m.title,
            description=m.description,
            organizer=m.organizer,
            date=m.date,
            start_time=m.start_time,
            end_time=m.end_time,
            attendees=list(m.attendees),
        )
        for m in task.requestor.calendar
    ]
    requestor_resources = environment.create_agent_resources(
        owner=requestor_email,
        initial_meetings=requestor_initial_meetings,
        allowed_date=task.requestor.requested_meeting.date,
    )

    assistant_agent = CalendarAssistantAgent(
        model=assistant_model,
        model_client=assistant_client,
        assistant=task.assistant,
        allowed_contacts=[requestor_email],
        system_prompt=system_prompt,
        explicit_cot=assistant_explicit_cot,
        expose_preferences=expose_preferences,
        max_actions=max_actions_per_agent,
    )

    requestor_agent = CalendarRequestorAgent(
        model=requestor_model,
        model_client=requestor_client,
        requestor=task.requestor,
        allowed_contacts=[assistant_email],
        explicit_cot=requestor_explicit_cot,
        expose_preferences=expose_preferences,
        max_actions=max_actions_per_agent,
    )

    exec_error: str | None = None
    try:
        await _force_initial_request(
            requestor_agent=requestor_agent,
            requestor_resources=requestor_resources,
            task=task,
            assistant_email=assistant_email,
        )

        timeout_ctx = (
            asyncio.timeout(max_wall_time_seconds)
            if max_wall_time_seconds is not None
            else _NullAsyncContext()
        )
        try:
            async with timeout_ctx:
                await _wait_for_any(
                    environment=environment,
                    assistant_agent=assistant_agent,
                    assistant_resources=assistant_resources,
                    requestor_agent=requestor_agent,
                    requestor_resources=requestor_resources,
                    cancel_event=cancel_event,
                )
        except asyncio.TimeoutError:
            environment.mark_ended(reason="max_wall_time")

        if not environment.end_event.is_set():
            environment.mark_ended(reason="max_actions")
    except asyncio.CancelledError:
        environment.mark_ended(reason="cancelled")
        raise
    except Exception as e:
        exec_error = f"Calendar execution error: {e}"
        benchmark_logger.error(
            "Task %d - Fatal error: %s\n%s", task.id, exec_error, traceback.format_exc()
        )
        environment.mark_ended(reason="error")
    finally:
        await assistant_agent.close()
        await requestor_agent.close()

    benchmark_logger.debug(
        "Task %d execution completed - total_actions: %d, end_reason: %s",
        task.id,
        environment.action_count,
        environment.end_reason,
    )

    return CalendarExecutionResult(
        task=task,
        emails=environment.get_all_emails(),
        final_assistant_calendar=list(assistant_resources.calendar.list_meetings()),
        final_requestor_calendar=list(requestor_resources.calendar.list_meetings()),
        assistant_context=assistant_agent.messages,
        requestor_context=requestor_agent.messages,
        assistant_tools=assistant_agent.tools,
        requestor_tools=requestor_agent.tools,
        total_actions=environment.action_count,
        end_reason=environment.end_reason,
        error=exec_error,
    )


async def _wait_for_any(
    *,
    environment: CalendarSchedulingEnvironment,
    assistant_agent: CalendarAssistantAgent,
    assistant_resources: AgentResources,
    requestor_agent: CalendarRequestorAgent,
    requestor_resources: AgentResources,
    cancel_event: asyncio.Event | None,
) -> None:
    """Run both agents until any of them finishes, env.end_event fires, or cancellation."""
    t_assistant = asyncio.create_task(assistant_agent.run(assistant_resources.execute))
    t_requestor = asyncio.create_task(requestor_agent.run(requestor_resources.execute))
    t_end = asyncio.create_task(environment.end_event.wait())
    watch: set[asyncio.Task] = {t_assistant, t_requestor, t_end}
    t_cancel: asyncio.Task | None = None
    if cancel_event is not None:
        t_cancel = asyncio.create_task(cancel_event.wait())
        watch.add(t_cancel)

    try:
        await asyncio.wait(watch, return_when=asyncio.FIRST_COMPLETED)
    finally:
        for t in (t_assistant, t_requestor, t_end, t_cancel):
            if t is not None and not t.done():
                t.cancel()
        await asyncio.gather(*[t for t in watch if t is not None], return_exceptions=True)


class _NullAsyncContext:
    async def __aenter__(self) -> None:
        return None

    async def __aexit__(self, *_exc) -> bool:
        return False


# Backward-compatible alias
run_single_task = execute_task

__all__ = [
    "execute_task",
    "run_single_task",
    "HashedCalendarTask",
    "CalendarExecutionResult",
]
