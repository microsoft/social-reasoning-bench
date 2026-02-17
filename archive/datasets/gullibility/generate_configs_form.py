#!/usr/bin/env python3
"""
Generate a single YAML file containing all strategies for form-filling.
Extracts only game_strategies (no grounding_texts) from all strategy files.
"""

from pathlib import Path

import yaml


def main():
    base_dir = Path(__file__).parent
    strategies_dir = base_dir / "output" / "strategies"
    output_file = base_dir / "../../sage-benchmark/data/form-filling/strategies.yaml"

    strategy_files = sorted(strategies_dir.glob("*.yaml"))
    print(f"Found {len(strategy_files)} strategy files")

    all_strategies = []

    for strategy_file in strategy_files:
        print(f"Processing: {strategy_file.name}")

        with open(strategy_file, "r") as f:
            strategy_data = yaml.safe_load(f)

        strategies = strategy_data.get("strategies", [])

        for idx, strategy in enumerate(strategies):
            game_strategy = strategy.get("game_strategies", "")

            if not game_strategy:
                print(f"  Warning: Strategy {idx} has no game_strategies, skipping")
                continue

            all_strategies.append(game_strategy)

    # Write all strategies to a single YAML file
    output_data = {"strategies": all_strategies}

    with open(output_file, "w") as f:
        yaml.dump(output_data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

    print(f"\nSaved {len(all_strategies)} strategies to {output_file}")


if __name__ == "__main__":
    main()
