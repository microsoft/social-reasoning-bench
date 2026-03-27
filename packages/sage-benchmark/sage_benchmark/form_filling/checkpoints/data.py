"""Checkpoint data model for resumable form-filling benchmark runs."""

from datetime import datetime

from pydantic import BaseModel, Field

from ..schemas import InteractiveTaskEvaluationResult, InteractiveTaskExecutionResult


class CheckpointData(BaseModel):
    """Checkpoint state for resumable form-filling benchmark runs."""

    execution_results: list[InteractiveTaskExecutionResult] = Field(
        default_factory=list,
        description="Completed execution results",
    )
    evaluation_results: list[InteractiveTaskEvaluationResult] = Field(
        default_factory=list,
        description="Completed evaluation results",
    )
    completed_task_keys: list[str] = Field(
        default_factory=list,
        description="Task keys (form_id) that have completed execution",
    )
    completed_eval_keys: list[str] = Field(
        default_factory=list,
        description="Task keys (form_id) that have completed evaluation",
    )
    last_updated: str = Field(
        default_factory=lambda: datetime.now().isoformat(),
        description="ISO timestamp of last update",
    )
    interrupted: bool = Field(
        default=False,
        description="Whether the run was interrupted",
    )
