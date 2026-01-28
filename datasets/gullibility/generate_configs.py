#!/usr/bin/env python3
"""
Generate config files for each strategy in the strategies folder.
Each config file uses the template and replaces buyer_1's private_strategy
with the game_strategies from each strategy.
"""

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
    return name


def main():
    # Define paths
    base_dir = Path(__file__).parent
    strategies_dir = base_dir / "output" / "strategies"
    config_dir = base_dir / "output" / "config"
    template_file = base_dir / "config-template.yaml"

    # Create config directory if it doesn't exist
    config_dir.mkdir(exist_ok=True)

    # Load the template
    with open(template_file, "r") as f:
        template = yaml.safe_load(f)

    # Get all strategy files
    strategy_files = sorted(strategies_dir.glob("*.yaml"))

    print(f"Found {len(strategy_files)} strategy files")

    # Counter for generated configs
    config_count = 0

    # Process each strategy file
    for strategy_file in strategy_files:
        print(f"Processing: {strategy_file.name}")

        # Load the strategy file
        with open(strategy_file, "r") as f:
            strategy_data = yaml.safe_load(f)

        # Get the source article name (for naming)
        source_article = strategy_data.get("source_article", strategy_file.stem)

        # Process each strategy in the file
        strategies = strategy_data.get("strategies", [])

        for idx, strategy in enumerate(strategies):
            game_strategy = strategy.get("game_strategies", "")

            if not game_strategy:
                print(f"  Warning: Strategy {idx} has no game_strategies, skipping")
                continue

            # Get grounding texts if available
            grounding_texts = strategy.get("grounding_texts", "")

            # Combine grounding texts and game strategy
            if grounding_texts:
                combined_strategy = f"# Grounding Texts (from Wikipedia):\n{grounding_texts}\n\n# Strategy:\n{game_strategy}"
            else:
                combined_strategy = game_strategy

            # Create a copy of the template
            config = yaml.safe_load(yaml.dump(template))

            # Replace the private_strategy for buyer_1
            for player in config["players"]:
                if player["name"] == "buyer_1":
                    player["private_strategy"] = combined_strategy
                    break

            # Generate a unique filename
            # Format: source_article_strategy_XXX.yaml
            sanitized_article = sanitize_filename(source_article)
            config_filename = f"{sanitized_article}_strategy_{idx:03d}.yaml"
            config_path = config_dir / config_filename

            # Write the config file
            with open(config_path, "w") as f:
                yaml.dump(config, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

            config_count += 1

    print(f"\nGenerated {config_count} config files in {config_dir}")


if __name__ == "__main__":
    main()
