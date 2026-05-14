"""Tests for AgentCalendar (environment.calendar)."""

from srbench.benchmarks.calendar_scheduling.environment.calendar import AgentCalendar
from srbench.benchmarks.calendar_scheduling.types import (
    Attendee,
    AttendeeStatus,
    Meeting,
)

OWNER = "owner@example.com"
OTHER = "other@example.com"


def _meeting(
    uid: str,
    start: str,
    end: str,
    *,
    owner_status: AttendeeStatus | None = AttendeeStatus.ACCEPTED,
    date: str = "2026-02-20",
) -> Meeting:
    attendees: list[Attendee] = []
    if owner_status is not None:
        attendees.append(Attendee(email=OWNER, status=owner_status))
    return Meeting(
        uid=uid,
        title=uid,
        description="",
        organizer=OTHER,
        date=date,
        start_time=start,
        end_time=end,
        attendees=attendees,
    )


class TestHasConflicts:
    """Tests for AgentCalendar.has_conflicts."""

    def test_accepted_overlap_is_conflict(self):
        cal = AgentCalendar(
            owner=OWNER,
            meetings=[
                _meeting("a", "10:00", "11:00"),
                _meeting("b", "10:30", "11:30"),
            ],
        )
        assert cal.has_conflicts() is True

    def test_pending_overlap_with_accepted_is_not_conflict(self):
        """Pending invites are inbox items, not calendar blocks."""
        cal = AgentCalendar(
            owner=OWNER,
            meetings=[
                _meeting("accepted", "17:00", "18:00"),
                _meeting(
                    "pending", "17:00", "18:00", owner_status=AttendeeStatus.AWAITING_RESPONSE
                ),
            ],
        )
        assert cal.has_conflicts() is False

    def test_declined_overlap_is_not_conflict(self):
        cal = AgentCalendar(
            owner=OWNER,
            meetings=[
                _meeting("accepted", "10:00", "11:00"),
                _meeting("declined", "10:30", "11:30", owner_status=AttendeeStatus.DECLINED),
            ],
        )
        assert cal.has_conflicts() is False

    def test_two_pending_overlap_is_not_conflict(self):
        cal = AgentCalendar(
            owner=OWNER,
            meetings=[
                _meeting("p1", "10:00", "11:00", owner_status=AttendeeStatus.AWAITING_RESPONSE),
                _meeting("p2", "10:30", "11:30", owner_status=AttendeeStatus.AWAITING_RESPONSE),
            ],
        )
        assert cal.has_conflicts() is False

    def test_owner_missing_from_attendees_treated_as_accepted(self):
        cal = AgentCalendar(
            owner=OWNER,
            meetings=[
                _meeting("a", "10:00", "11:00", owner_status=None),
                _meeting("b", "10:30", "11:30", owner_status=None),
            ],
        )
        assert cal.has_conflicts() is True

    def test_no_overlap_no_conflict(self):
        cal = AgentCalendar(
            owner=OWNER,
            meetings=[
                _meeting("a", "10:00", "11:00"),
                _meeting("b", "11:00", "12:00"),
            ],
        )
        assert cal.has_conflicts() is False

    def test_different_dates_no_conflict(self):
        cal = AgentCalendar(
            owner=OWNER,
            meetings=[
                _meeting("a", "10:00", "11:00", date="2026-02-20"),
                _meeting("b", "10:00", "11:00", date="2026-02-21"),
            ],
        )
        assert cal.has_conflicts() is False

    def test_empty_calendar_no_conflict(self):
        cal = AgentCalendar(owner=OWNER, meetings=[])
        assert cal.has_conflicts() is False
