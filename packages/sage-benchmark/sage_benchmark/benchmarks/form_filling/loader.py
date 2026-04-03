"""Task loader for form-filling benchmark.

Loads form tasks from YAML files (matching calendar/marketplace pattern).
Satellite files (form_model.py, images) live in a sibling ``forms/`` directory.
"""

from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path

import yaml

from .hashing import compute_file_hash
from .types import (
    FormFillingLoadedFile,
    FormFillingLoadedFiles,
    FormTask,
)

DEFAULT_FORMS_DIR_NAME = "forms"


def _resolve_form_model_path(yaml_dir: Path, task: FormTask) -> str:
    """Resolve form_model.py path from the sibling forms/ directory."""
    forms_dir = yaml_dir / DEFAULT_FORMS_DIR_NAME
    form_model = forms_dir / f"form_{task.id}" / "form_model.py"
    return str(form_model) if form_model.exists() else ""


def _load_file(yaml_path: Path) -> FormFillingLoadedFile:
    """Load a single YAML file containing form-filling tasks."""
    abs_path = str(yaml_path.absolute())
    file_hash = compute_file_hash(yaml_path)
    yaml_dir = yaml_path.parent

    with open(yaml_path) as f:
        data = yaml.safe_load(f)

    if "tasks" not in data:
        raise ValueError(f"YAML file must contain a 'tasks' key: {yaml_path}")

    tasks: list[FormTask] = []
    seen_ids: set[int] = set()
    for task_data in data["tasks"]:
        task = FormTask.model_validate(task_data)
        if task.id in seen_ids:
            raise ValueError(f"Duplicate task id {task.id} in {yaml_path}")
        seen_ids.add(task.id)
        task = task.model_copy(update={"form_model_path": _resolve_form_model_path(yaml_dir, task)})
        tasks.append(task)

    return FormFillingLoadedFile(path=abs_path, hash=file_hash, tasks=tasks)


def load_tasks(
    paths: Sequence[str | Path],
    limit: int | None = None,
) -> FormFillingLoadedFiles:
    """Load form tasks from YAML files or directories.

    Args:
        paths: List of YAML files or directories containing task YAMLs.
        limit: Optional limit on number of tasks to load.

    Returns:
        FormFillingLoadedFiles with .all_tasks and .file_hashes.
    """
    loaded_files: list[FormFillingLoadedFile] = []

    for path in paths:
        path = Path(path)
        if path.is_dir():
            yaml_files = sorted(list(path.glob("*.yaml")) + list(path.glob("*.yml")))
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

    result = FormFillingLoadedFiles(files=loaded_files)

    # Apply limit if specified
    if limit is not None:
        limited_files: list[FormFillingLoadedFile] = []
        remaining = limit
        for f in loaded_files:
            if remaining <= 0:
                break
            take = min(remaining, len(f.tasks))
            limited_files.append(
                FormFillingLoadedFile(path=f.path, hash=f.hash, tasks=f.tasks[:take])
            )
            remaining -= take
        result = FormFillingLoadedFiles(files=limited_files)

    return result
