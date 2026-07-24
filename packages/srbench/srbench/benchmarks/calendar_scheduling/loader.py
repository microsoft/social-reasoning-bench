from collections.abc import Sequence
from pathlib import Path

import yaml

from .hashing import compute_file_hash
from .types import (
    CalendarLoadedFile,
    CalendarLoadedFiles,
    CalendarTask,
)


def _resolve_preference_md(task_data: dict, yaml_path: Path) -> dict:
    """Inline the assistant's ``preference_file`` contents into the task data.

    ``CalendarTask`` is frozen, so the Markdown must be attached before
    validation. Doing it here also folds the preference text into the task
    content hash used for checkpoint dedup.

    Args:
        task_data: Raw task mapping parsed from YAML.
        yaml_path: Path to the YAML file, used to resolve relative references.

    Returns:
        The task mapping with ``assistant.preference_md`` populated when a
        ``preference_file`` is declared.

    Raises:
        FileNotFoundError: If the referenced preference file does not exist.
    """
    assistant = task_data.get("assistant")
    if not isinstance(assistant, dict):
        return task_data

    preference_file = assistant.get("preference_file")
    if not preference_file:
        return task_data

    preference_path = (yaml_path.parent / preference_file).resolve()
    if not preference_path.is_file():
        raise FileNotFoundError(
            f"preference_file '{preference_file}' referenced by task "
            f"{task_data.get('id')} in {yaml_path} does not exist "
            f"(resolved to {preference_path})"
        )

    return {
        **task_data,
        "assistant": {**assistant, "preference_md": preference_path.read_text().strip()},
    }


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
        task = CalendarTask.model_validate(_resolve_preference_md(task_data, yaml_path))
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
