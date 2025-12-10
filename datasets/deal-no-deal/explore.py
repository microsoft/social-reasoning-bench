"""
Script to explore and analyze Deal-No-Deal dataset files.
Reads data from train.txt, test.txt, val.txt, or hard.txt and displays it in a readable format.
"""

import argparse
import os
import sys
from typing import Dict, List

from utils.deal_no_deal_metrics import (
    check_envy_free,
    check_pareto_optimalities,
    compute_score,
    gen_choices,
    process_data,
    translate_values,
)


def load_and_parse_data(filepath: str, max_samples: int = None) -> List[Dict]:
    """
    Load and parse data from a Deal-No-Deal dataset file.

    Args:
        filepath: Path to the data file
        max_samples: Maximum number of samples to load (None for all)

    Returns:
        List of parsed data dictionaries
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")

    with open(filepath, "r") as f:
        lines = f.readlines()

    # Remove repetitive lines (every other line is duplicate)
    lines = [line.strip() for i, line in enumerate(lines) if i % 2 == 0]

    if max_samples:
        lines = lines[:max_samples]

    parsed_data = []

    for idx, line in enumerate(lines):
        if not line:
            continue

        try:
            # Parse the line
            (
                example_count,
                agent1_values,
                agent1_values_text,
                agent2_values,
                agent2_values_text,
                agent1_human_outcomes,
                agent2_human_outcomes,
            ) = process_data(line)

            # Check if outcomes contain special tokens indicating no agreement
            special_tokens = ["<disagree>", "<no_agreement>", "<disconnect>"]
            has_special_token = (
                agent1_human_outcomes
                and isinstance(agent1_human_outcomes[0], str)
                and agent1_human_outcomes[0] in special_tokens
            ) or (
                agent2_human_outcomes
                and isinstance(agent2_human_outcomes[0], str)
                and agent2_human_outcomes[0] in special_tokens
            )

            if has_special_token:
                # Skip scenarios with failed negotiations
                continue

            # Compute human scores
            agent1_human_score = compute_score(agent1_values, agent1_human_outcomes)
            agent2_human_score = compute_score(agent2_values, agent2_human_outcomes)

            # Check if human outcome is Pareto optimal
            is_pareto_optimal = check_pareto_optimalities(
                agent1_human_outcomes,
                agent1_values,
                agent2_human_outcomes,
                agent2_values,
                example_count,
                do_print=False,
            )

            # Check if human outcome is envy-free
            is_envy_free = check_envy_free(agent1_human_outcomes, agent2_human_outcomes, line)

            parsed_data.append(
                {
                    "index": idx,
                    "example_count": example_count,
                    "agent1_values": agent1_values,
                    "agent2_values": agent2_values,
                    "agent1_human_outcomes": agent1_human_outcomes,
                    "agent2_human_outcomes": agent2_human_outcomes,
                    "agent1_human_score": int(agent1_human_score),
                    "agent2_human_score": int(agent2_human_score),
                    "is_pareto_optimal": is_pareto_optimal,
                    "is_envy_free": is_envy_free,
                    "raw_line": line,
                }
            )
        except Exception as e:
            print(f"Warning: Failed to parse line {idx}: {e}")
            continue

    return parsed_data


def display_scenario(data: Dict, show_raw: bool = False):
    """Display a single scenario in a readable format."""
    print(f"\n{'=' * 70}")
    print(f"Scenario #{data['index']}")
    print(f"{'=' * 70}")

    # Display item counts
    print(f"\n📦 Available Items:")
    print(f"  Books: {data['example_count'][0]}")
    print(f"  Hats:  {data['example_count'][1]}")
    print(f"  Balls: {data['example_count'][2]}")

    # Display agent values
    print(f"\n💎 Agent 1 Values (points per item):")
    print(f"  Books: {data['agent1_values'][0]}")
    print(f"  Hats:  {data['agent1_values'][1]}")
    print(f"  Balls: {data['agent1_values'][2]}")
    total_value_1 = sum(v * c for v, c in zip(data["agent1_values"], data["example_count"]))
    print(f"  Total possible value: {total_value_1}")

    print(f"\n💎 Agent 2 Values (points per item):")
    print(f"  Books: {data['agent2_values'][0]}")
    print(f"  Hats:  {data['agent2_values'][1]}")
    print(f"  Balls: {data['agent2_values'][2]}")
    total_value_2 = sum(v * c for v, c in zip(data["agent2_values"], data["example_count"]))
    print(f"  Total possible value: {total_value_2}")

    # Display human outcomes
    print(f"\n🤝 Human Negotiation Outcome:")
    print(
        f"  Agent 1 gets: {data['agent1_human_outcomes'][0]} books, {data['agent1_human_outcomes'][1]} hats, {data['agent1_human_outcomes'][2]} balls"
    )
    print(
        f"  Agent 2 gets: {data['agent2_human_outcomes'][0]} books, {data['agent2_human_outcomes'][1]} hats, {data['agent2_human_outcomes'][2]} balls"
    )
    print(f"  Agent 1 score: {data['agent1_human_score']}")
    print(f"  Agent 2 score: {data['agent2_human_score']}")
    print(f"  Total score: {data['agent1_human_score'] + data['agent2_human_score']}")

    # Display analysis
    print(f"\n📊 Outcome Analysis:")
    print(f"  Pareto Optimal: {'✓ Yes' if data['is_pareto_optimal'] else '✗ No'}")
    print(f"  Envy-Free:      {'✓ Yes' if data['is_envy_free'] else '✗ No'}")

    if show_raw:
        print(f"\n📝 Raw Data:")
        print(f"  {data['raw_line'][:100]}...")


def display_summary_stats(data_list: List[Dict], filename: str):
    """Display summary statistics for the dataset."""
    print(f"\n{'=' * 70}")
    print(f"Dataset Summary: {filename}")
    print(f"{'=' * 70}")

    total_scenarios = len(data_list)
    print(f"\n📈 General Statistics:")
    print(f"  Total scenarios: {total_scenarios}")

    # Pareto optimal percentage
    pareto_count = sum(1 for d in data_list if d["is_pareto_optimal"])
    pareto_pct = (pareto_count / total_scenarios * 100) if total_scenarios > 0 else 0
    print(f"  Pareto optimal outcomes: {pareto_count} ({pareto_pct:.1f}%)")

    # Envy-free percentage
    envy_free_count = sum(1 for d in data_list if d["is_envy_free"])
    envy_free_pct = (envy_free_count / total_scenarios * 100) if total_scenarios > 0 else 0
    print(f"  Envy-free outcomes: {envy_free_count} ({envy_free_pct:.1f}%)")

    # Both Pareto optimal and envy-free
    both_count = sum(1 for d in data_list if d["is_pareto_optimal"] and d["is_envy_free"])
    both_pct = (both_count / total_scenarios * 100) if total_scenarios > 0 else 0
    print(f"  Both Pareto optimal & envy-free: {both_count} ({both_pct:.1f}%)")

    # Score statistics
    agent1_scores = [d["agent1_human_score"] for d in data_list]
    agent2_scores = [d["agent2_human_score"] for d in data_list]
    total_scores = [d["agent1_human_score"] + d["agent2_human_score"] for d in data_list]

    print(f"\n💯 Score Statistics:")
    print(f"  Agent 1 average score: {sum(agent1_scores) / len(agent1_scores):.2f}")
    print(f"  Agent 2 average score: {sum(agent2_scores) / len(agent2_scores):.2f}")
    print(f"  Average total score: {sum(total_scores) / len(total_scores):.2f}")
    print(f"  Max total score: {max(total_scores)}")
    print(f"  Min total score: {min(total_scores)}")


def interactive_explore(data_list: List[Dict]):
    """Interactive exploration mode."""
    print(f"\n{'=' * 70}")
    print("Interactive Exploration Mode")
    print(f"{'=' * 70}")
    print("\nCommands:")
    print("  [number] - View scenario by index")
    print("  'n' or 'next' - View next scenario")
    print("  'p' or 'prev' - View previous scenario")
    print("  'r' or 'random' - View random scenario")
    print("  's' or 'stats' - Show summary statistics")
    print("  'q' or 'quit' - Quit")
    print(f"\nTotal scenarios: {len(data_list)}")

    current_idx = 0

    while True:
        print(f"\n{'─' * 70}")
        cmd = input(f"\nCurrent: #{current_idx}. Enter command: ").strip().lower()

        if cmd in ["q", "quit", "exit"]:
            print("Goodbye!")
            break
        elif cmd in ["n", "next"]:
            current_idx = (current_idx + 1) % len(data_list)
            display_scenario(data_list[current_idx])
        elif cmd in ["p", "prev"]:
            current_idx = (current_idx - 1) % len(data_list)
            display_scenario(data_list[current_idx])
        elif cmd in ["r", "random"]:
            import random

            current_idx = random.randint(0, len(data_list) - 1)
            display_scenario(data_list[current_idx])
        elif cmd in ["s", "stats"]:
            display_summary_stats(data_list, "current dataset")
        elif cmd.isdigit():
            idx = int(cmd)
            if 0 <= idx < len(data_list):
                current_idx = idx
                display_scenario(data_list[current_idx])
            else:
                print(f"Error: Index {idx} out of range (0-{len(data_list) - 1})")
        else:
            print("Unknown command. Try 'n', 'p', 'r', 's', [number], or 'q'")


def main():
    parser = argparse.ArgumentParser(description="Explore Deal-No-Deal dataset files.")

    parser.add_argument(
        "filename",
        type=str,
        nargs="?",
        default="test.txt",
        help="Dataset filename (test.txt, train.txt, val.txt, or hard.txt). Default: test.txt",
    )
    parser.add_argument(
        "--max-samples",
        type=int,
        default=None,
        help="Maximum number of samples to load. Default: load all",
    )
    parser.add_argument(
        "--show-all", action="store_true", help="Display all scenarios (non-interactive)"
    )
    parser.add_argument("--stats-only", action="store_true", help="Only show summary statistics")
    parser.add_argument("--index", type=int, default=None, help="Show specific scenario by index")
    parser.add_argument("--raw", action="store_true", help="Show raw data line")

    args = parser.parse_args()

    # Construct filepath
    if args.filename in ["test.txt", "train.txt", "val.txt", "hard.txt"]:
        filepath = os.path.join("data", args.filename)
    else:
        filepath = args.filename

    print(f"Loading data from: {filepath}")

    # Load data
    data_list = load_and_parse_data(filepath, args.max_samples)

    if not data_list:
        print("No data loaded!")
        return

    print(f"Loaded {len(data_list)} scenarios")

    # Display based on mode
    if args.stats_only:
        display_summary_stats(data_list, args.filename)
    elif args.index is not None:
        if 0 <= args.index < len(data_list):
            display_scenario(data_list[args.index], show_raw=args.raw)
        else:
            print(f"Error: Index {args.index} out of range (0-{len(data_list) - 1})")
    elif args.show_all:
        for data in data_list:
            display_scenario(data, show_raw=args.raw)
        print("\n")
        display_summary_stats(data_list, args.filename)
    else:
        # Interactive mode (default)
        display_summary_stats(data_list, args.filename)
        interactive_explore(data_list)


if __name__ == "__main__":
    main()
