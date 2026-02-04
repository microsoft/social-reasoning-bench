import argparse
import asyncio
import logging
import signal
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from pydantic_core import to_json
from sage_llm import ModelClient, clear_traces, get_tracer, save_traces

from .agents.assistant import get_system_prompt, list_available_presets
from .checkpoints import CheckpointManager, RunConfig
from .evaluation.evaluator import (
    compute_evaluation_summary,
    evaluate_tasks,
    print_evaluation_summary,
    print_per_task_summary,
)
from .loader import load_artifacts, load_tasks
from .run_paths import RunPaths
from .runner import run_tasks
from .types import BenchmarkMetadata, BenchmarkOutput

logger = logging.getLogger(__name__)


def _str_to_bool(value: str) -> bool:
    if value.lower() == "true":
        return True
    if value.lower() == "false":
        return False
    raise argparse.ArgumentTypeError(f"Expected 'true' or 'false', got '{value}'")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Calendar scheduling benchmark - runs tasks and evaluates results",
        allow_abbrev=False,
    )
    parser.add_argument(
        "paths",
        nargs="*",
        help="YAML files or directories containing task definitions (optional when resuming)",
    )
    parser.add_argument(
        "--max-rounds",
        type=int,
        default=20,
        help="Maximum conversation rounds per task (default: 20)",
    )
    parser.add_argument(
        "--max-steps-per-turn",
        type=int,
        default=20,
        help="Maximum tool calls per agent turn (default: 20)",
    )

    # Default model options (can be overridden by agent-specific options)
    parser.add_argument(
        "--model",
        help="Default model for all agents",
    )
    parser.add_argument(
        "--base-url",
        default=None,
        help="Default base URL for OpenAI-compatible API",
    )
    parser.add_argument(
        "--api-version",
        default=None,
        help="Default API version for all agents",
    )

    # Assistant agent options
    parser.add_argument(
        "--assistant-model",
        default=None,
        help="Model for assistant agent (overrides --model)",
    )
    parser.add_argument(
        "--assistant-base-url",
        default=None,
        help="Base URL for assistant agent's OpenAI-compatible API (overrides --base-url)",
    )
    parser.add_argument(
        "--assistant-api-version",
        default=None,
        help="API version for assistant agent (overrides --api-version)",
    )

    # Requestor agent options
    parser.add_argument(
        "--requestor-model",
        default=None,
        help="Model for requestor agent (overrides --model)",
    )
    parser.add_argument(
        "--requestor-base-url",
        default=None,
        help="Base URL for requestor agent's OpenAI-compatible API (overrides --base-url)",
    )
    parser.add_argument(
        "--requestor-api-version",
        default=None,
        help="API version for requestor agent (overrides --api-version)",
    )

    # Logging options
    parser.add_argument(
        "--log-level",
        default="info",
        choices=["debug", "info", "warning", "error"],
        help="Logging level (default: info)",
    )

    # Judge (evaluation) options
    parser.add_argument(
        "--judge-model",
        default=None,
        help="Model for LLM-as-judge evaluation (overrides --model)",
    )
    parser.add_argument(
        "--judge-base-url",
        default=None,
        help="Base URL for judge's OpenAI-compatible API (overrides --base-url)",
    )
    parser.add_argument(
        "--judge-api-version",
        default=None,
        help="API version for judge (overrides --api-version)",
    )

    # Artifacts option
    parser.add_argument(
        "--artifacts",
        default=None,
        help="Path to artifacts JSON file to inject into assistant context",
    )

    # System prompt options
    parser.add_argument(
        "--assistant-system-prompt",
        choices=list_available_presets(),
        help="System prompt preset for assistant agent (required when not resuming)",
    )
    parser.add_argument(
        "--assistant-system-prompt-file",
        type=Path,
        default=None,
        help="Path to custom system prompt file (overrides --assistant-system-prompt)",
    )

    # Task limiting option
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Limit the number of tasks to load (default: None, loads all tasks)",
    )

    # Batch size for parallelization
    parser.add_argument(
        "--batch-size",
        type=int,
        default=32,
        help="Number of tasks/evals to run in parallel (default: 32)",
    )

    # Preference exposure option
    parser.add_argument(
        "--expose-preferences",
        type=_str_to_bool,
        default=None,
        metavar="{true,false}",
        help="Include (true) or exclude (false) scheduling preferences in assistant agent prompt",
    )

    # Reasoning effort options
    parser.add_argument(
        "--reasoning-effort",
        "-r",
        choices=["none", "minimal", "low", "medium", "high", "xhigh", "default"],
        default=None,
        help="Default reasoning effort level for all agents (gpt-5.x, gemini)",
    )
    parser.add_argument(
        "--assistant-reasoning-effort",
        choices=["none", "minimal", "low", "medium", "high", "xhigh", "default"],
        default=None,
        help="Reasoning effort for assistant agent (overrides --reasoning-effort)",
    )
    parser.add_argument(
        "--requestor-reasoning-effort",
        choices=["none", "minimal", "low", "medium", "high", "xhigh", "default"],
        default=None,
        help="Reasoning effort for requestor agent (overrides --reasoning-effort)",
    )
    parser.add_argument(
        "--judge-reasoning-effort",
        choices=["none", "minimal", "low", "medium", "high", "xhigh", "default"],
        default=None,
        help="Reasoning effort for judge (overrides --reasoning-effort)",
    )

    # Explicit CoT flags (enables explicit chain-of-thought prompting before tool calls)
    parser.add_argument(
        "--explicit-cot",
        type=_str_to_bool,
        default=None,
        metavar="{true,false}",
        help="Enable (true) or disable (false) explicit chain-of-thought prompting for all agents",
    )

    # Per-agent CoT overrides (optional, override --explicit-cot)
    parser.add_argument(
        "--assistant-explicit-cot",
        type=_str_to_bool,
        default=None,
        metavar="{true,false}",
        help="Explicit CoT override for assistant agent (overrides --explicit-cot)",
    )
    parser.add_argument(
        "--requestor-explicit-cot",
        type=_str_to_bool,
        default=None,
        metavar="{true,false}",
        help="Explicit CoT override for requestor agent (overrides --explicit-cot)",
    )

    # Resume and checkpoint options
    parser.add_argument(
        "--resume",
        nargs="?",
        const=True,
        default=None,
        help="Resume from checkpoint. Optionally specify run directory or checkpoint path.",
    )
    parser.add_argument(
        "--force-resume",
        action="store_true",
        default=False,
        help="Allow resume even if source files have changed (warn instead of error)",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Base directory for outputs (default: outputs/calendar_scheduling)",
    )

    args = parser.parse_args()

    # Validate args that are required for new runs but come from checkpoint on resume
    if not args.resume:
        if args.model is None and not all(
            [args.assistant_model, args.requestor_model, args.judge_model]
        ):
            parser.error(
                "--model is required when not resuming, unless --assistant-model, --requestor-model, and --judge-model are all specified"
            )
        if args.assistant_system_prompt is None:
            parser.error("--assistant-system-prompt is required when not resuming")
        if args.expose_preferences is None:
            parser.error("--expose-preferences {true,false} is required when not resuming")
        if args.explicit_cot is None:
            parser.error("--explicit-cot {true,false} is required when not resuming")

    return args


