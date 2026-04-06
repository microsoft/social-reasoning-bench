import argparse
import asyncio
import sys
from pathlib import Path
from types import ModuleType

from sage_data_gen.calendar_scheduling.cli import main as calendar_main
from sage_data_gen.form_filling.cli import main as form_filling_main
from sage_data_gen.marketplace.cli import main as marketplace_main

SUBCOMMANDS = ("calendar", "form-filling", "marketplace", "malicious")
BENCHMARKS = ("calendar", "form-filling", "marketplace")


# ---------------------------------------------------------------------------
# sagegen malicious
# ---------------------------------------------------------------------------


def _get_malicious_module(benchmark: str) -> ModuleType:
    """Import and return the malicious module for a benchmark."""
    if benchmark == "calendar":
        from sage_data_gen.calendar_scheduling import malicious as mod
    elif benchmark == "form-filling":
        from sage_data_gen.form_filling import malicious as mod
    else:
        from sage_data_gen.marketplace import malicious as mod
    return mod


def _build_malicious_parser() -> argparse.ArgumentParser:
    """Build the unified parser for ``sagegen malicious``."""
    from sage_data_gen.shared.whimsical import DEFAULT_SEEDS_DIR

    parser = argparse.ArgumentParser(
        prog="sagegen malicious",
        description="Generate malicious task variants (whimsical).",
    )
    parser.add_argument("benchmark", choices=BENCHMARKS)

    parser.add_argument("--input", type=Path, required=True, help="Input tasks file/dir")
    parser.add_argument("--attack-type", default=None, help="Attack type (omit for all)")
    parser.add_argument("-o", "--output", type=Path, default=None, help="Output path")

    # Whimsical options
    whim = parser.add_argument_group("whimsical options")
    whim.add_argument("-m", "--model", default=None, help="Model for strategy generation")
    whim.add_argument(
        "--reasoning-effort", default=None, help="Reasoning effort for strategy generation model"
    )
    whim.add_argument("-n", "--count", type=int, default=1, help="Strategies to generate")
    whim.add_argument(
        "--strategy-assignment",
        choices=["sequential", "random", "unique", "single"],
        default="single",
    )
    whim.add_argument("--seeds-dir", type=Path, default=DEFAULT_SEEDS_DIR)
    whim.add_argument("--topics", nargs="+")
    whim.add_argument("--seed-chunk-size", type=int, default=5000)
    whim.add_argument("--max-chunks-per-seed", type=int)
    whim.add_argument("--max-strategies-per-chunk", type=int)
    whim.add_argument("--max-strategies-per-seed", type=int)
    whim.add_argument("--prefetch-seeds", type=int)
    whim.add_argument("--prefetch-strategies", type=int)
    whim.add_argument("--strategies-file", type=Path)
    whim.add_argument("--rng-seed", type=int, default=42)

    # Validation options (generate → benchmark → select best)
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
        help="Number of candidate strategies to generate for validation",
    )
    val.add_argument("--agent-model", default=None, help="Model for the agent under test")
    val.add_argument("--agent-reasoning-effort", default=None, help="Reasoning effort for agent")
    val.add_argument(
        "--agent-cot",
        action="store_true",
        default=False,
        help="Enable explicit chain-of-thought for agent",
    )
    val.add_argument("--judge-model", default=None, help="Model for the evaluation judge")
    val.add_argument("--judge-reasoning-effort", default=None, help="Reasoning effort for judge")
    val.add_argument("--val-tasks-data", type=Path, default=None, help="Validation task YAML")
    val.add_argument("--val-tasks-limit", type=int, default=None, help="Max validation tasks")
    val.add_argument("--val-output-dir", type=Path, default=None, help="Validation output dir")
    val.add_argument(
        "--batch-size", type=int, default=100, help="Max concurrent tasks (default: 100)"
    )
    val.add_argument(
        "--task-concurrency", type=int, default=None, help="Max concurrent LLM calls per task"
    )
    val.add_argument(
        "--llm-concurrency",
        type=int,
        default=None,
        help="Max total concurrent LLM calls per provider",
    )
    val.add_argument(
        "--logger",
        default="progress",
        choices=["progress", "verbose", "quiet"],
        help="Logger style for validation benchmark (default: progress)",
    )
    val.add_argument(
        "--log-level",
        default="info",
        choices=["debug", "info", "warning", "error"],
        help="Python log level for benchmark loggers (default: info)",
    )

    return parser


