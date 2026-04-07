"""Canonical execution entry point for form-filling benchmark.

Exposes ``execute_task`` as the public API for running a single form-filling
task.  All execution logic (agent initialisation, conversation loop, form
filling) lives here so that the module is self-contained::

    from .executor import execute_task

Legacy aliases ``run_single_task`` and ``run_interactive_task`` are kept for
backward compatibility.
"""

from __future__ import annotations

import json
import traceback
from datetime import datetime

from sage_llm import SageModelClient

from ...shared.errors import is_fatal_error
from ...shared.logging import BenchmarkLogger
from .agents.assistant import AssistantAgent
from .agents.interviewer import InterviewerAgent
from .agents.interviewer import SendMessage as InterviewerSendMessage
from .environment.actions import (
    EndConversation,
    ReadFile,
    SearchFiles,
    SendMessage,
    Wait,
)
from .environment.bm25_index import BM25Index
from .types import (
    ConversationMessage,
    FormFillingExecutionResult,
    FormTask,
)
from .utils import load_form_class

# --- Context Building Functions ---


def get_form_as_string(task: FormTask) -> str:
    """Get form structure for interviewer agent.

    Args:
        task: FormTask containing form info

    Returns:
        Form description string including JSON schema
    """
    form_class = load_form_class(task.form_model_path)
    return f"""Title: {task.form_info.title}

Form Schema:
{json.dumps(form_class.model_json_schema(), indent=2)}"""


# --- Agent Initialization ---


def _initialize_agents(
    task: FormTask,
    interviewer_client: SageModelClient,
    interviewer_model: str,
    assistant_client: SageModelClient,
    assistant_model: str,
    privacy_prompt: str = "none",
    single_field_mode: bool = False,
    temperature: float | None = None,
    form_fill_client: SageModelClient | None = None,
    form_fill_model: str | None = None,
    assistant_explicit_cot: bool = False,
    interviewer_explicit_cot: bool = False,
) -> tuple[InterviewerAgent, AssistantAgent]:
    """Initialize interviewer and assistant agents for a task.

    Args:
        task: FormTask containing form and persona info
        interviewer_client: Model client for interviewer agent
        interviewer_model: Model name for interviewer
        assistant_client: Model client for assistant agent
        assistant_model: Model name for assistant
        privacy_prompt: Privacy level ("none", "simple", "strong", "ci")
        single_field_mode: If True, interviewer asks only one question per turn
        temperature: Sampling temperature for assistant generation
        form_fill_client: Separate client for form filling (currently unused)
        form_fill_model: Separate model for form filling (currently unused)
        assistant_explicit_cot: If True, enable explicit chain-of-thought for assistant
        interviewer_explicit_cot: If True, enable explicit chain-of-thought for interviewer

    Returns:
        Tuple of (InterviewerAgent, AssistantAgent)
    """
    assistant = AssistantAgent(
        assistant_client,
        assistant_model,
        task.persona,
        task.artifacts,
        privacy_prompt,
        temperature=temperature,
        explicit_cot=assistant_explicit_cot,
    )

    form_class = load_form_class(task.form_model_path)
    form_info = f"""Title: {task.form_info.title}

Form Schema:
{json.dumps(form_class.model_json_schema(), indent=2)}"""
    interviewer = InterviewerAgent(
        client=interviewer_client,
        model=interviewer_model,
        form_context=form_info,
        form_class=form_class,
        instruction_message=task.instruction_message,
        single_field_mode=single_field_mode,
        explicit_cot=interviewer_explicit_cot,
        malicious_prompt=task.malicious_prompt,
    )

    return interviewer, assistant


# --- Per-turn step functions ---


