"""Unified async runner for form filling benchmark with one-shot and interactive modes."""

import asyncio
import json
import logging
import traceback
from datetime import datetime
from pathlib import Path
from typing import Literal, Union

from tqdm.asyncio import tqdm

from sage_benchmark.form_filling.evaluator import (
    evaluate_interactive_task,
)
from sage_benchmark.form_filling.evaluator import (
    evaluate_task as evaluate_one_shot_task,
)
from sage_benchmark.form_filling.interactive import run_single_task as run_interactive_task
from sage_benchmark.form_filling.loader import load_all_form_tasks
from sage_benchmark.form_filling.one_shot import run_single_task as run_one_shot_task
from sage_benchmark.form_filling.schemas import (
    FormTask,
    FormTaskEvaluationResult,
    InteractiveTaskEvaluationResult,
    InteractiveTaskExecutionResult,
    TaskExecutionResult,
)
from sage_benchmark.form_filling.utils import reconstruct_task_execution_result
from sage_benchmark.shared.model_clients import get_async_client

logger = logging.getLogger(__name__)


def append_batch_to_json_list(path: Path, items: list[dict]):
    """Atomically append multiple items to JSON array.

    Args:
        path: Path to JSON file
        items: List of items to append
    """
    if path.exists():
        with open(path) as f:
            data = json.load(f)
    else:
        data = []

    data.extend(items)

    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def load_json_list(path: Path) -> list[dict]:
    """Load JSON array from file."""
    with open(path) as f:
        return json.load(f)


def _load_prior_interactive_results(
    task_results_path: str, tasks: list[FormTask]
) -> list[InteractiveTaskExecutionResult]:
    """Load results from prior interactive run from file."""
    print(f"Loading task results from: {task_results_path}")
    task_results_data = load_json_list(Path(task_results_path))

    # Reconstruct InteractiveTaskExecutionResult objects
    task_map = {task.form_id: task for task in tasks}

    execution_results: list[InteractiveTaskExecutionResult] = []

    for task_result_data in task_results_data:
        exec_data = task_result_data["execution"]
        form_id = task_result_data["form_id"]

        if form_id not in task_map:
            print(f"Warning: Form {form_id} not found, skipping")
            continue

        exec_result = InteractiveTaskExecutionResult.model_validate(
            {**exec_data, "task": task_map[form_id], "form_id": form_id}
        )
        execution_results.append(exec_result)

    return execution_results


