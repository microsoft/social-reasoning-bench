"""
Sotopia Dataset Browser
========================

Browse the Sotopia dataset - 7,200 social interaction episodes between agents.

Usage:
    uv run python datasets/sotopia/explore_sotopia.py
"""

import argparse
import json
from collections import Counter

from rich.console import Console
from rich.table import Table

console = Console()


def load_dataset(path="datasets/sotopia/sotopia_episodes_part_*.jsonl"):
    """Load the Sotopia dataset from split files."""
    import glob

    episodes = []
    # Handle both single file and glob pattern
    if "*" in path:
        files = sorted(glob.glob(path))
    else:
        files = [path]

    for file_path in files:
        with open(file_path) as f:
            for line in f:
                episodes.append(json.loads(line))
    return episodes


def calculate_statistics(dataset):
    """Calculate summary statistics for the dataset."""
    stats = {
        "total": len(dataset),
        "hard": sum(1 for ep in dataset if ep.get("difficulty") == "hard"),
        "normal": sum(1 for ep in dataset if ep.get("difficulty") == "normal"),
        "unique_env_ids": len(set(ep["environment_id"] for ep in dataset)),
        "unique_agent_pairs": len(set(tuple(sorted(ep["agent_ids"])) for ep in dataset)),
        "experiment_tags": Counter(ep["experiment_tag"] for ep in dataset),
        "conversation_lengths": [],
    }

    # Calculate conversation lengths (number of turns)
    for ep in dataset:
        # raw_messages is a list of turns, count them
        if "raw_messages" in ep and ep["raw_messages"]:
            stats["conversation_lengths"].append(len(ep["raw_messages"]))

    if stats["conversation_lengths"]:
        stats["min_turns"] = min(stats["conversation_lengths"])
        stats["max_turns"] = max(stats["conversation_lengths"])
        stats["avg_turns"] = sum(stats["conversation_lengths"]) / len(stats["conversation_lengths"])

    return stats


def display_overview(stats):
    """Display overview statistics."""
    console.print()
    console.rule("[bold cyan]SOTOPIA DATASET OVERVIEW[/]", style="cyan")
    console.print()

    # Create main statistics table
    table = Table(show_header=False, box=None, padding=(0, 2))
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="white")

    table.add_row("Total Episodes", f"{stats['total']:,}")
    table.add_row(
        "Hard Episodes",
        f"[red]{stats['hard']:,}[/] ({stats['hard'] / stats['total'] * 100:.1f}%)",
    )
    table.add_row(
        "Normal Episodes",
        f"[green]{stats['normal']:,}[/] ({stats['normal'] / stats['total'] * 100:.1f}%)",
    )
    table.add_row("Unique Environments", f"{stats['unique_env_ids']}")
    table.add_row("Unique Agent Pairs", f"{stats['unique_agent_pairs']}")

    if "min_turns" in stats:
        table.add_row(
            "Conversation Length",
            f"min={stats['min_turns']}, max={stats['max_turns']}, avg={stats['avg_turns']:.1f} turns",
        )

    console.print(table)

    console.print()
    console.print(
        "[dim]Commands: number (jump), n (next), p (previous), t (toggle mode), q (quit)[/]"
    )
    console.print()


def display_entry_json(entry, index, total):
    """Display a single dataset entry with pretty-printed JSON."""
    console.print()
    difficulty_color = "red" if entry.get("difficulty") == "hard" else "green"
    difficulty_label = entry.get("difficulty", "unknown").upper()

    console.rule(
        f"[bold cyan]EPISODE {index + 1}/{total}[/] [{difficulty_color}]{difficulty_label}[/] [dim](JSON MODE)[/]"
    )

    # Format the entire episode as JSON with no syntax highlighting (to work with light terminals)
    json_str = json.dumps(entry, indent=2, ensure_ascii=False)
    console.print(json_str)
    console.print()


