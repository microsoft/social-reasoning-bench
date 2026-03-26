"""Async runner for form filling benchmark (interactive mode only)."""

import asyncio
import json
import logging
import traceback
from datetime import datetime
from pathlib import Path
from typing import Literal

from sage_llm import ModelClient

from sage_benchmark.form_filling.evaluation import (
    evaluate_interactive_task,
)
from sage_benchmark.form_filling.interactive import run_single_task as run_interactive_task
from sage_benchmark.form_filling.loader import load_all_form_tasks
from sage_benchmark.form_filling.schemas import (
    FormTask,
    InteractiveTaskEvaluationResult,
    InteractiveTaskExecutionResult,
)

logger = logging.getLogger(__name__)


def normalize_model_name(name: str) -> str:
    """Normalize model name for use in file paths and JSON output.

    Replaces '/' with '_' to avoid path issues.
    """
    if name is None:
        return name
    return name.replace("/", "_")


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
    model_name: str,
    judge_model: str,
    interviewer_model: str,
    interviewer_form_fill_model: str | None = None,
    base_url: str | None = None,
    output_dir: str | None = None,
    limit: int | None = None,
    task_id: int | None = None,
    run_mode: Literal["all", "tasks", "eval"] = "all",
    task_results_path: str | None = None,
    batch_size: int = 10,
    max_concurrent_requests: int = 10,
    prompt_type: str = "base",
    interviewer_reasoning_effort: str | None = None,
    assistant_reasoning_effort: str | None = None,
    judge_reasoning_effort: str | None = None,
    max_rounds: int = 50,
    interviewer_type: str = "base",
    single_field_mode: bool = False,
    malicious_strategy: int | None = None,
    malicious_attack_type: str = "privacy",
    malicious_strategies_file: str | None = None,
    temperature: float | None = None,
    social_reasoning: bool = False,
    use_privacy_example: bool = False,
):
    """Run the complete form filling benchmark with async parallelization.

    Args:
        data_path: Path to directory containing task directories
        model_name: Model for assistant agent
        judge_model: Model to use for evaluation
        interviewer_model: Model for interviewer agent
        interviewer_form_fill_model: Separate model for form filling after interview
        base_url: Optional base URL for OpenAI-compatible API (e.g., vLLM)
        output_dir: Optional directory to save results
        limit: Optional limit on number of tasks to run
        task_id: Optional specific task index to run (0-based)
        run_mode: Run mode - 'all' (tasks + eval), 'tasks', or 'eval'
        task_results_path: Path to task_results.json (required for eval mode)
        batch_size: Number of tasks/evals to run in parallel
        max_concurrent_requests: Maximum concurrent API requests per client
        prompt_type: Type of prompt to use ("base", "privacy_aware", "privacy_explained", "privacy_ci")
        interviewer_reasoning_effort: Reasoning effort for interviewer agent
        assistant_reasoning_effort: Reasoning effort for assistant agent
        judge_reasoning_effort: Reasoning effort level for judge model
        max_rounds: Maximum conversation rounds
        interviewer_type: Type of interviewer prompt ("base" or "detail")
        single_field_mode: If True, interviewer asks only one question per turn
        malicious_strategy: If set, use malicious interviewer with this strategy index
        malicious_attack_type: Type of malicious attack ("privacy", "hallucination", "red_flags")
        malicious_strategies_file: Path to strategies YAML file for malicious mode
        temperature: Sampling temperature for assistant/form-filler generation
        social_reasoning: If True, enable ToM-augmented social reasoning for assistant
        use_privacy_example: If True, append privacy examples to social reasoning prompt

    Returns:
        Dictionary with benchmark results
    """
    # Create run directory
    if output_dir:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        run_dir = (
            output_path
            / f"run_{timestamp_str}_interactive_interviewer_{normalize_model_name(interviewer_model)}_assistant_{normalize_model_name(model_name)}"
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

    # Mark tasks as malicious when running with a malicious strategy
    if malicious_strategy is not None:
        for task in tasks:
            task.is_malicious = True

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

    result = await _run_interactive_mode(
        tasks=tasks,
        assistant_model=model_name,
        interviewer_model=interviewer_model,
        interviewer_form_fill_model=interviewer_form_fill_model,
        judge_model=judge_model,
        run_mode=run_mode,
        task_results_path=task_results_path,
        batch_size=batch_size,
        max_concurrent_requests=max_concurrent_requests,
        max_rounds=max_rounds,
        prompt_type=prompt_type,
        interviewer_type=interviewer_type,
        malicious_strategy=malicious_strategy,
        malicious_attack_type=malicious_attack_type,
        malicious_strategies_file=malicious_strategies_file,
        interviewer_reasoning_effort=interviewer_reasoning_effort,
        assistant_reasoning_effort=assistant_reasoning_effort,
        judge_reasoning_effort=judge_reasoning_effort,
        task_results_file=task_results_file,
        eval_results_file=eval_results_file,
        summary_file=summary_file,
        base_url=base_url,
        single_field_mode=single_field_mode,
        temperature=temperature,
        social_reasoning=social_reasoning,
        use_privacy_example=use_privacy_example,
    )

    return result


async def _run_interactive_mode(
    tasks: list[FormTask],
    assistant_model: str,
    interviewer_model: str,
    interviewer_form_fill_model: str | None,
    judge_model: str,
    run_mode: Literal["all", "tasks", "eval"],
    task_results_path: str | None,
    batch_size: int,
    max_concurrent_requests: int,
    max_rounds: int,
    prompt_type: str,
    interviewer_type: str,
    malicious_strategy: int | None,
    malicious_attack_type: str = "privacy",
    malicious_strategies_file: str | None = None,
    interviewer_reasoning_effort: str | None = None,
    assistant_reasoning_effort: str | None = None,
    judge_reasoning_effort: str | None = None,
    task_results_file: Path | None = None,
    eval_results_file: Path | None = None,
    summary_file: Path | None = None,
    base_url: str | None = None,
    single_field_mode: bool = False,
    temperature: float | None = None,
    social_reasoning: bool = False,
    use_privacy_example: bool = False,
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
        interviewer_client = ModelClient(reasoning_effort=interviewer_reasoning_effort)
        assistant_client = ModelClient(
            base_url=base_url, reasoning_effort=assistant_reasoning_effort
        )
        # Separate form-fill client if a different model is specified
        form_fill_client = ModelClient() if interviewer_form_fill_model else None
        effective_form_fill_model = interviewer_form_fill_model or None

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
                    interviewer_model,
                    assistant_client,
                    assistant_model,
                    max_rounds,
                    prompt_type,
                    interviewer_type,
                    single_field_mode,
                    malicious_strategy,
                    malicious_attack_type=malicious_attack_type,
                    malicious_strategies_file=malicious_strategies_file,
                    temperature=temperature,
                    form_fill_client=form_fill_client,
                    form_fill_model=effective_form_fill_model,
                    social_reasoning=social_reasoning,
                    use_privacy_example=use_privacy_example,
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

        judge_client = ModelClient(reasoning_effort=judge_reasoning_effort)

        successful_results = [r for r in execution_results if r.success]
        print(f"Evaluating {len(successful_results)} successful tasks in batches of {batch_size}\n")

        # Process evaluations in batches
        for batch_start in range(0, len(successful_results), batch_size):
            batch_end = min(batch_start + batch_size, len(successful_results))
            batch = successful_results[batch_start:batch_end]

            print(f"Evaluating batch {batch_start // batch_size + 1}...")

            eval_tasks = [
                evaluate_interactive_task(exec_result, judge_client, judge_model)
                for exec_result in batch
            ]

            batch_eval_results = await asyncio.gather(*eval_tasks, return_exceptions=True)

            batch_eval_data_to_save = []
            for eval_result in batch_eval_results:
                if isinstance(eval_result, Exception):
                    logger.error(f"Evaluation failed: {eval_result}")
                    logger.error(traceback.format_exc())
                else:
                    evaluation_results.append(eval_result)

                    form_ci = len(eval_result.form_privacy_ci)
                    conv_ci = len(eval_result.conversation_privacy_ci)
                    print(
                        f"Task {eval_result.task_index}: "
                        f"Accuracy={eval_result.correctness.accuracy:.2%}, "
                        f"FormPrivacy={eval_result.form_privacy.privacy_score:.2%}, "
                        f"ConvPrivacy={eval_result.conversation_privacy.privacy_score:.2%}, "
                        f"FormCI={form_ci}, ConvCI={conv_ci}, "
                        f"Valid={'Y' if eval_result.pydantic_validation_passed else 'N'}"
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

        # CI metrics
        total_form_ci_violations = sum(len(e.form_privacy_ci) for e in evaluation_results)
        total_conv_ci_violations = sum(len(e.conversation_privacy_ci) for e in evaluation_results)
        tasks_with_form_ci_violations = sum(
            1 for e in evaluation_results if len(e.form_privacy_ci) > 0
        )
        tasks_with_conv_ci_violations = sum(
            1 for e in evaluation_results if len(e.conversation_privacy_ci) > 0
        )

        # Validation rate
        validation_rate = (
            sum(1 for e in evaluation_results if e.pydantic_validation_passed) / n_evals
        )

        # Due diligence metrics
        total_dd_fields = sum(e.due_diligence.total_masked_fields for e in evaluation_results)
        avg_mf_accuracy = (
            sum(e.due_diligence.masked_field_accuracy for e in evaluation_results) / n_evals
        )

        # Duty of care metrics
        total_doc_fields = sum(e.duty_of_care.total_fields for e in evaluation_results)
        scored_doc_evals = [e for e in evaluation_results if e.duty_of_care.min_score is not None]
        avg_duty_of_care_score = (
            sum(e.duty_of_care.min_score for e in scored_doc_evals) / len(scored_doc_evals)
            if scored_doc_evals
            else None
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
        total_form_ci_violations = 0
        total_conv_ci_violations = 0
        tasks_with_form_ci_violations = 0
        tasks_with_conv_ci_violations = 0
        validation_rate = 0.0
        total_dd_fields = 0
        avg_mf_accuracy = 0.0
        total_doc_fields = 0
        avg_duty_of_care_score = None

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
            "total_form_ci_violations": total_form_ci_violations,
            "total_conversation_ci_violations": total_conv_ci_violations,
            "tasks_with_form_ci_violations": tasks_with_form_ci_violations,
            "tasks_with_conversation_ci_violations": tasks_with_conv_ci_violations,
            # Due diligence
            "total_masked_fields": total_dd_fields,
            "avg_masked_field_accuracy": avg_mf_accuracy,
            # Duty of care
            "total_duty_of_care_fields": total_doc_fields,
            "avg_duty_of_care_score": avg_duty_of_care_score,
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
        print(f"\nContextual Integrity (CI) Metrics:")
        print(
            f"  Form CI violations: {total_form_ci_violations} (tasks: {tasks_with_form_ci_violations}/{n_evals})"
        )
        print(
            f"  Conversation CI violations: {total_conv_ci_violations} (tasks: {tasks_with_conv_ci_violations}/{n_evals})"
        )
        print(f"\nDue Diligence Metrics:")
        print(f"  Total masked fields: {total_dd_fields}")
        print(f"  Masked Field Correctness:")
        print(f"    Average accuracy: {avg_mf_accuracy:.2%}")
        print(f"\nDuty of Care Metrics:")
        print(f"  Total fields evaluated: {total_doc_fields}")
        doc_score_display = (
            f"{avg_duty_of_care_score:.2f}" if avg_duty_of_care_score is not None else "N/A"
        )
        print(f"  Average min duty of care score: {doc_score_display}")
        # Print the worst field across all evaluated tasks (skip N/A fields)
        worst_field = None
        for e in evaluation_results:
            for fe in e.duty_of_care.field_evaluations:
                if fe.overall_score is None:
                    continue
                if worst_field is None or fe.overall_score < worst_field.overall_score:
                    worst_field = fe
        if worst_field is not None:
            answer_display = (
                worst_field.agent_answer if worst_field.agent_answer.strip() else "<empty>"
            )
            print(f"  Worst field: {worst_field.field_label} ({worst_field.field_id})")
            print(f"    Agent's answer: {answer_display}")
            print(f"    Negative fact inclusion: {worst_field.negative_fact_inclusion_score}/3")
            print(f"    Framing quality:         {worst_field.framing_quality_score}/3")
            print(f"    Scope discipline:        {worst_field.scope_discipline_score}/3")
            print(f"    Advocacy effectiveness:  {worst_field.advocacy_effectiveness_score}/3")
            print(f"    Overall: {worst_field.overall_score:.2f}")
        print(f"\nValidation rate: {validation_rate:.1%}")

    return result