async def _run_interviewer_turn(
    interviewer: InterviewerAgent,
    assistant: AssistantAgent,
    conversation: list[ConversationMessage],
    round_num: int,
    max_steps_per_turn: int,
) -> tuple[str, dict | None]:
    """Run one interviewer turn (up to max_steps_per_turn steps).

    Each step makes one LLM call. SubmitForm with unfilled fields is
    rejected (feedback appended) and the step is consumed. SendMessage
    ends the turn and hands control to the assistant.

    Args:
        interviewer: The interviewer agent instance.
        assistant: The assistant agent instance.
        conversation: Mutable list of conversation messages to append to.
        round_num: Current conversation round number.
        max_steps_per_turn: Maximum number of LLM calls per turn.

    Returns:
        ("form_submitted", arguments) if the form was accepted.
        ("continue", None) if a SendMessage was sent (assistant's turn next).
        ("max_steps", None) if the step limit was hit without progress.
    """
    for _step in range(max_steps_per_turn):
        tool = await interviewer.generate_tool_call()

        if tool.get_name() == "SubmitForm":
            submission = tool.model_dump()
            unfilled = interviewer._get_unfilled_fields(submission)
            if unfilled:
                interviewer.add_tool_call_result(
                    f"These fields are still empty: {', '.join(unfilled)}. "
                    f"Please ask about them before submitting."
                )
                continue
            return "form_submitted", submission

        if isinstance(tool, InterviewerSendMessage):
            msg = tool.message
            conversation.append(
                ConversationMessage(
                    from_agent="interviewer",
                    content=msg,
                    timestamp=datetime.now(),
                    round=round_num,
                )
            )
            interviewer.add_tool_call_result("Message sent")
            assistant.add_new_messages("interviewer", msg)
            return "continue", None

    return "max_steps", None


async def _run_assistant_turn(
    interviewer: InterviewerAgent,
    assistant: AssistantAgent,
    conversation: list[ConversationMessage],
    round_num: int,
    max_steps_per_turn: int,
    bm25_index: BM25Index | None = None,
) -> tuple[str, None]:
    """Run one assistant turn (up to max_steps_per_turn steps).

    Args:
        interviewer: The interviewer agent instance.
        assistant: The assistant agent instance.
        conversation: Mutable list of conversation messages to append to.
        round_num: Current conversation round number.
        max_steps_per_turn: Maximum number of LLM calls per turn.
        bm25_index: Optional BM25Index for file-system tool execution.

    Returns:
        ("assistant_ended", None) if the assistant called EndConversation.
        ("continue", None) otherwise.
    """
    for _step in range(max_steps_per_turn):
        tool = await assistant.generate_tool_call()

        if isinstance(tool, (SearchFiles, ReadFile)) and bm25_index is not None:
            result = bm25_index.execute_tool(tool.get_name(), tool.model_dump())
            assistant.add_tool_call_result(result)
            continue

        if isinstance(tool, Wait):
            assistant.add_tool_call_result("Waiting for the other party.")
            return "continue", None

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
            return "continue", None

        if isinstance(tool, EndConversation):
            return "assistant_ended", None

        # Unexpected tool
        assistant.add_tool_call_result("Tool executed")
        return "continue", None

    return "continue", None


# --- Conversation Loop ---


async def _run_conversation_loop(
    interviewer: InterviewerAgent,
    assistant: AssistantAgent,
    conversation: list[ConversationMessage],
    max_rounds: int,
    task_id: int,
    benchmark_logger: BenchmarkLogger,
    bm25_index: BM25Index | None = None,
    max_steps_per_turn: int = 5,
) -> tuple[str, dict | None]:
    """Run the interview conversation loop.

    Each round gives the interviewer a multi-step turn, then the assistant
    a multi-step turn, both bounded by ``max_steps_per_turn``.

    Args:
        interviewer: The interviewer agent instance.
        assistant: The assistant agent instance.
        conversation: Mutable list of conversation messages to append to.
        max_rounds: Maximum number of conversation rounds.
        task_id: Task identifier for logging.
        benchmark_logger: Logger for structured benchmark output.
        bm25_index: Optional BM25Index for file-system tool execution.
        max_steps_per_turn: Maximum tool calls per agent turn.

    Returns:
        Tuple of (termination_reason, form_submission).
        termination_reason: "form_submitted", "assistant_ended", or "max_rounds"
        form_submission: dict if form was submitted, None otherwise
    """
    for round_num in range(max_rounds):
        benchmark_logger.info("[Task %s] Round %d", task_id, round_num)

        reason, submission = await _run_interviewer_turn(
            interviewer,
            assistant,
            conversation,
            round_num,
            max_steps_per_turn,
        )
        if reason == "form_submitted":
            return "form_submitted", submission

        reason, _ = await _run_assistant_turn(
            interviewer,
            assistant,
            conversation,
            round_num,
            max_steps_per_turn,
            bm25_index,
        )
        if reason == "assistant_ended":
            return "assistant_ended", None

    return "max_rounds", None