async def run_tasks(
    data_path: str,
    execution_mode: Literal["one-shot", "interactive"],
    model_name: str,
    judge_model: str,
    interviewer_model: str | None = None,
    base_url: str | None = None,
    output_dir: str | None = None,
    limit: int | None = None,
    task_id: int | None = None,
    run_mode: Literal["all", "tasks", "eval"] = "all",
    task_results_path: str | None = None,
    batch_size: int = 10,
    max_concurrent_requests: int = 10,
    prompt_type: str = "base",
    reasoning_effort: str | None = None,
    judge_reasoning_effort: str | None = None,
    max_rounds: int = 50,
    interviewer_type: str = "base",
):
    """Run the complete form filling benchmark with async parallelization.

    Args:
        data_path: Path to directory containing task directories
        execution_mode: "one-shot" for structured output, "interactive" for interview Q&A
        model_name: Model for form filling (one-shot) or assistant (interactive)
        judge_model: Model to use for evaluation
        interviewer_model: Model for interviewer agent (interactive mode only)
        base_url: Optional base URL for OpenAI-compatible API (e.g., vLLM)
        output_dir: Optional directory to save results
        limit: Optional limit on number of tasks to run
        task_id: Optional specific task index to run (0-based)
        run_mode: Run mode - 'all' (tasks + eval), 'tasks', or 'eval'
        task_results_path: Path to task_results.json (required for eval mode)
        batch_size: Number of tasks/evals to run in parallel
        max_concurrent_requests: Maximum concurrent API requests per client
        prompt_type: Type of prompt to use ("base", "privacy_aware", "privacy_explained")
        reasoning_effort: Reasoning effort level for agent model (gpt-5.x, gemini)
        judge_reasoning_effort: Reasoning effort level for judge model (gpt-5.x, gemini)
        prompt_type: Type of prompt for one-shot mode ("base", "privacy_aware", "privacy_explained")
        max_rounds: Maximum conversation rounds for interactive mode
        interviewer_type: Type of interviewer prompt ("base" or "detail")

    Returns:
        Dictionary with benchmark results
    """
    # Create run directory
    if output_dir:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        if execution_mode == "one-shot":
            run_dir = output_path / f"run_{model_name}_{timestamp_str}"
        else:
            run_dir = (
                output_path
                / f"run_{timestamp_str}_interactive_interviewer_{interviewer_model}_assistant_{model_name}"
            )
        run_dir.mkdir(parents=True, exist_ok=True)

        task_results_file = run_dir / "task_results.json"
        eval_results_file = run_dir / "eval_results.json"
        summary_file = run_dir / "summary.json"
        print(f"Run directory: {run_dir}")
    else:
        run_dir = None
        task_results_file = None
        eval_results_file = None
        summary_file = None

    # Load tasks
    tasks = load_all_form_tasks(data_path)
    print(f"Loaded {len(tasks)} form tasks from {data_path}")

    # Handle task_id - run only a specific task
    if task_id is not None:
        if task_id < 0 or task_id >= len(tasks):
            raise ValueError(
                f"--id {task_id} is out of range. Must be between 0 and {len(tasks) - 1}."
            )
        tasks = [tasks[task_id]]
        print(f"Running only task at index {task_id}")
    elif limit:
        tasks = tasks[:limit]
        print(f"Running first {limit} tasks")

    # Dispatch to appropriate mode
    if execution_mode == "one-shot":
        result = await _run_one_shot_mode(
            tasks=tasks,
            model_name=model_name,
            judge_model=judge_model,
            base_url=base_url,
            run_mode=run_mode,
            task_results_path=task_results_path,
            batch_size=batch_size,
            max_concurrent_requests=max_concurrent_requests,
            prompt_type=prompt_type,
            reasoning_effort=reasoning_effort,
            judge_reasoning_effort=judge_reasoning_effort,
            task_results_file=task_results_file,
            eval_results_file=eval_results_file,
            summary_file=summary_file,
        )
    else:
        result = await _run_interactive_mode(
            tasks=tasks,
            assistant_model=model_name,
            interviewer_model=interviewer_model,
            judge_model=judge_model,
            run_mode=run_mode,
            task_results_path=task_results_path,
            batch_size=batch_size,
            max_concurrent_requests=max_concurrent_requests,
            max_rounds=max_rounds,
            prompt_type=prompt_type,
            interviewer_type=interviewer_type,
            task_results_file=task_results_file,
            eval_results_file=eval_results_file,
            summary_file=summary_file,
            base_url=base_url,
        )

    return result


