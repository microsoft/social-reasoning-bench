"""Tests for duty of care scoring functions."""

import pytest
from sage_benchmark.calendar_scheduling.environment.calendar import AgentCalendar
from sage_benchmark.calendar_scheduling.evaluation.duty_of_care import (
    compute_preference_score,
)
from sage_benchmark.calendar_scheduling.evaluation.duty_of_care.duty_of_care import (
    find_best_available_slot,
)
from sage_benchmark.calendar_scheduling.evaluation.duty_of_care.evaluate import (
    evaluate_duty_of_care,
)
from sage_benchmark.calendar_scheduling.types import Meeting, TimeSlotPreference


def make_meeting(
    start_time: str,
    end_time: str,
    date: str = "2024-01-15",
    uid: str = "test-meeting",
    title: str = "Test Meeting",
) -> Meeting:
    """Helper to create a Meeting with minimal required fields."""
    return Meeting(
        uid=uid,
        title=title,
        description="Test meeting",
        organizer="test@example.com",
        date=date,
        start_time=start_time,
        end_time=end_time,
    )


def _make_calendar(meetings: list[Meeting]) -> AgentCalendar:
    return AgentCalendar(owner="user@example.com", meetings=meetings)


PREFS = [
    TimeSlotPreference(start_time="09:00", end_time="12:00", score=1.0),
]

# Calendar with 09:00-12:00 fully blocked by existing meetings (not the scheduled one)
FULL_CALENDAR_MEETINGS = [
    make_meeting("09:00", "10:00", uid="existing-1", title="Existing 1"),
    make_meeting("10:00", "11:00", uid="existing-2", title="Existing 2"),
    make_meeting("11:00", "12:00", uid="existing-3", title="Existing 3"),
]


class TestComputePreferenceScore:
    """Tests for compute_preference_score function."""

    def test_meeting_fully_within_preference_window(self):
        """Meeting fully within high preference window."""
        meeting = make_meeting("10:00", "11:00")
        preferences = [
            TimeSlotPreference(start_time="09:00", end_time="12:00", score=0.9),
        ]

        score = compute_preference_score(meeting, preferences)

        assert score is not None
        assert score == 0.9

    def test_meeting_spanning_multiple_preferences(self):
        """Meeting spanning two preference windows with different scores."""
        meeting = make_meeting("11:00", "13:00")  # 120 min total
        preferences = [
            TimeSlotPreference(start_time="09:00", end_time="12:00", score=1.0),  # 60 min overlap
            TimeSlotPreference(start_time="12:00", end_time="15:00", score=0.5),  # 60 min overlap
        ]

        score = compute_preference_score(meeting, preferences)

        # 60 min at 1.0 + 60 min at 0.5 = 90 total score / 120 min duration = 0.75
        assert score is not None
        assert score == 0.75

    def test_meeting_outside_all_preferences(self):
        """Meeting entirely outside all preference windows should return 0."""
        meeting = make_meeting("20:00", "21:00")
        preferences = [
            TimeSlotPreference(start_time="09:00", end_time="12:00", score=0.9),
            TimeSlotPreference(start_time="14:00", end_time="17:00", score=0.7),
        ]

        score = compute_preference_score(meeting, preferences)

        assert score == 0.0

    def test_no_preferences(self):
        """No preferences defined should return None."""
        meeting = make_meeting("10:00", "11:00")

        score = compute_preference_score(meeting, [])

        assert score is None

    def test_partial_overlap_with_preference(self):
        """Meeting partially overlapping preference window."""
        meeting = make_meeting("11:00", "13:00")  # 120 min
        preferences = [
            TimeSlotPreference(start_time="09:00", end_time="12:00", score=0.8),  # 60 min overlap
        ]

        score = compute_preference_score(meeting, preferences)

        # 60 min covered at 0.8 = 48 / 120 min = 0.4
        assert score is not None
        assert score == pytest.approx(0.4)


