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
from .outcome_optimality import evaluate_outcome_optimality
from .privacy import evaluate_privacy_leakage
from .task_completion import evaluate_task_completion

if TYPE_CHECKING:
    from srbench_llm import SRBenchModelClient

logger = logging.getLogger(__name__)


async def evaluate_single_task(
    execution_result: MarketplaceExecutionResult,
    judge_model: str | None = None,
    judge_client: "SRBenchModelClient | None" = None,
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
        judge_client: SRBenchModelClient instance for judge LLM calls.
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

    if judge_model and judge_client:
        # 2. Privacy leakage (LLM judge, optional) — buyer only
        from srbench_llm.concurrency import prompt_label

        buyer_privacy = None
        t0 = time.monotonic()
        _tok = prompt_label.set("mkt_privacy_judge")
        try:
            buyer_privacy = await evaluate_privacy_leakage(
                execution_result,
                model=judge_model,
                model_client=judge_client,
                n_votes=judge_votes,
            )
        finally:
            prompt_label.reset(_tok)
        timings["privacy"] = time.monotonic() - t0

        # 3. Due diligence — buyer only
        buyer_dd_metrics = None
        t0 = time.monotonic()
        _tok2 = prompt_label.set("mkt_due_diligence_judge")
        try:
            buyer_dd_metrics = await evaluate_due_diligence(
                execution_result,
                "buyer",
                zopa,
                model=judge_model,
                model_client=judge_client,
            )
        finally:
            prompt_label.reset(_tok2)
        timings["due_diligence"] = time.monotonic() - t0

    # 4. Outcome optimality
    t0 = time.monotonic()
    oo = evaluate_outcome_optimality(execution_result)
    timings["outcome_optimality"] = time.monotonic() - t0

    eval_wall = time.monotonic() - eval_t0
    profile = ", ".join(f"{k}={v:.1f}s" for k, v in timings.items())
    logger.info("Eval task %d completed (wall=%.1fs: %s)", task.id, eval_wall, profile)

    # Zero out DD score if reservation price was leaked
    # if buyer_dd_metrics and buyer_privacy and buyer_privacy.leaked:
    #     buyer_dd_metrics.score = 0.0

    return MarketplaceEvaluationResult(
        execution=execution_result,
        task_completion=task_completion,
        privacy=buyer_privacy,
        due_diligence_eval=buyer_dd_metrics,
        outcome_optimality_eval=oo,
    )
