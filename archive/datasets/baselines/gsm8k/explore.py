"""
GSM-8K Dataset Explorer - Interactive browser for grade school math problems.

Run: python sample.py
"""

import json
from pathlib import Path

import pandas as pd
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()


def load_gsm8k():
    """Load dataset from local JSON files."""
    data_dir = Path(__file__).parent

    with open(data_dir / "train.json") as f:
        train_data = json.load(f)

    with open(data_dir / "test.json") as f:
        test_data = json.load(f)

    train_df = pd.DataFrame(train_data)
    test_df = pd.DataFrame(test_data)

    return train_df, test_df


def show_problem(row, split_name):
    """Display a math problem with rich formatting."""
    console.print()
    console.print(
        Panel(
            f"[bold]GSM-8K Math Problem[/bold]\n[dim]Split: {split_name}[/dim]",
            title=f"[bold blue]Problem {row.name}[/bold blue]",
            title_align="left",
        )
    )

    console.print("\n[bold cyan]Question[/bold cyan]")
    console.print(row["question"])

    console.print("\n[bold green]Answer[/bold green]")
    console.print(Text(row["answer"], style="green"))


def main():
    console.print("[dim]Loading GSM-8K dataset...[/dim]")
    train_df, test_df = load_gsm8k()

    console.print(
        Panel(
            "[bold]GSM-8K[/bold]: Grade School Math 8K\n\n"
            f"High-quality grade school math word problems.\n"
            f"Train: {len(train_df)} problems | Test: {len(test_df)} problems",
            title="[bold green]Welcome[/bold green]",
        )
    )

    # Start with train split
    current_split = "train"
    df = train_df
    idx = 0

    while True:
        show_problem(df.iloc[idx], current_split)

        console.print(f"\n[dim]({idx + 1}/{len(df)}) [{current_split}][/dim] ", end="")
        console.print(
            "[bold]n[/bold]=next  [bold]p[/bold]=prev  [bold]t[/bold]=toggle split  "
            "[bold]#[/bold]=goto  [bold]q[/bold]=quit"
        )

        try:
            cmd = console.input("[bold]> [/bold]").strip().lower()
        except (KeyboardInterrupt, EOFError):
            break

        if cmd in ("n", ""):
            idx = (idx + 1) % len(df)
        elif cmd == "p":
            idx = (idx - 1) % len(df)
        elif cmd == "t":
            # Toggle between train and test
            if current_split == "train":
                current_split = "test"
                df = test_df
            else:
                current_split = "train"
                df = train_df
            idx = 0
        elif cmd == "q":
            break
        elif cmd.isdigit():
            num = int(cmd)
            if 0 <= num < len(df):
                idx = num
            else:
                console.print(f"[red]Enter 0-{len(df) - 1}[/red]")


if __name__ == "__main__":
    main()
