"""Tests for the preference-adherence scoring engine.

The engine is pure: it takes the two calendars plus a task's hard constraints
and weighted soft preferences and grades whatever the assistant scheduled.
These tests pin the scoring contract branch by branch.
"""

import pytest
from srbench.benchmarks.calendar_scheduling.evaluation.preference_adherence import (
    SoftPreference,
    ends_by,
    outside,
    score_task,
    starts_at_or_after,
    to_hhmm,
    to_minutes,
    within,
)
from srbench.benchmarks.calendar_scheduling.types import LabeledMeeting, Meeting

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


def _scheduled(start_time: str, end_time: str) -> Meeting:
    """Return the meeting the assistant booked."""
    return Meeting(
        uid="new-001",
        title="Project sync",
        description="",
        organizer="bob@example.com",
        date="2024-06-15",
        start_time=start_time,
        end_time=end_time,
        attendees=[],
    )


def _score(scheduled, assistant_calendar=None, requestor_calendar=None, **kwargs):
    """Call score_task with empty calendars and a 60-minute meeting by default."""
    return score_task(
        scheduled_meeting=scheduled,
        assistant_calendar=assistant_calendar or [],
        requestor_calendar=requestor_calendar or [],
        duration_minutes=DURATION,
        **kwargs,
    )


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
    """Tests for the predicate constructors, including boundary behaviour."""

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


class TestNothingScheduled:
    """Case 1: the assistant declined to schedule."""

    def test_declining_is_correct_when_no_slot_is_feasible(self):
        """Hard constraints that exclude the whole day make declining the right call."""
        result = _score(None, hard_constraints=[within("22:00", "23:00")])

        assert result.hard_constraints_satisfied
        assert result.soft_constraints_score == 1.0
        assert result.feasible_slots == []

    def test_declining_is_wrong_when_a_slot_was_available(self):
        """Failing to schedule a satisfiable task scores zero on both axes."""
        result = _score(None)

        assert not result.hard_constraints_satisfied
        assert result.soft_constraints_score == 0.0
        assert "09:00" in result.feasible_slots

    def test_busy_calendars_alone_can_make_a_task_infeasible(self):
        """Feasibility accounts for both calendars, not just hard constraints."""
        blocked = [_busy("08:00", "19:00")]

        result = _score(None, assistant_calendar=blocked)

        assert result.hard_constraints_satisfied
        assert result.feasible_slots == []


class TestScheduledButUnacceptable:
    """Cases 2 and 3: something was scheduled that should not have been."""

    def test_scheduling_when_nothing_is_feasible_scores_zero(self):
        """The assistant should have declined instead."""
        result = _score(_scheduled("09:00", "10:00"), hard_constraints=[within("22:00", "23:00")])

        assert not result.hard_constraints_satisfied
        assert result.soft_constraints_score == 0.0
        assert result.chosen_slot == "09:00"

    def test_violating_a_hard_constraint_scores_zero(self):
        """A slot outside the allowed window fails even though other slots were fine."""
        result = _score(_scheduled("15:00", "16:00"), hard_constraints=[outside("12:00", "16:00")])

        assert not result.hard_constraints_satisfied
        assert result.soft_constraints_score == 0.0
        assert "hard constraint" in result.explanation

    def test_double_booking_scores_zero(self):
        """Landing on a slot the requestor is busy for fails."""
        result = _score(_scheduled("09:00", "10:00"), requestor_calendar=[_busy("09:00", "10:00")])

        assert not result.hard_constraints_satisfied
        assert result.soft_constraints_score == 0.0

    def test_wrong_duration_scores_zero(self):
        """A 30-minute booking does not satisfy a 60-minute request."""
        result = _score(_scheduled("09:00", "09:30"))

        assert not result.hard_constraints_satisfied
        assert "30 minutes" in result.explanation

    def test_reported_conflicts_score_zero(self):
        """Conflicts the assistant introduced are only visible via has_conflicts."""
        result = _score(_scheduled("09:00", "10:00"), has_conflicts=True)

        assert not result.hard_constraints_satisfied
        assert "conflict" in result.explanation


