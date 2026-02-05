"""Tests for duty of care scoring functions."""

import pytest
from sage_benchmark.calendar_scheduling.evaluation.duty_of_care import (
    compute_preference_score,
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
