"""Convert MAGPIE dataset rows to OpenAIAgentProfile format.

This script loads the jaypasnagasai/magpie dataset from HuggingFace and converts
each agent in each scenario to an OpenAIAgentProfile.

Requirements:
    pip install datasets

Usage:
    # Preview first 5 profiles
    python scripts/convert_magpie_to_profiles.py --preview 5

    # Convert and save to JSON
    python scripts/convert_magpie_to_profiles.py --output data/magpie_profiles.json

    # Use programmatically
    from scripts.convert_magpie_to_profiles import convert_magpie_to_profiles
    profiles = convert_magpie_to_profiles()
"""

import json
from pathlib import Path
from typing import cast

from datasets import Dataset, load_dataset
from pydantic_core import to_json
from sage_agents import OpenAIAgentProfile


def generate_email(name: str) -> str:
    """Generate an email address from a name.

    Args:
        name: The agent's name

    Returns:
        Generated email address
    """
    # Convert name to lowercase, replace spaces with dots
    email_local = name.lower().replace(" ", ".").replace("'", "")
    return f"{email_local}@example.com"


def extract_agent_info(agent_dict: dict, task: str) -> dict:
    """Extract relevant information from an agent dictionary.

    Args:
        agent_dict: The agent dictionary from the dataset
        task: The overall task description

    Returns:
        Dictionary with extracted agent information

    Raises:
        ValueError: If agent name is not found in agent_dict
    """
    # Get agent name - error if not found
    name = agent_dict.get("name") or agent_dict.get("agent_name")
    if not name:
        raise ValueError(
            f"Agent name not found in agent_dict: {to_json(agent_dict, indent=2).decode()}"
        )

    # Description is the entire agent_dict as formatted JSON
    description = to_json(agent_dict, indent=2).decode()

    # Task is always the task argument (scenario-level task)
    agent_task = task

    return {
        "name": name,
        "description": description,
        "task": agent_task,
    }