async def _run_one_shot_mode(
    tasks: list[FormTask],
    model_name: str,
    judge_model: str,
    base_url: str | None,
    run_mode: Literal["all", "tasks", "eval"],
    task_results_path: str | None,
    batch_size: int,
    max_concurrent_requests: int,
    prompt_type: str,
    reasoning_effort: str | None,
    judge_reasoning_effort: str | None,
    task_results_file: Path | None,
    eval_results_file: Path | None,
    summary_file: Path | None,
):
    """Run one-shot mode (structured output)."""
    execution_results: list[TaskExecutionResult] = []

    if run_mode == "eval":
        # Load task results from file
        if not task_results_path:
            raise ValueError("task_results_path is required for eval mode")

        print(f"Loading task results from: {task_results_path}")
        task_results_data = load_json_list(Path(task_results_path))
        print(f"Loaded {len(task_results_data)} task results")

        # Reconstruct TaskExecutionResult objects from saved data
        task_map = {task.form_id: task for task in tasks}

        for task_result_data in task_results_data:
            exec_data = task_result_data["execution"]
            form_id = task_result_data["form_id"]

            if form_id not in task_map:
                print(f"Warning: Form {form_id} not found in data_path, skipping")
                continue

            exec_result = reconstruct_task_execution_result(exec_data, task_map[form_id])
            execution_results.append(exec_result)

    else:
        # Run tasks in parallel batches
        agent_client = get_async_client(
            model_name,
            base_url=base_url,
            max_concurrent_requests=max_concurrent_requests,
            reasoning_effort=reasoning_effort,
        )

        print(f"\n{'=' * 60}")
        print(f"Running {len(tasks)} tasks in one-shot mode (batches of {batch_size})")
        print(f"{'=' * 60}\n")

        # Process tasks in batches
        for batch_start in range(0, len(tasks), batch_size):
            batch_end = min(batch_start + batch_size, len(tasks))
            batch = tasks[batch_start:batch_end]

            print(
                f"Processing batch {batch_start // batch_size + 1} (tasks {batch_start}-{batch_end - 1})..."
            )

            # Run batch in parallel
            batch_tasks = [
                run_one_shot_task(task, idx, agent_client, prompt_type=prompt_type)
                for idx, task in enumerate(batch, start=batch_start)
            ]

            # Use gather with return_exceptions to handle errors gracefully
            batch_results = await asyncio.gather(*batch_tasks, return_exceptions=True)

            # Process results and handle exceptions
            batch_data_to_save = []
            for task_idx, result in zip(range(batch_start, batch_end), batch_results):
                if isinstance(result, Exception):
                    # Log error and create failed TaskExecutionResult
                    error_msg = f"Task {task_idx} failed with exception: {str(result)}"
                    logger.error(error_msg)
                    logger.error(traceback.format_exc())
                    print(f"Task {task_idx}: FAILED - {str(result)}")

                    # Create failed result
                    failed_result = TaskExecutionResult(
                        task_index=task_idx,
                        task=batch[task_idx - batch_start],
                        action=None,
                        llm_calls=[],
                        success=False,
                        error_message=str(result),
                    )
                    execution_results.append(failed_result)

                    if task_results_file:
                        batch_data_to_save.append(
                            {
                                "task_index": failed_result.task_index,
                                "form_id": failed_result.task.form_id,
                                "execution": failed_result.model_dump(mode="json"),
                            }
                        )
                else:
                    # Success
                    execution_results.append(result)

                    # Print summary
                    if result.success:
                        print(
                            f"Task {result.task_index}: {result.action.action_type.upper()} - "
                            f"Form {result.task.form_id}"
                        )
                    else:
                        print(f"Task {result.task_index}: FAILED after retries")

                    if task_results_file:
                        batch_data_to_save.append(
                            {
                                "task_index": result.task_index,
                                "form_id": result.task.form_id,
                                "execution": result.model_dump(mode="json"),
                            }
                        )

            # Batch-level file write (atomic)
            if task_results_file and batch_data_to_save:
                append_batch_to_json_list(task_results_file, batch_data_to_save)
                print(
                    f"Saved batch {batch_start // batch_size + 1} results to {task_results_file}\n"
                )

    # Evaluate results in parallel batches
    evaluation_results: list[FormTaskEvaluationResult] = []

    if run_mode != "tasks":
        print(f"\n{'=' * 60}")
        print("Evaluating results...")
        print("Correctness: 0 - 1, fraction of fields matching ground truth.")
        print("Privacy: 0 - 1, fraction of secrets protected.")
        print("Validation: pass/fail, pydantic schema validation.")
        print(f"{'=' * 60}\n")

        # Create judge client
        judge_client = get_async_client(
            judge_model,
            max_concurrent_requests=max_concurrent_requests,
            reasoning_effort=judge_reasoning_effort,
        )

        # Filter to successful executions only
        successful_results = [r for r in execution_results if r.success]
        print(f"Evaluating {len(successful_results)} successful tasks in batches of {batch_size}\n")

        # Process evaluations in batches
        for batch_start in range(0, len(successful_results), batch_size):
            batch_end = min(batch_start + batch_size, len(successful_results))
            batch = successful_results[batch_start:batch_end]

            print(
                f"Evaluating batch {batch_start // batch_size + 1} (evals {batch_start}-{batch_end - 1})..."
            )

            # Run eval batch in parallel
            eval_tasks = [
                evaluate_one_shot_task(exec_result, exec_result.task, judge_client)
                for exec_result in batch
            ]

            batch_eval_results = await asyncio.gather(*eval_tasks, return_exceptions=True)

            # Process eval results and handle exceptions
            batch_eval_data_to_save = []
            for eval_idx, eval_result in enumerate(batch_eval_results):
                if isinstance(eval_result, Exception):
                    # Log error but continue
                    error_msg = f"Evaluation {batch_start + eval_idx} failed: {str(eval_result)}"
                    logger.error(error_msg)
                    logger.error(traceback.format_exc())
                    print(f"Eval {batch_start + eval_idx}: FAILED - {str(eval_result)}")
                else:
                    # Success
                    evaluation_results.append(eval_result)

                    print(
                        f"Task {eval_result.task_index}: "
                        f"Correctness={eval_result.correctness.accuracy:.2%} "
                        f"({eval_result.correctness.exact_matches}/{eval_result.correctness.total_fields}), "
                        f"Privacy={eval_result.privacy.privacy_score:.2%} "
                        f"({len(eval_result.privacy.secrets_checked) - len(eval_result.privacy.secrets_leaked)}/{len(eval_result.privacy.secrets_checked)}), "
                        f"Valid={'✓' if eval_result.pydantic_validation_passed else '✗'}"
                    )

                    if eval_results_file:
                        batch_eval_data_to_save.append(
                            {
                                "task_index": eval_result.task_index,
                                "form_id": eval_result.task.form_id,
                                "evaluation": eval_result.model_dump(mode="json"),
                            }
                        )

            # Batch-level eval file write
            if eval_results_file and batch_eval_data_to_save:
                append_batch_to_json_list(eval_results_file, batch_eval_data_to_save)
                print(
                    f"Saved batch {batch_start // batch_size + 1} eval results to {eval_results_file}\n"
                )

    # Build and return summary
    return _build_one_shot_summary(
        execution_results=execution_results,
        evaluation_results=evaluation_results,
        model_name=model_name,
        judge_model=judge_model,
        run_mode=run_mode,
        batch_size=batch_size,
        summary_file=summary_file,
    )


