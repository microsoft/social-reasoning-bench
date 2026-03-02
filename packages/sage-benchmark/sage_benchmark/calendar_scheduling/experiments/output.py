"""Output utilities for experiment finalization."""

import logging
from datetime import datetime

from pydantic_core import to_json
from sage_llm import save_traces

from ..checkpoints import CheckpointManager, RunConfig
from ..evaluation.evaluator import compute_evaluation_summary
from ..run_paths import RunPaths
from ..types import BenchmarkMetadata, BenchmarkOutput, KeyedCalendarTask, TaskEvaluationResult

logger = logging.getLogger(__name__)

# Alias for clarity in this module
ExperimentConfig = RunConfig


def build_output(
    tasks: list[KeyedCalendarTask],
    eval_results: list[TaskEvaluationResult],
    config: ExperimentConfig,
    elapsed_seconds: float | None = None,
) -> BenchmarkOutput:
    """Build final benchmark output from evaluation results.

    Args:
        tasks: List of tasks that were evaluated
        eval_results: List of evaluation results
        config: Experiment configuration

    Returns:
        BenchmarkOutput with metadata, summary, and results
    """
    # Resolve CoT settings (per-agent overrides take precedence)
    assistant_cot = (
        config.assistant_explicit_cot
        if config.assistant_explicit_cot is not None
        else config.explicit_cot
    )
    requestor_cot = (
        config.requestor_explicit_cot
        if config.requestor_explicit_cot is not None
        else config.explicit_cot
    )

    # Resolve reasoning effort (per-agent overrides take precedence)
    assistant_effort = config.assistant_reasoning_effort or config.reasoning_effort
    requestor_effort = config.requestor_reasoning_effort or config.reasoning_effort
    judge_effort = config.judge_reasoning_effort or config.reasoning_effort

    metadata = BenchmarkMetadata(
        timestamp=datetime.now().isoformat(),
        assistant_model=config.resolved_assistant_model or "unknown",
        requestor_model=config.resolved_requestor_model or "unknown",
        judge_model=config.resolved_judge_model or "unknown",
        max_rounds=config.max_rounds,
        batch_size=config.batch_size,
        task_count=len(tasks),
        system_prompt=config.assistant_system_prompt,
        expose_preferences=config.expose_preferences or False,
        assistant_explicit_cot=assistant_cot,
        assistant_reasoning_effort=str(assistant_effort) if assistant_effort else None,
        requestor_explicit_cot=requestor_cot,
        requestor_reasoning_effort=str(requestor_effort) if requestor_effort else None,
        judge_reasoning_effort=str(judge_effort) if judge_effort else None,
        elapsed_seconds=elapsed_seconds,
    )

    summary = compute_evaluation_summary(eval_results)

    return BenchmarkOutput(
        metadata=metadata,
        summary=summary,
        results=eval_results,
    )


def save_output(
    output: BenchmarkOutput,
    run_paths: RunPaths,
    checkpoint_mgr: CheckpointManager | None = None,
    llm_tracing: bool = False,
) -> None:
    """Save output to disk and clean up checkpoint.

    Args:
        output: BenchmarkOutput to save
        run_paths: Paths for output files
        checkpoint_mgr: Optional checkpoint manager to clean up
        llm_tracing: If True, save LLM traces to disk
    """
    # Write final output
    run_paths.eval_path.write_bytes(to_json(output, indent=2))
    logger.info("Saved %d evaluation results to %s", len(output.results), run_paths.eval_path)

    # Save LLM traces if enabled
    if llm_tracing:
        save_llm_traces(run_paths)

    # Cleanup checkpoint on success
    if checkpoint_mgr:
        checkpoint_mgr.cleanup()


def save_llm_traces(run_paths: RunPaths) -> None:
    """Save LLM traces to disk.

    Args:
        run_paths: Paths for output files
    """
    traces_path = run_paths.get_traces_path()
    save_traces(traces_path)
    logger.info("Saved LLM traces to %s", traces_path)
