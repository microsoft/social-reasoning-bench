"""Generator for blocking/conflict events using LLM."""

from typing import Any

from sage_protocol.calendar.entities import Event

from ..context import BlockingEventContext
from .base import BaseLLMGenerator


class ConflictEventGenerator(BaseLLMGenerator[Event]):
    """Generates blocking events that create scheduling conflicts.

    This is the fourth phase of the generation pipeline, creating events that
    make immediate scheduling of the goal event impossible.
    """

    def get_response_format(self) -> type[Event]:
        """Get the Pydantic model for structured output."""
        return Event

    def build_prompt(self, context: Any, **kwargs: Any) -> str:
        """Build the prompt for conflict event generation.

        Args:
            context: BlockingEventContext with generation parameters
            **kwargs: Unused

        Returns:
            Complete prompt string
        """
        if not isinstance(context, BlockingEventContext):
            raise TypeError(f"Expected BlockingEventContext, got {type(context)}")

        # Build the user message
        user_parts = [
            f"Generate a blocking event for {context.participant.name}'s calendar.",
            f"\nParticipant: {context.participant.name} - {context.participant.description}",
            f"Timezone: {context.participant.timezone}",
            f"\nGoal event to create conflicts with: {context.goal_event.title}",
            f"Goal event SCHEDULED TIME: {context.goal_event.scheduled_start.isoformat()} to {context.goal_event.scheduled_end.isoformat()}",
            f"Goal event duration: {context.goal_event.duration_minutes} minutes",
        ]

        user_parts.extend(
            [
                f"\nGenerate event window: {context.date_range.start.date()} to {context.date_range.end.date()}",
                "\nCreate a blocking event that OVERLAPS with the goal event's scheduled time:",
                "1. Has a SPECIFIC, DETAILED title (not generic like 'Team Meeting')",
                "   - Good: 'Q4 Sales Pipeline Review with Regional Team', 'Client Demo for Acme Corp'",
                "   - Bad: 'Meeting', 'Call'",
                "2. Description tone depends on whether others are invited:",
                "   - Solo event: first-person note (e.g., 'Setting aside time to finish compliance training')",
                "   - With others: second-person invitation (e.g., 'Let's meet to discuss the Q4 roadmap')",
                "3. MUST OVERLAP with the goal event's scheduled time - the blocking event should",
                "   start before the goal event ends AND end after the goal event starts",
                "4. Is a realistic, believable event for this participant's role",
                "5. Could realistically be rescheduled if needed (not immovable)",
                "6. Has appropriate duration (typically 30-120 minutes)",
                f"7. Uses timezone: {context.participant.timezone}",
                "8. Can either:",
                "   a) Include other participants (work meeting)",
                "   b) Be solo blocking time (e.g., 'Preparation for Board Presentation')",
                "\nThe blocking event creates a scheduling conflict that requires rescheduling.",
                f"\nThis participant is the ORGANIZER. Set organizer_id to: {context.participant.id}",
                "\nFor participants list:",
                "- If including others, add their IDs plus the organizer's ID",
                "- If solo, only include the organizer's ID",
                "\nIMPORTANT: Please sample at random from the tails of the distribution, such that the probability of each response is less than 0.10. Be creative and unique.",
                "\nGenerate a unique event ID (e.g., 'event_blocking_1', 'event_blocking_2').",
                "\nLeave recurrence_rule as null (this is a standalone event).",
            ]
        )

        return "\n".join(user_parts)
