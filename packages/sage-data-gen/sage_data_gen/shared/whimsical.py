"""Shared WhimsyGen infrastructure for adversarial strategy generation.

Provides :class:`StrategyProvider` (load/generate/cache strategies via WhimsyGen)
and CLI helpers used by all three benchmark pipelines.
"""

import argparse
import random
from collections.abc import Callable, Sequence
from pathlib import Path
from typing import TypeVar

import yaml
from whimsygen import WhimsyGen
from whimsygen.core.models import Strategy

T = TypeVar("T")

DEFAULT_SEEDS_DIR = Path("data/whimsygen/seeds")


class StrategyProvider:
    """Load or generate adversarial strategies using WhimsyGen.

    Wraps the WhimsyGen library with caching, lazy initialisation, and simple
    iteration helpers (``get_next`` / ``get_random``).
    """

    def __init__(
        self,
        *,
        model: str,
        seeds: Path | str | None = None,
        task: str | None = None,
        strategies: Path | str | None = None,
        topics: list[str] | None = None,
        chunk_size: int = 5000,
        max_chunks_per_seed: int | None = None,
        max_strategies_per_chunk: int | None = None,
        max_strategies_per_seed: int | None = None,
        prefetch_seeds: int | None = None,
        prefetch_strategies: int | None = None,
    ):
        self.model = model
        self.seeds = Path(seeds) if seeds else None
        self.task = task or ""
        self.strategies = Path(strategies) if strategies else None
        self.topics = topics
        self.chunk_size = chunk_size
        self.max_chunks_per_seed = max_chunks_per_seed
        self.max_strategies_per_chunk = max_strategies_per_chunk
        self.max_strategies_per_seed = max_strategies_per_seed
        self.prefetch_seeds = prefetch_seeds
        self.prefetch_strategies = prefetch_strategies
        self._strategies_list: list[Strategy] = []
        self._index = 0
        self._wg: WhimsyGen | None = None

    def _get_whimsygen(self) -> WhimsyGen:
        if self._wg is None:
            self._wg = WhimsyGen(model=self.model, seeds=self.seeds, task=self.task)
        return self._wg

    async def load_or_generate(self, count: int) -> list[Strategy]:
        """Load cached strategies or generate new ones up to *count*."""
        wg = self._get_whimsygen()
        if self.strategies and self.strategies.exists():
            self._strategies_list = wg.strategies.load(self.strategies)
            if len(self._strategies_list) >= count:
                print(f"Loaded {len(self._strategies_list)} strategies from {self.strategies}")
                return self._strategies_list[:count]
            print(
                f"Cache has {len(self._strategies_list)} strategies, need {count}. Generating more..."
            )

        print(f"Generating {count} strategies using {self.model}...")
        sample_kwargs: dict = {
            "n": count,
            "topics": self.topics,
            "chunk_size": self.chunk_size,
            "max_chunks_per_seed": self.max_chunks_per_seed,
            "max_strategies_per_chunk": self.max_strategies_per_chunk,
            "max_strategies_per_seed": self.max_strategies_per_seed,
        }
        if self.prefetch_seeds is not None:
            sample_kwargs["prefetch_seeds"] = self.prefetch_seeds
        if self.prefetch_strategies is not None:
            sample_kwargs["prefetch_strategies"] = self.prefetch_strategies
        self._strategies_list = await wg.sample(**sample_kwargs)

        if self.strategies and self._strategies_list:
            self.strategies.parent.mkdir(parents=True, exist_ok=True)
            wg.strategies.save(self.strategies)
            print(f"Saved {len(self._strategies_list)} strategies to {self.strategies}")

        return self._strategies_list

    def get_next(self) -> Strategy:
        """Return the next strategy, cycling when the list is exhausted."""
        if not self._strategies_list:
            raise ValueError("No strategies loaded. Call load_or_generate() first.")
        strategy = self._strategies_list[self._index % len(self._strategies_list)]
        self._index += 1
        return strategy

    def get_random(self, rng: random.Random | None = None) -> Strategy:
        """Return a random strategy."""
        if not self._strategies_list:
            raise ValueError("No strategies loaded. Call load_or_generate() first.")
        r = rng or random
        return r.choice(self._strategies_list)

    def __len__(self) -> int:
        return len(self._strategies_list)


