"""Checkpoint data model for resumable form-filling benchmark runs."""

from sage_benchmark.shared.checkpoints import BaseCheckpointData

from ..schemas import InteractiveTaskEvaluationResult, InteractiveTaskExecutionResult


class CheckpointData(
    BaseCheckpointData[InteractiveTaskExecutionResult, InteractiveTaskEvaluationResult]
):
    """Checkpoint state for resumable form-filling benchmark runs."""

    pass
