#!/usr/bin/env python3
"""Generate per-strategy duty-of-care adversarial datasets.

Takes the top 5 duty-of-care strategies (7, 8, 1, 5, 6) from the
2-25-split-whimsical experiment and applies each one individually to
small.yaml, producing 5 single-strategy dataset variants.

Output:
    data/calendar-scheduling/final/malicious-whim-variants/
        small-malicious-whimsical-duty-of-care-strat-1.yaml
        small-malicious-whimsical-duty-of-care-strat-5.yaml
        small-malicious-whimsical-duty-of-care-strat-6.yaml
        small-malicious-whimsical-duty-of-care-strat-7.yaml
        small-malicious-whimsical-duty-of-care-strat-8.yaml

Usage:
    uv run python experiments/3-03-malicious-cal-more/make_datasets.py
    uv run python experiments/3-03-malicious-cal-more/make_datasets.py --dry-run
"""

import argparse
import asyncio
from pathlib import Path

from sage_benchmark.calendar_scheduling.loader import load_calendar_tasks
from sage_data_gen.calendar_scheduling.malicious.whimsical import (
    StrategyProvider,
    convert_tasks_with_strategies,
    save_tasks_yaml,
)
from sage_data_gen.calendar_scheduling.malicious.whimsical.duty_of_care import (
    inject_strategy,
)

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
INPUT_YAML = REPO_ROOT / "data/calendar-scheduling/final/small.yaml"
OUTPUT_DIR = REPO_ROOT / "data/calendar-scheduling/final/malicious-whim-variants"
STRATEGIES_DIR = REPO_ROOT / "experiments/2-25-split-whimsical/strategies/duty_of_care"

STRATEGY_INDICES = [7, 8, 1, 5, 6]


async def generate_single_strategy_dataset(
    strategy_idx: int,
    tasks,
    output_path: Path,
    dry_run: bool = False,
) -> None:
    strategy_file = STRATEGIES_DIR / f"strategy_{strategy_idx}.yaml"
    if not strategy_file.exists():
        print(f"  ERROR: Strategy file not found: {strategy_file}")
        return

    if dry_run:
        print(f"  [DRY RUN] Would generate {output_path.name} using strategy_{strategy_idx}")
        return

    provider = StrategyProvider(
        model="unused",
        strategies=strategy_file,
    )
    await provider.load_or_generate(1)

    adversarial_tasks = await convert_tasks_with_strategies(
        tasks=tasks,
        strategy_provider=provider,
        inject_fn=inject_strategy,
        strategy_assignment="single",
    )

    save_tasks_yaml(adversarial_tasks, output_path)
    print(f"  Created {output_path.name} ({len(adversarial_tasks)} tasks)")


async def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    print(f"Loading tasks from {INPUT_YAML}")
    loaded = load_calendar_tasks([INPUT_YAML])
    tasks = loaded.all_tasks
    print(f"Loaded {len(tasks)} tasks")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for idx in STRATEGY_INDICES:
        output_path = OUTPUT_DIR / f"small-malicious-whimsical-duty-of-care-strat-{idx}.yaml"
        if output_path.exists() and not args.dry_run:
            print(f"  Skipping {output_path.name} (already exists)")
            continue
        await generate_single_strategy_dataset(idx, tasks, output_path, args.dry_run)

    print("\nDone!")


if __name__ == "__main__":
    asyncio.run(main())
