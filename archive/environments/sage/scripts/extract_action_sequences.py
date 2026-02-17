"""Extract action sequences from messenger marketplace database.

This script reads a messenger marketplace SQLite database and generates
action sequence files for each agent, showing all actions they performed
in chronological order.

Usage:
    # Extract action sequences from default database
    python scripts/extract_action_sequences.py

    # Extract from specific database
    python scripts/extract_action_sequences.py --database path/to/db.db

    # Specify output directory
    python scripts/extract_action_sequences.py --output-dir action_sequences/
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


async def load_actions(db_path: str) -> list[dict]:
    """Load all actions from database.

    Args:
        db_path: Path to SQLite database

    Returns:
        List of action dictionaries with parsed data, sorted by timestamp
    """
    async with connect_to_sqlite_database(db_path) as db:
        action_rows = await db.actions.get_all()

        actions = []
        for row in action_rows:
            action = {
                "agent_id": row.data.agent_id,
                "timestamp": row.created_at.isoformat(),
                "action_type": None,
                "parameters": {},
                "result": {},
                "is_error": False,
            }

            # Extract request information
            if hasattr(row.data, "request"):
                request = row.data.request
                action["action_type"] = getattr(request, "name", None)
                action["parameters"] = getattr(request, "parameters", {})

            # Extract result information
            if hasattr(row.data, "result"):
                result = row.data.result
                action["is_error"] = getattr(result, "is_error", False)

                # Get result content
                content = getattr(result, "content", None)
                if content is not None:
                    # Convert to dict if it's a Pydantic model
                    if hasattr(content, "model_dump"):
                        action["result"] = content.model_dump()
                    elif isinstance(content, (dict, str, list, int, float, bool)):
                        action["result"] = content
                    else:
                        action["result"] = str(content)

            actions.append(action)

        return actions


def serialize_for_yaml(obj):
    """Serialize objects for YAML output, handling various types."""
    if isinstance(obj, dict):
        return {k: serialize_for_yaml(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [serialize_for_yaml(item) for item in obj]
    elif isinstance(obj, (str, int, float, bool, type(None))):
        return obj
    else:
        # For other types, convert to string
        return str(obj)


def generate_agent_action_sequences(actions: list[dict], agents: dict, output_dir: Path) -> None:
    """Generate action sequence files for each agent in YAML format.

    Args:
        actions: List of all actions
        agents: Dictionary mapping agent_id to name
        output_dir: Directory to save action sequences
    """
    # Group actions by agent_id
    agent_actions = defaultdict(list)
    for action in actions:
        agent_id = action.get("agent_id")
        if agent_id:
            agent_actions[agent_id].append(action)

    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)

    # Generate action sequence file for each agent
    for agent_id, agent_action_list in agent_actions.items():
        agent_name = get_agent_name(agent_id, agents)

        # Create safe filename
        safe_name = "".join(c if c.isalnum() or c in (" ", "-", "_") else "_" for c in agent_name)
        filename = f"{safe_name}.yaml"
        filepath = output_dir / filename

        # Build action sequence structure
        action_sequence = {
            "agent_name": agent_name,
            "agent_id": agent_id,
            "total_actions": len(agent_action_list),
            "actions": [],
        }

        for action in agent_action_list:
            action_entry = {
                "timestamp": action["timestamp"],
                "action_type": action["action_type"],
                "parameters": serialize_for_yaml(action["parameters"]),
                "is_error": action["is_error"],
            }

            # Only include result if it's not empty
            if action["result"]:
                action_entry["result"] = serialize_for_yaml(action["result"])

            action_sequence["actions"].append(action_entry)

        # Write YAML file with literal block scalars for multiline strings
        with open(filepath, "w") as f:
            yaml.dump(
                action_sequence,
                f,
                Dumper=LiteralDumper,
                default_flow_style=False,
                allow_unicode=True,
                sort_keys=False,
            )

        print(f"Generated action sequence: {filepath}")


async def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description="Extract action sequences from messenger marketplace database"
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
        default="action_sequences",
        help="Output directory for action sequences (default: action_sequences/)",
    )

    args = parser.parse_args()

    # Check database exists
    if not args.database.exists():
        print(f"Error: Database not found at {args.database}")
        return 1

    print(f"Loading data from {args.database}...")

    # Load data
    agents = await load_agents(args.database)
    actions = await load_actions(args.database)

    print(f"Found {len(agents)} agents")
    print(f"Found {len(actions)} actions")

    # Create output directory with database name
    args.output_dir = args.output_dir / args.database.stem
    args.output_dir.mkdir(parents=True, exist_ok=True)

    # Generate action sequences
    print("\nGenerating action sequences...")
    generate_agent_action_sequences(actions, agents, args.output_dir)

    print(f"\nAction sequences saved to: {args.output_dir.absolute()}")
    return 0


if __name__ == "__main__":
    exit(asyncio.run(main()))
