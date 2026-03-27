"""CLI for form filling benchmark (interactive mode)."""

import argparse
import asyncio
import json
import logging
import signal
from pathlib import Path

from dotenv import load_dotenv

from sage_benchmark.form_filling.checkpoints import CheckpointManager
from sage_benchmark.form_filling.loader import load_all_form_tasks
from sage_benchmark.form_filling.runner import run_tasks
from sage_benchmark.form_filling.schemas import InteractiveTaskExecutionResult
from sage_benchmark.shared.cli_utils import parse_reasoning_effort
from sage_benchmark.shared.logging import create_benchmark_logger

logger = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Form filling benchmark")

    # Model configuration
    parser.add_argument(
        "--assistant-model",
        required=True,
        help="Model for assistant agent (interactive mode)",
    )
    parser.add_argument(
        "--interviewer-model",
        required=True,
        help="Model for interviewer agent (interactive mode)",
    )
    parser.add_argument(
        "--interviewer-form-fill-model",
        default=None,
        help="Separate model for the form-filling step after the interview (defaults to --interviewer-model). "
        "Useful when the interviewer model doesn't support constrained decoding.",
    )

    # Common arguments
    parser.add_argument(
        "--data", required=True, help="Path to task directory (e.g., data/form-filling/tasks)"
    )
    parser.add_argument("--judge-model", default="gpt-4.1", help="Model for evaluation")
    parser.add_argument(
        "--base-url",
        type=str,
        default=None,
        help="Base URL for OpenAI-compatible API (e.g., http://localhost:8001/v1 for vLLM)",
    )
    parser.add_argument("--output-dir", default="outputs/form_filling", help="Output directory")
    parser.add_argument("--limit", type=int, default=None, help="Limit number of tasks to run")
    parser.add_argument(
        "--id",
        type=int,
        default=None,
        help="Run only the task at this index (0-based). Must be less than total number of tasks.",
    )
    parser.add_argument(
        "--run-mode",
        choices=["all", "eval"],
        default="all",
        help="Run mode: 'all' (execute + evaluate), 'eval' (re-evaluate with prior exec results)",
    )
    parser.add_argument(
        "--task-results-path",
        help="Path to task_results.json file (required for --run-mode eval)",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=75,
        help="Number of tasks/evals to run in parallel (default: 75)",
    )
    parser.add_argument(
        "--max-concurrent-requests",
        type=int,
        default=100,
        help="Maximum concurrent API requests per client (default: 100)",
    )

    parser.add_argument(
        "--logger",
        choices=["verbose", "progress", "quiet"],
        default="progress",
        help="Logging style: verbose, progress (tqdm), or quiet (default: progress). "
        "Note: not yet fully wired into form-filling runner.",
    )

    # Prompt type
    parser.add_argument(
        "--prompt-type",
        type=str,
        default="base",
        choices=["base", "privacy_aware", "privacy_explained", "privacy_ci"],
        help='Type of prompt to use for the agent (default: "base")',
    )

    # Interactive mode specific arguments
    parser.add_argument(
        "--max-rounds",
        type=int,
        default=50,
        help="Maximum conversation rounds per task in interactive mode (default: 50)",
    )
    parser.add_argument(
        "--interviewer-reasoning-effort",
        type=parse_reasoning_effort,
        default=None,
        help="Reasoning effort for interviewer agent: none/minimal/low/medium/high/xhigh/default, or integer budget tokens",
    )
    parser.add_argument(
        "--assistant-reasoning-effort",
        type=parse_reasoning_effort,
        default=None,
        help="Reasoning effort for assistant agent: none/minimal/low/medium/high/xhigh/default, or integer budget tokens",
    )
    parser.add_argument(
        "--judge-reasoning-effort",
        type=parse_reasoning_effort,
        default=None,
        help="Reasoning effort for judge: none/minimal/low/medium/high/xhigh/default, or integer budget tokens",
    )
    parser.add_argument(
        "--interviewer-type",
        type=str,
        default="base",
        choices=["base", "detail"],
        help="Type of interviewer prompt in interactive mode: 'base' or 'detail' (default: 'base')",
    )
    parser.add_argument(
        "--single-field-mode",
        action="store_true",
        help="If set, interviewer asks only one question per turn",
    )
    parser.add_argument(
        "--malicious-strategy",
        type=int,
        default=None,
        help="Use malicious interviewer with the n-th strategy (0-indexed) from strategies file. "
        "When set, overrides --interviewer-type.",
    )
    parser.add_argument(
        "--malicious-attack-type",
        choices=["privacy", "hallucination", "red_flags"],
        default="privacy",
        help="Type of malicious attack (only used with --malicious-strategy)",
    )
    parser.add_argument(
        "--malicious-strategies-file",
        type=str,
        default=None,
        help="Path to strategies YAML file for malicious mode. Required when --malicious-strategy is set.",
    )

    parser.add_argument(
        "--social-reasoning",
        action="store_true",
        help="Enable social reasoning for assistant agent (ToM-augmented)",
    )
    parser.add_argument(
        "--use-privacy-example",
        action="store_true",
        help="Append privacy/sensitive information examples to the social reasoning prompt (requires --social-reasoning)",
    )

    # Logging style
    parser.add_argument(
        "--logger",
        default="progress",
        choices=["verbose", "progress", "quiet"],
        help="Logging style: verbose, progress (default, tqdm bar), quiet (minimal)",
    )

    # Resume / checkpoint
    parser.add_argument(
        "--resume",
        nargs="?",
        const=True,
        default=None,
        help="Resume from checkpoint. Optionally specify the checkpoint JSON path.",
    )

    return parser.parse_args()


