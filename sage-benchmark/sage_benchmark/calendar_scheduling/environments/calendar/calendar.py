from typing import Sequence, overload

from pydantic import Field

from ...types import CalendarEvent
from .actions import (
    AddEvent,
    CalendarAction,
    CancelEvent,
    GetEvent,
    ListEvents,
    ModifyEvent,
)

CALENDAR_EVENT_PUBLIC_FIELDS = set(CalendarEvent.model_fields.keys())


class IdentifiedCalendarEvent(CalendarEvent):
    id: int = Field(description="Unique event identifier")


class Calendar:
    def __init__(
        self,
        events: Sequence[CalendarEvent] | None = None,
    ):
        self._events: dict[int, CalendarEvent] = {}
        self._next_id: int = 0

        if events:
            for event in events:
                self._add_event(event)

    @overload
    def execute(self, action: AddEvent) -> int: ...
    @overload
    def execute(self, action: CancelEvent) -> CalendarEvent: ...
    @overload
    def execute(self, action: ModifyEvent) -> CalendarEvent: ...
    @overload
    def execute(self, action: GetEvent) -> CalendarEvent: ...
    @overload
    def execute(self, action: ListEvents) -> list[CalendarEvent]: ...

    def execute(self, action: CalendarAction) -> int | CalendarEvent | list[CalendarEvent]:
        """Execute a calendar action.

        Args:
            action: The action to execute.

        Returns:
            Result depends on action type:
            - AddEvent: int (assigned event ID)
            - CancelEvent: CalendarEvent (the cancelled event)
            - ModifyEvent: CalendarEvent (the updated event)
            - GetEvent: CalendarEvent
            - ListEvents: list[CalendarEvent]
        """
        match action:
            case AddEvent():
                return self._add_event(action.event)
            case CancelEvent():
                return self._cancel_event(action.event_id)
            case ModifyEvent():
                return self._modify_event(
                    action.event_id,
                    action.title,
                    action.description,
                    action.start_time,
                    action.duration,
                    action.participants,
                )
            case GetEvent():
                return self._get_event(action.event_id)
            case ListEvents():
                return self._list_events()

    def _add_event(self, event: CalendarEvent) -> int:
        if event.start_time < 0:
            raise ValueError("Event starts before day begins (0)")
        if event.start_time + event.duration > 24:
            raise ValueError("Event ends after day ends (24)")

        event_id = self._next_id
        # Dump and validate to remove any subclass fields
        self._events[event_id] = CalendarEvent.model_validate(
            event.model_dump(include=CALENDAR_EVENT_PUBLIC_FIELDS)
        )
        self._next_id += 1
        return event_id

    def _cancel_event(self, event_id: int) -> CalendarEvent:
        return self._events.pop(event_id)

    def _modify_event(
        self,
        event_id: int,
        title: str | None,
        description: str | None,
        start_time: int | None,
        duration: int | None,
        participants: list[str] | None,
    ) -> CalendarEvent:
        event = self._events[event_id]
        updates = {
            k: v
            for k, v in {
                "title": title,
                "description": description,
                "start_time": start_time,
                "duration": duration,
                "participants": participants,
            }.items()
            if v is not None
        }
        updated = event.model_copy(update=updates)

        if updated.start_time < 0:
            raise ValueError("Event starts before day begins (0)")
        if updated.start_time + updated.duration > 24:
            raise ValueError("Event ends after day ends (24)")

        self._events[event_id] = updated
        return updated

    def _get_event(self, event_id: int) -> CalendarEvent:
        return self._events[event_id]

    def _list_events(self) -> list[CalendarEvent]:
        return sorted(self._events.values(), key=lambda event: event.start_time)

    def has_conflicts(self) -> bool:
        """Return True if any events on the calendar overlap with each other."""
        events = list(self._events.values())
        for i, event_a in enumerate(events):
            end_a = event_a.start_time + event_a.duration
            for event_b in events[i + 1 :]:
                end_b = event_b.start_time + event_b.duration
                if event_a.start_time < end_b and event_b.start_time < end_a:
                    return True
        return False
