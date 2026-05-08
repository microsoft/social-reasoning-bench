"""Experiment runner: signal handling, single/multi-experiment orchestration.

Operates on :class:`~srbench.benchmarks.base.Benchmark` instances.  The caller
creates (or provides a factory for) concrete ``Benchmark`` subclasses;
this module handles interrupt handling, cross-experiment task pooling, and
sweep-level bookkeeping.
"""

from __future__ import annotations

import asyncio
import json
import logging
import os
import re
import signal
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Iterable

from ..benchmarks.base.benchmark import Benchmark
from ..benchmarks.base.types import BaseRunConfig, BenchmarkOutput
from ..shared.executors import TaskPoolExecutor
from ..shared.logging import (
    BenchmarkLogger,
    LogParams,
    SweepCompleteParams,
    SweepStartParams,
    create_benchmark_logger,
)
from .collect import collect_all

logger = logging.getLogger(__name__)


def _resolve_setting(
    cli_value: int | None,
    config_values: Iterable[int | None],
    default: int | None = None,
) -> int | None:
    """CLI wins if explicitly set; else max of non-None config values; else default."""
    if cli_value is not None:
        return cli_value
    non_none = [v for v in config_values if v is not None]
    if non_none:
        return max(non_none)
    return default


class RunCancelled(Exception):
    """Raised when a run is cancelled via interrupt."""

    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        super().__init__(f"Run cancelled. Output dir: {output_dir}")


# ──────────────────────────────────────────────────────────────────────
# Single-experiment helpers
# ──────────────────────────────────────────────────────────────────────


async def run_single_async(
    benchmark: Benchmark,
) -> BenchmarkOutput:
    """Run a single benchmark with signal handling.

    Args:
        benchmark: The prepared ``Benchmark`` instance to execute.

    Returns:
        The ``BenchmarkOutput`` containing config, evaluation, and per-task results.

    Raises:
        RunCancelled: If the run is interrupted via SIGINT/SIGTERM.
    """
    loop = asyncio.get_event_loop()
    cancel_event = asyncio.Event()

    def signal_handler():
        logger.warning("Interrupt received, cancelling tasks and saving checkpoint...")
        cancel_event.set()
        for sig in (signal.SIGINT, signal.SIGTERM):
            loop.remove_signal_handler(sig)

    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, signal_handler)

    try:
        output = await benchmark.run(cancel_event=cancel_event)

        if cancel_event.is_set():
            logger.info(
                "Run cancelled, checkpoint saved to %s",
                benchmark.run_paths.checkpoint_path,
            )
            raise RunCancelled(str(benchmark.run_paths.output_dir))

        return output
    finally:
        for sig in (signal.SIGINT, signal.SIGTERM):
            try:
                loop.remove_signal_handler(sig)
            except (ValueError, RuntimeError):
                pass


def run_single(benchmark: Benchmark) -> BenchmarkOutput:
    """Run a single benchmark synchronously.  See :func:`run_single_async`.

    Args:
        benchmark: The prepared ``Benchmark`` instance to execute.

    Returns:
        The ``BenchmarkOutput`` containing config, evaluation, and per-task results.
    """
    return asyncio.run(run_single_async(benchmark))


# ──────────────────────────────────────────────────────────────────────
# Cross-experiment pool executor
# ──────────────────────────────────────────────────────────────────────


