"""Base checkpoint data model for resumable benchmark runs."""

from datetime import datetime
from typing import Generic, TypeVar

from pydantic import BaseModel, Field

TExec = TypeVar("TExec", bound=BaseModel)
TEval = TypeVar("TEval", bound=BaseModel)


class BaseCheckpointData(BaseModel, Generic[TExec, TEval]):
    """Base checkpoint state shared across all benchmarks.

    Each benchmark extends this with benchmark-specific fields (e.g. ``config``,
    ``metadata``, ``source_file_hashes``).
    """

    execution_results: list[TExec] = Field(
        default_factory=list,
        description="Completed execution results",
    )
    evaluation_results: list[TEval] = Field(
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
