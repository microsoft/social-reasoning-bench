"""Async runner for form filling benchmark with batching and parallelization."""

import asyncio
import json
import logging
import traceback
from datetime import datetime
from pathlib import Path
from typing import Literal

from tqdm.asyncio import tqdm

from sage_benchmark.form_filling.agent import run_single_task
from sage_benchmark.form_filling.evaluator import evaluate_task
from sage_benchmark.form_filling.loader import load_all_form_tasks
from sage_benchmark.form_filling.schemas import TaskExecutionResult
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


async def run_tasks(
    data_path: str,
    model_name: str,
    judge_model: str,
    base_url: str | None = None,
    output_dir: str | None = None,
    limit: int | None = None,
    mode: Literal["all", "tasks", "eval"] = "all",
    task_results_path: str | None = None,
    batch_size: int = 10,
    max_concurrent_requests: int = 10,
    prompt_type: str = "base",
):
    """Run the complete form filling benchmark with async parallelization.

    Args:
        data_path: Path to directory containing task directories
        model_name: Model to use for form filling
        judge_model: Model to use for evaluation
        base_url: Optional base URL for OpenAI-compatible API (e.g., vLLM)
        output_dir: Optional directory to save results
        limit: Optional limit on number of tasks to run
        mode: Run mode - 'all' (tasks + eval), 'tasks', or 'eval'
        task_results_path: Path to task_results.json (required for eval mode)
        batch_size: Number of tasks/evals to run in parallel
        max_concurrent_requests: Maximum concurrent API requests per client
        prompt_type: Type of prompt to use ("base", "privacy_aware", "privacy_explained")

    Returns:
        Dictionary with benchmark results
    """
    # Create run directory
    if output_dir:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        run_dir = output_path / f"run_{model_name}_{timestamp_str}"
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

    # Execute tasks (or load from file)
    execution_results: list[TaskExecutionResult] = []

    if mode == "eval":
        # Load task results from file
        if not task_results_path:
            raise ValueError("task_results_path is required for eval mode")

        print(f"Loading task results from: {task_results_path}")
        task_results_data = load_json_list(Path(task_results_path))
        print(f"Loaded {len(task_results_data)} task results")

        # Reconstruct TaskExecutionResult objects from saved data
        tasks = load_all_form_tasks(data_path)
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
        tasks = load_all_form_tasks(data_path)
        print(f"Loaded {len(tasks)} form tasks from {data_path}")

        if limit:
            tasks = tasks[:limit]
            print(f"Running first {limit} tasks")

        # Create async client
        agent_client = get_async_client(
            model_name, base_url=base_url, max_concurrent_requests=max_concurrent_requests
        )

        print(f"\n{'=' * 60}")
        print(f"Running {len(tasks)} tasks in batches of {batch_size}")
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
                run_single_task(task, idx, agent_client, prompt_type=prompt_type)
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
    evaluation_results = []

    if mode != "tasks":
        print(f"\n{'=' * 60}")
        print("Evaluating results...")
        print("Correctness: 0 - 1, fraction of fields matching ground truth.")
        print("Privacy: 0 - 1, fraction of secrets protected.")
        print("Validation: pass/fail, pydantic schema validation.")
        print(f"{'=' * 60}\n")

        # Create judge client
        judge_client = get_async_client(
            judge_model, max_concurrent_requests=max_concurrent_requests
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
                evaluate_task(exec_result, exec_result.task, judge_client) for exec_result in batch
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
    n_evals = len(evaluation_results) if evaluation_results else 0
    result = {
        "summary": {
            "agent_model": model_name,
            "judge_model": judge_model,
            "timestamp": datetime.now().isoformat(),
            "mode": mode,
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
    print(f"Mode: {mode}")
    print(f"Model: {model_name}")
    print(f"Judge: {judge_model}")
    print(f"Batch size: {batch_size}")
    print(f"Total tasks: {len(execution_results)}")
    print(f"Successful executions: {result['summary']['successful_executions']}")
    if mode != "tasks" and n_evals > 0:
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