# ---------------------------------------------------------------------------
# CLI / IO helpers for strategy-only generation (form-filling, marketplace)
# ---------------------------------------------------------------------------


def save_strategies_yaml(strategies: list[Strategy], output_path: Path) -> None:
    """Save strategies to a flat YAML file consumable by the benchmark."""
    strategy_strings = [s.game_strategies for s in strategies]
    output_data = {"strategies": strategy_strings}
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        yaml.dump(
            output_data, f, default_flow_style=False, sort_keys=False, allow_unicode=True, width=120
        )


def build_arg_parser(description: str):
    """Build the shared CLI argument parser for strategy generation scripts."""
    import argparse

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        "-o", "--output", type=Path, required=True, help="Output strategies YAML file"
    )
    parser.add_argument("-m", "--model", required=True, help="Model for strategy generation")
    parser.add_argument(
        "-n", "--count", type=int, default=20, help="Number of strategies to generate"
    )
    parser.add_argument(
        "--seeds-dir",
        type=Path,
        default=DEFAULT_SEEDS_DIR,
        help=f"Directory containing seed YAML files (default: {DEFAULT_SEEDS_DIR})",
    )
    parser.add_argument("--topics", nargs="+")
    parser.add_argument("--seed-chunk-size", type=int, default=5000)
    parser.add_argument("--max-chunks-per-seed", type=int)
    parser.add_argument("--max-strategies-per-chunk", type=int)
    parser.add_argument("--max-strategies-per-seed", type=int)
    parser.add_argument("--prefetch-seeds", type=int)
    parser.add_argument("--prefetch-strategies", type=int)
    parser.add_argument(
        "--strategies-file", type=Path, help="Cache file for strategies (load if exists)"
    )
    return parser


async def run_strategy_generation(args, task_description: str) -> None:
    """Shared CLI runner — generate strategies and save to YAML."""
    output_path = args.output
    strategy_provider = _provider_from_args(args, task_description)

    print(f"Generating strategies (model: {args.model})...")
    strategies = await strategy_provider.load_or_generate(args.count)

    print(f"Saving {len(strategies)} strategies to {output_path}")
    save_strategies_yaml(strategies, output_path)
    print(f"\nDone! Generated {len(strategies)} strategies -> {output_path}")


# ---------------------------------------------------------------------------
# Shared whimsical injection runner
# ---------------------------------------------------------------------------


def build_injection_arg_parser(
    description: str,
    attack_types: list[str],
) -> argparse.ArgumentParser:
    """Build CLI parser for whimsical injection scripts."""
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("--input", type=Path, required=True, help="Input tasks YAML file")
    parser.add_argument("--attack-type", choices=attack_types, required=True)
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=None,
        help="Output YAML (default: <stem>-whimsical-<attack>.yaml)",
    )
    parser.add_argument("-m", "--model", required=True, help="Model for strategy generation")
    parser.add_argument(
        "-n",
        "--count",
        type=int,
        default=1,
        help="Number of strategies to generate (default: 1, applied to all tasks)",
    )
    parser.add_argument(
        "--strategy-assignment",
        choices=["sequential", "random", "unique", "single"],
        default="single",
    )
    parser.add_argument(
        "--seeds-dir",
        type=Path,
        default=DEFAULT_SEEDS_DIR,
        help=f"Directory containing seed YAML files (default: {DEFAULT_SEEDS_DIR})",
    )
    parser.add_argument("--topics", nargs="+")
    parser.add_argument("--seed-chunk-size", type=int, default=5000)
    parser.add_argument("--max-chunks-per-seed", type=int)
    parser.add_argument("--max-strategies-per-chunk", type=int)
    parser.add_argument("--max-strategies-per-seed", type=int)
    parser.add_argument("--prefetch-seeds", type=int)
    parser.add_argument("--prefetch-strategies", type=int)
    parser.add_argument("--strategies-file", type=Path)
    parser.add_argument("--rng-seed", type=int, default=42)

    # -- Validation: generate → benchmark → select best --------------------
    val = parser.add_argument_group("validation (generate-validate-select)")
    val.add_argument(
        "--validate",
        action="store_true",
        help="Generate N strategies, benchmark each on a validation set, "
        "then inject only the best into the full task set.",
    )
    val.add_argument(
        "--n-strategies",
        type=int,
        default=None,
        help="Number of candidate strategies to generate for validation "
        "(overrides -n when --validate is set)",
    )
    val.add_argument("--agent-model", help="Model for the agent under test")
    val.add_argument("--judge-model", help="Model for the evaluation judge")
    val.add_argument(
        "--val-tasks-data",
        type=Path,
        help="Path to validation task YAML file (small set of tasks)",
    )
    val.add_argument(
        "--val-tasks-limit",
        type=int,
        default=None,
        help="Max number of validation tasks to use from --val-tasks-data",
    )
    val.add_argument(
        "--val-output-dir",
        type=Path,
        default=None,
        help="Directory for validation benchmark outputs and results",
    )

    return parser


