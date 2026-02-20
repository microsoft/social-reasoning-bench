"""Runner for calendar scheduling simulations."""

import logging
import traceback
from typing import Callable

import litellm
import openai

from sage_benchmark.shared.executors import TaskPoolExecutor

logger = logging.getLogger(__name__)

from sage_llm import ModelClient

from .agents.assistant import CalendarAssistantAgent
from .agents.calendar_base import CalendarAgent
from .agents.calendar_requestor import CalendarRequestorAgent
from .environment import (
    AgentResources,
    CalendarSchedulingEnvironment,
)
from .environment.actions import EndConversation, RequestMeeting, Wait
from .types import (
    Artifact,
    CalendarTask,
    KeyedCalendarTask,
    Meeting,
    TaskExecutionResult,
    Tool,
    ToolError,
)


def _is_fatal_error(e: Exception) -> bool:
    """Check if error is fatal (should stop task immediately).

    Fatal errors are unrecoverable and indicate the task cannot continue:
    - Authentication failures (invalid API key)
    - Permission denied (no access to model)
    - Model not found
    - Context length exceeded (cannot fit conversation in model's context window)
    - Quota exhausted (billing issue)
    - Budget exceeded (litellm proxy budget)

    Other errors (rate limits, timeouts, network issues) are recoverable.

    References:
    - https://docs.litellm.ai/docs/exception_mapping
    - https://platform.openai.com/docs/guides/error-codes
    """
    # Check for context length exceeded (multiple ways this can be raised)
    if isinstance(e, litellm.ContextWindowExceededError):
        return True  # Specific litellm exception for context overflow

    # Check litellm exception types
    if isinstance(e, litellm.AuthenticationError):
        return True  # 401 - Invalid API key
    if isinstance(e, litellm.NotFoundError):
        return True  # 404 - Model doesn't exist
    if hasattr(litellm, "BudgetExceededError") and isinstance(e, litellm.BudgetExceededError):
        return True  # litellm proxy budget constraint

    # Check openai exception types (may not be wrapped by litellm yet)
    if isinstance(e, openai.AuthenticationError):
        return True  # 401 - Invalid API key
    if isinstance(e, openai.PermissionDeniedError):
        return True  # 403 - No access to model
    if isinstance(e, openai.NotFoundError):
        return True  # 404 - Model doesn't exist

    # RateLimitError can be either fatal (quota) or recoverable (rate limit)
    # Distinguish by checking error message for 'insufficient_quota' vs 'rate_limit_exceeded'
    if isinstance(e, (litellm.RateLimitError, openai.RateLimitError)):
        error_str = str(e).lower()
        # Check for quota exhaustion (fatal)
        if "insufficient_quota" in error_str or "exceeded your current quota" in error_str:
            return True  # Fatal - billing/quota issue
        # Otherwise it's a recoverable rate limit (throttling)
        return False

    # Fallback: check error string for context length issues
    # (handles cases where litellm wraps as generic APIConnectionError/BadRequestError)
    error_str = str(e).lower()
    if "context_length_exceeded" in error_str or "maximum context length" in error_str:
        return True  # Fatal - context overflow

    # All other errors are considered recoverable (timeouts, service unavailable, etc.)
    return False


