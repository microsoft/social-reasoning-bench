from pathlib import Path

import yaml

from .schemas import FormTask


def load_form_tasks(yaml_path: str | Path) -> list[FormTask]:
    """
    Load form tasks from a YAML file.

    Args:
        yaml_path: Path to the YAML file containing form tasks

    Returns:
        List of validated FormTask objects
    """
    with open(yaml_path) as f:
        data = yaml.safe_load(f)

    if "tasks" not in data:
        raise ValueError("YAML file must contain a 'tasks' key")

    return [FormTask(**task) for task in data["tasks"]]


if __name__ == "__main__":
    tasks = load_form_tasks("form-tasks.yaml")
    print(f"Loaded {len(tasks)} form tasks\n")
    for i, task in enumerate(tasks, 1):
        print(f"{'=' * 80}")
        print(f"Task {i}")
        print(f"{'=' * 80}")
        print(task.model_dump_json(indent=2))
        print()
