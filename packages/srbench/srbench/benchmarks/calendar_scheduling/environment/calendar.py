"""Calendar system for iTIP-style interactions with cross-calendar synchronization."""

from typing import Callable, Optional

from ..types import AttendeeStatus, Meeting
from .utils import time_to_minutes


class AgentCalendar:
    """Calendar for a single agent.

    Receives a callback for looking up other agents' calendars, injected by CalendarManager.
    """

    def __init__(
        self,
        owner: str,
        meetings: list[Meeting] | None = None,
        get_calendar_callback: Optional[Callable[[str], Optional["AgentCalendar"]]] = None,
    ) -> None:
        self._owner = owner
        self._meetings: dict[str, Meeting] = {}
        self._get_calendar = get_calendar_callback

        if meetings:
            for meeting in meetings:
                self._meetings[meeting.uid] = meeting

        self._initial_meetings: dict[str, Meeting] = {
            uid: meeting.model_copy(deep=True) for uid, meeting in self._meetings.items()
        }

    @property
    def owner(self) -> str:
        """Return the email address of the calendar owner.

        Returns:
            The email address string of the calendar owner.
        """
        return self._owner

    def get_other_calendar(self, email: str) -> Optional["AgentCalendar"]:
        """Get another agent's calendar (if callback is set).

        Args:
            email: Email address of the agent whose calendar to retrieve.

        Returns:
            The agent's calendar if found, or None if no callback is set
            or agent not found.
        """
        if self._get_calendar:
            return self._get_calendar(email)
        return None

    def add_meeting(self, meeting: Meeting) -> None:
        """Add a meeting to this calendar.

        Args:
            meeting: The meeting to add to the calendar.
        """
        self._meetings[meeting.uid] = meeting

    def remove_meeting(self, uid: str) -> Meeting | None:
        """Remove a meeting from this calendar by UID.

        Args:
            uid: Unique identifier of the meeting to remove.

        Returns:
            The removed meeting, or None if no meeting with the given UID exists.
        """
        return self._meetings.pop(uid, None)

    def get_meeting(self, uid: str) -> Meeting | None:
        """Get a meeting by UID.

        Args:
            uid: Unique identifier of the meeting to retrieve.

        Returns:
            The meeting if found, or None if no meeting with the given UID exists.
        """
        return self._meetings.get(uid)

    def list_meetings(self) -> list[Meeting]:
        """List all meetings sorted by date and time.

        Returns:
            List of meetings sorted by date, start time, and end time.
        """
        return sorted(
            self._meetings.values(),
            key=lambda m: (m.date, m.start_time, m.end_time),
        )

    def update_attendee_status(
        self,
        uid: str,
        attendee_email: str,
        status: AttendeeStatus,
    ) -> bool:
        """Update an attendee's status on a meeting.

        Args:
            uid: Unique identifier of the meeting.
            attendee_email: Email address of the attendee to update.
            status: The new status to set for the attendee.

        Returns:
            True if the update was successful, False if meeting or attendee
            not found.
        """
        meeting = self._meetings.get(uid)
        if meeting:
            for attendee in meeting.attendees:
                if attendee.email == attendee_email:
                    from ..types import Attendee as AttendeeModel

                    idx = meeting.attendees.index(attendee)
                    meeting.attendees[idx] = AttendeeModel(
                        email=attendee.email,
                        status=status,
                    )
                    return True
        return False

    def has_conflicts(self) -> bool:
        """Check if any meetings on the calendar overlap.

        Only checks meetings on the same date.

        Returns:
            True if any meetings overlap on the same date, False otherwise.
        """
        meetings = list(self._meetings.values())

        # Group meetings by date
        by_date: dict[str, list[Meeting]] = {}
        for meeting in meetings:
            if meeting.date not in by_date:
                by_date[meeting.date] = []
            by_date[meeting.date].append(meeting)

        # Check for conflicts within each date
        for date_meetings in by_date.values():
            for i, meeting_a in enumerate(date_meetings):
                start_a = time_to_minutes(meeting_a.start_time)
                end_a = time_to_minutes(meeting_a.end_time)

                for meeting_b in date_meetings[i + 1 :]:
                    start_b = time_to_minutes(meeting_b.start_time)
                    end_b = time_to_minutes(meeting_b.end_time)

                    if start_a < end_b and start_b < end_a:
                        return True

        return False

    def is_initial_meeting(self, uid: str) -> bool:
        """
        Determine if the meeting uid was on the initial calendar
        """
        return uid in self._initial_meetings


class CalendarManager:
    """Manages calendar creation and cross-calendar lookups."""

    def __init__(self) -> None:
        self._calendars: dict[str, AgentCalendar] = {}

    def create_calendar(
        self,
        owner: str,
        initial_meetings: list[Meeting] | None = None,
    ) -> AgentCalendar:
        """Factory: creates AgentCalendar with lookup callback wired to this manager.

        Args:
            owner: Email address of the calendar owner.
            initial_meetings: Optional list of meetings to pre-populate the calendar.

        Returns:
            A new AgentCalendar instance with cross-calendar lookup configured.
        """

        def get_calendar(email: str) -> AgentCalendar | None:
            return self._calendars.get(email)

        calendar = AgentCalendar(
            owner=owner,
            meetings=initial_meetings,
            get_calendar_callback=get_calendar,
        )
        self._calendars[owner] = calendar
        return calendar
