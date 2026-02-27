#!/usr/bin/env python3
"""Generate N unique whimsygen strategies for privacy and duty-of-care attacks separately.

Usage:
    uv run --package sage-data-gen python experiments/2-25-split-whimsical/generate_strategies.py -n 10
    uv run --package sage-data-gen python experiments/2-25-split-whimsical/generate_strategies.py -n 10 -m openai/gpt-4.1
    uv run --package sage-data-gen python experiments/2-25-split-whimsical/generate_strategies.py -n 10 --task privacy
    uv run --package sage-data-gen python experiments/2-25-split-whimsical/generate_strategies.py -n 10 --task duty_of_care
    uv run --package sage-data-gen python experiments/2-25-split-whimsical/generate_strategies.py -n 10 -v  # verbose
"""

import argparse
import asyncio
import logging
from pathlib import Path

import yaml
from whimsygen import WhimsyGen


def setup_logging(verbose: bool) -> None:
    """Configure logging verbosity."""
    if verbose:
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s %(name)s %(levelname)s: %(message)s",
            datefmt="%H:%M:%S",
        )
        logging.getLogger("LiteLLM").setLevel(logging.DEBUG)
    else:
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s %(levelname)s: %(message)s",
            datefmt="%H:%M:%S",
        )


from sage_data_gen.calendar_scheduling.malicious.whimsical.duty_of_care import (
    TASK_DESCRIPTION as DUTY_OF_CARE_TASK,
)
from sage_data_gen.calendar_scheduling.malicious.whimsical.privacy import (
    TASK_DESCRIPTION as PRIVACY_TASK,
)

TASKS = {
    "privacy": PRIVACY_TASK,
    "duty_of_care": DUTY_OF_CARE_TASK,
}


async def generate_strategies(
    n: int,
    model: str,
    seeds_dir: Path,
    output_dir: Path,
    task_text: str,
    task_label: str,
) -> None:
    """Generate N unique strategies and save each to a separate file."""
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Generating {n} {task_label} strategies using {model}...")
    print(f"Seeds directory: {seeds_dir}")
    print(f"Output directory: {output_dir}")
    print()

    wg = WhimsyGen(
        model=model,
        seeds=seeds_dir,
        task=task_text,
    )

    # Stream strategies as they're generated for progress visibility
    strategies = []
    async for strategy in wg.isample(max_strategies=n, max_strategies_per_seed=1):
        i = len(strategies)
        strategies.append(strategy)

        # Save in StrategyCollection format
        output_file = output_dir / f"strategy_{i}.yaml"
        strategy_dict = {
            "strategies": [strategy.model_dump()],
        }

        with open(output_file, "w") as f:
            yaml.dump(strategy_dict, f, default_flow_style=False, allow_unicode=True, width=120)

        # Verbose progress
        seed_title = strategy.source_seed
        strategy_preview = strategy.game_strategies[:80].replace("\n", " ") + "..."
        print(f"[{i + 1}/{n}] Generated from '{seed_title}'")
        print(f"       {strategy_preview}")
        print(f"       Saved to {output_file.name}")
        print()

        if len(strategies) >= n:
            break

    print(f"Done! Generated {len(strategies)} {task_label} strategies.")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate N unique whimsygen strategies for privacy and/or duty-of-care"
    )
    parser.add_argument(
        "-n", "--num-strategies", type=int, default=10, help="Number of strategies to generate"
    )
    parser.add_argument(
        "-m", "--model", default="gemini-3-flash-preview", help="Model to use for generation"
    )
    parser.add_argument(
        "--seeds-dir",
        type=Path,
        default=Path("data/whimsygen/seeds"),
        help="Directory for Wikipedia seeds (default: data/whimsygen/seeds)",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        type=Path,
        default=Path("experiments/2-25-split-whimsical/strategies"),
        help="Base output directory for strategy files",
    )
    parser.add_argument(
        "--task",
        choices=["privacy", "duty_of_care", "both"],
        default="both",
        help="Which task to generate strategies for (default: both)",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose debug logging",
    )

    args = parser.parse_args()

    setup_logging(args.verbose)

    tasks_to_run = list(TASKS.keys()) if args.task == "both" else [args.task]

    for task_name in tasks_to_run:
        asyncio.run(
            generate_strategies(
                n=args.num_strategies,
                model=args.model,
                seeds_dir=args.seeds_dir,
                output_dir=args.output_dir / task_name,
                task_text=TASKS[task_name],
                task_label=task_name,
            )
        )

    # Force exit - LiteLLM aiohttp sessions don't close cleanly and hang asyncio.run()
    raise SystemExit(0)


if __name__ == "__main__":
    main()
