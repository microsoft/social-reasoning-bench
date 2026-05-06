"""CLI entry point for sage-benchmark.

Usage::

    sagebench benchmark calendar [--model gpt-4o ...]
    sagebench benchmark marketplace [--model gpt-4o ...]

    sagebench experiment experiments/ [--collect] [-k PATTERN ...]
    sagebench experiment experiments/ --set model=azure_pool/gpt-5.4
    sagebench experiment experiments/ --set model=azure_pool/gpt-4.1 --and --set model=azure_pool/gpt-5.4
"""

import argparse
import asyncio
import sys
from pathlib import Path
from typing import Any

from .benchmarks.base.benchmark import Benchmark
from .benchmarks.base.types import BaseRunConfig
from .benchmarks.calendar_scheduling import CalendarBenchmark
from .benchmarks.calendar_scheduling.config import CalendarRunConfig
from .benchmarks.marketplace import MarketplaceBenchmark
from .benchmarks.marketplace.config import MarketplaceRunConfig

# ── Registry: config type → benchmark class ──────────────────────────

_CONFIG_TO_BENCHMARK: dict[type[BaseRunConfig], type[Benchmark]] = {
    CalendarRunConfig: CalendarBenchmark,
    MarketplaceRunConfig: MarketplaceBenchmark,
}

_BENCHMARK_BY_NAME: dict[str, type[Benchmark]] = {
    cls.benchmark_name(): cls for cls in [CalendarBenchmark, MarketplaceBenchmark]
}


def _benchmark_factory(config: BaseRunConfig, **kwargs) -> Benchmark:
    """Create the right Benchmark subclass for a given config.

    Args:
        config: A run configuration whose type determines the benchmark class.
        **kwargs: Additional keyword arguments forwarded to the benchmark constructor
            (e.g. ``restart_exec``, ``restart_eval``, ``benchmark_logger``).

    Returns:
        An instantiated ``Benchmark`` subclass matching the config type.

    Raises:
        ValueError: If no benchmark is registered for the given config type.
    """
    for config_cls, benchmark_cls in _CONFIG_TO_BENCHMARK.items():
        if isinstance(config, config_cls):
            return benchmark_cls(config, **kwargs)
    raise ValueError(
        f"No benchmark registered for config type {type(config).__name__}. "
        f"Known types: {[c.__name__ for c in _CONFIG_TO_BENCHMARK]}"
    )


# ── benchmark subcommand ─────────────────────────────────────────────


def _run_benchmark(argv: list[str]) -> None:
    """Parse args and run a single benchmark.

    Args:
        argv: Command-line arguments after ``sagebench benchmark``, where the
            first element is the benchmark name (e.g. ``'calendar'``).
    """
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

    Args:
        argv: Raw command-line arguments to split.

    Returns:
        A list of argument groups, split at each ``--and`` separator.
    """
    groups: list[list[str]] = [[]]
    for arg in argv:
        if arg == "--and":
            groups.append([])
        else:
            groups[-1].append(arg)
    return groups


def _parse_set_overrides(argv: list[str]) -> dict[str, Any]:
    """Extract ``--set KEY=VALUE`` pairs from an argv group.

    Values that look like JSON (lists, dicts, numbers, booleans, null)
    are parsed as such. Everything else is kept as a string.

    Args:
        argv: A single argument group (already split on ``--and``).

    Returns:
        A dict mapping override keys to their coerced values.
    """
    import json

    overrides: dict[str, Any] = {}
    i = 0
    while i < len(argv):
        if argv[i] == "--set" and i + 1 < len(argv):
            key, _, value = argv[i + 1].partition("=")
            if value:
                overrides[key] = _coerce_value(value)
            i += 2
        else:
            i += 1
    return overrides


def _coerce_value(value: str) -> Any:
    """Try to parse a CLI value as JSON; fall back to string.

    Handles CLI-friendly bracket syntax like ``[a,b,c]`` (without quotes)
    by auto-quoting items before JSON parsing.

    Args:
        value: Raw string value from the command line.

    Returns:
        The parsed value as a Python object (list, dict, int, float, bool, None,
        or the original string if no conversion applies).
    """
    import json
    import re

    stripped = value.strip()

    # Handle bracket-list syntax: [a, b, c] → ["a", "b", "c"]
    if stripped.startswith("[") and stripped.endswith("]"):
        inner = stripped[1:-1].strip()
        if not inner:
            return []
        # If already valid JSON, use it directly
        try:
            return json.loads(stripped)
        except (json.JSONDecodeError, ValueError):
            pass
        # Auto-quote unquoted items: split on commas, quote each
        items = [item.strip() for item in inner.split(",")]
        quoted = ", ".join(item if item.startswith('"') else f'"{item}"' for item in items if item)
        try:
            return json.loads(f"[{quoted}]")
        except (json.JSONDecodeError, ValueError):
            pass

    # Handle dict/object syntax
    if stripped.startswith("{") and stripped.endswith("}"):
        try:
            return json.loads(stripped)
        except (json.JSONDecodeError, ValueError):
            pass

    # Handle booleans and null
    if stripped == "true":
        return True
    if stripped == "false":
        return False
    if stripped == "null":
        return None

    # Try numeric
    try:
        if "." in stripped:
            return float(stripped)
        return int(stripped)
    except ValueError:
        pass

    return value


def _strip_set_args(argv: list[str]) -> list[str]:
    """Remove ``--set KEY=VALUE`` pairs so argparse doesn't choke.

    Args:
        argv: Raw command-line arguments that may contain ``--set`` pairs.

    Returns:
        A new argument list with all ``--set KEY=VALUE`` pairs removed.
    """
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
    """Collect experiment files and run them.

    Args:
        argv: Command-line arguments after ``sagebench experiment``, including
            the experiment path, ``--set`` overrides, ``--and`` separators,
            and other flags like ``--collect`` or ``-k``.
    """
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
        "--finalize",
        action="store_true",
        default=False,
        help="Convert checkpoint.json to results.json without running any tasks",
    )
    parser.add_argument(
        "--logger",
        default="progress",
        choices=["verbose", "progress", "quiet"],
        help="Logging style (default: progress)",
    )
    parser.add_argument(
        "--log-level",
        default="warning",
        choices=["debug", "info", "warning", "error"],
        help="Python logging level for library loggers (default: warning)",
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
            finalize=args.finalize,
            logger_style=args.logger,
            log_level=args.log_level,
        )
    )


# ── dashboard subcommand ─────────────────────────────────────────────


def _run_dashboard(argv: list[str]) -> None:
    """Open the interactive results dashboard in the default browser.

    Args:
        argv: Command-line arguments after ``sagebench dashboard`` (currently unused).
    """
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