async def _run_interactive_mode(
    tasks: list[FormTask],
    assistant_model: str,
    interviewer_model: str,
    judge_model: str,
    run_mode: Literal["all", "tasks", "eval"],
    task_results_path: str | None,
    batch_size: int,
    max_concurrent_requests: int,
    max_rounds: int,
    prompt_type: str,
    interviewer_type: str,
    task_results_file: Path | None,
    eval_results_file: Path | None,
    summary_file: Path | None,
    base_url: str | None = None,
):
    """Run interactive mode (interview Q&A)."""
    execution_results: list[InteractiveTaskExecutionResult] = []

    if run_mode == "eval":
        # eval only - load prior results
        if not task_results_path:
            raise ValueError("task_results_path is required for eval mode")
        execution_results = _load_prior_interactive_results(task_results_path, tasks)
        print(f"Loaded {len(execution_results)} task results")

    else:
        # Create async clients
        interviewer_client = get_async_client(
            interviewer_model, max_concurrent_requests=max_concurrent_requests
        )
        assistant_client = get_async_client(
            assistant_model, base_url=base_url, max_concurrent_requests=max_concurrent_requests
        )

        print(f"\n{'=' * 60}")
        print(f"Running {len(tasks)} tasks in interactive mode (batches of {batch_size})")
        print(f"Max rounds per task: {max_rounds}")
        print(f"{'=' * 60}\n")

        # Process tasks in batches
        for batch_start in range(0, len(tasks), batch_size):
            batch_end = min(batch_start + batch_size, len(tasks))
            batch = tasks[batch_start:batch_end]

            print(
                f"Processing batch {batch_start // batch_size + 1} (tasks {batch_start}-{batch_end - 1})..."
            )

            # Run batch in parallel
            batch_tasks = [
                run_interactive_task(
                    task,
                    idx,
                    interviewer_client,
                    assistant_client,
                    max_rounds,
                    prompt_type,
                    interviewer_type,
                )
                for idx, task in enumerate(batch, start=batch_start)
            ]
            batch_results = await asyncio.gather(*batch_tasks, return_exceptions=True)

            # Process results
            batch_data_to_save = []
            for task_idx, result in zip(range(batch_start, batch_end), batch_results):
                if isinstance(result, Exception):
                    logger.error(f"Task {task_idx} failed: {result}")
                    print(f"Task {task_idx}: FAILED - {result}")
                else:
                    execution_results.append(result)
                    print(
                        f"Task {task_idx}: {result.termination_reason} - "
                        f"{result.total_rounds} rounds"
                    )

                    if task_results_file:
                        batch_data_to_save.append(
                            {
                                "task_index": result.task_index,
                                "form_id": result.form_id,
                                "execution": result.model_dump(mode="json"),
                            }
                        )

            # Batch-level file write
            if task_results_file and batch_data_to_save:
                append_batch_to_json_list(task_results_file, batch_data_to_save)
                print(f"Saved batch {batch_start // batch_size + 1} results\n")

    # Run evaluation
    evaluation_results: list[InteractiveTaskEvaluationResult] = []

    if run_mode != "tasks":
        print(f"\n{'=' * 60}")
        print("Evaluating results...")
        print("Correctness: 0 - 1, fraction of fields matching ground truth.")
        print("FormPrivacy: 0 - 1, fraction of secrets protected in form.")
        print("ConvPrivacy: 0 - 1, fraction of secrets protected in conversation.")
        print("Validation: pass/fail, pydantic schema validation.")
        print(f"{'=' * 60}\n")

        judge_client = get_async_client(
            judge_model, max_concurrent_requests=max_concurrent_requests
        )

        successful_results = [r for r in execution_results if r.success]
        print(f"Evaluating {len(successful_results)} successful tasks in batches of {batch_size}\n")

        # Process evaluations in batches
        for batch_start in range(0, len(successful_results), batch_size):
            batch_end = min(batch_start + batch_size, len(successful_results))
            batch = successful_results[batch_start:batch_end]

            print(f"Evaluating batch {batch_start // batch_size + 1}...")

            eval_tasks = [
                evaluate_interactive_task(exec_result, judge_client) for exec_result in batch
            ]

            batch_eval_results = await asyncio.gather(*eval_tasks, return_exceptions=True)

            batch_eval_data_to_save = []
            for eval_result in batch_eval_results:
                if isinstance(eval_result, Exception):
                    logger.error(f"Evaluation failed: {eval_result}")
                    logger.error(traceback.format_exc())
                else:
                    evaluation_results.append(eval_result)

                    print(
                        f"Task {eval_result.task_index}: "
                        f"Accuracy={eval_result.correctness.accuracy:.2%}, "
                        f"FormPrivacy={eval_result.form_privacy.privacy_score:.2%}, "
                        f"ConvPrivacy={eval_result.conversation_privacy.privacy_score:.2%}, "
                        f"Valid={'✓' if eval_result.pydantic_validation_passed else '✗'}"
                    )

                    if eval_results_file:
                        batch_eval_data_to_save.append(
                            {
                                "task_index": eval_result.task_index,
                                "form_id": eval_result.form_id,
                                "evaluation": eval_result.model_dump(mode="json"),
                            }
                        )

            if eval_results_file and batch_eval_data_to_save:
                append_batch_to_json_list(eval_results_file, batch_eval_data_to_save)
                print("Saved batch eval results\n")

    # Build and return summary
    return _build_interactive_summary(
        execution_results=execution_results,
        evaluation_results=evaluation_results,
        interviewer_model=interviewer_model,
        assistant_model=assistant_model,
        judge_model=judge_model,
        run_mode=run_mode,
        batch_size=batch_size,
        max_rounds=max_rounds,
        summary_file=summary_file,
    )


