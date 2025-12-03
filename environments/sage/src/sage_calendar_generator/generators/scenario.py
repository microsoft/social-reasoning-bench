"""Generator for scenario descriptions using LLM."""

from typing import Any

from pydantic import BaseModel, Field

from ..context import ScenarioContext
from .base import BaseLLMGenerator


class ScenarioDescription(BaseModel):
    """LLM response schema for scenario generation."""

    description: str = Field(
        description="Detailed scenario description including context, setting, and the general nature of the scheduling challenge"
    )
    theme: str = Field(
        description="Brief theme or domain (e.g., 'enterprise team meeting', 'academic committee', 'startup planning')"
    )
    suggested_goal_title: str = Field(
        description="Suggested title for the goal event to be scheduled"
    )


class ScenarioGenerator(BaseLLMGenerator[ScenarioDescription]):
    """Generates scenario descriptions using LLM.

    This is the first phase of the generation pipeline.
    """

    def get_response_format(self) -> type[ScenarioDescription]:
        """Get the Pydantic model for structured output."""
        return ScenarioDescription

    def build_prompt(self, context: Any, **kwargs: Any) -> str:
        """Build the prompt for scenario generation.

        Args:
            context: ScenarioContext with generation parameters
            **kwargs: Unused

        Returns:
            Complete prompt string
        """
        if not isinstance(context, ScenarioContext):
            raise TypeError(f"Expected ScenarioContext, got {type(context)}")

        # Build the user message
        user_parts = [
            f"Generate a scheduling scenario with {context.num_participants} participants.",
        ]

        if context.scenario_hint:
            user_parts.append(f"Theme/hint: {context.scenario_hint}")

        user_parts.append(
            "\nCreate a rich, detailed scenario description that will guide the generation of participant profiles and calendar events."
        )

        return "\n".join(user_parts)

    async def generate(
        self,
        context: Any,
        messages: list[dict[str, Any]],
        **kwargs: Any,
    ) -> ScenarioDescription:
        """Override generate to add system message on first call.

        Args:
            context: Scenario generation context
            messages: Shared LLM conversation history (will be appended to)
            **kwargs: Additional keyword arguments

        Returns:
            Generated scenario description
        """
        # Build the system message
        system_message = """You are an expert at creating realistic multi-party scheduling scenarios for testing AI scheduling systems.

Your task is to generate a detailed scenario description that will be used to create a calendar scheduling challenge. The scenario should:

1. Use SPECIFIC details: actual company names, product names, team names, project codenames
   - Good: "TechFlow Solutions", "Project Aurora", "Enterprise Sales Team"
   - Bad: "a tech company", "a project", "the team"
2. Have a clear context and setting (e.g., enterprise team, academic committee, startup, non-profit, etc.)
3. Include believable roles and relationships between participants
4. Describe a realistic scheduling situation that requires coordination
5. Set up a context where scheduling conflicts are natural and expected

The scenario should feel authentic and grounded in real-world situations.

IMPORTANT: Please sample at random from the tails of the distribution, such that the probability of each response is less than 0.10. Be creative and unique."""

        # Add system message on first call
        if not messages:
            messages.append({"role": "system", "content": system_message})

        # Call parent implementation
        return await super().generate(context, messages, **kwargs)
