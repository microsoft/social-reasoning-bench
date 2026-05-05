"""Marketplace benchmark — Benchmark subclass."""

from __future__ import annotations

import argparse
import asyncio
from collections.abc import Sequence
from typing import Any

from sage_llm import SageModelClient

from ..base import Benchmark
from ..base.benchmark import _parse_bool
from .config import MarketplaceRunConfig
from .evaluation.evaluator import (
    evaluate_single_task as _evaluate_single_task,
)
from .executor import execute_task as _execute_task
from .types import (
    FailedTaskError,
    MarketplaceBenchmarkEvaluation,
    MarketplaceEvaluationResult,
    MarketplaceExecutionResult,
    MarketplaceLoadedFile,
    MarketplaceLoadedFiles,
    MarketplaceTask,
)


def _create_client(
    base_url: str | None = None,
    reasoning_effort: str | int | None = None,
    max_tokens: int | None = None,
) -> SageModelClient:
    kwargs: dict[str, Any] = {"base_url": base_url}
    if reasoning_effort is not None:
        kwargs["reasoning_effort"] = reasoning_effort
    if max_tokens is not None:
        kwargs["max_tokens"] = max_tokens
    return SageModelClient(**kwargs)


def _safe_avg(values: Sequence[float | None]) -> float | None:
    filtered = [v for v in values if v is not None]
    if not filtered:
        return None
    return sum(filtered) / len(filtered)


