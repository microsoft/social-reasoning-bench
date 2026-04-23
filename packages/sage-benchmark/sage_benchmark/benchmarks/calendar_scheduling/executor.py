"""Canonical execution entry point for calendar scheduling.

The executor takes a task and produces a CalendarExecutionResult -- the raw
record of what happened, with no judgement.

    execute_task(task: HashedCalendarTask, ...) -> CalendarExecutionResult

The execution result carries:
    - task: HashedCalendarTask (with .hash for checkpoint dedup)
    - emails exchanged, final calendars, agent contexts/tools
    - Execution health (rounds_completed, exec_error)
"""

from __future__ import annotations

import asyncio
import logging
import traceback

from sage_llm import SageModelClient

from ...shared.agent import ToolCallRetriesExhausted
from ...shared.errors import is_fatal_error
from ...shared.logging import BenchmarkLogger, VerboseLogger
from .agents.assistant import CalendarAssistantAgent
from .agents.calendar_base import CalendarAgent
from .agents.calendar_requestor import CalendarRequestorAgent
from .environment import (
    AgentResources,
    CalendarSchedulingEnvironment,
)
from .environment.actions import EndConversation, RequestMeeting, Wait
from .types import (
    CalendarExecutionResult,
    CalendarTask,
    Meeting,
    Tool,
    ToolError,
)

# v2: CalendarTask has hash built in, no separate HashedCalendarTask
HashedCalendarTask = CalendarTask

logger = logging.getLogger(__name__)


async def _run_agent_turn(
    agent: CalendarAgent,
    resources: AgentResources,
    max_steps: int,
    benchmark_logger: BenchmarkLogger,
) -> tuple[list[Tool], bool]:
    """Run an agent until Wait, EndConversation, or max_steps.

    Args:
        agent: The agent to run
        resources: The agent's resources (calendar, email)
        max_steps: Maximum number of tool calls per turn

    Returns:
        Tuple of (list of tool calls made, whether conversation ended)
    """
    all_tool_calls: list[Tool] = []

    for _ in range(max_steps):
        try:
            tool_call = await agent.generate_tool_call()
        except ToolCallRetriesExhausted:
            benchmark_logger.warning(
                "[%s] Tool call retries exhausted, forcing Wait", resources.owner
            )
            tool_call = Wait()
        except Exception as e:
            # Log the error and re-raise to let caller decide if it's fatal
            benchmark_logger.error(
                "[%s] Error generating tool call: %s", resources.owner, traceback.format_exc()
            )
            raise

        all_tool_calls.append(tool_call)

        # Execute the action
        execution_succeeded = False
        try:
            benchmark_logger.debug(
                "[%s] %s: %s", resources.owner, type(tool_call).__qualname__, tool_call
            )
            result = resources.execute(tool_call)
            execution_succeeded = True
            benchmark_logger.debug("[%s] Result: %s", resources.owner, result)
        except ToolError as e:
            result = f"Error: {e}"
        except Exception:
            result = f"Error: {traceback.format_exc()}"

        agent.add_tool_call_result(result)

        # if not succeeded, let the agent try and recover up to max_steps
        if execution_succeeded:
            # Check for turn-ending actions
            if isinstance(tool_call, Wait):
                return all_tool_calls, False
            if isinstance(tool_call, EndConversation):
                return all_tool_calls, True

    # Max steps exceeded - treat as end of turn
    return all_tool_calls, False


async def _force_initial_request(
    requestor_agent: CalendarRequestorAgent,
    requestor_resources: AgentResources,
    task: CalendarTask,
    assistant_email: str,
) -> list[Tool]:
    """Force the requestor to send the initial meeting request.

    Lets the agent make a normal tool call (so it generates a natural email
    message), then replaces the meeting parameters with the predetermined
    values from the task to ensure deterministic scheduling details.

    Args:
        requestor_agent: The requestor agent to record the forced actions on.
        requestor_resources: The agent's environment resources used to execute
            the request and wait actions.
        task: The calendar task containing the requested meeting details.
        assistant_email: Email address of the assistant to include as attendee.

    Returns:
        List of tool calls made (RequestMeeting + Wait).
    """
    requested_meeting = task.requestor.requested_meeting

    message = await requestor_agent.generate_text_response(
        f"Generate a plain text message to accompany the following meeting request:\n\n```json\n{requested_meeting.model_dump_json()}\n```\n\n RESPOND WITH TEXT ONLY. DO NOT CALL ANY TOOLS."
    )
    if not message:
        logger.warning("CalendarRequestorAgent failed to generate an opening message. Sending Request with no message.")
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

    # Execute and record
    result = requestor_resources.execute(request_action)
    requestor_agent.add_forced_action(request_action, result)

    # Then Wait
    wait_action = Wait()
    wait_result = requestor_resources.execute(wait_action)
    requestor_agent.add_forced_action(wait_action, wait_result)

    return [request_action, wait_action]


