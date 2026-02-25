"""CLI for experiment runner.

Usage:
    uv run -m sage_benchmark.calendar_scheduling.experiments experiments/
    uv run -m sage_benchmark.calendar_scheduling.experiments --collect experiments/
    uv run -m sage_benchmark.calendar_scheduling.experiments experiments/ -k "normal"
"""

import argparse
import asyncio
import sys
from pathlib import Path

from .runner import run_multiple


def main() -> int:
    parser = argparse.ArgumentParser(
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
        type=str,
        metavar="PATTERN",
        help="Only run experiments matching this pattern",
    )
    parser.add_argument(
        "--output-base",
        type=Path,
        default=Path("outputs/calendar_scheduling"),
        help="Base directory for experiment outputs (default: outputs/calendar_scheduling)",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=100,
        help="Number of tasks to run concurrently (default: 100)",
    )

    args = parser.parse_args()

    if not args.path.exists():
        print(f"Error: {args.path} not found", file=sys.stderr)
        return 1

    try:
        asyncio.run(
            run_multiple(
                path=args.path,
                output_base=args.output_base,
                pattern=args.k,
                collect_only=args.collect,
                batch_size=args.batch_size,
            )
        )
        return 0
    except KeyboardInterrupt:
        return 130


if __name__ == "__main__":
    sys.exit(main())
