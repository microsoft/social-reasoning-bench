"""Content hashing utilities for checkpoint deduplication.

Every benchmark MUST have a ``checkpoints/hashing.py`` module that
provides these two functions. The loader imports them to compute
task and file hashes.

Task hashes enable deterministic resume: the same logical task always
produces the same hash, so the checkpoint manager can detect which
tasks have already been executed/evaluated.

File hashes enable change detection: if a source data file changes
between runs, the checkpoint manager can warn or refuse to resume.

Form-filling extends the base task hash to include the form_model.py
source, so changes to either the task data or the form schema produce
a different hash.
"""

from __future__ import annotations

import hashlib
from pathlib import Path


def compute_file_hash(path: Path) -> str:
    """SHA256 hash of a file's raw bytes for change detection.

    Args:
        path: Path to the file to hash.

    Returns:
        Hex-encoded SHA256 digest string.
    """
    return hashlib.sha256(path.read_bytes()).hexdigest()
