"""Async runner for form filling benchmark (interactive mode only).

Supports coupled execution+evaluation, checkpoint/resume, and BenchmarkLogger.
"""

import json
import logging
import traceback
from datetime import datetime
from pathlib import Path

from sage_llm import ModelClient

from sage_benchmark.form_filling.checkpoints import CheckpointManager
from sage_benchmark.form_filling.evaluation import (
    evaluate_interactive_task,
)
from sage_benchmark.form_filling.evaluation_summary import (
    compute_summary,
    print_evaluation_summary,
    print_per_task_summary,
)
from sage_benchmark.form_filling.interactive import run_single_task as run_interactive_task
from sage_benchmark.form_filling.loader import load_all_form_tasks
from sage_benchmark.form_filling.schemas import (
    FormFillingBenchmarkMetadata,
    FormFillingBenchmarkOutput,
    FormTask,
    InteractiveTaskEvaluationResult,
    InteractiveTaskExecutionResult,
)
from sage_benchmark.shared.errors import is_fatal_error
from sage_benchmark.shared.logging import BenchmarkLogger, VerboseLogger

logger = logging.getLogger(__name__)


def normalize_model_name(name: str) -> str:
    """Normalize model name for use in file paths and JSON output.

    Replaces '/' with '_' to avoid path issues.
    """
    if name is None:
        return name
    return name.replace("/", "_")


