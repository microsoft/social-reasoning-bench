"""CLI for minimal marketplace simulation benchmark."""

import argparse
import asyncio
import json
import logging
import signal
import time
from datetime import datetime
from pathlib import Path

from sage_llm import ModelClient

from sage_benchmark.shared.logging import create_benchmark_logger

from .checkpoints import CheckpointManager, RunConfig
from .evaluation_summary import compute_summary, print_evaluation_summary, print_per_task_summary
from .loader import load_tasks
from .runner import run_and_evaluate_tasks
from .types import (
    MarketplaceBenchmarkMetadata,
    MarketplaceBenchmarkOutput,
    TaskExecutionResult,
)

logger = logging.getLogger(__name__)

CHECKPOINT_FILENAME = "checkpoint.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Minimal marketplace negotiation simulation")
    parser.add_argument(
        "--data",
        nargs="+",
        default=None,
        help="YAML file(s) or directories containing marketplace tasks",
    )
    parser.add_argument("--limit", type=int, default=None, help="Limit tasks to run")
    parser.add_argument(
        "--max-steps-per-turn",
        type=int,
        default=3,
        help="Maximum tool calls per agent turn (default: 3)",
    )
    parser.add_argument(
        "--model", default=None, help="Default model for buyer and seller (LLM mode)"
    )
    parser.add_argument("--buyer-model", default=None, help="Buyer model (overrides --model)")
    parser.add_argument("--seller-model", default=None, help="Seller model (overrides --model)")
    parser.add_argument(
        "--base-url",
        default=None,
        help="Default base URL for OpenAI-compatible API (LLM mode)",
    )
    parser.add_argument(
        "--buyer-base-url", default=None, help="Buyer base URL (overrides --base-url)"
    )
    parser.add_argument(
        "--seller-base-url", default=None, help="Seller base URL (overrides --base-url)"
    )
    parser.add_argument(
        "--judge-model",
        default=None,
        help="Model for privacy leakage judge (enables LLM-based leakage detection)",
    )
    parser.add_argument(
        "--judge-base-url",
        default=None,
        help="Base URL for privacy leakage judge API (defaults to --base-url)",
    )
    parser.add_argument(
        "--output-dir",
        default="outputs/marketplace",
        help="Directory to write execution results",
    )
    parser.add_argument(
        "--reasoning-effort",
        default=None,
        help="Reasoning effort for models (e.g. 'low', 'medium', 'high', or integer budget)",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=50,
        help="Number of tasks to run in parallel (default: 50)",
    )
    parser.add_argument(
        "--logger",
        default="progress",
        choices=["verbose", "progress", "quiet"],
        help="Logging style: verbose, progress (default, tqdm bar), quiet (minimal)",
    )
    # Resume/checkpoint options
    parser.add_argument(
        "--resume",
        nargs="?",
        const=True,
        default=None,
        help=(
            "Resume from checkpoint. Optionally specify path to checkpoint directory. "
            "If provided without path, auto-discovers from output dir."
        ),
    )
    # Reeval flag (matches calendar pattern)
    parser.add_argument(
        "--reeval",
        action="store_true",
        default=False,
        help=(
            "Re-evaluate existing execution results without re-running tasks. "
            "Requires --resume to specify a checkpoint with execution results."
        ),
    )
    return parser.parse_args()


def _find_latest_checkpoint(output_dir: Path) -> Path | None:
    """Find the most recent checkpoint in output_dir subdirectories."""
    candidates = list(output_dir.glob(f"run_*/{CHECKPOINT_FILENAME}"))
    if not candidates:
        return None
    return max(candidates, key=lambda p: p.stat().st_mtime)


def _resolve_checkpoint_path(args: argparse.Namespace) -> Path:
    """Resolve the checkpoint file path based on --resume and --output-dir.

    Resolution order for ``--resume <path>``:
      1. <path> is an existing checkpoint file  -> use it directly
      2. <path>/checkpoint.json exists           -> use it
      3. <path>/run_*/checkpoint.json exists     -> use the most recent one
      4. fall back to <path>/checkpoint.json     (will fail gracefully later)

    For bare ``--resume`` (no path), the same search is applied to
    ``--output-dir``.
    """
    if isinstance(args.resume, str):
        resume_path = Path(args.resume)
        if resume_path.is_file():
            return resume_path
        # Direct checkpoint inside directory
        direct = resume_path / CHECKPOINT_FILENAME
        if direct.exists():
            return direct
        # Auto-discover from run_* subdirectories
        found = _find_latest_checkpoint(resume_path)
        if found:
            return found
        # Fall back (will be handled as "not found" downstream)
        return direct

    # Bare --resume: search output dir
    output_dir = Path(args.output_dir)
    direct = output_dir / CHECKPOINT_FILENAME
    if direct.exists():
        return direct
    found = _find_latest_checkpoint(output_dir)
    if found:
        return found
    return direct


