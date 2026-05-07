"""Hashing utilities for marketplace benchmark."""

import hashlib
from pathlib import Path


def compute_file_hash(path: Path) -> str:
    """Compute a SHA-256 hash of a file's contents.

    Args:
        path: Path to the file to hash.

    Returns:
        Hex-encoded SHA-256 digest of the file contents.
    """
    return hashlib.sha256(path.read_bytes()).hexdigest()
