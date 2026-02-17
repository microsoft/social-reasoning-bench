import argparse
import asyncio
import contextlib
from pathlib import Path

from dotenv import load_dotenv
from magentic_marketplace.experiments.utils import load_businesses_from_yaml
from magentic_marketplace.marketplace.agents import BusinessAgent
from magentic_marketplace.marketplace.protocol.protocol import SimpleMarketplaceProtocol
from magentic_marketplace.platform.database.sqlite import connect_to_sqlite_database
from magentic_marketplace.platform.launcher import AgentLauncher, MarketplaceLauncher


async def launch_agents(args: argparse.Namespace, launcher: MarketplaceLauncher):
    businesses_dir = args.data_dir / "businesses"

    if not businesses_dir.exists():
        print(f"Error: Business data directory not found: {businesses_dir}")
        raise SystemExit(1)

    print(f"\nLoading businesses from: {businesses_dir}")
    businesses = load_businesses_from_yaml(businesses_dir)
    print(f"Loaded {len(businesses)} businesses")

    # Create business agents
    business_agents = [BusinessAgent(business, launcher.server_url) for business in businesses]

    print(f"Launching {len(business_agents)} business agents...")

    # Launch agents in the background
    async with AgentLauncher(launcher.server_url) as agent_launcher:
        # Run business agents (no primary agents, just dependent ones)
        agent_task = asyncio.create_task(agent_launcher.run_agents(*business_agents))

        print("Business agents launched successfully")
        print("=" * 70 + "\n")

        try:
            # Keep the server running
            await asyncio.Event().wait()
        except KeyboardInterrupt:
            print("\n\nShutting down Marketplace Server...")
            agent_task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await agent_task


async def main():
    """Start the Marketplace server."""
    parser = argparse.ArgumentParser(description="Launch Marketplace server.")
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
        help="SQLite database path (default: marketplace.db)",
    )
    parser.add_argument(
        "--resume",
        action="store_true",
        default=False,
        help="Resume from an existing database.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        default=False,
        help="Overwrite database if it exists.",
    )
    parser.add_argument(
        "--no-launch-agents",
        action="store_false",
        default=True,
        help="Launch business agents after starting server.",
    )
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=None,
        help="Directory containing business data (default: data/mexican_3_9)",
    )

    args = parser.parse_args()

    if args.resume and args.overwrite:
        print("Error: Cannot specify both --resume and --overwrite. Specify one or zero.")
        raise SystemExit(1)

    loaded_envs = load_dotenv()
    if loaded_envs:
        print("Successfully loaded environment variables from .env file.")
    else:
        print("No .env file found or loaded.")

    # Set default database name if not specified
    if args.database is None:
        args.database = Path("marketplace.db")

    # Check if database already exists
    db_path = Path(args.database)
    if db_path.exists():
        if args.resume:
            print(f"Warning: Resuming existing database at {db_path.absolute()}")
        elif args.overwrite:
            print(f"Warning: Overwriting existing database at {db_path.absolute()}")
            db_path.unlink()
        else:
            print(f"Error: Database already exists at {db_path.absolute()}")
            print(
                "Please remove the existing database, "
                "or specify a different path using --database, "
                "or resume the existing database using --resume, "
                "or overwrite the existing database using --overwrite."
            )
            raise SystemExit(1)

    # Set default data directory if not specified
    if args.data_dir is None:
        # Use the data directory relative to this file
        args.data_dir = Path(__file__).parent / "data" / "mexican_3_9"

    protocol = SimpleMarketplaceProtocol()

    async with MarketplaceLauncher(
        protocol=protocol,
        database_factory=lambda: connect_to_sqlite_database(args.database),
        host=args.host,
        port=args.port,
        title="Marketplace API",
        description="A marketplace for multi-agent interactions",
        experiment_name="marketplace",
    ) as launcher:
        print("\n" + "=" * 70)
        print("Marketplace Server Running")
        print("=" * 70)
        print(f"Server URL: {launcher.server_url}")
        print(f"API Docs: {launcher.server_url}/docs")
        print(f"Database: {args.database}")
        print("=" * 70)

        # Launch business agents if requested
        if args.no_launch_agents:
            await launch_agents(args, launcher)
        else:
            try:
                # Keep the server running
                await asyncio.Event().wait()
            except KeyboardInterrupt:
                print("\n\nShutting down Marketplace Server...")


if __name__ == "__main__":
    asyncio.run(main())