class ExperimentPoolExecutor:
    """Runs multiple benchmarks with a unified task pool.

    Instead of running benchmarks sequentially (which causes "tail draining"
    where a few remaining tasks block starting the next experiment), this
    pools all tasks together in a single :class:`TaskPoolExecutor`.
    """

    def __init__(
        self,
        benchmarks: list[Benchmark],
        batch_size: int = 100,
        cancel_event: asyncio.Event | None = None,
        benchmark_logger: BenchmarkLogger | None = None,
        task_concurrency: int | None = None,
    ):
        self.benchmarks = benchmarks
        self.batch_size = batch_size
        self.cancel_event = cancel_event
        self.bl = benchmark_logger
        self.task_concurrency = task_concurrency

        self._results_by_bm: dict[int, list] = {id(bm): [] for bm in benchmarks}
        self._task_counts: dict[int, int] = {}
        self._finish_times: dict[int, float] = {}
        self._start_time: float = 0.0
        self.total_tasks: int = 0
        self.skipped_tasks: int = 0

    async def run(self) -> list[BenchmarkOutput]:
        """Run all benchmarks and return their outputs.

        Returns:
            A list of ``BenchmarkOutput`` objects, one per benchmark. Returns an
            empty list if the run was cancelled.
        """
        self._start_time = time.monotonic()

        total_all = 0
        total_skipped = 0
        for bm in self.benchmarks:
            bm_total = len(bm.tasks)
            bm_skipped = sum(
                1 for t in bm.tasks if t.hash in bm.skip_exec_keys and t.hash in bm.skip_eval_keys
            )
            count = bm_total - bm_skipped
            self._task_counts[id(bm)] = count
            total_all += bm_total
            total_skipped += bm_skipped

        total = sum(self._task_counts.values())

        self.total_tasks = total_all
        self.skipped_tasks = total_skipped

        if total_skipped:
            logger.info(
                "Resuming: %d/%d tasks remaining (%d checkpointed)",
                total,
                total_all,
                total_skipped,
            )

        if self.bl:
            self.bl.on_sweep_start(
                SweepStartParams(
                    total_tasks=total,
                    total_experiments=len(self.benchmarks),
                    experiments=[
                        LogParams(
                            benchmark=bm.benchmark_name(),
                            variant=bm.config.variant,
                        )
                        for bm in self.benchmarks
                    ],
                )
            )

        def generate_all():
            for bm in self.benchmarks:
                prior_exec_by_key = {r.task.hash: r for r in bm.prior_exec_results}
                for task in bm.tasks:
                    h = task.hash
                    if h in bm.skip_exec_keys and h in bm.skip_eval_keys:
                        continue
                    yield self._tagged_task(bm, task, prior_exec_by_key)

        executor = TaskPoolExecutor(
            batch_size=self.batch_size,
            on_task_complete=self._on_complete,
            task_logger=logger,
            cancel_event=self.cancel_event,
            task_concurrency=self.task_concurrency,
        )
        await executor.run(generate_all())

        elapsed = time.monotonic() - self._start_time

        if self.cancel_event and self.cancel_event.is_set():
            if self.bl:
                all_results = [r for v in self._results_by_bm.values() for r in v]
                failed = sum(
                    1
                    for r in all_results
                    if not r.finished_successfully or not r.execution.finished_successfully
                )
                succeeded = len(all_results) - failed
                self.bl.on_sweep_complete(
                    SweepCompleteParams(completed=succeeded, failed=failed, elapsed_seconds=elapsed)
                )
            return []

        # Finalize each benchmark
        outputs: list[BenchmarkOutput] = []
        for bm in self.benchmarks:
            new_results = self._results_by_bm[id(bm)]
            all_eval = bm.prior_eval_results + new_results
            all_eval.sort(key=lambda r: r.execution.task.id)
            bm_elapsed = self._finish_times.get(id(bm), elapsed)
            output = bm._build_output(all_eval, bm_elapsed)
            bm._save_output(output)
            outputs.append(output)

        if self.bl:
            self.bl.on_sweep_complete(
                SweepCompleteParams(
                    completed=len(outputs),
                    failed=0,
                    elapsed_seconds=elapsed,
                )
            )

        return outputs

    async def _tagged_task(self, bm: Benchmark, task: Any, prior_exec_by_key: dict) -> Any:
        result = await bm._exec_and_eval_single(task, prior_exec_by_key, self.cancel_event)
        return (id(bm), result)

    def _on_complete(self, tagged: Any) -> None:
        bm_id, result = tagged
        if result is not None:
            self._results_by_bm[bm_id].append(result)

        expected = self._task_counts.get(bm_id, 0)
        completed = len(self._results_by_bm[bm_id])
        if expected > 0 and completed >= expected:
            self._finish_times[bm_id] = time.monotonic() - self._start_time


