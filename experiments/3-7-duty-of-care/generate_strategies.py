"""Generate 100 WhimsyGen strategies for double-booking attacks.

Each strategy is saved as a separate YAML file (strategy_0.yaml, strategy_1.yaml, ...).

Usage:
    uv run python experiments/3-7-duty-of-care/generate_strategies.py --count 100
    uv run python experiments/3-7-duty-of-care/generate_strategies.py --count 100 -m gemini-3.1-pro-preview
"""

import argparse
import asyncio
from pathlib import Path

import yaml
from sage_data_gen.calendar_scheduling.malicious.whimsical.double_booking import TASK_DESCRIPTION
from whimsygen import WhimsyGen

EXPERIMENT_DIR = Path(__file__).parent


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Generate double-booking strategies")
    p.add_argument("--count", type=int, default=100, help="Number of strategies to generate")
    p.add_argument(
        "-m", "--model", default="gemini-3.1-pro-preview", help="Model for strategy generation"
    )
    p.add_argument(
        "--output-dir",
        type=Path,
        default=EXPERIMENT_DIR / "data/strategies/duty-of-care",
        help="Output directory for strategy YAMLs",
    )
    p.add_argument(
        "--seeds-dir",
        type=Path,
        default=Path("data/whimsygen/seeds"),
        help="Directory with WhimsyGen seed YAMLs",
    )
    return p.parse_args()


async def main() -> None:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    wg = WhimsyGen(model=args.model, seeds=args.seeds_dir, task=TASK_DESCRIPTION)

    print(f"Generating {args.count} strategies using {args.model}...")
    strategies = await wg.sample(n=args.count)
    print(f"Generated {len(strategies)} strategies")

    # Save each strategy as a separate file
    for i, strategy in enumerate(strategies):
        out_path = args.output_dir / f"strategy_{i}.yaml"
        data = {
            "strategies": [
                {
                    "game_strategies": strategy.game_strategies,
                    "grounding_texts": strategy.grounding_texts,
                    "source_seed": strategy.source_seed,
                    "source_chunk": strategy.source_chunk,
                }
            ]
        }
        with open(out_path, "w") as f:
            yaml.dump(
                data, f, default_flow_style=False, sort_keys=False, allow_unicode=True, width=120
            )

    print(f"Saved {len(strategies)} strategy files to {args.output_dir}")


if __name__ == "__main__":
    asyncio.run(main())
