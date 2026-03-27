"""Checkpoint data model for resumable calendar benchmark runs."""

from pydantic import Field

from sage_benchmark.shared.checkpoints import BaseCheckpointData

from ..types import BenchmarkMetadata, TaskEvaluationResult, TaskExecutionResult
from .run_config import RunConfig


class CheckpointData(BaseCheckpointData[TaskExecutionResult, TaskEvaluationResult]):
    """Checkpoint state for resumable calendar benchmark runs."""

    config: RunConfig | None = Field(
        default=None,
        description="Run configuration for resuming with same options",
    )
    metadata: BenchmarkMetadata | None = Field(
        default=None,
        description="Benchmark run metadata",
    )
    # Keys are absolute file paths, values are sha256 hashes
    source_file_hashes: dict[str, str] = Field(
        default_factory=dict,
        description="Map of source filename to sha256 hash (use .keys() for paths)",
    )
