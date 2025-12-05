def create_evaluation_prompt(
    scenario: str,
    agent_1_name: str,
    agent_2_name: str,
    agent_1_background: str,
    agent_2_background: str,
    agent_1_goal: str,
    agent_2_goal: str,
    conversation: str,
) -> str:
    """
    Create an evaluation prompt for Sotopia social interactions.

    """
    return f"""Here is the context of this interaction:
Scenario: {scenario}
Participants: {agent_1_name} and {agent_2_name}
{agent_1_name}'s background: {agent_1_background}
{agent_2_name}'s background: {agent_2_background}
{agent_1_name}'s goal: {agent_1_goal}
{agent_2_name}'s goal: {agent_2_goal}
{conversation}
Based on previous interactions, evaluate how well participants achieve their goals.

The output should be formatted as a JSON instance that conforms to the provided JSON schema."""