class TestFindBestAvailableSlot:
    """Tests for _find_best_available_slot."""

    def test_empty_calendar_returns_best_pref(self):
        """Empty calendar → first slot in highest-scored preference window."""
        meeting = make_meeting("14:00", "15:00")  # 60 min duration
        preferences = [
            TimeSlotPreference(start_time="09:00", end_time="12:00", score=1.0),
            TimeSlotPreference(start_time="14:00", end_time="17:00", score=0.5),
        ]
        calendar = _make_calendar([meeting])

        result = find_best_available_slot(meeting, preferences, calendar, "2024-01-15")

        assert result is not None
        assert result == ("09:00-10:00", 1.0)

    def test_best_window_blocked_falls_back(self):
        """Best preference window full → returns slot in next-best window."""
        meeting = make_meeting("18:00", "19:00")  # scheduled outside prefs
        preferences = [
            TimeSlotPreference(start_time="09:00", end_time="12:00", score=1.0),
            TimeSlotPreference(start_time="14:00", end_time="17:00", score=0.5),
        ]
        blockers = [
            make_meeting("09:00", "12:00", uid="blocker-1"),
        ]
        calendar = _make_calendar([meeting, *blockers])

        result = find_best_available_slot(meeting, preferences, calendar, "2024-01-15")

        assert result is not None
        assert result[1] == 0.5
        assert result[0] == "14:00-15:00"

    def test_all_slots_blocked_returns_none(self):
        """All preference windows fully booked → None."""
        meeting = make_meeting("18:00", "19:00")
        calendar = _make_calendar([meeting, *FULL_CALENDAR_MEETINGS])

        result = find_best_available_slot(meeting, PREFS, calendar, "2024-01-15")

        assert result is None

    def test_excludes_scheduled_meeting_from_conflicts(self):
        """The scheduled meeting itself should not block its own slot."""
        meeting = make_meeting("09:00", "10:00")
        calendar = _make_calendar([meeting])

        result = find_best_available_slot(meeting, PREFS, calendar, "2024-01-15")

        assert result is not None
        assert result == ("09:00-10:00", 1.0)

    def test_partial_block_finds_gap(self):
        """Partial block in preference window → finds the remaining gap."""
        meeting = make_meeting("14:00", "15:00")  # 60 min
        preferences = [
            TimeSlotPreference(start_time="09:00", end_time="12:00", score=1.0),
        ]
        blocker = make_meeting("09:00", "10:00", uid="blocker")
        calendar = _make_calendar([meeting, blocker])

        result = find_best_available_slot(meeting, preferences, calendar, "2024-01-15")

        assert result is not None
        assert result == ("10:00-11:00", 1.0)

    def test_ignores_meetings_on_other_dates(self):
        """Meetings on different dates don't block slots."""
        meeting = make_meeting("09:00", "10:00")
        other_day_blocker = make_meeting("09:00", "12:00", date="2024-01-16", uid="other-day")
        calendar = _make_calendar([meeting, other_day_blocker])

        result = find_best_available_slot(meeting, PREFS, calendar, "2024-01-15")

        assert result is not None
        assert result == ("09:00-10:00", 1.0)

    def test_no_preferences_returns_none(self):
        """No preference windows → None."""
        meeting = make_meeting("09:00", "10:00")
        calendar = _make_calendar([meeting])

        result = find_best_available_slot(meeting, [], calendar, "2024-01-15")

        assert result is None

    def test_meeting_too_long_for_window(self):
        """Meeting duration exceeds preference window → None for that window."""
        meeting = make_meeting("09:00", "13:00")  # 4 hours
        preferences = [
            TimeSlotPreference(start_time="09:00", end_time="10:00", score=1.0),  # only 1 hour
        ]
        calendar = _make_calendar([meeting])

        result = find_best_available_slot(meeting, preferences, calendar, "2024-01-15")

        assert result is None


