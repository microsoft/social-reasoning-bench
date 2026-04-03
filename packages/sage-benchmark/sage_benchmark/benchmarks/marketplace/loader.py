from collections.abc import Sequence
from pathlib import Path

import yaml

from .hashing import compute_file_hash
from .types import MarketplaceLoadedFile, MarketplaceLoadedFiles, MarketplaceTask


def _load_file(path: Path) -> MarketplaceLoadedFile:
    with open(path) as f:
        data = yaml.safe_load(f) or {}

    if "tasks" not in data:
        raise ValueError(f"{path}: YAML file must contain 'tasks'")

    seen_keys: set[tuple[int, str | None]] = set()
    tasks: list[MarketplaceTask] = []
    for raw_task in data["tasks"]:
        task = MarketplaceTask.model_validate(raw_task)
        key = (task.id, task.variant)
        if key in seen_keys:
            raise ValueError(f"Duplicate task (id={task.id}, variant={task.variant}) in {path}")
        seen_keys.add(key)
        tasks.append(task)

    return MarketplaceLoadedFile(
        path=str(path.absolute()), hash=compute_file_hash(path), tasks=tasks
    )


def load_tasks(paths: Sequence[str | Path], limit: int | None = None) -> MarketplaceLoadedFiles:
    loaded_files: list[MarketplaceLoadedFile] = []
    for raw_path in paths:
        path = Path(raw_path)
        if path.is_dir():
            for candidate in sorted(list(path.glob("*.yaml")) + list(path.glob("*.yml"))):
                loaded_files.append(_load_file(candidate))
        else:
            loaded_files.append(_load_file(path))

    all_keys: set[tuple[int, str | None]] = set()
    for loaded_file in loaded_files:
        for task in loaded_file.tasks:
            key = (task.id, task.variant)
            if key in all_keys:
                raise ValueError(
                    f"Duplicate task (id={task.id}, variant={task.variant}) across files"
                )
            all_keys.add(key)

    if limit is None:
        return MarketplaceLoadedFiles(files=loaded_files)

    limited: list[MarketplaceLoadedFile] = []
    remaining = limit
    for loaded_file in loaded_files:
        if remaining <= 0:
            break
        take = min(remaining, len(loaded_file.tasks))
        limited.append(
            MarketplaceLoadedFile(
                path=loaded_file.path,
                hash=loaded_file.hash,
                tasks=loaded_file.tasks[:take],
            )
        )
        remaining -= take
    return MarketplaceLoadedFiles(files=limited)
