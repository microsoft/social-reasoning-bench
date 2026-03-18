"""Generate validation data: inject the winning strategy into all tasks.

Reads the winner from screening results, then applies that strategy
to every task in the base dataset.

Usage:
    uv run python experiments/3-6-refactor/experiment/data_gen.py \
        --input data/calendar-scheduling/final/large.yaml
"""

import argparse
import asyncio
import json
from pathlib import Path

from sage_benchmark.calendar_scheduling.loader import load_calendar_tasks
from sage_data_gen.calendar_scheduling.malicious.whimsical import (
    StrategyProvider,
    convert_tasks_with_strategies,
    save_tasks_yaml,
)
from sage_data_gen.calendar_scheduling.malicious.whimsical.privacy import (
    TASK_DESCRIPTION,
    inject_strategy,
)

EXPERIMENT_DIR = Path(__file__).parent.parent


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Generate validation data")
    p.add_argument("--input", required=True, help="Base tasks YAML (e.g. large.yaml)")
    p.add_argument("--strategies-dir", type=Path, default=EXPERIMENT_DIR / "data/strategies/privacy",
                   help="Dir of raw strategy YAMLs")
    p.add_argument("--output-dir", type=Path, default=EXPERIMENT_DIR / "data/validation-privacy",
                   help="Dir to write strategy-injected task YAML")
    p.add_argument("--force-strategy", type=str, default=None,
                   help="Override winner (e.g. strategy_40)")
    return p.parse_args()


async def main() -> None:
    args = parse_args()

    # Determine winner
    if args.force_strategy:
        winner = args.force_strategy
    else:
        results_path = EXPERIMENT_DIR / "results" / "screening_results.json"
        if not results_path.exists():
            raise FileNotFoundError(f"No screening results at {results_path}. Run screen.py first or use --force-strategy.")
        winner = json.loads(results_path.read_text())["winner"]

    strategy_file = args.strategies_dir / f"{winner}.yaml"
    if not strategy_file.exists():
        raise FileNotFoundError(f"Strategy file not found: {strategy_file}")

    # Load all tasks
    loaded = load_calendar_tasks([Path(args.input)])
    tasks = loaded.all_tasks
    print(f"Loaded {len(tasks)} tasks from {args.input}")
    print(f"Injecting winner: {winner}")

    # Inject strategy
    args.output_dir.mkdir(parents=True, exist_ok=True)
    out = args.output_dir / f"{winner}.yaml"
    if out.exists():
        print(f"Already exists: {out}")
        return

    provider = StrategyProvider(model="unused", strategies=strategy_file, task=TASK_DESCRIPTION)
    adversarial = await convert_tasks_with_strategies(
        tasks=tasks,
        strategy_provider=provider,
        inject_fn=inject_strategy,
        strategy_assignment="single",
    )
    save_tasks_yaml(adversarial, out)
    print(f"Wrote {len(adversarial)} tasks → {out}")


if __name__ == "__main__":
    asyncio.run(main())
