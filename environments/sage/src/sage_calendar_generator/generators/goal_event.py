"""Generator for goal events using LLM."""

from typing import Any

from ..context import GoalEventContext
from ..entities import GoalEvent
from .base import BaseLLMGenerator


class GoalEventGenerator(BaseLLMGenerator[GoalEvent]):
    """Generates the goal event with a specific scheduled time.

    This is the third phase of the generation pipeline, creating the central
    scheduling challenge. Conflict events will be generated to block this time.
    """

    def get_response_format(self) -> type[GoalEvent]:
        """Get the Pydantic model for structured output."""
        return GoalEvent

    def build_prompt(self, context: Any, **kwargs: Any) -> str:
        """Build the prompt for goal event generation.

        Args:
            context: GoalEventContext with generation parameters
            **kwargs: Unused

        Returns:
            Complete prompt string
        """
        if not isinstance(context, GoalEventContext):
            raise TypeError(f"Expected GoalEventContext, got {type(context)}")

        # Build the user message
        user_parts = [
            "Generate the goal event - the event that participants need to coordinate.",
            f"\nScenario context: {context.scenario_description}",
            f"\nOrganizer: {context.organizer.name} ({context.organizer.description})",
            f"Organizer timezone: {context.organizer.timezone}",
            "\nRequired attendees:",
        ]

        for attendee in context.required_attendees:
            user_parts.append(
                f"- {attendee.name} ({attendee.description}) - timezone: {attendee.timezone}"
            )

        user_parts.extend(
            [
                f"\nTarget duration: {context.duration_minutes} minutes",
                f"\nScheduling window: {context.seed_range.start.isoformat()} to {context.seed_range.end.isoformat()}",
                "\nCreate a goal event with a SPECIFIC SCHEDULED TIME:",
                "1. Has a SPECIFIC, DETAILED title (not generic like 'Planning Meeting')",
                "2. Fits naturally within the scenario context",
                "3. Requires all specified attendees",
                "4. Has a clear purpose and description",
                "5. Pick a specific scheduled_start and scheduled_end datetime within the scheduling window",
                "   - Choose a time during business hours (9am-6pm) in the organizer's timezone",
                "   - The duration should match the target duration",
                "   - Use timezone-aware datetimes",
                f"\nUse organizer ID: {context.organizer.id}",
                f"Use required attendee IDs: {[a.id for a in context.required_attendees]}",
                "\nIMPORTANT: Please sample at random from the tails of the distribution, such that the probability of each response is less than 0.10. Be creative and unique.",
            ]
        )

        return "\n".join(user_parts)
