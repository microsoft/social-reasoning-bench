"""Content hashing utilities for checkpointing."""

import hashlib
from pathlib import Path

from .types import CalendarTask


def compute_task_hash(task: CalendarTask) -> str:
    """Compute content hash for a task.

    Args:
        task: The CalendarTask to hash

    Returns:
        First 16 characters of the sha256 hash of the task's JSON representation
    """
    content = task.model_dump_json(exclude_none=False, exclude={"hash"})
    return hashlib.sha256(content.encode()).hexdigest()[:16]


def compute_file_hash(path: Path) -> str:
    """Compute hash of a file's contents for auditability.

    Args:
        path: Path to the file to hash

    Returns:
        Full sha256 hash of the file contents
    """
    return hashlib.sha256(path.read_bytes()).hexdigest()
