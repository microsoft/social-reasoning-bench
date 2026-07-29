"""Tests for the soft-preference port of ``small.yaml``.

The port swaps each task's numeric preference table for a preference document
the assistant reads and a verifier that grades against it. That only works if
the three agree, so these tests check the parts a machine can check: that the
scenarios are otherwise untouched, that every document has a verifier and vice
versa, that each verifier ranks slots exactly as the numeric table it replaced,
that each document states the ranking its verifier enforces, and that every
task stays schedulable.

These are properties of the whole dataset rather than assertions about
individual tasks, so they hold for however many tasks the dataset grows to.
"""

import importlib
import re
from pathlib import Path

import pytest
import yaml
from srbench.benchmarks.calendar_scheduling.evaluation.preference_adherence import (
    registry,
    to_hhmm,
    to_minutes,
)
from srbench.benchmarks.calendar_scheduling.evaluation.preference_adherence.helpers import (
    _busy_intervals,
    _feasible_starts,
    _weight_of,
)
from srbench.benchmarks.calendar_scheduling.loader import load_tasks
from srbench.benchmarks.calendar_scheduling.types import CalendarTask

DATA_DIR = Path(__file__).parents[3] / "data" / "calendar-scheduling"
SOFT_DIR = DATA_DIR / "small_soft"
SOFT_YAML = SOFT_DIR / "tasks.yaml"
LEGACY_YAML = DATA_DIR / "small.yaml"

# The hours the numeric tables score, and so the hours the documents rank.
GRID = [hour * 60 for hour in range(8, 19)]


def _verifier(task_id: int):
    """Return the verifier module that grades a task."""
    package = "srbench.benchmarks.calendar_scheduling.evaluation.preference_adherence.verifiers"
    return importlib.import_module(f"{package}.task_{task_id:03d}")


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


def _numeric_profile(raw_task: dict) -> dict[int, float]:
    """Read a legacy task's numeric preference table as ``{start_minutes: score}``."""
    return {
        to_minutes(preference["start_time"]): preference["score"]
        for preference in raw_task["assistant"]["preferences"]
    }


def _induced_profile(task: CalendarTask) -> dict[int, float]:
    """Score each hour of the grid the way the task's verifier would.

    Args:
        task: The task to score, read for its verifier and its meeting length.
            A preference is a condition on a slot rather than on an instant, so
            the length matters.

    Returns:
        Each grid hour mapped to its share of the highest weight on the day,
        which is the scale the numeric tables use.
    """
    preferences = _verifier(task.id).SOFT_PREFERENCES
    duration = task.requestor.requested_meeting.duration_minutes
    raw = {hour: _weight_of(hour, hour + duration, preferences)[0] for hour in GRID}
    top = max(raw.values())
    return {hour: weight / top for hour, weight in raw.items()}


def _feasible(task: CalendarTask) -> list[int]:
    """Return every start time free on both calendars and inside the bookable day."""
    duration = task.requestor.requested_meeting.duration_minutes
    busy = _busy_intervals(task.assistant.calendar) + _busy_intervals(task.requestor.calendar)
    return _feasible_starts(duration, busy, _verifier(task.id).HARD_CONSTRAINTS)


def _ranked_hours(document: str) -> list[list[int]]:
    """Return the hours each rung of a document's ranking lists, in order."""
    return [
        [to_minutes(hour) for hour in re.findall(r"\d\d:\d\d", line.split("**")[1])]
        for line in document.splitlines()
        if line.startswith("**")
    ]


class TestNothingButThePreferencesChanged:
    """The port reuses ``small.yaml``'s scenarios verbatim."""

    def test_every_task_was_ported(self, soft_raw, legacy_raw):
        assert sorted(soft_raw) == sorted(legacy_raw)

    def test_the_requestor_is_untouched(self, soft_raw, legacy_raw):
        for task_id, soft in soft_raw.items():
            assert soft["requestor"] == legacy_raw[task_id]["requestor"]

    def test_the_assistant_differs_only_in_its_preferences(self, soft_raw, legacy_raw):
        for task_id, soft in soft_raw.items():
            legacy = dict(legacy_raw[task_id]["assistant"])
            legacy.pop("preferences")
            assert {k: v for k, v in soft["assistant"].items() if k != "preference_file"} == legacy


