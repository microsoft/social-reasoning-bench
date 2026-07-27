"""Tests for the preference vocabulary and the slot search built on it.

A task's preference document is hand-translated into predicates using this
vocabulary. These tests pin the boundary behavior of each constructor and the
search that turns them into bookable start times.
"""

import pytest
from srbench.benchmarks.calendar_scheduling.evaluation.preference_adherence import (
    SoftPreference,
    ends_by,
    outside,
    starts_at_or_after,
    to_hhmm,
    to_minutes,
    within,
)
from srbench.benchmarks.calendar_scheduling.evaluation.preference_adherence.helpers import (
    _as_windows,
    _busy_intervals,
    _feasible_starts,
    _is_free,
    _weight_of,
)
from srbench.benchmarks.calendar_scheduling.types import LabeledMeeting

DURATION = 60


def _busy(start_time: str, end_time: str) -> LabeledMeeting:
    """Return a calendar entry occupying the given window."""
    return LabeledMeeting(
        uid=f"busy-{start_time}",
        title="Existing commitment",
        description="",
        organizer="someone@example.com",
        date="2024-06-15",
        start_time=start_time,
        end_time=end_time,
        attendees=[],
        is_movable=False,
        is_secret=False,
    )


def _windows(busy=None, constraints=None, duration=DURATION) -> list[str]:
    """Return the feasible start times as windows."""
    starts = _feasible_starts(duration, busy=busy or [], constraints=constraints or [])
    return _as_windows(starts)


class TestTimeHelpers:
    """Tests for the HH:MM conversions."""

    @pytest.mark.parametrize(
        ("hhmm", "minutes"), [("00:00", 0), ("08:00", 480), ("13:30", 810), ("23:59", 1439)]
    )
    def test_round_trip(self, hhmm, minutes):
        """Times convert to minutes and back without loss."""
        assert to_minutes(hhmm) == minutes
        assert to_hhmm(minutes) == hhmm


class TestPredicates:
    """Tests for the predicate constructors, including boundary behavior."""

    def test_within_accepts_contained_slots(self):
        """A slot inside the window passes, including an exact fit."""
        predicate = within("09:00", "12:00")

        assert predicate(to_minutes("09:00"), to_minutes("10:00"))
        assert predicate(to_minutes("09:00"), to_minutes("12:00"))

    def test_within_rejects_slots_crossing_either_edge(self):
        """A slot starting before or ending after the window fails."""
        predicate = within("09:00", "12:00")

        assert not predicate(to_minutes("08:30"), to_minutes("09:30"))
        assert not predicate(to_minutes("11:30"), to_minutes("12:30"))

    def test_outside_rejects_any_overlap(self):
        """Partial and total overlaps with the excluded window fail."""
        predicate = outside("12:00", "13:00")

        assert not predicate(to_minutes("12:00"), to_minutes("13:00"))
        assert not predicate(to_minutes("11:30"), to_minutes("12:30"))
        assert not predicate(to_minutes("12:30"), to_minutes("13:30"))

    def test_outside_accepts_touching_the_boundary(self):
        """Ending exactly when the window opens, or starting when it closes, is fine."""
        predicate = outside("12:00", "13:00")

        assert predicate(to_minutes("11:00"), to_minutes("12:00"))
        assert predicate(to_minutes("13:00"), to_minutes("14:00"))

    def test_ends_by_is_inclusive(self):
        """Ending exactly at the limit passes; ending later fails."""
        predicate = ends_by("17:00")

        assert predicate(to_minutes("16:00"), to_minutes("17:00"))
        assert not predicate(to_minutes("16:30"), to_minutes("17:30"))

    def test_starts_at_or_after_is_inclusive(self):
        """Starting exactly at the limit passes; starting earlier fails."""
        predicate = starts_at_or_after("13:00")

        assert predicate(to_minutes("13:00"), to_minutes("14:00"))
        assert not predicate(to_minutes("12:00"), to_minutes("13:00"))


class TestCalendarFreedom:
    """Tests for reading calendars as busy intervals."""

    def test_meetings_become_minute_intervals(self):
        """Each entry is converted to minutes from midnight."""
        assert _busy_intervals([_busy("09:00", "10:30")]) == [(540, 630)]

    def test_overlapping_slots_are_not_free(self):
        """Any intersection with a commitment makes a slot unavailable."""
        busy = _busy_intervals([_busy("09:00", "10:00")])

        assert not _is_free(to_minutes("09:30"), to_minutes("10:30"), busy)
        assert not _is_free(to_minutes("08:30"), to_minutes("09:30"), busy)

    def test_abutting_slots_are_free(self):
        """Ending exactly when a commitment starts, or starting when it ends, is free."""
        busy = _busy_intervals([_busy("09:00", "10:00")])

        assert _is_free(to_minutes("08:00"), to_minutes("09:00"), busy)
        assert _is_free(to_minutes("10:00"), to_minutes("11:00"), busy)


