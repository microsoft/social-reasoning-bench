#!/usr/bin/env python3
"""Analyze all results in a directory. Usage: uv run python analyze_config.py [path] [player_name] [--sort {asc,desc}]
Examples:
  uv run python analyze_config.py batch_20251111_184524         # searches in results/batch_*, player="buyer 1"
  uv run python analyze_config.py results/batch_20251111_184524 # absolute path, player="buyer 1"
  uv run python analyze_config.py batch_20251111_184524 "seller_1" # specify player name
  uv run python analyze_config.py batch_20251111_184524 --sort desc # sort by gain descending (default)
  uv run python analyze_config.py batch_20251111_184524 --sort asc # sort by gain ascending
  uv run python analyze_config.py batch_20251111_184524 "buyer_1" --sort desc # with player name and sort
"""
import argparse
import sqlite3
from pathlib import Path

# Parse arguments
parser = argparse.ArgumentParser(description="Analyze simulation results")
parser.add_argument("directory", nargs="?", default="results", help="Results directory (absolute or under results/)")
parser.add_argument("player_name", nargs="?", default="buyer_1", help="Player name to analyze")
parser.add_argument("--sort", choices=["asc", "desc"], help="Sort results by gain (asc=ascending, desc=descending)")
args = parser.parse_args()

# Get directory: absolute path or prefix under results/
results_dir = Path(args.directory) if Path(args.directory).exists() else Path(f"results/{args.directory}")
player_name = args.player_name

# Collect results
results = []

print(f"\n=== Analyzing all results in {results_dir} for player '{player_name}' ===")
for db in sorted(results_dir.glob("*.db")):
    if db.stat().st_size == 0:
        results.append((db.name, None, None, None, None, "EMPTY"))
        continue
    row = sqlite3.connect(db).execute(
        "SELECT coffee_beans, cash, utility_per_bean FROM agents WHERE name=?",
        (player_name,)
    ).fetchone()
    if row:
        gain = (row[0] * row[2] + row[1])
        results.append((db.name, gain, row[0], row[1], row[2], None))
    else:
        results.append((db.name, None, None, None, None, f"Player '{player_name}' not found"))

# Sort by gain if requested
if args.sort:
    reverse = (args.sort == "desc")
    results.sort(key=lambda x: x[1] if x[1] is not None else float('-inf'), reverse=reverse)

# Print results
gains = []
for i, (db_name, gain, beans, cash, utility, error) in enumerate(results, 1):
    if error:
        print(f"  {i}. {db_name}: {error}")
    else:
        gains.append(gain)
        print(f"  {i}. {db_name}: ${gain:.2f} (beans={beans}, cash=${cash:.2f}, utility={utility:.2f})")

print("\n=== Aggregate Statistics ===")
if gains:
    avg = sum(gains)/len(gains)
    print(f"  Average gain: ${avg:.2f}")
    print(f"  Min gain: ${min(gains):.2f}")
    print(f"  Max gain: ${max(gains):.2f}")
    print(f"  Total runs: {len(gains)}")
else:
    print("  No valid results found")
