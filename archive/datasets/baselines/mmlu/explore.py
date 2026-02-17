"""
MMLU Dataset Explorer - Interactive browser for multitask language understanding questions.

Run: python sample.py
"""

import json
from pathlib import Path

import pandas as pd
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

console = Console()


def load_mmlu():
    """Load dataset from local JSON file (small version)."""
    data_dir = Path(__file__).parent

    with open(data_dir / "data" / "mmlu_small.json") as f:
        all_data = json.load(f)

    # Convert to dictionary of DataFrames (like HuggingFace dataset format)
    dataset = {split_name: pd.DataFrame(data) for split_name, data in all_data.items()}

    return dataset


def show_question(row, subject, split_name):
    """Display a question with rich formatting."""
    console.print()
    console.print(
        Panel(
            f"[bold]{subject}[/bold]\n[dim]Split: {split_name}[/dim]",
            title=f"[bold blue]Question {row.name}[/bold blue]",
            title_align="left",
        )
    )

    console.print("\n[bold cyan]Question[/bold cyan]")
    console.print(row["question"])

    console.print("\n[bold cyan]Choices[/bold cyan]")
    choices = row["choices"]
    answer_idx = row["answer"]

    for i, choice in enumerate(choices):
        label = chr(65 + i)  # A, B, C, D
        if i == answer_idx:
            console.print(f"  [bold green]{label}. {choice} ✓[/bold green]")
        else:
            console.print(f"  {label}. {choice}")


def main():
    console.print("[dim]Loading MMLU dataset...[/dim]")
    dataset = load_mmlu()

    # Use test split by default
    df = dataset["test"]

    # Get list of unique subjects
    subjects = sorted(df["subject"].unique())

    console.print(
        Panel(
            "[bold]MMLU[/bold]: Massive Multitask Language Understanding\n\n"
            f"Comprehensive knowledge benchmark across {len(subjects)} subjects.\n"
            f"Total questions: {len(df)}",
            title="[bold green]Welcome[/bold green]",
        )
    )

    # Show available subjects
    console.print("\n[bold cyan]Available Subjects:[/bold cyan]")
    table = Table(show_header=False)
    table.add_column("Index", style="dim")
    table.add_column("Subject")
    table.add_column("Questions", style="dim")

    for i, subject in enumerate(subjects[:20]):  # Show first 20
        count = len(df[df["subject"] == subject])
        table.add_row(str(i), subject, str(count))

    console.print(table)
    if len(subjects) > 20:
        console.print(f"[dim]...and {len(subjects) - 20} more subjects[/dim]")

    # Start with first subject
    current_subject_idx = 0
    current_subject = subjects[current_subject_idx]

    # Filter by subject
    subject_df = df[df["subject"] == current_subject].reset_index(drop=True)
    idx = 0

    while True:
        if idx >= len(subject_df):
            idx = 0

        show_question(subject_df.iloc[idx], current_subject, "test")

        console.print(f"\n[dim]({idx + 1}/{len(subject_df)}) [{current_subject}][/dim] ", end="")
        console.print(
            "[bold]n[/bold]=next  [bold]p[/bold]=prev  [bold]s[/bold]=change subject  "
            "[bold]#[/bold]=goto  [bold]q[/bold]=quit"
        )

        try:
            cmd = console.input("[bold]> [/bold]").strip().lower()
        except (KeyboardInterrupt, EOFError):
            break

        if cmd in ("n", ""):
            idx = (idx + 1) % len(subject_df)
        elif cmd == "p":
            idx = (idx - 1) % len(subject_df)
        elif cmd == "s":
            # Show subjects and let user pick
            console.print(
                "\n[bold cyan]Select a subject (0-{}):[/bold cyan]".format(len(subjects) - 1)
            )
            for i, subject in enumerate(subjects):
                count = len(df[df["subject"] == subject])
                console.print(f"  {i}: {subject} ({count} questions)")

            try:
                subject_cmd = console.input("[bold]Subject #> [/bold]").strip()
                if subject_cmd.isdigit():
                    new_idx = int(subject_cmd)
                    if 0 <= new_idx < len(subjects):
                        current_subject_idx = new_idx
                        current_subject = subjects[current_subject_idx]
                        subject_df = df[df["subject"] == current_subject].reset_index(drop=True)
                        idx = 0
                    else:
                        console.print(f"[red]Enter 0-{len(subjects) - 1}[/red]")
            except (KeyboardInterrupt, EOFError):
                continue
        elif cmd == "q":
            break
        elif cmd.isdigit():
            num = int(cmd)
            if 0 <= num < len(subject_df):
                idx = num
            else:
                console.print(f"[red]Enter 0-{len(subject_df) - 1}[/red]")


if __name__ == "__main__":
    main()