def _resolve_run_dir(args: argparse.Namespace) -> Path:
    """Resolve the run directory for output."""
    if args.resume:
        # When resuming, use the same directory as the checkpoint
        checkpoint_path = _resolve_checkpoint_path(args)
        return checkpoint_path.parent
    return Path(args.output_dir) / f"run_{datetime.now().strftime('%Y%m%d_%H%M%S')}"


def _apply_cli_overrides(config: RunConfig, args: argparse.Namespace) -> RunConfig:
    """Apply CLI argument overrides to a checkpoint-loaded RunConfig.

    Only overrides fields that were explicitly provided on the command line
    (i.e. not None).
    """
    overrides: dict = {}
    if args.model is not None:
        overrides["model"] = args.model
    if args.buyer_model is not None:
        overrides["buyer_model"] = args.buyer_model
    if args.seller_model is not None:
        overrides["seller_model"] = args.seller_model
    if getattr(args, "judge_model", None) is not None:
        overrides["judge_model"] = args.judge_model
    if args.base_url is not None:
        overrides["base_url"] = args.base_url
    if args.buyer_base_url is not None:
        overrides["buyer_base_url"] = args.buyer_base_url
    if args.seller_base_url is not None:
        overrides["seller_base_url"] = args.seller_base_url
    if getattr(args, "judge_base_url", None) is not None:
        overrides["judge_base_url"] = args.judge_base_url
    if args.reasoning_effort is not None:
        overrides["reasoning_effort"] = args.reasoning_effort
    if overrides:
        config = config.model_copy(update=overrides)
    return config