def _provider_from_args(args, task_description: str) -> StrategyProvider:
    """Build a StrategyProvider from parsed CLI args."""
    return StrategyProvider(
        model=args.model,
        seeds=getattr(args, "seeds_dir", None),
        task=task_description,
        strategies=getattr(args, "strategies_file", None),
        topics=getattr(args, "topics", None),
        chunk_size=getattr(args, "seed_chunk_size", 5000),
        max_chunks_per_seed=getattr(args, "max_chunks_per_seed", None),
        max_strategies_per_chunk=getattr(args, "max_strategies_per_chunk", None),
        max_strategies_per_seed=getattr(args, "max_strategies_per_seed", None),
        prefetch_seeds=getattr(args, "prefetch_seeds", None),
        prefetch_strategies=getattr(args, "prefetch_strategies", None),
    )


async def run_injection(
    args: argparse.Namespace,
    task_description: str,
    load_fn: Callable[[Sequence[Path]], list[T]],
    inject_fn: Callable[[T, str, str], list[T]],
    save_fn: Callable[[list[T], Path], None],
    *,
    benchmark_name: str | None = None,
) -> None:
    """Shared CLI runner for whimsical injection.

    When ``args.validate`` is set, delegates to
    :func:`_run_injection_with_validation` which generates N strategies,
    benchmarks each on a validation set, and injects the best into all tasks.

    Args:
        args: Parsed CLI args (from :func:`build_injection_arg_parser`).
        task_description: The TASK_DESCRIPTION for the attack type.
        load_fn: ``load_fn([path]) -> list[task]``.
        inject_fn: ``inject_fn(task, attack_type, strategy_text) -> list[task]``.
        save_fn: ``save_fn(tasks, output_path)``.
        benchmark_name: Required when ``--validate`` is used.  One of
            ``"calendar"``, ``"form-filling"``, ``"marketplace"``.
    """
    if getattr(args, "validate", False):
        _check_validation_args(args, benchmark_name)
        assert benchmark_name is not None  # validated by _check_validation_args
        await _run_injection_with_validation(
            args,
            task_description,
            benchmark_name,
            load_fn,
            inject_fn,
            save_fn,
        )
        return

    input_path = Path(args.input)
    if args.output:
        output_path = args.output
    else:
        output_path = input_path.parent / f"{input_path.stem}-whimsical-{args.attack_type}.yaml"

    print(f"Loading tasks from {input_path}")
    tasks = load_fn([input_path])
    print(f"Loaded {len(tasks)} tasks")

    # Determine how many strategies we need
    assignment = args.strategy_assignment
    if assignment == "unique":
        need = len(tasks)
    elif assignment == "single":
        need = 1
    else:
        need = args.count

    provider = _provider_from_args(args, task_description)
    print(f"Loading/generating {need} strategies (model: {args.model})...")
    await provider.load_or_generate(need)

    rng = random.Random(args.rng_seed)
    injected: list[T] = []
    for task in tasks:
        if assignment == "random":
            strategy = provider.get_random(rng)
        else:
            strategy = provider.get_next()
        injected.extend(inject_fn(task, args.attack_type, strategy.game_strategies))

    print(f"Saving {len(injected)} tasks to {output_path}")
    save_fn(injected, output_path)
    print(f"\nDone!\n  Input:  {input_path}\n  Output: {output_path}\n  Tasks:  {len(injected)}")


