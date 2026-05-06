from collections.abc import Sequence
from pathlib import Path

import yaml

from .hashing import compute_file_hash
from .types import (
    CalendarLoadedFile,
    CalendarLoadedFiles,
    CalendarTask,
)


def _load_file(yaml_path: Path) -> CalendarLoadedFile:
    """Load a single YAML file with content-based task keys.

    Args:
        yaml_path: Path to the YAML file containing task definitions under
            a top-level ``tasks`` key.

    Returns:
        A ``CalendarLoadedFile`` with the absolute path, content hash,
        and parsed tasks.

    Raises:
        ValueError: If the YAML file is missing a ``tasks`` key or contains
            duplicate task IDs.
    """
    abs_path = str(yaml_path.absolute())
    file_hash = compute_file_hash(yaml_path)

    with open(yaml_path) as f:
        data = yaml.safe_load(f)

    if "tasks" not in data:
        raise ValueError("YAML file must contain a 'tasks' key")

    tasks: list[CalendarTask] = []
    seen_ids: set[int] = set()
    for task_data in data["tasks"]:
        task = CalendarTask.model_validate(task_data)
        if task.id in seen_ids:
            raise ValueError(f"Duplicate task id {task.id} in {yaml_path}")
        seen_ids.add(task.id)
        tasks.append(task)

    return CalendarLoadedFile(path=abs_path, hash=file_hash, tasks=tasks)


def load_tasks(
    paths: Sequence[str | Path],
    limit: int | None = None,
) -> CalendarLoadedFiles:
    """Load tasks from YAML files or directories.

    Args:
        paths: List of YAML files or directories containing task definitions
        limit: Optional limit on number of tasks to load

    Returns:
        CalendarLoadedFiles containing files with their paths, hashes, and tasks.
        Use .all_tasks for flat task list, .file_hashes for hash dict.
    """
    loaded_files: list[CalendarLoadedFile] = []

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

    result = CalendarLoadedFiles(files=loaded_files)

    # Apply limit if specified (need to rebuild with limited tasks)
    if limit is not None:
        limited_files: list[CalendarLoadedFile] = []
        remaining = limit
        for f in loaded_files:
            if remaining <= 0:
                break
            take = min(remaining, len(f.tasks))
            limited_files.append(CalendarLoadedFile(path=f.path, hash=f.hash, tasks=f.tasks[:take]))
            remaining -= take
        result = CalendarLoadedFiles(files=limited_files)

    return result
