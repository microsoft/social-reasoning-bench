"""Factory functions for agent creation."""

from pathlib import Path

from pydantic_core import from_json

from ..agents import ChatCompletionsAgent, OpenAIAgentProfile, ResponsesAgent


def load_profiles_from_dir(
    dirpath: Path | str,
) -> list[OpenAIAgentProfile]:
    """Load all agent profiles from a directory.

    Args:
        scenario_dir: Path to directory containing agent_*.json files

    Returns:
        List of OpenAIAgentProfile instances, sorted by agent number

    Raises:
        FileNotFoundError: If directory doesn't exist
        ValueError: If no agent files found in directory
    """
    dirpath = Path(dirpath)

    if not dirpath.exists():
        raise FileNotFoundError(f"Directory not found: {dirpath}")

    # Find all agent JSON files
    agent_files = sorted(dirpath.glob("*.json"))

    if not agent_files:
        raise ValueError(f"No *.json files found in: {dirpath}")

    # Load and parse each profile
    # Use from_json + model_validate instead of model_validate_json to avoid
    # Pydantic lazy validation issues with OpenAI's Union[TypedDict] types
    profiles = []
    for agent_file in agent_files:
        with open(agent_file, "rb") as f:
            data = from_json(f.read())
        profile = OpenAIAgentProfile.model_validate(data)
        profiles.append(profile)

    return profiles


def create_agent_from_profile(
    profile: OpenAIAgentProfile,
    base_url: str,
    agent_type: str = "chat-completions",
    openai_api_key: str | None = None,
    openai_model: str = "",
    max_iterations: int = 50,
) -> ChatCompletionsAgent | ResponsesAgent:
    """Factory function to create an agent from a profile.

    Args:
        profile: The agent profile
        base_url: Marketplace server URL
        agent_type: Type of agent to create ('chat-completions' or 'responses')
        openai_api_key: OpenAI API key (or use OPENAI_API_KEY env var)
        openai_model: OpenAI model to use
        max_iterations: Maximum number of steps before stopping

    Returns:
        Agent instance (ChatCompletionsAgent or ResponsesAgent)

    Raises:
        ValueError: If agent_type is not recognized
    """
    if agent_type == "chat-completions":
        return ChatCompletionsAgent(
            profile=profile,
            base_url=base_url,
            openai_api_key=openai_api_key,
            openai_model=openai_model,
            max_iterations=max_iterations,
        )
    elif agent_type == "responses":
        return ResponsesAgent(
            profile=profile,
            base_url=base_url,
            openai_api_key=openai_api_key,
            openai_model=openai_model,
            max_iterations=max_iterations,
        )
    else:
        raise ValueError(
            f"Unknown agent type: {agent_type}. Must be 'chat-completions' or 'responses'"
        )
