"""Checkpoint manager for resumable form-filling benchmark runs."""

from sage_benchmark.shared.checkpoints import BaseCheckpointManager

from ..schemas import InteractiveTaskEvaluationResult, InteractiveTaskExecutionResult
from .data import CheckpointData


class CheckpointManager(
    BaseCheckpointManager[
        InteractiveTaskExecutionResult, InteractiveTaskEvaluationResult, CheckpointData
    ]
):
    """Form-filling checkpoint manager."""

    _data_cls = CheckpointData

    @staticmethod
    def _get_exec_task_key(result: InteractiveTaskExecutionResult) -> str:
        """Extract task key from an execution result."""
        return result.form_id

    @staticmethod
    def _get_eval_task_key(result: InteractiveTaskEvaluationResult) -> str:
        """Extract task key from an evaluation result."""
        return result.form_id

    def initialize(self) -> None:
        """Initialize a new (empty) checkpoint."""
        self._data = CheckpointData()
        self._completed_task_keys = set()
        self._completed_eval_keys = set()
        self.save()
