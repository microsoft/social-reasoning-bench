"""Tests for natural-language preference loading in the calendar task loader.

These cover ``CalendarAssistant.preference_file`` / ``preference_md`` and the
loader step that inlines the referenced Markdown before validation. They focus
on path resolution, error handling, and leaving numeric-preference tasks alone.
"""

from pathlib import Path

import pytest
import yaml
from pydantic import ValidationError
from srbench.benchmarks.calendar_scheduling.loader import load_tasks
from srbench.benchmarks.calendar_scheduling.types import CalendarAssistant

DATA_DIR = Path(__file__).parents[3] / "data" / "calendar-scheduling"
SMALL_YAML = DATA_DIR / "small.yaml"

PREFERENCE_TEXT = """# Scheduling preferences

- User prefers meetings in the afternoon, from 1pm onwards.
- User never takes meetings during the noon hour.
"""


def _first_task_data() -> dict:
    """Return the first task of ``small.yaml`` as a raw mapping.

    Building a task by hand would duplicate a large amount of required schema,
    so the shipped dataset is used as a realistic base. This also means the
    tests fail loudly if the task schema drifts.

    Returns:
        The raw task mapping parsed from the shipped small dataset.
    """
    with open(SMALL_YAML) as f:
        return yaml.safe_load(f)["tasks"][0]


def _write_task_yaml(directory: Path, task_data: dict) -> Path:
    """Write a single-task YAML file into ``directory``.

    Args:
        directory: Directory to write ``tasks.yaml`` into.
        task_data: Raw task mapping to serialize.

    Returns:
        Path to the written YAML file.
    """
    yaml_path = directory / "tasks.yaml"
    yaml_path.write_text(yaml.safe_dump({"tasks": [task_data]}), encoding="utf-8")
    return yaml_path


class TestPreferenceFileResolution:
    """The loader inlines ``preference_file`` into ``preference_md``."""

    def test_contents_are_inlined(self, tmp_path: Path):
        """A declared preference file is read verbatim into ``preference_md``."""
        task_data = _first_task_data()
        task_data["assistant"]["preference_file"] = "preference.md"
        (tmp_path / "preference.md").write_text(PREFERENCE_TEXT, encoding="utf-8")
        yaml_path = _write_task_yaml(tmp_path, task_data)

        task = load_tasks([yaml_path]).all_tasks[0]

        assert task.assistant.preference_md == PREFERENCE_TEXT
        assert task.assistant.preference_file == "preference.md"

    def test_path_is_relative_to_the_declaring_yaml(self, tmp_path: Path):
        """Paths resolve against the YAML file, not the process working directory."""
        task_data = _first_task_data()
        task_data["assistant"]["preference_file"] = "preferences/amara_okafor.md"
        (tmp_path / "preferences").mkdir()
        (tmp_path / "preferences" / "amara_okafor.md").write_text(PREFERENCE_TEXT, encoding="utf-8")
        yaml_path = _write_task_yaml(tmp_path, task_data)

        task = load_tasks([yaml_path]).all_tasks[0]

        assert task.assistant.preference_md == PREFERENCE_TEXT

    def test_missing_file_raises(self, tmp_path: Path):
        """A declared but absent preference file fails loudly at load time."""
        task_data = _first_task_data()
        task_data["assistant"]["preference_file"] = "does_not_exist.md"
        yaml_path = _write_task_yaml(tmp_path, task_data)

        with pytest.raises(FileNotFoundError, match="does_not_exist.md"):
            load_tasks([yaml_path])

    def test_preference_text_changes_the_task_hash(self, tmp_path: Path):
        """Editing a preference document invalidates checkpointed runs."""
        hashes = []
        for text in (PREFERENCE_TEXT, PREFERENCE_TEXT + "\n- User prefers short meetings.\n"):
            case_dir = tmp_path / f"case_{len(hashes)}"
            case_dir.mkdir()
            task_data = _first_task_data()
            task_data["assistant"]["preference_file"] = "preference.md"
            (case_dir / "preference.md").write_text(text, encoding="utf-8")
            yaml_path = _write_task_yaml(case_dir, task_data)
            hashes.append(load_tasks([yaml_path]).all_tasks[0].hash)

        assert hashes[0] != hashes[1]


