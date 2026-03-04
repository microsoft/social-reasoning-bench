"""Interactive mode execution for form filling benchmark using interview Q&A."""

import json
import logging
import traceback
from datetime import datetime

from sage_llm import ModelClient

from sage_benchmark.form_filling.agents.assistant import AssistantAgent
from sage_benchmark.form_filling.agents.interviewer import InterviewerAgent
from sage_benchmark.form_filling.agents.oracle_user import OracleUser
from sage_benchmark.form_filling.environment.bm25_index import BM25Index
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
    single_field_mode: bool = False,
    malicious_strategy: int | None = None,
    temperature: float | None = None,
    file_system: bool = False,
    bm25_index: BM25Index | None = None,
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
        single_field_mode: If True, interviewer asks only one question per turn
        malicious_strategy: If set, use malicious interviewer with this strategy index
        temperature: Sampling temperature for assistant generation
        file_system: If True, add file-system search/read tools to assistant
        bm25_index: BM25 index for file-system tool execution

    Returns:
        Tuple of (InterviewerAgent, AssistantAgent)
    """
    assistant = AssistantAgent(
        assistant_client,
        assistant_model,
        task.persona,
        task.artifacts,
        prompt_type,
        temperature=temperature,
        file_system=file_system,
        bm25_index=bm25_index,
    )

    form_info = get_form_as_string(task)
    interviewer = InterviewerAgent(
        interviewer_client,
        interviewer_model,
        form_info,
        interviewer_type,
        single_field_mode,
        malicious_strategy,
    )

    return interviewer, assistant


# --- Conversation Loop ---


async def _run_conversation_loop(
    interviewer: InterviewerAgent,
    assistant: AssistantAgent,
    oracle_user: OracleUser,
    conversation: list[ConversationMessage],
    max_rounds: int,
    task_id: int,
    max_ask_rounds: int = 50,
    user_qa_history: list[dict[str, str]] | None = None,
) -> str:
    """Run the interview conversation loop.

    Args:
        interviewer: Interviewer agent
        assistant: Assistant agent
        oracle_user: Oracle user for answering ask_user questions
        conversation: Conversation message list (mutated in place)
        max_rounds: Maximum conversation rounds
        task_id: Task ID for logging
        max_ask_rounds: Maximum number of ask_user rounds
        user_qa_history: List to track ask_user Q&A exchanges (mutated in place)

    Returns:
        Termination reason: "interviewer_ended", "assistant_ended", or "max_rounds"
    """
    if user_qa_history is None:
        user_qa_history = []
    ask_user_count = 0

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

        # 2. Assistant's turn (may include multiple AskUser calls before responding)
        while True:
            tool_name, arguments = await assistant.generate_action()

            if tool_name == "AskUser":
                # Side channel: ask oracle user, don't send to interviewer
                question = arguments.get("question", "")
                ask_user_count += 1
                print(f"[Task {task_id}] AskUser #{ask_user_count}: {question[:80]}...")

                if ask_user_count > max_ask_rounds:
                    print(f"[Task {task_id}] Max ask_user rounds reached ({max_ask_rounds})")
                    assistant.add_tool_result(
                        "You have reached the maximum number of questions you can ask the user."
                    )
                    break

                user_answer = await oracle_user.answer_question(question)
                print(f"[Task {task_id}] User answers: {user_answer[:80]}...")
                user_qa_history.append({"question": question, "answer": user_answer})
                assistant.add_tool_result(user_answer)
                continue  # Let assistant generate another action

            elif tool_name == "EndConversation":
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
                break  # Done with assistant's turn
            else:
                break  # Unknown tool, move on

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
    single_field_mode: bool = False,
    malicious_strategy: int | None = None,
    temperature: float | None = None,
    oracle_user: OracleUser | None = None,
    max_ask_rounds: int = 50,
    file_system: bool = False,
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
        single_field_mode: If True, interviewer asks only one question per turn
        malicious_strategy: If set, use malicious interviewer with this strategy index
        temperature: Sampling temperature for assistant generation
        oracle_user: Oracle user for answering ask_user questions
        max_ask_rounds: Maximum number of ask_user rounds (default: 50)
        file_system: If True, use file-system mode with search/read tools

    Returns:
        InteractiveTaskExecutionResult with conversation and form submission
    """
    conversation: list[ConversationMessage] = []
    user_qa_history: list[dict[str, str]] = []
    interviewer = None
    assistant = None

    # Initialize BM25 index for file-system mode
    bm25_index: BM25Index | None = None
    if file_system and task.filesystem_artifacts:
        bm25_index = BM25Index([a.model_dump() for a in task.filesystem_artifacts])

    # 1. INITIALIZATION
    interviewer, assistant = _initialize_agents(
        task,
        interviewer_client,
        interviewer_model,
        assistant_client,
        assistant_model,
        prompt_type,
        interviewer_type,
        single_field_mode,
        malicious_strategy,
        temperature=temperature,
        file_system=file_system,
        bm25_index=bm25_index,
    )

    try:
        # 2. CONVERSATION
        termination_reason = await _run_conversation_loop(
            interviewer,
            assistant,
            oracle_user,
            conversation,
            max_rounds,
            task.form_id,
            max_ask_rounds=max_ask_rounds,
            user_qa_history=user_qa_history,
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
            user_qa_history=user_qa_history,
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
            user_qa_history=user_qa_history,
        )
