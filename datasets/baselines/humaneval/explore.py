"""
HumanEval Dataset Explorer - Interactive browser for Python coding problems.

Run: python sample.py
"""

import json
from pathlib import Path

import pandas as pd
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax

console = Console()


def load_humaneval():
    """Load dataset from local JSON file."""
    data_dir = Path(__file__).parent

    with open(data_dir / "test.json") as f:
        test_data = json.load(f)

    return pd.DataFrame(test_data)


def show_problem(row):
    """Display a coding problem with rich formatting."""
    console.print()
    console.print(
        Panel(
            f"[bold]{row['task_id']}[/bold]\n[dim]Entry point: {row['entry_point']}[/dim]",
            title=f"[bold blue]Problem {row.name}[/bold blue]",
            title_align="left",
        )
    )

    console.print("\n[bold cyan]Prompt[/bold cyan]")
    prompt_syntax = Syntax(row["prompt"], "python", theme="monokai", line_numbers=False)
    console.print(prompt_syntax)

    console.print("\n[bold green]Canonical Solution[/bold green]")
    solution_syntax = Syntax(
        row["canonical_solution"], "python", theme="monokai", line_numbers=False
    )
    console.print(solution_syntax)

    console.print("\n[bold yellow]Tests[/bold yellow]")
    test_syntax = Syntax(row["test"], "python", theme="monokai", line_numbers=False)
    console.print(test_syntax)


def main():
    console.print("[dim]Loading HumanEval dataset...[/dim]")
    df = load_humaneval()

    console.print(
        Panel(
            "[bold]HumanEval[/bold]: Hand-Written Python Programming Problems\n\n"
            f"Benchmark for code generation with {len(df)} problems.\n"
            "Each problem includes function signature, docstring, solution, and tests.",
            title="[bold green]Welcome[/bold green]",
        )
    )

    idx = 0

    while True:
        show_problem(df.iloc[idx])

        console.print(f"\n[dim]({idx + 1}/{len(df)})[/dim] ", end="")
        console.print(
            "[bold]n[/bold]=next  [bold]p[/bold]=prev  [bold]#[/bold]=goto  [bold]q[/bold]=quit"
        )

        try:
            cmd = console.input("[bold]> [/bold]").strip().lower()
        except (KeyboardInterrupt, EOFError):
            break

        if cmd in ("n", ""):
            idx = (idx + 1) % len(df)
        elif cmd == "p":
            idx = (idx - 1) % len(df)
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