async def _run_and_evaluate(args: argparse.Namespace) -> None:
    reeval = args.reeval
    benchmark_logger = create_benchmark_logger(args.logger)

    # Determine run directory and checkpoint path
    run_dir = _resolve_run_dir(args)
    run_dir.mkdir(parents=True, exist_ok=True)
    checkpoint_path = run_dir / CHECKPOINT_FILENAME

    checkpoint_mgr = CheckpointManager(checkpoint_path)

    # Handle resume: load existing checkpoint
    skip_exec_keys: set[str] = set()
    skip_eval_keys: set[str] = set()
    prior_exec_results: list[TaskExecutionResult] = []
    config: RunConfig | None = None

    if args.resume:
        existing = checkpoint_mgr.load()
        if existing:
            config = existing.config
            # Apply any CLI overrides (e.g. --judge-model, --model)
            if config is not None:
                config = _apply_cli_overrides(config, args)
            skip_exec_keys = checkpoint_mgr.get_completed_keys()
            skip_eval_keys = checkpoint_mgr.get_completed_eval_keys()
            prior_exec_results = checkpoint_mgr.get_execution_results()
            logger.info(
                "Resuming: %d executions, %d evaluations already completed",
                len(skip_exec_keys),
                len(skip_eval_keys),
            )
        else:
            logger.warning("No checkpoint found at %s, starting fresh", checkpoint_path)

    # Build config from CLI args if not resuming from checkpoint
    if config is None:
        config = RunConfig.from_args(args)

    # Reeval mode: skip ALL executions (reuse prior), clear eval progress
    if reeval:
        if not prior_exec_results:
            # Try loading checkpoint if not already loaded via --resume
            existing = (
                checkpoint_mgr.load() if checkpoint_mgr._data is None else checkpoint_mgr._data
            )
            if existing is None:
                raise ValueError(
                    "--reeval requires a checkpoint with execution results. "
                    "Use --resume to specify a checkpoint path."
                )
            prior_exec_results = checkpoint_mgr.get_execution_results()
            if not prior_exec_results:
                raise ValueError("No execution results found in checkpoint for --reeval.")
        # Skip all executions, re-evaluate everything from scratch
        skip_exec_keys = {r.task_key for r in prior_exec_results}
        skip_eval_keys = set()

    # Resolve models
    buyer_model = (
        args.buyer_model or args.model or (config.resolved_buyer_model if config else None)
    )
    seller_model = (
        args.seller_model or args.model or (config.resolved_seller_model if config else None)
    )
    if not buyer_model or not seller_model:
        raise ValueError("Requires --model or both --buyer-model and --seller-model")

    # Load tasks
    data_paths = args.data or (config.paths if config else None)
    if not data_paths:
        raise ValueError("Task paths are required. Use --data to specify YAML files/directories.")
    loaded = load_tasks(data_paths, limit=args.limit or (config.limit if config else None))
    tasks = loaded.all_tasks
    if not tasks:
        raise ValueError("No tasks loaded")

    benchmark_logger.log_message(
        logging.INFO,
        "Starting marketplace experiment: "
        "tasks=%d buyer_model=%s seller_model=%s "
        "max_steps_per_turn=%d batch_size=%d reeval=%s",
        len(tasks),
        buyer_model,
        seller_model,
        args.max_steps_per_turn,
        args.batch_size,
        reeval,
    )

    reasoning_effort: str | int = "none"
    if args.reasoning_effort is not None:
        try:
            reasoning_effort = int(args.reasoning_effort)
        except ValueError:
            reasoning_effort = args.reasoning_effort

    buyer_client = ModelClient(
        base_url=args.buyer_base_url or args.base_url,
        reasoning_effort=reasoning_effort,
    )
    seller_client = ModelClient(
        base_url=args.seller_base_url or args.base_url,
        reasoning_effort=reasoning_effort,
    )

    judge_model = args.judge_model or (config.resolved_judge_model if config else None)
    judge_client = None
    if judge_model:
        judge_base_url = (
            args.judge_base_url
            or (config.judge_base_url if config else None)
            or (config.base_url if config else None)
            or args.base_url
        )
        judge_client = ModelClient(base_url=judge_base_url)

    # Initialize checkpoint if not resuming
    if not args.resume or checkpoint_mgr._data is None:
        checkpoint_mgr.initialize(config, loaded.file_hashes)

    # Set up SIGINT handler
    cancel_event = asyncio.Event()
    loop = asyncio.get_event_loop()

    def signal_handler() -> None:
        logger.warning("Interrupt received, saving checkpoint...")
        cancel_event.set()
        checkpoint_mgr.set_interrupted(True)
        for sig in (signal.SIGINT, signal.SIGTERM):
            loop.remove_signal_handler(sig)

    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, signal_handler)

    try:
        run_start = time.monotonic()

        with benchmark_logger:
            paired_results = await run_and_evaluate_tasks(
                tasks,
                buyer_model=buyer_model,
                seller_model=seller_model,
                buyer_client=buyer_client,
                seller_client=seller_client,
                max_steps_per_turn=args.max_steps_per_turn,
                batch_size=args.batch_size,
                benchmark_logger=benchmark_logger,
                judge_model=judge_model,
                judge_client=judge_client,
                skip_exec_keys=skip_exec_keys,
                skip_eval_keys=skip_eval_keys,
                prior_exec_results=prior_exec_results,
                checkpoint_mgr=checkpoint_mgr,
                cancel_event=cancel_event,
            )

        if cancel_event.is_set():
            logger.info("Interrupted, checkpoint saved to %s", checkpoint_path)
            logger.info("To resume: sagebench marketplace --resume %s", run_dir)
            return

        run_elapsed = time.monotonic() - run_start

        # Merge newly completed with checkpoint results
        prev_exec = checkpoint_mgr.get_execution_results()
        prev_eval = checkpoint_mgr.get_evaluation_results()

        exec_map = {r.task_key: r for r in prev_exec}
        eval_map = {e.task_key: e for e in prev_eval}
        for r, e in paired_results:
            exec_map[r.task_key] = r
            if e is not None:
                eval_map[e.task_key] = e

        results = list(exec_map.values())
        evaluations = [eval_map.get(r.task_key) for r in results]

    finally:
        for sig in (signal.SIGINT, signal.SIGTERM):
            try:
                loop.remove_signal_handler(sig)
            except (ValueError, RuntimeError):
                pass

    # Build structured output
    valid_evals = [e for e in evaluations if e is not None]
    summary = compute_summary(valid_evals, results)

    metadata = MarketplaceBenchmarkMetadata(
        timestamp=datetime.now().isoformat(),
        buyer_model=buyer_model,
        seller_model=seller_model,
        judge_model=judge_model,
        max_steps_per_turn=args.max_steps_per_turn,
        batch_size=args.batch_size,
        task_count=len(results),
        reasoning_effort=args.reasoning_effort,
        elapsed_seconds=run_elapsed,
    )

    output = MarketplaceBenchmarkOutput(
        metadata=metadata,
        summary=summary,
        results=valid_evals,
    )

    # Write output
    out_path = run_dir / "results.json"
    out_path.write_text(json.dumps(output.model_dump(mode="json"), indent=2))

    # Clean up checkpoint on successful completion
    checkpoint_mgr.cleanup()

    # Print per-task and evaluation summaries
    print_per_task_summary(valid_evals, results)
    print_evaluation_summary(summary)

    print(f"\nSaved results to {out_path}")
    mins, secs = divmod(run_elapsed, 60)
    print(f"Total time: {int(mins)}m{secs:04.1f}s")


def main() -> None:
    args = parse_args()
    asyncio.run(_run_and_evaluate(args))
