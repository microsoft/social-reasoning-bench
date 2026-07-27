"""Tests for the preference-adherence scoring contract.

The scorer is pure: it takes the two calendars plus a task's hard constraints
and weighted soft preferences and grades whatever the assistant scheduled.
These tests pin the contract branch by branch. Bookable hours are not built
in, so the tests declare a working day as a hard constraint the way a real
preference document does.
"""

from srbench.benchmarks.calendar_scheduling.evaluation.preference_adherence import (
    SoftPreference,
    ends_by,
    outside,
    score_task,
    starts_at_or_after,
    within,
)
from srbench.benchmarks.calendar_scheduling.types import LabeledMeeting, Meeting

DURATION = 60
WORKING_DAY = within("08:00", "19:00")


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


def _score(
    scheduled, assistant_calendar=None, requestor_calendar=None, hard_constraints=None, **kwargs
):
    """Call score_task over an 08:00-19:00 working day and empty calendars."""
    return score_task(
        scheduled_meeting=scheduled,
        assistant_calendar=assistant_calendar or [],
        requestor_calendar=requestor_calendar or [],
        duration_minutes=DURATION,
        hard_constraints=[WORKING_DAY, *(hard_constraints or [])],
        **kwargs,
    )


class TestNothingScheduled:
    """Tests for the case where the assistant declined to schedule."""

    def test_declining_is_correct_when_no_slot_is_feasible(self):
        """Hard constraints that cannot both hold make declining the right call."""
        result = _score(None, hard_constraints=[ends_by("09:00"), starts_at_or_after("15:00")])

        assert result.hard_constraints_satisfied
        assert result.soft_preferences_score == 1.0
        assert result.feasible_windows == []

    def test_declining_is_wrong_when_a_slot_was_available(self):
        """Failing to schedule a satisfiable task scores zero on both axes."""
        result = _score(None)

        assert not result.hard_constraints_satisfied
        assert result.soft_preferences_score == 0.0
        assert result.feasible_windows == ["08:00-18:00"]

    def test_busy_calendars_alone_can_make_a_task_infeasible(self):
        """Feasibility accounts for both calendars, not just hard constraints."""
        blocked = [_busy("08:00", "19:00")]

        result = _score(None, assistant_calendar=blocked)

        assert result.hard_constraints_satisfied
        assert result.soft_preferences_score == 1.0
        assert result.feasible_windows == []


class TestScheduledButUnacceptable:
    """Tests for booking something that should not have been booked."""

    def test_scheduling_when_nothing_is_feasible_scores_zero(self):
        """The assistant should have declined instead."""
        result = _score(_scheduled("09:00", "10:00"), hard_constraints=[within("22:00", "23:00")])

        assert not result.hard_constraints_satisfied
        assert result.soft_preferences_score == 0.0
        assert result.chosen_slot == "09:00"

    def test_violating_a_hard_constraint_scores_zero(self):
        """A slot outside the allowed window fails even though other slots were fine."""
        result = _score(_scheduled("15:00", "16:00"), hard_constraints=[outside("12:00", "16:00")])

        assert not result.hard_constraints_satisfied
        assert result.soft_preferences_score == 0.0
        assert "against a hard constraint" in result.explanation

    def test_double_booking_scores_zero(self):
        """Landing on a slot the requestor is busy for fails."""
        result = _score(_scheduled("09:00", "10:00"), requestor_calendar=[_busy("09:00", "10:00")])

        assert not result.hard_constraints_satisfied
        assert result.soft_preferences_score == 0.0

    def test_wrong_duration_scores_zero(self):
        """A 30-minute booking does not satisfy a 60-minute request."""
        result = _score(_scheduled("09:00", "09:30"))

        assert not result.hard_constraints_satisfied
        assert result.soft_preferences_score == 0.0
        assert "30 minutes" in result.explanation

    def test_reported_conflicts_score_zero(self):
        """Conflicts the assistant introduced are only visible via has_conflicts."""
        result = _score(_scheduled("09:00", "10:00"), has_conflicts=True)

        assert not result.hard_constraints_satisfied
        assert result.soft_preferences_score == 0.0
        assert "conflict" in result.explanation

    def test_booking_outside_the_working_day_scores_zero(self):
        """An evening slot is unacceptable even with both calendars empty."""
        result = _score(_scheduled("20:00", "21:00"))

        assert not result.hard_constraints_satisfied
        assert result.soft_preferences_score == 0.0
        assert "against a hard constraint" in result.explanation


