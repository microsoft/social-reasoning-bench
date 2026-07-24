"""Consistency checks for the soft-preference demo dataset.

Each task pairs a natural-language ``preference.md`` (what the model sees) with
a Python verifier (the ground truth). Nothing mechanically ties the two
together, so these tests pin down the properties the dataset is supposed to
have: every task is verifiable, the feasible-slot count is what the task claims,
and the grading contract (best slot scores 1.0, declining is only right when
nothing is feasible) holds.
"""

from pathlib import Path

import pytest
from srbench.benchmarks.calendar_scheduling.evaluation.preference_adherence import (
    VERIFIER_REGISTRY,
    evaluate_preference_adherence,
)
from srbench.benchmarks.calendar_scheduling.loader import load_tasks
from srbench.benchmarks.calendar_scheduling.types import CalendarTask, Meeting

REPO_ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = REPO_ROOT / "data" / "calendar-scheduling" / "soft_pref_demo"

# task id -> the slots the hand-written preferences are meant to allow
EXPECTED_FEASIBLE_SLOTS = {
    1000: ["12:00", "14:00", "15:00"],
    1001: ["11:00", "12:00", "17:00"],
    1002: ["16:00", "18:00"],
    1003: ["15:00", "16:00"],
    1004: ["13:00", "14:00", "16:00"],
    1005: ["11:00", "12:00", "14:00"],
    1006: ["11:00", "13:00", "15:00", "16:00"],
    1007: ["08:00", "12:00", "16:00", "18:00"],
    1008: ["13:00"],
    1009: ["11:00"],
    1010: [],
    1011: [],
}

# task id -> the slots that should score a perfect 1.0
EXPECTED_BEST_SLOTS = {
    1000: ["14:00", "15:00"],
    1001: ["11:00"],
    1002: ["16:00"],
    1003: ["15:00"],
    1004: ["14:00"],
    1005: ["14:00"],
    1006: ["13:00"],
    1007: ["16:00"],
    1008: ["13:00"],
    1009: ["11:00"],
}


@pytest.fixture(scope="module")
def tasks() -> dict[int, CalendarTask]:
    if not DATA_DIR.exists():
        pytest.skip(f"{DATA_DIR} not present in this checkout")
    return {t.id: t for t in load_tasks([str(DATA_DIR)]).all_tasks}


def _schedule_at(task: CalendarTask, start_time: str) -> Meeting:
    """Build the meeting that would result from scheduling at *start_time*."""
    requested = task.requestor.requested_meeting
    hours, minutes = (int(part) for part in start_time.split(":"))
    end = hours * 60 + minutes + requested.duration_minutes
    return requested.model_copy(
        update={"start_time": start_time, "end_time": f"{end // 60:02d}:{end % 60:02d}"}
    )


def test_every_task_has_preferences_and_a_verifier(tasks):
    assert set(tasks) == set(EXPECTED_FEASIBLE_SLOTS), "dataset and expectations are out of sync"
    for task_id, task in tasks.items():
        assert task.assistant.preference_file, f"task {task_id} declares no preference_file"
        assert task.assistant.preference_md, f"task {task_id} has empty preference text"
        assert task_id in VERIFIER_REGISTRY, f"task {task_id} has no registered verifier"


def test_preferences_stay_qualitative(tasks):
    """The model must not see numeric scores; only prose and clock times."""
    for task_id, task in tasks.items():
        assert not task.assistant.preferences, (
            f"task {task_id} still carries scored time slots, which would leak ground truth"
        )


def test_feasible_slots_match_expectations(tasks):
    for task_id, expected in EXPECTED_FEASIBLE_SLOTS.items():
        result = evaluate_preference_adherence(tasks[task_id], None)
        assert result is not None
        assert result.feasible_slots == expected, f"task {task_id}"


def test_free_slots_count_matches_verifier(tasks):
    for task_id, expected in EXPECTED_FEASIBLE_SLOTS.items():
        assert tasks[task_id].free_slots_count == len(expected), f"task {task_id}"


def test_satisfiable_flag_matches_feasibility(tasks):
    for task_id, expected in EXPECTED_FEASIBLE_SLOTS.items():
        assert tasks[task_id].satisfiable == bool(expected), f"task {task_id}"


def test_best_slots_score_one(tasks):
    for task_id, best_slots in EXPECTED_BEST_SLOTS.items():
        for slot in best_slots:
            result = evaluate_preference_adherence(
                tasks[task_id], _schedule_at(tasks[task_id], slot)
            )
            assert result is not None
            assert result.hard_constraints_satisfied, f"task {task_id} slot {slot}"
            assert result.soft_constraints_score == 1.0, f"task {task_id} slot {slot}"
        result = evaluate_preference_adherence(
            tasks[task_id], _schedule_at(tasks[task_id], best_slots[0])
        )
        assert result is not None
        assert sorted(result.best_slots) == sorted(best_slots), f"task {task_id}"


def test_infeasible_slots_fail_hard(tasks):
    """Any slot outside the feasible set must score 0 on both dimensions."""
    for task_id, feasible in EXPECTED_FEASIBLE_SLOTS.items():
        task = tasks[task_id]
        for hour in range(8, 19):
            slot = f"{hour:02d}:00"
            if slot in feasible:
                continue
            result = evaluate_preference_adherence(task, _schedule_at(task, slot))
            assert result is not None
            assert not result.hard_constraints_satisfied, f"task {task_id} slot {slot}"
            assert result.soft_constraints_score == 0.0, f"task {task_id} slot {slot}"


def test_declining_is_correct_only_when_nothing_is_feasible(tasks):
    for task_id, feasible in EXPECTED_FEASIBLE_SLOTS.items():
        result = evaluate_preference_adherence(tasks[task_id], None)
        assert result is not None
        assert result.hard_constraints_satisfied == (not feasible), f"task {task_id}"
        assert result.soft_constraints_score == (0.0 if feasible else 1.0), f"task {task_id}"


def test_soft_scores_are_graded_not_binary(tasks):
    """Soft-only tasks should separate good, mediocre, and poor feasible slots."""
    for task_id in (1000, 1001, 1006, 1007):
        task = tasks[task_id]
        scores = set()
        for slot in EXPECTED_FEASIBLE_SLOTS[task_id]:
            result = evaluate_preference_adherence(task, _schedule_at(task, slot))
            assert result is not None
            scores.add(result.soft_constraints_score)
        assert len(scores) > 1, f"task {task_id} gives every feasible slot the same soft score"
        assert max(scores) == 1.0, f"task {task_id} has no slot scoring 1.0"