async def execute_task(
    task: HashedCalendarTask,
    assistant_model: str,
    assistant_client: SageModelClient,
    requestor_model: str,
    requestor_client: SageModelClient,
    max_rounds: int,
    max_steps_per_turn: int,
    system_prompt: str | None,
    assistant_explicit_cot: bool,
    requestor_explicit_cot: bool,
    expose_preferences: bool,
    cancel_event: asyncio.Event | None = None,
    benchmark_logger: BenchmarkLogger | None = None,
) -> CalendarExecutionResult:
    """Execute a single calendar scheduling task.

    This is the canonical execution entry point. It runs the multi-turn
    requestor <-> assistant conversation and produces a CalendarExecutionResult.

    Args:
        task: The HashedCalendarTask to run (includes content hash for checkpointing)
        assistant_model: Model to use for the assistant agent
        assistant_client: SageModelClient for the assistant
        requestor_model: Model to use for the requestor agent
        requestor_client: SageModelClient for the requestor
        max_rounds: Maximum number of conversation rounds
        max_steps_per_turn: Maximum tool calls per turn
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
    )

    requestor_agent = CalendarRequestorAgent(
        model=requestor_model,
        model_client=requestor_client,
        requestor=task.requestor,
        allowed_contacts=[assistant_email],
        explicit_cot=requestor_explicit_cot,
        expose_preferences=expose_preferences,
    )

    # Force initial request from requestor (LLM generates the email body)
    await _force_initial_request(
        requestor_agent=requestor_agent,
        requestor_resources=requestor_resources,
        task=task,
        assistant_email=assistant_email,
    )

    if benchmark_logger is None:
        benchmark_logger = VerboseLogger(logger)

    # Track execution state
    rounds_completed = 0
    exec_error = None
    conversation_ended_naturally = False

    # Main simulation loop - assistant goes first since requestor already sent request
    for round_idx in range(max_rounds):
        # Check for cancellation at the start of each round
        if cancel_event and cancel_event.is_set():
            benchmark_logger.info("Task %d cancelled via event", task.id)
            break

        benchmark_logger.info("Task %d - Round %d", task.id, round_idx + 1)
        rounds_completed = round_idx + 1

        # Inject emails into assistant's context at start of their turn
        assistant_emails = assistant_resources.email.get_unread()
        assistant_agent.add_new_messages(assistant_emails)

        # Assistant turn
        assistant_ended = False
        try:
            _, assistant_ended = await _run_agent_turn(
                assistant_agent, assistant_resources, max_steps_per_turn, benchmark_logger
            )
        except asyncio.CancelledError:
            # Re-raise cancellation to propagate up
            raise
        except Exception as e:
            if is_fatal_error(e):
                exec_error = f"Assistant fatal error in round {round_idx + 1}: {str(e)}"
                benchmark_logger.error("Task %d - Fatal error: %s", task.id, exec_error)
                break
            # Recoverable error - already logged in _run_agent_turn
            # End this turn and continue to next round
            benchmark_logger.warning(
                "Task %d - Recoverable error in assistant turn, ending turn", task.id
            )

        if assistant_ended:
            conversation_ended_naturally = True
            break

        # Check for cancellation between turns
        if cancel_event and cancel_event.is_set():
            benchmark_logger.info("Task %d cancelled via event", task.id)
            break

        # Inject emails into requestor's context at start of their turn
        requestor_emails = requestor_resources.email.get_unread()
        requestor_agent.add_new_messages(requestor_emails)

        # Requestor turn
        requestor_ended = False
        try:
            _, requestor_ended = await _run_agent_turn(
                requestor_agent, requestor_resources, max_steps_per_turn, benchmark_logger
            )
        except asyncio.CancelledError:
            # Re-raise cancellation to propagate up
            raise
        except Exception as e:
            if is_fatal_error(e):
                exec_error = f"Requestor fatal error in round {round_idx + 1}: {str(e)}"
                benchmark_logger.error("Task %d - Fatal error: %s", task.id, exec_error)
                break
            # Recoverable error - already logged in _run_agent_turn
            # End this turn and continue to next round
            benchmark_logger.warning(
                "Task %d - Recoverable error in requestor turn, ending turn", task.id
            )

        if requestor_ended:
            conversation_ended_naturally = True
            break

    max_rounds_reached = rounds_completed >= max_rounds and not conversation_ended_naturally
    if max_rounds_reached:
        exec_error = f"Max rounds reached ({max_rounds}) without natural conversation end"

    # Log completion (don't call on_task_complete here - that's done after eval)
    benchmark_logger.debug(
        "Task %d execution completed - rounds: %d, max_rounds_reached: %s, exec_error: %s",
        task.id,
        rounds_completed,
        max_rounds_reached,
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
        rounds_completed=rounds_completed,
        max_rounds_reached=max_rounds_reached,
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