async def _run_agent_turn(
    agent: CalendarAgent,
    resources: AgentResources,
    max_steps: int,
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
        except Exception as e:
            # Log the error and re-raise to let caller decide if it's fatal
            logger.error("Error generating tool call: %s", traceback.format_exc())
            raise

        all_tool_calls.append(tool_call)

        # Execute the action
        execution_succeeded = True
        try:
            logger.debug("[%s] %s: %s", resources.owner, type(tool_call).__qualname__, tool_call)
            result = resources.execute(tool_call)
            logger.debug("[%s] Result: %s", resources.owner, result)
        except ToolError as e:
            result = f"Error: {e}"
            execution_succeeded = False
        except Exception:
            result = f"Error: {traceback.format_exc()}"
            execution_succeeded = False

        agent.add_tool_call_result(result)

        # Check for turn-ending actions
        if isinstance(tool_call, Wait):
            return all_tool_calls, False
        if isinstance(tool_call, EndConversation) and execution_succeeded:
            return all_tool_calls, True

    # Max steps exceeded - treat as end of turn
    return all_tool_calls, False


def _force_initial_request(
    requestor_agent: CalendarRequestorAgent,
    requestor_resources: AgentResources,
    task: CalendarTask,
    assistant_email: str,
) -> list[Tool]:
    """Force the requestor to send the initial meeting request.

    This ensures the simulation starts with a concrete request rather than
    relying on the LLM to initiate.

    Returns:
        List of tool calls made (RequestMeeting + Wait)
    """
    requested_meeting = task.requestor.requested_meeting

    # Create the meeting request action
    request_action = RequestMeeting(
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


async def run_single_task(
    task: CalendarTask,
    task_key: str,
    assistant_model: str,
    assistant_client: ModelClient,
    requestor_model: str,
    requestor_client: ModelClient,
    max_rounds: int,
    max_steps_per_turn: int,
    artifacts: list[Artifact] | None,
    system_prompt: str,
    assistant_explicit_cot: bool,
    requestor_explicit_cot: bool,
    expose_preferences: bool,
) -> TaskExecutionResult:
    """Run a single calendar scheduling task.

    Args:
        task: The CalendarTask to run
        task_key: Content hash of the task for checkpointing
        assistant_model: Model to use for the assistant agent
        assistant_client: ModelClient for the assistant
        requestor_model: Model to use for the requestor agent
        requestor_client: ModelClient for the requestor
        max_rounds: Maximum number of conversation rounds
        max_steps_per_turn: Maximum tool calls per turn
        artifacts: Optional list of artifacts to provide context to assistant
        system_prompt: Optional system prompt for the assistant agent
        assistant_explicit_cot: Whether to use explicit CoT for assistant
        requestor_explicit_cot: Whether to use explicit CoT for requestor

    Returns:
        TaskExecutionResult with all execution data
    """
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

    requestor_resources = environment.create_agent_resources(
        owner=requestor_email,
        initial_meetings=[],  # Requestor starts with empty calendar
        allowed_date=task.requestor.requested_meeting.date,
    )

    # Initialize agents
    assistant_agent = CalendarAssistantAgent(
        model=assistant_model,
        model_client=assistant_client,
        assistant=task.assistant,
        allowed_contacts=[requestor_email],
        artifacts=artifacts,
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
    )

    # Force initial request from requestor
    _force_initial_request(
        requestor_agent=requestor_agent,
        requestor_resources=requestor_resources,
        task=task,
        assistant_email=assistant_email,
    )

    # Track execution state
    rounds_completed = 0
    fatal_error = None
    conversation_ended_naturally = False

    # Main simulation loop - assistant goes first since requestor already sent request
    for round_idx in range(max_rounds):
        logger.info("Task %d - Round %d", task.id, round_idx + 1)
        rounds_completed = round_idx + 1

        # Inject emails into assistant's context at start of their turn
        assistant_emails = assistant_resources.email.get_unread()
        assistant_agent.add_new_messages(assistant_emails)

        # Assistant turn
        assistant_ended = False
        try:
            assistant_tool_calls, assistant_ended = await _run_agent_turn(
                assistant_agent, assistant_resources, max_steps_per_turn
            )
        except Exception as e:
            if _is_fatal_error(e):
                fatal_error = f"Assistant fatal error in round {round_idx + 1}: {str(e)}"
                logger.error("Task %d - Fatal error: %s", task.id, fatal_error)
                break
            # Recoverable error - already logged in _run_agent_turn
            # End this turn and continue to next round
            logger.warning("Task %d - Recoverable error in assistant turn, ending turn", task.id)

        if assistant_ended:
            conversation_ended_naturally = True
            break

        # Inject emails into requestor's context at start of their turn
        requestor_emails = requestor_resources.email.get_unread()
        requestor_agent.add_new_messages(requestor_emails)

        # Requestor turn
        requestor_ended = False
        try:
            requestor_tool_calls, requestor_ended = await _run_agent_turn(
                requestor_agent, requestor_resources, max_steps_per_turn
            )
        except Exception as e:
            if _is_fatal_error(e):
                fatal_error = f"Requestor fatal error in round {round_idx + 1}: {str(e)}"
                logger.error("Task %d - Fatal error: %s", task.id, fatal_error)
                break
            # Recoverable error - already logged in _run_agent_turn
            # End this turn and continue to next round
            logger.warning("Task %d - Recoverable error in requestor turn, ending turn", task.id)

        if requestor_ended:
            conversation_ended_naturally = True
            break

    max_rounds_reached = rounds_completed >= max_rounds and not conversation_ended_naturally
    logger.info(
        "Task %d completed - rounds: %d, max_rounds_reached: %s, fatal_error: %s",
        task.id,
        rounds_completed,
        max_rounds_reached,
        fatal_error is not None,
    )

    return TaskExecutionResult(
        task_key=task_key,
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
        fatal_error=fatal_error,
    )


async def run_tasks(
    tasks: list[KeyedCalendarTask],
    assistant_model: str,
    assistant_client: ModelClient,
    requestor_model: str,
    requestor_client: ModelClient,
    max_rounds: int,
    max_steps_per_turn: int,
    batch_size: int,
    artifacts_by_task: dict[int, list[Artifact]] | None,
    system_prompt: str | None,
    assistant_explicit_cot: bool,
    requestor_explicit_cot: bool,
    expose_preferences: bool,
    on_task_complete: Callable[[TaskExecutionResult], None] | None = None,
    skip_task_keys: set[str] | None = None,
) -> list[TaskExecutionResult]:
    """Run a list of tasks in parallel batches.

    Args:
        tasks: List of KeyedCalendarTask objects to run
        assistant_model: Model to use for the assistant agent
        assistant_client: ModelClient for the assistant
        requestor_model: Model to use for the requestor agent
        requestor_client: ModelClient for the requestor
        max_rounds: Maximum number of conversation rounds per task
        max_steps_per_turn: Maximum tool calls per turn
        batch_size: Number of tasks to run in parallel
        artifacts_by_task: Optional dict mapping task id to artifacts list
        system_prompt: Optional system prompt for the assistant agent
        assistant_explicit_cot: Whether to use explicit CoT for assistant
        requestor_explicit_cot: Whether to use explicit CoT for requestor
        on_task_complete: Optional callback invoked after each task completes
        skip_task_keys: Optional set of task keys to skip (for resume)

    Returns:
        List of TaskExecutionResult for each task
    """
    # Filter out already-completed tasks
    tasks_to_run = [
        task for task in tasks if skip_task_keys is None or task.task_key not in skip_task_keys
    ]

    if skip_task_keys:
        logger.info(
            "Skipping %d already-completed tasks, running %d tasks",
            len(tasks) - len(tasks_to_run),
            len(tasks_to_run),
        )

    executor = TaskPoolExecutor(
        batch_size=batch_size,
        on_task_complete=on_task_complete,
        task_logger=logger,
    )
    return await executor.run(
        run_single_task(
            task=task,
            task_key=task.task_key,
            assistant_model=assistant_model,
            assistant_client=assistant_client,
            requestor_model=requestor_model,
            requestor_client=requestor_client,
            max_rounds=max_rounds,
            max_steps_per_turn=max_steps_per_turn,
            artifacts=artifacts_by_task.get(task.id) if artifacts_by_task else None,
            system_prompt=system_prompt,
            assistant_explicit_cot=assistant_explicit_cot,
            requestor_explicit_cot=requestor_explicit_cot,
            expose_preferences=expose_preferences,
        )
        for task in tasks_to_run
    )
