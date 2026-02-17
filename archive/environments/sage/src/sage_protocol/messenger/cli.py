import argparse
import asyncio
from pathlib import Path

from magentic_marketplace.platform.database.sqlite import connect_to_sqlite_database
from magentic_marketplace.platform.launcher import MarketplaceLauncher

from .protocol import MessengerProtocol


async def main():
    """Start the Messenger marketplace server."""
    parser = argparse.ArgumentParser(description="Launch Messenger marketplace server.")
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
        help=("SQLite database path (default: messenger_marketplace.db)"),
    )
    parser.add_argument(
        "--resume", action="store_true", default=False, help="Resume from an existing database."
    )

    parser.add_argument(
        "--overwrite", action="store_true", default=False, help="Overwrite database if it exists."
    )

    args = parser.parse_args()

    if args.resume and args.overwrite:
        print("Error: Cannot specify both --resume and --overwrite. Specify one or zero.")
        raise SystemExit(1)

    # Set default database name based on scenario directory if not specified
    if args.database is None:
        args.database = Path("messenger_marketplace.db")

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

    protocol = MessengerProtocol()

    async with MarketplaceLauncher(
        protocol=protocol,
        database_factory=lambda: connect_to_sqlite_database(args.database),
        host=args.host,
        port=args.port,
        title="Messenger Marketplace API",
        description="A marketplace for text messaging-based agent communication",
        experiment_name="messenger_marketplace",
    ) as launcher:
        print("\n" + "=" * 70)
        print("Messenger Marketplace Server Running")
        print("=" * 70)
        print(f"Server URL: {launcher.server_url}")
        print(f"API Docs: {launcher.server_url}/docs")
        print(f"Database: {args.database}")
        print("=" * 70)

        try:
            # Keep the server running
            await asyncio.Event().wait()
        except KeyboardInterrupt:
            print("\n\nShutting down Messenger Marketplace Server...")


if __name__ == "__main__":
    asyncio.run(main())
