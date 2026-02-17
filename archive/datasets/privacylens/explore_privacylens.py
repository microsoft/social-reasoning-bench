"""
PrivacyLens Dataset Browser
===========================

Browse the PrivacyLens dataset - 493 privacy-sensitive scenarios for
evaluating whether LLM agents leak sensitive information.

Usage
-----
    uv run python datasets/privacylens/explore_privacylens.py
"""

import argparse
import json

from rich.console import Console
from rich.panel import Panel

console = Console()


def load_dataset(path="datasets/privacylens/privacylens.json"):
    """Load the PrivacyLens dataset."""
    with open(path) as f:
        return json.load(f)


def display_entry(entry, index, total):
    """Display a single dataset entry."""
    console.print()
    console.rule(f"[bold cyan]ENTRY {index + 1}/{total}: {entry['name']}[/]")

    # Privacy norm
    seed = entry["seed"]
    norm_text = (
        f"{seed['data_sender']} should not share "
        f"[yellow]{seed['data_type']}[/] about [yellow]{seed['data_subject']}[/] "
        f"with [yellow]{seed['data_recipient']}[/]"
    )
    console.print(Panel(norm_text, title="[bold]Privacy Norm[/]", border_style="yellow"))
    console.print(f"[dim]Source: {seed['source']}[/]")

    # Scenario
    console.print()
    console.rule("[bold cyan]SCENARIO[/]", style="cyan")
    console.print(f"\n{entry['vignette']['story']}\n")

    # Task
    console.print()
    console.rule("[bold cyan]TASK[/]", style="cyan")
    traj = entry["trajectory"]
    console.print(f"\n[green]{traj['user_instruction']}[/]")
    console.print(f"[dim]Final action: {traj['final_action']}[/]")
    console.print(f"[dim]Tools available: {', '.join(traj['toolkits'])}[/]\n")

    # What LLM sees
    console.print()
    console.rule("[bold cyan]WHAT THE LLM SEES[/]", style="cyan")
    console.print(f"\n[dim]{traj['executable_trajectory']}[/]\n")

    # Sensitive info
    console.print()
    console.rule("[bold red]SENSITIVE INFO - must NOT appear in output[/]", style="red")
    for item in traj["sensitive_info_items"]:
        console.print(f"  [red]- {item}[/]")
    console.print()


def interactive_mode(dataset):
    """Run interactive terminal interface."""
    total = len(dataset)
    idx = 0

    console.print()
    console.rule("[bold cyan]PRIVACYLENS DATASET BROWSER[/]", style="cyan")
    console.print(
        f"\n{total} privacy scenarios. Commands: number to jump, n/p for next/prev, q to quit.\n"
    )

    while True:
        display_entry(dataset[idx], idx, total)

        try:
            cmd = console.input("[cyan]Command:[/] ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            console.print()
            break

        if cmd == "q":
            break
        elif cmd == "n":
            idx = (idx + 1) % total
        elif cmd == "p":
            idx = (idx - 1) % total
        elif cmd.isdigit():
            new_idx = int(cmd) - 1
            if 0 <= new_idx < total:
                idx = new_idx
            else:
                console.print(f"[yellow]Enter a number between 1 and {total}[/]")


def main():
    parser = argparse.ArgumentParser(description="Browse the PrivacyLens dataset")
    parser.add_argument(
        "--data", "-d", default="datasets/privacylens/privacylens.json", help="Path to dataset file"
    )
    args = parser.parse_args()

    dataset = load_dataset(args.data)
    interactive_mode(dataset)


if __name__ == "__main__":
    main()
