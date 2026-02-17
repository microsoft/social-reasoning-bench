"""
MAGPIE Dataset Explorer - Interactive browser for multi-agent privacy scenarios.

Run: python sample.py
"""

from datasets import load_dataset
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()


def load_magpie():
    """Load dataset (cached after first download)."""
    return load_dataset("jaypasnagasai/magpie", split="train").to_pandas()


def show_scenario(row):
    """Display a scenario with rich formatting."""
    console.print()
    console.print(
        Panel(
            f"[bold]{row['file_name']}[/bold]\n[dim]{row['agent_number']} agents: {row['agent_names']}[/dim]",
            title=f"[bold blue]Scenario {row.name}[/bold blue]",
            title_align="left",
        )
    )

    console.print("\n[bold cyan]Scenario[/bold cyan]")
    console.print(row["scenario"])

    console.print("\n[bold cyan]Task[/bold cyan]")
    console.print(row["task"])

    console.print("\n[bold cyan]Success Criteria[/bold cyan]")
    console.print(row["success_criteria"])

    console.print("\n[bold red]Constraints[/bold red]")
    console.print(Text(row["constraints"], style="red"))

    console.print("\n[bold cyan]Deliverable[/bold cyan]")
    console.print(row["deliverable"])


def main():
    console.print("[dim]Loading MAGPIE dataset...[/dim]")
    df = load_magpie()

    console.print(
        Panel(
            "[bold]MAGPIE[/bold]: Multi-Agent Privacy Evaluation\n\n"
            "Tests whether AI agents leak private info during collaboration.\n"
            "200 scenarios where sensitive data is needed to complete the task.",
            title="[bold green]Welcome[/bold green]",
        )
    )

    idx = 0
    while True:
        show_scenario(df.iloc[idx])

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
