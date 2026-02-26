import hashlib
from collections.abc import Sequence
from pathlib import Path

import yaml

from .types import KeyedMarketplaceTask, LoadedFile, LoadedFiles, MarketplaceTask


def _compute_file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _compute_task_key(task: MarketplaceTask) -> str:
    content = task.model_dump_json(exclude_none=True)
    return hashlib.sha256(content.encode()).hexdigest()[:16]


def _load_file(path: Path) -> LoadedFile:
    with open(path) as f:
        data = yaml.safe_load(f) or {}

    if "tasks" not in data:
        raise ValueError(f"{path}: YAML file must contain 'tasks'")

    seen_ids: set[int] = set()
    tasks: list[KeyedMarketplaceTask] = []
    for raw_task in data["tasks"]:
        task = MarketplaceTask(**raw_task)
        if task.id in seen_ids:
            raise ValueError(f"Duplicate task id {task.id} in {path}")
        seen_ids.add(task.id)
        tasks.append(KeyedMarketplaceTask(**task.model_dump(), task_key=_compute_task_key(task)))

    return LoadedFile(path=str(path.absolute()), hash=_compute_file_hash(path), tasks=tasks)


def load_tasks(paths: Sequence[str | Path], limit: int | None = None) -> LoadedFiles:
    loaded_files: list[LoadedFile] = []
    for raw_path in paths:
        path = Path(raw_path)
        if path.is_dir():
            for candidate in sorted(list(path.glob("*.yaml")) + list(path.glob("*.yml"))):
                loaded_files.append(_load_file(candidate))
        else:
            loaded_files.append(_load_file(path))

    all_ids: set[int] = set()
    for loaded_file in loaded_files:
        for task in loaded_file.tasks:
            if task.id in all_ids:
                raise ValueError(f"Duplicate task id {task.id} across files")
            all_ids.add(task.id)

    if limit is None:
        return LoadedFiles(files=loaded_files)

    limited: list[LoadedFile] = []
    remaining = limit
    for loaded_file in loaded_files:
        if remaining <= 0:
            break
        take = min(remaining, len(loaded_file.tasks))
        limited.append(
            LoadedFile(
                path=loaded_file.path,
                hash=loaded_file.hash,
                tasks=loaded_file.tasks[:take],
            )
        )
        remaining -= take
    return LoadedFiles(files=limited)
