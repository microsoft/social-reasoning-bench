"""Strategy validation: benchmark each candidate and select the most damaging one.

Generates N×M tasks (N strategies × M validation tasks), runs them in a
single benchmark for full parallelisation, then groups results by strategy
to find the one that causes the most damage to the target metric.
"""

from __future__ import annotations

import time
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml
from whimsygen.core.models import Strategy

# ── Attack type → target metric mapping ──────────────────────────────────


@dataclass(frozen=True)
class MetricTarget:
    """Which metric to optimise and in which direction."""

    # Attribute name on ``BenchmarkEvaluationResult``
    metric_name: str
    # True ⇒ higher value = more damage (e.g. leakage_rate)
    # False ⇒ lower value = more damage (e.g. duty_of_care score)
    maximize: bool


# Maps each attack type to the ``BenchmarkEvaluationResult`` field that
# measures damage, and whether more damage means a higher or lower value.
ATTACK_METRIC_MAP: dict[str, MetricTarget] = {
    "privacy": MetricTarget("avg_leakage_rate", maximize=True),
    "duty_of_care": MetricTarget("avg_duty_of_care", maximize=False),
    "red_flags": MetricTarget("avg_duty_of_care", maximize=False),
    "due_diligence": MetricTarget("avg_due_diligence", maximize=False),
    "hallucination": MetricTarget("avg_task_completion", maximize=False),
}


# ── Result containers ────────────────────────────────────────────────────


@dataclass
class StrategyScore:
    """Pairs a candidate strategy with its validation score."""

    strategy: Strategy
    metric_value: float | None  # None when all tasks failed
    rank: int = 0


@dataclass
class ValidationResult:
    """Full output of the validation loop."""

    attack_type: str
    target_metric: str
    direction: str  # "maximize" or "minimize"
    scores: list[StrategyScore]
    best: StrategyScore
    elapsed_seconds: float = 0.0


# ── Benchmark factory ────────────────────────────────────────────────────


def _get_benchmark_factory(
    benchmark_name: str,
) -> tuple[type, type]:
    """Return ``(BenchmarkClass, RunConfigClass)`` for *benchmark_name*.

    Both classes are returned unparameterised (``type``) because the generic
    parameters differ across benchmarks and the caller does not need them.

    Raises:
        ValueError: Unknown benchmark name.
    """
    if benchmark_name == "calendar":
        from sage_benchmark.benchmarks.calendar_scheduling.benchmark import (
            CalendarBenchmark,
        )
        from sage_benchmark.benchmarks.calendar_scheduling.config import (
            CalendarRunConfig,
        )

        return CalendarBenchmark, CalendarRunConfig

    if benchmark_name == "form-filling":
        from sage_benchmark.benchmarks.form_filling.benchmark import (
            FormFillingBenchmark,
        )
        from sage_benchmark.benchmarks.form_filling.config import (
            FormFillingRunConfig,
        )

        return FormFillingBenchmark, FormFillingRunConfig

    if benchmark_name == "marketplace":
        from sage_benchmark.benchmarks.marketplace.benchmark import (
            MarketplaceBenchmark,
        )
        from sage_benchmark.benchmarks.marketplace.config import (
            MarketplaceRunConfig,
        )

        return MarketplaceBenchmark, MarketplaceRunConfig

    raise ValueError(
        f"Unknown benchmark: {benchmark_name!r}. "
        f"Expected one of: 'calendar', 'form-filling', 'marketplace'"
    )


# ── Core validation loop ─────────────────────────────────────────────────


