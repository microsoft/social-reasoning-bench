from pathlib import Path

import yaml

from .types import CalendarTask


def load_calendar_tasks(yaml_path: str | Path) -> list[CalendarTask]:
    """
    Load calendar tasks from a YAML file.

    Args:
        yaml_path: Path to the YAML file containing calendar tasks

    Returns:
        List of validated CalendarTask objects
    """
    with open(yaml_path) as f:
        data = yaml.safe_load(f)

    if "tasks" not in data:
        raise ValueError("YAML file must contain a 'tasks' key")

    return [CalendarTask(**task) for task in data["tasks"]]


if __name__ == "__main__":
    tasks = load_calendar_tasks("calendar-tasks.yaml")
    print(f"Loaded {len(tasks)} calendar tasks\n")
    for i, task in enumerate(tasks, 1):
        print(f"{'=' * 80}")
        print(f"Task {i}")
        print(f"{'=' * 80}")
        print(task.model_dump_json(indent=2))
        print()
