"""Tests for difficulty-aware calendar task assembly."""

import random

from srbench.benchmarks.calendar_scheduling.types import (
    LabeledMeeting,
)
from srbench_data_gen.calendar_scheduling.assemble import (
    _slot_index_for_time,
)
from srbench_data_gen.calendar_scheduling.generate_preferences import (
    sample_preferences,
)

# ── Helpers ──────────────────────────────────────────────────────────


def _make_meeting(slot_index: int, is_secret: bool = False) -> LabeledMeeting:
    """Create a LabeledMeeting at the given working-slot index (0=08:00, 10=18:00)."""
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
        is_secret=is_secret,
    )


# ── Tests for ranked preference generation ───────────────────────────


class TestRankedPreferences:
    """Test that sample_preferences assigns unique ranked scores to free slots."""

    def _make_calendar(self, busy_slots: list[int]) -> list[LabeledMeeting]:
        return [_make_meeting(i) for i in busy_slots]

    def test_free_slots_get_unique_scores(self):
        """Every free slot should have a distinct preference score."""
        cal = self._make_calendar([0, 6, 7, 8, 9, 10])  # free: 1,2,3,4,5
        prefs = sample_preferences(
            calendar=cal,
            mutually_free_indices={1, 2, 3, 4, 5},
            requested_slot_index=0,
            rng=random.Random(42),
        )
        free_scores = [
            p.score for p in prefs if _slot_index_for_time(p.start_time) in {1, 2, 3, 4, 5}
        ]
        assert len(free_scores) == len(set(free_scores)), f"Duplicate scores: {free_scores}"

    def test_scores_span_full_range(self):
        """Free slot scores should span from SCORE_MIN to SCORE_MAX."""
        cal = self._make_calendar([0, 6, 7, 8, 9, 10])  # free: 1,2,3,4,5
        prefs = sample_preferences(
            calendar=cal,
            mutually_free_indices={1, 2, 3, 4, 5},
            requested_slot_index=0,
            rng=random.Random(42),
        )
        free_scores = [
            p.score for p in prefs if _slot_index_for_time(p.start_time) in {1, 2, 3, 4, 5}
        ]
        assert max(free_scores) == 1.0
        assert min(free_scores) == 0.0

    def test_occupied_slots_get_low_score(self):
        """Occupied slots should all get OCCUPIED_SCORE."""
        cal = self._make_calendar([0, 6, 7, 8, 9, 10])
        prefs = sample_preferences(
            calendar=cal,
            mutually_free_indices={1, 2, 3, 4, 5},
            requested_slot_index=0,
            rng=random.Random(42),
        )
        for p in prefs:
            idx = _slot_index_for_time(p.start_time)
            if idx in {0, 6, 7, 8, 9, 10}:
                assert p.score == 0.0, f"Occupied slot {idx} has score {p.score}"

    def test_single_free_slot_gets_max(self):
        """A single free slot should get SCORE_MAX."""
        cal = self._make_calendar([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])  # only slot 10 free
        prefs = sample_preferences(
            calendar=cal, mutually_free_indices={10}, requested_slot_index=0, rng=random.Random(42)
        )
        free_pref = [p for p in prefs if _slot_index_for_time(p.start_time) == 10][0]
        assert free_pref.score == 1.0

    def test_different_seeds_produce_different_rankings(self):
        """Different RNG seeds should shuffle the rank order."""
        cal = self._make_calendar([0, 6, 7, 8, 9, 10])
        prefs1 = sample_preferences(
            calendar=cal,
            mutually_free_indices={1, 2, 3, 4, 5},
            requested_slot_index=0,
            rng=random.Random(1),
        )
        prefs2 = sample_preferences(
            calendar=cal,
            mutually_free_indices={1, 2, 3, 4, 5},
            requested_slot_index=0,
            rng=random.Random(2),
        )
        scores1 = [p.score for p in prefs1]
        scores2 = [p.score for p in prefs2]
        assert scores1 != scores2, "Different seeds should give different rankings"

    def test_deterministic_with_same_seed(self):
        """Same seed should produce identical preferences."""
        cal = self._make_calendar([0, 6, 7, 8, 9, 10])
        prefs1 = sample_preferences(
            calendar=cal,
            mutually_free_indices={1, 2, 3, 4, 5},
            requested_slot_index=0,
            rng=random.Random(42),
        )
        prefs2 = sample_preferences(
            calendar=cal,
            mutually_free_indices={1, 2, 3, 4, 5},
            requested_slot_index=0,
            rng=random.Random(42),
        )
        for p1, p2 in zip(prefs1, prefs2):
            assert p1.score == p2.score
