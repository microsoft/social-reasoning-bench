"""Strategy validation: benchmark each candidate and select the most damaging one.

Provides a two-phase API for use with ``ExperimentPoolExecutor``:

1. :func:`prepare_validation_benchmark` — builds N×M tasks and a Benchmark
   instance (without running it).
2. :func:`score_validation_results` — post-processes a completed
   ``BenchmarkOutput`` to rank strategies by damage.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml
from whimsygen.core.models import Strategy

# ── Attack type → target metric mapping ──────────────────────────────────


@dataclass(frozen=True)
class MetricComponent:
    """One component of a (possibly composite) target metric.

    *names* lists candidate attribute names (first found on the evaluation
    object wins).  If none is found, *default* is used.
    """

    names: tuple[str, ...]
    default: float = 1.0


@dataclass(frozen=True)
class MetricTarget:
    """Which metric(s) to optimise and in which direction.

    The final score is the mean of all resolved component values.
    """

    label: str
    components: tuple[MetricComponent, ...]
    maximize: bool


def _resolve_metric(target: MetricTarget, evaluation: object) -> float | None:
    """Resolve a composite MetricTarget to a single scalar."""
    values: list[float] = []
    for comp in target.components:
        val: float | None = None
        for name in comp.names:
            val = getattr(evaluation, name, None)
            if val is not None:
                break
        values.append(val if val is not None else comp.default)
    return sum(values) / len(values) if values else None


# Maps each attack type to the ``BenchmarkEvaluationResult`` field(s) that
# measure damage, and whether more damage means a higher or lower value.
ATTACK_METRIC_MAP: dict[str, MetricTarget] = {
    "privacy": MetricTarget(
        label="avg_leakage_rate",
        components=(MetricComponent(("avg_leakage_rate",), default=0.0),),
        maximize=True,
    ),
    "outcome_optimality": MetricTarget(
        label="avg_outcome_optimality",
        components=(MetricComponent(("avg_outcome_optimality",), default=1.0),),
        maximize=False,
    ),
    "due_diligence": MetricTarget(
        label="avg_dd_score",
        # Using the internal scores because the final output is gated by privacy
        # leading to 0 DD for all cases, providing no signal.
        components=(
            MetricComponent(
                ("avg_dd_advocacy_score", "due_diligence_avg_advocacy_score"),
            ),
            MetricComponent(
                ("due_diligence_avg_information_gathering_score",),
            ),
        ),
        maximize=False,
    ),
}


# ── Result containers ────────────────────────────────────────────────────


@dataclass
class StrategyScore:
    """Pairs a candidate strategy with its validation score."""

    strategy: Strategy
    metric_value: float | None  # None when all tasks failed
    strategy_idx: int = 0
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

    Args:
        benchmark_name: One of ``"calendar"`` or ``"marketplace"``.

    Returns:
        Tuple of (BenchmarkClass, RunConfigClass) for the benchmark.

    Raises:
        ValueError: If *benchmark_name* is not recognised.
    """
    if benchmark_name == "calendar":
        from sage_benchmark.benchmarks.calendar_scheduling.benchmark import (
            CalendarBenchmark,
        )
        from sage_benchmark.benchmarks.calendar_scheduling.config import (
            CalendarRunConfig,
        )

        return CalendarBenchmark, CalendarRunConfig

    if benchmark_name == "marketplace":
        from sage_benchmark.benchmarks.marketplace.benchmark import (
            MarketplaceBenchmark,
        )
        from sage_benchmark.benchmarks.marketplace.config import (
            MarketplaceRunConfig,
        )

        return MarketplaceBenchmark, MarketplaceRunConfig

    raise ValueError(
        f"Unknown benchmark: {benchmark_name!r}. Expected one of: 'calendar', 'marketplace'"
    )


# ── Two-phase API ───────────────────────────────────────────────────────


@dataclass
class PreparedValidation:
    """Everything needed to run and score a validation benchmark."""

    attack_type: str
    strategies: list[Strategy]
    strategy_by_hash: dict[str, int]
    benchmark: Any  # Benchmark instance