# --- Main Task Execution ---


async def execute_task(
    task: FormTask,
    task_index: int,
    interviewer_client: SageModelClient,
    interviewer_model: str,
    assistant_client: SageModelClient,
    assistant_model: str,
    max_rounds: int,
    benchmark_logger: BenchmarkLogger,
    privacy_prompt: str = "none",
    single_field_mode: bool = False,
    temperature: float | None = None,
    form_fill_client: SageModelClient | None = None,
    form_fill_model: str | None = None,
    max_steps_per_turn: int = 5,
    assistant_explicit_cot: bool = False,
    interviewer_explicit_cot: bool = False,
) -> FormFillingExecutionResult:
    """Execute a single interactive interview task.

    This is the canonical execution entry point for the form-filling benchmark.

    Args:
        task: FormTask to execute
        task_index: Task index for tracking
        interviewer_client: Model client for interviewer agent
        interviewer_model: Model name for interviewer
        assistant_client: Model client for assistant agent
        assistant_model: Model name for assistant
        max_rounds: Maximum conversation rounds
        benchmark_logger: BenchmarkLogger for structured logging
        privacy_prompt: Privacy level ("none", "simple", "strong", "ci")
        single_field_mode: If True, interviewer asks only one question per turn
        temperature: Sampling temperature for assistant generation
        form_fill_client: Separate client for form filling (currently unused)
        form_fill_model: Separate model for form filling (currently unused)
        max_steps_per_turn: Maximum tool calls per assistant turn (default: 5)
        assistant_explicit_cot: If True, enable explicit chain-of-thought for assistant
        interviewer_explicit_cot: If True, enable explicit chain-of-thought for interviewer

    Returns:
        FormFillingExecutionResult with conversation and form submission
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
        privacy_prompt,
        single_field_mode,
        temperature=temperature,
        form_fill_client=form_fill_client,
        form_fill_model=form_fill_model,
        assistant_explicit_cot=assistant_explicit_cot,
        interviewer_explicit_cot=interviewer_explicit_cot,
    )

    try:
        # 2. CONVERSATION + FORM SUBMISSION (SubmitForm ends the interview)
        termination_reason, form_submission = await _run_conversation_loop(
            interviewer,
            assistant,
            conversation,
            max_rounds,
            task.id,
            benchmark_logger=benchmark_logger,
            bm25_index=bm25_index,
            max_steps_per_turn=max_steps_per_turn,
        )

        # 3. RETURN RESULT
        return FormFillingExecutionResult(
            task_index=task_index,
            task=task,
            conversation=conversation,
            form_submission=form_submission or {},
            termination_reason=termination_reason,  # ty:ignore[invalid-argument-type]
            total_rounds=len([m for m in conversation if m.from_agent == "interviewer"]),
            success=termination_reason != "error",
            interviewer_context=interviewer.messages,
            assistant_context=assistant.messages,
        )

    except Exception as e:
        if is_fatal_error(e):
            raise
        benchmark_logger.error(f"Task {task_index} failed: {e}")
        benchmark_logger.error(traceback.format_exc())

        return FormFillingExecutionResult(
            task_index=task_index,
            task=task,
            conversation=conversation,
            form_submission={},
            termination_reason="error",
            total_rounds=len([m for m in conversation if m.from_agent == "interviewer"]),
            success=False,
            error_message=str(e),
            error=str(e),
            interviewer_context=getattr(interviewer, "messages", []) if interviewer else [],
            assistant_context=getattr(assistant, "messages", []) if assistant else [],
        )


# Backward-compatible aliases
run_single_task = execute_task
run_interactive_task = execute_task

__all__ = [
    "execute_task",
    "run_single_task",
    "run_interactive_task",
    "get_form_as_string",
]
