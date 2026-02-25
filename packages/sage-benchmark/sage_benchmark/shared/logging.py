"""Benchmark logging strategies with multiple output styles."""

import logging
from abc import ABC, abstractmethod

from tqdm import tqdm

logger = logging.getLogger(__name__)


class BenchmarkLogger(ABC):
    """Base class for benchmark logging strategies.

    Provides hooks for tracking progress through benchmark phases.
    Implementations can display progress in different ways (verbose logs,
    progress bars, minimal output, etc.).
    """

    @abstractmethod
    def on_phase_start(self, phase: str, total_items: int) -> None:
        """Called when execution or evaluation phase begins.

        Args:
            phase: Phase name ("execution" or "evaluation")
            total_items: Total number of items to process
        """
        pass

    @abstractmethod
    def on_task_start(self, task_id: int) -> None:
        """Called when a task begins execution.

        Args:
            task_id: The task identifier
        """
        pass

    @abstractmethod
    def on_task_round(self, task_id: int, round_idx: int, max_rounds: int) -> None:
        """Called at the start of each conversation round.

        Args:
            task_id: The task identifier
            round_idx: Zero-based round index
            max_rounds: Maximum rounds allowed
        """
        pass

    @abstractmethod
    def on_task_complete(self, task_id: int, success: bool, error: str | None = None) -> None:
        """Called when a task finishes.

        Args:
            task_id: The task identifier
            success: Whether the task completed successfully
            error: Error message if task failed
        """
        pass

    @abstractmethod
    def on_phase_complete(self, phase: str, completed: int, failed: int) -> None:
        """Called when execution or evaluation phase ends.

        Args:
            phase: Phase name ("execution" or "evaluation")
            completed: Number of successfully completed items
            failed: Number of failed items
        """
        pass

    @abstractmethod
    def log_message(self, level: int, message: str, *args) -> None:
        """Log a general message (for non-progress info).

        Args:
            level: Logging level (e.g., logging.INFO)
            message: Message format string
            *args: Format arguments
        """
        pass

    def __enter__(self):
        """Context manager entry - for progress bar setup."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - for progress bar cleanup."""
        pass


class VerboseLogger(BenchmarkLogger):
    """Verbose logging - outputs every task/round as logger.info().

    This preserves the original behavior of the benchmark runner.
    """

    def __init__(self, log: logging.Logger | None = None):
        self._logger = log or logger

    def on_phase_start(self, phase: str, total_items: int) -> None:
        self._logger.info("Starting %s: %d items", phase, total_items)

    def on_task_start(self, task_id: int) -> None:
        pass  # Verbose logs at round level

    def on_task_round(self, task_id: int, round_idx: int, max_rounds: int) -> None:
        self._logger.info("Task %d - Round %d", task_id, round_idx + 1)

    def on_task_complete(self, task_id: int, success: bool, error: str | None = None) -> None:
        if error:
            self._logger.error("Task %d failed: %s", task_id, error)
        else:
            self._logger.info("Task %d completed", task_id)

    def on_phase_complete(self, phase: str, completed: int, failed: int) -> None:
        self._logger.info("%s complete: %d succeeded, %d failed", phase, completed, failed)

    def log_message(self, level: int, message: str, *args) -> None:
        self._logger.log(level, message, *args)


class ProgressLogger(BenchmarkLogger):
    """Progress bar logging using tqdm.

    Shows a progress bar with task counts and current status.
    Detailed logs are written via tqdm.write() to avoid display corruption.
    """

    def __init__(self, log: logging.Logger | None = None):
        self._logger = log or logger
        self._pbar: tqdm | None = None
        self._phase: str = ""
        self._completed: int = 0
        self._failed: int = 0

    def on_phase_start(self, phase: str, total_items: int) -> None:
        self._phase = phase
        self._completed = 0
        self._failed = 0
        # Close existing bar if any
        if self._pbar:
            self._pbar.close()
        self._pbar = tqdm(
            total=total_items,
            desc=f"{phase.capitalize()}",
            unit="task",
            dynamic_ncols=True,
        )

    def on_task_start(self, task_id: int) -> None:
        if self._pbar:
            self._pbar.set_postfix({"task": task_id}, refresh=True)

    def on_task_round(self, task_id: int, round_idx: int, max_rounds: int) -> None:
        if self._pbar:
            self._pbar.set_postfix(
                {"task": task_id, "round": f"{round_idx + 1}/{max_rounds}"},
                refresh=True,
            )

    def on_task_complete(self, task_id: int, success: bool, error: str | None = None) -> None:
        if success:
            self._completed += 1
        else:
            self._failed += 1

        if self._pbar:
            self._pbar.update(1)

        if error:
            # Write error below progress bar
            tqdm.write(f"Task {task_id} failed: {error}")

    def on_phase_complete(self, phase: str, completed: int, failed: int) -> None:
        if self._pbar:
            self._pbar.close()
            self._pbar = None
        # Summary printed outside progress bar
        print(f"{phase.capitalize()} complete: {completed} succeeded, {failed} failed")

    def log_message(self, level: int, message: str, *args) -> None:
        # Use tqdm.write() to avoid breaking progress bar
        formatted = message % args if args else message
        tqdm.write(formatted)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._pbar:
            self._pbar.close()
            self._pbar = None


class QuietLogger(BenchmarkLogger):
    """Minimal logging - only errors and final summary.

    Useful for CI/CD environments or when running many experiments.
    """

    def __init__(self, log: logging.Logger | None = None):
        self._logger = log or logger
        self._errors: list[str] = []
        self._phase: str = ""

    def on_phase_start(self, phase: str, total_items: int) -> None:
        self._phase = phase
        self._errors.clear()

    def on_task_start(self, task_id: int) -> None:
        pass

    def on_task_round(self, task_id: int, round_idx: int, max_rounds: int) -> None:
        pass

    def on_task_complete(self, task_id: int, success: bool, error: str | None = None) -> None:
        if error:
            self._errors.append(f"Task {task_id}: {error}")

    def on_phase_complete(self, phase: str, completed: int, failed: int) -> None:
        print(f"{phase.capitalize()}: {completed}/{completed + failed} succeeded")
        for err in self._errors:
            print(f"  ERROR: {err}")
        self._errors.clear()

    def log_message(self, level: int, message: str, *args) -> None:
        if level >= logging.ERROR:
            self._logger.log(level, message, *args)


def create_benchmark_logger(
    style: str,
    log: logging.Logger | None = None,
) -> BenchmarkLogger:
    """Factory to create the appropriate logger based on style choice.

    Args:
        style: Logger style - "verbose", "progress", or "quiet"
        log: Optional logger for verbose/quiet modes

    Returns:
        BenchmarkLogger instance

    Raises:
        ValueError: If style is unknown
    """
    if style == "verbose":
        return VerboseLogger(log)
    elif style == "progress":
        return ProgressLogger(log)
    elif style == "quiet":
        return QuietLogger(log)
    else:
        raise ValueError(f"Unknown logger style: {style}")
