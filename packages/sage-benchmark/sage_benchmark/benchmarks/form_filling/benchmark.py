"""Form-filling benchmark — Benchmark subclass."""

from __future__ import annotations

import argparse
import asyncio
from collections.abc import Sequence

from sage_llm import SageModelClient

from ..base import Benchmark
from ..base.benchmark import _parse_bool
from .config import FormFillingRunConfig
from .evaluation.evaluator import (
    evaluate_single_task as _evaluate_single_task,
)
from .executor import execute_task as _execute_task
from .types import (
    FailedTaskError,
    FormFillingBenchmarkEvaluation,
    FormFillingEvaluationResult,
    FormFillingExecutionResult,
    FormTask,
)


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


class FormFillingBenchmark(
    Benchmark[
        FormFillingRunConfig,
        FormTask,
        FormFillingExecutionResult,
        FormFillingEvaluationResult,
        FormFillingBenchmarkEvaluation,
    ]
):
    """Form-filling interview benchmark."""

    @classmethod
    def benchmark_name(cls) -> str:
        return "form_filling"

    @classmethod
    def add_benchmark_args(cls, parser: argparse.ArgumentParser) -> None:
        g = parser.add_argument_group("form-filling agents")
        g.add_argument("--assistant-model", default=None)
        g.add_argument("--assistant-base-url", default=None)
        g.add_argument("--assistant-api-version", default=None)
        g.add_argument("--interviewer-model", default=None)
        g.add_argument("--interviewer-base-url", default=None)
        g.add_argument("--interviewer-api-version", default=None)
        g.add_argument("--assistant-reasoning-effort", default=None)
        g.add_argument("--interviewer-reasoning-effort", default=None)

        g = parser.add_argument_group("form-filling options")
        g.add_argument("--prompt-type", default="none", choices=["none", "simple", "strong", "ci"])
        g.add_argument(
            "--single-field-mode",
            type=_parse_bool,
            default=False,
            metavar="{true,false}",
        )
        g.add_argument(
            "--eval-batch-size",
            type=int,
            default=0,
            help="Max concurrent evaluation work items per task (0 = auto-scale)",
        )

    @classmethod
    def create_config(cls, args: argparse.Namespace) -> FormFillingRunConfig:
        return FormFillingRunConfig.from_args(args)

    def setup(self, config: FormFillingRunConfig) -> None:
        self.assistant_client = _create_client(
            config.resolved_assistant_base_url,
            config.resolved_assistant_reasoning_effort,
        )
        self.interviewer_client = _create_client(
            config.resolved_interviewer_base_url,
            config.resolved_interviewer_reasoning_effort,
        )
        self.judge_client = _create_client(
            config.resolved_judge_base_url,
            config.resolved_judge_reasoning_effort,
        )

    async def execute_task(
        self,
        task: FormTask,
        cancel_event: asyncio.Event | None = None,
    ) -> FormFillingExecutionResult:
        config = self.config
        if not config.resolved_assistant_model or not config.resolved_interviewer_model:
            raise RuntimeError("Assistant and interviewer models must be configured")

        return await _execute_task(
            task,
            task_index=0,
            interviewer_client=self.interviewer_client,
            interviewer_model=config.resolved_interviewer_model,
            assistant_client=self.assistant_client,
            assistant_model=config.resolved_assistant_model,
            max_rounds=config.max_rounds,
            benchmark_logger=self._benchmark_logger,
            prompt_type=config.prompt_type,
            single_field_mode=config.single_field_mode,
            max_steps_per_turn=config.max_steps_per_turn,
            explicit_cot=config.explicit_cot or False,
        )

    def make_execution_error_result(
        self, task: FormTask, error: Exception
    ) -> FormFillingExecutionResult:
        return FormFillingExecutionResult(
            task=task,
            error=str(error),
        )

    _MAX_TOTAL_EVAL_CONCURRENCY = 80

    async def evaluate_task(
        self, exec_result: FormFillingExecutionResult
    ) -> FormFillingEvaluationResult:
        config = self.config
        if not config.resolved_judge_model:
            raise RuntimeError("Judge model must be configured")

        eval_batch_size = config.eval_batch_size
        if eval_batch_size <= 0:
            # Auto-scale: keep total concurrency ≈ _MAX_TOTAL_EVAL_CONCURRENCY
            eval_batch_size = max(1, self._MAX_TOTAL_EVAL_CONCURRENCY // config.batch_size)

        return await _evaluate_single_task(
            exec_result,
            config.resolved_judge_model,
            self.judge_client,
            self._benchmark_logger,
            judge_votes=config.judge_votes,
            eval_batch_size=eval_batch_size,
        )

    def make_evaluation_error_result(
        self, exec_result: FormFillingExecutionResult, error: Exception
    ) -> FormFillingEvaluationResult:
        return FormFillingEvaluationResult(
            execution=exec_result,
            error=str(error),
        )

    def compute_evaluation(
        self, eval_results: list[FormFillingEvaluationResult]
    ) -> FormFillingBenchmarkEvaluation:
        valid = [
            r for r in eval_results if r.finished_successfully and r.execution.finished_successfully
        ]
        total = len(eval_results)
        successes = [r for r in valid if r.task_completed]

        return FormFillingBenchmarkEvaluation(
            # Base enforced fields
            total_tasks=total,
            avg_task_completion=len(successes) / len(valid) if valid else None,
            avg_leakage_rate=_safe_avg([r.leakage_rate for r in valid]),
            avg_duty_of_care=_safe_avg([r.duty_of_care for r in valid]),
            avg_due_diligence=_safe_avg([float(r.due_diligence) for r in valid]),
            # Form-filling-specific
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
            avg_accuracy=_safe_avg([r.correctness.accuracy for r in valid]),
            avg_precision=_safe_avg([r.correctness.precision for r in valid]),
            avg_recall=_safe_avg([r.correctness.recall for r in valid]),
            avg_f1_score=_safe_avg([r.correctness.f1_score for r in valid]),
            avg_form_privacy_score=_safe_avg([r.form_privacy.privacy_score for r in valid]),
            avg_conversation_privacy_score=_safe_avg(
                [r.conversation_privacy.privacy_score for r in valid]
            ),
            total_secrets_leaked=sum(len(r.privacy_leaks) for r in valid),
            total_duty_of_care_fields=sum(r.duty_of_care_eval.total_fields for r in valid),
            avg_duty_of_care_score=_safe_avg([r.duty_of_care_eval.min_score for r in valid]),
            avg_effort_action_count=_safe_avg(
                [float(r.due_diligence_eval.effort_action_count) for r in valid]
            ),
            avg_masked_field_accuracy=_safe_avg(
                [r.due_diligence_eval.masked_field_accuracy for r in valid]
            ),
            pydantic_pass_rate=(
                sum(1 for r in valid if r.pydantic_validation_passed) / len(valid)
                if valid
                else None
            ),
        )

    def print_per_task_summary(self, eval_results: list[FormFillingEvaluationResult]) -> None:
        self._benchmark_logger.info(
            f"\n{'ID':>4}  {'F1':>5}  {'FPrv':>5}  {'CPrv':>5}  {'DoC':>5}  {'DD':>3}  {'Err':>3}"
        )
        self._benchmark_logger.info("-" * 40)
        for r in sorted(eval_results, key=lambda r: r.execution.task.id):
            tid = r.execution.task.id
            f1 = f"{r.correctness.f1_score:.2f}"
            fp = f"{r.form_privacy.privacy_score:.2f}"
            cp = f"{r.conversation_privacy.privacy_score:.2f}"
            doc = f"{r.duty_of_care:.2f}"
            dd = str(r.due_diligence)
            err = "Y" if r.error else ""
            self._benchmark_logger.info(
                f"{tid:>4}  {f1:>5}  {fp:>5}  {cp:>5}  {doc:>5}  {dd:>3}  {err:>3}"
            )

    def print_evaluation_summary(self, evaluation: FormFillingBenchmarkEvaluation) -> None:
        self._benchmark_logger.info("\n=== Form-Filling Evaluation ===")
        self._benchmark_logger.info(f"Total tasks: {evaluation.total_tasks}")
        if evaluation.avg_task_completion is not None:
            self._benchmark_logger.info(
                f"Task completion rate: {evaluation.avg_task_completion:.1%}"
            )
        if evaluation.avg_f1_score is not None:
            self._benchmark_logger.info(f"Avg F1 score: {evaluation.avg_f1_score:.3f}")
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
            self.config.resolved_interviewer_model or "unknown",
        ]

    def get_concurrency_hints(self) -> list[str]:
        return list(
            {
                self.config.resolved_assistant_model,
                self.config.resolved_interviewer_model,
                self.config.resolved_judge_model,
            }
            - {None}
        )

    def load_tasks(self) -> tuple[list[FormTask], dict[str, str]]:
        if not self.config.paths:
            return [], {}
        from .loader import load_tasks

        loaded = load_tasks(self.config.paths, limit=self.config.limit)
        tasks = loaded.all_tasks

        # Handcrafted injection: expand benign tasks into malicious variants
        if self.config.attack_types:
            from .handcrafted import ATTACK_TYPES, inject

            expanded: list[FormTask] = list(tasks)
            for at in self.config.attack_types:
                if at not in ATTACK_TYPES:
                    raise ValueError(
                        f"Unknown attack type {at!r}. Valid form-filling types: {ATTACK_TYPES}"
                    )
            benign = [t for t in tasks if not t.is_malicious]
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
