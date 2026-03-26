"""Core experiment runner logic."""

import asyncio
import json
import logging
import os
import signal
import time
from datetime import datetime
from pathlib import Path

from sage_llm import get_tracer

from sage_benchmark.shared.logging import BenchmarkLogger

from ..checkpoints import CheckpointManager, RunConfig
from ..types import (
    BenchmarkMetadata,
    BenchmarkOutput,
    KeyedCalendarTask,
    TaskEvaluationResult,
    TaskExecutionResult,
)
from .output import build_output, save_llm_traces, save_output
from .setup import (
    create_assistant_client,
    create_judge_client,
    create_requestor_client,
    create_run_paths,
    load_experiment_tasks,
    load_system_prompt,
    resolve_explicit_cot,
)

logger = logging.getLogger(__name__)

# Alias for clarity in this module
ExperimentConfig = RunConfig


class ExperimentOutput(BenchmarkOutput):
    """Output from an experiment run."""

    pass


class RunCancelled(Exception):
    """Raised when a run is cancelled via interrupt."""

    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        super().__init__(f"Run cancelled. Output dir: {output_dir}")


class Experiment:
    """Prepared experiment ready to run.

    Handles setup, execution, evaluation, and finalization of a single experiment.
    """

    def __init__(
        self,
        config: ExperimentConfig,
        restart_exec: bool = False,
        restart_eval: bool = False,
        llm_tracing: bool = False,
    ):
        """Initialize experiment from config.

        Args:
            config: Experiment configuration
            restart_exec: If True, ignore checkpointed execution progress
            restart_eval: If True, ignore checkpointed evaluation progress
            llm_tracing: If True, enable LLM call tracing and save traces
        """
        self.config = config
        self.llm_tracing = llm_tracing
        self.run_paths = create_run_paths(config)
        self.run_paths.ensure_dir()

        # Setup checkpoint
        self.checkpoint_mgr = CheckpointManager(self.run_paths.checkpoint_path)

        # Track prior results for resume
        self.skip_exec_keys: set[str] = set()
        self.skip_eval_keys: set[str] = set()
        self.prior_exec_results: list[TaskExecutionResult] = []
        self.prior_eval_results: list[TaskEvaluationResult] = []

        # Load checkpoint if exists (unless restart flags are set)
        if self.run_paths.checkpoint_path.exists():
            existing_checkpoint = self.checkpoint_mgr.load()
            if existing_checkpoint:
                if restart_exec:
                    # Clear execution checkpoint - re-run everything
                    logger.info("Restart-exec: ignoring checkpointed execution progress")
                else:
                    self.skip_exec_keys = self.checkpoint_mgr.get_completed_task_keys()
                    self.prior_exec_results = self.checkpoint_mgr.get_execution_results()

                if restart_eval:
                    # Clear evaluation checkpoint - re-evaluate everything
                    logger.info("Restart-eval: ignoring checkpointed evaluation progress")
                else:
                    self.skip_eval_keys = self.checkpoint_mgr.get_completed_eval_keys()
                    self.prior_eval_results = self.checkpoint_mgr.get_evaluation_results()

                if not restart_exec and not restart_eval:
                    logger.info(
                        "Resuming: %d executions, %d evaluations complete",
                        len(self.skip_exec_keys),
                        len(self.skip_eval_keys),
                    )

        # Load tasks from YAML paths
        self.tasks, file_hashes = load_experiment_tasks(
            paths=config.paths,
            limit=config.limit,
        )

        # Reeval mode: if no tasks from paths but we have prior execution results,
        # reconstruct tasks from those results
        if not self.tasks and self.prior_exec_results:
            self.tasks = [
                KeyedCalendarTask(**r.task.model_dump(), task_key=r.task_key)
                for r in self.prior_exec_results
            ]
            file_hashes = {}

        # Initialize checkpoint with config and file hashes
        # Resolve CoT settings
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
        # Resolve reasoning effort
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
            task_count=len(self.tasks),
            system_prompt=config.assistant_system_prompt,
            expose_preferences=config.expose_preferences or False,
            assistant_explicit_cot=assistant_cot,
            assistant_reasoning_effort=str(assistant_effort) if assistant_effort else None,
            requestor_explicit_cot=requestor_cot,
            requestor_reasoning_effort=str(requestor_effort) if requestor_effort else None,
            judge_reasoning_effort=str(judge_effort) if judge_effort else None,
        )
        self.checkpoint_mgr.initialize(config, metadata, file_hashes)

        # Create clients
        self.assistant_client = create_assistant_client(config)
        self.requestor_client = create_requestor_client(config)
        self.judge_client = create_judge_client(config)

        # Load system prompt
        self.system_prompt = load_system_prompt(config)

        # Resolve explicit CoT
        self.assistant_explicit_cot, self.requestor_explicit_cot = resolve_explicit_cot(config)

    @property
    def key(self) -> str:
        """Unique identifier for this experiment."""
        return str(self.run_paths.output_dir)

    @property
    def name(self) -> str:
        """Display name for this experiment."""
        return self.config.variant or "default"

    @property
    def task_count(self) -> int:
        """Number of tasks remaining to run."""
        return len(self.tasks) - len(self.skip_eval_keys)

    async def run(self, cancel_event: asyncio.Event | None = None) -> ExperimentOutput:
        """Run the experiment and return results.

        This is the main entry point for running an experiment.
        Each task is executed and immediately evaluated before moving to the next.

        Args:
            cancel_event: Optional event to signal cancellation to running tasks.
        """
        from sage_benchmark.shared.executors import TaskPoolExecutor

        from ..evaluation.evaluator import evaluate_single_task
        from ..runner import run_single_task

        config = self.config

        # Validate models are configured and store in local vars for type narrowing
        if not config.resolved_assistant_model or not config.resolved_requestor_model:
            raise RuntimeError("Assistant and requestor models must be configured")
        if not config.resolved_judge_model:
            raise RuntimeError("Judge model must be configured")
        assistant_model = config.resolved_assistant_model
        requestor_model = config.resolved_requestor_model
        judge_model = config.resolved_judge_model

        # Count tasks that need work
        total_tasks = sum(1 for task in self.tasks if task.task_key not in self.skip_eval_keys)

        # Build lookup for prior exec results (for eval-only tasks)
        prior_exec_by_key = {r.task_key: r for r in self.prior_exec_results}

        # Track new eval results
        new_eval_results: list[TaskEvaluationResult] = []

        async def run_and_evaluate(
            task: KeyedCalendarTask,
            task_index: int,
        ) -> TaskEvaluationResult:
            """Execute a task (if needed) and evaluate it."""
            # Check if we already have execution result
            if task.task_key in self.skip_exec_keys:
                exec_result = prior_exec_by_key.get(task.task_key)
                if exec_result is None:
                    raise RuntimeError(
                        f"Task {task.task_key} in skip_exec_keys but no prior exec result"
                    )
            else:
                # Execute
                exec_result = await run_single_task(
                    task,
                    task.task_key,
                    assistant_model,
                    self.assistant_client,
                    requestor_model,
                    self.requestor_client,
                    config.max_rounds,
                    config.max_steps_per_turn,
                    self.system_prompt,
                    self.assistant_explicit_cot,
                    self.requestor_explicit_cot,
                    config.expose_preferences or False,
                    cancel_event,
                )
                self.checkpoint_mgr.add_execution_result(exec_result)

            # Skip evaluation if cancelled — eval can happen on resume
            if cancel_event and cancel_event.is_set():
                raise asyncio.CancelledError("Skipping evaluation due to cancellation")

            # Evaluate
            eval_result = await evaluate_single_task(
                exec_result,
                judge_model,
                self.judge_client,
                config.judge_votes,
            )
            self.checkpoint_mgr.add_evaluation_result(eval_result)

            return eval_result

        def on_task_complete(result: TaskEvaluationResult):
            new_eval_results.append(result)

        # Generate task coroutines
        def generate_tasks():
            for task_index, task in enumerate(self.tasks):
                if task.task_key in self.skip_eval_keys:
                    continue
                yield run_and_evaluate(task, task_index)

        executor = TaskPoolExecutor(
            batch_size=config.batch_size,
            on_task_complete=on_task_complete,
            task_logger=logger,
            cancel_event=cancel_event,
        )
        run_start = time.monotonic()
        await executor.run(generate_tasks())
        elapsed = time.monotonic() - run_start

        # Merge with prior results and sort
        all_eval_results = self.prior_eval_results + new_eval_results
        all_eval_results = sorted(all_eval_results, key=lambda r: r.execution.task.id or 0)

        # Build and save output (skip save if cancelled — checkpoint is already saved per-task)
        output = build_output(self.tasks, all_eval_results, config, elapsed_seconds=elapsed)
        if not (cancel_event and cancel_event.is_set()):
            save_output(output, self.run_paths, self.checkpoint_mgr, self.llm_tracing)

        return ExperimentOutput(**output.model_dump())