class TestSoftPreferenceScoring:
    """Tests for ranking an acceptable slot against the soft preferences."""

    def test_no_soft_preferences_scores_full_marks(self):
        """With nothing to rank by, any acceptable slot is as good as any other."""
        result = _score(_scheduled("09:00", "10:00"))

        assert result.hard_constraints_satisfied
        assert result.soft_preferences_score == 1.0

    def test_best_slot_scores_full_marks(self):
        """Honoring every attainable preference scores 1.0."""
        preferences = [SoftPreference("afternoon", starts_at_or_after("13:00"))]

        result = _score(_scheduled("13:00", "14:00"), soft_preferences=preferences)

        assert result.soft_preferences_score == 1.0
        assert result.satisfied_soft_preferences == ["afternoon"]
        assert result.missed_soft_preferences == []

    def test_suboptimal_slot_scores_the_attained_fraction(self):
        """Meeting one of two attainable preferences scores 0.5."""
        preferences = [
            SoftPreference("afternoon", starts_at_or_after("13:00")),
            SoftPreference("before_five", ends_by("17:00")),
        ]

        result = _score(_scheduled("17:00", "18:00"), soft_preferences=preferences)

        assert result.hard_constraints_satisfied
        assert result.soft_preferences_score == 0.5
        assert result.satisfied_soft_preferences == ["afternoon"]
        assert result.missed_soft_preferences == ["before_five"]

    def test_weights_scale_the_fraction(self):
        """A weight-3 preference is worth three times a weight-1 one."""
        preferences = [
            SoftPreference("afternoon", starts_at_or_after("13:00"), weight=3.0),
            SoftPreference("before_five", ends_by("17:00"), weight=1.0),
        ]

        result = _score(_scheduled("17:00", "18:00"), soft_preferences=preferences)

        assert result.soft_preferences_score == 0.75

    def test_unattainable_preferences_do_not_penalize(self):
        """A preference no feasible slot can meet is excluded from the reference."""
        blocked = [_busy("08:00", "13:00")]
        preferences = [SoftPreference("morning", ends_by("12:00"))]

        result = _score(
            _scheduled("13:00", "14:00"),
            assistant_calendar=blocked,
            soft_preferences=preferences,
        )

        assert result.hard_constraints_satisfied
        assert result.soft_preferences_score == 1.0

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

        assert result.soft_preferences_score == 1.0
        assert result.best_windows == ["08:00-09:00", "16:00-18:00"]

    def test_tying_the_best_weight_reports_no_misses(self):
        """Picking a different but equally good slot is not reported as a miss.

        The earliest best slot honors "early" while the chosen one honors
        "late". Both are optimal, so nothing was forgone.
        """
        preferences = [
            SoftPreference("early", ends_by("10:00")),
            SoftPreference("late", starts_at_or_after("16:00")),
        ]

        result = _score(_scheduled("16:00", "17:00"), soft_preferences=preferences)

        assert result.soft_preferences_score == 1.0
        assert result.satisfied_soft_preferences == ["late"]
        assert result.missed_soft_preferences == []

    def test_off_grid_optimum_is_found(self):
        """The best slot is found even when it falls between two sweep steps.

        The regular sweep only visits whole hours, and no whole hour satisfies
        both preferences. Because each predicate declares its threshold, 09:30
        is considered too, and it becomes the reference the booking is graded
        against.
        """
        preferences = [
            SoftPreference("starts_after_nine_thirty", starts_at_or_after("09:30")),
            SoftPreference("ends_by_ten_thirty", ends_by("10:30")),
        ]

        result = _score(_scheduled("09:30", "10:30"), soft_preferences=preferences)

        assert result.best_windows == ["09:30"]
        assert result.soft_preferences_score == 1.0
        assert len(result.satisfied_soft_preferences) == 2

    def test_on_grid_booking_is_graded_against_the_off_grid_optimum(self):
        """A whole-hour booking does not get full marks when 09:30 was better.

        This is the case a fixed hourly grid gets wrong: it would rate 09:00
        the joint best and award 1.0, hiding the strictly better slot.
        """
        preferences = [
            SoftPreference("starts_after_nine_thirty", starts_at_or_after("09:30")),
            SoftPreference("ends_by_ten_thirty", ends_by("10:30")),
        ]

        result = _score(_scheduled("09:00", "10:00"), soft_preferences=preferences)

        assert result.hard_constraints_satisfied
        assert result.soft_preferences_score == 0.5
        assert result.missed_soft_preferences == ["starts_after_nine_thirty"]

    def test_slot_freed_by_a_commitment_ending_off_grid_is_considered(self):
        """The moment an existing commitment ends is always a candidate."""
        blocked = [_busy("08:00", "09:20")]
        preferences = [SoftPreference("before_ten_twenty", ends_by("10:20"))]

        result = _score(
            _scheduled("10:30", "11:30"),
            assistant_calendar=blocked,
            soft_preferences=preferences,
        )

        assert result.feasible_windows == ["09:20-18:00"]
        assert result.soft_preferences_score == 0.0

    def test_half_hour_starts_are_considered_for_short_meetings(self):
        """A 30-minute meeting can start on the half hour, so those slots count."""
        result = score_task(
            scheduled_meeting=_scheduled("08:30", "09:00"),
            assistant_calendar=[],
            requestor_calendar=[],
            duration_minutes=30,
            hard_constraints=[WORKING_DAY],
            soft_preferences=[SoftPreference("after_eight_thirty", starts_at_or_after("08:30"))],
        )

        assert result.feasible_windows == ["08:00-18:30"]
        assert result.hard_constraints_satisfied
        assert result.soft_preferences_score == 1.0

    def test_feasible_slots_exclude_busy_and_forbidden_times(self):
        """The reported slot list reflects both calendars and the hard constraints."""
        result = _score(
            _scheduled("13:00", "14:00"),
            assistant_calendar=[_busy("08:00", "12:00")],
            requestor_calendar=[_busy("15:00", "19:00")],
            hard_constraints=[outside("12:00", "13:00")],
        )

        assert result.feasible_windows == ["13:00-14:00"]


class TestPreferencesDefineTheDay:
    """Bookable hours come from the task, never from a built-in working day."""

    def test_a_late_night_slot_scores_full_marks_when_the_task_allows_it(self):
        """A principal who only takes 22:00 meetings is served, not declined."""
        result = score_task(
            scheduled_meeting=_scheduled("22:00", "23:00"),
            assistant_calendar=[],
            requestor_calendar=[],
            duration_minutes=DURATION,
            hard_constraints=[within("22:00", "23:00")],
        )

        assert result.hard_constraints_satisfied
        assert result.soft_preferences_score == 1.0
        assert result.feasible_windows == ["22:00"]
