"""Task pool executor with continuous batching for async tasks."""

import asyncio
import logging
from typing import (
    Any,
    Callable,
    Coroutine,
    Iterable,
    TypeVar,
)

logger = logging.getLogger(__name__)

T = TypeVar("T")


class TaskPoolExecutor:
    """Executes async tasks with continuous batching.

    Maintains approximately batch_size concurrent tasks at all times by
    starting new tasks as soon as others complete.

    Supports cooperative cancellation via an asyncio.Event. When the event
    is set, the executor stops pulling new tasks and waits for running tasks
    to finish (they should check the same event and return early).

    Example:
        async def process(item: str) -> int:
            return len(item)

        executor = TaskPoolExecutor(batch_size=10)
        results = await executor.run(process(item) for item in items)
    """

    def __init__(
        self,
        batch_size: int = 50,
        on_task_complete: Callable[[Any], None] | None = None,
        on_task_error: Callable[[Exception], None] | None = None,
        task_logger: logging.Logger | None = None,
        quiet_cancel: bool = False,
        cancel_event: asyncio.Event | None = None,
    ):
        """Initialize the executor.

        Args:
            batch_size: Maximum number of concurrent tasks.
            on_task_complete: Optional callback when a task completes successfully.
            on_task_error: Optional callback when a task fails.
            task_logger: Optional logger for task lifecycle events.
            quiet_cancel: If True, suppress cancellation log messages (for nested executors).
            cancel_event: Optional event for cooperative cancellation. When set,
                the executor stops pulling new tasks and waits for running tasks to drain.
        """
        self.batch_size = batch_size
        self._on_task_complete = on_task_complete
        self._on_task_error = on_task_error
        self._logger = task_logger or logger
        self._quiet_cancel = quiet_cancel
        self._cancel_event = cancel_event

    async def run(
        self,
        tasks: Iterable[Coroutine[Any, Any, T]],
    ) -> list[T]:
        """Execute tasks from iterable with continuous batching.

        Args:
            tasks: Iterable of coroutines to execute (generator, list, etc.)

        Returns:
            List of results in completion order (excludes failed tasks).
        """
        results: list[T] = []
        pending: set[asyncio.Task[T]] = set()
        tasks_iter = iter(tasks)
        exhausted = False
        cancelling = False

        try:
            while not exhausted or pending:
                # Check for cooperative cancellation
                if not cancelling and self._cancel_event and self._cancel_event.is_set():
                    cancelling = True
                    exhausted = True
                    if not self._quiet_cancel:
                        self._logger.warning(
                            "Cancel event received, force-cancelling %d running tasks...",
                            len(pending),
                        )
                    # Force-cancel all pending tasks so LLM calls are interrupted
                    for task in pending:
                        task.cancel()
                    # Wait briefly for cleanup, then move on
                    if pending:
                        try:
                            await asyncio.wait_for(
                                asyncio.gather(*pending, return_exceptions=True),
                                timeout=5.0,
                            )
                        except asyncio.TimeoutError:
                            if not self._quiet_cancel:
                                self._logger.warning(
                                    "Cleanup timed out, %d tasks still running",
                                    len(pending),
                                )
                    pending.clear()
                    break

                # Fill pool up to batch_size (skip if cancelling)
                while not cancelling and len(pending) < self.batch_size and not exhausted:
                    try:
                        # Get next unawaited coroutine
                        coro = next(tasks_iter)
                        pending.add(asyncio.create_task(coro))
                    except StopIteration:
                        # Reached end of tasks_iter
                        exhausted = True
                        break

                if not pending:
                    # Nothing to await
                    break

                # Wait for at least one to complete.
                # If we have a cancel_event that hasn't fired yet, include a
                # waiter so we wake up immediately when cancellation is requested.
                cancel_waiter: asyncio.Task | None = None
                if self._cancel_event and not cancelling:
                    cancel_waiter = asyncio.create_task(self._cancel_event.wait())
                    done, pending = await asyncio.wait(
                        pending | {cancel_waiter},
                        return_when=asyncio.FIRST_COMPLETED,
                    )
                    # Clean up cancel_waiter
                    if cancel_waiter in done:
                        done.discard(cancel_waiter)
                        # cancel_event was set — mark as cancelling, loop will handle it
                    else:
                        pending.discard(cancel_waiter)
                        cancel_waiter.cancel()
                        try:
                            await cancel_waiter
                        except asyncio.CancelledError:
                            pass
                    completed = done
                else:
                    completed, pending = await asyncio.wait(
                        pending, return_when=asyncio.FIRST_COMPLETED
                    )

                # Collect results
                for task in completed:
                    try:
                        result = task.result()
                        results.append(result)
                        if self._on_task_complete:
                            self._on_task_complete(result)
                    except asyncio.CancelledError:
                        # Task was cancelled (e.g. by force-cancel fallback)
                        pass
                    except Exception as e:
                        if self._on_task_error:
                            self._on_task_error(e)
                        else:
                            self._logger.exception("Task failed")

        except asyncio.CancelledError:
            if not self._quiet_cancel:
                self._logger.warning(
                    "Executor cancelled, cleaning up %d pending tasks",
                    len(pending),
                )
            # Cancel all pending tasks
            for task in pending:
                task.cancel()
            # Wait briefly for cleanup, but don't block forever
            # LLM calls can take a long time to cancel properly
            try:
                await asyncio.wait_for(
                    asyncio.gather(*pending, return_exceptions=True),
                    timeout=5.0,
                )
            except asyncio.TimeoutError:
                if not self._quiet_cancel:
                    self._logger.warning("Cleanup timed out, %d tasks still running", len(pending))
            raise

        return results
