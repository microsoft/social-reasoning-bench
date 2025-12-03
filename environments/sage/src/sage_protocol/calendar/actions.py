"""Calendar actions for magentic-marketplace integration."""

from magentic_marketplace.platform.shared.models import BaseAction
from pydantic import AwareDatetime, Field

from .entities import RecurrenceRule


class GetEvents(BaseAction):
    """Get all events in a date range for the requesting agent."""

    start_datetime: AwareDatetime = Field(
        description="Start datetime (inclusive). Must include timezone, e.g., '2024-01-15T00:00:00-08:00'"
    )
    end_datetime: AwareDatetime = Field(
        description="End datetime (exclusive). Must include timezone, e.g., '2024-01-22T00:00:00-08:00'"
    )


class GetEventDetails(BaseAction):
    """Get detailed information about a specific event."""

    event_id: str = Field(description="Event ID to retrieve")


class AddEvent(BaseAction):
    """Create a new event (standalone or recurring).

    For standalone events: provide start_datetime and end_datetime only.
    For recurring events: provide start_datetime, end_datetime, and recurrence.
    """

    title: str = Field(description="Event title")
    description: str = Field(description="Event description")
    start_datetime: AwareDatetime = Field(
        description="Event start time (timezone-aware). Must include timezone, e.g., '2024-01-15T14:30:00-08:00'"
    )
    end_datetime: AwareDatetime = Field(
        description="Event end time (timezone-aware). Must include timezone, e.g., '2024-01-15T16:30:00-08:00'"
    )
    recurrence: RecurrenceRule | None = Field(
        default=None,
        description="Recurrence pattern for recurring events. Omit for standalone events.",
    )
    participants: list[str] = Field(
        default_factory=list,
        description="List of participant IDs to invite (organizer will be added automatically)",
    )


class UpdateEvent(BaseAction):
    """Update an event (standalone, series parent, or series instance)."""

    event_id: str = Field(description="Event ID to update")
    title: str | None = Field(default=None, description="New title")
    description: str | None = Field(default=None, description="New description")
    start_datetime: AwareDatetime | None = Field(
        default=None,
        description="New start time (timezone-aware). Must include timezone, e.g., '2024-01-15T14:30:00-08:00'",
    )
    end_datetime: AwareDatetime | None = Field(
        default=None,
        description="New end time (timezone-aware). Must include timezone, e.g., '2024-01-15T16:30:00-08:00'",
    )
    recurrence: RecurrenceRule | None = Field(
        default=None,
        description="New recurrence pattern (for series parents only)",
    )
    participants: list[str] | None = Field(default=None, description="New participant list")


class DeleteEvent(BaseAction):
    """Delete an event (standalone, series parent, or series instance)."""

    event_id: str = Field(description="Event ID to delete")
