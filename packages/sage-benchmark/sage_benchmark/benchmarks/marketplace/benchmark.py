"""Marketplace benchmark — Benchmark subclass."""

from __future__ import annotations

import argparse
import asyncio
from collections.abc import Sequence

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
) -> SageModelClient:
    if reasoning_effort is not None:
        return SageModelClient(base_url=base_url, reasoning_effort=reasoning_effort)
    return SageModelClient(base_url=base_url)


def _expand_privacy_variants(
    tasks: list[MarketplaceTask], privacy_level: str
) -> list[MarketplaceTask]:
    """Expand tasks into privacy-level variants.

    - Malicious buyer  → 1 variant: seller gets privacy, variant="seller"
    - Malicious seller → 1 variant: buyer gets privacy, variant="buyer"
    - Non-malicious    → 4 variants: none/buyer/seller/both
    """
    expanded: list[MarketplaceTask] = []
    for task in tasks:
        task_dict = task.model_dump(mode="json")
        buyer_malicious = task.buyer.is_malicious
        seller_malicious = task.seller.is_malicious

        if buyer_malicious or seller_malicious:
            # Privacy goes to the victim (non-malicious) role only
            if not buyer_malicious:
                task_dict["buyer"]["privacy_level"] = privacy_level
            if not seller_malicious:
                task_dict["seller"]["privacy_level"] = privacy_level
            victim = "seller" if buyer_malicious else "buyer"
            task_dict["variant"] = victim
            expanded.append(MarketplaceTask.model_validate(task_dict))
        else:
            # Non-malicious: 4 variants
            for variant_name, buyer_pl, seller_pl in [
                ("none", None, None),
                ("buyer", privacy_level, None),
                ("seller", None, privacy_level),
                ("both", privacy_level, privacy_level),
            ]:
                d = task_dict.copy()
                d["buyer"] = {**task_dict["buyer"], "privacy_level": buyer_pl}
                d["seller"] = {**task_dict["seller"], "privacy_level": seller_pl}
                d["variant"] = variant_name
                expanded.append(MarketplaceTask.model_validate(d))

    return expanded


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

        g = parser.add_argument_group("marketplace options")
        g.add_argument(
            "--system-prompt-preset",
            dest="system_prompt",
            choices=["none", "simple", "strong", "ci"],
            default=None,
        )

    @classmethod
    def create_config(cls, args: argparse.Namespace) -> MarketplaceRunConfig:
        return MarketplaceRunConfig.from_args(args)

    def setup(self, config: MarketplaceRunConfig) -> None:
        self.buyer_client = _create_client(
            config.resolved_buyer_base_url,
            config.resolved_buyer_reasoning_effort,
        )
        self.seller_client = _create_client(
            config.resolved_seller_base_url,
            config.resolved_seller_reasoning_effort,
        )
        self.judge_client = _create_client(
            config.resolved_judge_base_url,
            config.resolved_judge_reasoning_effort,
        )

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
            explicit_cot=config.explicit_cot or False,
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
            avg_buyer_leakage_score=_safe_avg(
                [r.buyer_privacy.leakage_score for r in valid if r.buyer_privacy]
            ),
            avg_seller_leakage_score=_safe_avg(
                [r.seller_privacy.leakage_score for r in valid if r.seller_privacy]
            ),
            avg_buyer_duty_of_care=_safe_avg(
                [r.duty_of_care_eval.buyer_duty_of_care for r in valid]
            ),
            avg_seller_duty_of_care=_safe_avg(
                [r.duty_of_care_eval.seller_duty_of_care for r in valid]
            ),
            avg_deal_ratio_centered=_safe_avg(
                [r.duty_of_care_eval.deal_ratio_centered for r in valid]
            ),
            avg_buyer_effort_actions=_safe_avg(
                [float(r.buyer_metrics.effort_action_count) for r in valid]
            ),
            avg_seller_effort_actions=_safe_avg(
                [float(r.seller_metrics.effort_action_count) for r in valid]
            ),
            avg_buyer_messages=_safe_avg([float(r.buyer_metrics.message_count) for r in valid]),
            avg_seller_messages=_safe_avg([float(r.seller_metrics.message_count) for r in valid]),
        )

    def print_per_task_summary(self, eval_results: list[MarketplaceEvaluationResult]) -> None:
        bl_ = self._benchmark_logger
        bl_.info(
            f"\n{'ID':>4}  {'Deal':>4}  {'Price':>7}  {'Done':>4}  "
            f"{'BLeak':>5}  {'SLeak':>5}  {'BDoC':>5}  {'SDoC':>5}  "
            f"{'BEff':>4}  {'SEff':>4}"
        )
        bl_.info("-" * 65)
        for r in sorted(eval_results, key=lambda r: r.execution.task.id):
            tid = r.execution.task.id
            deal = "Y" if r.execution.outcome.deal_reached else "N"
            price = (
                f"{r.execution.outcome.deal_price:.0f}" if r.execution.outcome.deal_price else "-"
            )
            done = "Y" if r.task_completed else "N"
            bl = f"{r.buyer_privacy.leakage_score:.2f}" if r.buyer_privacy else "-"
            sl = f"{r.seller_privacy.leakage_score:.2f}" if r.seller_privacy else "-"
            bd = (
                f"{r.duty_of_care_eval.buyer_duty_of_care:.2f}"
                if r.duty_of_care_eval.buyer_duty_of_care is not None
                else "-"
            )
            sd = (
                f"{r.duty_of_care_eval.seller_duty_of_care:.2f}"
                if r.duty_of_care_eval.seller_duty_of_care is not None
                else "-"
            )
            be = str(r.buyer_metrics.effort_action_count)
            se = str(r.seller_metrics.effort_action_count)
            bl_.info(
                f"{tid:>4}  {deal:>4}  {price:>7}  {done:>4}  "
                f"{bl:>5}  {sl:>5}  {bd:>5}  {sd:>5}  "
                f"{be:>4}  {se:>4}"
            )

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
        if evaluation.avg_due_diligence is not None:
            bl.info(f"Avg due diligence: {evaluation.avg_due_diligence:.1f}")
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
        tasks = loaded.all_tasks

        # Handcrafted injection: expand benign tasks into malicious variants
        if self.config.attack_types:
            from .handcrafted import ATTACK_TYPES, inject

            expanded: list[MarketplaceTask] = list(tasks)
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
            for task in benign:
                for at in self.config.attack_types:
                    expanded.extend(inject(task, at))
            tasks = expanded

        privacy_level = self.config.system_prompt
        if privacy_level and privacy_level != "none":
            tasks = _expand_privacy_variants(tasks, privacy_level)

        return tasks, loaded.file_hashes
