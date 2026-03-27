"""Checkpoint manager for resumable marketplace benchmark runs."""

from __future__ import annotations

from sage_benchmark.shared.checkpoints import BaseCheckpointManager

from ..types import TaskEvaluationResult, TaskExecutionResult
from .data import CheckpointData
from .run_config import RunConfig


class CheckpointManager(
    BaseCheckpointManager[TaskExecutionResult, TaskEvaluationResult, CheckpointData]
):
    """Marketplace checkpoint manager."""

    _data_cls = CheckpointData

    def initialize(
        self,
        config: RunConfig,
        source_file_hashes: dict[str, str],
    ) -> None:
        """Initialize a new checkpoint.

        Args:
            config: Run configuration (CLI options)
            source_file_hashes: Map of source file path to sha256 hash
        """
        self._data = CheckpointData(
            config=config,
            source_file_hashes=source_file_hashes,
        )
        self._completed_task_keys = set()
        self._completed_eval_keys = set()
        self.save()

    def add_result(
        self, exec_result: TaskExecutionResult, eval_result: TaskEvaluationResult
    ) -> None:
        """Add a completed execution+evaluation result pair and save checkpoint."""
        if self._data is None:
            return

        self._data.execution_results.append(exec_result)
        self._data.evaluation_results.append(eval_result)
        task_key = exec_result.task_key
        self._data.completed_task_keys.append(task_key)
        self._data.completed_eval_keys.append(task_key)
        self._completed_task_keys.add(task_key)
        self._completed_eval_keys.add(task_key)
        self.save()

    def get_completed_keys(self) -> set[str]:
        """Get set of completed execution task keys.

        Alias kept for backward compatibility with existing marketplace callers.
        """
        return self.get_completed_task_keys()

    def get_config(self) -> RunConfig | None:
        """Get the run configuration from checkpoint."""
        if self._data is None:
            return None
        return self._data.config