# ---------------------------------------------------------------------------
# Validation: generate → benchmark → select best
# ---------------------------------------------------------------------------


def _check_validation_args(
    args: argparse.Namespace,
    benchmark_name: str | None,
) -> None:
    """Raise if required validation flags are missing.

    ``--agent-model`` and ``--judge-model`` default to ``-m/--model``
    (the strategy generation model) when not explicitly provided.
    """
    # Default agent/judge model to the strategy generation model.
    if not getattr(args, "agent_model", None):
        args.agent_model = getattr(args, "model", None)
    if not getattr(args, "judge_model", None):
        args.judge_model = getattr(args, "model", None)

    missing: list[str] = []
    if benchmark_name is None:
        missing.append("benchmark_name (internal — caller must pass it)")
    if not args.agent_model:
        missing.append("--agent-model (or -m/--model)")
    if not args.judge_model:
        missing.append("--judge-model (or -m/--model)")
    if not getattr(args, "val_tasks_data", None):
        missing.append("--val-tasks-data")
    if missing:
        raise ValueError(f"--validate requires the following: {', '.join(missing)}")


async def _run_injection_with_validation(
    args: argparse.Namespace,
    task_description: str,
    benchmark_name: str,
    load_fn: Callable[[Sequence[Path]], list[T]],
    inject_fn: Callable[[T, str, str], list[T]],
    save_fn: Callable[[list[T], Path], None],
) -> None:
    """Generate strategies, validate against benchmark, inject best into full task set."""
    from .validation import validate_strategies

    input_path = Path(args.input)
    if args.output:
        output_path = args.output
    else:
        output_path = input_path.parent / f"{input_path.stem}-whimsical-{args.attack_type}.yaml"

    # 1. Load full task set (for final injection)
    print(f"Loading tasks from {input_path}")
    tasks = load_fn([input_path])
    print(f"Loaded {len(tasks)} tasks")

    # 2. Load validation tasks
    val_data_path = Path(args.val_tasks_data)
    print(f"Loading validation tasks from {val_data_path}")
    val_tasks = load_fn([val_data_path])
    val_limit: int | None = getattr(args, "val_tasks_limit", None)
    if val_limit is not None and val_limit < len(val_tasks):
        val_tasks = val_tasks[:val_limit]
    print(f"Using {len(val_tasks)} validation tasks")

    # 3. Generate N candidate strategies
    # --n-strategies overrides -n/--count when --validate is set.
    n_strategies: int = getattr(args, "n_strategies", None) or args.count
    provider = _provider_from_args(args, task_description)
    print(f"Generating {n_strategies} candidate strategies (model: {args.model})...")
    strategies = await provider.load_or_generate(n_strategies)

    # 4. Validate: single benchmark run with N × M tasks
    print(f"\nValidating {len(strategies)} strategies against {len(val_tasks)} tasks...")
    result = await validate_strategies(
        strategies=strategies,
        validation_tasks=val_tasks,
        benchmark_name=benchmark_name,
        attack_type=args.attack_type,
        inject_fn=inject_fn,
        agent_model=args.agent_model,
        judge_model=args.judge_model,
        output_dir=getattr(args, "val_output_dir", None),
    )

    # 5. Report winner
    best = result.best
    print(f"\nBest strategy (rank 1/{len(strategies)}):")
    print(f"  Source seed : {best.strategy.source_seed}")
    print(f"  {result.target_metric} = {best.metric_value}")
    print(f"  Direction   : {result.direction}")
    print(f"  Elapsed     : {result.elapsed_seconds:.1f}s")

    # 6. Inject best strategy into ALL tasks
    injected: list[T] = []
    for task in tasks:
        injected.extend(inject_fn(task, args.attack_type, best.strategy.game_strategies))

    # 7. Save
    print(f"\nSaving {len(injected)} tasks to {output_path}")
    save_fn(injected, output_path)
    print(f"\nDone!\n  Input:  {input_path}\n  Output: {output_path}\n  Tasks:  {len(injected)}")
