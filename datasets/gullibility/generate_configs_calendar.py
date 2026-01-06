#!/usr/bin/env python3
"""
Generate calendar config files by appending strategies to Bob's instruction_message.
Uses email-verification-test.yaml as the template.
"""

import re
from pathlib import Path

import yaml


def sanitize_filename(name):
    """Remove or replace characters that are invalid in filenames."""
    name = re.sub(r'[/\\:*?"<>|]', "_", name)
    name = re.sub(r"_+", "_", name)
    name = name.strip("_ ")
    return name


def main():
    base_dir = Path(__file__).parent
    strategies_dir = base_dir / "strategies_calendar"
    config_dir = base_dir / "config_calendar"
    template_file = (
        base_dir / "../../sage-benchmark/data/calendar-scheduling/email-verification-test.yaml"
    )

    config_dir.mkdir(exist_ok=True)

    # Load the template
    with open(template_file, "r") as f:
        template = yaml.safe_load(f)

    strategy_files = sorted(strategies_dir.glob("*.yaml"))
    print(f"Found {len(strategy_files)} strategy files")

    config_count = 0

    for strategy_file in strategy_files:
        print(f"Processing: {strategy_file.name}")

        with open(strategy_file, "r") as f:
            strategy_data = yaml.safe_load(f)

        source_article = strategy_data.get("source_article", strategy_file.stem)
        strategies = strategy_data.get("strategies", [])

        for idx, strategy in enumerate(strategies):
            game_strategy = strategy.get("game_strategies", "")

            if not game_strategy:
                print(f"  Warning: Strategy {idx} has no game_strategies, skipping")
                continue

            # Create a copy of the template
            config = yaml.safe_load(yaml.dump(template))

            # Find Bob's task (requestor) and append strategy to instruction_message
            for task in config["tasks"]:
                requestor = task.get("requestor", {})
                if "bob" in requestor.get("email", "").lower():
                    original_instruction = requestor.get("instruction_message", "")
                    requestor["instruction_message"] = (
                        f"{original_instruction}\n\nStrategy:\n{game_strategy}"
                    )
                    break

            # Generate filename
            sanitized_article = sanitize_filename(source_article)
            config_filename = f"{sanitized_article}_strategy_{idx:03d}.yaml"
            config_path = config_dir / config_filename

            with open(config_path, "w") as f:
                yaml.dump(config, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

            config_count += 1

    print(f"\nGenerated {config_count} config files in {config_dir}")


if __name__ == "__main__":
    main()