async def validate_strategies(
    *,
    strategies: list[Strategy],
    validation_tasks: list[Any],
    benchmark_name: str,
    attack_type: str,
    inject_fn: Any,
    agent_model: str,
    judge_model: str,
    output_dir: Path | None = None,
) -> ValidationResult:
    """Run every strategy against the validation set in a single benchmark.

    1. Injects every strategy into every validation task → N×M tasks.
    2. Runs **one** benchmark with all N×M tasks (full parallelisation).
    3. Groups results by strategy and ranks by damage to the target metric.

    Args:
        strategies: Candidate strategies to evaluate.
        validation_tasks: Small set of base tasks to test each strategy against.
        benchmark_name: One of ``"calendar"``, ``"form-filling"``, ``"marketplace"``.
        attack_type: Attack type key (must exist in :data:`ATTACK_METRIC_MAP`).
        inject_fn: ``inject_fn(task, attack_type, strategy_text) → injected_task``.
        agent_model: Model identifier for the agent under test.
        judge_model: Model identifier for the evaluation judge.
        output_dir: Optional directory for benchmark outputs and
            ``validation_results.yaml``.

    Returns:
        :class:`ValidationResult` with ranked scores and the best strategy.

    Raises:
        ValueError: If *attack_type* is not in :data:`ATTACK_METRIC_MAP`.
    """
    if attack_type not in ATTACK_METRIC_MAP:
        raise ValueError(
            f"Unknown attack type for validation: {attack_type!r}. "
            f"Known types: {sorted(ATTACK_METRIC_MAP)}"
        )

    target = ATTACK_METRIC_MAP[attack_type]
    num_strategies = len(strategies)
    num_val_tasks = len(validation_tasks)

    # ── 1. Build flat task list: N strategies × M validation tasks ────────
    #
    # Each task gets a unique ID encoding its strategy index and position:
    #   task.id = strategy_idx * num_val_tasks + task_position
    #
    # We also build a hash→strategy_idx map so we can group results back
    # to their originating strategy after the benchmark run.
    all_tasks: list[Any] = []
    strategy_by_hash: dict[str, int] = {}

    for strategy_idx, strategy in enumerate(strategies):
        for task_pos, val_task in enumerate(validation_tasks):
            variants = inject_fn(val_task, attack_type, strategy.game_strategies)
            for variant in variants:
                new_id = strategy_idx * num_val_tasks + task_pos
                # Tasks are frozen Pydantic models; model_copy creates a new instance.
                re_ided = variant.model_copy(update={"id": new_id})
                all_tasks.append(re_ided)
                strategy_by_hash[re_ided.hash] = strategy_idx

    total_tasks = len(all_tasks)
    print(
        f"  Built {total_tasks} validation tasks "
        f"({num_strategies} strategies × {num_val_tasks} tasks)"
    )

    # ── 2. Run one benchmark with all N×M tasks ──────────────────────────
    from sage_benchmark.shared.logging import create_benchmark_logger

    BenchmarkCls, ConfigCls = _get_benchmark_factory(benchmark_name)
    config = ConfigCls(
        model=agent_model,
        judge_model=judge_model,
        output_dir=output_dir,
    )
    bl = create_benchmark_logger("quiet")

    t0 = time.monotonic()
    benchmark = BenchmarkCls(config, tasks=all_tasks, benchmark_logger=bl)
    output = await benchmark.run()
    elapsed = time.monotonic() - t0

    # ── 3. Group results by strategy index ────────────────────────────────
    groups: dict[int, list[Any]] = defaultdict(list)
    for result in output.results:
        task_hash: str = result.execution.task.hash
        if task_hash not in strategy_by_hash:
            raise RuntimeError(
                f"Result for task hash {task_hash!r} not found in strategy map. "
                "This indicates a bug in task ID assignment."
            )
        groups[strategy_by_hash[task_hash]].append(result)

    # ── 4. Compute per-strategy metrics and rank ─────────────────────────
    scores: list[StrategyScore] = []
    for strategy_idx, strategy in enumerate(strategies):
        group = groups.get(strategy_idx, [])
        if not group:
            print(f"  Strategy {strategy_idx}: no results (all tasks failed)")
            scores.append(StrategyScore(strategy=strategy, metric_value=None))
            continue

        # Reuse the benchmark's own aggregation logic.
        evaluation = benchmark.compute_evaluation(group)
        metric_value: float | None = getattr(evaluation, target.metric_name, None)
        scores.append(StrategyScore(strategy=strategy, metric_value=metric_value))

        label = f"{metric_value:.4f}" if metric_value is not None else "None"
        print(f"  Strategy {strategy_idx}: {target.metric_name} = {label}")

    # Sort: best damage first.  None values sort to the end (worst rank).
    def _sort_key(s: StrategyScore) -> float:
        if s.metric_value is None:
            return float("-inf") if target.maximize else float("inf")
        return s.metric_value if target.maximize else -s.metric_value

    scores.sort(key=_sort_key, reverse=True)
    for rank, score in enumerate(scores):
        score.rank = rank + 1

    best = scores[0]
    direction = "maximize" if target.maximize else "minimize"

    result = ValidationResult(
        attack_type=attack_type,
        target_metric=target.metric_name,
        direction=direction,
        scores=scores,
        best=best,
        elapsed_seconds=elapsed,
    )

    # ── 5. Persist results for debugging ─────────────────────────────────
    if output_dir is not None:
        _save_validation_results(result, Path(output_dir) / "validation_results.yaml")

    return result


# ── Persistence ──────────────────────────────────────────────────────────


def _save_validation_results(result: ValidationResult, path: Path) -> None:
    """Write all strategy scores to YAML for debugging and reproducibility."""
    data: dict[str, Any] = {
        "attack_type": result.attack_type,
        "target_metric": result.target_metric,
        "direction": result.direction,
        "elapsed_seconds": round(result.elapsed_seconds, 1),
        "best_strategy": {
            "rank": result.best.rank,
            "metric_value": result.best.metric_value,
            "source_seed": result.best.strategy.source_seed,
            "strategy_text": result.best.strategy.game_strategies,
        },
        "all_strategies": [
            {
                "rank": s.rank,
                "metric_value": s.metric_value,
                "source_seed": s.strategy.source_seed,
                "strategy_text": s.strategy.game_strategies,
            }
            for s in result.scores
        ],
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        yaml.dump(
            data,
            f,
            default_flow_style=False,
            sort_keys=False,
            allow_unicode=True,
            width=120,
        )
    print(f"  Validation results saved to {path}")
