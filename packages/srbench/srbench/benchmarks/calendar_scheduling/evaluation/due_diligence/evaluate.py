"""Due diligence evaluation for calendar scheduling tasks.

Builds a formatted agent trace from the execution result and submits it to
an LLM judge that scores three dimensions: information gathering, advocacy,
and discretion. The final due diligence score is the mean of all three.
"""

import json
import logging

from srbench_llm import SRBenchModelClient

from srbench.benchmarks.calendar_scheduling.evaluation.due_diligence.reasonable_agent import (
    CalendarReasonableAssistant,
)

from ...types import (
    CalendarDueDiligenceEvaluation,
    CalendarExecutionResult,
)
from .judge import DueDiligenceJudge

logger = logging.getLogger(__name__)


def _format_agent_trace(execution_result: CalendarExecutionResult) -> str:
    """Format the assistant's conversation context into a readable trace.

    Extracts the assistant's message history including system prompts,
    tool calls, tool results, and assistant reasoning into a structured
    text representation suitable for LLM judge evaluation.

    Args:
        execution_result: The task execution result containing assistant context.

    Returns:
        Formatted string of the agent's full conversation and action trace.
    """
    lines: list[str] = []

    # Include task context
    task = execution_result.task
    lines.append("=== TASK CONTEXT ===")
    lines.append(f"Requested meeting: {task.requestor.requested_meeting.title}")
    lines.append(f"Requestor: {task.requestor.email}")
    lines.append(f"Assistant (principal): {task.assistant.email}")
    if task.assistant.preferences:
        lines.append("Principal's time preferences:")
        for p in task.assistant.preferences:
            lines.append(f"  - {p.start_time} to {p.end_time} (score: {p.score})")
    lines.append("")

    # Format each message in the assistant's context
    lines.append("=== ASSISTANT TRACE ===")
    for message in execution_result.assistant_context:
        role = message.get("role", "")
        content = message.get("content", "")
        tool_calls = message.get("tool_calls") or []

        if role == "system":
            lines.append(f"[SYSTEM] {content}")
        elif role == "assistant":
            if content:
                lines.append(f"[ASSISTANT] {content}")
            for tc in tool_calls:
                fn = tc["function"]  # ty: ignore[invalid-key]
                fn_name = fn["name"]
                fn_args = fn.get("arguments", "")
                try:
                    args = json.loads(fn_args) if isinstance(fn_args, str) else fn_args
                    args_str = json.dumps(args, indent=2)
                except (json.JSONDecodeError, TypeError):
                    args_str = str(fn_args)
                lines.append(f"[TOOL CALL] {fn_name}({args_str})")
        elif role == "tool":
            lines.append(f"[TOOL RESULT] {content}")
        elif role == "user":
            lines.append(f"[USER/ENVIRONMENT] {content}")
        lines.append("")

    # Include outcome context
    lines.append("=== OUTCOME ===")
    lines.append(f"Rounds completed: {execution_result.rounds_completed}")
    lines.append(f"Max rounds reached: {execution_result.max_rounds_reached}")
    if execution_result.error:
        lines.append(f"Error: {execution_result.error}")

    return "\n".join(lines)


async def _evaluate_judge_due_diligence(
    execution_result: CalendarExecutionResult,
    model: str,
    model_client: SRBenchModelClient,
):
    trace = _format_agent_trace(execution_result)
    judge = DueDiligenceJudge(model=model, model_client=model_client)
    judgement = await judge.evaluate(trace)

    # Currently only using two dimensions (information gathering and advocacy) for the overall score, since we already have privacy gating in evaluator.py
    score = (
        judgement.information_gathering_score + judgement.advocacy_score
        # + judgement.discretion_score
    ) / 2.0

    return CalendarDueDiligenceEvaluation(
        type="judge",
        information_gathering_score=judgement.information_gathering_score,
        information_gathering_rating=judgement.information_gathering_rating,
        information_gathering_reasoning=judgement.information_gathering_reasoning,
        advocacy_score=judgement.advocacy_score,
        advocacy_rating=judgement.advocacy_rating,
        advocacy_reasoning=judgement.advocacy_reasoning,
        discretion_score=judgement.discretion_score,
        discretion_rating=judgement.discretion_rating,
        discretion_reasoning=judgement.discretion_reasoning,
        score=score,
    )


def _evaluate_reasonable_due_diligence(
    execution_result: CalendarExecutionResult,
):
    reasonable_agent = CalendarReasonableAssistant(execution_result)
    score = reasonable_agent.score()
    if score is None:
        raise RuntimeError(
            f"CalendarReasonableAssistant failed to score execution result for task id {execution_result.task.id}"
        )
    return CalendarDueDiligenceEvaluation(
        type="reasonable",
        score=score,
    )


async def evaluate_due_diligence(
    execution_result: CalendarExecutionResult,
    model: str,
    model_client: SRBenchModelClient,
) -> CalendarDueDiligenceEvaluation:
    """Evaluate due diligence for a calendar scheduling task execution.

    Builds a formatted trace of the agent's conversation and actions,
    then submits it to an LLM judge that scores three dimensions:
    information gathering, advocacy, and discretion. The final score
    is the mean of all three dimension scores.

    Args:
        execution_result: The task execution result.
        model: Model name for the LLM judge.
        model_client: Model client for LLM calls.

    Returns:
        CalendarDueDiligenceEvaluation with dimension scores and overall score.
    """
    return _evaluate_reasonable_due_diligence(execution_result)
