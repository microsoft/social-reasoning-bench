"""CLI entry point for sage-benchmark.

Usage::

    sagebench benchmark calendar [--model gpt-4o ...]
    sagebench benchmark marketplace [--model gpt-4o ...]
    sagebench benchmark form_filling [--model gpt-4o ...]

    sagebench experiment experiments/ [--collect] [-k PATTERN ...]
    sagebench experiment experiments/ --set model=trapi/gpt-5.4
    sagebench experiment experiments/ --set model=trapi/gpt-4.1 --and --set model=trapi/gpt-5.4
"""

import argparse
import asyncio
import sys
from pathlib import Path

from .benchmarks.base.benchmark import Benchmark
from .benchmarks.base.types import BaseRunConfig
from .benchmarks.calendar_scheduling import CalendarBenchmark
from .benchmarks.calendar_scheduling.config import CalendarRunConfig
from .benchmarks.form_filling import FormFillingBenchmark
from .benchmarks.form_filling.config import FormFillingRunConfig
from .benchmarks.marketplace import MarketplaceBenchmark
from .benchmarks.marketplace.config import MarketplaceRunConfig

# ── Registry: config type → benchmark class ──────────────────────────

_CONFIG_TO_BENCHMARK: dict[type[BaseRunConfig], type[Benchmark]] = {
    CalendarRunConfig: CalendarBenchmark,
    MarketplaceRunConfig: MarketplaceBenchmark,
    FormFillingRunConfig: FormFillingBenchmark,
}

_BENCHMARK_BY_NAME: dict[str, type[Benchmark]] = {
    cls.benchmark_name(): cls
    for cls in [CalendarBenchmark, MarketplaceBenchmark, FormFillingBenchmark]
}


def _benchmark_factory(config: BaseRunConfig, **kwargs) -> Benchmark:
    """Create the right Benchmark subclass for a given config."""
    for config_cls, benchmark_cls in _CONFIG_TO_BENCHMARK.items():
        if isinstance(config, config_cls):
            return benchmark_cls(config, **kwargs)
    raise ValueError(
        f"No benchmark registered for config type {type(config).__name__}. "
        f"Known types: {[c.__name__ for c in _CONFIG_TO_BENCHMARK]}"
    )


# ── benchmark subcommand ─────────────────────────────────────────────


def _run_benchmark(argv: list[str]) -> None:
    """Parse args and run a single benchmark."""
    if not argv or argv[0] not in _BENCHMARK_BY_NAME:
        names = ", ".join(_BENCHMARK_BY_NAME)
        print(f"Usage: sagebench benchmark {{{names}}} [options]", file=sys.stderr)
        sys.exit(1)

    benchmark_cls = _BENCHMARK_BY_NAME[argv[0]]

    # Let the benchmark own the rest of argv
    sys.argv = [f"sagebench benchmark {argv[0]}"] + argv[1:]
    benchmark_cls.main()


# ── experiment subcommand ────────────────────────────────────────────


def _split_on_and(argv: list[str]) -> list[list[str]]:
    """Split argv on ``--and`` separator into groups.

    Example::

        ['experiments/', '--set', 'model=X', '--and', '--set', 'model=Y']
        -> [['experiments/', '--set', 'model=X'], ['--set', 'model=Y']]
    """
    groups: list[list[str]] = [[]]
    for arg in argv:
        if arg == "--and":
            groups.append([])
        else:
            groups[-1].append(arg)
    return groups


def _parse_set_overrides(argv: list[str]) -> dict[str, str]:
    """Extract ``--set KEY=VALUE`` pairs from an argv group."""
    overrides: dict[str, str] = {}
    i = 0
    while i < len(argv):
        if argv[i] == "--set" and i + 1 < len(argv):
            key, _, value = argv[i + 1].partition("=")
            if value:
                overrides[key] = value
            i += 2
        else:
            i += 1
    return overrides


def _strip_set_args(argv: list[str]) -> list[str]:
    """Remove ``--set KEY=VALUE`` pairs so argparse doesn't choke."""
    cleaned: list[str] = []
    i = 0
    while i < len(argv):
        if argv[i] == "--set" and i + 1 < len(argv):
            i += 2  # skip --set and its value
        else:
            cleaned.append(argv[i])
            i += 1
    return cleaned