def _build_one_shot_summary(
    execution_results: list[TaskExecutionResult],
    evaluation_results: list[FormTaskEvaluationResult],
    model_name: str,
    judge_model: str,
    run_mode: str,
    batch_size: int,
    summary_file: Path | None,
) -> dict:
    """Build summary for one-shot mode."""
    # Aggregate metrics
    if evaluation_results:
        n_evals = len(evaluation_results)

        # Correctness metrics
        avg_accuracy = sum(e.correctness.accuracy for e in evaluation_results) / n_evals
        avg_precision = sum(e.correctness.precision for e in evaluation_results) / n_evals
        avg_recall = sum(e.correctness.recall for e in evaluation_results) / n_evals
        avg_f1 = sum(e.correctness.f1_score for e in evaluation_results) / n_evals

        # Perfect forms: F1 = 1.0
        perfect_forms = sum(1 for e in evaluation_results if e.correctness.f1_score == 1.0)
        perfect_forms_rate = perfect_forms / n_evals

        # Privacy metrics
        avg_privacy = sum(e.privacy.privacy_score for e in evaluation_results) / n_evals

        # Leakage count: forms with any secret leaked
        leakage_count = sum(1 for e in evaluation_results if len(e.privacy.secrets_leaked) > 0)
        leakage_rate = leakage_count / n_evals

        # Total secrets stats
        total_secrets = sum(len(e.privacy.secrets_checked) for e in evaluation_results)
        total_leaked_secrets = sum(len(e.privacy.secrets_leaked) for e in evaluation_results)
        secret_leakage_rate = total_leaked_secrets / total_secrets if total_secrets > 0 else 0.0

        # Validation rate
        validation_rate = (
            sum(1 for e in evaluation_results if e.pydantic_validation_passed) / n_evals
        )
    else:
        n_evals = 0
        avg_accuracy = 0.0
        avg_precision = 0.0
        avg_recall = 0.0
        avg_f1 = 0.0
        perfect_forms = 0
        perfect_forms_rate = 0.0
        avg_privacy = 0.0
        leakage_count = 0
        leakage_rate = 0.0
        total_secrets = 0
        total_leaked_secrets = 0
        secret_leakage_rate = 0.0
        validation_rate = 0.0

    # Build final summary
    result = {
        "summary": {
            "execution_mode": "one-shot",
            "agent_model": model_name,
            "judge_model": judge_model,
            "timestamp": datetime.now().isoformat(),
            "mode": run_mode,
            "total_tasks": len(execution_results),
            "successful_executions": sum(1 for r in execution_results if r.success),
            "evaluated_forms": n_evals,
            # Correctness metrics
            "avg_accuracy": avg_accuracy,
            "avg_precision": avg_precision,
            "avg_recall": avg_recall,
            "avg_f1_score": avg_f1,
            "perfect_forms": perfect_forms,
            "perfect_forms_rate": perfect_forms_rate,
            # Privacy metrics
            "avg_privacy_score": avg_privacy,
            "leakage_count": leakage_count,
            "leakage_rate": leakage_rate,
            "total_secrets": total_secrets,
            "total_leaked_secrets": total_leaked_secrets,
            "secret_leakage_rate": secret_leakage_rate,
            # Validation
            "validation_rate": validation_rate,
            "batch_size": batch_size,
        },
    }

    # Save summary
    if summary_file:
        with open(summary_file, "w") as f:
            json.dump(result, f, indent=2)
        print(f"\nSummary saved to: {summary_file}")

    # Print summary
    print(f"\n{'=' * 60}")
    print("SUMMARY")
    print(f"{'=' * 60}")
    print(f"Execution mode: one-shot")
    print(f"Mode: {run_mode}")
    print(f"Model: {model_name}")
    print(f"Judge: {judge_model}")
    print(f"Batch size: {batch_size}")
    print(f"Total tasks: {len(execution_results)}")
    print(f"Successful executions: {result['summary']['successful_executions']}")
    if run_mode != "tasks" and n_evals > 0:
        print(f"\nCorrectness Metrics:")
        print(f"  Average precision: {avg_precision:.2%}")
        print(f"  Average recall: {avg_recall:.2%}")
        print(f"  Average F1 score: {avg_f1:.2%}")
        print(f"  Perfect forms (F1=1.0): {perfect_forms}/{n_evals} ({perfect_forms_rate:.1%})")
        print(f"\nPrivacy Metrics:")
        print(f"  Average privacy score: {avg_privacy:.2%}")
        print(f"  Leakage rate of forms: {leakage_count}/{n_evals} ({leakage_rate:.1%})")
        print(f"  Total secrets: {total_secrets}")
        print(f"  Total leaked secrets: {total_leaked_secrets}")
        if total_secrets > 0:
            print(f"  Leakage rate per secret: {secret_leakage_rate:.1%}")
        print(f"\nValidation rate: {validation_rate:.1%}")

    return result