def convert_magpie_to_profiles(
    dataset_name: str = "jaypasnagasai/magpie",
    split: str = "train",
    output_file: Path | None = None,
    output_dir: Path | None = None,
) -> list[OpenAIAgentProfile]:
    """Convert MAGPIE dataset to OpenAIAgentProfile instances.

    Args:
        dataset_name: Name of the HuggingFace dataset
        split: Dataset split to load
        output_file: Optional path to save all profiles as single JSON file
        output_dir: Optional directory to save profiles grouped by scenario
                    (one folder per scenario, one file per agent)

    Returns:
        List of OpenAIAgentProfile instances
    """
    print(f"Loading dataset: {dataset_name} (split: {split})...")
    dataset = cast(Dataset, load_dataset(dataset_name, split=split))

    profiles = []

    print(f"Processing {len(dataset)} scenarios...")
    for idx, row in enumerate(dataset):
        # Suppress linter errors
        assert isinstance(row, dict)
        scenario = row.get("scenario", "")
        task = row.get("task", "")
        agents_json = row.get("agents", "[]")

        # Parse JSON fields
        try:
            agents = json.loads(agents_json) if isinstance(agents_json, str) else agents_json
        except json.JSONDecodeError as e:
            print(f"Warning: Could not parse JSON in row {idx}: {e}")
            continue

        # If agents is a list of dicts, process each agent
        if isinstance(agents, list):
            for agent_idx, agent in enumerate(agents):
                if isinstance(agent, dict):
                    try:
                        # Extract agent info
                        agent_info = extract_agent_info(agent, task)

                        # Generate email and use it as ID
                        email_address = generate_email(agent_info["name"])

                        # Create profile
                        profile = OpenAIAgentProfile(
                            id=email_address,
                            full_name=agent_info["name"],
                            email_address=email_address,
                            messages=[
                                {
                                    "role": "system",
                                    "content": agent_info["description"],
                                },
                                {"role": "user", "content": agent_info["task"]},
                            ],
                            metadata={
                                "source": "magpie",
                                "scenario_id": idx,
                                "file_name": row.get("file_name", ""),
                                "scenario": scenario,
                                "task": task,
                                "success_criteria": row.get("success_criteria", ""),
                                "constraints": row.get("constraints", ""),
                                "deliverable": row.get("deliverable", ""),
                            },
                        )
                        profiles.append(profile)
                    except ValueError as e:
                        print(f"Warning: Skipping agent {agent_idx} in scenario {idx}: {e}")
                        continue
        elif isinstance(agents, dict):
            try:
                # Handle case where agents is a single dict
                agent_info = extract_agent_info(agents, task)

                # Generate email and use it as ID
                email_address = generate_email(agent_info["name"])

                profile = OpenAIAgentProfile(
                    id=email_address,
                    full_name=agent_info["name"],
                    email_address=email_address,
                    messages=[
                        {"role": "system", "content": agent_info["description"]},
                        {"role": "user", "content": agent_info["task"]},
                    ],
                    metadata={
                        "source": "magpie",
                        "scenario_id": idx,
                        "file_name": row.get("file_name", ""),
                        "scenario": scenario,
                        "task": task,
                        "success_criteria": row.get("success_criteria", ""),
                        "constraints": row.get("constraints", ""),
                        "deliverable": row.get("deliverable", ""),
                    },
                )
                profiles.append(profile)
            except ValueError as e:
                print(f"Warning: Skipping scenario {idx}: {e}")
                continue

    print(f"Created {len(profiles)} agent profiles from {len(dataset)} scenarios")

    # Save to single file if requested
    if output_file:
        output_file = Path(output_file)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        # Convert to JSON-serializable format
        profiles_data = [profile.model_dump(mode="json") for profile in profiles]

        with open(output_file, "w") as f:
            json.dump(profiles_data, f, indent=2)

        print(f"Saved all profiles to: {output_file}")

    # Save to directory structure if requested (grouped by scenario)
    if output_dir:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        # Group profiles by scenario
        from collections import defaultdict

        scenario_groups: dict[int, list[OpenAIAgentProfile]] = defaultdict(list)
        for profile in profiles:
            scenario_id = profile.metadata.get("scenario_id")
            if scenario_id is not None:
                scenario_groups[scenario_id].append(profile)

        # Save each scenario to its own folder
        for scenario_id, scenario_profiles in scenario_groups.items():
            scenario_dir = output_dir / f"scenario_{scenario_id}"
            scenario_dir.mkdir(exist_ok=True)

            # Save each agent as a separate file
            for agent_idx, profile in enumerate(scenario_profiles):
                agent_file = scenario_dir / f"agent_{agent_idx}.json"
                profile_data = profile.model_dump(mode="json")

                with open(agent_file, "w") as f:
                    json.dump(profile_data, f, indent=2)

        print(
            f"Saved {len(profiles)} profiles to {len(scenario_groups)} "
            f"scenario folders in: {output_dir}"
        )

    return profiles


def main():
    """Main entry point for the script."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Convert MAGPIE dataset to OpenAIAgentProfile format"
    )
    parser.add_argument(
        "--dataset",
        default="jaypasnagasai/magpie",
        help="HuggingFace dataset name",
    )
    parser.add_argument(
        "--split",
        default="train",
        help="Dataset split to load",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Output JSON file path (saves all profiles to single file)",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        help="Output directory (saves profiles grouped by scenario: "
        "one folder per scenario, one file per agent)",
    )
    parser.add_argument(
        "--preview",
        type=int,
        default=0,
        help="Number of profiles to preview (0 for none)",
    )

    args = parser.parse_args()

    # Convert dataset
    profiles = convert_magpie_to_profiles(
        dataset_name=args.dataset,
        split=args.split,
        output_file=args.output,
        output_dir=args.output_dir,
    )

    # Preview profiles if requested
    if args.preview > 0:
        print(f"\nPreviewing first {args.preview} profiles:")
        print("=" * 80)
        for profile in profiles[: args.preview]:
            print(f"\nName: {profile.full_name}")
            print(f"Email: {profile.email_address}")
            messages = profile.get_messages()
            system_msg = next((m["content"] for m in messages if m["role"] == "system"), "")
            user_msg = next((m["content"] for m in messages if m["role"] == "user"), "")
            print(f"Description: {str(system_msg)[:100]}...")
            print(f"Task: {str(user_msg)[:100]}...")
            print("-" * 80)


if __name__ == "__main__":
    main()
