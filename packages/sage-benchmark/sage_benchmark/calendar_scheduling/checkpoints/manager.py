"""Checkpoint manager for resumable calendar benchmark runs."""

from __future__ import annotations

from typing import TYPE_CHECKING

from sage_benchmark.shared.checkpoints import BaseCheckpointManager

from ..types import TaskEvaluationResult, TaskExecutionResult
from .data import CheckpointData
from .run_config import RunConfig

if TYPE_CHECKING:
    from ..types import BenchmarkMetadata


class CheckpointManager(
    BaseCheckpointManager[TaskExecutionResult, TaskEvaluationResult, CheckpointData]
):
    """Calendar-scheduling checkpoint manager."""

    _data_cls = CheckpointData

    def initialize(
        self,
        config: RunConfig,
        metadata: BenchmarkMetadata,
        source_file_hashes: dict[str, str],
    ) -> None:
        """Initialize a new checkpoint.

        Args:
            config: Run configuration (CLI options)
            metadata: Benchmark run metadata
            source_file_hashes: Map of source file path to sha256 hash
        """
        self._data = CheckpointData(
            config=config,
            metadata=metadata,
            source_file_hashes=source_file_hashes,
        )
        self._completed_task_keys = set()
        self._completed_eval_keys = set()
        self.save()

    def get_config(self) -> RunConfig | None:
        """Get the run configuration from checkpoint."""
        if self._data is None:
            return None
        return self._data.config

    @staticmethod
    def _get_eval_task_key(result: TaskEvaluationResult) -> str:
        """Calendar eval results store the key on ``result.execution.task_key``."""
        return result.execution.task_key
