"""Utility for expanding recurring events into individual event instances."""

from datetime import date

from ..entities import Event, TimeRange
from .dates import combine_date_and_time, expand_recurrence


class SeriesExpander:
    """Handles expansion of recurring events into individual event instances.

    Centralizes the logic for:
    - Expanding recurrence patterns into concrete dates
    - Checking for cancellations
    - Applying instance-level modifications
    - Creating event instances with proper IDs
    """

    @staticmethod
    def expand_event_to_instances(
        parent_event: Event,
        date_range: TimeRange,
        include_cancelled: bool = False,
        skip_first_occurrence: bool = False,
    ) -> list[Event]:
        """Expand a recurring event into concrete instances within a date range.

        Args:
            parent_event: The parent event with recurrence_rule
            date_range: Date range to expand into
            include_cancelled: Whether to include cancelled instances
            skip_first_occurrence: Whether to skip the first occurrence (parent is concrete)

        Returns:
            List of event instances sorted by start time
        """
        if not parent_event.is_recurring:
            raise ValueError("Cannot expand non-recurring event")

        # Type assertion: is_recurring guarantees recurrence_rule is not None
        assert parent_event.recurrence_rule is not None

        events: list[Event] = []

        # Get all occurrence dates in range
        first_occurrence = parent_event.start_datetime.date()
        occurrence_dates = expand_recurrence(
            first_occurrence,
            parent_event.recurrence_rule,
            date_range,
        )

        for d in occurrence_dates:
            # Skip first occurrence if parent is concrete
            if skip_first_occurrence and d == first_occurrence:
                continue

            # Check if cancelled
            if not include_cancelled and parent_event.is_cancelled(d):
                continue

            # Create event instance for this date
            event = SeriesExpander.expand_event_for_date(parent_event, d)
            events.append(event)

        # Sort by start time
        events.sort(key=lambda e: e.start_datetime)

        return events

    @staticmethod
    def expand_event_for_date(parent_event: Event, occurrence_date: date) -> Event:
        """Create a single event instance for a specific occurrence.

        Applies any instance-level modifications if they exist.

        Args:
            parent_event: The parent event with recurrence_rule
            occurrence_date: The specific date to create an instance for

        Returns:
            Event instance for this occurrence
        """
        if not parent_event.is_recurring:
            raise ValueError("Cannot expand non-recurring event")

        # Get modification if exists
        mod = parent_event.get_modification(occurrence_date)

        # Extract time and duration from parent event
        start_time = parent_event.start_datetime.time()
        duration = parent_event.end_datetime - parent_event.start_datetime

        # Determine event properties (use modification overrides if present)
        if mod:
            start_dt = mod.new_start or combine_date_and_time(occurrence_date, start_time)
            end_dt = mod.new_end or (start_dt + duration)
            title = mod.title_override or parent_event.title
            description = mod.description_override or parent_event.description
            participants = mod.participants_override or parent_event.participants
        else:
            start_dt = combine_date_and_time(occurrence_date, start_time)
            end_dt = start_dt + duration
            title = parent_event.title
            description = parent_event.description
            participants = parent_event.participants

        # Create event instance (ID encodes parent relationship)
        event = Event(
            id=f"{parent_event.id}_{occurrence_date.isoformat()}",
            recurrence_rule=None,
            start_datetime=start_dt,
            end_datetime=end_dt,
            title=title,
            description=description,
            organizer_id=parent_event.organizer_id,
            participants=participants,
        )

        return event
