"""Generator for baseline calendar events and series using LLM."""

from typing import Any

from openai import AsyncOpenAI
from pydantic import AwareDatetime, BaseModel, Field
from sage_protocol.calendar.entities import Event, RecurrenceRule

from ..context import BaselineCalendarContext
from .base import BaseLLMGenerator


class RecurringEventResponse(BaseModel):
    """LLM response schema for recurring event generation."""

    id: str = Field(description="Unique event identifier")
    start_datetime: AwareDatetime = Field(description="Event start time (timezone-aware)")
    end_datetime: AwareDatetime = Field(description="Event end time (timezone-aware)")
    title: str = Field(description="Event title")
    description: str = Field(description="Event description")
    recurrence_rule: RecurrenceRule = Field(description="Recurrence pattern")
    organizer_id: str = Field(description="ID of the participant who organized/created this event")
    participants: list[str] = Field(
        description="List of participant IDs (attendees/invitees, including organizer)",
        default_factory=list,
    )


class _RecurringEventGenerator(BaseLLMGenerator[RecurringEventResponse]):
    """Internal generator for recurring events."""

    def get_response_format(self) -> type[RecurringEventResponse]:
        """Get the Pydantic model for structured output."""
        return RecurringEventResponse

    def build_prompt(self, context: Any, **kwargs: Any) -> str:
        """Build the prompt for recurring event generation."""
        if not isinstance(context, BaselineCalendarContext):
            raise TypeError(f"Expected BaselineCalendarContext, got {type(context)}")

        series_index = kwargs.get("series_index", 0)

        # Build the user message
        user_parts = [
            f"Generate recurring event {series_index + 1} of {context.target_series_count} for {context.participant.name}'s calendar.",
            f"\nParticipant: {context.participant.name} - {context.participant.description}",
            f"Timezone: {context.participant.timezone}",
            f"\nCalendar range: {context.date_range.start.date()} to {context.date_range.end.date()}",
            "\nCreate a recurring event that:",
            "1. Has a SPECIFIC, DETAILED title (not generic like 'Weekly Team Meeting')",
            "   - Good: 'Product Roadmap Review with Engineering Team'",
            "   - Bad: 'Weekly Meeting'",
            "2. Description tone depends on whether others are invited:",
            "   - Solo event: first-person note (e.g., 'Setting aside time for deep work on the API redesign')",
            "   - With others: second-person invitation (e.g., 'Let's sync on sprint progress and blockers')",
            "3. Fits the participant's role and responsibilities",
            "4. Can be either:",
            "   a) Work meetings WITH other participants (include their IDs in participants list)",
            "   b) Personal blocking time WITHOUT other participants (e.g., 'Deep Work Block', 'Focus Time')",
            "5. Has appropriate frequency and recurrence pattern",
            "6. Uses timezone-aware times",
            "7. Has a reasonable end condition (count or until_date within the range)",
            f"\nThis participant is the ORGANIZER and their ID is: {context.participant.id}",
            f"\nSet organizer_id to: {context.participant.id}",
            "\nFor participants list:",
            "- If this is a meeting WITH others, include their participant IDs plus the organizer's ID",
            "- If this is personal blocking time, only include the organizer's ID",
            "\nSeries types to vary:",
            "- Work meetings: 'Sprint Planning with Dev Team', 'Client Success Review', '1-on-1 with [Name]'",
            "- Personal blocks: 'Deep Work', 'Email & Admin Time', 'Lunch Break'",
            "- Professional development: 'Learning Hour', 'Code Review Time'",
            "\nAdvanced recurrence patterns (optional):",
            "- First Monday of month: frequency=MONTHLY, by_day=[MONDAY], by_set_pos=[1]",
            "- Last Friday of month: frequency=MONTHLY, by_day=[FRIDAY], by_set_pos=[-1]",
            "- 1st and 15th of month: frequency=MONTHLY, by_month_day=[1, 15]",
            "- 2nd and 4th Tuesday: frequency=MONTHLY, by_day=[TUESDAY], by_set_pos=[2, 4]",
            "\nIMPORTANT: Please sample at random from the tails of the distribution, such that the probability of each response is less than 0.10. Be creative and unique.",
            "\nEnsure times include proper timezone information.",
            f"\nGenerate unique event ID: event_recurring_{context.participant.id}_{series_index}",
            "\nStart the event within the date range.",
        ]

        if context.existing_events:
            user_parts.append(
                f"\nNote: Avoid conflicts with {len(context.existing_events)} existing events on this calendar."
            )

        return "\n".join(user_parts)