class TestTheDatasetIsWiredUp:
    """Every task points at a document that a verifier grades."""

    def test_every_task_declares_its_own_document(self, soft_tasks):
        for task_id, task in soft_tasks.items():
            assert task.assistant.preference_file == f"preferences/task_{task_id:03d}.md"

    def test_the_loader_inlines_every_document(self, soft_tasks):
        for task in soft_tasks.values():
            assert task.assistant.preference_md
            assert task.assistant.name in task.assistant.preference_md

    def test_no_task_keeps_a_numeric_table_to_fall_back_on(self, soft_tasks):
        for task in soft_tasks.values():
            assert task.assistant.preferences == []

    def test_every_task_has_a_verifier(self, soft_tasks):
        """Importing the verifier package is what registers them, so this proves it happened."""
        for task in soft_tasks.values():
            assert task.assistant.preference_file in registry._VERIFIERS

    def test_every_document_and_verifier_has_its_counterpart(self):
        """Either half alone fails at grading time, which is far too late to notice."""
        on_disk = {f"preferences/{path.name}" for path in (SOFT_DIR / "preferences").glob("*.md")}

        assert on_disk == set(registry._VERIFIERS)


class TestThePortIsFaithful:
    """The documents rank slots exactly as the numeric tables they replace."""

    def test_every_verifier_reproduces_its_numeric_table(self, soft_tasks, legacy_raw):
        """Every hour keeps the score ``small.yaml`` gave it, so no preference was invented."""
        for task_id, task in soft_tasks.items():
            assert _induced_profile(task) == pytest.approx(_numeric_profile(legacy_raw[task_id]))

    def test_the_best_bookable_slot_is_one_the_numeric_table_liked_best(
        self, soft_tasks, legacy_raw
    ):
        """Grading the same day either way picks the same hour, which is the point."""
        for task_id, task in soft_tasks.items():
            numeric = _numeric_profile(legacy_raw[task_id])
            induced = _induced_profile(task)
            hours = [start for start in _feasible(task) if start in numeric]
            best = max(hours, key=lambda hour: induced[hour])

            assert numeric[best] == max(numeric[hour] for hour in hours), task_id


class TestTheDocumentSaysWhatItsVerifierEnforces:
    """The prose and the predicates are two renderings of one ranking."""

    def test_every_document_ranks_every_hour_of_the_bookable_day(self, soft_tasks):
        """An hour the notes never mention is one the assistant cannot reason about."""
        for task in soft_tasks.values():
            listed = [hour for rung in _ranked_hours(task.assistant.preference_md) for hour in rung]

            assert sorted(listed) == GRID, task.id

    def test_hours_ranked_together_score_the_same(self, soft_tasks):
        """A rung that mixed scores would promise the assistant something untrue."""
        for task in soft_tasks.values():
            induced = _induced_profile(task)

            for rung in _ranked_hours(task.assistant.preference_md):
                assert len({induced[hour] for hour in rung}) == 1, (task.id, rung)

    def test_the_rungs_run_from_best_to_worst(self, soft_tasks):
        """The heading says "best first", so a reader may rely on the order."""
        for task in soft_tasks.values():
            induced = _induced_profile(task)
            scores = [induced[rung[0]] for rung in _ranked_hours(task.assistant.preference_md)]

            assert scores == sorted(scores, reverse=True), task.id
            assert len(set(scores)) == len(scores), task.id

    def test_every_document_states_the_bookable_day_its_verifier_enforces(self, soft_tasks):
        """Bookable hours are the document's to declare; unstated, the whole day opens up."""
        stated = f"Bookable {to_hhmm(GRID[0])}-{to_hhmm(GRID[-1] + 60)}."

        for task in soft_tasks.values():
            constraints = _verifier(task.id).HARD_CONSTRAINTS
            duration = task.requestor.requested_meeting.duration_minutes
            allowed = [
                minute
                for minute in range(24 * 60 - duration + 1)
                if all(constraint(minute, minute + duration) for constraint in constraints)
            ]

            assert stated in task.assistant.preference_md, task.id
            assert allowed[0] == GRID[0], task.id
            assert allowed[-1] + duration == GRID[-1] + 60, task.id


class TestEveryTaskStaysSchedulable:
    """Swapping the preferences must not make a task impossible."""

    def test_satisfiable_means_a_feasible_slot_exists(self, soft_tasks):
        """Under numeric preferences this meant free on both calendars; the document's
        hard constraints narrow it further, so the flag has to be rechecked."""
        for task in soft_tasks.values():
            assert task.satisfiable == bool(_feasible(task)), task.id

    def test_no_task_lost_its_bookable_slots_in_the_port(self, soft_tasks):
        """Every task in ``small.yaml`` is satisfiable, and the port keeps it that way."""
        assert all(_feasible(task) for task in soft_tasks.values())