class TestNumericPreferencesAreUntouched:
    """Tasks without a preference file behave exactly as before."""

    def test_absent_field_is_a_no_op(self, tmp_path: Path):
        """Omitting ``preference_file`` leaves ``preference_md`` unset."""
        task_data = _first_task_data()
        yaml_path = _write_task_yaml(tmp_path, task_data)

        task = load_tasks([yaml_path]).all_tasks[0]

        assert task.assistant.preference_file is None
        assert task.assistant.preference_md is None
        assert task.assistant.preferences, "numeric preferences should still load"

    def test_shipped_dataset_still_loads(self):
        """Every task in the shipped small dataset loads with no preference text."""
        tasks = load_tasks([SMALL_YAML]).all_tasks

        assert len(tasks) == 21
        assert all(task.assistant.preference_md is None for task in tasks)
        assert all(task.assistant.preferences for task in tasks)


# Task hashes as produced before ``preference_file`` and ``preference_md``
# existed. These are pinned rather than recomputed because checkpoints written
# by earlier versions are keyed on them: if adding a field changes them, every
# such checkpoint is stranded and silently re-executed.
LEGACY_HASHES = {
    0: "fb8a7ee51b33aeb8",
    1: "6064f2174ece53cd",
    2: "7f65b95913a0a576",
    20: "7eba6a25512ba3ce",
    21: "d8152b8b6e2fec0a",
    22: "db9542fcde9b4a3e",
    40: "26bf3e2a9825fb88",
    41: "2efc1bd948f5f104",
    42: "b146535365e9aae6",
    60: "e87da144e6fb445f",
    61: "98d43cc1a928d923",
    62: "49a75d9a91ba50e6",
    80: "82cb2898e4f9b577",
    81: "289d480d91b82b94",
    82: "9df75f7d56c26b7c",
    100: "60f72b15df746e58",
    101: "b18d786a8e193283",
    102: "61468c9c13428e6b",
    120: "04b3d3cec71f3ded",
    121: "90202537dde466e7",
    122: "8794ab0789d35157",
}


class TestTaskHashesAreStable:
    """The new fields must not change the identity of tasks that lack them."""

    def test_shipped_tasks_hash_as_they_did_before(self):
        """Adding a field must not strand checkpoints keyed on the old hashes."""
        tasks = load_tasks([SMALL_YAML]).all_tasks

        assert {task.id: task.hash for task in tasks} == LEGACY_HASHES

    def test_a_declared_document_is_part_of_the_hash(self, tmp_path: Path):
        """A task graded on prose must not reuse a run graded on other prose."""
        task_data = _first_task_data()
        task_data["assistant"]["preference_file"] = "preferences/p.md"
        (tmp_path / "preferences").mkdir()
        document = tmp_path / "preferences" / "p.md"
        yaml_path = _write_task_yaml(tmp_path, task_data)

        document.write_text(PREFERENCE_TEXT, encoding="utf-8")
        before = load_tasks([yaml_path]).all_tasks[0].hash
        document.write_text("User prefers mornings.\n", encoding="utf-8")
        after = load_tasks([yaml_path]).all_tasks[0].hash

        assert before != after

    def test_declaring_a_document_changes_the_hash(self, tmp_path: Path):
        """A prose-graded task is not the same task as its numeric original."""
        numeric = load_tasks([_write_task_yaml(tmp_path, _first_task_data())]).all_tasks[0]

        soft_dir = tmp_path / "soft"
        (soft_dir / "preferences").mkdir(parents=True)
        (soft_dir / "preferences" / "p.md").write_text(PREFERENCE_TEXT, encoding="utf-8")
        task_data = _first_task_data()
        task_data["assistant"]["preference_file"] = "preferences/p.md"
        soft = load_tasks([_write_task_yaml(soft_dir, task_data)]).all_tasks[0]

        assert numeric.hash != soft.hash


class TestBothPreferenceFieldsTravelTogether:
    """The prompt reads ``preference_md`` but grading keys on ``preference_file``."""

    def test_an_empty_document_is_rejected(self, tmp_path: Path):
        """Otherwise the task is graded on preferences it never showed."""
        task_data = _first_task_data()
        task_data["assistant"]["preference_file"] = "preferences/p.md"
        (tmp_path / "preferences").mkdir()
        (tmp_path / "preferences" / "p.md").write_text("   \n", encoding="utf-8")
        yaml_path = _write_task_yaml(tmp_path, task_data)

        with pytest.raises(ValidationError, match="must be set together"):
            load_tasks([yaml_path])

    def test_prose_without_a_document_path_is_rejected(self):
        """``preference_md`` alone would be shown to the agent but never graded."""
        assistant = _first_task_data()["assistant"]
        assistant["preference_md"] = PREFERENCE_TEXT

        with pytest.raises(ValidationError, match="must be set together"):
            CalendarAssistant.model_validate(assistant)
