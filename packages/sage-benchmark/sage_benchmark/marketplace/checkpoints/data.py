"""Checkpoint data model for resumable marketplace benchmark runs."""

from pydantic import Field

from sage_benchmark.shared.checkpoints import BaseCheckpointData

from ..types import TaskEvaluationResult, TaskExecutionResult
from .run_config import RunConfig


class CheckpointData(BaseCheckpointData[TaskExecutionResult, TaskEvaluationResult]):
    """Checkpoint state for resumable marketplace benchmark runs."""

    config: RunConfig | None = Field(
        default=None,
        description="Run configuration for resuming with same options",
    )
    # Keys are absolute file paths, values are sha256 hashes
    source_file_hashes: dict[str, str] = Field(
        default_factory=dict,
        description="Map of source filename to sha256 hash",
    )
