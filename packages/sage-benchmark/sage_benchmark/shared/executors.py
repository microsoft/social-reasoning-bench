"""Task pool executor with continuous batching and concurrency-aware scheduling."""

import asyncio
import logging
from collections import deque
from typing import (
    Any,
    Callable,
    Coroutine,
    Iterable,
    TypeVar,
)

from sage_llm import concurrency

logger = logging.getLogger(__name__)

T = TypeVar("T")

# Sentinel for tasks with no concurrency hints (untagged)
_NO_HINTS: tuple[str, ...] = ()


class TaskPoolExecutor:
    """Executes async tasks with continuous batching and concurrency-aware scheduling.

    Maintains approximately batch_size concurrent tasks at all times by
    starting new tasks as soon as others complete.

    Tasks can be tagged with concurrency hints — keys identifying shared
    resources (typically model names). When a resource is under rate-limit
    pressure, the executor defers tasks that need it and launches tasks
    targeting available resources instead.

    Supports cooperative cancellation via an asyncio.Event. When the event
    is set, the executor stops pulling new tasks and waits for running tasks
    to finish (they should check the same event and return early).

    Example::

        executor = TaskPoolExecutor(batch_size=10)

        # Untagged (backward compatible):
        results = await executor.run(process(item) for item in items)

        # Tagged with concurrency hints:
        results = await executor.run(
            (process(item), ["gpt-4.1"]) for item in items
        )
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
        tasks: Iterable[Coroutine[Any, Any, T] | tuple[Coroutine[Any, Any, T], list[str]]],
    ) -> list[T]:
        """Execute tasks from iterable with continuous batching.

        Args:
            tasks: Iterable of coroutines or ``(coroutine, concurrency_hints)``
                tuples. Hints are lists of keys (e.g. model names) checked
                against :mod:`concurrency` for capacity before launching.

        Returns:
            List of results in completion order (excludes failed tasks).
        """
        results: list[T] = []
        pending: set[asyncio.Task[T]] = set()
        deferred: deque[tuple[Coroutine[Any, Any, T], tuple[str, ...]]] = deque()
        tasks_iter = iter(tasks)
        exhausted = False
        cancelling = False

        try:
            while not exhausted or pending or deferred:
                # Check for cooperative cancellation
                if not cancelling and self._cancel_event and self._cancel_event.is_set():
                    cancelling = True
                    exhausted = True
                    if not self._quiet_cancel:
                        self._logger.warning(
                            "Cancel event received, force-cancelling %d running tasks...",
                            len(pending),
                        )
                    for task in pending:
                        task.cancel()
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
                    # Discard deferred coroutines to avoid "coroutine never awaited"
                    for coro, _ in deferred:
                        coro.close()
                    deferred.clear()
                    break

                # Fill pool: try deferred first, then pull new tasks
                prev_pending = len(pending)

                if not cancelling:
                    exhausted = self._fill_pool(pending, deferred, tasks_iter, exhausted)

                if len(pending) != prev_pending and not self._quiet_cancel:
                    self._logger.info(
                        "Pool: %d tasks in flight, %d deferred (batch_size=%d)",
                        len(pending),
                        len(deferred),
                        self.batch_size,
                    )

                if not pending:
                    if deferred:
                        # All deferred, nothing in flight — wait briefly for
                        # capacity to free up (Retry-After expiry)
                        await asyncio.sleep(0.5)
                        continue
                    break

                # Wait for at least one to complete
                cancel_waiter: asyncio.Task | None = None
                if self._cancel_event and not cancelling:
                    cancel_waiter = asyncio.create_task(self._cancel_event.wait())
                    done, pending = await asyncio.wait(
                        pending | {cancel_waiter},
                        return_when=asyncio.FIRST_COMPLETED,
                    )
                    if cancel_waiter in done:
                        done.discard(cancel_waiter)
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
            for task in pending:
                task.cancel()
            try:
                await asyncio.wait_for(
                    asyncio.gather(*pending, return_exceptions=True),
                    timeout=5.0,
                )
            except asyncio.TimeoutError:
                if not self._quiet_cancel:
                    self._logger.warning("Cleanup timed out, %d tasks still running", len(pending))
            for coro, _ in deferred:
                coro.close()
            deferred.clear()
            raise

        return results

    def _fill_pool(
        self,
        pending: set[asyncio.Task[T]],
        deferred: deque[tuple[Coroutine[Any, Any, T], tuple[str, ...]]],
        tasks_iter: Any,
        exhausted: bool,
    ) -> bool:
        """Fill the pool from deferred queue and iterator. Returns updated exhausted flag."""
        prev_deferred = len(deferred)

        # 1. Try deferred tasks (scan for first launchable)
        for _ in range(len(deferred)):
            if len(pending) >= self.batch_size:
                break
            coro, hints = deferred[0]
            if concurrency.has_capacity(*hints):
                deferred.popleft()
                pending.add(asyncio.create_task(coro))
            else:
                # Rotate: move to back so we try the next one
                deferred.rotate(-1)

        recovered = prev_deferred - len(deferred)
        if recovered and not self._quiet_cancel:
            self._logger.info(
                "Launched %d previously deferred tasks (%d still deferred)",
                recovered,
                len(deferred),
            )

        # 2. Pull new tasks from iterator
        newly_deferred = 0
        while len(pending) < self.batch_size and not exhausted:
            try:
                item = next(tasks_iter)
                coro, hints = self._unpack_item(item)
                if concurrency.has_capacity(*hints):
                    pending.add(asyncio.create_task(coro))
                else:
                    deferred.append((coro, hints))
                    newly_deferred += 1
            except StopIteration:
                exhausted = True
                break

        if newly_deferred and not self._quiet_cancel:
            self._logger.warning(
                "Deferred %d tasks due to rate limiting (%d total deferred)",
                newly_deferred,
                len(deferred),
            )

        return exhausted

    @staticmethod
    def _unpack_item(
        item: Coroutine[Any, Any, T] | tuple[Coroutine[Any, Any, T], list[str]],
    ) -> tuple[Coroutine[Any, Any, T], tuple[str, ...]]:
        """Unpack a task item into (coroutine, hints)."""
        if isinstance(item, tuple):
            coro, hints = item
            return coro, tuple(hints)
        return item, _NO_HINTS