async def run():
    args = parse_args()

    load_dotenv()

    # Initialize LLM tracer to collect traces for all LiteLLM calls
    get_tracer()

    # Track state for resume
    skip_exec_keys: set[str] = set()
    skip_eval_keys: set[str] = set()
    prior_exec_results: list = []
    prior_eval_results: list = []
    config: RunConfig | None = None

    # Handle resume - load config from checkpoint first
    if args.resume:
        if isinstance(args.resume, str):
            run_output = RunPaths.from_path(Path(args.resume))
        else:
            raise ValueError(
                "When using --resume without a path, you must specify the run directory or checkpoint file"
            )

        # Ensure output directory exists
        run_output.ensure_dir()

        # Initialize checkpoint manager and load checkpoint
        checkpoint_mgr = CheckpointManager(run_output.checkpoint_path)
        existing_checkpoint = checkpoint_mgr.load()

        if existing_checkpoint and existing_checkpoint.config:
            # Use config from checkpoint
            loaded_config = existing_checkpoint.config
            config = loaded_config
            logger.info("Loaded configuration from checkpoint")

            # Load tasks using paths from checkpoint config
            loaded = load_tasks(loaded_config.paths, limit=loaded_config.limit)
            tasks_with_keys = loaded.all_tasks

            # Validate source file hashes haven't changed
            for filename, saved_hash in existing_checkpoint.source_file_hashes.items():
                if filename not in loaded.file_hashes:
                    msg = f"Source file from checkpoint not found: {filename}"
                    if args.force_resume:
                        logger.warning(msg)
                    else:
                        raise ValueError(f"{msg}. Use --force-resume to continue anyway.")
                    continue

                current_hash = loaded.file_hashes[filename]
                if current_hash != saved_hash:
                    msg = f"Source file changed since checkpoint: {filename}"
                    if args.force_resume:
                        logger.warning(msg)
                    else:
                        raise ValueError(f"{msg}. Use --force-resume to continue anyway.")

            # Load completed task keys and results
            skip_exec_keys = checkpoint_mgr.get_completed_task_keys()
            skip_eval_keys = checkpoint_mgr.get_completed_eval_keys()
            prior_exec_results = checkpoint_mgr.get_execution_results()
            prior_eval_results = checkpoint_mgr.get_evaluation_results()

            logger.info(
                "Resuming: %d/%d executions, %d/%d evaluations already complete",
                len(skip_exec_keys),
                len(tasks_with_keys),
                len(skip_eval_keys),
                len(tasks_with_keys),
            )
        else:
            raise ValueError(
                f"No valid checkpoint found at {run_output.checkpoint_path}. "
                "Cannot resume without a checkpoint."
            )
    else:
        # New run - require paths
        if not args.paths:
            raise ValueError(
                "Task paths are required when not resuming. Use --resume to continue a previous run."
            )

        # Create config from CLI arguments
        new_config = RunConfig.from_args(args)
        config = new_config

        # Resolve model names for output directory naming
        assistant_model = new_config.resolved_assistant_model
        requestor_model = new_config.resolved_requestor_model
        judge_model = new_config.resolved_judge_model

        # Create new run output directory
        if args.output_dir:
            run_output = RunPaths(args.output_dir)
        else:
            run_output = RunPaths.create_for_run(assistant_model, requestor_model, judge_model)

        # Ensure output directory exists
        run_output.ensure_dir()

        # Initialize checkpoint manager
        checkpoint_mgr = CheckpointManager(run_output.checkpoint_path)

        # Load tasks with content-based keys
        loaded = load_tasks(new_config.paths, limit=new_config.limit)
        tasks_with_keys = loaded.all_tasks

        # Initialize new checkpoint with config
        metadata = BenchmarkMetadata(
            timestamp=datetime.now().isoformat(),
            assistant_model=new_config.resolved_assistant_model,
            requestor_model=new_config.resolved_requestor_model,
            judge_model=new_config.resolved_judge_model,
            max_rounds=new_config.max_rounds,
            batch_size=new_config.batch_size,
            task_count=len(tasks_with_keys),
            system_prompt=new_config.assistant_system_prompt,
            expose_preferences=new_config.expose_preferences,
        )
        checkpoint_mgr.initialize(new_config, metadata, loaded.file_hashes)

    # At this point, config is guaranteed to be set
    assert config is not None

    # Resolve model names from config
    assistant_model = config.resolved_assistant_model
    requestor_model = config.resolved_requestor_model
    judge_model = config.resolved_judge_model

    # Resolve reasoning effort with fallback to defaults
    assistant_reasoning_effort = config.assistant_reasoning_effort or config.reasoning_effort
    requestor_reasoning_effort = config.requestor_reasoning_effort or config.reasoning_effort
    judge_reasoning_effort = config.judge_reasoning_effort or config.reasoning_effort

    # Configure logging with file handler
    log_level = getattr(logging, args.log_level.upper())
    logging.basicConfig(
        level=log_level,
        format="%(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(run_output.get_log_path()),
        ],
    )

    logger.info("Output directory: %s", run_output.output_dir)

    # Resolve explicit CoT flags: per-agent overrides take precedence when set
    assistant_explicit_cot = (
        config.assistant_explicit_cot
        if config.assistant_explicit_cot is not None
        else config.explicit_cot
    )
    requestor_explicit_cot = (
        config.requestor_explicit_cot
        if config.requestor_explicit_cot is not None
        else config.explicit_cot
    )

    # Create model clients (reasoning_effort is passed normally, CoT is handled separately)
    # Initialize model clients
    assistant_client = ModelClient(
        base_url=config.assistant_base_url or config.base_url,
        api_version=config.assistant_api_version or config.api_version,
        reasoning_effort=assistant_reasoning_effort,
    )
    requestor_client = ModelClient(
        base_url=config.requestor_base_url or config.base_url,
        api_version=config.requestor_api_version or config.api_version,
        reasoning_effort=requestor_reasoning_effort,
    )
    judge_client = ModelClient(
        base_url=config.judge_base_url or config.base_url,
        api_version=config.judge_api_version or config.api_version,
        reasoning_effort=judge_reasoning_effort,
    )

    # Load artifacts if provided
    artifacts_by_task = None
    if config.artifacts:
        logger.info(f"Loading artifacts from {config.artifacts}...")
        artifacts_by_task = load_artifacts(config.artifacts)

    # Resolve system prompt
    if config.assistant_system_prompt_file:
        prompt_file = Path(config.assistant_system_prompt_file)
        if not prompt_file.exists():
            raise FileNotFoundError(f"System prompt file not found: {prompt_file}")
        system_prompt: str | None = prompt_file.read_text().strip()
        logger.info(f"Using custom system prompt from {prompt_file}")
    else:
        system_prompt = get_system_prompt(config.assistant_system_prompt)
        if system_prompt is None:
            logger.info("Running without system prompt")
        else:
            logger.info(f"Using system prompt preset: {config.assistant_system_prompt}")

    # Set up signal handlers for graceful interruption using asyncio
    loop = asyncio.get_event_loop()
    main_task: asyncio.Task | None = None

    def signal_handler():
        logger.warning("Interrupt received, cancelling tasks and saving checkpoint...")
        checkpoint_mgr.set_interrupted(True)
        if main_task is not None:
            main_task.cancel()

    # Use asyncio signal handlers for proper task cancellation
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, signal_handler)

    async def run_benchmark():
        """Inner coroutine that can be cancelled."""
        nonlocal prior_exec_results, prior_eval_results

        # Execution phase
        logger.info("Running %d task(s)...", len(tasks_with_keys) - len(skip_exec_keys))
        new_exec_results = await run_tasks(
            tasks=tasks_with_keys,
            assistant_model=assistant_model,
            assistant_client=assistant_client,
            requestor_model=requestor_model,
            requestor_client=requestor_client,
            max_rounds=config.max_rounds,
            max_steps_per_turn=config.max_steps_per_turn,
            batch_size=config.batch_size,
            artifacts_by_task=artifacts_by_task,
            system_prompt=system_prompt,
            assistant_explicit_cot=assistant_explicit_cot,
            requestor_explicit_cot=requestor_explicit_cot,
            expose_preferences=config.expose_preferences,
            on_task_complete=checkpoint_mgr.add_execution_result,
            skip_task_keys=skip_exec_keys if skip_exec_keys else None,
        )

        # Merge with prior results
        all_exec_results = prior_exec_results + new_exec_results

        # Evaluation phase
        logger.info(
            "Evaluating %d execution results...", len(all_exec_results) - len(skip_eval_keys)
        )
        new_eval_results = await evaluate_tasks(
            execution_results=all_exec_results,
            model=judge_model,
            model_client=judge_client,
            batch_size=config.batch_size,
            on_task_complete=checkpoint_mgr.add_evaluation_result,
            skip_task_keys=skip_eval_keys if skip_eval_keys else None,
        )

        # Merge with prior results
        all_eval_results = prior_eval_results + new_eval_results

        # Sort results by task index for consistent ordering
        all_eval_results = sorted(all_eval_results, key=lambda r: r.execution.task_index)

        # Create final output
        final_metadata = BenchmarkMetadata(
            timestamp=datetime.now().isoformat(),
            assistant_model=assistant_model,
            requestor_model=requestor_model,
            judge_model=judge_model,
            max_rounds=config.max_rounds,
            batch_size=config.batch_size,
            task_count=len(tasks_with_keys),
            system_prompt=config.assistant_system_prompt,
            expose_preferences=config.expose_preferences,
        )
        summary = compute_evaluation_summary(all_eval_results)
        output = BenchmarkOutput(metadata=final_metadata, summary=summary, results=all_eval_results)

        # Write final output
        run_output.eval_path.write_bytes(to_json(output, indent=2))
        logger.info(
            "Saved %d evaluation results to %s", len(all_eval_results), run_output.eval_path
        )

        # Save LLM traces
        traces_path = run_output.get_traces_path()
        save_traces(traces_path)
        logger.info("Saved LLM traces to %s", traces_path)

        # Cleanup checkpoint on success
        checkpoint_mgr.cleanup()

        print_per_task_summary(all_eval_results)
        print_evaluation_summary(summary)

    # Run the benchmark as a cancellable task
    try:
        main_task = asyncio.create_task(run_benchmark())
        await main_task
    except asyncio.CancelledError:
        logger.info("Run cancelled, checkpoint saved to %s", run_output.checkpoint_path)
        traces_path = run_output.get_traces_path()
        save_traces(traces_path)
        logger.info("Saved LLM traces to %s", traces_path)
        logger.info(
            "To resume: uv run -m sage_benchmark.calendar_scheduling --resume %s",
            run_output.output_dir,
        )


def main():
    asyncio.run(run())


if __name__ == "__main__":
    main()
