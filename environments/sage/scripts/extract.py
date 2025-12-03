"""Extract action sequences and transcripts from messenger marketplace database.

This wrapper script extracts both action sequences and transcripts from a
messenger marketplace SQLite database, organizing them into separate
subdirectories.

Usage:
    # Extract from default database
    python scripts/extract.py

    # Extract from specific database
    python scripts/extract.py --database path/to/db.db

    # Specify output directory (will create actions/ and transcripts/ subdirs)
    python scripts/extract.py --output-dir output/

    # Extract only action sequences
    python scripts/extract.py --actions-only

    # Extract only transcripts
    python scripts/extract.py --transcripts-only
"""

import argparse
import asyncio
import sys
from pathlib import Path

# Import the extraction functions from the renamed scripts
from extract_action_sequences import (  # noqa: E402  # type: ignore
    generate_agent_action_sequences,
    load_actions,
    load_agents,
)
from extract_transcripts import (  # noqa: E402  # type: ignore
    generate_dm_transcripts,
    generate_group_transcripts,
    load_groups,
    load_messages,
)


async def main():
    """Main entry point for the extraction wrapper script."""
    parser = argparse.ArgumentParser(
        description=("Extract action sequences and transcripts from messenger marketplace database")
    )
    parser.add_argument(
        "--database",
        type=Path,
        default="messenger_marketplace.db",
        help="Path to SQLite database (default: messenger_marketplace.db)",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default="output",
        help="Base output directory (default: output/)",
    )
    parser.add_argument(
        "--actions-only",
        action="store_true",
        help="Extract only action sequences",
    )
    parser.add_argument(
        "--transcripts-only",
        action="store_true",
        help="Extract only transcripts",
    )

    args = parser.parse_args()

    # Check database exists
    if not args.database.exists():
        print(f"Error: Database not found at {args.database}")
        return 1

    # Determine what to extract
    extract_actions = not args.transcripts_only
    extract_transcripts = not args.actions_only

    print(f"Loading data from {args.database}...")
    print("=" * 70)

    # Load common data
    agents = await load_agents(args.database)
    print(f"Found {len(agents)} agents")

    # Create base output directory with database name subdirectory
    base_output_dir = args.output_dir / args.database.stem
    base_output_dir.mkdir(parents=True, exist_ok=True)

    # Extract action sequences
    if extract_actions:
        print("\n" + "=" * 70)
        print("EXTRACTING ACTION SEQUENCES")
        print("=" * 70)

        actions = await load_actions(args.database)
        print(f"Found {len(actions)} actions")

        # Pass the base output dir; generate_agent_action_sequences will use it directly
        actions_output_dir = base_output_dir / "actions"
        actions_output_dir.mkdir(parents=True, exist_ok=True)

        print("\nGenerating action sequences...")
        generate_agent_action_sequences(actions, agents, actions_output_dir)
        print(f"Action sequences saved to: {actions_output_dir.absolute()}")

    # Extract transcripts
    if extract_transcripts:
        print("\n" + "=" * 70)
        print("EXTRACTING TRANSCRIPTS")
        print("=" * 70)

        groups = await load_groups(args.database)
        messages = await load_messages(args.database)
        print(f"Found {len(groups)} groups")
        print(f"Found {len(messages)} messages")

        # Pass the base output dir; transcript functions will create subdirectories
        transcripts_output_dir = base_output_dir / "transcripts"
        transcripts_output_dir.mkdir(parents=True, exist_ok=True)

        print("\nGenerating transcripts...")
        generate_group_transcripts(messages, groups, agents, transcripts_output_dir)
        generate_dm_transcripts(messages, agents, transcripts_output_dir)
        print(f"Transcripts saved to: {transcripts_output_dir.absolute()}")

    # Summary
    print("\n" + "=" * 70)
    print("EXTRACTION COMPLETE")
    print("=" * 70)
    print(f"All outputs saved to: {base_output_dir.absolute()}")

    if extract_actions:
        print(f"  - Action sequences: {(base_output_dir / 'actions').absolute()}")
    if extract_transcripts:
        print(f"  - Transcripts: {(base_output_dir / 'transcripts').absolute()}")

    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
