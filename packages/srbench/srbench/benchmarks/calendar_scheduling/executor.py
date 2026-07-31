"""Canonical execution entry point for calendar scheduling.

The executor takes a task and produces a CalendarExecutionResult -- the raw
record of what happened, with no judgement.

    execute_task(task: HashedCalendarTask, ...) -> CalendarExecutionResult

Each agent owns its run loop and touches the environment only through tools:
``AgentResources.invoke_tool`` is the single execution path for every action —
the environment owns all tool validation — and the executor hands it directly
to ``agent.run``, forces the requestor's opening meeting request, then races
both loops against the environment's end signal and external cancellation.
``Wait`` blocks until the counterpart acts and returns any new emails, so no
scheduler injects turns. The forced opening reaches the assistant the same
way, from its first ``Wait``.

The assistant side supports "bring your own agent". Pass
``assistant_agent_factory`` (any callable returning a ``BaseAssistantAgent``,
called with ``task=CalendarAssistantTask(...)``) to replace the built-in
``CalendarAssistantAgent``.

The execution result carries:
    - task: HashedCalendarTask (with .hash for checkpoint dedup)
    - emails exchanged, final calendars, agent contexts/tools
    - Execution health (max_rounds_reached, exec_error)
"""

from __future__ import annotations

import asyncio
import logging
import traceback
from typing import Callable

from srbench_llm import SRBenchModelClient

from ...shared.agent import BaseAssistantAgent
from ...shared.logging import BenchmarkLogger, VerboseLogger
from ...shared.signals import run_agents_until_end
from .agents.assistant import CalendarAssistantAgent
from .agents.calendar_requestor import CalendarRequestorAgent
from .environment import (
    AgentResources,
    CalendarSchedulingEnvironment,
)
from .environment.actions import CALENDAR_TOOLS, EndConversation, RequestMeeting
from .environment.utils import BUSINESS_HOURS_WINDOW, WHOLE_DAY_WINDOW
from .types import (
    CalendarAssistantTask,
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

# The environment owns each role's tool space and hands it to ``agent.run``.
# The same Tool classes seed the environment's ``invoke_tool`` registry, and
# their OpenAI schemas are what the agent sees. Only the assistant may end the
# conversation.
ASSISTANT_TOOLS: list[type[Tool]] = list(CALENDAR_TOOLS) + [EndConversation]
REQUESTOR_TOOLS: list[type[Tool]] = list(CALENDAR_TOOLS)
ASSISTANT_TOOL_SPACE = [t.get_openai_function_tool_param() for t in ASSISTANT_TOOLS]
REQUESTOR_TOOL_SPACE = [t.get_openai_function_tool_param() for t in REQUESTOR_TOOLS]


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

    # Route the forced opening through the same name+arguments boundary every
    # agent uses, so the environment owns its validation and execution.
    result = await requestor_resources.invoke_tool(
        request_action.get_name(), request_action.model_dump()
    )
    requestor_agent.add_forced_action(
        request_action.get_name(), request_action.model_dump(), result
    )

    return request_action


async def execute_task(
    task: HashedCalendarTask,
    assistant_model: str | None,
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
    preference_guidance: bool = True,
    *,
    assistant_agent_factory: Callable[..., BaseAssistantAgent] | None = None,
) -> CalendarExecutionResult:
    """Execute a single calendar scheduling task.

    This is the canonical execution entry point. It runs the requestor and
    assistant agent loops concurrently until an agent ends the conversation,
    a budget runs out, or the conversation stalls, and produces a
    CalendarExecutionResult.

    Args:
        task: The HashedCalendarTask to run (includes content hash for checkpointing)
        assistant_model: Model to use for the built-in assistant agent. May be
            ``None`` when ``assistant_agent_factory`` is provided.
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
        assistant_agent_factory: Optional factory for a user-provided
        assistant_agent_factory: Optional factory for a user-provided
            assistant agent (bring your own agent). Called with the keyword
            argument ``task`` (a ``CalendarAssistantTask`` carrying the
            assistant's brief and ``max_actions``). The tool space and
            ``invoke_tool`` are delivered separately through ``agent.run``.
            When provided, the built-in ``CalendarAssistantAgent`` and its LLM
            configuration (``assistant_model``, ``system_prompt``,
            ``assistant_explicit_cot``, ``expose_preferences``) are not used.

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
        tools=ASSISTANT_TOOLS,
        allowed_contacts=[requestor_email],
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
        tools=REQUESTOR_TOOLS,
        allowed_contacts=[assistant_email],
    )

    # The assistant's private brief, delivered through its constructor.
    assistant_task = CalendarAssistantTask(
        assistant=task.assistant,
        max_actions=max_actions_per_agent,
    )

    # Initialize agents
    assistant_agent: BaseAssistantAgent
    if assistant_agent_factory is not None:
        assistant_agent = assistant_agent_factory(task=assistant_task)
    else:
        if assistant_model is None:
            raise ValueError(
                "assistant_model is required when no assistant_agent_factory is provided"
            )
        assistant_agent = CalendarAssistantAgent(
            model=assistant_model,
            model_client=assistant_client,
            task=assistant_task,
            system_prompt=system_prompt,
            explicit_cot=assistant_explicit_cot,
            expose_preferences=expose_preferences,
            preference_guidance=preference_guidance,
        )

    requestor_agent = CalendarRequestorAgent(
        model=requestor_model,
        model_client=requestor_client,
        requestor=task.requestor,
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

        # The forced request left the opening email unread and the
        # assistant's wake signal set, so the assistant's first Wait returns
        # immediately with the request. Delivery happens through tools, not
        # by pushing context into the agent.
        await run_agents_until_end(
            [
                assistant_agent.run(assistant_resources.invoke_tool, ASSISTANT_TOOL_SPACE),
                requestor_agent.run(requestor_resources.invoke_tool, REQUESTOR_TOOL_SPACE),
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
        action_trace=list(environment.action_trace),
        # Transcripts are debugging artifacts, captured only when the agent
        # exposes them. Evaluation reads the environment's action trace.
        assistant_context=list(getattr(assistant_agent, "messages", [])),
        requestor_context=list(requestor_agent.messages),
        assistant_tools=list(ASSISTANT_TOOL_SPACE),
        requestor_tools=list(REQUESTOR_TOOL_SPACE),
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