def append_batch_to_json_list(path: Path, items: list[dict]):
    """Append multiple items to a JSON array file.

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
    max_steps_per_turn: int = 5,
    benchmark_logger: BenchmarkLogger | None = None,
    checkpoint_mgr: CheckpointManager | None = None,
    skip_exec_keys: set[str] | None = None,
    skip_eval_keys: set[str] | None = None,
    prior_exec_results: list[InteractiveTaskExecutionResult] | None = None,
    explicit_cot: bool = False,
):
    """Run the complete form filling benchmark with coupled execution+evaluation.

    Uses a single code path controlled by skip sets (matching calendar pattern):
    - Normal run: both skip sets empty -> execute + evaluate everything
    - Resume: skip sets populated from checkpoint -> skip completed work
    - Re-eval: skip_exec_keys = ALL keys, skip_eval_keys = empty -> re-evaluate all

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
        batch_size: Number of tasks/evals to run in parallel
        max_concurrent_requests: Maximum concurrent API requests per client
        prompt_type: Type of prompt to use
        interviewer_reasoning_effort: Reasoning effort for interviewer agent
        assistant_reasoning_effort: Reasoning effort for assistant agent
        judge_reasoning_effort: Reasoning effort level for judge model
        max_rounds: Maximum conversation rounds
        interviewer_type: Type of interviewer prompt ("base" or "detail")
        single_field_mode: If True, interviewer asks only one question per turn
        malicious_strategy: If set, use malicious interviewer with this strategy index
        malicious_attack_type: Type of malicious attack
        malicious_strategies_file: Path to strategies YAML file for malicious mode
        temperature: Sampling temperature for assistant/form-filler generation
        max_steps_per_turn: Maximum tool calls per assistant turn (default: 5)
        benchmark_logger: Logger for progress output (defaults to VerboseLogger)
        checkpoint_mgr: Checkpoint manager for saving progress
        skip_exec_keys: Set of task keys (form_ids) to skip execution for (reuse prior)
        skip_eval_keys: Set of task keys (form_ids) to skip entirely
        prior_exec_results: Prior execution results to reuse when skipping execution
        explicit_cot: If True, enable explicit chain-of-thought prompting for assistant

    Returns:
        FormFillingBenchmarkOutput with structured metadata, summary, and results.
    """
    if benchmark_logger is None:
        benchmark_logger = VerboseLogger()
    if skip_exec_keys is None:
        skip_exec_keys = set()
    if skip_eval_keys is None:
        skip_eval_keys = set()
    if prior_exec_results is None:
        prior_exec_results = []

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
        benchmark_logger.log_message(logging.INFO, "Run directory: %s", run_dir)
    else:
        run_dir = None
        task_results_file = None
        eval_results_file = None
        summary_file = None

    # Load tasks
    tasks = load_all_form_tasks(data_path)
    benchmark_logger.log_message(
        logging.INFO, "Loaded %d form tasks from %s", len(tasks), data_path
    )

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
        benchmark_logger.log_message(logging.INFO, "Running only task at index %d", task_id)
    elif limit:
        tasks = tasks[:limit]
        benchmark_logger.log_message(logging.INFO, "Running first %d tasks", limit)

    result = await _run_interactive_mode(
        tasks=tasks,
        assistant_model=model_name,
        interviewer_model=interviewer_model,
        interviewer_form_fill_model=interviewer_form_fill_model,
        judge_model=judge_model,
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
        max_steps_per_turn=max_steps_per_turn,
        benchmark_logger=benchmark_logger,
        checkpoint_mgr=checkpoint_mgr,
        skip_exec_keys=skip_exec_keys,
        skip_eval_keys=skip_eval_keys,
        prior_exec_results=prior_exec_results,
        explicit_cot=explicit_cot,
    )

    return result


async def _run_interactive_mode(
    tasks: list[FormTask],
    assistant_model: str,
    interviewer_model: str,
    interviewer_form_fill_model: str | None,
    judge_model: str,
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
    max_steps_per_turn: int = 5,
    benchmark_logger: BenchmarkLogger | None = None,
    checkpoint_mgr: CheckpointManager | None = None,
    skip_exec_keys: set[str] | None = None,
    skip_eval_keys: set[str] | None = None,
    prior_exec_results: list[InteractiveTaskExecutionResult] | None = None,
    explicit_cot: bool = False,
):
    """Run interactive mode with a single code path controlled by skip sets.

    Skip sets are checked independently for each task:
    - Neither skipped: exec + eval (normal)
    - Skip exec only: reuse prior exec result, still eval (reeval)
    - Skip eval only: exec, skip eval (exec-only)
    - Both skipped: skip entirely (fully done resume)
    """
    if benchmark_logger is None:
        benchmark_logger = VerboseLogger()
    if skip_exec_keys is None:
        skip_exec_keys = set()
    if skip_eval_keys is None:
        skip_eval_keys = set()
    if prior_exec_results is None:
        prior_exec_results = []

    # Build lookup for prior execution results
    prior_exec_by_key: dict[str, InteractiveTaskExecutionResult] = {
        r.form_id: r for r in prior_exec_results
    }

    execution_results: list[InteractiveTaskExecutionResult] = []
    evaluation_results: list[InteractiveTaskEvaluationResult] = []

    # If resuming, include prior results from checkpoint
    if checkpoint_mgr is not None:
        execution_results.extend(checkpoint_mgr.get_execution_results())
        evaluation_results.extend(checkpoint_mgr.get_evaluation_results())

    # Create async clients
    interviewer_client = ModelClient(reasoning_effort=interviewer_reasoning_effort)
    assistant_client = ModelClient(base_url=base_url, reasoning_effort=assistant_reasoning_effort)
    # Separate form-fill client if a different model is specified
    form_fill_client = ModelClient() if interviewer_form_fill_model else None
    effective_form_fill_model = interviewer_form_fill_model or None

    # Judge client (always needed - single code path always evaluates)
    judge_client = ModelClient(reasoning_effort=judge_reasoning_effort)

    # Count tasks that will be processed (skip only where BOTH exec and eval are done)
    tasks_to_process = [
        (idx, task)
        for idx, task in enumerate(tasks)
        if not (task.form_id in skip_exec_keys and task.form_id in skip_eval_keys)
    ]
    skipped_both = len(tasks) - len(tasks_to_process)
    skipped_exec = sum(1 for _, t in tasks_to_process if t.form_id in skip_exec_keys)

    if skipped_both > 0:
        benchmark_logger.log_message(
            logging.INFO,
            "Skipping %d fully-completed tasks",
            skipped_both,
        )
    if skipped_exec > 0:
        benchmark_logger.log_message(
            logging.INFO,
            "Reusing %d prior execution results (re-evaluating)",
            skipped_exec,
        )

    total_to_run = len(tasks_to_process)
    benchmark_logger.on_phase_start("execution+evaluation", total_to_run)

    completed = 0
    failed = 0

    for idx, task in tasks_to_process:
        form_id = task.form_id

        try:
            # --- Execution: skip or run ---
            if form_id in skip_exec_keys:
                exec_result = prior_exec_by_key.get(form_id)
                if exec_result is None:
                    raise RuntimeError(f"Task {form_id} in skip_exec_keys but no prior exec result")
            else:
                benchmark_logger.on_task_start(idx)

                exec_result = await run_interactive_task(
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
                    max_steps_per_turn=max_steps_per_turn,
                    explicit_cot=explicit_cot,
                )

                if checkpoint_mgr is not None:
                    checkpoint_mgr.add_execution_result(exec_result)

                # Incremental file save for execution
                if task_results_file:
                    append_batch_to_json_list(
                        task_results_file,
                        [
                            {
                                "task_index": exec_result.task_index,
                                "form_id": exec_result.form_id,
                                "execution": exec_result.model_dump(mode="json"),
                            }
                        ],
                    )

            execution_results.append(exec_result)

            if not exec_result.success:
                failed += 1
                benchmark_logger.on_task_complete(
                    idx, success=False, error=exec_result.error_message
                )
                continue

            # --- Evaluation: skip or run (independent of exec) ---
            if form_id in skip_eval_keys:
                completed += 1
                benchmark_logger.on_task_complete(idx, success=True)
                continue

            eval_result = await evaluate_interactive_task(exec_result, judge_client, judge_model)
            evaluation_results.append(eval_result)

            if checkpoint_mgr is not None:
                checkpoint_mgr.add_evaluation_result(eval_result)

            # Incremental file save for evaluation
            if eval_results_file:
                append_batch_to_json_list(
                    eval_results_file,
                    [
                        {
                            "task_index": eval_result.task_index,
                            "form_id": eval_result.form_id,
                            "evaluation": eval_result.model_dump(mode="json"),
                        }
                    ],
                )

            completed += 1
            benchmark_logger.on_task_complete(idx, success=True)

        except Exception as e:
            if is_fatal_error(e):
                raise
            logger.error("Task %d failed with exception: %s", idx, e)
            logger.error(traceback.format_exc())
            failed += 1
            benchmark_logger.on_task_complete(idx, success=False, error=str(e))

    benchmark_logger.on_phase_complete("execution+evaluation", completed, failed)

    # Build and return structured output
    return _build_interactive_summary(
        execution_results=execution_results,
        evaluation_results=evaluation_results,
        interviewer_model=interviewer_model,
        assistant_model=assistant_model,
        judge_model=judge_model,
        batch_size=batch_size,
        max_rounds=max_rounds,
        prompt_type=prompt_type,
        interviewer_type=interviewer_type,
        single_field_mode=single_field_mode,
        max_steps_per_turn=max_steps_per_turn,
        interviewer_reasoning_effort=interviewer_reasoning_effort,
        assistant_reasoning_effort=assistant_reasoning_effort,
        judge_reasoning_effort=judge_reasoning_effort,
        summary_file=summary_file,
    )


def _build_interactive_summary(
    execution_results: list[InteractiveTaskExecutionResult],
    evaluation_results: list[InteractiveTaskEvaluationResult],
    interviewer_model: str,
    assistant_model: str,
    judge_model: str,
    batch_size: int,
    max_rounds: int,
    prompt_type: str,
    interviewer_type: str,
    single_field_mode: bool,
    max_steps_per_turn: int,
    interviewer_reasoning_effort: str | None,
    assistant_reasoning_effort: str | None,
    judge_reasoning_effort: str | None,
    summary_file: Path | None,
) -> FormFillingBenchmarkOutput:
    """Build structured benchmark output for interactive mode."""
    metadata = FormFillingBenchmarkMetadata(
        timestamp=datetime.now().isoformat(),
        assistant_model=assistant_model,
        interviewer_model=interviewer_model,
        judge_model=judge_model,
        max_rounds=max_rounds,
        batch_size=batch_size,
        task_count=len(execution_results),
        prompt_type=prompt_type,
        interviewer_type=interviewer_type,
        single_field_mode=single_field_mode,
        max_steps_per_turn=max_steps_per_turn,
        interviewer_reasoning_effort=interviewer_reasoning_effort,
        assistant_reasoning_effort=assistant_reasoning_effort,
        judge_reasoning_effort=judge_reasoning_effort,
    )

    summary = compute_summary(execution_results, evaluation_results)

    output = FormFillingBenchmarkOutput(
        metadata=metadata,
        summary=summary,
        results=evaluation_results,
    )

    # Save structured output
    if summary_file:
        with open(summary_file, "w") as f:
            json.dump(output.model_dump(mode="json"), f, indent=2)
        print(f"\nSummary saved to: {summary_file}")

    # Print per-task table and aggregate summary
    print_per_task_summary(evaluation_results)
    print_evaluation_summary(summary)

    return output
