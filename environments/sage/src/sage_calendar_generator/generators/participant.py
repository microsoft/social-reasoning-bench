"""Generator for participant profiles using LLM."""

from typing import Any

from sage_protocol.calendar.entities import ParticipantProfile
from sage_protocol.calendar.utils.participant_mapper import ParticipantMapper

from ..context import ParticipantContext
from .base import BaseLLMGenerator


class ParticipantGenerator(BaseLLMGenerator[ParticipantProfile]):
    """Generates participant profiles using LLM.

    This is the second phase of the generation pipeline, creating N participants
    with diverse roles and timezones.
    """

    def get_response_format(self) -> type[ParticipantProfile]:
        """Get the Pydantic model for structured output."""
        return ParticipantProfile

    async def generate(
        self,
        context: Any,
        messages: list[dict[str, Any]],
        **kwargs: Any,
    ) -> ParticipantProfile:
        """Generate participant profile with email ID validation.

        Overrides base to add validation that participant ID is a valid email.

        Args:
            context: ParticipantContext
            messages: Shared LLM conversation history
            **kwargs: Additional arguments

        Returns:
            Generated participant profile

        Raises:
            ValueError: If generated ID is not a valid email format
        """
        # Call parent to generate
        participant = await super().generate(context, messages, **kwargs)

        # Validate that ID is a valid email
        if not ParticipantMapper.is_valid_email(participant.id):
            raise ValueError(
                f"Generated participant ID '{participant.id}' is not a valid email address. "
                f"Participant: {participant.name}. "
                f"The LLM must generate email-formatted IDs (e.g., firstname.lastname@company.com)."
            )

        return participant

    def build_prompt(self, context: Any, **kwargs: Any) -> str:
        """Build the prompt for participant generation.

        Args:
            context: ParticipantContext with generation parameters
            **kwargs: Unused

        Returns:
            Complete prompt string
        """
        if not isinstance(context, ParticipantContext):
            raise TypeError(f"Expected ParticipantContext, got {type(context)}")

        # Build the user message
        user_parts = [
            f"Generate participant {context.participant_index + 1} of {context.num_participants} for this scenario.",
            f"\nScenario context: {context.scenario_description}",
        ]

        if context.existing_participants:
            user_parts.append("\nExisting participants:")
            for p in context.existing_participants:
                user_parts.append(f"- {p.name} ({p.description}), timezone: {p.timezone}")

        user_parts.extend(
            [
                f"\nThis participant should be in timezone: {context.timezone_hint}",
            ]
        )

        if context.email_hint:
            user_parts.append(
                f"\nEmail hint: {context.email_hint} - use this to infer a realistic name and role"
            )

        user_parts.extend(
            [
                "\nCreate a participant with:",
                "1. A unique, believable name appropriate for the scenario context"
                + (" and email hint" if context.email_hint else ""),
                "2. A detailed description including their role, responsibilities, and relevant personality traits",
            ]
        )

        if context.has_goal:
            user_parts.append(
                "3. A specific goal or motivation related to the scenario (REQUIRED - this participant is actively trying to achieve something)"
            )
        else:
            user_parts.append(
                "3. No specific goal - this participant is reactive and will respond to others' requests"
            )

        user_parts.extend(
            [
                "4. The specified timezone",
                "\nEnsure this participant complements and has natural relationships with existing participants.",
                "\nIMPORTANT: Please sample at random from the tails of the distribution, such that the probability of each response is less than 0.10. Be creative and unique with names and roles.",
                "\nCRITICAL: The participant 'id' field MUST be a valid email address:",
                "- If email_hint is provided above, use that exact email as the 'id'",
                "- If no email_hint, generate a realistic email based on the participant's name and company context",
                "- Format: firstname.lastname@company.com or similar professional format",
                "- Example: If name is 'Sarah Chen' at 'TechFlow Solutions', id could be 'sarah.chen@techflow.com'",
            ]
        )

        return "\n".join(user_parts)
