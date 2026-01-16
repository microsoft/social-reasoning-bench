"""Main evaluation dispatcher for interviewer tasks."""

from sage_benchmark.shared.model_clients import AsyncModelClient

from ..schemas import (
    TaskEvaluationResult,
    TaskExecutionResult,
)
from .evaluation_form import evaluate_task_form
from .evaluation_yaml import evaluate_task_yaml


async def evaluate_task(
    exec_result: TaskExecutionResult,
    judge_client: AsyncModelClient,
) -> TaskEvaluationResult:
    """Evaluate task based on format.

    Dispatches to format-specific evaluators:
    - evaluate_task_yaml for YAML format
    - evaluate_task_form for form_filling format

    Args:
        exec_result: Task execution result
        judge_client: LLM judge client

    Returns:
        TaskEvaluationResult

    Raises:
        ValueError: If task failed or format is unknown
    """
    if not exec_result.success:
        raise ValueError("Cannot evaluate failed task")

    task_format = exec_result.task_format

    if task_format == "yaml":
        return await evaluate_task_yaml(exec_result, judge_client)
    elif task_format in ("form_filling", "form"):
        return await evaluate_task_form(exec_result, judge_client)
    else:
        raise ValueError(f"Unknown task format: {task_format}")
