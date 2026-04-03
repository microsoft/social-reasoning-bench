"""Calendar scheduling benchmark — Benchmark subclass."""

from __future__ import annotations

import argparse
import asyncio
import logging
from collections.abc import Sequence
from pathlib import Path

from sage_llm import SageModelClient

from ..base import Benchmark
from .agents.assistant import get_system_prompt
from .config import CalendarRunConfig
from .evaluation.evaluator import (
    evaluate_single_task as _evaluate_single_task,
)
from .executor import (
    execute_task as _execute_task,
)
from .types import (
    CalendarBenchmarkEvaluation,
    CalendarEvaluationResult,
    CalendarExecutionResult,
    CalendarTask,
    FailedTaskError,
    SuboptimalDutyCare,
)

logger = logging.getLogger(__name__)


def _create_client(
    base_url: str | None = None,
    reasoning_effort: str | int | None = None,
) -> SageModelClient:
    if reasoning_effort is not None:
        return SageModelClient(base_url=base_url, reasoning_effort=reasoning_effort)
    return SageModelClient(base_url=base_url)


def _safe_avg(values: Sequence[float | None]) -> float | None:
    filtered = [v for v in values if v is not None]
    if not filtered:
        return None
    return sum(filtered) / len(filtered)


class CalendarBenchmark(
    Benchmark[
        CalendarRunConfig,
        CalendarTask,
        CalendarExecutionResult,
        CalendarEvaluationResult,
        CalendarBenchmarkEvaluation,
    ]
):
    """Calendar scheduling benchmark."""

    # ==================================================================
    # Abstract method implementations
    # ==================================================================

    @classmethod
    def benchmark_name(cls) -> str:
        return "calendar"

    @classmethod
    def add_benchmark_args(cls, parser: argparse.ArgumentParser) -> None:
        g = parser.add_argument_group("calendar agents")
        g.add_argument("--assistant-model", default=None)
        g.add_argument("--assistant-base-url", default=None)
        g.add_argument("--assistant-api-version", default=None)
        g.add_argument("--requestor-model", default=None)
        g.add_argument("--requestor-base-url", default=None)
        g.add_argument("--requestor-api-version", default=None)
        g.add_argument("--assistant-reasoning-effort", default=None)
        g.add_argument("--requestor-reasoning-effort", default=None)
        from ..base.benchmark import _parse_bool

        g.add_argument(
            "--assistant-explicit-cot", type=_parse_bool, default=None, metavar="{true,false}"
        )
        g.add_argument(
            "--requestor-explicit-cot", type=_parse_bool, default=None, metavar="{true,false}"
        )

        g = parser.add_argument_group("calendar options")
        g.add_argument(
            "--expose-preferences",
            type=_parse_bool,
            default=None,
            metavar="{true,false}",
            help="Expose scheduling preferences to assistant",
        )

    @classmethod
    def create_config(cls, args: argparse.Namespace) -> CalendarRunConfig:
        return CalendarRunConfig.from_args(args)

    def setup(self, config: CalendarRunConfig) -> None:
        self.assistant_client = _create_client(
            config.resolved_assistant_base_url,
            config.resolved_assistant_reasoning_effort,
        )
        self.requestor_client = _create_client(
            config.resolved_requestor_base_url,
            config.resolved_requestor_reasoning_effort,
        )
        self.judge_client = _create_client(
            config.resolved_judge_base_url,
            config.resolved_judge_reasoning_effort,
        )

        # Resolve system prompt
        if config.assistant_system_prompt_file:
            self.system_prompt: str | None = Path(config.assistant_system_prompt_file).read_text()
        elif config.assistant_system_prompt:
            self.system_prompt = get_system_prompt(config.assistant_system_prompt)
        else:
            self.system_prompt = None

    async def execute_task(
        self,
        task: CalendarTask,
        cancel_event: asyncio.Event | None = None,
    ) -> CalendarExecutionResult:
        config = self.config
        if not config.resolved_assistant_model or not config.resolved_requestor_model:
            raise RuntimeError("Assistant and requestor models must be configured")

        return await _execute_task(
            task,
            config.resolved_assistant_model,
            self.assistant_client,
            config.resolved_requestor_model,
            self.requestor_client,
            config.max_rounds,
            config.max_steps_per_turn,
            self.system_prompt,
            config.resolved_assistant_explicit_cot,
            config.resolved_requestor_explicit_cot,
            config.expose_preferences or False,
            cancel_event,
            benchmark_logger=self._benchmark_logger,
        )

    def make_execution_error_result(
        self, task: CalendarTask, error: Exception
    ) -> CalendarExecutionResult:
        return CalendarExecutionResult(
            task=task,
            error=str(error),
        )

    async def evaluate_task(self, exec_result: CalendarExecutionResult) -> CalendarEvaluationResult:
        config = self.config
        if not config.resolved_judge_model:
            raise RuntimeError("Judge model must be configured")

        return await _evaluate_single_task(
            exec_result,
            config.resolved_judge_model,
            self.judge_client,
            config.judge_votes,
            benchmark_logger=self._benchmark_logger,
        )

    def make_evaluation_error_result(
        self, exec_result: CalendarExecutionResult, error: Exception
    ) -> CalendarEvaluationResult:
        return CalendarEvaluationResult(
            execution=exec_result,
            error=str(error),
        )

    def compute_evaluation(
        self, eval_results: list[CalendarEvaluationResult]
    ) -> CalendarBenchmarkEvaluation:
        valid = [
            r for r in eval_results if r.finished_successfully and r.execution.finished_successfully
        ]

        total = len(eval_results)
        successes = [r for r in valid if r.task_completed]

        leakage_rates = [r.leakage_rate for r in valid]
        doc_scores = [r.assistant_duty_of_care_score for r in valid]
        dd_counts = [r.effort_action_count for r in valid]

        return CalendarBenchmarkEvaluation(
            # Base enforced fields
            total_tasks=total,
            avg_task_completion=len(successes) / len(valid) if valid else None,
            avg_leakage_rate=_safe_avg(leakage_rates),
            avg_duty_of_care=_safe_avg(doc_scores),
            avg_due_diligence=_safe_avg([float(d) for d in dd_counts if d is not None]),
            # Calendar-specific
            tasks_succeeded=[r.execution.task.id for r in successes],
            tasks_failed_execution=[
                FailedTaskError(task_id=r.execution.task.id, error=r.execution.error or "")
                for r in eval_results
                if not r.execution.finished_successfully
            ],
            tasks_failed_evaluation=[
                FailedTaskError(task_id=r.execution.task.id, error=r.error or "")
                for r in eval_results
                if r.execution.finished_successfully and not r.finished_successfully
            ],
            tasks_hit_max_rounds=sum(1 for r in valid if r.execution.max_rounds_reached),
            task_conflicts=sum(1 for r in valid if r.has_conflicts),
            task_illegal_moves=sum(1 for r in valid if r.illegal_moves),
            task_missing_meetings=sum(
                1
                for r in valid
                if r.execution.task.satisfiable
                and not r.requestor_is_malicious
                and not r.scheduled_meeting_found
            ),
            task_unwanted_meetings=sum(
                1
                for r in valid
                if (not r.execution.task.satisfiable or r.requestor_is_malicious)
                and r.scheduled_meeting_found
            ),
            privacy_tasks_with_leakage=sum(1 for r in valid if r.leakage_rate > 0),
            fiduciary_tasks_with_preferences=sum(
                1 for r in valid if r.execution.task.assistant.preferences
            ),
            fiduciary_avg_preference_score=_safe_avg([r.preference_score for r in valid]),
            fiduciary_avg_assistant_duty_of_care_score=_safe_avg(doc_scores),
            fiduciary_suboptimal_assistant_duty_of_care=[
                SuboptimalDutyCare(
                    task_id=r.execution.task.id,
                    explanation=r.preference_explanation.explanation
                    if r.preference_explanation
                    else "",
                )
                for r in valid
                if r.assistant_duty_of_care_score is not None
                and r.assistant_duty_of_care_score < 1.0
                and r.preference_explanation
            ],
            fiduciary_avg_scheduled_duration_error=_safe_avg(
                [
                    float(r.scheduled_duration_error)
                    for r in valid
                    if r.scheduled_duration_error is not None
                ]
            ),
            due_diligence_avg_effort_action_count=_safe_avg(
                [float(d) for d in dd_counts if d is not None]
            ),
            due_diligence_avg_message_count=_safe_avg(
                [
                    float(r.due_diligence_message_count)
                    for r in valid
                    if r.due_diligence_message_count is not None
                ]
            ),
            due_diligence_avg_preference_mention_count=_safe_avg(
                [
                    float(r.due_diligence_preference_mention_count)
                    for r in valid
                    if r.due_diligence_preference_mention_count is not None
                ]
            ),
            due_diligence_avg_proposal_count=_safe_avg(
                [
                    float(r.due_diligence_proposal_count)
                    for r in valid
                    if r.due_diligence_proposal_count is not None
                ]
            ),
        )

    def print_per_task_summary(self, eval_results: list[CalendarEvaluationResult]) -> None:
        # Delegate to the original summary printer via conversion.
        # For now, a simple table.
        self._benchmark_logger.info(
            f"\n{'ID':>4}  {'Done':>4}  {'Leak':>5}  {'DoC':>5}  {'DD':>3}  {'Err':>3}"
        )
        self._benchmark_logger.info("-" * 35)
        for r in sorted(eval_results, key=lambda r: r.execution.task.id):
            tid = r.execution.task.id
            done = "Y" if r.task_completed else "N"
            leak = f"{r.leakage_rate:.2f}"
            doc = f"{r.duty_of_care:.2f}"
            dd = str(r.due_diligence)
            err = "Y" if r.error else ""
            self._benchmark_logger.info(
                f"{tid:>4}  {done:>4}  {leak:>5}  {doc:>5}  {dd:>3}  {err:>3}"
            )

    def print_evaluation_summary(self, evaluation: CalendarBenchmarkEvaluation) -> None:
        self._benchmark_logger.info("\n=== Calendar Scheduling Evaluation ===")
        self._benchmark_logger.info(f"Total tasks: {evaluation.total_tasks}")
        if evaluation.avg_task_completion is not None:
            self._benchmark_logger.info(
                f"Task completion rate: {evaluation.avg_task_completion:.1%}"
            )
        if evaluation.avg_leakage_rate is not None:
            self._benchmark_logger.info(f"Avg leakage rate: {evaluation.avg_leakage_rate:.3f}")
        if evaluation.avg_duty_of_care is not None:
            self._benchmark_logger.info(f"Avg duty of care: {evaluation.avg_duty_of_care:.3f}")
        if evaluation.avg_due_diligence is not None:
            self._benchmark_logger.info(f"Avg due diligence: {evaluation.avg_due_diligence:.1f}")
        if evaluation.tasks_failed_execution:
            self._benchmark_logger.info(
                f"Execution failures: {len(evaluation.tasks_failed_execution)}"
            )
        if evaluation.tasks_failed_evaluation:
            self._benchmark_logger.info(
                f"Evaluation failures: {len(evaluation.tasks_failed_evaluation)}"
            )

    # ==================================================================
    # Optional overrides
    # ==================================================================

    def get_run_path_models(self) -> list[str]:
        return [
            self.config.resolved_assistant_model or "unknown",
            self.config.resolved_requestor_model or "unknown",
        ]

    def load_tasks(self) -> tuple[list[CalendarTask], dict[str, str]]:
        if not self.config.paths:
            return [], {}
        from .loader import load_tasks

        loaded = load_tasks(self.config.paths, limit=self.config.limit)
        tasks = loaded.all_tasks

        # Handcrafted injection: expand benign tasks into malicious variants
        if self.config.attack_types:
            from .handcrafted import ATTACK_TYPES, inject

            expanded: list[CalendarTask] = list(tasks)
            for at in self.config.attack_types:
                if at not in ATTACK_TYPES:
                    raise ValueError(
                        f"Unknown attack type {at!r}. Valid calendar types: {ATTACK_TYPES}"
                    )
            benign = [t for t in tasks if not t.requestor.is_malicious]
            if not benign:
                raise RuntimeError(
                    "--attack-types was set but no benign tasks found to inject into. "
                    "All loaded tasks are already malicious."
                )
            for task in benign:
                for at in self.config.attack_types:
                    expanded.extend(inject(task, at))
            tasks = expanded

        return tasks, loaded.file_hashes
