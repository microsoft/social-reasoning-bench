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
from .preference_adherence import evaluate_preference_adherence
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

    Runs task completion first, then runs due diligence and preference
    adherence concurrently. Duty of care is derived as
    preference_adherence × due_diligence.

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
        # 1. Task completion first (preference adherence depends on the scheduled meeting)
        t0 = time.monotonic()
        _tok = prompt_label.set("cal_completion_judge")
        try:
            completion_result = await evaluate_task_completion(
                execution_result, judge_model, judge_client
            )
        finally:
            prompt_label.reset(_tok)
        timings["task_completion"] = time.monotonic() - t0

        async def _due_diligence():
            t = time.monotonic()
            _t = prompt_label.set("cal_due_diligence_judge")
            try:
                result = await evaluate_due_diligence(execution_result, judge_model, judge_client)
            finally:
                prompt_label.reset(_t)
            timings["due_diligence"] = time.monotonic() - t
            return result

        def _preference_adherence():
            t = time.monotonic()
            result = evaluate_preference_adherence(
                task,
                completion_result.scheduled_meeting,
                has_conflicts=completion_result.has_conflicts,
            )
            timings["preference_adherence"] = time.monotonic() - t
            return result

        due_diligence_result, adherence_result = await asyncio.gather(
            _due_diligence(),
            asyncio.to_thread(_preference_adherence),
        )

        total_secrets = sum(1 for m in task.assistant.calendar if m.is_secret)
        privacy_eval = CalendarPrivacyEvaluation(
            leaked_secrets=[],
            total_secrets=0,
        )

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
            hard_constraints_satisfied=(
                adherence_result.hard_constraints_satisfied if adherence_result else None
            ),
            soft_constraints_score=(
                adherence_result.soft_constraints_score if adherence_result else None
            ),
            preference_adherence_eval=adherence_result.model_dump() if adherence_result else None,
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
