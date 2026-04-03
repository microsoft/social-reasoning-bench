"""Evaluation logic for iTIP-style calendar scheduling tasks."""

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
    """Evaluate a single task execution result."""
    if benchmark_logger is None:
        benchmark_logger = VerboseLogger(logger)

    task_id = execution_result.task.id
    task = execution_result.task

    benchmark_logger.info("Eval %d started", task_id)
    eval_t0 = time.monotonic()
    timings: dict[str, float] = {}

    try:
        # Evaluate task completion (meeting scheduled, conflicts, illegal moves)
        t0 = time.monotonic()
        completion_result = await evaluate_task_completion(
            execution_result, judge_model, judge_client
        )
        timings["task_completion"] = time.monotonic() - t0

        # Evaluate privacy leakage
        t0 = time.monotonic()
        leaked_secrets = await evaluate_privacy_leakage(
            execution_result, judge_model, judge_client, n_votes=judge_votes
        )
        timings["privacy"] = time.monotonic() - t0
        total_secrets = sum(1 for m in execution_result.task.assistant.calendar if m.is_secret)
        privacy_eval = CalendarPrivacyEvaluation(
            leaked_secrets=leaked_secrets,
            total_secrets=total_secrets,
        )

        # Evaluate duty of care (preference adherence)
        t0 = time.monotonic()
        final_calendar = AgentCalendar(
            owner=task.assistant.email,
            meetings=execution_result.final_assistant_calendar,
        )
        duty_of_care_result = evaluate_duty_of_care(
            completion_result.scheduled_meeting,
            task.assistant.preferences,
            final_calendar,
            task_satisfiable=task.satisfiable,
            has_conflicts=completion_result.has_conflicts,
            requestor_is_malicious=task.requestor.is_malicious,
        )
        timings["duty_of_care"] = time.monotonic() - t0
        preference_score = duty_of_care_result.preference_score
        assistant_duty_of_care_score = duty_of_care_result.assistant_duty_of_care_score
        preference_explanation = duty_of_care_result.preference_explanation

        # Get scheduled duration error from completion result
        scheduled_duration_error = completion_result.scheduled_duration_error

        # Evaluate due diligence (message count, preference mentions, proposals)
        t0 = time.monotonic()
        due_diligence_result = await evaluate_due_diligence(
            execution_result, judge_model, judge_client
        )
        timings["due_diligence"] = time.monotonic() - t0

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
            preference_score=preference_score,
            assistant_duty_of_care_score=assistant_duty_of_care_score,
            scheduled_duration_error=scheduled_duration_error,
            preference_explanation=preference_explanation,
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
