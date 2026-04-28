"""Tests for trim_calendar_events and trim_requestor_calendar in assemble.py."""

import random

import pytest
from sage_benchmark.benchmarks.calendar_scheduling.types import LabeledMeeting
from sage_data_gen.calendar_scheduling.assemble import (
    NUM_WORKING_SLOTS,
    _get_free_slot_indices,
    trim_calendar_events,
    trim_requestor_calendar,
)

# ── Helpers ──────────────────────────────────────────────────────────


def _make_meeting(slot_index: int) -> LabeledMeeting:
    """Create a working-hour LabeledMeeting at the given slot index (0=08:00, 10=18:00)."""
    hour = 8 + slot_index
    return LabeledMeeting(
        uid=f"meeting-{slot_index}",
        title=f"Meeting at {hour}",
        description="",
        organizer="test@test.com",
        date="2026-02-20",
        start_time=f"{hour:02d}:00",
        end_time=f"{hour + 1:02d}:00",
        attendees=[],
        is_movable=False,
        is_secret=False,
    )


def _make_sleep() -> LabeledMeeting:
    """Create the synthetic sleep block (00:00-08:00)."""
    return LabeledMeeting(
        uid="emp-sleep",
        title="Sleep",
        description="Overnight rest",
        organizer="test@test.com",
        date="2026-02-20",
        start_time="00:00",
        end_time="08:00",
        attendees=[],
        is_movable=False,
        is_secret=False,
    )


def _make_personal() -> LabeledMeeting:
    """Create the synthetic personal-time block (19:00-23:59)."""
    return LabeledMeeting(
        uid="emp-personal",
        title="Personal time",
        description="Evening personal time",
        organizer="test@test.com",
        date="2026-02-20",
        start_time="19:00",
        end_time="23:59",
        attendees=[],
        is_movable=False,
        is_secret=False,
    )


def _full_calendar() -> list[LabeledMeeting]:
    """All 11 working slots occupied, plus sleep and personal blocks."""
    return [_make_sleep()] + [_make_meeting(i) for i in range(NUM_WORKING_SLOTS)] + [_make_personal()]


def _partial_calendar(n_busy: int) -> list[LabeledMeeting]:
    """Calendar with n_busy occupied working slots (0 through n_busy-1), plus sleep and personal."""
    return [_make_sleep()] + [_make_meeting(i) for i in range(n_busy)] + [_make_personal()]


# ── trim_calendar_events ─────────────────────────────────────────────


class TestTrimCalendarEvents:
    """Core behavior: target_free_slots is an absolute target, protected slot is preserved."""

    def test_hits_target_free_slots(self):
        """Achieves the exact target free-slot count on a fully-occupied calendar."""
        cal = _full_calendar()
        for target in [1, 5, 10]:
            result = trim_calendar_events(cal[:], target, -1, random.Random(42))
            assert len(_get_free_slot_indices(result)) == target

    def test_partial_calendar_reaches_target(self):
        """Starting with 3 free slots, target=5 removes only the 2-slot deficit."""
        cal = _partial_calendar(8)
        result = trim_calendar_events(cal, 5, -1, random.Random(42))
        assert len(_get_free_slot_indices(result)) == 5

    def test_no_removal_when_at_or_above_target(self):
        """No events removed when the calendar already meets or exceeds the target."""
        for n_busy, target in [(6, 5), (3, 5)]:
            cal = _partial_calendar(n_busy)
            result = trim_calendar_events(cal, target, -1, random.Random(42))
            assert len(result) == len(cal)

    def test_protected_slot_never_removed(self):
        """The protected slot survives trimming across 20 different seeds."""
        cal = _full_calendar()
        protected = 5
        for seed in range(20):
            result = trim_calendar_events(cal[:], 10, protected, random.Random(seed))
            assert any(e.uid == f"meeting-{protected}" for e in result)


# ── trim_requestor_calendar ──────────────────────────────────────────


class TestTrimRequestorCalendar:
    """Core behavior: requestor_fullness is the absolute target, min_mutual_free_slots is guaranteed."""

    def test_hits_target_fullness(self):
        """Achieves exact target free-slot count across a range of values."""
        for target in [1, 3, 5, 7, 10]:
            cal = _full_calendar()
            result = trim_requestor_calendar(
                cal, target, set(range(NUM_WORKING_SLOTS)), random.Random(42),
                min_mutual_free_slots=0,
            )
            assert len(_get_free_slot_indices(result)) == target

    def test_target_with_deficit(self):
        """Deficit removal + fullness trimming together hit the exact target."""
        cal = _full_calendar()
        result = trim_requestor_calendar(
            cal, 5, {1, 3, 5, 7, 9}, random.Random(42), min_mutual_free_slots=3,
        )
        free = _get_free_slot_indices(result)
        assert len(free) == 5
        assert len(free & {1, 3, 5, 7, 9}) >= 3

    def test_target_with_partial_calendar(self):
        """Starting with existing free slots, target is still reached exactly."""
        cal = _partial_calendar(8)  # 3 already free (slots 8, 9, 10)
        result = trim_requestor_calendar(
            cal, 5, {8, 9, 10}, random.Random(42), min_mutual_free_slots=2,
        )
        free = _get_free_slot_indices(result)
        assert len(free) == 5
        assert len(free & {8, 9, 10}) >= 2

    def test_mutual_free_guarantee(self):
        """At least min_mutual_free_slots overlap, verified across 50 seeds."""
        for seed in range(50):
            cal = _full_calendar()
            result = trim_requestor_calendar(
                cal, 3, {1, 4, 7, 9}, random.Random(seed), min_mutual_free_slots=2,
            )
            mutual = _get_free_slot_indices(result) & {1, 4, 7, 9}
            assert len(mutual) >= 2, f"seed={seed}: only {len(mutual)} mutual free"

    def test_raises_when_mutual_free_impossible(self):
        """Raises RuntimeError when there aren't enough overlap candidates."""
        cal = _full_calendar()
        with pytest.raises(RuntimeError, match="Cannot guarantee min_mutual_free_slots"):
            trim_requestor_calendar(cal, 3, {5}, random.Random(42), min_mutual_free_slots=3)
        with pytest.raises(RuntimeError, match="Cannot guarantee min_mutual_free_slots"):
            trim_requestor_calendar(cal, 3, set(), random.Random(42), min_mutual_free_slots=1)
