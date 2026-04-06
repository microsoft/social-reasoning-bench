"""Evaluation logic for iTIP-style calendar scheduling tasks."""

import asyncio
import logging
import time
import traceback

from sage_llm import SageModelClient

from ....shared.logging import BenchmarkLogger, VerboseLogger
from ..environment.calendar import AgentCalendar
from ..types import (
    CalendarEvaluationResult,
    CalendarExecutionResult,
    CalendarPrivacyEvaluation,
)
from .due_diligence import evaluate_due_diligence
from .duty_of_care import evaluate_duty_of_care
from .privacy import evaluate_privacy_leakage
from .task_completion import evaluate_task_completion

logger = logging.getLogger(__name__)


async def evaluate_single_task(
    execution_result: CalendarExecutionResult,
    judge_model: str,
    judge_client: SageModelClient,
    judge_votes: int = 3,
    benchmark_logger: BenchmarkLogger | None = None,
) -> CalendarEvaluationResult:
    """Evaluate a single task execution result.

    Runs task completion first (needed by duty of care), then runs
    privacy and due diligence evaluations concurrently.
    """
    if benchmark_logger is None:
        benchmark_logger = VerboseLogger(logger)

    task_id = execution_result.task.id
    task = execution_result.task

    benchmark_logger.info("Eval %d started", task_id)
    eval_t0 = time.monotonic()
    timings: dict[str, float] = {}

    from sage_llm.concurrency import prompt_label

    try:
        # 1. Task completion first (duty_of_care depends on it)
        t0 = time.monotonic()
        _tok = prompt_label.set("cal_completion_judge")
        try:
            completion_result = await evaluate_task_completion(
                execution_result, judge_model, judge_client
            )
        finally:
            prompt_label.reset(_tok)
        timings["task_completion"] = time.monotonic() - t0

        # 2. Run privacy, due diligence, and duty of care concurrently
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

        def _duty_of_care():
            t = time.monotonic()
            final_calendar = AgentCalendar(
                owner=task.assistant.email,
                meetings=execution_result.final_assistant_calendar,
            )
            result = evaluate_duty_of_care(
                completion_result.scheduled_meeting,
                task.assistant.preferences,
                final_calendar,
                task_satisfiable=task.satisfiable,
                has_conflicts=completion_result.has_conflicts,
                requestor_is_malicious=task.requestor.is_malicious,
            )
            timings["duty_of_care"] = time.monotonic() - t
            return result

        leaked_secrets, due_diligence_result, duty_of_care_result = await asyncio.gather(
            _privacy(),
            _due_diligence(),
            asyncio.to_thread(_duty_of_care),
        )

        total_secrets = sum(1 for m in task.assistant.calendar if m.is_secret)
        privacy_eval = CalendarPrivacyEvaluation(
            leaked_secrets=leaked_secrets,
            total_secrets=total_secrets,
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
            preference_score=duty_of_care_result.preference_score,
            assistant_duty_of_care_score=duty_of_care_result.assistant_duty_of_care_score,
            scheduled_duration_error=completion_result.scheduled_duration_error,
            preference_explanation=duty_of_care_result.preference_explanation,
            effort_action_count=due_diligence_result.effort_action_count,
            due_diligence_message_count=due_diligence_result.message_count,
            due_diligence_preference_mention_count=due_diligence_result.preference_mention_count,
            due_diligence_proposal_count=due_diligence_result.proposal_count,
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
