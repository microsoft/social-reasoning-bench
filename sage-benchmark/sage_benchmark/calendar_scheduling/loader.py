import json
from pathlib import Path

import yaml
from pydantic import TypeAdapter

from .types import Artifact, CalendarTask


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


def load_artifacts(json_path: str | Path) -> dict[int, list[Artifact]]:
    """Load artifacts from a JSON file.

    Args:
        json_path: Path to the artifacts JSON file

    Returns:
        Dict mapping task_index to list of Artifact objects
    """
    with open(json_path) as f:
        data = json.load(f)

    artifact_adapter = TypeAdapter(Artifact)
    result: dict[int, list[Artifact]] = {}
    for task_artifacts in data.get("task_artifacts", []):
        task_index = task_artifacts["task_index"]
        artifacts = [artifact_adapter.validate_python(a) for a in task_artifacts["artifacts"]]
        result[task_index] = artifacts

    return result
