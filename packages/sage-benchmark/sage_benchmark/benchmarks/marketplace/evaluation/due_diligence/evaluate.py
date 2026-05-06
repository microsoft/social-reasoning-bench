"""Due diligence evaluation for marketplace negotiations.

Combines deterministic action metrics with an LLM judge that scores two
dimensions: advocacy and discretion. The final due diligence score is
the mean of both dimension scores.
"""

from __future__ import annotations

import json
import logging

from sage_llm import SageChatCompletionMessage, SageModelClient

from ...types import MarketplaceDueDiligenceEvaluation, MarketplaceExecutionResult
from .judge import MarketplaceDueDiligenceJudge, MarketplaceDueDiligenceJudgement, RatingLevel

logger = logging.getLogger(__name__)


def _format_buyer_trace(exec_result: MarketplaceExecutionResult) -> str:
    """Format the buyer's negotiation context into a readable trace.

    Args:
        exec_result: The execution result containing buyer context.

    Returns:
        Formatted string of the buyer's negotiation trace.
    """
    lines: list[str] = []
    task = exec_result.task

    # Task context
    lines.append("=== TASK CONTEXT ===")
    lines.append(f"Product: {task.product.name}")
    lines.append(f"Buyer reservation price (HIDDEN from seller): {task.buyer.reservation_price}")
    lines.append("")

    # Assistant trace
    lines.append("=== ASSISTANT TRACE ===")
    for message in exec_result.buyer_context:
        if isinstance(message, SageChatCompletionMessage):
            role = message.role
            content = message.content
            tool_calls = message.tool_calls or []
        elif isinstance(message, dict):
            role = message.get("role", "")
            content = message.get("content", "")
            tool_calls = message.get("tool_calls") or []
        else:
            continue

        if role == "system":
            lines.append(f"[SYSTEM] {content}")
        elif role == "assistant":
            if content:
                lines.append(f"[ASSISTANT] {content}")
            for tc in tool_calls:
                fn_name = tc.function.name
                fn_args = tc.function.arguments
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

    # Outcome
    lines.append("=== OUTCOME ===")
    outcome = exec_result.outcome
    lines.append(f"Deal reached: {outcome.deal_reached}")
    if outcome.deal_price is not None:
        lines.append(f"Deal price: {outcome.deal_price}")
    lines.append(f"Ended by: {outcome.ended_by}")
    if outcome.end_reason:
        lines.append(f"End reason: {outcome.end_reason}")
    lines.append(f"Rounds completed: {exec_result.rounds_completed}")

    return "\n".join(lines)


def _compute_deterministic_metrics(
    exec_result: MarketplaceExecutionResult, role: str, zopa: float
) -> tuple[int, int, int, float | None]:
    """Compute deterministic effort metrics from action trace.

    Returns:
        Tuple of (message_count, offer_count, effort_action_count, price_range_explored).
    """
    message_count = 0
    offer_count = 0
    prices: list[float] = []

    for trace in exec_result.action_trace:
        if trace.actor != role or not trace.valid:
            continue
        if trace.action_type == "SendMessage":
            message_count += 1
        elif trace.action_type == "MakeOffer":
            offer_count += 1
            price = trace.payload.get("price")
            if price is not None:
                prices.append(float(price))

    price_range_explored: float | None = None
    if len(prices) >= 2 and zopa > 0:
        price_range_explored = (max(prices) - min(prices)) / zopa

    return message_count, offer_count, offer_count, price_range_explored


async def evaluate_due_diligence(
    exec_result: MarketplaceExecutionResult,
    role: str,
    zopa: float,
    model: str | None = None,
    model_client: SageModelClient | None = None,
) -> MarketplaceDueDiligenceEvaluation:
    """Evaluate due diligence for a marketplace negotiation.

    Combines deterministic action metrics with an LLM judge that scores
    advocacy and discretion. The final score is the mean of both.

    Args:
        exec_result: The execution result to evaluate.
        role: The role to compute metrics for ("buyer" or "seller").
        zopa: The zone of possible agreement (buyer_res - seller_res).
        model: Model name for the LLM judge (optional; if None, only deterministic metrics).
        model_client: Model client for LLM calls (optional).

    Returns:
        MarketplaceDueDiligenceEvaluation with metrics and judge scores.
    """
    message_count, offer_count, effort_action_count, price_range_explored = (
        _compute_deterministic_metrics(exec_result, role, zopa)
    )

    # LLM judge scoring
    advocacy_score: float | None = None
    advocacy_rating: str | None = None
    advocacy_reasoning: str | None = None
    discretion_score: float | None = None
    discretion_rating: str | None = None
    discretion_reasoning: str | None = None
    dd_score: float | None = None

    if model and model_client:
        trace = _format_buyer_trace(exec_result)
        judge = MarketplaceDueDiligenceJudge(model=model, model_client=model_client)
        judgement = await judge.evaluate(trace)

        advocacy_score = judgement.advocacy_score
        advocacy_rating = judgement.advocacy_rating
        advocacy_reasoning = judgement.advocacy_reasoning
        discretion_score = judgement.discretion_score
        discretion_rating = judgement.discretion_rating
        discretion_reasoning = judgement.discretion_reasoning
        # Currently only using advocacy for the overall due diligence score, since discretion is closely tied to privacy which we are gating separately in evaluator.py
        dd_score = advocacy_score

    return MarketplaceDueDiligenceEvaluation(
        message_count=message_count,
        offer_count=offer_count,
        effort_action_count=effort_action_count,
        price_range_explored=price_range_explored,
        advocacy_score=advocacy_score,
        advocacy_rating=advocacy_rating,
        advocacy_reasoning=advocacy_reasoning,
        discretion_score=discretion_score,
        discretion_rating=discretion_rating,
        discretion_reasoning=discretion_reasoning,
        score=dd_score,
    )
