"""Tests for sage_llm.concurrency — AIMD concurrency control."""

import asyncio

import pytest
from sage_llm.concurrency import (
    ConcurrencyController,
    _ConcurrencyControllers,
    acquire,
    has_capacity,
    on_rate_limit,
    on_success,
    release,
)

# ── ConcurrencyController unit tests ───────────────────────────────


class TestConcurrencyController:
    def test_initial_capacity(self):
        c = ConcurrencyController(initial=4)
        assert c.has_capacity
        assert not c.is_throttled
        assert c.concurrency == 4

    @pytest.mark.asyncio
    async def test_acquire_release_tracks_in_flight(self):
        c = ConcurrencyController(initial=2)
        await c.acquire()
        assert c._in_flight == 1
        assert c.has_capacity
        await c.acquire()
        assert c._in_flight == 2
        assert not c.has_capacity
        assert c.is_throttled
        c.release()
        assert c._in_flight == 1
        assert c.has_capacity

    def test_release_floors_at_zero(self):
        c = ConcurrencyController(initial=2)
        c.release()
        assert c._in_flight == 0

    @pytest.mark.asyncio
    async def test_acquire_does_not_block(self):
        """Acquire is non-blocking to avoid deadlocking multi-round tasks."""
        c = ConcurrencyController(initial=1)
        await c.acquire()  # fills the one slot
        await c.acquire()  # should NOT block, just over-subscribes
        assert c._in_flight == 2
        c.release()
        c.release()

    @pytest.mark.asyncio
    async def test_on_rate_limit_halves_concurrency(self):
        c = ConcurrencyController(initial=16)
        await c.on_rate_limit()
        assert c.concurrency == 8
        await c.on_rate_limit()
        assert c.concurrency == 4

    @pytest.mark.asyncio
    async def test_on_rate_limit_respects_min(self):
        c = ConcurrencyController(initial=2, min_concurrency=1)
        await c.on_rate_limit()
        assert c.concurrency == 1
        await c.on_rate_limit()
        assert c.concurrency == 1

    @pytest.mark.asyncio
    async def test_on_rate_limit_with_retry_after_blocks(self):
        c = ConcurrencyController(initial=8)
        await c.on_rate_limit(retry_after=10.0)
        assert not c.has_capacity
        assert c.is_throttled

    @pytest.mark.asyncio
    async def test_on_success_capped_at_2x_in_flight(self):
        """Concurrency never exceeds 2x current in_flight."""
        c = ConcurrencyController(initial=10)
        # Fill to capacity
        for _ in range(10):
            await c.acquire()
        # in_flight=10, cap=20, 10+1=11 -> 11 (under cap)
        await c.on_success()
        assert c.concurrency == 11
        for _ in range(10):
            c.release()

    @pytest.mark.asyncio
    async def test_on_success_no_increase_when_no_demand(self):
        """With 0 in_flight, concurrency doesn't grow."""
        c = ConcurrencyController(initial=64)
        await c.on_success()
        assert c.concurrency == 64  # cap=2*0=0, no increase

    @pytest.mark.asyncio
    async def test_on_success_respects_max(self):
        c = ConcurrencyController(initial=10, max_concurrency=11)
        for _ in range(10):
            await c.acquire()
        await c.on_success()
        assert c.concurrency == 11  # capped at max
        await c.on_success()
        assert c.concurrency == 11
        for _ in range(10):
            c.release()

    @pytest.mark.asyncio
    async def test_aimd_cycle(self):
        """Full AIMD cycle: rate limit halves, success recovers."""
        c = ConcurrencyController(initial=64)
        for _ in range(64):
            await c.acquire()
        # Hit rate limit: 64 -> 32
        await c.on_rate_limit()
        assert c.concurrency == 32
        # Recover: in_flight=64, cap=128, so +1 works
        await c.on_success()
        assert c.concurrency == 33
        await c.on_success()
        assert c.concurrency == 34
        for _ in range(64):
            c.release()

    @pytest.mark.asyncio
    async def test_async_context_manager(self):
        c = ConcurrencyController(initial=2)
        async with c:
            assert c._in_flight == 1
        assert c._in_flight == 0


# ── _ConcurrencyControllers tests ──────────────────────────────────


class TestConcurrencyControllers:
    def test_get_creates_on_first_access(self):
        cc = _ConcurrencyControllers(default_initial=8)
        c = cc.get("model-a")
        assert c.concurrency == 8

    def test_get_returns_same_controller(self):
        cc = _ConcurrencyControllers()
        c1 = cc.get("model-a")
        c2 = cc.get("model-a")
        assert c1 is c2

    def test_different_keys_different_controllers(self):
        cc = _ConcurrencyControllers()
        c1 = cc.get("model-a")
        c2 = cc.get("model-b")
        assert c1 is not c2


# ── Module-level public API tests ──────────────────────────────────


class TestPublicAPI:
    def test_has_capacity_empty_keys(self):
        assert has_capacity() is True

    @pytest.mark.asyncio
    async def test_on_success_and_has_capacity(self):
        key = "test-public-api-success"
        assert has_capacity(key)
        await on_success(key)
        assert has_capacity(key)

    @pytest.mark.asyncio
    async def test_on_rate_limit_reduces_capacity(self):
        key = "test-public-api-ratelimit"
        await on_rate_limit(key)
        assert has_capacity(key)

    @pytest.mark.asyncio
    async def test_acquire_release(self):
        key = "test-public-api-acquire"
        await acquire(key)
        release(key)
        assert has_capacity(key)

    @pytest.mark.asyncio
    async def test_context_manager_single_key(self):
        from sage_llm.concurrency import get as get_controller

        key = "test-ctx-single"
        ctrl = get_controller(key)
        assert ctrl._in_flight == 0
        async with ctrl:
            assert ctrl._in_flight == 1
        assert ctrl._in_flight == 0

    @pytest.mark.asyncio
    async def test_track_multiple_keys(self):
        from sage_llm.concurrency import get as get_controller
        from sage_llm.concurrency import track

        k1 = "test-track-a"
        k2 = "test-track-b"
        async with track(k1, k2):
            assert get_controller(k1)._in_flight == 1
            assert get_controller(k2)._in_flight == 1
        assert get_controller(k1)._in_flight == 0
        assert get_controller(k2)._in_flight == 0

    @pytest.mark.asyncio
    async def test_track_empty_keys(self):
        from sage_llm.concurrency import track

        async with track():
            pass  # should not raise

    def test_has_capacity_multiple_keys(self):
        k1 = "test-multi-a"
        k2 = "test-multi-b"
        assert has_capacity(k1, k2)

    @pytest.mark.asyncio
    async def test_has_capacity_one_throttled(self):
        k1 = "test-throttle-a"
        k2 = "test-throttle-b"
        from sage_llm import concurrency

        concurrency._controllers._controllers[k1] = ConcurrencyController(initial=1)
        await acquire(k1)
        assert not has_capacity(k1, k2)
        assert has_capacity(k2)
        release(k1)
        assert has_capacity(k1, k2)