def run_single(config: ExperimentConfig) -> ExperimentOutput:
    """Run a single experiment synchronously.

    Args:
        config: Experiment configuration

    Returns:
        ExperimentOutput with results

    Raises:
        RunCancelled: If the run is interrupted
    """
    return asyncio.run(run_single_async(config))


async def run_single_async(config: ExperimentConfig, llm_tracing: bool = False) -> ExperimentOutput:
    """Run a single experiment asynchronously.

    Args:
        config: Experiment configuration
        llm_tracing: If True, enable LLM call tracing and save traces

    Returns:
        ExperimentOutput with results

    Raises:
        RunCancelled: If the run is interrupted
    """
    # Initialize LLM tracer only when requested
    if llm_tracing:
        get_tracer()

    experiment = Experiment(config, llm_tracing=llm_tracing)

    # Set up signal handlers for graceful interruption
    loop = asyncio.get_event_loop()
    cancel_event = asyncio.Event()

    def signal_handler():
        logger.warning("Interrupt received, cancelling tasks and saving checkpoint...")
        cancel_event.set()
        experiment.checkpoint_mgr.set_interrupted(True)
        # Remove handlers so next Ctrl+C forces immediate exit
        for sig in (signal.SIGINT, signal.SIGTERM):
            loop.remove_signal_handler(sig)

    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, signal_handler)

    try:
        output = await experiment.run(cancel_event=cancel_event)

        if cancel_event.is_set():
            logger.info(
                "Run cancelled, checkpoint saved to %s", experiment.run_paths.checkpoint_path
            )
            if llm_tracing:
                save_llm_traces(experiment.run_paths)
            raise RunCancelled(str(experiment.run_paths.output_dir))

        return output
    finally:
        # Remove signal handlers (may already be removed by signal_handler)
        for sig in (signal.SIGINT, signal.SIGTERM):
            try:
                loop.remove_signal_handler(sig)
            except (ValueError, RuntimeError):
                pass