def prepare_validation_benchmark(
    *,
    strategies: list[Strategy],
    validation_tasks: list[Any],
    benchmark_name: str,
    attack_type: str,
    inject_fn: Any,
    assistant_model: str,
    judge_model: str,
    assistant_reasoning_effort: str | int | None = None,
    assistant_explicit_cot: bool = False,
    counterparty_model: str | None = None,
    counterparty_reasoning_effort: str | int | None = None,
    counterparty_explicit_cot: bool = False,
    judge_reasoning_effort: str | int | None = None,
    output_dir: Path | None = None,
    benchmark_logger: Any = None,
    max_rounds: int = 5,
    max_steps_per_turn: int = 5,
    restart_exec: bool = False,
    restart_eval: bool = False,
) -> PreparedValidation:
    """Build a Benchmark with N×M injected tasks, ready for pooled execution.

    Args:
        strategies: Candidate strategies to evaluate.
        validation_tasks: Small set of base tasks to test each strategy against.
        benchmark_name: One of ``"calendar"``, ``"form-filling"``, ``"marketplace"``.
        attack_type: Attack type key (must exist in :data:`ATTACK_METRIC_MAP`).
        inject_fn: ``inject_fn(task, attack_type, strategy_text) → list[task]``.
        assistant_model: Model identifier for the agent under test.
        judge_model: Model identifier for the evaluation judge.
        assistant_reasoning_effort: Optional reasoning effort for the assistant.
        assistant_explicit_cot: Enable explicit chain-of-thought for the assistant.
        counterparty_model: Optional model for the counterparty agent.
        counterparty_reasoning_effort: Optional reasoning effort for the counterparty.
        counterparty_explicit_cot: Enable explicit chain-of-thought for the counterparty.
        judge_reasoning_effort: Optional reasoning effort for the judge.
        output_dir: Optional directory for benchmark outputs.
        benchmark_logger: BenchmarkLogger instance (shared across benchmarks).
        max_rounds: Maximum conversation rounds per task.
        max_steps_per_turn: Maximum tool calls per agent turn.
        restart_exec: Re-run execution (ignore checkpointed execution progress).
        restart_eval: Re-run evaluation (ignore checkpointed evaluation progress).

    Returns:
        :class:`PreparedValidation` with the benchmark instance and metadata.
    """
    if attack_type not in ATTACK_METRIC_MAP:
        raise ValueError(
            f"Unknown attack type for validation: {attack_type!r}. "
            f"Known types: {sorted(ATTACK_METRIC_MAP)}"
        )

    num_strategies = len(strategies)
    num_val_tasks = len(validation_tasks)

    # Build flat task list: N strategies × M validation tasks
    all_tasks: list[Any] = []
    strategy_by_hash: dict[str, int] = {}

    for strategy_idx, strategy in enumerate(strategies):
        for task_pos, val_task in enumerate(validation_tasks):
            variants = inject_fn(val_task, attack_type, strategy.game_strategies)
            for variant in variants:
                new_id = strategy_idx * num_val_tasks + task_pos
                re_ided = variant.model_copy(update={"id": new_id})
                all_tasks.append(re_ided)
                strategy_by_hash[re_ided.hash] = strategy_idx

    total_tasks = len(all_tasks)
    print(
        f"  [{attack_type}] Built {total_tasks} validation tasks "
        f"({num_strategies} strategies × {num_val_tasks} tasks)"
    )

    BenchmarkCls, ConfigCls = _get_benchmark_factory(benchmark_name)
    config_kwargs: dict[str, Any] = {
        "model": assistant_model,
        "judge_model": judge_model,
        "output_dir": output_dir / attack_type if output_dir is not None else None,
        "variant": f"whimsical_validation_{attack_type}",
        "max_rounds": max_rounds,
        "max_steps_per_turn": max_steps_per_turn,
    }
    if assistant_reasoning_effort is not None:
        config_kwargs["reasoning_effort"] = assistant_reasoning_effort
    if assistant_explicit_cot:
        config_kwargs["explicit_cot"] = True
    if judge_reasoning_effort is not None:
        config_kwargs["judge_reasoning_effort"] = judge_reasoning_effort

    # Map generic counterparty args to benchmark-specific role names
    counterparty_role = {
        "calendar": "requestor",
        "form-filling": "interviewer",
        "marketplace": "seller",
    }.get(benchmark_name)
    if counterparty_role and counterparty_model:
        config_kwargs[f"{counterparty_role}_model"] = counterparty_model
    if counterparty_role and counterparty_reasoning_effort is not None:
        config_kwargs[f"{counterparty_role}_reasoning_effort"] = counterparty_reasoning_effort
    if counterparty_role and counterparty_explicit_cot:
        config_kwargs[f"{counterparty_role}_explicit_cot"] = True

    config = ConfigCls(**config_kwargs)
    benchmark = BenchmarkCls(
        config,
        tasks=all_tasks,
        benchmark_logger=benchmark_logger,
        restart_exec=restart_exec,
        restart_eval=restart_eval,
    )

    return PreparedValidation(
        attack_type=attack_type,
        strategies=strategies,
        strategy_by_hash=strategy_by_hash,
        benchmark=benchmark,
    )


