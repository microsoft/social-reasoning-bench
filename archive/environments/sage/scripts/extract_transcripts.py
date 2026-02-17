"""Extract transcripts from messenger marketplace database.

This script reads a messenger marketplace SQLite database and generates
transcript files for each group chat and direct message conversation.

Usage:
    # Extract transcripts from default database
    python scripts/extract_transcripts.py

    # Extract from specific database
    python scripts/extract_transcripts.py --database path/to/db.db

    # Specify output directory
    python scripts/extract_transcripts.py --output-dir transcripts/
"""

import argparse
import asyncio
from collections import defaultdict
from pathlib import Path

import yaml
from magentic_marketplace.platform.database.sqlite import connect_to_sqlite_database


# Custom YAML representer for literal block style multiline strings
def literal_str_representer(dumper, data):
    """Use literal block style (|-) for multiline strings.

    PyYAML has restrictions on trailing spaces and tabs in block literals,
    so we clean those up before representing.
    """
    if len(data.splitlines()) > 1:
        # Remove trailing spaces (PyYAML restriction)
        cleaned = "\n".join([line.rstrip() for line in data.strip().splitlines()])
        # Replace tabs with spaces (PyYAML restriction)
        cleaned = cleaned.replace("\t", "    ")
        return dumper.represent_scalar("tag:yaml.org,2002:str", cleaned, style="|")
    return dumper.represent_scalar("tag:yaml.org,2002:str", data)


# Custom dumper class
class LiteralDumper(yaml.SafeDumper):
    pass


LiteralDumper.add_representer(str, literal_str_representer)


def get_agent_name(agent_id: str, agents: dict[str, str]) -> str:
    """Get agent name from ID, with fallback to ID if not found."""
    return agents.get(agent_id, agent_id)


async def load_agents(db_path: str) -> dict[str, str]:
    """Load agent ID to name mapping from database.

    Args:
        db_path: Path to SQLite database

    Returns:
        Dictionary mapping agent_id to full_name
    """
    async with connect_to_sqlite_database(db_path) as db:
        agent_rows = await db.agents.get_all()

        agents = {}
        for row in agent_rows:
            full_name = getattr(row.data, "full_name", row.data.id)
            agents[row.data.id] = full_name

        return agents


async def load_groups(db_path: str) -> dict[str, dict]:
    """Load group information from database actions.

    Args:
        db_path: Path to SQLite database

    Returns:
        Dictionary mapping group_id to group info
    """
    async with connect_to_sqlite_database(db_path) as db:
        action_rows = await db.actions.get_all()

        groups = {}
        for row in action_rows:
            # Check if this action has a group creation result
            if hasattr(row.data, "result") and hasattr(row.data.result, "content"):
                result_content = row.data.result.content
                if isinstance(result_content, dict):
                    group_id = result_content.get("id")
                    if group_id and group_id.startswith("group_"):
                        groups[group_id] = {
                            "name": result_content.get("name", group_id),
                            "members": result_content.get("members", []),
                            "created_by": result_content.get("created_by"),
                        }

        return groups


async def load_messages(db_path: str) -> list[dict]:
    """Load all messages from database.

    Args:
        db_path: Path to SQLite database

    Returns:
        List of message dictionaries sorted by rowid
    """
    async with connect_to_sqlite_database(db_path) as db:
        action_rows = await db.actions.get_all()

        messages = []
        for row in action_rows:
            # Check if this action is a SendMessage action
            if hasattr(row.data, "request"):
                request = row.data.request
                request_name = getattr(request, "name", None)

                # Handle both class name (SendMessageToConversation) and type field (SendMessage)
                if request_name in ("SendMessage", "SendMessageToConversation"):
                    params = getattr(request, "parameters", {})
                    conversation_id = params.get("conversation_id")

                    message = {
                        "from": row.data.agent_id,
                        "message": params.get("message"),
                        "timestamp": row.created_at.isoformat(),
                        "conversation_id": conversation_id,
                    }

                    # Determine if group or direct message based on conversation_id
                    if conversation_id and conversation_id.startswith("group_"):
                        message["type"] = "group"
                        message["group_id"] = conversation_id
                    else:
                        message["type"] = "direct"
                        message["to"] = conversation_id

                    messages.append(message)

        return messages