class TestWindows:
    """Tests for collapsing start times into readable ranges."""

    def test_consecutive_minutes_become_one_range(self):
        """A run of adjacent start times is reported as a single window."""
        assert _as_windows([540, 541, 542]) == ["09:00-09:02"]

    def test_gaps_split_the_ranges(self):
        """A missing minute starts a new window."""
        assert _as_windows([540, 541, 543]) == ["09:00-09:01", "09:03"]

    def test_a_lone_minute_is_reported_bare(self):
        """A single start time needs no range notation."""
        assert _as_windows([540]) == ["09:00"]

    def test_nothing_feasible_is_empty(self):
        """No start times means no windows."""
        assert _as_windows([]) == []


class TestFeasibleStarts:
    """Tests for the search over bookable start times."""

    def test_an_empty_day_is_one_window(self):
        """With nothing in the way, every minute leaving room for the meeting works."""
        assert _windows() == ["00:00-23:00"]

    def test_a_slot_must_end_within_the_day(self):
        """A longer meeting has to start earlier."""
        assert _windows(duration=90) == ["00:00-22:30"]

    def test_commitments_carve_out_windows(self):
        """Busy time removes the starts that would overlap it."""
        busy = _busy_intervals([_busy("10:00", "11:00"), _busy("14:00", "15:00")])

        assert _windows(busy=busy) == ["00:00-09:00", "11:00-13:00", "15:00-23:00"]

    def test_off_the_hour_commitments_are_respected_to_the_minute(self):
        """A commitment ending at 09:20 frees the slot starting exactly then."""
        busy = _busy_intervals([_busy("00:00", "09:20")])

        assert _windows(busy=busy) == ["09:20-23:00"]

    def test_constraints_narrow_the_windows(self):
        """Hard constraints remove starts the calendars would otherwise allow."""
        assert _windows(constraints=[starts_at_or_after("13:00")]) == ["13:00-23:00"]
        assert _windows(constraints=[ends_by("10:00")]) == ["00:00-09:00"]

    def test_contradictory_constraints_leave_nothing(self):
        """Constraints that cannot both hold yield no windows."""
        constraints = [ends_by("09:00"), starts_at_or_after("15:00")]

        assert _windows(constraints=constraints) == []

    def test_half_hour_starts_are_available_to_short_meetings(self):
        """A 30-minute meeting can start on any minute, not just the hour."""
        busy = _busy_intervals([_busy("00:00", "08:30")])

        assert _windows(busy=busy, duration=30) == ["08:30-23:30"]


class TestSlotWeights:
    """Tests for scoring a single slot against the soft preferences."""

    def test_satisfied_preferences_are_totaled_and_named(self):
        """The weight is the sum over the preferences the slot honors."""
        preferences = [
            SoftPreference("afternoon", starts_at_or_after("13:00"), weight=3.0),
            SoftPreference("before_five", ends_by("17:00")),
        ]

        weight, names = _weight_of(to_minutes("13:00"), to_minutes("14:00"), preferences)

        assert weight == 4.0
        assert names == ["afternoon", "before_five"]

    def test_a_slot_honoring_nothing_weighs_zero(self):
        """Missing every preference is reported as an empty list, not an error."""
        preferences = [SoftPreference("afternoon", starts_at_or_after("13:00"))]

        assert _weight_of(to_minutes("09:00"), to_minutes("10:00"), preferences) == (0, [])


class TestExactness:
    """The search must not step over a better slot."""

    def test_an_optimum_between_whole_hours_is_reachable(self):
        """A 09:30 start is available even though it is off the hour.

        An hourly grid would miss it, rate 09:00 the best available, and hide
        the strictly better slot that satisfies both preferences.
        """
        constraints = [starts_at_or_after("09:30"), ends_by("10:30")]

        assert _windows(constraints=constraints) == ["09:30"]


class TestSearchSpansTheWholeDay:
    """Only a hard constraint may narrow the bookable hours."""

    def test_a_late_night_constraint_is_satisfiable(self):
        """A preference for 22:00-23:00 yields that slot rather than no slot."""
        assert _windows(constraints=[within("22:00", "23:00")]) == ["22:00"]

    def test_the_last_slot_ends_at_midnight(self):
        """The day bound is exclusive, so a meeting may end exactly at midnight."""
        assert _windows()[-1].endswith("23:00")
