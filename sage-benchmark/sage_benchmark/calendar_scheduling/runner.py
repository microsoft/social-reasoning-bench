from openai import OpenAI
from pydantic_core import to_json

from .agents.assistant import CalendarAssistantAgent, EndConversation
from .agents.requestor import CalendarRequestorAgent
from .environments.calendar import CALENDAR_EVENT_PUBLIC_FIELDS, Calendar, CalendarAction
from .environments.messenger import Message, Messenger
from .environments.messenger.actions import SendMessage
from .types import CalendarEvent, CalendarTask, TaskExecutionResult, Tool


def execute_requestor_tool_call(
    tool_call: Tool, messenger: Messenger, requestor_name: str, assistant_name: str
):
    if isinstance(tool_call, SendMessage):
        messenger.send_message(
            Message(to=assistant_name, from_=requestor_name, message=tool_call.message)
        )
        return "Success"
    else:
        raise ValueError(f"Unrecognized tool call {tool_call}")


def execute_assistant_tool_call(
    tool_call: Tool,
    messenger: Messenger,
    calendar: Calendar,
    assistant_name: str,
    requestor_name: str,
):
    if isinstance(tool_call, SendMessage):
        messenger.send_message(
            Message(to=requestor_name, from_=assistant_name, message=tool_call.message)
        )
        return "Success"
    elif isinstance(tool_call, CalendarAction):
        return to_json(calendar.execute(tool_call)).decode()
    elif isinstance(tool_call, EndConversation):
        return "Success"
    else:
        raise ValueError(f"Unrecognized tool call {tool_call}")


def run_single_task(
    task_index: int,
    task: CalendarTask,
    assistant_model: str,
    assistant_client: OpenAI,
    requestor_model: str,
    requestor_client: OpenAI,
    max_rounds=100,
):
    # Get agent names from task
    assistant_name = task.assistant.email
    requestor_name = task.requestor.email

    # Setup the environment
    # Downcast LabeledCalendarEvent to CalendarEvent to hide label fields from agents
    assistant_calendar = Calendar(
        [
            CalendarEvent.model_validate(event.model_dump(include=CALENDAR_EVENT_PUBLIC_FIELDS))
            for event in task.assistant.calendar
        ]
    )
    messenger = Messenger()

    # Initialize the agents
    assistant_agent = CalendarAssistantAgent(
        model=assistant_model,
        model_client=assistant_client,
        assistant=task.assistant,
        allowed_contacts=[task.requestor.email],
    )

    requestor_agent = CalendarRequestorAgent(
        model=requestor_model,
        model_client=requestor_client,
        requestor=task.requestor,
        allowed_contacts=[task.assistant.email],
    )

    # Begin the simulation

    # Generate the first action from the requestor
    requestor_tool_call = requestor_agent.generate_tool_call()
    # Execute the action in the "environment" (just the messenger for the requestor)
    requestor_tool_call_result = execute_requestor_tool_call(
        requestor_tool_call, messenger, requestor_name, assistant_name
    )
    # Update the requestor with the action result
    requestor_agent.add_tool_call_result(requestor_tool_call_result)

    for round_idx in range(max_rounds):
        print(f"Round {round_idx + 1}")
        # Get any new messages to the assistant
        new_messages_to_assistant = [
            message.model_dump(include={"from_", "message"})
            for message in messenger.get_unread_messages(assistant_name)
        ]
        if new_messages_to_assistant:
            # Add the new messages to the assistant (simulates a tool call round in the assistant context)
            assistant_agent.add_new_messages(new_messages_to_assistant)

        # Get the next action for the assistant
        assistant_tool_call = assistant_agent.generate_tool_call()
        # Execute the action in the environment (messenger + calendar)
        assistant_tool_call_result = execute_assistant_tool_call(
            assistant_tool_call, messenger, assistant_calendar, assistant_name, requestor_name
        )
        # Update the assistant with the action result
        assistant_agent.add_tool_call_result(assistant_tool_call_result)

        # If the assistant refuses to schedule the event, exit
        if isinstance(assistant_tool_call, EndConversation):
            break
        # Only invoke the requestor once the assistant sends a new message
        # Because the requestor has to wait for new messages before it can do anything
        elif isinstance(assistant_tool_call, SendMessage):
            new_messages_to_requestor = [
                message.model_dump(include={"from_", "message"})
                for message in messenger.get_unread_messages(requestor_name)
            ]
            requestor_agent.add_new_messages(new_messages_to_requestor)
            requestor_tool_call = requestor_agent.generate_tool_call()
            requestor_tool_call_result = execute_requestor_tool_call(
                requestor_tool_call, messenger, requestor_name, assistant_name
            )
            requestor_agent.add_tool_call_result(requestor_tool_call_result)

    return TaskExecutionResult(
        task_index=task_index,
        task=task,
        messages=list(messenger._messages),
        final_assistant_calendar=list(assistant_calendar._events.values()),
        assistant_context=list(assistant_agent._messages),
        requestor_context=list(requestor_agent._messages),
    )


def run_tasks(
    tasks: list[CalendarTask],
    assistant_model: str,
    assistant_client: OpenAI,
    requestor_model: str,
    requestor_client: OpenAI,
    max_rounds: int = 100,
) -> list[TaskExecutionResult]:
    """Run a list of tasks.

    Args:
        tasks: List of CalendarTask to run.
        assistant_model: Model to use for the assistant agent.
        assistant_client: OpenAI client for the assistant.
        requestor_model: Model to use for the requestor agent.
        requestor_client: OpenAI client for the requestor.
        max_rounds: Maximum number of conversation rounds per task.

    Returns:
        List of TaskExecutionResult for each task.
    """
    results: list[TaskExecutionResult] = []
    for index, task in enumerate(tasks):
        print(f"\n{'=' * 60}")
        print(f"Task {index}")
        print(f"{'=' * 60}")
        result = run_single_task(
            task_index=index,
            task=task,
            assistant_model=assistant_model,
            assistant_client=assistant_client,
            requestor_model=requestor_model,
            requestor_client=requestor_client,
            max_rounds=max_rounds,
        )
        results.append(result)

    return results