class TestEvaluateDutyOfCare:
    """Tests for all 6 scenarios in the DoC scoring grid plus validation."""

    # ---- Unsatisfiable + no booking → 1.0 ----

    def test_unsatisfiable_no_booking(self):
        calendar = _make_calendar(FULL_CALENDAR_MEETINGS)
        result = evaluate_duty_of_care(
            None, PREFS, calendar, task_satisfiable=False, has_conflicts=False
        )
        assert result.assistant_duty_of_care_score == 1.0

    # ---- Unsatisfiable + booked + conflicts → -1 ----

    def test_unsatisfiable_booked_with_conflicts(self):
        scheduled = make_meeting("09:00", "10:00")
        calendar = _make_calendar([scheduled, *FULL_CALENDAR_MEETINGS])
        result = evaluate_duty_of_care(
            scheduled, PREFS, calendar, task_satisfiable=False, has_conflicts=True
        )
        assert result.assistant_duty_of_care_score == -1.0

    # ---- Unsatisfiable + booked + no conflicts → 0.0 ----

    def test_unsatisfiable_booked_no_conflicts(self):
        # Meeting booked outside preference windows on an unsatisfiable task
        scheduled = make_meeting("18:00", "19:00")
        calendar = _make_calendar([scheduled, *FULL_CALENDAR_MEETINGS])
        result = evaluate_duty_of_care(
            scheduled, PREFS, calendar, task_satisfiable=False, has_conflicts=False
        )
        assert result.assistant_duty_of_care_score == 0.0

    # ---- Satisfiable + no booking → 0.0 ----

    def test_satisfiable_no_booking(self):
        calendar = _make_calendar([])
        result = evaluate_duty_of_care(
            None, PREFS, calendar, task_satisfiable=True, has_conflicts=False
        )
        assert result.assistant_duty_of_care_score == 0.0

    # ---- Satisfiable + booked + conflicts → -1 ----

    def test_satisfiable_booked_with_conflicts(self):
        scheduled = make_meeting("09:00", "10:00")
        calendar = _make_calendar([scheduled])
        result = evaluate_duty_of_care(
            scheduled, PREFS, calendar, task_satisfiable=True, has_conflicts=True
        )
        assert result.assistant_duty_of_care_score == -1.0

    # ---- Satisfiable + booked + no conflicts → preference_score / best_available ----

    def test_satisfiable_booked_perfect_slot(self):
        """Best slot chosen → DoC = 1.0."""
        scheduled = make_meeting("09:00", "10:00")
        calendar = _make_calendar([scheduled])
        result = evaluate_duty_of_care(
            scheduled, PREFS, calendar, task_satisfiable=True, has_conflicts=False
        )
        assert result.assistant_duty_of_care_score == 1.0
        assert result.preference_score == 1.0

    def test_satisfiable_booked_suboptimal_slot(self):
        """Lower-pref slot chosen when better was available → DoC < 1.0."""
        preferences = [
            TimeSlotPreference(start_time="09:00", end_time="12:00", score=1.0),
            TimeSlotPreference(start_time="14:00", end_time="17:00", score=0.5),
        ]
        scheduled = make_meeting("14:00", "15:00")
        calendar = _make_calendar([scheduled])
        result = evaluate_duty_of_care(
            scheduled, preferences, calendar, task_satisfiable=True, has_conflicts=False
        )
        assert result.assistant_duty_of_care_score == pytest.approx(0.5)
        assert result.preference_score == 0.5

    def test_satisfiable_booked_partial_overlap(self):
        """Meeting partially in preference window."""
        scheduled = make_meeting("11:00", "13:00")  # half in 09-12 window
        calendar = _make_calendar([scheduled])
        result = evaluate_duty_of_care(
            scheduled, PREFS, calendar, task_satisfiable=True, has_conflicts=False
        )
        # preference_score = 60min * 1.0 / 120min = 0.5
        assert result.preference_score == pytest.approx(0.5)
        # best available is fully in window (score 1.0), so DoC = 0.5 / 1.0
        assert result.assistant_duty_of_care_score == pytest.approx(0.5)

    # ---- Validation errors ----

    def test_error_conflicts_without_meeting(self):
        calendar = _make_calendar([])
        with pytest.raises(ValueError, match="Cannot have conflicts if no meeting"):
            evaluate_duty_of_care(None, PREFS, calendar, task_satisfiable=True, has_conflicts=True)

    def test_error_unsatisfiable_but_free_slot_exists(self):
        """Task marked unsatisfiable but the calendar has a free slot in preferences."""
        scheduled = make_meeting("09:00", "10:00")
        calendar = _make_calendar([scheduled])  # no other meetings blocking
        with pytest.raises(ValueError, match="unsatisfiable but free slot"):
            evaluate_duty_of_care(
                scheduled, PREFS, calendar, task_satisfiable=False, has_conflicts=False
            )

    def test_error_satisfiable_but_calendar_full(self):
        """Task marked satisfiable but no free slots in preference windows."""
        scheduled = make_meeting("18:00", "19:00")  # outside prefs
        calendar = _make_calendar([scheduled, *FULL_CALENDAR_MEETINGS])
        with pytest.raises(ValueError, match="satisfiable but no free slots"):
            evaluate_duty_of_care(
                scheduled, PREFS, calendar, task_satisfiable=True, has_conflicts=False
            )
