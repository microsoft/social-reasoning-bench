"""Benchmark logging with structured event params."""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from tqdm import tqdm

_logger = logging.getLogger(__name__)


# ── Event params ─────────────────────────────────────────────────────


@dataclass
class LogParams:
    """Base context carried by every log event."""

    benchmark: str
    variant: str | None = None


@dataclass
class SweepStartParams:
    """Emitted when a multi-experiment sweep begins."""

    total_tasks: int
    total_experiments: int
    experiments: list[LogParams] = field(default_factory=list)


@dataclass
class SweepCompleteParams:
    """Emitted when a sweep finishes."""

    completed: int
    failed: int
    elapsed_seconds: float


@dataclass
class TaskStartParams(LogParams):
    """Emitted when a single exec+eval unit begins."""

    task_id: int = 0
    task_hash: str = ""


@dataclass
class TaskPhaseParams(LogParams):
    """Emitted when a task transitions between phases (exec → eval)."""

    task_id: int = 0
    phase: str = ""  # "exec", "eval"


@dataclass
class TaskStepParams(LogParams):
    """Emitted on each agent step (tool call) within execution."""

    task_id: int = 0
    step: int = 0
    round: int = 0
    action: str = ""  # tool name


@dataclass
class TaskCompleteParams(LogParams):
    """Emitted when a single exec+eval unit finishes."""

    task_id: int = 0
    task_hash: str = ""
    success: bool = True
    error: str | None = None
    elapsed_seconds: float = 0.0


# ── Logger ABC ───────────────────────────────────────────────────────


class BenchmarkLogger(ABC):
    """Base class for benchmark logging strategies."""

    # -- structured events --

    @abstractmethod
    def on_sweep_start(self, params: SweepStartParams) -> None: ...

    @abstractmethod
    def on_sweep_complete(self, params: SweepCompleteParams) -> None: ...

    @abstractmethod
    def on_task_start(self, params: TaskStartParams) -> None: ...

    @abstractmethod
    def on_task_complete(self, params: TaskCompleteParams) -> None: ...

    def on_task_phase(self, params: TaskPhaseParams) -> None:
        """Optional: called on exec→eval phase transition."""

    def on_task_step(self, params: TaskStepParams) -> None:
        """Optional: called on each agent step (tool call)."""

    # -- general logging --

    @abstractmethod
    def debug(self, message: str, *args: object) -> None: ...

    @abstractmethod
    def info(self, message: str, *args: object) -> None: ...

    @abstractmethod
    def warning(self, message: str, *args: object) -> None: ...

    @abstractmethod
    def error(self, message: str, *args: object) -> None: ...

    # -- context manager --

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


# ── Implementations ──────────────────────────────────────────────────


class VerboseLogger(BenchmarkLogger):
    """Logs every event via the standard logging module."""

    def __init__(self, log: logging.Logger | None = None):
        self._log = log or _logger

    def on_sweep_start(self, params: SweepStartParams) -> None:
        self._log.info(
            "Starting sweep: %d tasks across %d experiments",
            params.total_tasks,
            params.total_experiments,
        )
        for exp in params.experiments:
            self._log.info("  %s [%s]", exp.variant or "default", exp.benchmark)

    def on_sweep_complete(self, params: SweepCompleteParams) -> None:
        self._log.info(
            "Sweep complete: %d succeeded, %d failed in %.1fs",
            params.completed,
            params.failed,
            params.elapsed_seconds,
        )

    def on_task_start(self, params: TaskStartParams) -> None:
        tag = f"{params.benchmark}/{params.variant}" if params.variant else params.benchmark
        self._log.info("[%s] Task %d started", tag, params.task_id)

    def on_task_complete(self, params: TaskCompleteParams) -> None:
        tag = f"{params.benchmark}/{params.variant}" if params.variant else params.benchmark
        if params.error:
            self._log.error(
                "[%s] Task %d failed (%.1fs): %s",
                tag,
                params.task_id,
                params.elapsed_seconds,
                params.error,
            )
        else:
            self._log.info(
                "[%s] Task %d completed (%.1fs)",
                tag,
                params.task_id,
                params.elapsed_seconds,
            )

    def debug(self, message: str, *args: object) -> None:
        self._log.debug(message, *args)

    def info(self, message: str, *args: object) -> None:
        self._log.info(message, *args)

    def warning(self, message: str, *args: object) -> None:
        self._log.warning(message, *args)

    def error(self, message: str, *args: object) -> None:
        self._log.error(message, *args)


