"""AIMD concurrency control for rate-limited resources.

Provides per-key (typically per-model) concurrency controllers that
automatically scale concurrency using Additive Increase / Multiplicative
Decrease (AIMD), similar to TCP congestion control.

Providers acquire/release slots around each API call. ``acquire`` blocks
(async) when at capacity, creating natural back-pressure.

Usage from LLM providers::

    from sage_llm.concurrency import acquire, release, on_rate_limit, on_success

    await acquire("gpt-4.1")       # blocks if at capacity
    try:
        response = await call()
        await on_success("gpt-4.1")
    except RateLimitError:
        await on_rate_limit("gpt-4.1", retry_after=2.0)
    finally:
        release("gpt-4.1")        # always release

Usage from TaskPoolExecutor::

    from sage_llm import concurrency

    if concurrency.has_capacity("gpt-4.1", "gpt-5.4"):
        # launch task
"""

from __future__ import annotations

import asyncio
import logging
import time

logger = logging.getLogger(__name__)


class ConcurrencyController:
    """AIMD concurrency controller for a single key.

    - **Multiplicative Decrease**: on rate limit, halve concurrency
    - **Additive Increase**: on success, +1 capped at 2×in_flight
    - **Retry-After**: blocks ``has_capacity`` for a duration
    """

    def __init__(
        self,
        key: str = "",
        initial: int = 64,
        min_concurrency: int = 1,
        max_concurrency: int | None = None,
    ):
        self.key = key
        self.concurrency = initial
        self.min = min_concurrency
        self.max = max_concurrency
        self._in_flight: int = 0
        self._blocked_until: float = 0.0
        self._lock = asyncio.Lock()

    @property
    def is_throttled(self) -> bool:
        if self._blocked_until > 0 and time.monotonic() < self._blocked_until:
            return True
        return self._in_flight >= self.concurrency

    @property
    def has_capacity(self) -> bool:
        if self._blocked_until > 0 and time.monotonic() < self._blocked_until:
            return False
        return self._in_flight < self.concurrency

    async def acquire(self) -> None:
        """Claim a concurrency slot.

        Non-blocking: increments in_flight immediately. The concurrency
        limit is enforced at the executor level (``has_capacity``) to
        prevent new *tasks* from launching, not to block individual API
        calls within already-running tasks (which would deadlock).
        """
        self._in_flight += 1

    def release(self) -> None:
        """Release a concurrency slot."""
        self._in_flight = max(0, self._in_flight - 1)

    async def on_rate_limit(self, retry_after: float | None = None) -> None:
        async with self._lock:
            prev = self.concurrency
            self.concurrency = max(self.min, self.concurrency // 2)
            if retry_after:
                self._blocked_until = time.monotonic() + retry_after
            logger.warning(
                'Rate limit hit: key="%s" concurrency=%d→%d in_flight=%d%s',
                self.key,
                prev,
                self.concurrency,
                self._in_flight,
                f" retry_after={retry_after:.1f}s" if retry_after else "",
            )

    async def on_success(self) -> None:
        async with self._lock:
            prev = self.concurrency
            # +1 but never exceed 2×in_flight (tie growth to actual demand)
            cap = 2 * self._in_flight if self._in_flight > 0 else self.concurrency
            new = self.concurrency + 1
            if self.max is not None:
                new = min(self.max, new)
            new = min(cap, new)
            if new > prev:
                self.concurrency = new
                logger.info(
                    'Concurrency increased: key="%s" concurrency=%d→%d in_flight=%d',
                    self.key,
                    prev,
                    self.concurrency,
                    self._in_flight,
                )

    async def __aenter__(self) -> ConcurrencyController:
        await self.acquire()
        return self

    async def __aexit__(self, *exc: object) -> None:
        self.release()


class _ConcurrencyControllers:
    """Internal singleton: per-key controller registry."""

    def __init__(self, default_initial: int = 64):
        self._controllers: dict[str, ConcurrencyController] = {}
        self._default_initial = default_initial

    def get(self, key: str) -> ConcurrencyController:
        if key not in self._controllers:
            self._controllers[key] = ConcurrencyController(key=key, initial=self._default_initial)
        return self._controllers[key]


_controllers = _ConcurrencyControllers()


# ── Public API ──────────────────────────────────────────────────────


async def on_rate_limit(key: str, retry_after: float | None = None) -> None:
    """Signal that *key* received a rate-limit (429) response."""
    await _controllers.get(key).on_rate_limit(retry_after)


async def on_success(key: str) -> None:
    """Signal a successful API call for *key*."""
    await _controllers.get(key).on_success()


def has_capacity(*keys: str) -> bool:
    """True if ALL keys have capacity. Returns True if no keys given."""
    if not keys:
        return True
    return all(_controllers.get(k).has_capacity for k in keys)


async def acquire(key: str) -> None:
    """Acquire a concurrency slot for *key*. Blocks if at capacity."""
    await _controllers.get(key).acquire()


def release(key: str) -> None:
    """Release a concurrency slot for *key*."""
    _controllers.get(key).release()


def get(key: str) -> ConcurrencyController:
    """Get the controller for *key* (created on first access).

    Supports async context manager usage::

        async with concurrency.get("gpt-4.1"):
            await client.acomplete(...)
    """
    return _controllers.get(key)


class _MultiKeyTracker:
    """Async context manager that acquires/releases multiple keys."""

    __slots__ = ("_controllers",)

    def __init__(self, controllers: list[ConcurrencyController]):
        self._controllers = controllers

    async def __aenter__(self) -> _MultiKeyTracker:
        for c in self._controllers:
            await c.acquire()
        return self

    async def __aexit__(self, *exc: object) -> None:
        for c in self._controllers:
            c.release()


def track(*keys: str) -> _MultiKeyTracker:
    """Async context manager that acquires/releases multiple keys.

    Usage::

        async with concurrency.track("gpt-4.1", "gpt-5.4"):
            ...
    """
    return _MultiKeyTracker([_controllers.get(k) for k in keys])