def _build_interactive_summary(
    execution_results: list[InteractiveTaskExecutionResult],
    evaluation_results: list[InteractiveTaskEvaluationResult],
    interviewer_model: str,
    assistant_model: str,
    judge_model: str,
    run_mode: str,
    batch_size: int,
    max_rounds: int,
    summary_file: Path | None,
) -> dict:
    """Build summary for interactive mode."""
    n_evals = len(evaluation_results)

    if n_evals > 0:
        # Correctness metrics
        avg_accuracy = sum(e.correctness.accuracy for e in evaluation_results) / n_evals
        avg_precision = sum(e.correctness.precision for e in evaluation_results) / n_evals
        avg_recall = sum(e.correctness.recall for e in evaluation_results) / n_evals
        avg_f1 = sum(e.correctness.f1_score for e in evaluation_results) / n_evals

        # Perfect forms: F1 = 1.0
        perfect_forms = sum(1 for e in evaluation_results if e.correctness.f1_score == 1.0)
        perfect_forms_rate = perfect_forms / n_evals

        # Privacy metrics
        avg_form_privacy = sum(e.form_privacy.privacy_score for e in evaluation_results) / n_evals
        avg_conv_privacy = (
            sum(e.conversation_privacy.privacy_score for e in evaluation_results) / n_evals
        )

        # Leakage counts
        form_leakage_count = sum(
            1 for e in evaluation_results if len(e.form_privacy.secrets_leaked) > 0
        )
        conv_leakage_count = sum(
            1
            for e in evaluation_results
            if len(e.conversation_privacy.secrets_leaked_in_conversation) > 0
        )

        # Total secrets stats
        total_secrets = sum(len(e.form_privacy.secrets_checked) for e in evaluation_results)
        total_form_leaked = sum(len(e.form_privacy.secrets_leaked) for e in evaluation_results)
        total_conv_leaked = sum(
            len(e.conversation_privacy.secrets_leaked_in_conversation) for e in evaluation_results
        )

        # Validation rate
        validation_rate = (
            sum(1 for e in evaluation_results if e.pydantic_validation_passed) / n_evals
        )
    else:
        avg_accuracy = 0.0
        avg_precision = 0.0
        avg_recall = 0.0
        avg_f1 = 0.0
        perfect_forms = 0
        perfect_forms_rate = 0.0
        avg_form_privacy = 0.0
        avg_conv_privacy = 0.0
        form_leakage_count = 0
        conv_leakage_count = 0
        total_secrets = 0
        total_form_leaked = 0
        total_conv_leaked = 0
        validation_rate = 0.0

    # Build summary
    result = {
        "summary": {
            "execution_mode": "interactive",
            "interviewer_model": interviewer_model,
            "assistant_model": assistant_model,
            "judge_model": judge_model,
            "timestamp": datetime.now().isoformat(),
            "mode": run_mode,
            "total_tasks": len(execution_results),
            "successful_executions": sum(1 for r in execution_results if r.success),
            "evaluated_forms": n_evals,
            # Correctness metrics
            "avg_accuracy": avg_accuracy,
            "avg_precision": avg_precision,
            "avg_recall": avg_recall,
            "avg_f1_score": avg_f1,
            "perfect_forms": perfect_forms,
            "perfect_forms_rate": perfect_forms_rate,
            # Privacy metrics
            "avg_form_privacy_score": avg_form_privacy,
            "avg_conversation_privacy_score": avg_conv_privacy,
            "form_leakage_count": form_leakage_count,
            "conversation_leakage_count": conv_leakage_count,
            "total_secrets": total_secrets,
            "total_form_leaked_secrets": total_form_leaked,
            "total_conversation_leaked_secrets": total_conv_leaked,
            # Validation
            "validation_rate": validation_rate,
            "batch_size": batch_size,
            "max_rounds": max_rounds,
        },
    }

    # Save summary
    if summary_file:
        with open(summary_file, "w") as f:
            json.dump(result, f, indent=2)
        print(f"\nSummary saved to: {summary_file}")

    # Print summary
    print(f"\n{'=' * 60}")
    print("SUMMARY")
    print(f"{'=' * 60}")
    print(f"Execution mode: interactive")
    print(f"Mode: {run_mode}")
    print(f"Interviewer Model: {interviewer_model}")
    print(f"Assistant Model: {assistant_model}")
    print(f"Judge Model: {judge_model}")
    print(f"Batch size: {batch_size}")
    print(f"Max rounds: {max_rounds}")
    print(f"Total tasks: {len(execution_results)}")
    print(f"Successful executions: {result['summary']['successful_executions']}")

    if run_mode != "tasks" and n_evals > 0:
        print(f"\nCorrectness Metrics:")
        print(f"  Average precision: {avg_precision:.2%}")
        print(f"  Average recall: {avg_recall:.2%}")
        print(f"  Average F1 score: {avg_f1:.2%}")
        print(f"  Perfect forms (F1=1.0): {perfect_forms}/{n_evals} ({perfect_forms_rate:.1%})")
        print(f"\nPrivacy Metrics:")
        print(f"  Average form privacy score: {avg_form_privacy:.2%}")
        print(f"  Average conversation privacy score: {avg_conv_privacy:.2%}")
        print(
            f"  Form leakage rate: {form_leakage_count}/{n_evals} ({form_leakage_count / n_evals:.1%})"
        )
        print(
            f"  Conversation leakage rate: {conv_leakage_count}/{n_evals} ({conv_leakage_count / n_evals:.1%})"
        )
        print(f"  Total secrets: {total_secrets}")
        print(f"  Total form leaked: {total_form_leaked}")
        print(f"  Total conversation leaked: {total_conv_leaked}")
        print(f"\nValidation rate: {validation_rate:.1%}")

    return result
