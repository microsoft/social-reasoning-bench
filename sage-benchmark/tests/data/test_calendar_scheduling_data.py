from pathlib import Path

import pytest
from sage_benchmark.calendar_scheduling.loader import load_calendar_tasks
from sage_benchmark.calendar_scheduling.types import CalendarTask

# Path to data directory relative to project root
DATA_DIR = Path(__file__).parent.parent.parent / "data" / "calendar-scheduling"


def get_yaml_files() -> list[Path]:
    """Get all YAML files in the calendar-scheduling data directory."""
    return list(DATA_DIR.glob("*.yaml"))


@pytest.mark.parametrize("yaml_file", get_yaml_files(), ids=lambda p: p.name)
def test_calendar_scheduling_data_loads(yaml_file: Path) -> None:
    """Test that each YAML file can be loaded by the calendar scheduling loader."""
    tasks = load_calendar_tasks(yaml_file)

    # Validate return type
    assert isinstance(tasks, list)
    assert len(tasks) > 0, f"Expected at least one task in {yaml_file.name}"

    # Validate each task is a CalendarTask instance
    for task in tasks:
        assert isinstance(task, CalendarTask)