def generate_group_transcripts(
    messages: list[dict], groups: dict, agents: dict, output_dir: Path
) -> None:
    """Generate transcript files for group chats in YAML format.

    Args:
        messages: List of all messages
        groups: Dictionary of group information
        agents: Dictionary mapping agent_id to name
        output_dir: Directory to save transcripts
    """
    # Group messages by group_id
    group_messages = defaultdict(list)
    for msg in messages:
        if msg["type"] == "group":
            group_id = msg.get("group_id")
            if group_id:
                group_messages[group_id].append(msg)

    # Generate transcript for each group
    group_dir = output_dir / "groups"
    group_dir.mkdir(exist_ok=True)

    for group_id, msgs in group_messages.items():
        group_info = groups.get(group_id, {})
        group_name = group_info.get("name", group_id)

        # Create safe filename
        safe_name = "".join(c if c.isalnum() or c in (" ", "-", "_") else "_" for c in group_name)
        filename = f"{safe_name}_{group_id}.yaml"
        filepath = group_dir / filename

        # Build YAML structure
        transcript = {
            "title": group_name,
            "id": group_id,
            "members": [get_agent_name(m, agents) for m in group_info.get("members", [])],
            "total_messages": len(msgs),
            "messages": [
                {
                    "from": get_agent_name(msg["from"], agents),
                    "timestamp": msg["timestamp"],
                    "message": msg["message"],
                }
                for msg in msgs
            ],
        }

        # Write YAML file with literal block scalars for messages
        with open(filepath, "w") as f:
            yaml.dump(
                transcript,
                f,
                Dumper=LiteralDumper,
                default_flow_style=False,
                allow_unicode=True,
                sort_keys=False,
            )

        print(f"Generated group transcript: {filepath}")


def generate_dm_transcripts(messages: list[dict], agents: dict, output_dir: Path) -> None:
    """Generate transcript files for direct message conversations in YAML format.

    Args:
        messages: List of all messages
        agents: Dictionary mapping agent_id to name
        output_dir: Directory to save transcripts
    """
    # Group messages by conversation (sorted pair of participants)
    dm_conversations = defaultdict(list)
    for msg in messages:
        if msg["type"] == "direct":
            sender = msg.get("from")
            recipient = msg.get("to")
            if sender and recipient:
                # Create consistent key for conversation
                conv_key = tuple(sorted([sender, recipient]))
                dm_conversations[conv_key].append(msg)

    # Generate transcript for each DM conversation
    dm_dir = output_dir / "direct_messages"
    dm_dir.mkdir(exist_ok=True)

    for (participant1, participant2), msgs in dm_conversations.items():
        name1 = get_agent_name(participant1, agents)
        name2 = get_agent_name(participant2, agents)

        # Create safe filename
        safe_name1 = "".join(c if c.isalnum() or c in (" ", "-", "_") else "_" for c in name1)
        safe_name2 = "".join(c if c.isalnum() or c in (" ", "-", "_") else "_" for c in name2)
        filename = f"{safe_name1}_and_{safe_name2}.yaml"
        filepath = dm_dir / filename

        # Build YAML structure
        transcript = {
            "title": f"{name1} and {name2}",
            "participants": [name1, name2],
            "total_messages": len(msgs),
            "messages": [
                {
                    "from": get_agent_name(msg["from"], agents),
                    "timestamp": msg["timestamp"],
                    "message": msg["message"],
                }
                for msg in msgs
            ],
        }

        # Write YAML file
        with open(filepath, "w") as f:
            yaml.dump(
                transcript,
                f,
                Dumper=LiteralDumper,
                default_flow_style=False,
                allow_unicode=True,
                sort_keys=False,
            )

        print(f"Generated DM transcript: {filepath}")


async def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description="Extract transcripts from messenger marketplace database"
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
        default="transcripts",
        help="Output directory for transcripts (default: transcripts/)",
    )

    args = parser.parse_args()

    # Check database exists
    if not args.database.exists():
        print(f"Error: Database not found at {args.database}")
        return 1

    print(f"Loading data from {args.database}...")

    # Load data
    agents = await load_agents(args.database)
    groups = await load_groups(args.database)
    messages = await load_messages(args.database)

    print(f"Found {len(agents)} agents")
    print(f"Found {len(groups)} groups")
    print(f"Found {len(messages)} messages")

    # Create output directory
    args.output_dir = args.output_dir / args.database.stem
    args.output_dir.mkdir(parents=True, exist_ok=True)

    # Generate transcripts
    print("\nGenerating transcripts...")
    generate_group_transcripts(messages, groups, agents, args.output_dir)
    generate_dm_transcripts(messages, agents, args.output_dir)

    print(f"\nTranscripts saved to: {args.output_dir.absolute()}")
    return 0


if __name__ == "__main__":
    exit(asyncio.run(main()))
