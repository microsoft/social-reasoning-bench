"""
Sotopia Environment Browser
============================

Browse the 90 unique environments in the Sotopia dataset.
Each environment defines a social scenario with roles and goals.
Note: Agent names vary across episodes, but the scenario and goals remain constant.

Usage:
    uv run python datasets/sotopia/explore_sotopia_environments.py
"""

import argparse
import json
from collections import defaultdict

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()


def load_environments(path="datasets/sotopia/sotopia_environments.json"):
    """Load unique environments from the Sotopia dataset JSON file."""
    with open(path) as f:
        environments = json.load(f)

    return environments


def load_environments_from_jsonl(path="datasets/sotopia/sotopia_episodes_part_*.jsonl"):
    """Load unique environments from the Sotopia dataset JSONL files (legacy method)."""
    import glob

    # Use a dict to collect environment info, keyed by environment_id
    environments = {}
    env_episode_counts = defaultdict(int)
    env_agent_names = defaultdict(set)  # Track all agent name pairs per environment

    # Handle both single file and glob pattern
    if "*" in path:
        files = sorted(glob.glob(path))
    else:
        files = [path]

    for file_path in files:
        with open(file_path) as f:
            for line in f:
                episode = json.loads(line)
                env_id = episode["environment_id"]
                env_episode_counts[env_id] += 1

                # Extract environment details from the first message
                raw_messages = episode.get("raw_messages", [])
                if raw_messages and len(raw_messages) > 0:
                    first_turn = raw_messages[0]

                    # Collect agent names for this environment (to track variations)
                    agent_names_this_ep = []
                    for msg in first_turn:
                        if len(msg) >= 2 and msg[0] == "Environment":
                            agent_names_this_ep.append(msg[1])

                    if len(agent_names_this_ep) == 2:
                        env_agent_names[env_id].add(tuple(sorted(agent_names_this_ep)))

                    # If we haven't seen this environment yet, extract its info
                    if env_id not in environments:
                        # Parse the environment context from the messages
                        # There are typically 2 environment messages (one per agent)
                        # Each shows that agent's goal but marks the other as "Unknown"
                        scenario = None
                        goals = []

                        for msg in first_turn:
                            if len(msg) >= 3 and msg[0] == "Environment":
                                content = msg[2]

                                # Extract scenario (same in all messages)
                                if scenario is None and "Scenario:" in content:
                                    scenario_start = content.find("Scenario:") + len("Scenario:")
                                    scenario_end = content.find("Participants:")
                                    if scenario_end != -1:
                                        scenario = content[scenario_start:scenario_end].strip()

                                # Extract goals - look for pattern "NAME's goal: GOAL_TEXT"
                                # Goals can span multiple lines until the next agent's goal line
                                if "'s goal:" in content:
                                    # Find all instances of "'s goal:" in this message
                                    goal_marker = "'s goal:"
                                    search_pos = 0

                                    while True:
                                        goal_idx = content.find(goal_marker, search_pos)
                                        if goal_idx == -1:
                                            break

                                        # Extract the goal text starting after "'s goal:"
                                        goal_start = goal_idx + len(goal_marker)

                                        # Find the end - look for the next line that starts with a name followed by "'s goal:"
                                        # The goal ends at the newline before the next "NAME's goal:" line
                                        next_goal = content.find("\n", goal_start)
                                        if next_goal != -1:
                                            # Check if there's another goal after this
                                            next_goal_marker = content.find("'s goal:", next_goal)
                                            if next_goal_marker != -1:
                                                # Find the newline before this next goal marker
                                                # by going back from the goal marker to find the agent name
                                                goal_end = content.rfind(
                                                    "\n", goal_start, next_goal_marker
                                                )
                                                if goal_end == -1:
                                                    goal_end = next_goal_marker
                                            else:
                                                # No more goals, extend to "Conversation Starts:"
                                                conversation_starts = content.find(
                                                    "Conversation Starts:", goal_start
                                                )
                                                if conversation_starts != -1:
                                                    goal_end = conversation_starts
                                                else:
                                                    goal_end = len(content)
                                        else:
                                            goal_end = len(content)

                                        # Extract and clean the goal text
                                        goal_text = content[goal_start:goal_end].strip()

                                        # Remove any trailing agent goal lines (e.g., "NAME's goal: Unknown")
                                        # Check if goal ends with a line like "AGENT's goal:"
                                        lines = goal_text.split("\n")
                                        while lines and "'s goal:" in lines[-1]:
                                            lines.pop()
                                        goal_text = "\n".join(lines).strip()

                                        # Only add if not "Unknown"
                                        if goal_text and goal_text != "Unknown":
                                            goals.append(goal_text)

                                        # Move to next search position
                                        search_pos = goal_idx + 1

                        # Remove duplicates while preserving order
                        # BUT: we need exactly 2 goals (one per role), even if they're identical
                        unique_goals = []
                        for goal in goals:
                            if goal not in unique_goals:
                                unique_goals.append(goal)

                        # Handle cases where both roles have the same goal
                        # We expect 2 goals to be found (one per agent message)
                        # If we only found 1 unique goal but saw it twice, both roles have the same goal
                        role1_goal = "Unknown"
                        role2_goal = "Unknown"

                        if len(unique_goals) >= 2:
                            # Different goals for each role
                            role1_goal = unique_goals[0]
                            role2_goal = unique_goals[1]
                        elif len(unique_goals) == 1 and len(goals) >= 2:
                            # Same goal for both roles (e.g., prisoner's dilemma)
                            role1_goal = unique_goals[0]
                            role2_goal = unique_goals[0]
                        elif len(unique_goals) == 1:
                            # Only one goal found total
                            role1_goal = unique_goals[0]
                            role2_goal = "Unknown"

                        environments[env_id] = {
                            "id": env_id,
                            "scenario": scenario or "N/A",
                            "role1_goal": role1_goal,
                            "role2_goal": role2_goal,
                        }

    # Add episode counts and agent name variations to each environment
    for env_id in environments:
        environments[env_id]["episode_count"] = env_episode_counts[env_id]
        environments[env_id]["unique_agent_pairs"] = len(env_agent_names[env_id])

    # Convert to sorted list
    env_list = sorted(environments.values(), key=lambda x: x["id"])
    return env_list


