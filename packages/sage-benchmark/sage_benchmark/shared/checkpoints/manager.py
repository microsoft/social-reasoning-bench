"""Generic checkpoint manager for resumable benchmark runs."""

from __future__ import annotations

import logging
from datetime import datetime
from pathlib import Path
from typing import Generic, TypeVar

from pydantic import BaseModel
from pydantic_core import to_json

from .data import BaseCheckpointData

logger = logging.getLogger(__name__)

TExec = TypeVar("TExec", bound=BaseModel)
TEval = TypeVar("TEval", bound=BaseModel)
TData = TypeVar("TData", bound=BaseCheckpointData)  # type: ignore[type-arg]


class BaseCheckpointManager(Generic[TExec, TEval, TData]):
    """Generic checkpoint manager for resumable benchmark runs.

    Subclasses must set :pyattr:`_data_cls` to the concrete
    :class:`BaseCheckpointData` subclass used for deserialisation, and may
    override :meth:`_get_eval_task_key` when the evaluation result type does
    not carry ``task_key`` directly.
    """

    _data_cls: type[TData]
    """Concrete CheckpointData class used for ``model_validate_json``."""

    def __init__(self, checkpoint_path: Path, enabled: bool = True):
        """Initialize the checkpoint manager.

        Args:
            checkpoint_path: Path to the checkpoint file
            enabled: Whether checkpointing is enabled
        """
        self.checkpoint_path = checkpoint_path
        self.enabled = enabled
        self._data: TData | None = None
        self._completed_task_keys: set[str] = set()
        self._completed_eval_keys: set[str] = set()

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------

    def load(self) -> TData | None:
        """Load existing checkpoint if it exists.

        Returns:
            Checkpoint data if checkpoint exists, ``None`` otherwise.
        """
        if not self.checkpoint_path.exists():
            return None

        try:
            content = self.checkpoint_path.read_text()
            self._data = self._data_cls.model_validate_json(content)
            self._completed_task_keys = set(self._data.completed_task_keys)
            self._completed_eval_keys = set(self._data.completed_eval_keys)
            logger.info(
                "Loaded checkpoint: %d executions, %d evaluations completed",
                len(self._completed_task_keys),
                len(self._completed_eval_keys),
            )
            return self._data
        except Exception as e:
            logger.warning("Failed to load checkpoint: %s", e)
            return None

    def save(self) -> None:
        """Atomically save checkpoint data."""
        if not self.enabled or self._data is None:
            return

        self._data.last_updated = datetime.now().isoformat()

        # Ensure parent directory exists, then write atomically via temp file.
        self.checkpoint_path.parent.mkdir(parents=True, exist_ok=True)
        temp_path = self.checkpoint_path.with_suffix(".tmp")
        temp_path.write_bytes(to_json(self._data, indent=2))
        temp_path.rename(self.checkpoint_path)

    def cleanup(self) -> None:
        """Remove checkpoint file after successful completion."""
        if self.checkpoint_path.exists():
            self.checkpoint_path.unlink()
            logger.info("Removed checkpoint file")

    # ------------------------------------------------------------------
    # Mutation helpers
    # ------------------------------------------------------------------

    def add_execution_result(self, result: TExec) -> None:
        """Add an execution result and save checkpoint."""
        if self._data is None:
            return

        self._data.execution_results.append(result)
        task_key = self._get_exec_task_key(result)
        self._data.completed_task_keys.append(task_key)
        self._completed_task_keys.add(task_key)
        self.save()

    def add_evaluation_result(self, result: TEval) -> None:
        """Add an evaluation result and save checkpoint."""
        if self._data is None:
            return

        self._data.evaluation_results.append(result)
        task_key = self._get_eval_task_key(result)
        self._data.completed_eval_keys.append(task_key)
        self._completed_eval_keys.add(task_key)
        self.save()

    def set_interrupted(self, interrupted: bool = True) -> None:
        """Mark the run as interrupted."""
        if self._data is not None:
            self._data.interrupted = interrupted
            self.save()

    # ------------------------------------------------------------------
    # Read helpers
    # ------------------------------------------------------------------

    def get_completed_task_keys(self) -> set[str]:
        """Get set of completed execution task keys."""
        return self._completed_task_keys.copy()

    def get_completed_eval_keys(self) -> set[str]:
        """Get set of completed evaluation task keys."""
        return self._completed_eval_keys.copy()

    def get_execution_results(self) -> list[TExec]:
        """Get list of completed execution results."""
        if self._data is None:
            return []
        return list(self._data.execution_results)

    def get_evaluation_results(self) -> list[TEval]:
        """Get list of completed evaluation results."""
        if self._data is None:
            return []
        return list(self._data.evaluation_results)

    # ------------------------------------------------------------------
    # Hook for subclasses
    # ------------------------------------------------------------------

    @staticmethod
    def _get_exec_task_key(result: TExec) -> str:  # type: ignore[type-var]
        """Extract the task key from an execution result.

        Override in subclasses when the execution result stores the key
        under a different attribute (e.g. ``result.form_id``).
        """
        return result.task_key  # type: ignore[attr-defined, return-value]

    @staticmethod
    def _get_eval_task_key(result: TEval) -> str:  # type: ignore[type-var]
        """Extract the task key from an evaluation result.

        Override in subclasses when the evaluation result stores the key
        under a different attribute (e.g. ``result.execution.task_key``).
        """
        return result.task_key  # type: ignore[attr-defined, return-value]
