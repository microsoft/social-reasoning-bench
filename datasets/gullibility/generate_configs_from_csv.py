#!/usr/bin/env python3
"""
Generate config files from private_strategies_list.csv.
Each config file uses the template and replaces seller_1's private_strategy
with a strategy from the CSV.
"""

import csv
import re
from pathlib import Path

import yaml


def sanitize_filename(name):
    """Remove or replace characters that are invalid in filenames."""
    # Replace problematic characters with underscores
    name = re.sub(r'[/\\:*?"<>|]', "_", name)
    # Replace multiple underscores with single underscore
    name = re.sub(r"_+", "_", name)
    # Remove leading/trailing underscores and spaces
    name = name.strip("_ ")
    # Truncate to reasonable length
    if len(name) > 50:
        name = name[:50]
    return name


def main():
    # Define paths
    base_dir = Path(__file__).parent
    csv_file = base_dir / "output" / "private_strategies_list.csv"
    config_dir = base_dir / "output" / "config_private_strategies"
    template_file = base_dir / "config-template.yaml"

    # Create config directory if it doesn't exist
    config_dir.mkdir(parents=True, exist_ok=True)

    # Load the template
    with open(template_file, "r") as f:
        template = yaml.safe_load(f)

    # Read strategies from CSV
    strategies = []
    with open(csv_file, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            strategies.append(row)

    print(f"Found {len(strategies)} strategies in CSV")

    # Counter for generated configs
    config_count = 0

    # Process each strategy
    for idx, row in enumerate(strategies):
        strategy_text = row["strategy"]
        source = row["source"]

        if not strategy_text:
            print(f"  Warning: Strategy {idx} is empty, skipping")
            continue

        # Create a copy of the template
        config = yaml.safe_load(yaml.dump(template))

        # Replace the private_strategy for buyer_1
        for player in config["players"]:
            if player["name"] == "buyer_1":
                player["private_strategy"] = strategy_text
                break

        # Generate a unique filename
        # Format: source_strategy_XXX.yaml
        sanitized_source = sanitize_filename(source)
        config_filename = f"{sanitized_source}_strategy_{idx:04d}.yaml"
        config_path = config_dir / config_filename

        # Write the config file
        with open(config_path, "w") as f:
            yaml.dump(config, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

        config_count += 1

    print(f"\nGenerated {config_count} config files in {config_dir}")


if __name__ == "__main__":
    main()
