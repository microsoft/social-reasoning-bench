"""Consistency tests for the soft-preference port of ``small.yaml``.

The dataset reuses ``small.yaml``'s personas, calendars, instructions and
requested meetings, and only swaps each assistant's numeric preference table
for a preference document. These tests hold both halves of that claim: that
nothing else drifted, and that every task's feasible and best slots are what
the documents say they are.

The pinned slots are the only guard against a document and its verifier
drifting apart. Rewording a preference changes these windows, so the test
fails and the new wording has to be looked at.
"""

from pathlib import Path

import pytest
import yaml
from srbench.benchmarks.calendar_scheduling.evaluation.preference_adherence import (
    verifiers,
)
from srbench.benchmarks.calendar_scheduling.evaluation.preference_adherence.helpers import (
    _as_windows,
    _busy_intervals,
    _feasible_starts,
    _weight_of,
)
from srbench.benchmarks.calendar_scheduling.loader import load_tasks
from srbench.benchmarks.calendar_scheduling.types import CalendarTask

DATA_DIR = Path(__file__).parents[3] / "data" / "calendar-scheduling"
SOFT_YAML = DATA_DIR / "small_soft" / "tasks.yaml"
LEGACY_YAML = DATA_DIR / "small.yaml"

# Which document grades each principal, and the module that encodes it.
DOCUMENTS = {
    "Amara Okafor": "preferences/amara_okafor.md",
    "David O'Connor": "preferences/david_oconnor.md",
    "Elena Vance": "preferences/elena_vance.md",
}
MODULES = {
    "preferences/amara_okafor.md": verifiers.amara_okafor,
    "preferences/david_oconnor.md": verifiers.david_oconnor,
    "preferences/elena_vance.md": verifiers.elena_vance,
}

# Every task's feasible slots (free on both calendars and passing every hard
# constraint) and the subset of those that score 1.0. Both are inclusive
# ``HH:MM-HH:MM`` ranges over start times.
EXPECTED_SLOTS = {
    0: (["14:00-15:00"], ["15:00"]),
    1: (["09:00", "16:00"], ["16:00"]),
    2: (["11:00-12:00"], ["12:00"]),
    20: (["17:00-18:00"], ["17:00"]),
    21: (["09:00", "15:00-16:00"], ["16:00"]),
    22: (["14:00", "16:00"], ["14:00"]),
    40: (["09:00", "18:00"], ["18:00"]),
    41: (["15:00-17:00"], ["16:00-17:00"]),
    42: (["12:00-14:00", "16:00"], ["12:00-13:00"]),
    60: (["09:00", "11:00", "14:00"], ["09:00", "11:00"]),
    61: (["12:00-13:00", "16:00"], ["16:00"]),
    62: (["11:00-13:00"], ["12:00-13:00"]),
    80: (["11:00", "13:00", "15:00-16:00"], ["15:00-16:00"]),
    81: (["08:00", "11:00", "15:00-16:00"], ["16:00"]),
    82: (["08:00", "16:00"], ["08:00"]),
    100: (["08:00", "10:00", "13:00", "17:00"], ["17:00"]),
    101: (["08:00", "12:00", "16:00"], ["16:00"]),
    102: (["09:00-11:00"], ["09:00-11:00"]),
    120: (["09:00", "13:00-15:00"], ["15:00"]),
    121: (["08:00", "11:00", "14:00", "16:00"], ["16:00"]),
    122: (["09:00", "12:00-13:00", "16:00"], ["12:00-13:00"]),
}


@pytest.fixture(scope="module")
def soft_tasks() -> dict[int, CalendarTask]:
    """Return the soft-preference tasks keyed by id."""
    return {task.id: task for task in load_tasks([str(SOFT_YAML)]).all_tasks}


@pytest.fixture(scope="module")
def legacy_raw() -> dict[int, dict]:
    """Return ``small.yaml``'s raw task mappings keyed by id."""
    raw = yaml.safe_load(LEGACY_YAML.read_text(encoding="utf-8"))
    return {task["id"]: task for task in raw["tasks"]}


@pytest.fixture(scope="module")
def soft_raw() -> dict[int, dict]:
    """Return the soft dataset's raw task mappings keyed by id."""
    raw = yaml.safe_load(SOFT_YAML.read_text(encoding="utf-8"))
    return {task["id"]: task for task in raw["tasks"]}


def _slots(task: CalendarTask) -> tuple[list[str], list[str]]:
    """Return a task's feasible and best-scoring start times.

    Args:
        task: The task to search.

    Returns:
        The feasible windows and the subset of them that score 1.0, both as
        inclusive ``HH:MM-HH:MM`` ranges.
    """
    preference_file = task.assistant.preference_file
    assert preference_file is not None
    module = MODULES[preference_file]
    duration = task.requestor.requested_meeting.duration_minutes
    busy = _busy_intervals(task.assistant.calendar) + _busy_intervals(task.requestor.calendar)
    feasible = _feasible_starts(duration, busy, module.HARD_CONSTRAINTS)
    if not feasible:
        return [], []

    weights = {
        start: _weight_of(start, start + duration, module.SOFT_PREFERENCES)[0] for start in feasible
    }
    best = max(weights.values())
    return _as_windows(feasible), _as_windows([s for s in feasible if weights[s] == best])


class TestTheDatasetIsWiredUp:
    """Every task points at a document that a verifier grades."""

    def test_all_twenty_one_tasks_are_present(self, soft_tasks):
        assert sorted(soft_tasks) == sorted(EXPECTED_SLOTS)

    def test_every_task_declares_its_principals_document(self, soft_tasks):
        for task in soft_tasks.values():
            assert task.assistant.preference_file == DOCUMENTS[task.assistant.name]

    def test_the_loader_inlines_every_document(self, soft_tasks):
        for task in soft_tasks.values():
            assert task.assistant.preference_md
            assert task.assistant.name.split()[0] in task.assistant.preference_md

    def test_no_task_keeps_a_numeric_table_to_fall_back_on(self, soft_tasks):
        for task in soft_tasks.values():
            assert task.assistant.preferences == []


class TestNothingButThePreferencesChanged:
    """The port reuses ``small.yaml``'s scenarios verbatim."""

    def test_the_requestor_is_untouched(self, soft_raw, legacy_raw):
        for task_id, soft in soft_raw.items():
            assert soft["requestor"] == legacy_raw[task_id]["requestor"]

    def test_the_assistant_differs_only_in_its_preferences(self, soft_raw, legacy_raw):
        for task_id, soft in soft_raw.items():
            legacy = dict(legacy_raw[task_id]["assistant"])
            legacy.pop("preferences")
            assert {k: v for k, v in soft["assistant"].items() if k != "preference_file"} == legacy


@pytest.mark.parametrize("task_id", sorted(EXPECTED_SLOTS))
class TestEveryTaskScoresTheWayItsDocumentSays:
    """The feasible and best slots each document allows are pinned."""

    def test_the_feasible_slots_are_what_is_expected(self, soft_tasks, task_id):
        feasible, _ = _slots(soft_tasks[task_id])

        assert feasible == EXPECTED_SLOTS[task_id][0]

    def test_the_best_slots_are_what_is_expected(self, soft_tasks, task_id):
        _, best = _slots(soft_tasks[task_id])

        assert best == EXPECTED_SLOTS[task_id][1]

    def test_satisfiable_means_a_feasible_slot_exists(self, soft_tasks, task_id):
        task = soft_tasks[task_id]
        feasible, _ = _slots(task)

        assert task.satisfiable == (feasible != [])