def _run_experiment(argv: list[str]) -> None:
    """Collect experiment files and run them."""
    from .experiments.runner import run_multiple

    # Split on --and before argparse sees anything
    arg_groups = _split_on_and(argv)

    # Extract --set overrides from each group
    override_groups = [_parse_set_overrides(group) for group in arg_groups]

    # If all groups are empty, no overrides
    has_overrides = any(g for g in override_groups)
    final_override_groups = override_groups if has_overrides else None

    # Parse base args from first group (strip --set so argparse doesn't error)
    parser = argparse.ArgumentParser(
        prog="sagebench experiment",
        description="Run experiments defined in Python modules",
    )
    parser.add_argument(
        "path",
        type=Path,
        help="Path to experiment file or directory to search recursively",
    )
    parser.add_argument(
        "--collect",
        action="store_true",
        help="Collect and list experiments without running them",
    )
    parser.add_argument(
        "-k",
        action="append",
        metavar="PATTERN",
        help="Only run experiments matching this pattern (repeatable)",
    )
    parser.add_argument(
        "--output-base",
        type=Path,
        default=None,
        help="Base directory for experiment outputs",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=100,
        help="Number of tasks to run concurrently (default: 100)",
    )
    parser.add_argument(
        "--task-concurrency",
        type=int,
        default=None,
        help="Max concurrent LLM calls per task per provider (default: unlimited)",
    )
    parser.add_argument(
        "--llm-concurrency",
        type=int,
        default=None,
        help="Max total concurrent LLM calls per provider across all tasks (default: unlimited)",
    )
    parser.add_argument(
        "--restart-exec",
        action="store_true",
        default=False,
        help="Re-run execution (ignore checkpointed execution progress)",
    )
    parser.add_argument(
        "--restart-eval",
        action="store_true",
        default=False,
        help="Re-run evaluation (ignore checkpointed evaluation progress)",
    )
    parser.add_argument(
        "--logger",
        default="progress",
        choices=["verbose", "progress", "quiet"],
        help="Logging style (default: progress)",
    )
    parser.add_argument(
        "--log-level",
        default="info",
        choices=["debug", "info", "warning", "error"],
        help="Python logging level for library loggers (default: info)",
    )

    args = parser.parse_args(_strip_set_args(arg_groups[0]))

    if not args.path.exists():
        print(f"Error: {args.path} not found", file=sys.stderr)
        sys.exit(1)

    if has_overrides:
        for i, overrides in enumerate(override_groups):
            label = ", ".join(f"{k}={v}" for k, v in overrides.items()) or "(base)"
            print(f"  Override group {i + 1}: {label}")

    if args.collect:
        from .experiments.collect import collect_all

        configs = collect_all(args.path, patterns=args.k, override_groups=final_override_groups)
        if not configs:
            print("No experiments found.")
            return
        print(f"Found {len(configs)} experiments:")
        for _, name, config in configs:
            bm_type = type(config).__name__
            print(f"  {name}  ({bm_type})")
        return

    asyncio.run(
        run_multiple(
            benchmark_factory=_benchmark_factory,
            path=args.path,
            output_base=args.output_base,
            patterns=args.k,
            override_groups=final_override_groups,
            batch_size=args.batch_size,
            task_concurrency=args.task_concurrency,
            llm_concurrency=args.llm_concurrency,
            restart_exec=args.restart_exec,
            restart_eval=args.restart_eval,
            logger_style=args.logger,
            log_level=args.log_level,
        )
    )


# ── dashboard subcommand ─────────────────────────────────────────────


def _run_dashboard(argv: list[str]) -> None:
    """Open the interactive results dashboard in the default browser."""
    import webbrowser

    from .dashboard import get_dashboard_path

    path = get_dashboard_path()
    url = path.as_uri() if hasattr(path, "as_uri") else f"file://{path}"
    print(f"Opening dashboard: {url}")
    webbrowser.open(url)


# ── main ─────────────────────────────────────────────────────────────

_SUBCOMMANDS = ("benchmark", "experiment", "dashboard")


def main() -> None:
    if len(sys.argv) < 2 or sys.argv[1] not in _SUBCOMMANDS:
        print(f"Usage: sagebench {{{','.join(_SUBCOMMANDS)}}} ...", file=sys.stderr)
        sys.exit(1)

    subcommand = sys.argv[1]
    rest = sys.argv[2:]

    if subcommand == "benchmark":
        _run_benchmark(rest)
    elif subcommand == "experiment":
        _run_experiment(rest)
    elif subcommand == "dashboard":
        _run_dashboard(rest)