class TestSoftPreferenceScoring:
    """Case 4: the slot is acceptable, so soft preferences decide the score."""

    def test_no_soft_preferences_scores_full_marks(self):
        """With nothing to rank by, any acceptable slot is as good as any other."""
        result = _score(_scheduled("09:00", "10:00"))

        assert result.hard_constraints_satisfied
        assert result.soft_constraints_score == 1.0

    def test_best_slot_scores_full_marks(self):
        """Honouring every attainable preference scores 1.0."""
        preferences = [SoftPreference("afternoon", starts_at_or_after("13:00"))]

        result = _score(_scheduled("13:00", "14:00"), soft_preferences=preferences)

        assert result.soft_constraints_score == 1.0
        assert result.satisfied_soft_constraints == ["afternoon"]
        assert result.missed_soft_constraints == []

    def test_suboptimal_slot_scores_the_attained_fraction(self):
        """Meeting one of two attainable preferences scores 0.5."""
        preferences = [
            SoftPreference("afternoon", starts_at_or_after("13:00")),
            SoftPreference("before_five", ends_by("17:00")),
        ]

        result = _score(_scheduled("17:00", "18:00"), soft_preferences=preferences)

        assert result.hard_constraints_satisfied
        assert result.soft_constraints_score == 0.5
        assert result.satisfied_soft_constraints == ["afternoon"]
        assert result.missed_soft_constraints == ["before_five"]

    def test_weights_scale_the_fraction(self):
        """A weight-3 preference is worth three times a weight-1 one."""
        preferences = [
            SoftPreference("afternoon", starts_at_or_after("13:00"), weight=3.0),
            SoftPreference("before_five", ends_by("17:00"), weight=1.0),
        ]

        result = _score(_scheduled("17:00", "18:00"), soft_preferences=preferences)

        assert result.soft_constraints_score == 0.75

    def test_unattainable_preferences_do_not_penalise(self):
        """A preference no feasible slot can meet is excluded from the reference."""
        blocked = [_busy("08:00", "13:00")]
        preferences = [SoftPreference("morning", ends_by("12:00"))]

        result = _score(
            _scheduled("13:00", "14:00"),
            assistant_calendar=blocked,
            soft_preferences=preferences,
        )

        assert result.hard_constraints_satisfied
        assert result.soft_constraints_score == 1.0

    def test_conflicting_preferences_are_graded_against_the_best_slot(self):
        """Two preferences no slot can satisfy together still allow a perfect score.

        This is the case that makes grading against the best achievable slot
        necessary: scoring against all preferences would cap every run at 0.5
        and make the task look unsolvable.
        """
        preferences = [
            SoftPreference("early", ends_by("10:00")),
            SoftPreference("late", starts_at_or_after("16:00")),
        ]

        result = _score(_scheduled("09:00", "10:00"), soft_preferences=preferences)

        assert result.soft_constraints_score == 1.0
        assert sorted(result.best_slots) == ["08:00", "09:00", "16:00", "17:00", "18:00"]

    def test_tying_the_best_weight_reports_no_misses(self):
        """Picking a different but equally good slot is not reported as a miss.

        The earliest best slot honours "early" while the chosen one honours
        "late". Both are optimal, so nothing was forgone.
        """
        preferences = [
            SoftPreference("early", ends_by("10:00")),
            SoftPreference("late", starts_at_or_after("16:00")),
        ]

        result = _score(_scheduled("16:00", "17:00"), soft_preferences=preferences)

        assert result.soft_constraints_score == 1.0
        assert result.satisfied_soft_constraints == ["late"]
        assert result.missed_soft_constraints == []

    def test_off_grid_slot_beating_the_reference_is_clamped(self):
        """A slot between grid points may out-score the reference; 1.0 is the cap.

        Candidate starts are on the hour, so no considered slot satisfies both
        preferences. The 09:30 booking satisfies both and would score 2.0.
        """
        preferences = [
            SoftPreference("starts_after_nine_thirty", starts_at_or_after("09:30")),
            SoftPreference("ends_by_ten_thirty", ends_by("10:30")),
        ]

        result = _score(_scheduled("09:30", "10:30"), soft_preferences=preferences)

        assert result.hard_constraints_satisfied
        assert result.soft_constraints_score == 1.0
        assert len(result.satisfied_soft_constraints) == 2

    def test_feasible_slots_exclude_busy_and_forbidden_times(self):
        """The reported slot list reflects both calendars and the hard constraints."""
        result = _score(
            _scheduled("13:00", "14:00"),
            assistant_calendar=[_busy("08:00", "12:00")],
            requestor_calendar=[_busy("15:00", "19:00")],
            hard_constraints=[outside("12:00", "13:00")],
        )

        assert result.feasible_slots == ["13:00", "14:00"]