async def _run_whimsical(benchmark: str, attack_type: str, args: argparse.Namespace) -> None:
    """Run whimsical injection for a single (benchmark, attack_type) — non-validation path."""
    from sage_data_gen.shared.whimsical import run_injection

    mod = _get_malicious_module(benchmark)
    task_desc = mod.TASK_DESCRIPTIONS[attack_type]

    injection_args = argparse.Namespace(
        input=args.input,
        output=args.output,
        attack_type=attack_type,
        model=args.model,
        reasoning_effort=args.reasoning_effort,
        count=args.count,
        strategy_assignment=args.strategy_assignment,
        seeds_dir=args.seeds_dir,
        topics=args.topics,
        seed_chunk_size=args.seed_chunk_size,
        max_chunks_per_seed=args.max_chunks_per_seed,
        max_strategies_per_chunk=args.max_strategies_per_chunk,
        max_strategies_per_seed=args.max_strategies_per_seed,
        prefetch_seeds=args.prefetch_seeds,
        prefetch_strategies=args.prefetch_strategies,
        strategies_file=args.strategies_file,
        rng_seed=args.rng_seed,
    )
    await run_injection(
        injection_args,
        task_desc,
        mod.load,
        mod.inject_whimsical,
        mod.save,
        benchmark_name=benchmark,
    )


def _malicious_main():
    """``sagegen malicious {benchmark} [opts]``."""
    parser = _build_malicious_parser()
    args = parser.parse_args()

    if not args.model:
        parser.error("-m/--model is required for whimsical generation")

    if args.attack_type is None and args.output is not None:
        parser.error("--output cannot be used when running all attack types")

    mod = _get_malicious_module(args.benchmark)
    attack_types = mod.WHIMSICAL_ATTACK_TYPES
    types = [args.attack_type] if args.attack_type else attack_types

    if args.validate:
        # Default agent/judge model to -m/--model when not explicitly set.
        if not args.agent_model:
            args.agent_model = args.model
        if not args.judge_model:
            args.judge_model = args.model
        if not args.val_tasks_data:
            parser.error("--val-tasks-data is required when --validate is used")

        # Pooled validation: all attack types in one ExperimentPoolExecutor
        from sage_data_gen.shared.whimsical import run_pooled_validation

        asyncio.run(
            run_pooled_validation(
                args,
                attack_types=list(types),
                benchmark_name=args.benchmark,
                load_fn=mod.load,
                inject_fn=mod.inject_whimsical,
                save_fn=mod.save,
            )
        )
        return

    # Non-validation: run each attack type independently
    from sage_benchmark.shared import TaskPoolExecutor

    combos = list(types)

    async def _run_combo(attack_type: str) -> str:
        label = f"{args.benchmark} / whimsical / {attack_type}"
        print(f"\n{'=' * 60}\n  {label}\n{'=' * 60}\n")
        await _run_whimsical(args.benchmark, attack_type, args)
        return label

    async def _run_all() -> None:
        cancel = asyncio.Event()
        errors: list[Exception] = []

        def _on_error(exc: Exception) -> None:
            errors.append(exc)
            print(f"\n  [FAILED] {exc}")
            cancel.set()

        executor = TaskPoolExecutor(
            batch_size=len(combos),
            on_task_complete=lambda label: print(f"\n  [done] {label}"),
            on_task_error=_on_error,
            cancel_event=cancel,
        )
        await executor.run(_run_combo(at) for at in combos)

        if errors:
            raise errors[0]

    asyncio.run(_run_all())


# ---------------------------------------------------------------------------
# Top-level router
# ---------------------------------------------------------------------------


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in SUBCOMMANDS:
        print(f"Usage: sagegen {{{','.join(SUBCOMMANDS)}}} [options]")
        sys.exit(1)

    subcommand = sys.argv[1]
    sys.argv = [f"sagegen {subcommand}"] + sys.argv[2:]

    if subcommand == "calendar":
        calendar_main()
    elif subcommand == "form-filling":
        form_filling_main()
    elif subcommand == "marketplace":
        marketplace_main()
    elif subcommand == "malicious":
        _malicious_main()