# ──────────────────────────────────────────────────────────────────────
# Multi-experiment sweep
# ──────────────────────────────────────────────────────────────────────


async def run_multiple(
    benchmark_factory: Callable[..., Benchmark],
    path: Path,
    *,
    output_base: Path | None = None,
    patterns: list[str] | None = None,
    override_groups: list[dict] | None = None,
    batch_size: int | None = None,
    task_concurrency: int | None = None,
    llm_concurrency: int | None = None,
    restart_exec: bool = False,
    restart_eval: bool = False,
    finalize: bool = False,
    logger_style: str = "progress",
    log_level: str = "info",
) -> tuple[int, int, int]:
    """Collect and run multiple experiments.

    Args:
        benchmark_factory: Callable ``(config, *, restart_exec, restart_eval,
            benchmark_logger) -> Benchmark``.
        path: File or directory to search for ``experiment_*.py`` files.
        output_base: Base directory for experiment outputs.
        patterns: Optional list of patterns to filter experiment names (OR logic).
        override_groups: Optional list of override dicts.
        batch_size: Maximum concurrent tasks across all experiments. If None,
            uses max across collected configs (fallback 100).
        task_concurrency: Max concurrent LLM calls per task per provider. If
            None, uses max across collected configs.
        llm_concurrency: Max total concurrent LLM calls per provider. If None,
            uses max across collected configs.
        restart_exec: Re-run execution (ignore checkpointed execution progress).
        restart_eval: Re-run evaluation (ignore checkpointed evaluation progress).
        finalize: Convert checkpoint.json to results.json without running tasks.
        logger_style: Logger style — 'verbose', 'progress', or 'quiet'.
        log_level: Python logging level for library loggers (e.g. 'info', 'warning').

    Returns:
        ``(success_count, skipped_count, fail_count)``
    """
    from srbench_llm import concurrency

    bl = create_benchmark_logger(logger_style, log_level=log_level)

    raw_configs = collect_all(path, patterns, override_groups)

    print(f"Collected {len(raw_configs)} experiments")
    if not raw_configs:
        return (0, 0, 0)

    # Resolve effective concurrency: CLI wins if set, else max across configs.
    config_objs = [c for _, _, c in raw_configs]
    resolved_batch = _resolve_setting(batch_size, [c.batch_size for c in config_objs], default=100)
    batch_size = resolved_batch if resolved_batch is not None else 100
    task_concurrency = _resolve_setting(task_concurrency, [c.task_concurrency for c in config_objs])
    llm_concurrency = _resolve_setting(llm_concurrency, [c.llm_concurrency for c in config_objs])
    print(
        f"  batch_size={batch_size}  task_concurrency={task_concurrency}  "
        f"llm_concurrency={llm_concurrency}"
    )

    if llm_concurrency is not None or task_concurrency is not None:
        concurrency.configure(llm_size=llm_concurrency, task_size=task_concurrency)

    # Set output_dir on each config
    configs: list[BaseRunConfig] = []
    for file_path, name, config in raw_configs:
        dir_name = re.sub(r'[/\\:*?"<>|]', "_", name)
        if config.output_dir is None:
            base = output_base or Path("outputs")
            group_name = file_path.parent.name

            # If overrides were applied, the name contains "variant,k=v,k=v".
            # Split into variant (leaf dir) and override suffix (group dir).
            if "," in dir_name:
                variant_part, override_part = dir_name.split(",", 1)
                output_dir = base / f"{group_name},{override_part}" / variant_part
            else:
                output_dir = base / group_name / dir_name
        else:
            output_dir = Path(config.output_dir) / dir_name
        config = config.model_copy(update={"output_dir": output_dir, "batch_size": batch_size})
        configs.append(config)

    # All resume/retry logic is task-level (inside Benchmark.__init__).
    to_run = configs

    if not to_run:
        print("\nNo experiments found.")
        return (0, 0, 0)

    # Prepare benchmarks — fail fast if any experiment can't be prepared.
    # Cache loaded tasks so configs sharing the same data files skip
    # repeated YAML parsing, hashing, and validation.
    print(f"\nPreparing {len(to_run)} experiments...")
    prepared: list[Benchmark] = []
    task_cache: dict[tuple, tuple[list, dict]] = {}
    for config in to_run:
        variant = config.variant or "default"
        print(f"  Preparing {variant.split(',')[0]}...")
        cache_key = (type(config).__name__, tuple(config.paths), config.limit)
        kwargs: dict[str, Any] = dict(
            restart_exec=restart_exec,
            restart_eval=restart_eval,
            benchmark_logger=bl,
        )
        if cache_key in task_cache:
            kwargs["tasks"], kwargs["file_hashes"] = task_cache[cache_key]
        bm = benchmark_factory(config, **kwargs)
        if cache_key not in task_cache:
            task_cache[cache_key] = (bm._raw_tasks, bm.file_hashes)
        prepared.append(bm)

    total_tasks = 0
    for bm in prepared:
        loaded = len(bm.tasks)
        skip_exec = len(bm.skip_exec_keys)
        skip_eval = len(bm.skip_eval_keys)
        remaining = sum(
            1 for t in bm.tasks if not (t.hash in bm.skip_exec_keys and t.hash in bm.skip_eval_keys)
        )
        variant = bm.config.variant or bm.benchmark_name()
        print(
            f"  {variant}: {loaded} tasks loaded, "
            f"{skip_exec} prior exec, {skip_eval} prior eval, "
            f"{remaining} to run"
        )
        total_tasks += remaining

    if finalize:
        print(f"\nFinalizing {len(prepared)} experiments...")
        finalized = 0
        for bm in prepared:
            output = bm.finalize()
            variant = bm.config.variant or bm.benchmark_name()
            if output is not None:
                print(f"  {variant}: finalized {len(output.results)} results")
                bm.print_per_task_summary(output.results)
                bm.print_evaluation_summary(output.evaluation)
                finalized += 1
            else:
                print(f"  {variant}: no evaluation results to finalize")
        print(f"\nFinalized {finalized}/{len(prepared)} experiments")
        return (finalized, 0, len(prepared) - finalized)

    if total_tasks == 0:
        print("\nNo tasks to run (all completed)")
        return (0, 0, 0)

    print(
        f"Running {total_tasks} tasks across {len(prepared)} experiments "
        f"(unified pool, batch_size={batch_size})",
        flush=True,
    )

    # Signal handling
    loop = asyncio.get_event_loop()
    cancel_event = asyncio.Event()

    interrupt_count = 0

    def signal_handler():
        nonlocal interrupt_count
        interrupt_count += 1
        if interrupt_count == 1:
            print("\nKEYBOARD INTERRUPT RECEIVED, CHECKPOINTING...", flush=True)
            cancel_event.set()
        else:
            # Second interrupt: force exit immediately
            print("\nSECOND INTERRUPT, FORCING EXIT...", flush=True)
            for sig in (signal.SIGINT, signal.SIGTERM):
                loop.remove_signal_handler(sig)
            raise KeyboardInterrupt

    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, signal_handler)

    try:
        pool = ExperimentPoolExecutor(
            prepared,
            batch_size=batch_size,
            cancel_event=cancel_event,
            benchmark_logger=bl,
            task_concurrency=task_concurrency,
        )
        sweep_start = time.monotonic()
        outputs = await pool.run()
        sweep_elapsed = time.monotonic() - sweep_start

        if cancel_event.is_set():
            print("Interrupted — checkpoints saved")
            return (0, pool.skipped_tasks, 0)

        # Per-experiment evaluation summaries
        for bm, output in zip(prepared, outputs):
            variant = bm.config.variant or bm.benchmark_name()
            print(f"\n{'=' * 50}")
            print(f"  {variant} ({bm.benchmark_name()})")
            print(f"{'=' * 50}")
            bm.print_per_task_summary(output.results)
            bm.print_evaluation_summary(output.evaluation)

        # Per-experiment timing summary
        if pool._finish_times:
            print("\n--- Experiment timing ---")
            for bm in prepared:
                elapsed = pool._finish_times.get(id(bm))
                variant = bm.config.variant or str(bm.run_paths.output_dir)
                if elapsed is not None:
                    mins, secs = divmod(elapsed, 60)
                    print(f"  {variant}: {int(mins)}m{secs:04.1f}s")

        # Per-provider throughput summary
        provider_metrics = concurrency.get_metrics()
        provider_metrics_json: dict[str, dict] = {}
        if provider_metrics:
            now = time.monotonic()
            print("\n--- Provider throughput ---")
            for provider, m in sorted(provider_metrics.items()):
                if m.call_count == 0:
                    continue
                bench_elapsed = (now - m.first_call_time) if m.first_call_time is not None else 0.0
                bench_out_tps = m.completion_tokens / bench_elapsed if bench_elapsed > 0 else 0.0
                bench_tot_tps = m.total_tokens / bench_elapsed if bench_elapsed > 0 else 0.0
                call_out_tps = m.completion_tokens / m.call_seconds if m.call_seconds > 0 else 0.0
                call_tot_tps = m.total_tokens / m.call_seconds if m.call_seconds > 0 else 0.0
                print(
                    f"  {provider}: {m.call_count:,} calls, "
                    f"{m.prompt_tokens:,} prompt + {m.completion_tokens:,} completion = {m.total_tokens:,} tokens"
                )
                print(
                    f"    benchmark: {bench_out_tps:,.0f} output tok/s, {bench_tot_tps:,.0f} total tok/s"
                )
                print(
                    f"    per-call:  {call_out_tps:,.0f} output tok/s, {call_tot_tps:,.0f} total tok/s"
                )
                print(f"    avg in-flight: {m.in_flight_ema:.1f}")
                provider_metrics_json[provider] = {
                    "call_count": m.call_count,
                    "prompt_tokens": m.prompt_tokens,
                    "completion_tokens": m.completion_tokens,
                    "total_tokens": m.total_tokens,
                    "call_seconds": round(m.call_seconds, 2),
                    "benchmark_output_tps": round(bench_out_tps, 1),
                    "benchmark_total_tps": round(bench_tot_tps, 1),
                    "call_output_tps": round(call_out_tps, 1),
                    "call_total_tps": round(call_tot_tps, 1),
                    "in_flight_ema": round(m.in_flight_ema, 1),
                }

        # Save sweep metadata
        all_output_dirs = [bm.run_paths.output_dir for bm in prepared]
        sweep_output_dir = (
            Path(os.path.commonpath(all_output_dirs))
            if all_output_dirs
            else output_base or Path("outputs")
        )
        sweep_meta: dict[str, Any] = {
            "total_sweep_seconds": sweep_elapsed,
            "experiment_count": len(prepared),
            "skipped_tasks": pool.skipped_tasks,
            "timestamp": datetime.now().isoformat(),
        }
        if provider_metrics_json:
            sweep_meta["provider_metrics"] = provider_metrics_json
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        sweep_meta_path = sweep_output_dir / f"sweep_metadata_{ts}.json"
        sweep_meta_path.parent.mkdir(parents=True, exist_ok=True)
        sweep_meta_path.write_text(json.dumps(sweep_meta, indent=2))

        completed_tasks = sum(len(o.results) for o in outputs)
        failed_tasks = sum(
            1
            for o in outputs
            for r in o.results
            if not r.finished_successfully or not r.execution.finished_successfully
        )
        succeeded_tasks = completed_tasks - failed_tasks
        skipped_tasks = pool.skipped_tasks
        mins, secs = divmod(sweep_elapsed, 60)
        print(
            f"\nDone: {succeeded_tasks} succeeded, {failed_tasks} failed, {skipped_tasks} skipped ({completed_tasks}/{pool.total_tasks} total)"
        )
        print(f"Total sweep time: {int(mins)}m{secs:04.1f}s")
        return (succeeded_tasks, skipped_tasks, failed_tasks)

    finally:
        for sig in (signal.SIGINT, signal.SIGTERM):
            try:
                loop.remove_signal_handler(sig)
            except (ValueError, RuntimeError):
                pass
