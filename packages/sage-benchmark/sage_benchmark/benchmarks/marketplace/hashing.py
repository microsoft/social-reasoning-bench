"""Hashing utilities for marketplace benchmark."""

import hashlib
from pathlib import Path


def compute_file_hash(path: Path) -> str:
    """Compute a SHA-256 hash of a file's contents."""
    return hashlib.sha256(path.read_bytes()).hexdigest()
