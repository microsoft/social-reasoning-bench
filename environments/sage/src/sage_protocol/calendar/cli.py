"""Launch the Calendar marketplace server with optional scenario agents.

This CLI combines Calendar and Messenger protocols using CompositeProtocol,
allowing agents to use both calendar management and messaging actions.

Usage:
    # Server only
    python -m mm_environments.calendar

    # Run a scenario with agents from calendar JSON
    python -m mm_environments.calendar --scenario-json scenarios/scenario_20251118.json

    # Customize agent type and model
    python -m mm_environments.calendar \
        --scenario-json scenarios/scenario_20251118.json \
        --agent-type responses \
        --model gpt-4 \
        --max-iterations 100
"""

import argparse
import asyncio
from pathlib import Path

from magentic_marketplace.platform.database.sqlite import connect_to_sqlite_database
from magentic_marketplace.platform.launcher import MarketplaceLauncher

from .protocol import CalendarProtocol


async def main():
    """Start the Calendar marketplace server and optionally run scenario agents."""
    parser = argparse.ArgumentParser(
        description="Launch Calendar marketplace server with optional scenario agents"
    )
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Server host (default: 127.0.0.1)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8002,
        help="Server port (default: 8002)",
    )
    parser.add_argument(
        "--database",
        type=Path,
        default=None,
        help=(
            "SQLite database path (default: {scenario_json_name}.db if scenario provided, else calendar_marketplace.db)"
        ),
    )
    parser.add_argument(
        "--resume",
        action="store_true",
        help="Resume from existing database if it exists",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing database if it exists",
    )

    args = parser.parse_args()

    # Validate flags
    if args.resume and args.overwrite:
        print("Error: Cannot specify both --resume and --overwrite")
        raise SystemExit(1)

    # Set default database name based on scenario file if not specified
    if args.database is None:
        args.database = Path("calendar_marketplace.db")

    # Check if database already exists
    db_path = Path(args.database)
    if db_path.exists():
        if args.overwrite:
            print(f"Removing existing database at {db_path.absolute()}")
            db_path.unlink()
        elif args.resume:
            print(f"Resuming from existing database at {db_path.absolute()}")
        else:
            print(f"Error: Database already exists at {db_path.absolute()}")
            print("Please remove the existing database or use --resume or --overwrite flag")
            raise SystemExit(1)

    # Create composite protocol combining calendar and messenger
    protocol = CalendarProtocol()

    async with MarketplaceLauncher(
        protocol=protocol,
        database_factory=lambda: connect_to_sqlite_database(args.database),
        host=args.host,
        port=args.port,
        title="Calendar Marketplace API",
        description="A marketplace for calendar management and messaging agent communication",
        experiment_name="calendar_marketplace",
    ) as launcher:
        print("\n" + "=" * 70)
        print("Calendar Marketplace Server Running")
        print("=" * 70)
        print(f"Server URL: {launcher.server_url}")
        print(f"API Docs: {launcher.server_url}/docs")
        print(f"Database: {args.database}")
        print("Protocols: Calendar + Messenger (CompositeProtocol)")
        print("=" * 70)

        # Server-only mode (no agents)
        print("Press Ctrl+C to stop the server\n")

        try:
            # Keep the server running
            await asyncio.Event().wait()
        except KeyboardInterrupt:
            print("\n\nShutting down Calendar Marketplace Server...")


if __name__ == "__main__":
    asyncio.run(main())
