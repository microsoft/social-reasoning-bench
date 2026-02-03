"""Checkpoint data model for resumable benchmark runs."""

from datetime import datetime

from pydantic import BaseModel, Field

from ..types import BenchmarkMetadata, TaskEvaluationResult, TaskExecutionResult
from .run_config import RunConfig


class CheckpointData(BaseModel):
    """Checkpoint state for resumable benchmark runs."""

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
    execution_results: list[TaskExecutionResult] = Field(
        default_factory=list,
        description="Completed execution results",
    )
    evaluation_results: list[TaskEvaluationResult] = Field(
        default_factory=list,
        description="Completed evaluation results",
    )
    completed_task_keys: list[str] = Field(
        default_factory=list,
        description="Task keys that have completed execution",
    )
    completed_eval_keys: list[str] = Field(
        default_factory=list,
        description="Task keys that have completed evaluation",
    )
    last_updated: str = Field(
        default_factory=lambda: datetime.now().isoformat(),
        description="ISO timestamp of last update",
    )
    interrupted: bool = Field(
        default=False,
        description="Whether the run was interrupted",
    )
