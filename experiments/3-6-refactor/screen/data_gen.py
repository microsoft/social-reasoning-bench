"""Generate screening data: filter base tasks to specific IDs, then inject strategies.

Usage:
    uv run python experiments/3-6-refactor/screen/data_gen.py \
        --input data/calendar-scheduling/final/small.yaml \
        --task-ids 20
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
from sage_data_gen.calendar_scheduling.malicious.whimsical.privacy import (
    TASK_DESCRIPTION,
    inject_strategy,
)

EXPERIMENT_DIR = Path(__file__).parent.parent


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Generate screening data")
    p.add_argument("--input", required=True, help="Base tasks YAML")
    p.add_argument("--task-ids", type=int, nargs="+", required=True, help="Task ID(s) to include")
    p.add_argument("--strategies-dir", type=Path, default=EXPERIMENT_DIR / "data/strategies/privacy",
                   help="Dir of raw strategy YAMLs (strategy_0.yaml, strategy_1.yaml, ...)")
    p.add_argument("--output-dir", type=Path, default=EXPERIMENT_DIR / "data/screening-privacy",
                   help="Dir to write strategy-injected task YAMLs")
    p.add_argument("--num-strategies", type=int, default=None, help="Limit number of strategies")
    return p.parse_args()


async def main() -> None:
    args = parse_args()

    # Load and filter tasks
    loaded = load_calendar_tasks([Path(args.input)])
    all_tasks = loaded.all_tasks
    tasks = [t for t in all_tasks if t.id in args.task_ids]
    missing = set(args.task_ids) - {t.id for t in tasks}
    if missing:
        raise ValueError(f"Task ids not found: {missing}")
    print(f"Filtered to {len(tasks)} tasks: {args.task_ids}")

    # Find strategy files
    strategy_files = sorted(args.strategies_dir.glob("strategy_*.yaml"))
    if not strategy_files:
        raise FileNotFoundError(f"No strategy files in {args.strategies_dir}")
    if args.num_strategies:
        strategy_files = strategy_files[: args.num_strategies]

    args.output_dir.mkdir(parents=True, exist_ok=True)
    print(f"Applying {len(strategy_files)} strategies → {args.output_dir}")

    for sf in strategy_files:
        out = args.output_dir / sf.name
        if out.exists():
            print(f"  skip {sf.name} (exists)")
            continue

        print(f"  {sf.name}...")
        provider = StrategyProvider(model="unused", strategies=sf, task=TASK_DESCRIPTION)
        adversarial = await convert_tasks_with_strategies(
            tasks=tasks,
            strategy_provider=provider,
            inject_fn=inject_strategy,
            strategy_assignment="single",
        )
        save_tasks_yaml(adversarial, out)

    print("Done.")


if __name__ == "__main__":
    asyncio.run(main())