def display_entry_readable(entry, index, total):
    """Display a single dataset entry in readable format."""
    console.print()
    difficulty_color = "red" if entry.get("difficulty") == "hard" else "green"
    difficulty_label = entry.get("difficulty", "unknown").upper()

    console.rule(
        f"[bold cyan]EPISODE {index + 1}/{total}[/] [{difficulty_color}]{difficulty_label}[/] [dim](READABLE MODE)[/]"
    )
    console.print()

    # Extract agent names from first turn Environment messages
    agent_names = []
    raw_messages = entry.get("raw_messages", [])
    if raw_messages:
        first_turn = raw_messages[0]
        for msg in first_turn:
            if len(msg) >= 2 and msg[0] == "Environment":
                agent_names.append(msg[1])

    # Header with episode info
    info_table = Table(show_header=False, box=None, padding=(0, 1))
    info_table.add_column("Field", style="cyan", width=20)
    info_table.add_column("Value", style="white")

    # Add difficulty with color
    difficulty = entry.get("difficulty", "unknown")
    difficulty_styled = f"[{difficulty_color}]{difficulty}[/]"

    info_table.add_row("Difficulty", difficulty_styled)
    info_table.add_row("Episode ID", entry.get("episode_id", "N/A"))
    info_table.add_row("Environment ID", entry.get("environment_id", "N/A"))

    # Show agents with their names
    agent_ids = entry.get("agent_ids", [])
    for i, agent_id in enumerate(agent_ids):
        agent_name = agent_names[i] if i < len(agent_names) else "Unknown"
        info_table.add_row(f"Agent {i + 1}", f"{agent_name} ({agent_id})")

    info_table.add_row("Experiment Tag", entry.get("experiment_tag", "N/A"))
    info_table.add_row("Models", ", ".join(entry.get("experiment_model_name_pairs", [])))

    console.print(info_table)
    console.print()

    # Conversation
    console.rule("[bold]Conversation[/]", style="cyan")
    console.print()

    raw_messages = entry.get("raw_messages", [])
    for turn_idx, turn in enumerate(raw_messages):
        console.print(f"\n[bold cyan]# Step {turn_idx + 1}[/]\n")
        for message in turn:
            if len(message) >= 3:
                speaker = message[0]
                recipient = message[1]
                content = message[2]
                content = content.strip()

                console.print(f"[yellow]{speaker}[/] -> [yellow]{recipient}:[/]")
                console.print(content, highlight=False)
                console.print()
            else:
                console.print(f"{message}")

    # Rewards
    console.rule("[bold]Rewards[/]", style="cyan")
    console.print()

    rewards = entry.get("rewards", [])
    if rewards:
        for agent_idx, reward_data in enumerate(rewards):
            if isinstance(reward_data, dict):
                console.print(f"[bold]Agent {agent_idx + 1} Rewards:[/]")

                rewards_table = Table(show_header=True, box=None, padding=(0, 2))
                rewards_table.add_column("Metric", style="cyan")
                rewards_table.add_column("Score", style="white", justify="right")

                for metric, score in reward_data.items():
                    rewards_table.add_row(metric, f"{score:.2f}")

                console.print(rewards_table)
                console.print()
    else:
        console.print("[dim]No rewards available[/]")
        console.print()


def display_entry(entry, index, total, mode="readable"):
    """Display entry in the specified mode."""
    if mode == "json":
        display_entry_json(entry, index, total)
    else:
        display_entry_readable(entry, index, total)


def interactive_mode(dataset):
    """Run interactive terminal interface."""
    total = len(dataset)
    idx = None  # Start with no episode displayed
    mode = "readable"  # Start in readable mode

    # Calculate and display statistics
    stats = calculate_statistics(dataset)
    display_overview(stats)

    while True:
        # Only display entry if idx is set (not on first launch)
        if idx is not None:
            display_entry(dataset[idx], idx, total, mode)

        try:
            cmd = console.input("[cyan]Command:[/] ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            console.print()
            break

        if cmd == "q":
            break
        elif cmd == "n":
            if idx is None:
                idx = 0
            else:
                idx = (idx + 1) % total
        elif cmd == "p":
            if idx is None:
                idx = 0
            else:
                idx = (idx - 1) % total
        elif cmd == "t":
            # Toggle between modes
            mode = "json" if mode == "readable" else "readable"
            console.print(f"[green]Switched to {mode.upper()} mode[/]")
            # Redisplay current entry if one is loaded
            if idx is not None:
                display_entry(dataset[idx], idx, total, mode)
        elif cmd.isdigit():
            new_idx = int(cmd) - 1
            if 0 <= new_idx < total:
                idx = new_idx
            else:
                console.print(f"[yellow]Enter a number between 1 and {total}[/]")


def main():
    parser = argparse.ArgumentParser(description="Browse the Sotopia dataset")
    parser.add_argument(
        "--data",
        "-d",
        default="datasets/sotopia/sotopia_episodes_part_*.jsonl",
        help="Path to dataset file (supports glob patterns)",
    )
    args = parser.parse_args()

    console.print(f"[dim]Loading dataset from {args.data}...[/]")
    dataset = load_dataset(args.data)
    console.print(f"[green]Loaded {len(dataset)} episodes[/]")

    interactive_mode(dataset)


if __name__ == "__main__":
    main()
