"""Privacy leakage evaluation for task execution results."""

from sage_llm import SageModelClient

from ...types import (
    CalendarExecutionResult,
    CalendarLeakedSecret,
)
from .leakage import CalendarLeakageJudge


async def evaluate_privacy_leakage(
    execution_result: CalendarExecutionResult,
    model: str,
    model_client: SageModelClient,
    n_votes: int = 5,
    concurrency: int = 1,
) -> list[CalendarLeakedSecret]:
    """Evaluate privacy leakage using binary leak detection.

    Args:
        execution_result: The task execution result containing emails and task info
        model: Model name to use for evaluation
        model_client: SageModelClient instance for making LLM calls
        n_votes: Number of parallel judges for majority voting (default: 5)
        concurrency: Number of concurrent evaluations (default: 1, no concurrency)

    Returns:
        List of CalendarLeakedSecret objects for each detected leak
    """
    judge = CalendarLeakageJudge(
        model=model,
        model_client=model_client,
        n_votes=n_votes,
    )
    return await judge.evaluate_execution(execution_result, concurrency=concurrency)
