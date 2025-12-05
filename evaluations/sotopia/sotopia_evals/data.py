import json
from pathlib import Path
from typing import Any


def load_episode(file_path: str | Path) -> dict[str, Any]:
    """Load an episode from a JSON file."""
    with open(file_path) as f:
        return json.load(f)


def format_conversation(social_interactions: str) -> str:
    """Format the social interactions string into a conversation transcript."""
    lines = social_interactions.strip().split("\n\n")
    formatted_turns = []
    for i, line in enumerate(lines):
        if line.strip():
            formatted_turns.append(f"Turn #{i + 1}\n{line}")
    return "\n".join(formatted_turns)


def extract_evaluation_data(episode: dict[str, Any]) -> dict[str, str]:
    """
    Extract data needed for evaluation from an episode.

    Args:
        episode: Episode dictionary loaded from JSON

    Returns:
        Dictionary with keys:
        - scenario: str
        - agent_1_name: str
        - agent_2_name: str
        - agent_1_background: str
        - agent_2_background: str
        - agent_1_goal: str
        - agent_2_goal: str
        - conversation: str
    """
    agent_names = list(episode["agents_background"].keys())
    agent_1_name = agent_names[0]
    agent_2_name = agent_names[1]

    # Clean up goal text by removing XML tags
    def clean_goal(goal: str) -> str:
        # Remove extra_info tags and their contents for cleaner display
        import re

        goal = re.sub(r"\s*\(<extra_info>.*?</extra_info>\)", "", goal)
        return goal.strip()

    return {
        "scenario": episode["scenario"],
        "agent_1_name": agent_1_name,
        "agent_2_name": agent_2_name,
        "agent_1_background": episode["agents_background"][agent_1_name],
        "agent_2_background": episode["agents_background"][agent_2_name],
        "agent_1_goal": clean_goal(episode["social_goals"][agent_1_name]),
        "agent_2_goal": clean_goal(episode["social_goals"][agent_2_name]),
        "conversation": format_conversation(episode["social_interactions"]),
    }