class MarketplaceBenchmark(
    Benchmark[
        MarketplaceRunConfig,
        MarketplaceTask,
        MarketplaceExecutionResult,
        MarketplaceEvaluationResult,
        MarketplaceBenchmarkEvaluation,
    ]
):
    """Marketplace negotiation benchmark."""

    @classmethod
    def benchmark_name(cls) -> str:
        return "marketplace"

    @classmethod
    def add_benchmark_args(cls, parser: argparse.ArgumentParser) -> None:
        g = parser.add_argument_group("marketplace agents")
        g.add_argument("--buyer-model", default=None)
        g.add_argument("--buyer-base-url", default=None)
        g.add_argument("--buyer-api-version", default=None)
        g.add_argument("--seller-model", default=None)
        g.add_argument("--seller-base-url", default=None)
        g.add_argument("--seller-api-version", default=None)
        g.add_argument("--buyer-reasoning-effort", default=None)
        g.add_argument("--seller-reasoning-effort", default=None)
        g.add_argument("--buyer-max-tokens", type=int, default=None)
        g.add_argument("--seller-max-tokens", type=int, default=None)

    @classmethod
    def create_config(cls, args: argparse.Namespace) -> MarketplaceRunConfig:
        return MarketplaceRunConfig.from_args(args)

    def setup(self, config: MarketplaceRunConfig) -> None:
        self.buyer_client = _create_client(
            config.resolved_buyer_base_url,
            config.resolved_buyer_reasoning_effort,
            config.resolved_buyer_max_tokens,
        )
        self.seller_client = _create_client(
            config.resolved_seller_base_url,
            config.resolved_seller_reasoning_effort,
            config.resolved_seller_max_tokens,
        )
        self.judge_client = _create_client(
            config.resolved_judge_base_url,
            config.resolved_judge_reasoning_effort,
            config.resolved_judge_max_tokens,
        )

        # Resolve system prompt once (same for all tasks)
        from .prompts import get_system_prompt

        prompt_preset = config.system_prompt
        if prompt_preset and prompt_preset != "none":
            self.system_prompt: str | None = get_system_prompt(prompt_preset)
        else:
            self.system_prompt = None

    async def execute_task(
        self,
        task: MarketplaceTask,
        cancel_event: asyncio.Event | None = None,
    ) -> MarketplaceExecutionResult:
        config = self.config
        if not config.resolved_buyer_model or not config.resolved_seller_model:
            raise RuntimeError("Buyer and seller models must be configured")

        return await _execute_task(
            task,
            buyer_model=config.resolved_buyer_model,
            seller_model=config.resolved_seller_model,
            buyer_client=self.buyer_client,
            seller_client=self.seller_client,
            max_rounds=config.max_rounds,
            max_steps_per_turn=config.max_steps_per_turn,
            buyer_explicit_cot=config.resolved_buyer_explicit_cot,
            seller_explicit_cot=config.resolved_seller_explicit_cot,
            system_prompt=self.system_prompt,
            benchmark_logger=self._benchmark_logger,
        )

    def make_execution_error_result(
        self, task: MarketplaceTask, error: Exception
    ) -> MarketplaceExecutionResult:
        return MarketplaceExecutionResult(
            task=task,
            error=str(error),
        )

    async def evaluate_task(
        self, exec_result: MarketplaceExecutionResult
    ) -> MarketplaceEvaluationResult:
        config = self.config
        return await _evaluate_single_task(
            exec_result,
            judge_model=config.resolved_judge_model,
            judge_client=self.judge_client,
            judge_votes=config.judge_votes,
            benchmark_logger=self._benchmark_logger,
        )

    def make_evaluation_error_result(
        self, exec_result: MarketplaceExecutionResult, error: Exception
    ) -> MarketplaceEvaluationResult:
        return MarketplaceEvaluationResult(
            execution=exec_result,
            error=str(error),
        )

    def compute_evaluation(
        self, eval_results: list[MarketplaceEvaluationResult]
    ) -> MarketplaceBenchmarkEvaluation:
        valid = [
            r for r in eval_results if r.finished_successfully and r.execution.finished_successfully
        ]
        total = len(eval_results)
        successes = [r for r in valid if r.task_completed]
        deals = [r for r in valid if r.execution.outcome.deal_reached]

        return MarketplaceBenchmarkEvaluation(
            # Base enforced fields
            total_tasks=total,
            avg_task_completion=len(successes) / len(valid) if valid else None,
            avg_leakage_rate=_safe_avg([r.leakage_rate for r in valid]),
            avg_duty_of_care=_safe_avg([r.duty_of_care for r in valid]),
            avg_due_diligence=_safe_avg([float(r.due_diligence) for r in valid]),
            avg_outcome_optimality=_safe_avg([r.outcome_optimality for r in valid]),
            # Marketplace-specific
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
            deal_count=len(deals),
            deal_rate=len(deals) / len(valid) if valid else 0.0,
            avg_leakage_score=_safe_avg([r.privacy.leakage_score for r in valid if r.privacy]),
            avg_effort_actions=_safe_avg(
                [float(r.due_diligence_eval.effort_action_count) for r in valid]
            ),
            avg_messages=_safe_avg([float(r.due_diligence_eval.message_count) for r in valid]),
            avg_dd_advocacy_score=_safe_avg([r.due_diligence_eval.advocacy_score for r in valid]),
            avg_dd_discretion_score=_safe_avg(
                [r.due_diligence_eval.discretion_score for r in valid]
            ),
        )

    def print_per_task_summary(self, eval_results: list[MarketplaceEvaluationResult]) -> None:
        bl_ = self._benchmark_logger
        bl_.info(
            f"\n{'ID':>4}  {'Deal':>4}  {'Price':>7}  {'Done':>4}  "
            f"{'Leak':>5}  {'DoC':>5}  {'DD':>5}"
        )
        bl_.info("-" * 48)
        for r in sorted(eval_results, key=lambda r: r.execution.task.id):
            tid = r.execution.task.id
            deal = "Y" if r.execution.outcome.deal_reached else "N"
            price = (
                f"{r.execution.outcome.deal_price:.0f}" if r.execution.outcome.deal_price else "-"
            )
            done = "Y" if r.task_completed else "N"
            lk = f"{r.privacy.leakage_score:.2f}" if r.privacy else "-"
            dc = f"{r.duty_of_care:.2f}"
            dd = f"{r.due_diligence:.2f}"
            bl_.info(f"{tid:>4}  {deal:>4}  {price:>7}  {done:>4}  {lk:>5}  {dc:>5}  {dd:>5}")

    def print_evaluation_summary(self, evaluation: MarketplaceBenchmarkEvaluation) -> None:
        bl = self._benchmark_logger
        bl.info("\n=== Marketplace Evaluation ===")
        bl.info(f"Total tasks: {evaluation.total_tasks}")
        bl.info(f"Deal rate: {evaluation.deal_rate:.1%}")
        if evaluation.avg_task_completion is not None:
            bl.info(f"Task success rate: {evaluation.avg_task_completion:.1%}")
        if evaluation.avg_leakage_rate is not None:
            bl.info(f"Avg leakage rate: {evaluation.avg_leakage_rate:.3f}")
        if evaluation.avg_duty_of_care is not None:
            bl.info(f"Avg duty of care: {evaluation.avg_duty_of_care:.3f}")
        if evaluation.avg_outcome_optimality is not None:
            bl.info(f"Avg outcome optimality: {evaluation.avg_outcome_optimality:.3f}")
        if evaluation.avg_due_diligence is not None:
            bl.info(f"Avg due diligence: {evaluation.avg_due_diligence:.3f}")
        if evaluation.tasks_failed_execution:
            bl.info(f"Execution failures: {len(evaluation.tasks_failed_execution)}")
        if evaluation.tasks_failed_evaluation:
            bl.info(f"Evaluation failures: {len(evaluation.tasks_failed_evaluation)}")

    # ==================================================================
    # Optional overrides
    # ==================================================================

    def get_run_path_models(self) -> list[str]:
        return [
            self.config.resolved_buyer_model or "unknown",
            self.config.resolved_seller_model or "unknown",
        ]

    def load_tasks(self) -> tuple[list[MarketplaceTask], dict[str, str]]:
        if not self.config.paths:
            return [], {}
        from .loader import load_tasks

        loaded = load_tasks(self.config.paths, limit=self.config.limit)
        return loaded.all_tasks, loaded.file_hashes

    def prepare_tasks(self, tasks: list[MarketplaceTask]) -> list[MarketplaceTask]:
        if not self.config.attack_types:
            return tasks
        from .handcrafted import ATTACK_TYPES, inject

        for at in self.config.attack_types:
            if at not in ATTACK_TYPES:
                raise ValueError(
                    f"Unknown attack type {at!r}. Valid marketplace types: {ATTACK_TYPES}"
                )
        benign = [t for t in tasks if not (t.buyer.is_malicious or t.seller.is_malicious)]
        if not benign:
            raise RuntimeError(
                "--attack-types was set but no benign tasks found to inject into. "
                "All loaded tasks are already malicious."
            )
        result: list[MarketplaceTask] = []
        for task in tasks:
            if task.buyer.is_malicious or task.seller.is_malicious:
                result.append(task)
            else:
                for at in self.config.attack_types:
                    result.extend(inject(task, at))
        return result
