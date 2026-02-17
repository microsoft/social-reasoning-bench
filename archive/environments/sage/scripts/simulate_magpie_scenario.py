"""Simulate a MAGPIE scenario using the messenger protocol.

This script launches the messenger marketplace server and runs agents from a
specified scenario directory. Each agent runs autonomously until it calls
Shutdown or reaches max iterations.

Usage:
    # Run a scenario
    python scripts/simulate_magpie_scenario.py path/to/scenario_dir

    # With custom options
    python scripts/simulate_magpie_scenario.py path/to/scenario_dir \\
        --model gpt-4o \\
        --max-iterations 100 \\
        --port 8001

    # Overwrite existing database
    python scripts/simulate_magpie_scenario.py path/to/scenario_dir --overwrite

Requirements:
    - OpenAI API key (set OPENAI_API_KEY environment variable)
    - Scenario directory with agent_*.json profile files
"""

import argparse
import asyncio
from pathlib import Path

from dotenv import load_dotenv
from magentic_marketplace.platform.database.sqlite import connect_to_sqlite_database
from magentic_marketplace.platform.launcher import AgentLauncher, MarketplaceLauncher
from sage_agents import (
    ShutdownHook,
    WaitHook,
    create_agent_from_profile,
    load_profiles_from_dir,
)
from sage_protocol import AutonomousProtocol, Shutdown, Wait
from sage_protocol.messenger.protocol import MessengerProtocol


async def main():
    """Run a MAGPIE scenario simulation."""
    parser = argparse.ArgumentParser(
        description="Simulate a MAGPIE scenario using the messenger protocol"
    )
    parser.add_argument(
        "scenario_dir",
        type=Path,
        help="Path to scenario directory containing agent JSON files",
    )
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Server host (default: 127.0.0.1)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8001,
        help="Server port (default: 8001)",
    )
    parser.add_argument(
        "--database",
        type=Path,
        default=None,
        help="SQLite database path (default: <scenario_name>.db)",
    )
    parser.add_argument(
        "--model",
        default="gpt-4o",
        help="OpenAI model to use (default: gpt-4o)",
    )
    parser.add_argument(
        "--max-iterations",
        type=int,
        default=50,
        help="Maximum iterations per agent (default: 50)",
    )
    parser.add_argument(
        "--agent-type",
        choices=["chat-completions", "responses"],
        default="chat-completions",
        help="Agent type to use (default: chat-completions)",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing database if it exists",
    )

    args = parser.parse_args()

    # Load environment variables
    load_dotenv()

    # Validate scenario directory
    if not args.scenario_dir.exists():
        print(f"Error: Scenario directory not found: {args.scenario_dir}")
        raise SystemExit(1)

    if not args.scenario_dir.is_dir():
        print(f"Error: Not a directory: {args.scenario_dir}")
        raise SystemExit(1)

    # Set default database name based on scenario directory
    if args.database is None:
        args.database = Path(f"{args.scenario_dir.name}.db")

    # Check if database already exists
    if args.database.exists():
        if args.overwrite:
            print(f"Overwriting existing database: {args.database.absolute()}")
            args.database.unlink()
        else:
            print(f"Error: Database already exists: {args.database.absolute()}")
            print("Use --overwrite to replace it, or specify a different path with --database")
            raise SystemExit(1)

    # Load agent profiles
    print(f"\nLoading agent profiles from: {args.scenario_dir}")
    try:
        profiles = load_profiles_from_dir(args.scenario_dir)
    except (FileNotFoundError, ValueError) as e:
        print(f"Error loading profiles: {e}")
        raise SystemExit(1)

    print(f"Loaded {len(profiles)} agent profiles")
    for profile in profiles:
        print(f"  - {profile.full_name} ({profile.email_address})")

    # Create protocol with autonomous actions
    protocol = AutonomousProtocol(MessengerProtocol())

    # Launch server
    async with MarketplaceLauncher(
        protocol=protocol,
        database_factory=lambda: connect_to_sqlite_database(args.database),
        host=args.host,
        port=args.port,
        title="MAGPIE Scenario Simulation",
        description="Messenger marketplace for MAGPIE scenario simulation",
        experiment_name=args.scenario_dir.name,
    ) as launcher:
        print("\n" + "=" * 70)
        print("MAGPIE Scenario Simulation")
        print("=" * 70)
        print(f"Scenario: {args.scenario_dir.name}")
        print(f"Server URL: {launcher.server_url}")
        print(f"Database: {args.database}")
        print(f"Model: {args.model}")
        print(f"Max iterations: {args.max_iterations}")
        print(f"Agent type: {args.agent_type}")
        print("=" * 70)

        # Create agents from profiles
        agents = []
        for profile in profiles:
            agent = create_agent_from_profile(
                profile=profile,
                base_url=launcher.server_url,
                agent_type=args.agent_type,
                openai_model=args.model,
                max_iterations=args.max_iterations,
            )

            # Register hooks for autonomous actions
            agent.register_hooks(ShutdownHook(Shutdown))
            agent.register_hooks(WaitHook(Wait))

            agents.append(agent)

        print(f"\nCreated {len(agents)} agents")
        print("Starting simulation...\n")

        # Run agents
        async with AgentLauncher(launcher.server_url) as agent_launcher:
            try:
                await agent_launcher.run_agents(*agents)
            except Exception as e:
                print(f"\nError during simulation: {e}")
                raise

        print("\n" + "=" * 70)
        print("Simulation Complete")
        print("=" * 70)
        print(f"Database saved to: {args.database.absolute()}")
        print("\nTo extract transcripts, run:")
        print(f"  python scripts/extract_transcripts.py --database {args.database}")


if __name__ == "__main__":
    asyncio.run(main())