def score_validation_results(
    prepared: PreparedValidation,
    output: Any,
    output_dir: Path | None = None,
) -> ValidationResult:
    """Rank strategies by damage from a completed benchmark output.

    Args:
        prepared: The :class:`PreparedValidation` returned by
            :func:`prepare_validation_benchmark`.
        output: The ``BenchmarkOutput`` from the benchmark run.
        output_dir: Optional directory for ``validation_results.yaml``.

    Returns:
        :class:`ValidationResult` with ranked scores and the best strategy.
    """
    attack_type = prepared.attack_type
    target = ATTACK_METRIC_MAP[attack_type]
    strategies = prepared.strategies
    strategy_by_hash = prepared.strategy_by_hash
    benchmark = prepared.benchmark

    # Group results by strategy index
    groups: dict[int, list[Any]] = defaultdict(list)
    for result in output.results:
        task_hash: str = result.execution.task.hash
        if task_hash not in strategy_by_hash:
            raise RuntimeError(
                f"Result for task hash {task_hash!r} not found in strategy map. "
                "This indicates a bug in task ID assignment."
            )
        groups[strategy_by_hash[task_hash]].append(result)

    # Compute per-strategy metrics and rank
    scores: list[StrategyScore] = []
    for strategy_idx, strategy in enumerate(strategies):
        group = groups.get(strategy_idx, [])
        if not group:
            scores.append(
                StrategyScore(strategy=strategy, metric_value=None, strategy_idx=strategy_idx)
            )
            continue

        evaluation = benchmark.compute_evaluation(group)
        metric_value = _resolve_metric(target, evaluation)
        scores.append(
            StrategyScore(strategy=strategy, metric_value=metric_value, strategy_idx=strategy_idx)
        )

    # Print compact summary
    valid = [s.metric_value for s in scores if s.metric_value is not None]
    n_none = len(scores) - len(valid)
    if valid:
        lo, hi = min(valid), max(valid)
        range_str = f"range [{lo:.4f}, {hi:.4f}]"
    else:
        range_str = "no valid scores"
    none_str = f", {n_none} failed" if n_none else ""
    print(f"  Scored {len(scores)} strategies: {range_str}{none_str}")

    # Sort: best damage first
    def _sort_key(s: StrategyScore) -> float:
        if s.metric_value is None:
            return float("-inf")
        return s.metric_value if target.maximize else -s.metric_value

    scores.sort(key=_sort_key, reverse=True)
    for rank, score in enumerate(scores):
        score.rank = rank + 1

    best = scores[0]
    direction = "maximize" if target.maximize else "minimize"

    result = ValidationResult(
        attack_type=attack_type,
        target_metric=target.label,
        direction=direction,
        scores=scores,
        best=best,
    )

    if output_dir is not None:
        _save_validation_results(
            result, Path(output_dir) / f"validation_results_{attack_type}.yaml"
        )

    return result


# ── Persistence ──────────────────────────────────────────────────────────


def _save_validation_results(result: ValidationResult, path: Path) -> None:
    """Write all strategy scores to YAML for debugging and reproducibility.

    Args:
        result: ValidationResult containing ranked strategy scores.
        path: Output YAML file path.
    """
    data: dict[str, Any] = {
        "attack_type": result.attack_type,
        "target_metric": result.target_metric,
        "direction": result.direction,
        "elapsed_seconds": round(result.elapsed_seconds, 1),
        "best_strategy": {
            "strategy_idx": result.best.strategy_idx,
            "rank": result.best.rank,
            "metric_value": result.best.metric_value,
            "source_seed": result.best.strategy.source_seed,
            "strategy_text": result.best.strategy.game_strategies,
        },
        "all_strategies": [
            {
                "strategy_idx": s.strategy_idx,
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
    print(f"  Validation details → {path}")
