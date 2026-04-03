"""Tests for TaskPoolExecutor concurrency-aware scheduling."""

import asyncio

import pytest
from sage_benchmark.shared.executors import TaskPoolExecutor
from sage_llm import concurrency
from sage_llm.concurrency import ConcurrencyController


@pytest.mark.asyncio
async def test_untagged_backward_compat():
    """Untagged coroutines work exactly as before."""

    async def double(x: int) -> int:
        return x * 2

    executor = TaskPoolExecutor(batch_size=5, quiet_cancel=True)
    results = await executor.run(double(i) for i in range(10))
    assert sorted(results) == [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]


@pytest.mark.asyncio
async def test_tagged_tasks_run():
    """Tagged tasks with available capacity run normally."""

    async def double(x: int) -> int:
        return x * 2

    executor = TaskPoolExecutor(batch_size=5, quiet_cancel=True)
    results = await executor.run((double(i), ["test-tagged-run"]) for i in range(10))
    assert sorted(results) == [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]


@pytest.mark.asyncio
async def test_deferred_tasks_launch_when_capacity_frees():
    """Tasks deferred due to throttling launch once capacity returns."""
    key = "test-deferred-launch"
    concurrency._controllers._controllers[key] = ConcurrencyController(initial=1)

    async def track(x: int) -> int:
        await asyncio.sleep(0.01)
        return x

    executor = TaskPoolExecutor(batch_size=10, quiet_cancel=True)
    results = await executor.run((track(i), [key]) for i in range(5))
    assert sorted(results) == [0, 1, 2, 3, 4]


@pytest.mark.asyncio
async def test_mixed_tagged_and_throttled():
    """Tasks with different keys: throttled key defers, available key launches."""
    throttled_key = "test-mixed-throttled"
    available_key = "test-mixed-available"

    # Throttle one key: capacity=1, fill it via a running task
    concurrency._controllers._controllers[throttled_key] = ConcurrencyController(initial=1)
    concurrency._controllers._controllers[available_key] = ConcurrencyController(initial=100)

    async def task_a() -> str:
        return "a"

    async def task_b() -> str:
        return "b"

    executor = TaskPoolExecutor(batch_size=10, quiet_cancel=True)
    results = await executor.run(
        [
            (task_a(), [throttled_key]),
            (task_b(), [available_key]),
        ]
    )
    assert sorted(results) == ["a", "b"]


@pytest.mark.asyncio
async def test_all_deferred_waits_for_capacity():
    """When all tasks are deferred, executor waits and retries."""
    key = "test-all-deferred"
    ctrl = ConcurrencyController(initial=1)
    # Fill to capacity so has_capacity returns False
    await ctrl.acquire()
    concurrency._controllers._controllers[key] = ctrl

    async def release_after_delay():
        await asyncio.sleep(0.3)
        ctrl.release()

    asyncio.create_task(release_after_delay())

    async def work() -> int:
        return 42

    executor = TaskPoolExecutor(batch_size=10, quiet_cancel=True)
    results = await executor.run([(work(), [key])])
    assert results == [42]


@pytest.mark.asyncio
async def test_cancel_cleans_up_deferred():
    """Cancellation cleans up deferred coroutines without warnings."""
    key = "test-cancel-deferred"
    ctrl = ConcurrencyController(initial=1)
    await ctrl.acquire()
    concurrency._controllers._controllers[key] = ctrl

    cancel_event = asyncio.Event()

    async def slow_work() -> int:
        await asyncio.sleep(10)
        return 1

    async def cancel_soon():
        await asyncio.sleep(0.1)
        cancel_event.set()

    asyncio.create_task(cancel_soon())

    executor = TaskPoolExecutor(batch_size=10, quiet_cancel=True, cancel_event=cancel_event)
    results = await executor.run((slow_work(), [key]) for _ in range(5))
    assert isinstance(results, list)
    ctrl.release()
