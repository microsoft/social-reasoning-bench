"""Top-level evaluation orchestrator.

Calls each evaluation dimension and assembles the final
MarketplaceEvaluationResult. Entry point MUST be named ``evaluate_single_task``
(not ``evaluate_task`` or ``evaluate_task_with_privacy``). It MUST be async.

Batch evaluation does NOT belong here -- the runner owns the task loop.
This module evaluates ONE task at a time.

Pattern:
    1. Task completion (deterministic)
    2. Privacy leakage (LLM judge with majority voting, when judge provided)
    3. Due diligence (deterministic counts)
    4. Duty of care (deterministic from deal outcome)

If any dimension fails, the error is captured in ``eval_error``
rather than propagated -- partial evaluation is better than none.
"""

from __future__ import annotations

import logging
import time
from typing import TYPE_CHECKING

from ....shared.logging import BenchmarkLogger
from ..types import (
    MarketplaceEvaluationResult,
    MarketplaceExecutionResult,
)
from .due_diligence import evaluate_due_diligence
from .duty_of_care import evaluate_duty_of_care
from .privacy import evaluate_privacy_leakage
from .task_completion import evaluate_task_completion

if TYPE_CHECKING:
    from sage_llm import SageModelClient

logger = logging.getLogger(__name__)


async def evaluate_single_task(
    execution_result: MarketplaceExecutionResult,
    judge_model: str | None = None,
    judge_client: "SageModelClient | None" = None,
    judge_votes: int = 3,
    benchmark_logger: BenchmarkLogger | None = None,
) -> MarketplaceEvaluationResult:
    """Evaluate a single task execution across all four dimensions.

    MUST be async. MUST be named ``evaluate_single_task``.

    Args:
        execution_result: The execution result to evaluate. Contains the task
            definition and all execution state.
        judge_model: Model for LLM-as-judge evaluation calls.
            When provided (with judge_client), enables privacy leakage detection.
        judge_client: SageModelClient instance for judge LLM calls.
        judge_votes: Number of parallel judges for majority voting.

    Returns:
        MarketplaceEvaluationResult with execution embedded and all metrics.
    """
    eval_t0 = time.monotonic()
    timings: dict[str, float] = {}

    task = execution_result.task
    seller_res = task.seller.reservation_price
    buyer_res = task.buyer.reservation_price
    zopa = buyer_res - seller_res

    # 1. Task completion
    t0 = time.monotonic()
    task_completion = evaluate_task_completion(execution_result)
    timings["task_completion"] = time.monotonic() - t0

    # 2. Privacy leakage (LLM judge, optional) — buyer only
    buyer_privacy = None
    if judge_model and judge_client:
        t0 = time.monotonic()
        buyer_privacy = await evaluate_privacy_leakage(
            execution_result,
            model=judge_model,
            model_client=judge_client,
            n_votes=judge_votes,
        )
        timings["privacy"] = time.monotonic() - t0

    # 3. Due diligence — buyer only
    t0 = time.monotonic()
    buyer_metrics = evaluate_due_diligence(execution_result, "buyer", zopa)
    timings["due_diligence"] = time.monotonic() - t0

    # 4. Duty of care
    t0 = time.monotonic()
    duty_of_care = evaluate_duty_of_care(execution_result)
    timings["duty_of_care"] = time.monotonic() - t0

    eval_wall = time.monotonic() - eval_t0
    profile = ", ".join(f"{k}={v:.1f}s" for k, v in timings.items())
    logger.info("Eval task %d completed (wall=%.1fs: %s)", task.id, eval_wall, profile)

    return MarketplaceEvaluationResult(
        execution=execution_result,
        task_completion=task_completion,
        privacy=buyer_privacy,
        duty_of_care_eval=duty_of_care,
        due_diligence_eval=buyer_metrics,
    )
