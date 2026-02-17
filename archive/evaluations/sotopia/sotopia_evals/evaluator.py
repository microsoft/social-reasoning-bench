from .clients import ModelClient
from .prompts import create_evaluation_prompt
from .types import SotopiaEvaluation


class SotopiaEvaluator:
    """Evaluator for Sotopia social interactions using LLM-as-a-judge."""

    def __init__(self, client: ModelClient):
        """
        Initialize the evaluator.

        Args:
            client: ModelClient instance (OpenAI, Gemini, etc.)
        """
        self.client = client

    def evaluate(
        self,
        scenario: str,
        agent_1_name: str,
        agent_2_name: str,
        agent_1_background: str,
        agent_2_background: str,
        agent_1_goal: str,
        agent_2_goal: str,
        conversation: str,
    ) -> SotopiaEvaluation:
        """
        Evaluate a social interaction using LLM-as-a-judge.

        Args:
            scenario: Description of the scenario
            agent_1_name: Name of the first agent
            agent_2_name: Name of the second agent
            agent_1_background: Background description of the first agent
            agent_2_background: Background description of the second agent
            agent_1_goal: Social goal of the first agent
            agent_2_goal: Social goal of the second agent
            conversation: The conversation transcript

        Returns:
            SotopiaEvaluation with evaluations for both agents
        """
        prompt = create_evaluation_prompt(
            scenario=scenario,
            agent_1_name=agent_1_name,
            agent_2_name=agent_2_name,
            agent_1_background=agent_1_background,
            agent_2_background=agent_2_background,
            agent_1_goal=agent_1_goal,
            agent_2_goal=agent_2_goal,
            conversation=conversation,
        )

        return self.client.evaluate(prompt, SotopiaEvaluation)