def display_overview(environments):
    """Display overview of environments."""
    console.print()
    console.rule("[bold cyan]SOTOPIA ENVIRONMENTS OVERVIEW[/]", style="cyan")
    console.print()

    table = Table(show_header=False, box=None, padding=(0, 2))
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="white")

    total_episodes = sum(env["episode_count"] for env in environments)
    avg_episodes = total_episodes / len(environments) if environments else 0

    # Count by difficulty
    hard_count = sum(1 for env in environments if env.get("difficulty") == "hard")
    normal_count = sum(1 for env in environments if env.get("difficulty") == "normal")

    table.add_row("Total Unique Environments", f"{len(environments)}")
    table.add_row("  ├─ [red]Hard[/red]", f"{hard_count}")
    table.add_row("  └─ [green]Normal[/green]", f"{normal_count}")
    table.add_row("Total Episodes Across All", f"{total_episodes:,}")
    table.add_row("Avg Episodes per Environment", f"{avg_episodes:.1f}")

    console.print(table)
    console.print()
    console.print(
        "[dim]Note: Each environment has the same scenario and goals across all episodes,[/]"
    )
    console.print("[dim]but different agent names are used in different episodes.[/]")
    console.print()
    console.print("[dim]Commands: number (jump), n (next), p (previous), q (quit)[/]")
    console.print()


def display_environment(env, index, total):
    """Display a single environment."""
    console.print()
    console.rule(f"[bold cyan]ENVIRONMENT {index + 1}/{total}[/] [dim](ID: {env['id']})[/]")
    console.print()

    # Scenario section
    console.print(Panel(env["scenario"], title="[bold cyan]Scenario[/]", border_style="cyan"))
    console.print()

    # Roles and Goals table
    roles_table = Table(
        show_header=True,
        box=None,
        padding=(0, 2),
        title="[bold cyan]Roles & Goals[/]",
        title_style="bold cyan",
    )
    roles_table.add_column("Role", style="yellow", width=15)
    roles_table.add_column("Goal", style="white")

    roles_table.add_row("Role 1", env["role1_goal"])
    roles_table.add_row("Role 2", env["role2_goal"])

    console.print(roles_table)
    console.print()

    # Metadata
    metadata_table = Table(show_header=False, box=None, padding=(0, 2))
    metadata_table.add_column("Field", style="cyan", width=25)
    metadata_table.add_column("Value", style="white")

    metadata_table.add_row("Environment ID", env["id"])

    # Add difficulty with color coding
    difficulty = env.get("difficulty", "unknown")
    if difficulty == "hard":
        difficulty_display = "[red bold]HARD[/red bold]"
    elif difficulty == "normal":
        difficulty_display = "[green]normal[/green]"
    else:
        difficulty_display = "[dim]unknown[/dim]"
    metadata_table.add_row("Difficulty", difficulty_display)

    metadata_table.add_row("Episodes with this scenario", f"{env['episode_count']}")
    metadata_table.add_row("Unique agent name pairs", f"{env['unique_agent_pairs']}")

    console.print(metadata_table)
    console.print()
    console.print("[dim]Note: Agent names vary across episodes but roles/goals stay the same.[/]")
    console.print()


def interactive_mode(environments):
    """Run interactive terminal interface."""
    total = len(environments)
    idx = None  # Start with no environment displayed

    # Display overview
    display_overview(environments)

    while True:
        # Only display environment if idx is set
        if idx is not None:
            display_environment(environments[idx], idx, total)

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
        elif cmd.isdigit():
            new_idx = int(cmd) - 1
            if 0 <= new_idx < total:
                idx = new_idx
            else:
                console.print(f"[yellow]Enter a number between 1 and {total}[/]")


def main():
    parser = argparse.ArgumentParser(
        description="Browse unique environments in the Sotopia dataset"
    )
    parser.add_argument(
        "--data",
        "-d",
        default="datasets/sotopia/sotopia_environments.json",
        help="Path to environments JSON file",
    )
    args = parser.parse_args()

    console.print(f"[dim]Loading environments from {args.data}...[/]")
    environments = load_environments(args.data)
    console.print(f"[green]Loaded {len(environments)} unique environments[/]")

    interactive_mode(environments)


if __name__ == "__main__":
    main()