def _load_prior_exec_results(
    task_results_path: str, data_path: str
) -> list[InteractiveTaskExecutionResult]:
    """Load execution results from a prior run's task_results.json file.

    Args:
        task_results_path: Path to task_results.json from a prior run
        data_path: Path to task data directory (for reconstructing FormTask objects)

    Returns:
        List of InteractiveTaskExecutionResult from the prior run
    """
    logger.info("Loading task results from: %s", task_results_path)
    with open(task_results_path) as f:
        task_results_data = json.load(f)

    tasks = load_all_form_tasks(data_path)
    task_map = {task.form_id: task for task in tasks}

    execution_results: list[InteractiveTaskExecutionResult] = []
    for task_result_data in task_results_data:
        exec_data = task_result_data["execution"]
        form_id = task_result_data["form_id"]

        if form_id not in task_map:
            logger.warning("Form %s not found, skipping", form_id)
            continue

        exec_result = InteractiveTaskExecutionResult.model_validate(
            {**exec_data, "task": task_map[form_id], "form_id": form_id}
        )
        execution_results.append(exec_result)

    return execution_results


def main():
    """Main runner for form filling tasks."""
    args = parse_args()

    load_dotenv()

    # Configure logging
    logging.basicConfig(level=logging.INFO, format="%(message)s")

    if args.run_mode == "eval" and not args.task_results_path:
        raise ValueError("--task-results-path is required when using --run-mode eval")

    if args.malicious_strategy is not None and not args.malicious_strategies_file:
        raise ValueError(
            "--malicious-strategies-file is required when --malicious-strategy is set. "
            "Generate strategies first using: uv run --package sage-data-gen python -m "
            f"sage_data_gen.form_filling.malicious.whimsical.{args.malicious_attack_type} "
            "-m <model> -o <output.yaml>"
        )

    # Create benchmark logger
    benchmark_logger = create_benchmark_logger(args.logger)

    # Handle checkpoint/resume
    checkpoint_mgr: CheckpointManager | None = None
    skip_exec_keys: set[str] = set()
    skip_eval_keys: set[str] = set()
    prior_exec_results: list[InteractiveTaskExecutionResult] = []

    if args.run_mode == "eval":
        # Re-evaluate mode: load prior exec results, skip all execution
        prior_exec_results = _load_prior_exec_results(args.task_results_path, args.data)
        skip_exec_keys = {r.form_id for r in prior_exec_results}
        # skip_eval_keys stays empty -> re-evaluate all
        logger.info(
            "Eval mode: loaded %d prior exec results, will re-evaluate all",
            len(prior_exec_results),
        )

    elif args.resume is not None:
        # Resume mode: skip tasks that are fully done (exec + eval)
        if isinstance(args.resume, str):
            checkpoint_path = Path(args.resume)
            if checkpoint_path.is_dir():
                checkpoint_path = checkpoint_path / "checkpoint.json"
        else:
            # --resume without a path: look in output_dir
            checkpoint_path = Path(args.output_dir) / "checkpoint.json"

        checkpoint_mgr = CheckpointManager(checkpoint_path)
        existing = checkpoint_mgr.load()

        if existing is not None:
            completed_exec = checkpoint_mgr.get_completed_task_keys()
            completed_eval = checkpoint_mgr.get_completed_eval_keys()

            # Tasks with both exec + eval done: skip entirely
            skip_eval_keys = completed_exec & completed_eval

            # Tasks with exec done but not eval: reuse exec, re-evaluate
            exec_only_keys = completed_exec - completed_eval
            if exec_only_keys:
                skip_exec_keys = exec_only_keys
                prior_exec_results = [
                    r for r in checkpoint_mgr.get_execution_results() if r.form_id in exec_only_keys
                ]

            logger.info(
                "Resuming: %d fully done (skip), %d exec-only (re-eval), %d remaining",
                len(skip_eval_keys),
                len(exec_only_keys),
                -1,  # placeholder; actual count computed in runner
            )
        else:
            raise ValueError(
                f"No checkpoint found at {checkpoint_path}. "
                "Drop the --resume flag to start a new run."
            )
    else:
        # New run - create checkpoint in output_dir for incremental saves
        output_path = Path(args.output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        checkpoint_path = output_path / "checkpoint.json"
        checkpoint_mgr = CheckpointManager(checkpoint_path)
        checkpoint_mgr.initialize()

    # Set up SIGINT handler for graceful interruption
    loop = asyncio.new_event_loop()

    def sigint_handler():
        logger.warning("Interrupt received, saving checkpoint...")
        if checkpoint_mgr is not None:
            checkpoint_mgr.set_interrupted(True)
        # Remove handler so second Ctrl+C forces exit
        for sig in (signal.SIGINT, signal.SIGTERM):
            try:
                loop.remove_signal_handler(sig)
            except (ValueError, RuntimeError):
                pass

    async def _run():
        # Install signal handlers within the running loop
        running_loop = asyncio.get_event_loop()
        for sig in (signal.SIGINT, signal.SIGTERM):
            running_loop.add_signal_handler(sig, sigint_handler)

        try:
            with benchmark_logger:
                return await run_tasks(
                    data_path=args.data,
                    model_name=args.assistant_model,
                    interviewer_model=args.interviewer_model,
                    interviewer_form_fill_model=args.interviewer_form_fill_model,
                    judge_model=args.judge_model,
                    base_url=args.base_url,
                    output_dir=args.output_dir,
                    limit=args.limit,
                    task_id=args.id,
                    batch_size=args.batch_size,
                    max_concurrent_requests=args.max_concurrent_requests,
                    prompt_type=args.prompt_type,
                    interviewer_reasoning_effort=args.interviewer_reasoning_effort,
                    assistant_reasoning_effort=args.assistant_reasoning_effort,
                    judge_reasoning_effort=args.judge_reasoning_effort,
                    max_rounds=args.max_rounds,
                    interviewer_type=args.interviewer_type,
                    single_field_mode=args.single_field_mode,
                    malicious_strategy=args.malicious_strategy,
                    malicious_attack_type=args.malicious_attack_type,
                    malicious_strategies_file=args.malicious_strategies_file,
                    social_reasoning=args.social_reasoning,
                    use_privacy_example=args.use_privacy_example,
                    benchmark_logger=benchmark_logger,
                    checkpoint_mgr=checkpoint_mgr,
                    skip_exec_keys=skip_exec_keys,
                    skip_eval_keys=skip_eval_keys,
                    prior_exec_results=prior_exec_results,
                )
        finally:
            # Remove signal handlers
            running_loop = asyncio.get_event_loop()
            for sig in (signal.SIGINT, signal.SIGTERM):
                try:
                    running_loop.remove_signal_handler(sig)
                except (ValueError, RuntimeError):
                    pass

    asyncio.run(_run())


if __name__ == "__main__":
    main()
