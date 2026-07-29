"""Canonical execution entry point for calendar scheduling.

The executor takes a task and produces a CalendarExecutionResult -- the raw
record of what happened, with no judgement.

    execute_task(task: HashedCalendarTask, ...) -> CalendarExecutionResult

Each agent owns its run loop and touches the environment only through tools:
``AgentResources.execute`` is the single execution path for every action, and
the executor hands it directly to ``agent.run``, forces the requestor's
opening meeting request, then races both loops against the environment's end
signal and external cancellation. ``Wait`` blocks until the counterpart acts
and returns any new emails, so no scheduler injects turns.

The execution result carries:
    - task: HashedCalendarTask (with .hash for checkpoint dedup)
    - emails exchanged, final calendars, agent contexts/tools
    - Execution health (max_rounds_reached, exec_error)
"""

from __future__ import annotations

import asyncio
import logging
import traceback

from srbench_llm import SRBenchModelClient

from ...shared.logging import BenchmarkLogger, VerboseLogger
from ...shared.signals import run_agents_until_end
from .agents.assistant import CalendarAssistantAgent
from .agents.calendar_requestor import CalendarRequestorAgent
from .environment import (
    AgentResources,
    CalendarSchedulingEnvironment,
)
from .environment.actions import RequestMeeting
from .environment.utils import BUSINESS_HOURS_WINDOW, WHOLE_DAY_WINDOW
from .types import (
    CalendarExecutionResult,
    CalendarTask,
    Meeting,
    Tool,
)

# v2: CalendarTask has hash built in, no separate HashedCalendarTask
HashedCalendarTask = CalendarTask

logger = logging.getLogger(__name__)

# End reasons recorded by the harness (rather than by an agent's
# EndConversation) when a budget or coordination limit stops the run.
_HARNESS_STOP_REASONS = {"agent_stopped", "stalemate"}


async def _force_initial_request(
    requestor_agent: CalendarRequestorAgent,
    requestor_resources: AgentResources,
    task: CalendarTask,
    assistant_email: str,
) -> Tool:
    """Force the requestor to send the initial meeting request.

    Lets the agent generate a natural email message, then replaces the meeting
    parameters with the predetermined values from the task to ensure
    deterministic scheduling details, executes the request against the
    environment, and records the forced action on the requestor's transcript.

    Args:
        requestor_agent: The requestor agent to record the forced action on.
        requestor_resources: The requestor's environment resources.
        task: The calendar task containing the requested meeting details.
        assistant_email: Email address of the assistant to include as attendee.

    Returns:
        The RequestMeeting action that was executed.
    """
    requested_meeting = task.requestor.requested_meeting

    message = await requestor_agent.generate_text_response(
        f"Generate a plain text message to accompany the following meeting request:\n\n```json\n{requested_meeting.model_dump_json()}\n```\n\n RESPOND WITH TEXT ONLY. DO NOT CALL ANY TOOLS."
    )
    if not message:
        logger.warning(
            "CalendarRequestorAgent failed to generate an opening message. Sending Request with no message."
        )
    # Create the meeting request with predetermined params + agent's message
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
    max_actions_per_agent: int,
    system_prompt: str | None,
    assistant_explicit_cot: bool,
    requestor_explicit_cot: bool,
    expose_preferences: bool,
    cancel_event: asyncio.Event | None = None,
    benchmark_logger: BenchmarkLogger | None = None,
) -> CalendarExecutionResult:
    """Execute a single calendar scheduling task.

    This is the canonical execution entry point. It runs the requestor and
    assistant agent loops concurrently until an agent ends the conversation,
    a budget runs out, or the conversation stalls, and produces a
    CalendarExecutionResult.

    Args:
        task: The HashedCalendarTask to run (includes content hash for checkpointing)
        assistant_model: Model to use for the assistant agent
        assistant_client: SRBenchModelClient for the assistant
        requestor_model: Model to use for the requestor agent
        requestor_client: SRBenchModelClient for the requestor
        max_actions_per_agent: Maximum tool calls per agent for the whole conversation
        system_prompt: Optional resolved system prompt for the assistant agent
        assistant_explicit_cot: Whether to use explicit CoT for assistant
        requestor_explicit_cot: Whether to use explicit CoT for requestor
        expose_preferences: Whether to expose scheduling preferences
        cancel_event: Optional event to signal cancellation
        benchmark_logger: Optional logger for progress tracking

    Returns:
        CalendarExecutionResult with all execution data
    """
    if benchmark_logger is None:
        benchmark_logger = VerboseLogger(logger)

    # Get agent names from task
    assistant_email = task.assistant.email
    requestor_email = task.requestor.email

    # Create environment and agent resources
    environment = CalendarSchedulingEnvironment()
    signals = environment.signals

    # A preference document owns its principal's bookable hours, so the
    # calendar reports free blocks over the whole day and lets the document
    # narrow them. Numeric tasks keep the business-hours default.
    free_block_window = (
        WHOLE_DAY_WINDOW if task.assistant.preference_file else BUSINESS_HOURS_WINDOW
    )

    # Convert LabeledMeetings to Meetings for assistant's calendar
    # (strip the is_movable and is_secret fields that are hidden from the LLM)
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
        free_block_window=free_block_window,
    )

    # Convert LabeledMeetings to Meetings for requestor's calendar
    # (strip the is_movable and is_secret fields that are hidden from the LLM)
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
        free_block_window=free_block_window,
    )

    # Initialize agents
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

    exec_error = None
    try:
        # Force initial request from requestor (LLM generates the email body)
        await _force_initial_request(
            requestor_agent=requestor_agent,
            requestor_resources=requestor_resources,
            task=task,
            assistant_email=assistant_email,
        )

        # Surface the opening request in the assistant's context before its
        # loop starts (exactly what the turn-based executor did at the start
        # of each turn), and clear the wake signal that delivery produced.
        assistant_agent.add_new_messages(assistant_resources.email.get_unread())
        signals.clear(assistant_email)

        await run_agents_until_end(
            [
                assistant_agent.run(assistant_resources.execute),
                requestor_agent.run(requestor_resources.execute),
            ],
            signals=signals,
            cancel_event=cancel_event,
        )
    except asyncio.CancelledError:
        signals.end(reason="cancelled")
        raise
    except Exception as e:
        exec_error = f"Calendar execution error: {e}"
        benchmark_logger.error(
            "Task %d - Fatal error: %s\n%s", task.id, exec_error, traceback.format_exc()
        )
        signals.end(reason="error")

    # Log completion (don't call on_task_complete here - that's done after eval)
    benchmark_logger.debug(
        "Task %d execution completed - end_reason: %s, exec_error: %s",
        task.id,
        signals.end_reason,
        exec_error is not None,
    )

    return CalendarExecutionResult(
        task=task,
        emails=environment.get_all_emails(),
        final_assistant_calendar=list(assistant_resources.calendar.list_meetings()),
        final_requestor_calendar=list(requestor_resources.calendar.list_meetings()),
        assistant_context=list(assistant_agent._messages),
        requestor_context=list(requestor_agent._messages),
        assistant_tools=assistant_agent.tools,
        requestor_tools=requestor_agent.tools,
        max_rounds_reached=signals.end_reason in _HARNESS_STOP_REASONS,
        error=exec_error,
    )


# Backward-compatible alias
run_single_task = execute_task

__all__ = [
    "execute_task",
    "run_single_task",
    "HashedCalendarTask",
    "CalendarExecutionResult",
]