# ==============================================================================
# Experiment pool executor (unified task pool across experiments)
# ==============================================================================


class ExperimentPoolExecutor:
    """Executes multiple experiments with a unified task pool.

    Instead of running experiments sequentially (which causes "tail draining"
    where small remaining tasks block starting the next experiment), this
    pools all tasks across experiments together.

    Each task is executed and immediately evaluated before moving to the next,
    which provides incremental results and lower memory usage.
    """

    def __init__(
        self,
        experiments: list[Experiment],
        batch_size: int = 100,
        cancel_event: asyncio.Event | None = None,
        benchmark_logger: BenchmarkLogger | None = None,
        llm_tracing: bool = False,
    ):
        """Initialize the pool executor.

        Args:
            experiments: List of prepared Experiment objects.
            batch_size: Maximum concurrent tasks across all experiments.
            cancel_event: Optional event to signal cancellation to running tasks.
            benchmark_logger: Optional logger for progress tracking.
            llm_tracing: If True, enable LLM call tracing and save traces.
        """
        self.experiments = experiments
        self.batch_size = batch_size
        self.cancel_event = cancel_event
        self.benchmark_logger = benchmark_logger
        self.llm_tracing = llm_tracing

        # Maps experiment key to experiment for result routing
        self._exp_by_key: dict[str, Experiment] = {e.key: e for e in experiments}

        # Track eval results by experiment (eval results contain exec results)
        self._eval_results_by_exp: dict[str, list[TaskEvaluationResult]] = {
            e.key: [] for e in experiments
        }

        # Per-experiment timing: expected task count and completion time
        self._exp_task_counts: dict[str, int] = {}
        self._exp_finish_times: dict[str, float] = {}
        self._pool_start_time: float = 0.0

    async def run(self) -> list[ExperimentOutput]:
        """Run all experiments and return their outputs.

        Returns:
            List of ExperimentOutput, one per experiment.
            Empty list if cancelled before finalization.
        """
        # Single phase: execute and evaluate each task together
        await self._run_tasks()

        # Skip finalization if cancelled — checkpoints are already saved per-task
        if self.cancel_event and self.cancel_event.is_set():
            return []

        # Finalize and build outputs in parallel
        async def finalize_experiment(exp: Experiment) -> ExperimentOutput:
            all_eval = exp.prior_eval_results + self._eval_results_by_exp[exp.key]
            all_eval = sorted(all_eval, key=lambda r: r.execution.task.id or 0)
            elapsed = self._exp_finish_times.get(exp.key)
            output = build_output(exp.tasks, all_eval, exp.config, elapsed_seconds=elapsed)
            # Run blocking I/O in thread pool to parallelize across experiments
            await asyncio.to_thread(
                save_output, output, exp.run_paths, exp.checkpoint_mgr, self.llm_tracing
            )
            return ExperimentOutput(**output.model_dump())

        outputs = await asyncio.gather(*[finalize_experiment(exp) for exp in self.experiments])
        return list(outputs)

    async def _run_tasks(self):
        """Run execution + evaluation for all tasks across experiments."""
        from sage_benchmark.shared.executors import TaskPoolExecutor

        from ..evaluation.evaluator import evaluate_single_task
        from ..runner import run_single_task

        # Count tasks that need work (not already fully evaluated)
        total_tasks = sum(
            sum(1 for task in exp.tasks if task.task_key not in exp.skip_eval_keys)
            for exp in self.experiments
        )

        # Initialize per-experiment task counts for timing
        self._pool_start_time = time.monotonic()
        for exp in self.experiments:
            count = sum(1 for task in exp.tasks if task.task_key not in exp.skip_eval_keys)
            self._exp_task_counts[exp.key] = count

        if self.benchmark_logger:
            self.benchmark_logger.on_phase_start("exec+eval", total_tasks)
        else:
            logger.info(
                "Running %d tasks across %d experiments...", total_tasks, len(self.experiments)
            )

        # Build lookup for prior exec results by task key (for eval-only tasks)
        prior_exec_by_key: dict[str, dict[str, TaskExecutionResult]] = {}
        for exp in self.experiments:
            prior_exec_by_key[exp.key] = {r.task_key: r for r in exp.prior_exec_results}

        async def run_and_evaluate(
            exp: Experiment,
            task: KeyedCalendarTask,
            task_index: int,
        ) -> tuple[str, TaskEvaluationResult]:
            """Execute a task (if needed) and evaluate it."""
            config = exp.config

            # Check if we already have execution result (skip exec, run eval only)
            if task.task_key in exp.skip_exec_keys:
                exec_result = prior_exec_by_key[exp.key].get(task.task_key)
                if exec_result is None:
                    raise RuntimeError(
                        f"Task {task.task_key} in skip_exec_keys but no prior exec result"
                    )
            else:
                # Execute
                if not config.resolved_assistant_model or not config.resolved_requestor_model:
                    raise RuntimeError("Assistant and requestor models must be configured")
                exec_result = await run_single_task(
                    task,
                    task.task_key,
                    config.resolved_assistant_model,
                    exp.assistant_client,
                    config.resolved_requestor_model,
                    exp.requestor_client,
                    config.max_rounds,
                    config.max_steps_per_turn,
                    exp.system_prompt,
                    exp.assistant_explicit_cot,
                    exp.requestor_explicit_cot,
                    config.expose_preferences or False,
                    self.cancel_event,
                    self.benchmark_logger,
                )
                # Checkpoint execution
                exp.checkpoint_mgr.add_execution_result(exec_result)

            # Skip evaluation if cancelled — eval can happen on resume
            if self.cancel_event and self.cancel_event.is_set():
                raise asyncio.CancelledError("Skipping evaluation due to cancellation")

            # Evaluate
            if not config.resolved_judge_model:
                raise RuntimeError("Judge model must be configured")
            eval_result = await evaluate_single_task(
                exec_result,
                config.resolved_judge_model,
                exp.judge_client,
                config.judge_votes,
                self.benchmark_logger,
            )

            # Checkpoint evaluation
            exp.checkpoint_mgr.add_evaluation_result(eval_result)

            return (exp.key, eval_result)

        # Generate task coroutines
        def generate_tasks():
            for exp in self.experiments:
                for task_index, task in enumerate(exp.tasks):
                    # Skip already-evaluated tasks
                    if task.task_key in exp.skip_eval_keys:
                        continue
                    yield run_and_evaluate(exp, task, task_index)

        executor = TaskPoolExecutor(
            batch_size=self.batch_size,
            on_task_complete=self._on_task_complete,
            task_logger=logger,
            cancel_event=self.cancel_event,
        )

        try:
            await executor.run(generate_tasks())
        finally:
            # Always notify logger of phase completion (ensures progress bar is closed)
            if self.benchmark_logger:
                completed = sum(len(self._eval_results_by_exp[e.key]) for e in self.experiments)
                failed = sum(
                    1
                    for e in self.experiments
                    for r in self._eval_results_by_exp[e.key]
                    if r.eval_error is not None or r.execution.fatal_error is not None
                )
                self.benchmark_logger.on_phase_complete("exec+eval", completed - failed, failed)

    def _on_task_complete(self, tagged_result: tuple[str, TaskEvaluationResult]):
        """Handle completion of an exec+eval task."""
        exp_key, result = tagged_result
        self._eval_results_by_exp[exp_key].append(result)

        # Log when an experiment's last task completes
        expected = self._exp_task_counts.get(exp_key, 0)
        completed = len(self._eval_results_by_exp[exp_key])
        if expected > 0 and completed == expected:
            elapsed = time.monotonic() - self._pool_start_time
            self._exp_finish_times[exp_key] = elapsed
            exp = self._exp_by_key[exp_key]
            variant = exp.config.variant or exp_key
            logger.info(
                "Experiment %s finished (%d tasks) in %.1fs",
                variant,
                expected,
                elapsed,
            )


