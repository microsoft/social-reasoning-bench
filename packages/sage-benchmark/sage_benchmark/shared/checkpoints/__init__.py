"""Shared checkpoint infrastructure for resumable benchmark runs."""

from .data import BaseCheckpointData
from .manager import BaseCheckpointManager

__all__ = [
    "BaseCheckpointData",
    "BaseCheckpointManager",
]
