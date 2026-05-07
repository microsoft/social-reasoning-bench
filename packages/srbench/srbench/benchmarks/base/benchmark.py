"""The Benchmark ABC -- concrete lifecycle with abstract domain hooks."""

from __future__ import annotations

import argparse
import asyncio
import logging
import time
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any, Generic, get_args

from .checkpoint import CheckpointManager
from .types import (
    BenchmarkOutput,
    CheckpointData,
    TBenchmarkEvalResult,
    TConfig,
    TEvalResult,
    TExecResult,
    TTask,
)

logger = logging.getLogger(__name__)


def _parse_bool(value: str) -> bool:
    """Argparse ``type`` function for boolean flags.

    Args:
        value: String value to parse (e.g. ``'true'``, ``'false'``, ``'1'``, ``'0'``).

    Returns:
        The parsed boolean value.

    Raises:
        argparse.ArgumentTypeError: If *value* is not a recognized boolean string.
    """
    if value.lower() in ("true", "1", "yes"):
        return True
    if value.lower() in ("false", "0", "no"):
        return False
    raise argparse.ArgumentTypeError(f"Expected true/false, got {value!r}")


class Benchmark(ABC, Generic[TConfig, TTask, TExecResult, TEvalResult, TBenchmarkEvalResult]):
    """Abstract base class for SRBench benchmarks.

    Subclass and implement the abstract methods to create a fully
    functional benchmark with checkpointing, resume, parallel
    execution, CLI, and output serialization.
    """

    _checkpoint_data_type: type[CheckpointData]  # type: ignore[type-arg]
    _output_type: type[BenchmarkOutput]  # type: ignore[type-arg]

    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        for base in getattr(cls, "__orig_bases__", ()):
            args = get_args(base)
            if args and len(args) == 5:
                # args: TConfig, TTask, TExecResult, TEvalResult, TBenchmarkEvalResult
                cls._checkpoint_data_type = CheckpointData[args[2], args[3]]  # ty:ignore[invalid-type-form]
                cls._output_type = BenchmarkOutput[args[0], args[4], args[3]]  # ty:ignore[invalid-type-form]
                break

    # ==================================================================
    # Abstract methods
    # ==================================================================

    @classmethod
    @abstractmethod
    def benchmark_name(cls) -> str:
        """Short snake_case name (e.g. ``'calendar_scheduling'``).

        Returns:
            The benchmark's canonical name used in output paths and logging.
        """
        ...

    @classmethod
    @abstractmethod
    def add_benchmark_args(cls, parser: argparse.ArgumentParser) -> None:
        """Add benchmark-specific CLI flags to *parser*.

        Args:
            parser: The argument parser to extend with benchmark-specific flags.
        """
        ...

    @classmethod
    @abstractmethod
    def create_config(cls, args: argparse.Namespace) -> TConfig:
        """Build a run config from parsed CLI args.

        Args:
            args: Parsed command-line arguments from :meth:`create_parser`.

        Returns:
            A fully populated run configuration for this benchmark.
        """
        ...

    @abstractmethod
    def setup(self, config: TConfig) -> None:
        """Create model clients, load prompts, etc.

        Store anything the executor / evaluator needs as instance
        attributes (e.g. ``self.judge_client``).

        Args:
            config: The run configuration for this benchmark instance.
        """
        ...

    @abstractmethod
    async def execute_task(
        self,
        task: TTask,
        cancel_event: asyncio.Event | None = None,
    ) -> TExecResult:
        """Run a single task and return the execution result.

        Args:
            task: The task to execute.
            cancel_event: Optional event for cooperative cancellation.

        Returns:
            The execution result containing the task outcome.
        """
        ...

    @abstractmethod
    def make_execution_error_result(self, task: TTask, error: Exception) -> TExecResult:
        """Construct an exec result when execution fails.

        Called when :meth:`execute_task` raises.  The subclass knows
        which fields are required on its concrete ``TExecResult`` and
        can populate safe defaults alongside the error.

        Args:
            task: The task that failed during execution.
            error: The exception raised during execution.

        Returns:
            An error-state execution result with safe defaults for all required fields.
        """
        ...

    @abstractmethod
    async def evaluate_task(self, exec_result: TExecResult) -> TEvalResult:
        """Evaluate a single execution result.

        Args:
            exec_result: The completed execution result to evaluate.

        Returns:
            The evaluation result with scores across all enforced dimensions.
        """
        ...

    @abstractmethod
    def make_evaluation_error_result(
        self, exec_result: TExecResult, error: Exception
    ) -> TEvalResult:
        """Construct an eval result when evaluation fails.

        Called when :meth:`evaluate_task` raises.  The subclass knows
        which fields are required on its concrete ``TEvalResult`` and
        can populate safe defaults alongside the error.

        Args:
            exec_result: The execution result that was being evaluated.
            error: The exception raised during evaluation.

        Returns:
            An error-state evaluation result with safe defaults for all required fields.
        """
        ...

    @abstractmethod
    def compute_evaluation(
        self,
        eval_results: list[TEvalResult],
    ) -> TBenchmarkEvalResult:
        """Aggregate per-task results into a benchmark-level evaluation.

        Args:
            eval_results: List of per-task evaluation results to aggregate.

        Returns:
            A benchmark-level evaluation with averaged metrics across all tasks.
        """
        ...

    @abstractmethod
    def print_per_task_summary(self, eval_results: list[TEvalResult]) -> None:
        """Print a per-task table to stdout.

        Args:
            eval_results: List of per-task evaluation results to display.
        """
        ...

    @abstractmethod
    def print_evaluation_summary(self, evaluation: TBenchmarkEvalResult) -> None:
        """Print aggregate statistics to stdout.

        Args:
            evaluation: The benchmark-level evaluation to summarize.
        """
        ...

    # ==================================================================
    # Optional overrides (concrete defaults)
    # ==================================================================

    def get_run_path_models(self) -> list[str]:
        """Model names used in the output directory name.

        Override to list the agent models relevant to this benchmark
        (e.g. ``[config.resolved_buyer_model, ...]``).

        Returns:
            List of model name strings for directory naming.
        """
        return [self.config.model or "unknown"]

    def prepare_tasks(self, tasks: list[TTask]) -> list[TTask]:
        """Hook for preparing tasks after loading (e.g., hand-crafted injection).

        Called from ``__init__`` after tasks are set, regardless of whether
        they came from cache or a fresh ``load_tasks()`` call. Override in
        subclasses that need config-dependent task preparation.

        Args:
            tasks: The loaded tasks to potentially expand or transform.

        Returns:
            The (possibly expanded) list of tasks.
        """
        return tasks

    def load_tasks(self) -> tuple[list[TTask], dict[str, str]]:
        """Load tasks from ``self.config``.

        Default implementation raises -- override or pass tasks to
        :pymethod:`__init__` via *tasks*.

        Returns:
            A tuple of ``(tasks, file_hashes)`` where ``tasks`` is a list of
            loaded task objects and ``file_hashes`` maps source file paths to
            their content hashes.

        Raises:
            NotImplementedError: If the subclass does not override this method
                and no tasks were passed to ``__init__``.
        """
        raise NotImplementedError(
            f"{type(self).__name__} must override load_tasks() or pass tasks to __init__"
        )

    # ==================================================================
    # Concrete lifecycle
    # ==================================================================

    def __init__(
        self,
        config: TConfig,
        *,
        tasks: list[TTask] | None = None,
        file_hashes: dict[str, str] | None = None,
        restart_exec: bool = False,
        restart_eval: bool = False,
        benchmark_logger: Any = None,
    ) -> None:
        self.config = config
        self._benchmark_logger = benchmark_logger

        # -- paths --
        from .run_paths import RunPaths

        if config.output_dir:
            self.run_paths = RunPaths(Path(config.output_dir))
        else:
            self.run_paths = RunPaths.create_for_run(
                base_dir=Path(f"outputs/{self.benchmark_name()}"),
                models=self.get_run_path_models(),
            )
        self.run_paths.ensure_dir()

        # -- checkpoint --
        self.checkpoint_mgr: CheckpointManager[TExecResult, TEvalResult] = CheckpointManager(
            self.run_paths.checkpoint_path,
            checkpoint_model=self._checkpoint_data_type,
        )
        self.skip_exec_keys: set[str] = set()
        self.skip_eval_keys: set[str] = set()
        self.prior_exec_results: list[TExecResult] = []
        self.prior_eval_results: list[TEvalResult] = []

        # -- load prior results from checkpoint and/or results.json --
        # Both are sources of completed task state. Checkpoint has in-progress
        # work; results.json has completed runs. Merge both, dedup by task hash
        # (checkpoint takes precedence since it's more recent).
        all_exec_results: dict[str, TExecResult] = {}  # hash → result
        all_eval_results: dict[str, TEvalResult] = {}

        # Load prior results from checkpoint (in-progress) or results.json (completed).
        # Checkpoint is authoritative when it exists -- a checkpoint means the run
        # was interrupted or re-run, so results.json may be stale.
        if self.run_paths.checkpoint_path.exists():
            loaded = self.checkpoint_mgr.load()
            if loaded:
                exec_keys = self.checkpoint_mgr.completed_exec_keys
                eval_keys = self.checkpoint_mgr.completed_eval_keys

                if eval_keys and not exec_keys:
                    self._benchmark_logger.warning(
                        "Corrupt checkpoint deleted (eval keys without exec keys)"
                    )
                    self.checkpoint_mgr.cleanup()
                else:
                    for r in self.checkpoint_mgr.execution_results:
                        all_exec_results[r.task.hash] = r
                    for r in self.checkpoint_mgr.evaluation_results:
                        all_eval_results[r.execution.task.hash] = r
        elif self.run_paths.results_path.exists():
            try:
                prior_output = self._load_prior_output()
                for r in prior_output:
                    h = r.execution.task.hash
                    all_exec_results[h] = r.execution
                    all_eval_results[h] = r
            except Exception as exc:
                self._benchmark_logger.warning("Failed to load prior results.json: %s", exc)

        # Apply filtering based on flags
        bl = self._benchmark_logger
        if restart_exec:
            bl.info("Restart-exec: ignoring prior execution progress")
            all_exec_results.clear()
            all_eval_results.clear()  # can't eval without exec
        elif restart_eval:
            bl.info("Restart-eval: ignoring prior evaluation progress")
            all_eval_results.clear()

        # Always retry errored tasks on resume: remove execution and
        # evaluation results that finished with an error so they are
        # re-run instead of silently skipped.
        failed_count = 0
        for h in list(all_exec_results):
            if not all_exec_results[h].finished_successfully:
                del all_exec_results[h]
                all_eval_results.pop(h, None)
                failed_count += 1
        for h in list(all_eval_results):
            if not all_eval_results[h].finished_successfully:
                del all_eval_results[h]
                failed_count += 1
        if failed_count:
            bl.info("Retrying %d previously failed tasks", failed_count)

        self.skip_exec_keys = set(all_exec_results.keys())
        self.skip_eval_keys = set(all_eval_results.keys())
        self.prior_exec_results = list(all_exec_results.values())
        self.prior_eval_results = list(all_eval_results.values())

        if self.skip_exec_keys or self.skip_eval_keys:
            bl.info(
                "Loaded: %d successful executions, %d successful evaluations",
                len(self.skip_exec_keys),
                len(self.skip_eval_keys),
            )

        # -- tasks --
        if tasks is not None:
            self._raw_tasks = list(tasks)
            fh = file_hashes or {}
        else:
            self._raw_tasks, fh = self.load_tasks()
        self.tasks = self.prepare_tasks(list(self._raw_tasks))

        # reeval mode: reconstruct tasks from prior exec results
        if not self.tasks and self.prior_exec_results:
            self.tasks = [r.task for r in self.prior_exec_results]
            fh = {}

        # -- store file hashes for task cache sharing across benchmarks --
        self.file_hashes = fh

        # -- filter stale prior results --
        # Prior results whose task hash doesn't appear in the current task set
        # are stale (e.g., task schema changed, data regenerated). Discard them
        # so the user knows those tasks will be re-run.
        if self.tasks and (self.skip_exec_keys or self.skip_eval_keys):
            current_hashes = {t.hash for t in self.tasks}
            stale_exec = self.skip_exec_keys - current_hashes
            stale_eval = self.skip_eval_keys - current_hashes
            if stale_exec or stale_eval:
                bl.warning(
                    "Discarding %d stale prior results whose task hashes no longer "
                    "match the current task set (schema change or data regeneration). "
                    "These tasks will be re-run.",
                    len(stale_exec | stale_eval),
                )
                for h in stale_exec:
                    self.skip_exec_keys.discard(h)
                for h in stale_eval:
                    self.skip_eval_keys.discard(h)
                self.prior_exec_results = [
                    r for r in self.prior_exec_results if r.task.hash in current_hashes
                ]
                self.prior_eval_results = [
                    r for r in self.prior_eval_results if r.execution.task.hash in current_hashes
                ]

        # -- init checkpoint data (carry forward prior results so the on-disk
        #    checkpoint is never emptied during a resumed run) --
        self.checkpoint_mgr.initialize(
            config,
            fh,
            prior_exec_results=self.prior_exec_results,
            prior_eval_results=self.prior_eval_results,
        )

        # -- domain setup --
        self.setup(config)

    # ------------------------------------------------------------------
    # run() -- the main entry point
    # ------------------------------------------------------------------

    async def run(
        self,
        cancel_event: asyncio.Event | None = None,
    ) -> BenchmarkOutput[TConfig, TBenchmarkEvalResult, TEvalResult]:
        """Execute + evaluate all tasks, produce output.

        Args:
            cancel_event: Optional event for cooperative cancellation. When set,
                the executor stops pulling new tasks and saves a checkpoint.

        Returns:
            A ``BenchmarkOutput`` containing the config, aggregate evaluation,
            and all per-task evaluation results.
        """
        from ...shared.executors import TaskPoolExecutor

        prior_exec_by_key: dict[str, TExecResult] = {
            r.task.hash: r for r in self.prior_exec_results
        }

        new_eval_results: list[TEvalResult] = []

        def on_complete(result: TEvalResult | None) -> None:
            if result is not None:
                new_eval_results.append(result)

        def generate_tasks():
            for task in self.tasks:
                h = task.hash
                if h in self.skip_exec_keys and h in self.skip_eval_keys:
                    continue
                yield self._exec_and_eval_single(task, prior_exec_by_key, cancel_event)

        batch_size = self.config.batch_size
        executor = TaskPoolExecutor(
            batch_size=batch_size,
            on_task_complete=on_complete,
            task_logger=logger,
            cancel_event=cancel_event,
            task_concurrency=self.config.task_concurrency,
        )
        t0 = time.monotonic()
        await executor.run(generate_tasks())
        elapsed = time.monotonic() - t0

        # merge + sort
        all_eval = self.prior_eval_results + new_eval_results
        all_eval.sort(key=lambda r: r.execution.task.id)

        output = self._build_output(all_eval, elapsed)

        if not (cancel_event and cancel_event.is_set()):
            self._save_output(output)

        return output

    # ------------------------------------------------------------------
    # _exec_and_eval_single -- coupled exec+eval with skip-set logic
    # ------------------------------------------------------------------

    async def _exec_and_eval_single(
        self,
        task: TTask,
        prior_exec_by_key: dict[str, TExecResult],
        cancel_event: asyncio.Event | None = None,
    ) -> TEvalResult | None:
        from ...shared.logging import TaskCompleteParams, TaskStartParams

        h = task.hash
        bl = self._benchmark_logger
        t0 = time.monotonic()

        if bl:
            bl.on_task_start(
                TaskStartParams(
                    benchmark=self.benchmark_name(),
                    variant=self.config.variant,
                    task_id=task.id,
                    task_hash=h,
                )
            )

        error_msg: str | None = None
        variant_tag = self.config.variant or self.benchmark_name()

        # -- execution --
        if h in self.skip_exec_keys:
            exec_result = prior_exec_by_key.get(h)
            if exec_result is None:
                raise RuntimeError(f"Task {h} in skip_exec_keys but no prior exec result")
        else:
            logger.info("[%s] task %d: starting execution", variant_tag, task.id)
            try:
                exec_result = await self.execute_task(task, cancel_event)
            except Exception as exc:
                bl.error("Execution failed for task %s: %s", h, exc)
                error_msg = str(exc)
                exec_result = self.make_execution_error_result(task, exc)
            logger.info(
                "[%s] task %d: execution done (%.1fs)", variant_tag, task.id, time.monotonic() - t0
            )
            self.checkpoint_mgr.add_execution_result(exec_result, h)

        if cancel_event and cancel_event.is_set():
            raise asyncio.CancelledError("Cancelled before evaluation")

        # -- evaluation --
        if h in self.skip_eval_keys:
            return None

        if error_msg is not None:
            # Execution failed -- skip evaluation, create error eval result directly
            eval_result = self.make_evaluation_error_result(
                exec_result, Exception(f"Execution failed: {error_msg}")
            )
        else:
            logger.info("[%s] task %d: starting evaluation", variant_tag, task.id)
            try:
                eval_result = await self.evaluate_task(exec_result)
            except Exception as exc:
                bl.error("Evaluation failed for task %s: %s", h, exc)
                error_msg = str(exc)
                eval_result = self.make_evaluation_error_result(exec_result, exc)
        logger.info(
            "[%s] task %d: evaluation done (%.1fs)", variant_tag, task.id, time.monotonic() - t0
        )

        self.checkpoint_mgr.add_evaluation_result(eval_result, h)

        if bl:
            bl.on_task_complete(
                TaskCompleteParams(
                    benchmark=self.benchmark_name(),
                    variant=self.config.variant,
                    task_id=task.id,
                    task_hash=h,
                    success=error_msg is None,
                    error=error_msg,
                    elapsed_seconds=time.monotonic() - t0,
                )
            )

        return eval_result

    # ------------------------------------------------------------------
    # Finalize -- convert checkpoint to results without running tasks
    # ------------------------------------------------------------------

    def finalize(self) -> BenchmarkOutput[TConfig, TBenchmarkEvalResult, TEvalResult] | None:
        """Convert checkpoint data to results.json without running any tasks.

        Returns:
            The ``BenchmarkOutput``, or ``None`` if there are no eval results to finalize.
        """
        bl = self._benchmark_logger
        n_exec = len(self.prior_exec_results)
        n_eval = len(self.prior_eval_results)
        unevaluated = n_exec - n_eval

        if n_eval == 0:
            bl.warning("No evaluation results to finalize in %s", self.run_paths.output_dir)
            return None

        if unevaluated > 0:
            bl.warning(
                "%d tasks were executed but not evaluated (will be omitted from results)",
                unevaluated,
            )

        all_eval = list(self.prior_eval_results)
        all_eval.sort(key=lambda r: r.execution.task.id)
        output = self._build_output(all_eval)
        self._save_output(output)
        bl.info(
            "Finalized %d results to %s",
            len(all_eval),
            self.run_paths.results_path,
        )
        return output

    # ------------------------------------------------------------------
    # Output building + saving
    # ------------------------------------------------------------------

    def _build_output(
        self,
        eval_results: list[TEvalResult],
        elapsed_seconds: float = 0.0,
    ) -> BenchmarkOutput[TConfig, TBenchmarkEvalResult, TEvalResult]:
        evaluation = self.compute_evaluation(eval_results)
        return BenchmarkOutput(
            config=self.config,
            timestamp=datetime.now().isoformat(),
            elapsed_seconds=elapsed_seconds,
            evaluation=evaluation,
            results=eval_results,
        )

    def _load_prior_output(self) -> list[TEvalResult]:
        """Load eval results from a prior results.json.

        Returns:
            List of evaluation results deserialized from the results file.
        """
        output = self._output_type.model_validate_json(self.run_paths.results_path.read_text())
        return output.results

    def _save_output(
        self,
        output: BenchmarkOutput[TConfig, TBenchmarkEvalResult, TEvalResult],
    ) -> None:
        self.run_paths.results_path.write_text(output.model_dump_json(indent=2))
        self._benchmark_logger.info(
            "Saved %d results to %s",
            len(output.results),
            self.run_paths.results_path,
        )

        self.checkpoint_mgr.cleanup()

    # ------------------------------------------------------------------
    # CLI
    # ------------------------------------------------------------------

    @classmethod
    def create_parser(cls) -> argparse.ArgumentParser:
        """Build a full argument parser (shared flags + benchmark-specific).

        Returns:
            An ``ArgumentParser`` with both base and benchmark-specific arguments.
        """
        parser = cls._create_base_parser()
        cls.add_benchmark_args(parser)
        return parser

    @classmethod
    def _create_base_parser(cls) -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(
            description=f"{cls.benchmark_name()} benchmark",
            allow_abbrev=False,
        )

        # -- data & limits --
        g = parser.add_argument_group("data & limits")
        g.add_argument("--data", nargs="+", dest="paths", help="YAML files or directories")
        g.add_argument("--limit", type=int, default=None)
        g.add_argument("--batch-size", type=int, default=32)
        g.add_argument("--max-rounds", type=int, default=20)
        g.add_argument("--max-steps-per-turn", type=int, default=20)
        g.add_argument(
            "--task-concurrency",
            type=int,
            default=None,
            help="Max concurrent LLM calls per task per provider (default: unlimited)",
        )
        g.add_argument(
            "--llm-concurrency",
            type=int,
            default=None,
            help="Max total concurrent LLM calls per provider across all tasks (default: unlimited)",
        )

        # -- model defaults --
        g = parser.add_argument_group("model")
        g.add_argument("--model", help="Default model for all agents")
        g.add_argument("--base-url", default=None)
        g.add_argument("--api-version", default=None)

        # -- judge --
        g = parser.add_argument_group("judge")
        g.add_argument("--judge-model", default=None)
        g.add_argument("--judge-base-url", default=None)
        g.add_argument("--judge-api-version", default=None)
        g.add_argument("--judge-votes", type=int, default=3)
        g.add_argument("--judge-reasoning-effort", default=None)

        # -- system prompt --
        g = parser.add_argument_group("system prompt")
        g.add_argument(
            "--system-prompt",
            choices=["none", "privacy", "dd_info_gathering", "dd_advocacy", "oo"],
            default=None,
        )

        # -- reasoning & CoT --
        g = parser.add_argument_group("reasoning")
        g.add_argument("--reasoning-effort", default=None)
        g.add_argument("--explicit-cot", type=_parse_bool, default=None, metavar="{true,false}")

        # -- resume --
        g = parser.add_argument_group("resume")
        g.add_argument("--resume", nargs="?", const=True, default=None)
        g.add_argument("--force-resume", action="store_true", default=False)
        g.add_argument("--restart-eval", action="store_true", default=False)
        g.add_argument("--restart-exec", action="store_true", default=False)
        g.add_argument(
            "--finalize",
            action="store_true",
            default=False,
            help="Convert checkpoint.json to results.json without running any tasks",
        )

        # -- handcrafted injection --
        g = parser.add_argument_group("handcrafted injection")
        g.add_argument(
            "--attack-types",
            nargs="+",
            default=None,
            help="Hand-crafted attack types to inject at runtime (e.g. privacy duty_of_care)",
        )

        # -- output --
        g = parser.add_argument_group("output")
        g.add_argument("--output-dir", default=None)
        g.add_argument(
            "--log-level", default="warning", choices=["debug", "info", "warning", "error"]
        )
        g.add_argument("--logger", default="progress", choices=["verbose", "progress", "quiet"])

        return parser

    @classmethod
    def main(cls) -> None:
        """CLI entry point.  Parse args, create config, run."""
        from srbench_llm import concurrency

        from ...shared.logging import create_benchmark_logger

        parser = cls.create_parser()
        args = parser.parse_args()
        config = cls.create_config(args)

        llm_concurrency = getattr(args, "llm_concurrency", None)
        task_concurrency = getattr(args, "task_concurrency", None)
        if llm_concurrency is not None or task_concurrency is not None:
            concurrency.configure(llm_size=llm_concurrency, task_size=task_concurrency)

        bl = create_benchmark_logger(
            getattr(args, "logger", "verbose"),
            log_level=getattr(args, "log_level", "info"),
        )

        benchmark = cls(
            config,
            restart_exec=getattr(args, "restart_exec", False),
            restart_eval=getattr(args, "restart_eval", False),
            benchmark_logger=bl,
        )

        if getattr(args, "finalize", False):
            output = benchmark.finalize()
            if output is None:
                import sys

                sys.exit(1)
            return

        asyncio.run(benchmark.run())
