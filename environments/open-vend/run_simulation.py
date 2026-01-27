"""CLI entry point for OpenVend simulation."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def main() -> int:
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="OpenVend - AI Agent Vending Machine Simulation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run a new simulation with OpenAI
  uv run run_simulation.py run --provider openai --model gpt-4o

  # Run with Anthropic Claude
  uv run run_simulation.py run --provider anthropic --model claude-sonnet-4-20250514

  # Run with Google Gemini
  uv run run_simulation.py run --provider gemini --model gemini-2.0-flash

  # Resume an existing simulation
  uv run run_simulation.py resume .open_vend_run_20240101_120000

  # Quick test run (7 days)
  uv run run_simulation.py run --provider openai --model gpt-4o-mini --max-days 7
""",
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Run command
    run_parser = subparsers.add_parser("run", help="Start a new simulation")
    run_parser.add_argument(
        "--provider",
        required=True,
        choices=["openai", "anthropic", "gemini"],
        help="LLM provider to use",
    )
    run_parser.add_argument(
        "--model",
        required=True,
        help="Model name (e.g., gpt-4o, claude-sonnet-4-20250514, gemini-2.0-flash)",
    )
    run_parser.add_argument(
        "--api-key",
        help="API key (defaults to environment variable)",
    )
    run_parser.add_argument(
        "--output-dir",
        help="Output directory for logs (defaults to timestamped dir)",
    )
    run_parser.add_argument(
        "--max-days",
        type=int,
        default=365,
        help="Maximum simulation days (default: 365)",
    )
    run_parser.add_argument(
        "--max-messages",
        type=int,
        default=2000,
        help="Maximum messages before termination (default: 2000)",
    )
    run_parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress progress output",
    )

    # Resume command
    resume_parser = subparsers.add_parser("resume", help="Resume an existing simulation")
    resume_parser.add_argument(
        "output_dir",
        help="Path to existing simulation output directory",
    )
    resume_parser.add_argument(
        "--provider",
        help="Override LLM provider",
    )
    resume_parser.add_argument(
        "--model",
        help="Override model name",
    )
    resume_parser.add_argument(
        "--api-key",
        help="API key (defaults to environment variable)",
    )
    resume_parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress progress output",
    )

    # Info command
    info_parser = subparsers.add_parser("info", help="Show info about a simulation run")
    info_parser.add_argument(
        "output_dir",
        help="Path to simulation output directory",
    )

    args = parser.parse_args()

    if args.command == "run":
        return run_simulation(args)
    elif args.command == "resume":
        return resume_simulation(args)
    elif args.command == "info":
        return show_info(args)
    else:
        parser.print_help()
        return 1


def run_simulation(args: argparse.Namespace) -> int:
    """Run a new simulation."""
    from src.simulation.engine import SimulationEngine

    try:
        engine = SimulationEngine(
            provider=args.provider,
            model=args.model,
            api_key=args.api_key,
            output_dir=args.output_dir,
            max_days=args.max_days,
            max_messages=args.max_messages,
        )

        results = engine.run(verbose=not args.quiet)

        # Print final results
        print("\n" + "=" * 50)
        print("FINAL RESULTS")
        print("=" * 50)
        print(f"Termination: {results['termination_reason']}")
        print(f"Days Completed: {results['final_day']}")
        print(f"Final Net Worth: ${results['final_net_worth']:.2f}")
        print(f"Bank Balance: ${results['final_bank_balance']:.2f}")
        print(f"Machine Cash: ${results['final_machine_cash']:.2f}")
        print(f"Total Messages: {results['total_messages']}")
        if results["token_usage"]:
            print(f"Tokens Used: {results['token_usage']['total_tokens']:,}")
        print(f"Output Dir: {results['output_dir']}")

        return 0

    except KeyboardInterrupt:
        print("\nSimulation interrupted.")
        return 130
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def resume_simulation(args: argparse.Namespace) -> int:
    """Resume an existing simulation."""
    from src.simulation.engine import resume_simulation as resume_sim

    try:
        engine = resume_sim(
            output_dir=args.output_dir,
            provider=args.provider,
            model=args.model,
            api_key=args.api_key,
        )

        print(f"Resuming simulation from day {engine.state.current_day}")
        results = engine.run(verbose=not args.quiet)

        print("\n" + "=" * 50)
        print("FINAL RESULTS")
        print("=" * 50)
        print(f"Final Net Worth: ${results['final_net_worth']:.2f}")

        return 0

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def show_info(args: argparse.Namespace) -> int:
    """Show information about a simulation run."""
    import json

    output_dir = Path(args.output_dir)

    if not output_dir.exists():
        print(f"Error: Directory not found: {output_dir}", file=sys.stderr)
        return 1

    # Load run info
    run_info_file = output_dir / "run_info.json"
    if run_info_file.exists():
        with open(run_info_file) as f:
            run_info = json.load(f)

        print("=" * 50)
        print("SIMULATION INFO")
        print("=" * 50)
        print(f"Provider: {run_info.get('provider', 'N/A')}")
        print(f"Model: {run_info.get('model', 'N/A')}")
        print(f"Start Time: {run_info.get('start_time', 'N/A')}")
        print(f"End Time: {run_info.get('end_time', 'N/A')}")
        print(f"End Reason: {run_info.get('end_reason', 'N/A')}")
        print(f"Final Day: {run_info.get('final_day', 'N/A')}")
        print(f"Final Net Worth: ${run_info.get('final_net_worth', 0):.2f}")
        print(f"Total Messages: {run_info.get('total_messages', 'N/A')}")

        if run_info.get("token_usage"):
            usage = run_info["token_usage"]
            print(f"Input Tokens: {usage.get('input_tokens', 0):,}")
            print(f"Output Tokens: {usage.get('output_tokens', 0):,}")

    # Load current state
    state_file = output_dir / "state.json"
    if state_file.exists():
        with open(state_file) as f:
            state = json.load(f)

        print("\n" + "-" * 50)
        print("CURRENT STATE")
        print("-" * 50)
        print(f"Day: {state.get('current_day', 'N/A')}")
        print(f"Bank Balance: ${state.get('bank_balance', 0):.2f}")
        print(f"Machine Cash: ${state.get('machine_cash', 0):.2f}")
        print(f"Warehouse Items: {len(state.get('warehouse', {}))}")
        print(f"Emails: {len(state.get('emails', []))}")
        print(f"Memory Keys: {len(state.get('memory', {}))}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
