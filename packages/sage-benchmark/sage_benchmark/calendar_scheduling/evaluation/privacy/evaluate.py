"""Privacy leakage evaluation for task execution results."""

from typing import Literal

from privacy_judge import CIFlowAnalysis
from sage_llm import ModelClient

from sage_benchmark.calendar_scheduling.types import (
    LeakedSecret,
    TaskExecutionResult,
)

from .ci import CalendarCIJudge
from .leakage import CalendarLeakageJudge


async def evaluate_privacy_leakage(
    execution_result: TaskExecutionResult,
    model: str,
    model_client: ModelClient,
    n_judges: int = 5,
    concurrency: int = 1,
) -> list[LeakedSecret]:
    """Evaluate privacy leakage using binary leak detection.

    Args:
        execution_result: The task execution result containing emails and task info
        model: Model name to use for evaluation
        model_client: ModelClient instance for making LLM calls
        n_judges: Number of parallel judges for majority voting (default: 5)
        concurrency: Number of concurrent evaluations (default: 1, no concurrency)

    Returns:
        List of LeakedSecret objects for each detected leak
    """
    judge = CalendarLeakageJudge(
        model=model,
        model_client=model_client,
        n_judges=n_judges,
    )
    return await judge.evaluate_execution(execution_result, concurrency=concurrency)


async def evaluate_privacy_ci(
    execution_result: TaskExecutionResult,
    model: str,
    model_client: ModelClient,
) -> list[CIFlowAnalysis]:
    """Evaluate privacy using Contextual Integrity flow analysis.

    Identifies all information flows from assistant to requestor and
    returns those judged as violations.

    Args:
        execution_result: The task execution result containing emails and task info
        model: Model name to use for evaluation
        model_client: ModelClient instance for making LLM calls

    Returns:
        List of CIFlowAnalysis objects for each violation flow
    """
    judge = CalendarCIJudge(
        model=model,
        model_client=model_client,
    )

    judgment = await judge.evaluate_execution(execution_result)

    # Return only violation flows
    return [flow for flow in judge.filter_assistant_flows(judgment) if flow.verdict == "violation"]
