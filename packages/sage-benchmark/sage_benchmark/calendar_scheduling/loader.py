import json
from collections.abc import Sequence
from pathlib import Path

import yaml
from pydantic import TypeAdapter

from .checkpoints import compute_file_hash, compute_task_key
from .types import (
    Artifact,
    CalendarTask,
    KeyedCalendarTask,
    LoadedFile,
    LoadedFiles,
)


def _load_file(yaml_path: Path) -> LoadedFile:
    """Load a single YAML file with content-based task keys."""
    abs_path = str(yaml_path.absolute())
    file_hash = compute_file_hash(yaml_path)

    with open(yaml_path) as f:
        data = yaml.safe_load(f)

    if "tasks" not in data:
        raise ValueError("YAML file must contain a 'tasks' key")

    keyed_tasks: list[KeyedCalendarTask] = []
    seen_ids: set[int] = set()
    for task_data in data["tasks"]:
        task = CalendarTask(**task_data)
        if task.id in seen_ids:
            raise ValueError(f"Duplicate task id {task.id} in {yaml_path}")
        seen_ids.add(task.id)
        task_key = compute_task_key(task)
        keyed_task = KeyedCalendarTask(**task.model_dump(), task_key=task_key)
        keyed_tasks.append(keyed_task)

    return LoadedFile(path=abs_path, hash=file_hash, tasks=keyed_tasks)


def load_tasks(
    paths: Sequence[str | Path],
    limit: int | None = None,
) -> LoadedFiles:
    """Load tasks from YAML files or directories.

    Args:
        paths: List of YAML files or directories containing task definitions
        limit: Optional limit on number of tasks to load

    Returns:
        LoadedFiles containing files with their paths, hashes, and tasks.
        Use .all_tasks for flat task list, .file_hashes for hash dict.
    """
    loaded_files: list[LoadedFile] = []

    for path in paths:
        path = Path(path)
        if path.is_dir():
            yaml_files = list(path.glob("*.yaml")) + list(path.glob("*.yml"))
            for yaml_file in yaml_files:
                loaded_files.append(_load_file(yaml_file))
        else:
            loaded_files.append(_load_file(path))

    # Validate uniqueness across all loaded files
    all_ids: set[int] = set()
    for f in loaded_files:
        for task in f.tasks:
            if task.id in all_ids:
                raise ValueError(f"Duplicate task id {task.id} across files (found in {f.path})")
            all_ids.add(task.id)

    result = LoadedFiles(files=loaded_files)

    # Apply limit if specified (need to rebuild with limited tasks)
    if limit is not None:
        limited_files: list[LoadedFile] = []
        remaining = limit
        for f in loaded_files:
            if remaining <= 0:
                break
            take = min(remaining, len(f.tasks))
            limited_files.append(LoadedFile(path=f.path, hash=f.hash, tasks=f.tasks[:take]))
            remaining -= take
        result = LoadedFiles(files=limited_files)

    return result


def load_artifacts(json_path: str | Path) -> dict[int, list[Artifact]]:
    """Load artifacts from a JSON file.

    Args:
        json_path: Path to the artifacts JSON file

    Returns:
        Dict mapping task_id to list of Artifact objects
    """
    with open(json_path) as f:
        data = json.load(f)

    artifact_adapter = TypeAdapter(Artifact)
    result: dict[int, list[Artifact]] = {}
    for task_artifacts in data.get("task_artifacts", []):
        task_id = task_artifacts["task_id"]
        artifacts = [artifact_adapter.validate_python(a) for a in task_artifacts["artifacts"]]
        result[task_id] = artifacts

    return result


# Backward compatibility alias
load_calendar_tasks = load_tasks
