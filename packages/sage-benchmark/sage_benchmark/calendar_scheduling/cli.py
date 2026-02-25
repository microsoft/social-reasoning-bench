import argparse
import asyncio
import logging
import signal
import sys
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from pydantic_core import to_json
from sage_llm import ModelClient, clear_traces, get_tracer, save_traces

from sage_benchmark.shared.cli_utils import parse_reasoning_effort
from sage_benchmark.shared.logging import create_benchmark_logger

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


# ==============================================================================
# Argument group parsing utilities (-- / --with)
# ==============================================================================


def _split_on_and(argv: list[str]) -> list[list[str]]:
    """Split argv on --and separator into groups.

    Returns:
        List of arg groups. First group is base args, subsequent groups are --and groups.

    Example:
        ['--experiments', 'dir/', '--model', 'X', '--and', '--model', 'Y']
        -> [['--experiments', 'dir/', '--model', 'X'], ['--model', 'Y']]
    """
    groups: list[list[str]] = [[]]

    for arg in argv:
        if arg == "--and":
            groups.append([])
        else:
            groups[-1].append(arg)

    return groups


def _parse_override_group(
    parser: argparse.ArgumentParser,
    override_argv: list[str],
) -> dict:
    """Parse an override group and return a dict of overrides.

    Returns keys that were explicitly specified in override_argv
    and are override-eligible (model settings, etc.).
    """
    # Override-eligible args (things that make sense to override per experiment group)
    OVERRIDE_ARGS = {
        "model",
        "base_url",
        "api_version",
        "assistant_model",
        "assistant_base_url",
        "assistant_api_version",
        "requestor_model",
        "requestor_base_url",
        "requestor_api_version",
        "judge_model",
        "judge_base_url",
        "judge_api_version",
        "reasoning_effort",
        "assistant_reasoning_effort",
        "requestor_reasoning_effort",
        "judge_reasoning_effort",
        "explicit_cot",
        "assistant_explicit_cot",
        "requestor_explicit_cot",
        "expose_preferences",
        "assistant_system_prompt",
        "assistant_system_prompt_file",
        "max_rounds",
        "max_steps_per_turn",
        "batch_size",
        "limit",
    }

    # Parse the override args (unknown args are ignored)
    override_ns, _ = parser.parse_known_args(override_argv)

    # Extract arg names that were actually specified in the override argv
    specified_args = set()
    for arg in override_argv:
        if arg.startswith("--"):
            arg_name = arg[2:].replace("-", "_")
            specified_args.add(arg_name)

    # Only include override-eligible args that were explicitly specified
    overrides = {}
    for key, value in vars(override_ns).items():
        if key in specified_args and key in OVERRIDE_ARGS and value is not None:
            overrides[key] = value

    return overrides


def _variant_name(overrides: dict) -> str:
    """Create a readable variant name from overrides."""
    parts = []
    for key, value in overrides.items():
        # Shorten the key for display
        short_key = key.replace("_", "-")
        # Shorten the value if it's a model path
        if isinstance(value, str) and "/" in value:
            value = value.split("/")[-1]
        parts.append(f"{short_key}={value}")
    return ",".join(parts) if parts else "default"


def _str_to_bool(value: str) -> bool:
    if value.lower() == "true":
        return True
    if value.lower() == "false":
        return False
    raise argparse.ArgumentTypeError(f"Expected 'true' or 'false', got '{value}'")


