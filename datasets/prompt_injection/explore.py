"""Simple CSV explorer for prompt injection datasets."""

import csv
import glob
import os

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()


def list_csvs(directory="."):
    """List all CSV files in directory."""
    return sorted(glob.glob(os.path.join(directory, "*.csv")))


def load_csv(file_path):
    """Load CSV and return rows."""
    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    return rows


def display_overview(file_path, rows, columns):
    """Display dataset overview."""
    console.print()
    console.rule(f"[bold cyan]{os.path.basename(file_path)}[/]", style="cyan")
    console.print()

    table = Table(show_header=False, box=None, padding=(0, 2))
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="white")

    table.add_row("Total Rows", f"{len(rows)}")
    table.add_row("Columns", f"{', '.join(columns)}")

    console.print(table)
    console.print()
    console.print("[dim]Commands: number (jump), n (next), p (previous), q (quit)[/]")
    console.print()


def display_row(row, index, total, columns):
    """Display a single row."""
    console.print()
    console.rule(f"[bold cyan]ROW {index + 1}/{total}[/]")
    console.print()

    for col in columns:
        val = row.get(col, "")
        # Truncate long values
        if len(val) > 500:
            val = val[:500] + "..."
        console.print(Panel(val, title=f"[bold cyan]{col}[/]", border_style="cyan"))

    console.print()


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csvs = list_csvs(script_dir)

    if not csvs:
        console.print("[red]No CSV files found.[/]")
        return

    console.print()
    console.print("[bold cyan]Available CSV files:[/]")
    for i, f in enumerate(csvs, 1):
        console.print(f"  {i}. {os.path.basename(f)}")

    console.print()
    try:
        choice = console.input("[cyan]Select file (number):[/] ").strip()
        file_path = csvs[int(choice) - 1]
    except (ValueError, IndexError, EOFError, KeyboardInterrupt):
        console.print("[yellow]Invalid choice.[/]")
        return

    rows = load_csv(file_path)
    if not rows:
        console.print("[yellow]Empty CSV.[/]")
        return

    columns = list(rows[0].keys())
    display_overview(file_path, rows, columns)

    idx = None
    total = len(rows)

    while True:
        if idx is not None:
            display_row(rows[idx], idx, total, columns)

        try:
            cmd = console.input("[cyan]Command:[/] ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            console.print()
            break

        if cmd == "q":
            break
        elif cmd == "n":
            idx = 0 if idx is None else (idx + 1) % total
        elif cmd == "p":
            idx = 0 if idx is None else (idx - 1) % total
        elif cmd.isdigit():
            new_idx = int(cmd) - 1
            if 0 <= new_idx < total:
                idx = new_idx
            else:
                console.print(f"[yellow]Enter a number between 1 and {total}[/]")


if __name__ == "__main__":
    main()
