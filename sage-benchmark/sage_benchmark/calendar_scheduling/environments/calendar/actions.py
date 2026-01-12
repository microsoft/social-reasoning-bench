from typing import Union, get_args

from pydantic import Field

from ...types import CalendarEvent, Tool


class AddEvent(Tool):
    """Add an event to the calendar."""

    event: CalendarEvent = Field(description="The event to add")


class CancelEvent(Tool):
    """Cancel an event by ID."""

    event_id: int = Field(description="ID of the event to cancel")


class ModifyEvent(Tool):
    """Modify an existing event."""

    event_id: int = Field(description="ID of the event to modify")
    title: str | None = Field(default=None, description="New event title")
    description: str | None = Field(default=None, description="New event description")
    start_time: float | None = Field(default=None, description="New start hour (0-24)")
    duration: float | None = Field(default=None, description="New duration in hours")
    participants: list[str] | None = Field(default=None, description="New participant list")


class GetEvent(Tool):
    """Get an event by ID."""

    event_id: int = Field(description="ID of the event to retrieve")


class ListEvents(Tool):
    """List all events on the calendar."""

    pass


CalendarAction = Union[AddEvent, CancelEvent, ModifyEvent, GetEvent, ListEvents]
CALENDAR_TOOLS: list[type[Tool]] = list(get_args(CalendarAction))