def create_argument_parser() -> argparse.ArgumentParser:
    """Create the argument parser for CLI arguments.

    This is exposed so override parsing can reuse it.
    """
    parser = argparse.ArgumentParser(
        description="Calendar scheduling benchmark - runs tasks and evaluates results",
        allow_abbrev=False,
    )
    parser.add_argument(
        "--data",
        nargs="+",
        dest="paths",
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
    parser.add_argument(
        "--logger",
        default="verbose",
        choices=["verbose", "progress", "quiet"],
        help="Logging style: verbose (default), progress (tqdm bar), quiet (minimal)",
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
    parser.add_argument(
        "--judge-votes",
        type=int,
        default=3,
        help="Number of judge votes for majority voting in leakage detection (default: 3)",
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
        type=parse_reasoning_effort,
        default=None,
        help="Default reasoning effort: none/minimal/low/medium/high/xhigh/default, or integer budget tokens",
    )
    parser.add_argument(
        "--assistant-reasoning-effort",
        type=parse_reasoning_effort,
        default=None,
        help="Reasoning effort for assistant agent (overrides --reasoning-effort)",
    )
    parser.add_argument(
        "--requestor-reasoning-effort",
        type=parse_reasoning_effort,
        default=None,
        help="Reasoning effort for requestor agent (overrides --reasoning-effort)",
    )
    parser.add_argument(
        "--judge-reasoning-effort",
        type=parse_reasoning_effort,
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
        "--restart-eval",
        action="store_true",
        default=False,
        help="Re-run evaluation from scratch, ignoring checkpointed eval progress (use with --resume)",
    )
    parser.add_argument(
        "--restart-exec",
        action="store_true",
        default=False,
        help="Re-run execution from scratch, ignoring checkpointed exec progress (use with --resume)",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Base directory for outputs (default: outputs/calendar_scheduling)",
    )
    parser.add_argument(
        "--reeval",
        type=Path,
        default=None,
        help="Re-evaluate an existing output JSON file (skips execution, runs evaluation only)",
    )

    # Experiment mode arguments
    parser.add_argument(
        "--experiments",
        type=Path,
        default=None,
        help="Directory containing experiment Python files (experiment_*.py, experiments.py)",
    )
    parser.add_argument(
        "--collect-only",
        action="store_true",
        default=False,
        help="List discovered experiments without running them (requires --experiments)",
    )
    parser.add_argument(
        "-k",
        type=str,
        metavar="PATTERN",
        dest="experiment_pattern",
        help="Only run experiments matching this pattern (requires --experiments)",
    )

    return parser


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse CLI arguments with validation."""
    parser = create_argument_parser()
    args = parser.parse_args(argv)

    # Validate --reeval is mutually exclusive with --resume
    if args.reeval and args.resume:
        parser.error("--reeval and --resume are mutually exclusive")

    # Validate --experiments is mutually exclusive with other modes
    if args.experiments:
        if args.reeval:
            parser.error("--experiments and --reeval are mutually exclusive")
        if args.resume:
            parser.error("--experiments and --resume are mutually exclusive")
        if args.paths:
            parser.error("--experiments and --data are mutually exclusive")
        # In experiments mode, configs come from experiment files, not CLI
        return args

    # Validate args that are required for new runs but come from checkpoint on resume
    if not args.resume and not args.reeval:
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

    # Validate restart options require resume
    # --restart-eval and --restart-exec work with --resume or --experiments
    if args.restart_eval and not args.resume and not args.experiments:
        parser.error("--restart-eval requires --resume or --experiments")
    if args.restart_exec and not args.resume and not args.experiments:
        parser.error("--restart-exec requires --resume or --experiments")

    # Validate --reeval file exists
    if args.reeval and not args.reeval.exists():
        parser.error(f"--reeval file does not exist: {args.reeval}")

    return args


async def run_reeval(args: argparse.Namespace):
    """Re-evaluate an existing output JSON file with fresh evaluation."""
    import json

    # Load existing output
    logger.info("Loading existing output from %s", args.reeval)
    with open(args.reeval) as f:
        data = json.load(f)

    # Parse the output to extract execution results
    existing_output = BenchmarkOutput.model_validate(data)
    logger.info(
        "Loaded %d evaluation results from %s",
        len(existing_output.results),
        args.reeval,
    )

    # Extract execution results
    exec_results = [r.execution for r in existing_output.results]

    # Determine judge model - use CLI arg, fall back to original
    judge_model = args.judge_model or args.model or existing_output.metadata.judge_model
    judge_base_url = args.judge_base_url or args.base_url
    judge_api_version = args.judge_api_version or args.api_version
    judge_reasoning_effort = args.judge_reasoning_effort or args.reasoning_effort

    logger.info("Re-evaluating with judge model: %s", judge_model)

    # Create judge client
    judge_client = ModelClient(
        base_url=judge_base_url,
        api_version=judge_api_version,
        reasoning_effort=judge_reasoning_effort,
    )

    # Determine output path with timestamp
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    if args.output_dir:
        stem = args.reeval.stem
        output_path = args.output_dir / f"{stem}-reeval-{timestamp}.json"
    else:
        # Create output alongside input with suffix
        stem = args.reeval.stem
        output_path = args.reeval.parent / f"{stem}-reeval-{timestamp}.json"

    # Run evaluation
    logger.info("Evaluating %d execution results...", len(exec_results))
    eval_results = await evaluate_tasks(
        execution_results=exec_results,
        model=judge_model,
        model_client=judge_client,
        batch_size=args.batch_size,
        judge_votes=getattr(args, "judge_votes", 3),
    )

    # Sort by task id
    eval_results = sorted(eval_results, key=lambda r: r.execution.task.id or 0)

    # Create new output with updated metadata (preserve original settings, update judge)
    new_metadata = BenchmarkMetadata(
        timestamp=datetime.now().isoformat(),
        assistant_model=existing_output.metadata.assistant_model,
        requestor_model=existing_output.metadata.requestor_model,
        judge_model=judge_model,
        max_rounds=existing_output.metadata.max_rounds,
        batch_size=args.batch_size,
        task_count=len(eval_results),
        system_prompt=existing_output.metadata.system_prompt,
        expose_preferences=existing_output.metadata.expose_preferences,
        # Preserve original CoT/reasoning settings
        assistant_explicit_cot=existing_output.metadata.assistant_explicit_cot,
        assistant_reasoning_effort=existing_output.metadata.assistant_reasoning_effort,
        requestor_explicit_cot=existing_output.metadata.requestor_explicit_cot,
        requestor_reasoning_effort=existing_output.metadata.requestor_reasoning_effort,
        judge_reasoning_effort=str(judge_reasoning_effort) if judge_reasoning_effort else None,
    )
    summary = compute_evaluation_summary(eval_results)
    output = BenchmarkOutput(metadata=new_metadata, summary=summary, results=eval_results)

    # Write output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(to_json(output, indent=2))
    logger.info("Saved %d re-evaluation results to %s", len(eval_results), output_path)

    # Save traces
    traces_path = output_path.parent / f"llm-traces-{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    save_traces(traces_path)
    logger.info("Saved LLM traces to %s", traces_path)

    print_per_task_summary(eval_results)
    print_evaluation_summary(summary)


async def _run_experiments_with_overrides(
    arg_groups: list[list[str]],
    parser: argparse.ArgumentParser,
) -> None:
    """Run experiments with --and separated override groups.

    Args:
        arg_groups: List of argument groups from _split_on_and.
                   First group is base args, subsequent are --and groups.
        parser: Argument parser for parsing overrides
    """
    from .experiments import run_multiple

    # Parse base args (first group)
    base_args, _ = parser.parse_known_args(arg_groups[0])

    if not base_args.experiments.exists():
        print(f"Error: {base_args.experiments} not found", file=sys.stderr)
        sys.exit(1)

    output_base = base_args.output_dir or Path("outputs/calendar_scheduling")

    # Parse each group into overrides
    # First group: any override args in base (e.g., --experiments dir --model X)
    # Subsequent groups: --and groups (e.g., --and --model Y)
    override_groups: list[dict] = []

    for group_argv in arg_groups:
        overrides = _parse_override_group(parser, group_argv)
        override_groups.append(overrides)

    # Create benchmark logger
    benchmark_logger = create_benchmark_logger(base_args.logger)

    # If only one group and no overrides, just run normally
    if len(override_groups) == 1 and not override_groups[0]:
        with benchmark_logger:
            await run_multiple(
                path=base_args.experiments,
                output_base=output_base,
                pattern=base_args.experiment_pattern,
                collect_only=base_args.collect_only,
                batch_size=base_args.batch_size,
                benchmark_logger=benchmark_logger,
                restart_exec=base_args.restart_exec,
                restart_eval=base_args.restart_eval,
            )
        return

    # Build final override groups for run_multiple
    final_override_groups: list[dict] | None = None

    if len(override_groups) > 1:
        # Multiple groups (--and was used)
        final_override_groups = override_groups
        print(f"Running {len(final_override_groups)} experiment group(s):")
        for i, overrides in enumerate(final_override_groups):
            name = _variant_name(overrides) if overrides else "(original)"
            print(f"  Group {i + 1}: {name}")
    elif override_groups[0]:
        # Single group with overrides
        final_override_groups = override_groups
        print(f"Applying override: {_variant_name(override_groups[0])}")

    with benchmark_logger:
        await run_multiple(
            path=base_args.experiments,
            output_base=output_base,
            pattern=base_args.experiment_pattern,
            collect_only=base_args.collect_only,
            override_groups=final_override_groups,
            batch_size=base_args.batch_size,
            benchmark_logger=benchmark_logger,
            restart_exec=base_args.restart_exec,
            restart_eval=base_args.restart_eval,
        )


async def run():
    load_dotenv()

    # Split on --and separator
    arg_groups = _split_on_and(sys.argv[1:])

    # Parse base arguments (first group)
    parser = create_argument_parser()
    base_args, _ = parser.parse_known_args(arg_groups[0])

    # Initialize LLM tracer to collect traces for all LiteLLM calls
    get_tracer()

    # Handle --experiments mode
    if base_args.experiments:
        # Configure logging
        log_level = getattr(logging, base_args.log_level.upper())
        logging.basicConfig(level=log_level, format="%(message)s")

        # Use override handler (handles both simple and --and cases)
        await _run_experiments_with_overrides(arg_groups, parser)
        return

    # For non-experiments mode, use standard parsing with validation
    args = parse_args()

    # Handle --reeval mode (separate from normal run/resume)
    if args.reeval:
        # Configure logging
        log_level = getattr(logging, args.log_level.upper())
        logging.basicConfig(level=log_level, format="%(message)s")
        await run_reeval(args)
        return

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
            if args.restart_exec:
                # Restart execution: ignore checkpointed exec progress
                skip_exec_keys = set()
                prior_exec_results = []
                logger.info("Restart-exec mode: re-running all tasks from scratch")
            else:
                skip_exec_keys = checkpoint_mgr.get_completed_task_keys()
                prior_exec_results = checkpoint_mgr.get_execution_results()

            if args.restart_eval:
                # Restart evaluation: skip all exec, eval everything fresh
                skip_eval_keys = set()
                prior_eval_results = []
                logger.info(
                    "Restart-eval mode: re-evaluating all %d tasks",
                    len(skip_exec_keys) + len(prior_exec_results),
                )
            else:
                skip_eval_keys = checkpoint_mgr.get_completed_eval_keys()
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
        # Resolve CoT settings
        init_assistant_cot = (
            new_config.assistant_explicit_cot
            if new_config.assistant_explicit_cot is not None
            else new_config.explicit_cot
        )
        init_requestor_cot = (
            new_config.requestor_explicit_cot
            if new_config.requestor_explicit_cot is not None
            else new_config.explicit_cot
        )
        # Resolve reasoning effort
        init_assistant_effort = new_config.assistant_reasoning_effort or new_config.reasoning_effort
        init_requestor_effort = new_config.requestor_reasoning_effort or new_config.reasoning_effort
        init_judge_effort = new_config.judge_reasoning_effort or new_config.reasoning_effort

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
            assistant_explicit_cot=init_assistant_cot,
            assistant_reasoning_effort=str(init_assistant_effort)
            if init_assistant_effort
            else None,
            requestor_explicit_cot=init_requestor_cot,
            requestor_reasoning_effort=str(init_requestor_effort)
            if init_requestor_effort
            else None,
            judge_reasoning_effort=str(init_judge_effort) if init_judge_effort else None,
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

    # Create benchmark logger
    benchmark_logger = create_benchmark_logger(args.logger)

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
            benchmark_logger=benchmark_logger,
        )

        # Merge with prior results
        all_exec_results = prior_exec_results + new_exec_results

        # Evaluation phase
        new_eval_results = await evaluate_tasks(
            execution_results=all_exec_results,
            model=judge_model,
            model_client=judge_client,
            batch_size=config.batch_size,
            on_task_complete=checkpoint_mgr.add_evaluation_result,
            skip_task_keys=skip_eval_keys if skip_eval_keys else None,
            judge_votes=config.judge_votes,
            benchmark_logger=benchmark_logger,
        )

        # Merge with prior results
        all_eval_results = prior_eval_results + new_eval_results

        # Sort results by task id for consistent ordering
        all_eval_results = sorted(all_eval_results, key=lambda r: r.execution.task.id or 0)

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
            assistant_explicit_cot=assistant_explicit_cot,
            assistant_reasoning_effort=str(assistant_reasoning_effort)
            if assistant_reasoning_effort
            else None,
            requestor_explicit_cot=requestor_explicit_cot,
            requestor_reasoning_effort=str(requestor_reasoning_effort)
            if requestor_reasoning_effort
            else None,
            judge_reasoning_effort=str(judge_reasoning_effort) if judge_reasoning_effort else None,
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
            "To resume: sagebench calendar --resume %s",
            run_output.output_dir,
        )


def main():
    asyncio.run(run())


if __name__ == "__main__":
    main()