class _StandaloneEventGenerator(BaseLLMGenerator[Event]):
    """Internal generator for standalone events."""

    def get_response_format(self) -> type[Event]:
        """Get the Pydantic model for structured output."""
        return Event

    def build_prompt(self, context: Any, **kwargs: Any) -> str:
        """Build the prompt for event generation."""
        if not isinstance(context, BaselineCalendarContext):
            raise TypeError(f"Expected BaselineCalendarContext, got {type(context)}")

        event_index = kwargs.get("event_index", 0)

        # Build the user message
        user_parts = [
            f"Generate standalone event {event_index + 1} for {context.participant.name}'s calendar.",
            f"\nParticipant: {context.participant.name} - {context.participant.description}",
            f"Timezone: {context.participant.timezone}",
            f"\nCalendar range: {context.date_range.start.date()} to {context.date_range.end.date()}",
            "\nCreate a standalone (non-recurring) event that:",
            "1. Has a SPECIFIC, DETAILED title appropriate to the event type",
            "2. Description tone depends on whether others are invited:",
            "   - Solo event: first-person note (e.g., 'Blocking time for annual compliance training')",
            "   - With others: second-person invitation (e.g., 'Let's review the budget proposal together')",
            "3. Fits naturally into the participant's calendar",
            "4. Should be one of:",
            "   a) Work meeting (60%): Include other participants",
            "   b) Personal life event (20%): Doctor, Dentist, Gym, Parent-Teacher Conference, etc.",
            "   c) Professional event (20%): Conference attendance, training, networking",
            "5. Has appropriate duration and specific date/times",
            "6. Uses timezone-aware datetimes",
            f"\nThis participant is the ORGANIZER. Set organizer_id to: {context.participant.id}",
            "\nFor participants list:",
            "- Work meetings: Include participant IDs of attendees plus organizer",
            "- Personal/solo events: Only include organizer's ID",
            "\nEvent title examples:",
            "- Work: 'Budget Review for Q4 Initiative', 'Demo Preparation Session'",
            "- Personal: 'Annual Physical Exam', 'Dentist Appointment', 'Kid's Soccer Practice'",
            "- Professional: 'AWS Summit Keynote', 'Leadership Workshop'",
            "\nIMPORTANT: Please sample at random from the tails of the distribution, such that the probability of each response is less than 0.10. Be creative and unique.",
            f"\nGenerate unique event ID: event_standalone_{context.participant.id}_{event_index}",
            "\nLeave recurrence_rule as null (standalone event).",
            "\nUse a specific date within the range.",
        ]

        if context.existing_events:
            user_parts.append(
                f"\nNote: Avoid conflicts with {len(context.existing_events)} existing events."
            )

        return "\n".join(user_parts)


class BaselineCalendarGenerator:
    """Generates baseline calendar content (recurring and standalone events).

    This is the fifth phase of the generation pipeline, populating calendars
    with realistic recurring events and standalone events to create a believable
    baseline schedule.
    """

    def __init__(self, client: AsyncOpenAI, model: str = "gpt-4-turbo-preview"):
        """
        Initialize the baseline calendar generator.

        Args:
            client: OpenAI async client
            model: Model to use for generation
        """
        self._recurring_generator = _RecurringEventGenerator(client, model)
        self._standalone_generator = _StandaloneEventGenerator(client, model)

    async def generate_recurring_event(
        self,
        context: BaselineCalendarContext,
        messages: list[dict[str, Any]],
        series_index: int,
    ) -> Event:
        """
        Generate a single recurring event.

        Args:
            context: Baseline calendar generation context
            messages: Shared LLM conversation history (will be appended to)
            series_index: Index of this recurring event (for unique IDs)

        Returns:
            Generated recurring Event with recurrence_rule set
        """
        # Delegate to internal generator
        response = await self._recurring_generator.generate(
            context,
            messages,
            series_index=series_index,
        )

        # Convert to Event (adding instance_modifications as None)
        event = Event(
            id=response.id,
            recurrence_rule=response.recurrence_rule,
            start_datetime=response.start_datetime,
            end_datetime=response.end_datetime,
            title=response.title,
            description=response.description,
            organizer_id=response.organizer_id,
            participants=response.participants,
            instance_modifications=None,
        )

        return event

    async def generate_standalone_event(
        self,
        context: BaselineCalendarContext,
        messages: list[dict[str, Any]],
        event_index: int,
    ) -> Event:
        """
        Generate a single standalone event to fill calendar gaps.

        Args:
            context: Baseline calendar generation context
            messages: Shared LLM conversation history (will be appended to)
            event_index: Index of this event (for unique IDs)

        Returns:
            Generated standalone event
        """
        # Delegate to internal generator
        return await self._standalone_generator.generate(
            context,
            messages,
            event_index=event_index,
        )
