import argparse
import asyncio
import json
import logging
import signal
import sys
from pathlib import Path

from dotenv import load_dotenv
from sage_llm import get_tracer, save_traces

from sage_benchmark.shared.cli_utils import parse_reasoning_effort
from sage_benchmark.shared.logging import create_benchmark_logger

from .agents.assistant import list_available_presets
from .checkpoints import CheckpointManager, RunConfig
from .evaluation.evaluator import (
    print_evaluation_summary,
    print_per_task_summary,
)
from .experiments.runner import Experiment
from .run_paths import RunPaths
from .types import BenchmarkOutput

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

    # Tracing option
    parser.add_argument(
        "--llm-tracing",
        action="store_true",
        default=False,
        help="Enable LLM call tracing (disabled by default for performance)",
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
                llm_tracing=base_args.llm_tracing,
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
            llm_tracing=base_args.llm_tracing,
        )


async def run():
    load_dotenv()

    # Split on --and separator
    arg_groups = _split_on_and(sys.argv[1:])

    # Parse base arguments (first group)
    parser = create_argument_parser()
    base_args, _ = parser.parse_known_args(arg_groups[0])

    # Initialize LLM tracer only when explicitly requested
    if base_args.llm_tracing:
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

    # Handle --reeval mode: construct checkpoint from eval.json, then re-evaluate via Experiment
    if args.reeval:
        log_level = getattr(logging, args.log_level.upper())
        logging.basicConfig(level=log_level, format="%(message)s")

        # Load existing output
        existing_output = BenchmarkOutput.model_validate(json.loads(args.reeval.read_text()))
        logger.info("Loaded %d results from %s", len(existing_output.results), args.reeval)

        # Build config from metadata + CLI overrides for judge
        config = RunConfig.from_metadata(
            existing_output.metadata,
            judge_model=args.judge_model or args.model or existing_output.metadata.judge_model,
            judge_base_url=args.judge_base_url or args.base_url,
            judge_api_version=args.judge_api_version or args.api_version,
            judge_reasoning_effort=args.judge_reasoning_effort or args.reasoning_effort,
            batch_size=args.batch_size,
            output_dir=args.output_dir or args.reeval.parent,
        )

        # Write synthetic checkpoint with execution results
        output_dir = args.output_dir or args.reeval.parent
        run_paths = RunPaths(output_dir)
        run_paths.ensure_dir()
        checkpoint_mgr = CheckpointManager(run_paths.checkpoint_path)
        checkpoint_mgr.initialize(config, existing_output.metadata, {})
        for result in existing_output.results:
            checkpoint_mgr.add_execution_result(result.execution)

        # Re-evaluate via Experiment
        experiment = Experiment(config, restart_eval=True, llm_tracing=args.llm_tracing)
        output = await experiment.run()

        print_per_task_summary(output.results)
        print_evaluation_summary(output.summary)
        return

    # Build config for Experiment
    if args.resume:
        # Resume: load config from checkpoint
        if isinstance(args.resume, str):
            run_output = RunPaths.from_path(Path(args.resume))
        else:
            raise ValueError(
                "When using --resume without a path, you must specify the run directory or checkpoint file"
            )

        checkpoint_mgr = CheckpointManager(run_output.checkpoint_path)
        existing_checkpoint = checkpoint_mgr.load()

        if not existing_checkpoint or not existing_checkpoint.config:
            raise ValueError(
                f"No valid checkpoint found at {run_output.checkpoint_path}. "
                "Cannot resume without a checkpoint."
            )

        config = existing_checkpoint.config
        # Set output_dir so Experiment uses the same directory
        config = config.model_copy(update={"output_dir": run_output.output_dir})
        logger.info("Resuming from checkpoint: %s", run_output.output_dir)
    else:
        # New run - require paths
        if not args.paths:
            raise ValueError(
                "Task paths are required when not resuming. Use --resume to continue a previous run."
            )

        config = RunConfig.from_args(args)
        if args.output_dir:
            config = config.model_copy(update={"output_dir": Path(args.output_dir)})

    # Configure logging
    log_level = getattr(logging, args.log_level.upper())
    logging.basicConfig(level=log_level, format="%(message)s")

    # Create benchmark logger
    benchmark_logger = create_benchmark_logger(args.logger)

    # Create and run experiment
    experiment = Experiment(
        config,
        restart_exec=args.restart_exec,
        restart_eval=args.restart_eval,
        llm_tracing=args.llm_tracing,
    )

    # Add file handler for logging to output directory
    file_handler = logging.FileHandler(experiment.run_paths.get_log_path())
    logging.getLogger().addHandler(file_handler)

    logger.info("Output directory: %s", experiment.run_paths.output_dir)
    logger.info("Running %d task(s)...", experiment.task_count)

    # Set up signal handlers for graceful interruption
    loop = asyncio.get_event_loop()
    main_task: asyncio.Task | None = None
    cancel_event = asyncio.Event()

    def signal_handler():
        logger.warning("Interrupt received, cancelling tasks and saving checkpoint...")
        cancel_event.set()
        experiment.checkpoint_mgr.set_interrupted(True)
        if main_task is not None:
            main_task.cancel()

    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, signal_handler)

    try:
        with benchmark_logger:
            main_task = asyncio.create_task(experiment.run(cancel_event=cancel_event))
            output = await main_task

        print_per_task_summary(output.results)
        print_evaluation_summary(output.summary)

    except asyncio.CancelledError:
        logger.info("Run cancelled, checkpoint saved to %s", experiment.run_paths.output_dir)
        if args.llm_tracing:
            traces_path = experiment.run_paths.get_traces_path()
            save_traces(traces_path)
            logger.info("Saved LLM traces to %s", traces_path)
        logger.info(
            "To resume: sagebench calendar --resume %s",
            experiment.run_paths.output_dir,
        )
    finally:
        for sig in (signal.SIGINT, signal.SIGTERM):
            loop.remove_signal_handler(sig)


def main():
    asyncio.run(run())


if __name__ == "__main__":
    main()