# ==============================================================================
# Multiple experiment runner (parallel pool)
# ==============================================================================


async def run_multiple(
    path: Path,
    output_base: Path | None = None,
    pattern: str | None = None,
    collect_only: bool = False,
    override_groups: list[dict] | None = None,
    batch_size: int = 100,
    benchmark_logger: BenchmarkLogger | None = None,
    restart_exec: bool = False,
    restart_eval: bool = False,
    llm_tracing: bool = False,
) -> tuple[int, int, int]:
    """Run multiple experiments sequentially.

    Args:
        path: File or directory to search for experiments
        output_base: Base directory for experiment outputs
        pattern: Optional pattern to filter experiment names
        collect_only: If True, only collect and print experiments without running
        override_groups: Optional list of override dicts
        batch_size: Number of tasks to run concurrently (per experiment)
        benchmark_logger: Optional logger for progress tracking
        restart_exec: If True, re-run execution for all experiments (clears exec checkpoints)
        restart_eval: If True, re-run evaluation for all experiments (clears eval checkpoints)
        llm_tracing: If True, enable LLM call tracing and save traces

    Returns:
        Tuple of (success_count, skipped_count, fail_count)
    """
    from .collect import collect_all

    if output_base is None:
        output_base = Path("outputs/calendar_scheduling")

    # Collect experiments
    raw_configs = collect_all(path, pattern, override_groups)

    print(f"Collected {len(raw_configs)} experiments")

    if not raw_configs:
        return (0, 0, 0)

    if collect_only:
        for _, name, _ in raw_configs:
            print(f"  {name}")
        return (0, 0, 0)

    # Set output_dir on each config, always including variant name for unique checkpoints
    configs = []
    for file_path, name, config in raw_configs:
        # Use base variant name (before any comma) for directory path
        # This keeps directories clean while still allowing override variants
        dir_name = name.split(",")[0]
        if config.output_dir is None:
            group_name = file_path.parent.name
            output_dir = output_base / group_name / dir_name
        else:
            # Experiment file sets base output_dir - append variant name
            output_dir = Path(config.output_dir) / dir_name
        config = config.model_copy(update={"output_dir": output_dir})
        configs.append(config)

    # Skip already completed experiments (unless restart_exec or restart_eval)
    experiments = []
    skipped = []
    for config in configs:
        run_paths = create_run_paths(config)
        # If restart_exec or restart_eval, don't skip completed experiments
        if not restart_exec and not restart_eval and (run_paths.output_dir / "eval.json").exists():
            skipped.append(config)
            continue
        experiments.append(config)

    if not experiments:
        print("\nNo experiments to run (all skipped)")
        return (0, len(skipped), 0)

    # Initialize tracer only when requested
    if llm_tracing:
        get_tracer()

    # Prepare all experiments
    print(f"\nPreparing {len(experiments)} experiments...")
    prepared = []
    for config in experiments:
        try:
            variant = config.variant or "default"
            parts = variant.split(",")
            print(f"  Preparing {parts[0]}...")
            for override in sorted(parts[1:]):
                print(f"    ...with {override}")
            exp = Experiment(config, restart_exec=restart_exec, restart_eval=restart_eval)
            prepared.append(exp)
        except Exception as e:
            logger.error("Failed to prepare %s: %s", config.variant or "default", e)

    if not prepared:
        print("No experiments could be prepared")
        return (0, len(skipped), len(experiments))

    total_tasks = sum(exp.task_count for exp in prepared)
    print(
        f"Running {total_tasks} tasks across {len(prepared)} experiments (unified pool, batch_size={batch_size})"
    )

    # Run with pool executor
    loop = asyncio.get_event_loop()
    cancel_event = asyncio.Event()

    def signal_handler():
        logger.warning("Interrupt received, cancelling tasks and saving checkpoints...")
        cancel_event.set()
        for exp in prepared:
            exp.checkpoint_mgr.set_interrupted(True)
        # Remove handlers so next Ctrl+C forces immediate exit
        for sig in (signal.SIGINT, signal.SIGTERM):
            loop.remove_signal_handler(sig)

    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, signal_handler)

    try:
        pool = ExperimentPoolExecutor(
            prepared,
            batch_size=batch_size,
            cancel_event=cancel_event,
            benchmark_logger=benchmark_logger,
            llm_tracing=llm_tracing,
        )
        sweep_start = time.monotonic()
        outputs = await pool.run()
        sweep_elapsed = time.monotonic() - sweep_start

        if cancel_event.is_set():
            print("Interrupted - checkpoints saved")
            if llm_tracing:
                for exp in prepared:
                    save_llm_traces(exp.run_paths)
            return (0, len(skipped), len(prepared))

        # Log per-experiment timing summary
        if pool._exp_finish_times:
            print("\n--- Experiment timing ---")
            for exp in prepared:
                elapsed = pool._exp_finish_times.get(exp.key)
                variant = exp.config.variant or exp.key
                if elapsed is not None:
                    mins, secs = divmod(elapsed, 60)
                    print(f"  {variant}: {int(mins)}m{secs:04.1f}s")

        # Save sweep_metadata.json to the common output directory
        all_output_dirs = [exp.run_paths.output_dir for exp in prepared]
        sweep_output_dir = (
            Path(os.path.commonpath(all_output_dirs)) if all_output_dirs else output_base
        )
        sweep_meta = {
            "total_sweep_seconds": sweep_elapsed,
            "experiment_count": len(prepared),
            "skipped_count": len(skipped),
            "timestamp": datetime.now().isoformat(),
        }
        sweep_meta_path = sweep_output_dir / "sweep_metadata.json"
        sweep_meta_path.parent.mkdir(parents=True, exist_ok=True)
        sweep_meta_path.write_text(json.dumps(sweep_meta, indent=2))
        logger.info("Saved sweep metadata to %s", sweep_meta_path)

        # Count results
        success_count = len(outputs)
        mins, secs = divmod(sweep_elapsed, 60)
        print(f"\nDone: {success_count} succeeded, {len(skipped)} skipped, 0 failed")
        print(f"Total sweep time: {int(mins)}m{secs:04.1f}s")
        return (success_count, len(skipped), 0)

    finally:
        # Remove signal handlers (may already be removed by signal_handler)
        for sig in (signal.SIGINT, signal.SIGTERM):
            try:
                loop.remove_signal_handler(sig)
            except (ValueError, RuntimeError):
                pass
