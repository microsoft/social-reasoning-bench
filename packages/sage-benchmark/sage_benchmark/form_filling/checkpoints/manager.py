"""Checkpoint manager for resumable form-filling benchmark runs."""

import logging
from datetime import datetime
from pathlib import Path

from pydantic_core import to_json

from ..schemas import InteractiveTaskEvaluationResult, InteractiveTaskExecutionResult
from .data import CheckpointData

logger = logging.getLogger(__name__)


class CheckpointManager:
    """Manages checkpoint save/load operations for form-filling benchmarks."""

    def __init__(self, checkpoint_path: Path, enabled: bool = True):
        """Initialize the checkpoint manager.

        Args:
            checkpoint_path: Path to the checkpoint file
            enabled: Whether checkpointing is enabled
        """
        self.checkpoint_path = checkpoint_path
        self.enabled = enabled
        self._data: CheckpointData | None = None
        self._completed_task_keys: set[str] = set()
        self._completed_eval_keys: set[str] = set()

    def load(self) -> CheckpointData | None:
        """Load existing checkpoint if it exists.

        Returns:
            CheckpointData if checkpoint exists, None otherwise
        """
        if not self.checkpoint_path.exists():
            return None

        try:
            content = self.checkpoint_path.read_text()
            self._data = CheckpointData.model_validate_json(content)
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

        # Write to temp file, then rename for atomicity
        temp_path = self.checkpoint_path.with_suffix(".tmp")
        temp_path.write_bytes(to_json(self._data, indent=2))
        temp_path.rename(self.checkpoint_path)

    def initialize(self) -> None:
        """Initialize a new (empty) checkpoint."""
        self._data = CheckpointData()
        self._completed_task_keys = set()
        self._completed_eval_keys = set()
        self.save()

    def add_execution_result(self, result: InteractiveTaskExecutionResult) -> None:
        """Add an execution result and save checkpoint."""
        if self._data is None:
            return

        task_key = result.form_id
        self._data.execution_results.append(result)
        self._data.completed_task_keys.append(task_key)
        self._completed_task_keys.add(task_key)
        self.save()

    def add_evaluation_result(self, result: InteractiveTaskEvaluationResult) -> None:
        """Add an evaluation result and save checkpoint."""
        if self._data is None:
            return

        task_key = result.form_id
        self._data.evaluation_results.append(result)
        self._data.completed_eval_keys.append(task_key)
        self._completed_eval_keys.add(task_key)
        self.save()

    def set_interrupted(self, interrupted: bool = True) -> None:
        """Mark the run as interrupted."""
        if self._data is not None:
            self._data.interrupted = interrupted
            self.save()

    def get_completed_task_keys(self) -> set[str]:
        """Get set of completed execution task keys (form_ids)."""
        return self._completed_task_keys.copy()

    def get_completed_eval_keys(self) -> set[str]:
        """Get set of completed evaluation task keys (form_ids)."""
        return self._completed_eval_keys.copy()

    def get_execution_results(self) -> list[InteractiveTaskExecutionResult]:
        """Get list of completed execution results."""
        if self._data is None:
            return []
        return list(self._data.execution_results)

    def get_evaluation_results(self) -> list[InteractiveTaskEvaluationResult]:
        """Get list of completed evaluation results."""
        if self._data is None:
            return []
        return list(self._data.evaluation_results)

    def cleanup(self) -> None:
        """Remove checkpoint file after successful completion."""
        if self.checkpoint_path.exists():
            self.checkpoint_path.unlink()
            logger.info("Removed checkpoint file")