class ProgressLogger(BenchmarkLogger):
    """Shows a tqdm progress bar across all tasks."""

    def __init__(self, log: logging.Logger | None = None):
        self._log = log or _logger
        self._pbar: tqdm | None = None

    def on_sweep_start(self, params: SweepStartParams) -> None:
        if self._pbar:
            self._pbar.close()
        self._pbar = tqdm(
            total=params.total_tasks,
            desc=f"Running ({params.total_experiments} experiments)",
            unit="task",
            dynamic_ncols=True,
        )

    def on_sweep_complete(self, params: SweepCompleteParams) -> None:
        if self._pbar:
            self._pbar.close()
            self._pbar = None
        print(
            f"Done: {params.completed} succeeded, {params.failed} failed "
            f"in {params.elapsed_seconds:.1f}s"
        )

    def on_task_start(self, params: TaskStartParams) -> None:
        if self._pbar:
            tag = f"{params.benchmark}/{params.variant}" if params.variant else params.benchmark
            self._pbar.set_postfix_str(f"{tag} task {params.task_id}")

    def on_task_phase(self, params: TaskPhaseParams) -> None:
        if self._pbar:
            tag = params.variant or params.benchmark
            self._pbar.set_postfix_str(f"{tag} task {params.task_id} {params.phase}")

    def on_task_step(self, params: TaskStepParams) -> None:
        if self._pbar:
            tag = params.variant or params.benchmark
            self._pbar.set_postfix_str(
                f"{tag} task {params.task_id} r{params.round} {params.action}"
            )

    def on_task_complete(self, params: TaskCompleteParams) -> None:
        if self._pbar:
            self._pbar.update(1)
        if params.error:
            tag = f"{params.benchmark}/{params.variant}" if params.variant else params.benchmark
            tqdm.write(f"[{tag}] Task {params.task_id} failed: {params.error}")

    def debug(self, message: str, *args: object) -> None:
        pass  # suppress under progress bar

    def info(self, message: str, *args: object) -> None:
        formatted = message % args if args else message
        if self._pbar:
            self._pbar.set_postfix_str(formatted)
            self._pbar.refresh()
        else:
            print(formatted)

    def warning(self, message: str, *args: object) -> None:
        formatted = message % args if args else message
        tqdm.write(f"WARNING: {formatted}")

    def error(self, message: str, *args: object) -> None:
        formatted = message % args if args else message
        tqdm.write(f"ERROR: {formatted}")

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._pbar:
            self._pbar.close()
            self._pbar = None


class QuietLogger(BenchmarkLogger):
    """Only errors and final summary. Good for CI."""

    def __init__(self, log: logging.Logger | None = None):
        self._log = log or _logger
        self._errors: list[str] = []

    def on_sweep_start(self, params: SweepStartParams) -> None:
        self._errors.clear()

    def on_sweep_complete(self, params: SweepCompleteParams) -> None:
        print(f"{params.completed}/{params.completed + params.failed} succeeded")
        for err in self._errors:
            print(f"  ERROR: {err}")
        self._errors.clear()

    def on_task_start(self, params: TaskStartParams) -> None:
        pass

    def on_task_complete(self, params: TaskCompleteParams) -> None:
        if params.error:
            tag = f"{params.benchmark}/{params.variant}" if params.variant else params.benchmark
            self._errors.append(f"[{tag}] Task {params.task_id}: {params.error}")

    def debug(self, message: str, *args: object) -> None:
        pass

    def info(self, message: str, *args: object) -> None:
        pass

    def warning(self, message: str, *args: object) -> None:
        pass

    def error(self, message: str, *args: object) -> None:
        formatted = message % args if args else message
        self._log.error(formatted)


def create_benchmark_logger(
    style: str,
    log: logging.Logger | None = None,
) -> BenchmarkLogger:
    """Factory: 'verbose', 'progress', or 'quiet'."""
    if style == "verbose":
        # Ensure the logging module has at least a basic handler so that
        # VerboseLogger's calls to logger.info / .debug / etc. are not
        # silently dropped.  basicConfig is a no-op when handlers already exist.
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(message)s",
            datefmt="%H:%M:%S",
        )
        return VerboseLogger(log)
    if style == "progress":
        return ProgressLogger(log)
    if style == "quiet":
        return QuietLogger(log)
    raise ValueError(f"Unknown logger style: {style!r}")
