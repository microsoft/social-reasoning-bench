"""Runner for calendar scheduling simulations."""

import logging
import traceback

from sage_benchmark.shared.executors import TaskPoolExecutor

logger = logging.getLogger(__name__)

from .agents.calendar_assistant import CalendarAssistantAgent
from .agents.calendar_base import CalendarAgent
from .agents.calendar_requestor import CalendarRequestorAgent
from .environment import (
    AgentResources,
    CalendarSchedulingEnvironment,
)
from .environment.actions import EndConversation, RequestMeeting, Wait
from .model_client import ModelClient
from .types import Artifact, CalendarTask, Meeting, TaskExecutionResult, Tool, ToolError


async def _run_agent_turn(
    agent: CalendarAgent,
    resources: AgentResources,
    max_steps: int = 20,
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
        except Exception:
            # If we can't generate a tool call, treat as end of turn
            logger.error("Error generating tool call: %s", traceback.format_exc())
            break

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
    task_index: int,
    task: CalendarTask,
    assistant_model: str,
    assistant_client: ModelClient,
    requestor_model: str,
    requestor_client: ModelClient,
    max_rounds: int = 100,
    max_steps_per_turn: int = 20,
    artifacts: list[Artifact] | None = None,
) -> TaskExecutionResult:
    """Run a single calendar scheduling task.

    Args:
        task_index: Index of this task in the task list
        task: The CalendarTask to run
        assistant_model: Model to use for the assistant agent
        assistant_client: ModelClient for the assistant
        requestor_model: Model to use for the requestor agent
        requestor_client: ModelClient for the requestor
        max_rounds: Maximum number of conversation rounds
        max_steps_per_turn: Maximum tool calls per turn
        artifacts: Optional list of artifacts to provide context to assistant

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
    )

    requestor_agent = CalendarRequestorAgent(
        model=requestor_model,
        model_client=requestor_client,
        requestor=task.requestor,
        allowed_contacts=[assistant_email],
    )

    # Force initial request from requestor
    _force_initial_request(
        requestor_agent=requestor_agent,
        requestor_resources=requestor_resources,
        task=task,
        assistant_email=assistant_email,
    )

    # Main simulation loop - assistant goes first since requestor already sent request
    for round_idx in range(max_rounds):
        logger.info("Task %d - Round %d", task_index, round_idx + 1)

        # Assistant turn
        assistant_tool_calls, assistant_ended = await _run_agent_turn(
            assistant_agent, assistant_resources, max_steps_per_turn
        )

        if assistant_ended:
            break

        # Requestor turn
        requestor_tool_calls, requestor_ended = await _run_agent_turn(
            requestor_agent, requestor_resources, max_steps_per_turn
        )

        if requestor_ended:
            break

    logger.info("Task %d completed", task_index)

    return TaskExecutionResult(
        task_index=task_index,
        task=task,
        emails=environment.get_all_emails(),
        final_assistant_calendar=list(assistant_resources.calendar.list_meetings()),
        final_requestor_calendar=list(requestor_resources.calendar.list_meetings()),
        assistant_context=list(assistant_agent._messages),
        requestor_context=list(requestor_agent._messages),
    )


async def run_tasks(
    tasks: list[CalendarTask],
    assistant_model: str,
    assistant_client: ModelClient,
    requestor_model: str,
    requestor_client: ModelClient,
    max_rounds: int = 100,
    max_steps_per_turn: int = 20,
    batch_size: int = 50,
    artifacts_by_task: dict[int, list[Artifact]] | None = None,
) -> list[TaskExecutionResult]:
    """Run a list of tasks in parallel batches.

    Args:
        tasks: List of CalendarTask to run
        assistant_model: Model to use for the assistant agent
        assistant_client: ModelClient for the assistant
        requestor_model: Model to use for the requestor agent
        requestor_client: ModelClient for the requestor
        max_rounds: Maximum number of conversation rounds per task
        max_steps_per_turn: Maximum tool calls per turn
        batch_size: Number of tasks to run in parallel
        artifacts_by_task: Optional dict mapping task index to artifacts list

    Returns:
        List of TaskExecutionResult for each task
    """
    executor = TaskPoolExecutor(batch_size=batch_size, task_logger=logger)
    return await executor.run(
        run_single_task(
            task_index=task_index,
            task=task,
            assistant_model=assistant_model,
            assistant_client=assistant_client,
            requestor_model=requestor_model,
            requestor_client=requestor_client,
            max_rounds=max_rounds,
            max_steps_per_turn=max_steps_per_turn,
            artifacts=artifacts_by_task.get(task_index) if artifacts_by_task else None,
        )
        for task_index, task in enumerate(tasks)
    )
