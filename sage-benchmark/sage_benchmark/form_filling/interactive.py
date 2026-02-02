"""Interactive mode execution for form filling benchmark using interview Q&A."""

import json
import logging
import traceback
from datetime import datetime

from sage_llm import ModelClient

from sage_benchmark.form_filling.agents.assistant import AssistantAgent
from sage_benchmark.form_filling.agents.interviewer import InterviewerAgent
from sage_benchmark.form_filling.schemas import (
    ConversationMessage,
    FormTask,
    InteractiveTaskExecutionResult,
)

logger = logging.getLogger(__name__)


# --- Context Building Functions ---


def get_form_as_string(task: FormTask) -> str:
    """Get form structure for interviewer agent.

    Args:
        task: FormTask containing form info

    Returns:
        Form description string including JSON schema
    """
    return f"""Title: {task.form_title}

Form Schema:
{json.dumps(task.form_class.model_json_schema(), indent=2)}"""


# --- Agent Initialization ---


def _initialize_agents(
    task: FormTask,
    interviewer_client: ModelClient,
    interviewer_model: str,
    assistant_client: ModelClient,
    assistant_model: str,
    prompt_type: str = "base",
    interviewer_type: str = "base",
    malicious_strategy: int | None = None,
) -> tuple[InterviewerAgent, AssistantAgent]:
    """Initialize interviewer and assistant agents for a task.

    Args:
        task: FormTask containing form and persona info
        interviewer_client: Model client for interviewer agent
        interviewer_model: Model name for interviewer
        assistant_client: Model client for assistant agent
        assistant_model: Model name for assistant
        prompt_type: Type of prompt ("base", "privacy_aware", "privacy_explained", "privacy_ci")
        interviewer_type: Type of interviewer prompt ("base" or "detail")
        malicious_strategy: If set, use malicious interviewer with this strategy index

    Returns:
        Tuple of (InterviewerAgent, AssistantAgent)
    """
    assistant = AssistantAgent(
        assistant_client, assistant_model, task.persona, task.artifacts, prompt_type
    )

    form_info = get_form_as_string(task)
    interviewer = InterviewerAgent(
        interviewer_client, interviewer_model, form_info, interviewer_type, malicious_strategy
    )

    return interviewer, assistant


# --- Conversation Loop ---


async def _run_conversation_loop(
    interviewer: InterviewerAgent,
    assistant: AssistantAgent,
    conversation: list[ConversationMessage],
    max_rounds: int,
    task_id: int,
) -> str:
    """Run the interview conversation loop.

    Returns:
        Termination reason: "interviewer_ended", "assistant_ended", or "max_rounds"
    """
    for round_num in range(max_rounds):
        print(f"[Task {task_id}] Round {round_num}")

        # 1. Interviewer's turn
        tool_name, arguments = await interviewer.generate_action()

        if tool_name == "EndInterview":
            return "interviewer_ended"
        elif tool_name == "SendMessage":
            msg = arguments["message"]
            conversation.append(
                ConversationMessage(
                    from_agent="interviewer",
                    content=msg,
                    timestamp=datetime.now(),
                    round=round_num,
                )
            )
            interviewer.add_tool_result("Message sent")
            assistant.add_new_message("interviewer", msg)

        # 2. Assistant's turn
        tool_name, arguments = await assistant.generate_action()

        if tool_name == "EndConversation":
            return "assistant_ended"
        elif tool_name == "SendMessage":
            msg = arguments["message"]
            conversation.append(
                ConversationMessage(
                    from_agent="assistant",
                    content=msg,
                    timestamp=datetime.now(),
                    round=round_num,
                )
            )
            assistant.add_tool_result("Message sent")
            interviewer.add_new_message("assistant", msg)

    return "max_rounds"


# --- Main Task Execution ---


async def run_single_task(
    task: FormTask,
    task_index: int,
    interviewer_client: ModelClient,
    interviewer_model: str,
    assistant_client: ModelClient,
    assistant_model: str,
    max_rounds: int,
    prompt_type: str = "base",
    interviewer_type: str = "base",
    malicious_strategy: int | None = None,
) -> InteractiveTaskExecutionResult:
    """Execute a single interactive interview task.

    Args:
        task: FormTask to execute
        task_index: Task index for tracking
        interviewer_client: Model client for interviewer agent
        interviewer_model: Model name for interviewer
        assistant_client: Model client for assistant agent
        assistant_model: Model name for assistant
        max_rounds: Maximum conversation rounds
        prompt_type: Type of prompt ("base", "privacy_aware", "privacy_explained", "privacy_ci")
        interviewer_type: Type of interviewer prompt ("base" or "detail")
        malicious_strategy: If set, use malicious interviewer with this strategy index

    Returns:
        InteractiveTaskExecutionResult with conversation and form submission
    """
    conversation: list[ConversationMessage] = []
    interviewer = None
    assistant = None

    # 1. INITIALIZATION
    interviewer, assistant = _initialize_agents(
        task,
        interviewer_client,
        interviewer_model,
        assistant_client,
        assistant_model,
        prompt_type,
        interviewer_type,
        malicious_strategy,
    )

    try:
        # 2. CONVERSATION
        termination_reason = await _run_conversation_loop(
            interviewer, assistant, conversation, max_rounds, task.form_id
        )

        # 3. FORM FILLING
        form_submission = await interviewer.fill_form(
            form_context=get_form_as_string(task), form_class=task.form_class
        )

        # 4. RETURN SUCCESS RESULT
        return InteractiveTaskExecutionResult(
            task_index=task_index,
            task=task,
            form_id=task.form_id,
            conversation=conversation,
            form_submission=form_submission,
            termination_reason=termination_reason,
            total_rounds=len([m for m in conversation if m.from_agent == "interviewer"]),
            success=True,
            interviewer_context=interviewer.messages,
            assistant_context=assistant.messages,
        )

    except Exception as e:
        logger.error(f"Task {task_index} failed: {e}")
        logger.error(traceback.format_exc())

        return InteractiveTaskExecutionResult(
            task_index=task_index,
            task=task,
            form_id=task.form_id,
            conversation=conversation,
            form_submission={},
            termination_reason="error",
            total_rounds=len([m for m in conversation if m.from_agent == "interviewer"]),
            success=False,
            error_message=str(e),
            interviewer_context=getattr(interviewer, "messages", []) if interviewer else [],
            assistant_context=getattr(assistant, "messages", []) if assistant else [],
        )
