"""Interactive mode execution for form filling benchmark using interview Q&A."""

import json
import logging
import traceback
from datetime import datetime

from sage_llm import ModelClient

from sage_benchmark.form_filling.agents.assistant import AssistantAgent
from sage_benchmark.form_filling.agents.interviewer import InterviewerAgent
from sage_benchmark.form_filling.environment.actions import (
    EndConversation,
    ReadFile,
    SearchFiles,
    SendMessage,
    Wait,
)
from sage_benchmark.form_filling.environment.bm25_index import BM25Index
from sage_benchmark.form_filling.schemas import (
    ConversationMessage,
    FormTask,
    InteractiveTaskExecutionResult,
)
from sage_benchmark.shared.errors import is_fatal_error

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
    malicious_attack_type: str = "privacy",
    malicious_strategies_file: str | None = None,
    temperature: float | None = None,
    form_fill_client: ModelClient | None = None,
    form_fill_model: str | None = None,
    explicit_cot: bool = False,
) -> tuple[InterviewerAgent, AssistantAgent]:
    """Initialize interviewer and assistant agents for a task.

    Args:
        task: FormTask containing form and persona info
        interviewer_client: Model client for interviewer agent
        interviewer_model: Model name for interviewer
        assistant_client: Model client for assistant agent
        assistant_model: Model name for assistant
        prompt_type: Privacy level ("none", "simple", "strong", "ci")
        interviewer_type: Type of interviewer prompt ("base" or "detail")
        single_field_mode: If True, interviewer asks only one question per turn
        malicious_strategy: If set, use malicious interviewer with this strategy index
        malicious_attack_type: Type of malicious attack ("privacy", "hallucination", "red_flags")
        malicious_strategies_file: Path to strategies YAML file for malicious mode
        temperature: Sampling temperature for assistant generation
        form_fill_client: Separate client for form filling (defaults to interviewer client)
        form_fill_model: Separate model for form filling (defaults to interviewer model)
        explicit_cot: If True, enable explicit chain-of-thought prompting for assistant

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
        explicit_cot=explicit_cot,
    )

    form_info = get_form_as_string(task)
    interviewer = InterviewerAgent(
        interviewer_client,
        interviewer_model,
        form_info,
        interviewer_type,
        single_field_mode,
        malicious_strategy,
        malicious_attack_type=malicious_attack_type,
        malicious_strategies_file=malicious_strategies_file,
        form_fill_client=form_fill_client,
        form_fill_model=form_fill_model,
    )

    return interviewer, assistant


# --- Conversation Loop ---


async def _run_conversation_loop(
    interviewer: InterviewerAgent,
    assistant: AssistantAgent,
    conversation: list[ConversationMessage],
    max_rounds: int,
    task_id: int,
    bm25_index: BM25Index | None = None,
    max_steps_per_turn: int = 5,
) -> str:
    """Run the interview conversation loop.

    Follows the calendar/marketplace runner pattern: each round gives the
    interviewer one turn, then the assistant a multi-step turn.  The
    assistant may use SearchFiles/ReadFile (handled inline via BM25) or
    Wait/SendMessage (which end its turn) within ``max_steps_per_turn``
    steps.

    Args:
        interviewer: Interviewer agent
        assistant: Assistant agent
        conversation: Conversation message list (mutated in place)
        max_rounds: Maximum conversation rounds
        task_id: Task ID for logging
        bm25_index: BM25 index for executing file-system tool calls
        max_steps_per_turn: Maximum tool calls per assistant turn (default: 5)

    Returns:
        Termination reason: "interviewer_ended", "assistant_ended", or "max_rounds"
    """
    for round_num in range(max_rounds):
        logger.info("[Task %s] Round %d", task_id, round_num)

        # --- Interviewer turn ---
        tool_name, arguments = await interviewer.generate_action()

        if tool_name == "EndInterview":
            return "interviewer_ended"

        if tool_name == "SendMessage":
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
            assistant.add_new_messages("interviewer", msg)

        # --- Assistant turn (multi-step) ---
        for _step in range(max_steps_per_turn):
            tool = await assistant.generate_tool_call()

            if isinstance(tool, (SearchFiles, ReadFile)) and bm25_index is not None:
                result = bm25_index.execute_tool(tool.get_name(), tool.model_dump())
                assistant.add_tool_call_result(result)
                continue  # let agent make another call

            if isinstance(tool, Wait):
                # Yield turn back to interviewer
                assistant.add_tool_call_result("Waiting for the other party.")
                break

            if isinstance(tool, SendMessage):
                msg = tool.message
                conversation.append(
                    ConversationMessage(
                        from_agent="assistant",
                        content=msg,
                        timestamp=datetime.now(),
                        round=round_num,
                    )
                )
                assistant.add_tool_call_result("Message sent")
                interviewer.add_new_message("assistant", msg)
                break

            if isinstance(tool, EndConversation):
                return "assistant_ended"

            # AskUser or unexpected tool -- add result and continue
            assistant.add_tool_call_result("Tool executed")
            break

        # If max_steps reached without Wait/SendMessage, continue to next round

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
    malicious_attack_type: str = "privacy",
    malicious_strategies_file: str | None = None,
    temperature: float | None = None,
    form_fill_client: ModelClient | None = None,
    form_fill_model: str | None = None,
    max_steps_per_turn: int = 5,
    explicit_cot: bool = False,
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
        prompt_type: Privacy level ("none", "simple", "strong", "ci")
        interviewer_type: Type of interviewer prompt ("base" or "detail")
        single_field_mode: If True, interviewer asks only one question per turn
        malicious_strategy: If set, use malicious interviewer with this strategy index
        malicious_attack_type: Type of malicious attack ("privacy", "hallucination", "red_flags")
        malicious_strategies_file: Path to strategies YAML file for malicious mode
        temperature: Sampling temperature for assistant generation
        max_steps_per_turn: Maximum tool calls per assistant turn (default: 5)
        explicit_cot: If True, enable explicit chain-of-thought prompting for assistant

    Returns:
        InteractiveTaskExecutionResult with conversation and form submission
    """
    conversation: list[ConversationMessage] = []
    interviewer = None
    assistant = None

    # Initialize BM25 index for file-system mode
    bm25_index: BM25Index | None = None
    if task.filesystem_artifacts:
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
        malicious_attack_type=malicious_attack_type,
        malicious_strategies_file=malicious_strategies_file,
        temperature=temperature,
        form_fill_client=form_fill_client,
        form_fill_model=form_fill_model,
        explicit_cot=explicit_cot,
    )

    try:
        # 2. CONVERSATION
        termination_reason = await _run_conversation_loop(
            interviewer,
            assistant,
            conversation,
            max_rounds,
            task.form_id,
            bm25_index=bm25_index,
            max_steps_per_turn=max_steps_per_turn,
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
        if is_fatal_error(e):
            raise
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
