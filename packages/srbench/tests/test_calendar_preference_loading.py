"""Tests for natural-language preference loading in the calendar task loader.

These cover ``CalendarAssistant.preference_file`` / ``preference_md`` and the
loader step that inlines the referenced Markdown before validation. Nothing
consumes the fields yet, so the tests focus on resolution, error handling, and
leaving numeric-preference tasks alone.
"""

from pathlib import Path

import pytest
import yaml
from srbench.benchmarks.calendar_scheduling.loader import load_tasks

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
