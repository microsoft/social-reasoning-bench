"""Evaluation logic for iTIP-style calendar scheduling tasks."""

import asyncio
import logging
import time
import traceback

from srbench_llm import SRBenchModelClient

from ....shared.logging import BenchmarkLogger, VerboseLogger
from ..types import (
    CalendarEvaluationResult,
    CalendarExecutionResult,
    CalendarPrivacyEvaluation,
)
from .due_diligence import evaluate_due_diligence
from .outcome_optimality import evaluate_outcome_optimality
from .privacy import evaluate_privacy_leakage
from .task_completion import evaluate_task_completion

logger = logging.getLogger(__name__)


async def evaluate_single_task(
    execution_result: CalendarExecutionResult,
    judge_model: str,
    judge_client: SRBenchModelClient,
    judge_votes: int = 3,
    benchmark_logger: BenchmarkLogger | None = None,
) -> CalendarEvaluationResult:
    """Evaluate a single task execution result.

    Runs task completion first, then runs privacy, due diligence, and
    outcome optimality evaluations concurrently. Duty of care is derived
    as outcome_optimality × due_diligence.

    Args:
        execution_result: The completed task execution to evaluate.
        judge_model: Model name for judge evaluations.
        judge_client: Model client for judge evaluations.
        judge_votes: Number of parallel judges for majority voting (default: 3).
        benchmark_logger: Optional structured logger (defaults to VerboseLogger).

    Returns:
        CalendarEvaluationResult with all evaluation metrics, or an error
        result if evaluation fails.
    """
    if benchmark_logger is None:
        benchmark_logger = VerboseLogger(logger)

    task_id = execution_result.task.id
    task = execution_result.task

    benchmark_logger.info("Eval %d started", task_id)
    eval_t0 = time.monotonic()
    timings: dict[str, float] = {}

    from srbench_llm.concurrency import prompt_label

    try:
        # 1. Task completion first (outcome_optimality depends on it)
        t0 = time.monotonic()
        _tok = prompt_label.set("cal_completion_judge")
        try:
            completion_result = await evaluate_task_completion(
                execution_result, judge_model, judge_client
            )
        finally:
            prompt_label.reset(_tok)
        timings["task_completion"] = time.monotonic() - t0

        # 2. Run privacy, due diligence, and outcome optimality concurrently
        async def _privacy():
            t = time.monotonic()
            _t = prompt_label.set("cal_privacy_judge")
            try:
                result = await evaluate_privacy_leakage(
                    execution_result, judge_model, judge_client, n_votes=judge_votes
                )
            finally:
                prompt_label.reset(_t)
            timings["privacy"] = time.monotonic() - t
            return result

        async def _due_diligence():
            t = time.monotonic()
            _t = prompt_label.set("cal_due_diligence_judge")
            try:
                result = await evaluate_due_diligence(execution_result, judge_model, judge_client)
            finally:
                prompt_label.reset(_t)
            timings["due_diligence"] = time.monotonic() - t
            return result

        def _outcome_optimality():
            t = time.monotonic()
            result = evaluate_outcome_optimality(
                completion_result.scheduled_meeting,
                task.assistant.preferences,
                task.requestor.preferences,
                task.assistant.calendar,
                task.requestor.calendar,
                has_conflicts=completion_result.has_conflicts,
                requestor_is_malicious=task.requestor.is_malicious,
            )
            timings["outcome_optimality"] = time.monotonic() - t
            return result

        leaked_secrets, due_diligence_result, oo_result = await asyncio.gather(
            _privacy(),
            _due_diligence(),
            asyncio.to_thread(_outcome_optimality),
        )

        total_secrets = sum(1 for m in task.assistant.calendar if m.is_secret)
        privacy_eval = CalendarPrivacyEvaluation(
            leaked_secrets=leaked_secrets,
            total_secrets=total_secrets,
        )

        # Zero out DD score if secrets were leaked
        # if leaked_secrets and due_diligence_result is not None:
        #     due_diligence_result.score = 0.0

        eval_wall = time.monotonic() - eval_t0
        profile = ", ".join(f"{k}={v:.1f}s" for k, v in timings.items())
        benchmark_logger.info("Eval %d completed (wall=%.1fs: %s)", task_id, eval_wall, profile)

        return CalendarEvaluationResult(
            execution=execution_result,
            appropriately_scheduled_or_notscheduled=completion_result.success,
            scheduled_meeting=completion_result.scheduled_meeting,
            has_conflicts=completion_result.has_conflicts,
            illegal_moves=completion_result.illegal_moves,
            requestor_is_malicious=completion_result.requestor_is_malicious,
            privacy=privacy_eval,
            outcome_optimality_score=oo_result.outcome_optimality_score,
            outcome_optimality_eval=oo_result.model_dump(),
            scheduled_duration_error=completion_result.scheduled_duration_error,
            due_diligence_eval=due_diligence_result,
        )
    except Exception:
        error_msg = traceback.format_exc()
        benchmark_logger.error("Eval %d failed: %s", task_id, error_msg)
        return CalendarEvaluationResult(
            execution=execution_result,
            appropriately_scheduled_or_notscheduled=False,
            scheduled_meeting=None,
            has_conflicts=False,
            illegal_moves=[],
            requestor_is_malicious=task.requestor.is_malicious,
            error=error_msg,
        )
