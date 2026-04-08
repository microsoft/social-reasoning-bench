"""Per-(provider, model) concurrency control with AIMD and task-scoped semaphores.

Three-level concurrency model:

1. **BATCH_SIZE** — max parallel benchmark tasks (managed by TaskPoolExecutor)
2. **TASK_SIZE** — max concurrent LLM calls a single task can make to a given
   provider (ContextVar-scoped semaphore, set via ``task_scope``)
3. **LLM_SIZE** — initial concurrent LLM calls per (provider, model) pair.
   Adjusted automatically by AIMD when errors are hit.

Providers call ``with_llm_retry(provider_key, model, sdk_call)`` which
handles gating, retries, and AIMD feedback.

Configuration
-------------
Programmatic::

    from sage_llm import concurrency

    concurrency.configure(
        llm_size=20,       # initial per-(provider, model) limit (AIMD start)
        task_size=5,        # per-task per-provider limit
        providers={
            "anthropic": {"llm_size": 10},
            "trapi": {"task_size": 3},
        },
    )

Environment variables (read at import time)::

    SAGE_LLM_SIZE=20                  # default global limit
    SAGE_LLM_SIZE_OPENAI=30           # per-provider override
    SAGE_LLM_TASK_SIZE=5              # default per-task limit
    SAGE_LLM_TASK_SIZE_ANTHROPIC=3    # per-provider override
"""

from __future__ import annotations

import asyncio
import logging
import os
import time
from contextlib import AsyncExitStack, asynccontextmanager
from contextvars import ContextVar
from dataclasses import dataclass, field
from typing import AsyncIterator, Awaitable, Callable, TypeVar

logger = logging.getLogger(__name__)

T = TypeVar("T")

# Internal composite key: (provider_key, model)
_CKey = tuple[str, str]


def _display_key(provider_key: str, model: str) -> str:
    return f"{provider_key}/{model}"


# ---------------------------------------------------------------------------
# Resizable semaphore
# ---------------------------------------------------------------------------


class _ResizableSemaphore:
    """Semaphore whose capacity can be changed at runtime."""

    def __init__(self, capacity: int) -> None:
        self._capacity = max(1, capacity)
        self._count = 0
        self._cond = asyncio.Condition()

    @property
    def capacity(self) -> int:
        return self._capacity

    @property
    def available(self) -> bool:
        return self._count < self._capacity

    async def set_capacity(self, n: int) -> None:
        async with self._cond:
            self._capacity = max(0, n)
            if n > 0:
                self._cond.notify_all()

    async def acquire(self) -> None:
        async with self._cond:
            while self._count >= self._capacity:
                await self._cond.wait()
            self._count += 1

    async def release(self) -> None:
        async with self._cond:
            self._count -= 1
            self._cond.notify(1)

    async def __aenter__(self) -> _ResizableSemaphore:
        await self.acquire()
        return self

    async def __aexit__(self, *exc: object) -> None:
        await self.release()


# ---------------------------------------------------------------------------
# AIMD controller
# ---------------------------------------------------------------------------


class _AIMDController:
    """Simple AIMD concurrency controller for a single (provider, model).

    Tracks a rolling window of completions.  Every *n* completions the
    window is evaluated:

    - **Any failure** → multiplicative decrease (halve), lower the ceiling,
      skip stale in-flight completions.
    - **All success** → additive increase (+4, capped at ceiling),
      gated by throughput improvement.
    """

    _MAX_UPPER = 2**16

    def __init__(self, initial: int, key: _CKey = ("", "")) -> None:
        self.semaphore = _ResizableSemaphore(initial)
        self.concurrency = initial
        self.upper = self._MAX_UPPER  # no ceiling until first error
        self._upper_ema: float = 0.0  # EMA of failure concurrency level
        self.n = initial
        self._key = key
        self._window: list[bool] = []
        self._skip: int = 0  # records to ignore after a decrease
        # Throughput-gated increase: snapshot tokens/time at each increase
        self._snapshot_tokens: int = 0
        self._snapshot_time: float = 0.0
        self._prev_tps: float = 0.0

    def record(self, success: bool) -> None:
        if self._skip > 0:
            self._skip -= 1
            return
        self._window.append(success)
        if len(self._window) >= self.n:
            self._evaluate()

    def _current_tps(self) -> float:
        """Compute total tok/s since the last snapshot.

        Returns:
            Tokens per second since the last snapshot, or 0.0 if unavailable.
        """
        dk = _display_key(*self._key)
        m = _metrics.get(dk)
        if m is None:
            return 0.0
        now = time.monotonic()
        dt = now - self._snapshot_time if self._snapshot_time > 0 else 0.0
        if dt <= 0:
            return 0.0
        delta = m.total_tokens - self._snapshot_tokens
        return delta / dt

    def _take_snapshot(self) -> None:
        """Record current tokens/time for next comparison."""
        dk = _display_key(*self._key)
        m = _metrics.get(dk)
        self._snapshot_tokens = m.total_tokens if m else 0
        self._snapshot_time = time.monotonic()

    def _evaluate(self) -> None:
        dk = _display_key(*self._key)
        if any(not s for s in self._window):
            old = self.concurrency
            if self._upper_ema == 0:
                self._upper_ema = float(old)
            else:
                self._upper_ema = 0.3 * old + 0.7 * self._upper_ema
            self.upper = max(1, int(self._upper_ema))
            self.concurrency = old // 2  # can reach 0 (disabled)
            self.n = max(1, 4 * old)
            self._skip = max(1, 4 * old)
            self._prev_tps = 0.0
            self._take_snapshot()
        else:
            current_tps = self._current_tps()
            if self._prev_tps > 0 and current_tps <= self._prev_tps:
                self.n = max(1, self.concurrency)
                if self.concurrency < self.upper:
                    logger.info(
                        "Throughput plateau for %s (%.0f → %.0f tok/s). "
                        "Holding concurrency at %d (upper bound: %d).",
                        dk,
                        self._prev_tps,
                        current_tps,
                        self.concurrency,
                        self.upper,
                    )
                self._prev_tps = current_tps
                self._take_snapshot()
                self._window.clear()
                return
            self._prev_tps = current_tps
            self._take_snapshot()
            self.n = max(1, self.concurrency)
            self.concurrency = min(self.concurrency + 4, self.upper)
        self._window.clear()
        asyncio.ensure_future(self.semaphore.set_capacity(self.concurrency))
        # Window already cleared; detect decrease from skip being set
        if self._skip > 0:
            if self.concurrency == 0:
                logger.warning(
                    "Endpoint %s disabled — repeated errors at minimum concurrency.",
                    dk,
                )
            else:
                logger.warning(
                    "Errors detected for %s. Reducing concurrency %d → %d (upper bound: %d).",
                    dk,
                    self._skip // 4,
                    self.concurrency,
                    self.upper,
                )
        else:
            logger.info(
                "Increasing concurrency for %s → %d (upper bound: %d, tps: %.0f).",
                dk,
                self.concurrency,
                self.upper,
                self.n,
                self._prev_tps,
            )


# ---------------------------------------------------------------------------
# Internal state
# ---------------------------------------------------------------------------

KNOWN_PROVIDERS = ("openai", "anthropic", "google", "azure", "trapi", "phyagi")


@dataclass
class _ProviderLimits:
    """Per-provider concurrency limits."""

    llm_size: int | None = None
    task_size: int | None = None


@dataclass
class _Config:
    """Module-level concurrency configuration."""

    default_llm_size: int | None = None
    default_task_size: int | None = None
    provider_overrides: dict[str, _ProviderLimits] = field(default_factory=dict)

    def llm_size_for(self, provider_key: str) -> int | None:
        override = self.provider_overrides.get(provider_key)
        if override and override.llm_size is not None:
            return override.llm_size
        return self.default_llm_size

    def task_size_for(self, provider_key: str) -> int | None:
        override = self.provider_overrides.get(provider_key)
        if override and override.task_size is not None:
            return override.task_size
        return self.default_task_size


_config = _Config()

_aimd_controllers: dict[_CKey, _AIMDController | None] = {}


def _get_controller(provider_key: str, model: str) -> _AIMDController | None:
    """Return (or lazily create) the AIMD controller for *(provider_key, model)*.

    Args:
        provider_key: Provider identifier (e.g. ``"openai"``).
        model: Model name within the provider.

    Returns:
        The AIMD controller for the pair, or ``None`` if no LLM size is configured.
    """
    key: _CKey = (provider_key, model)
    if key not in _aimd_controllers:
        size = _config.llm_size_for(provider_key)
        _aimd_controllers[key] = _AIMDController(size, key=key) if size else None
    return _aimd_controllers[key]


# ---------------------------------------------------------------------------
# Per-task state (ContextVar)  — keyed by provider only (not model)
# ---------------------------------------------------------------------------


class _TaskState:
    """Holds lazily-created per-task semaphores keyed by provider."""

    def __init__(self, task_size_override: int | None = None) -> None:
        self._semaphores: dict[str, asyncio.Semaphore | None] = {}
        self._task_size_override = task_size_override

    def get_semaphore(self, provider_key: str) -> asyncio.Semaphore | None:
        if provider_key not in self._semaphores:
            size = self._resolve_task_size(provider_key)
            self._semaphores[provider_key] = asyncio.Semaphore(size) if size else None
        return self._semaphores[provider_key]

    def _resolve_task_size(self, provider_key: str) -> int | None:
        override = _config.provider_overrides.get(provider_key)
        if override and override.task_size is not None:
            return override.task_size
        if self._task_size_override is not None:
            return self._task_size_override
        return _config.default_task_size


_task_state: ContextVar[_TaskState | None] = ContextVar("_task_state", default=None)

# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def configure(
    *,
    llm_size: int | None = None,
    task_size: int | None = None,
    providers: dict[str, dict[str, int]] | None = None,
) -> None:
    """Set concurrency limits.

    Args:
        llm_size: Initial max concurrent LLM calls per (provider, model).
            AIMD adjusts this at runtime.
        task_size: Default max concurrent LLM calls per task per provider.
        providers: Per-provider overrides, e.g.
            ``{"anthropic": {"llm_size": 10, "task_size": 3}}``.
    """
    _config.default_llm_size = llm_size
    _config.default_task_size = task_size
    _config.provider_overrides.clear()
    _aimd_controllers.clear()

    if providers:
        for key, limits in providers.items():
            _config.provider_overrides[key] = _ProviderLimits(
                llm_size=limits.get("llm_size"),
                task_size=limits.get("task_size"),
            )


@asynccontextmanager
async def task_scope(task_size: int | None = None) -> AsyncIterator[None]:
    """Create per-task semaphores scoped to this async context.

    Args:
        task_size: Optional override for the per-task concurrency limit.
    """
    state = _TaskState(task_size_override=task_size)
    token = _task_state.set(state)
    try:
        yield
    finally:
        _task_state.reset(token)


@asynccontextmanager
async def llm_gate(provider_key: str, model: str) -> AsyncIterator[None]:
    """Acquire per-task and per-(provider, model) semaphores.

    Acquisition order: task semaphore first, then global semaphore.

    Args:
        provider_key: Provider identifier (e.g. ``"openai"``).
        model: Model name within the provider.
    """
    state = _task_state.get(None)
    task_sem = state.get_semaphore(provider_key) if state else None
    controller = _get_controller(provider_key, model)
    global_sem = controller.semaphore if controller else None
    dk = _display_key(provider_key, model)

    _failed = False
    try:
        async with AsyncExitStack() as stack:
            if task_sem is not None:
                await stack.enter_async_context(task_sem)
            if global_sem is not None:
                await stack.enter_async_context(global_sem)
            _in_flight[dk] = _in_flight.get(dk, 0) + 1
            _update_in_flight_ema(dk)
            try:
                yield
            except Exception:
                _failed = True
                raise
            finally:
                _in_flight[dk] -= 1
                _update_in_flight_ema(dk)
    finally:
        # Record AIMD after semaphore release
        if controller:
            controller.record(not _failed)


@asynccontextmanager
async def pool_in_flight(provider_key: str, model: str, deployment: str) -> AsyncIterator[None]:
    """Track aggregate in-flight count for a pool of deployments.

    Call inside ``llm_gate`` to maintain a pool-level ``in_flight_ema``
    alongside the per-deployment tracking that ``llm_gate`` already does.

    Also registers the deployment as a pool member so that
    ``_periodic_metrics_log`` can aggregate AIMD concurrency.

    Args:
        provider_key: Provider identifier (e.g. ``"azure_pool"``).
        model: Logical model name (e.g. ``"gpt-4.1"``).
        deployment: Deployment name used as the ``model`` arg to ``llm_gate``.
    """
    pool_dk = _display_key(provider_key, model)
    deploy_dk = _display_key(provider_key, deployment)
    _pool_members.setdefault(pool_dk, set()).add(deploy_dk)
    _in_flight[pool_dk] = _in_flight.get(pool_dk, 0) + 1
    _update_in_flight_ema(pool_dk)
    try:
        yield
    finally:
        _in_flight[pool_dk] -= 1
        _update_in_flight_ema(pool_dk)


# ---------------------------------------------------------------------------
# Retry with AIMD feedback
# ---------------------------------------------------------------------------


def is_rate_limit(exc: Exception) -> bool:
    status = getattr(exc, "status_code", None) or getattr(exc, "code", None)
    return status == 429


def is_fatal(exc: Exception) -> bool:
    """Non-retryable client errors (4xx except 429).

    Args:
        exc: The exception to inspect.

    Returns:
        True if the exception represents a non-retryable 4xx error.
    """
    status = getattr(exc, "status_code", None) or getattr(exc, "code", None)
    if status is None:
        return False
    return 400 <= status < 500 and status != 429


def parse_retry_after(exc: Exception) -> float | None:
    resp = getattr(exc, "response", None)
    if resp is None:
        return None
    headers = getattr(resp, "headers", {})
    raw = headers.get("retry-after") or headers.get("Retry-After")
    if raw is None:
        return None
    try:
        return float(raw)
    except (ValueError, TypeError):
        return None


async def with_llm_retry(
    provider_key: str,
    model: str,
    sdk_call: Callable[..., Awaitable[T]],
    *,
    max_retries: int = 5,
    gate: Callable[..., AsyncIterator[Any]] | None = None,
) -> tuple[T, float]:
    """Acquire gate, call *sdk_call*, retry on transient errors.

    The *gate* is an async context manager ``(provider_key, model) → ctx``.
    Its yielded value is passed to *sdk_call(ctx)*.  Default is
    :func:`llm_gate` (yields ``None``).  AIMD recording lives in
    ``llm_gate``, not here — this is a pure retry loop.

    Fatal errors (4xx except 429) raise immediately.  Transient errors
    (429, 5xx, timeouts, connection errors) trigger retry with backoff.

    Args:
        provider_key: Provider identifier (e.g. ``"openai"``).
        model: Model name within the provider.
        sdk_call: Async callable to invoke; receives the gate's yielded context.
        max_retries: Maximum number of retry attempts.
        gate: Async context-manager factory for concurrency gating.

    Returns:
        A ``(result, call_duration_seconds)`` tuple.
    """
    if gate is None:
        gate = llm_gate
    dk = _display_key(provider_key, model)
    last_exc: Exception | None = None
    for attempt in range(max_retries + 1):
        try:
            async with gate(provider_key, model) as ctx:
                t0 = time.monotonic()
                result = await sdk_call(ctx)
                duration = time.monotonic() - t0
            return result, duration
        except Exception as exc:
            if is_fatal(exc):
                raise
            last_exc = exc
            if is_rate_limit(exc):
                wait = parse_retry_after(exc) or 1.0
            else:
                wait = 5.0
            logger.info(
                "%s: %s (attempt %d/%d), retry after %.1fs",
                dk,
                type(exc).__name__,
                attempt + 1,
                max_retries + 1,
                wait,
            )
            if attempt < max_retries:
                await asyncio.sleep(wait)

    assert last_exc is not None  # unreachable if max_retries >= 0
    raise last_exc


def reset() -> None:
    """Reset all configuration and state.  Intended for tests."""
    global _metrics_task  # noqa: PLW0603
    _config.default_llm_size = None
    _config.default_task_size = None
    _config.provider_overrides.clear()
    _aimd_controllers.clear()
    _metrics.clear()
    _in_flight.clear()
    _pool_members.clear()
    if _metrics_task is not None:
        _metrics_task.cancel()
        _metrics_task = None


# ---------------------------------------------------------------------------
# Per-(provider, model) usage metrics
# ---------------------------------------------------------------------------


@dataclass
class _DecayingRate:
    """EMA-based rate tracker with time-weighted decay."""

    halflife: float
    _rate: float = 0.0
    _last_time: float = 0.0

    def record(self, tokens: int) -> None:
        now = time.monotonic()
        if self._last_time == 0.0:
            self._last_time = now
            return
        dt = now - self._last_time
        if dt <= 0:
            return
        self._last_time = now
        instant = tokens / dt
        alpha = 1.0 - 2.0 ** (-dt / self.halflife)
        self._rate = alpha * instant + (1.0 - alpha) * self._rate

    @property
    def rate(self) -> float:
        return self._rate


@dataclass
class _DecayingAvg:
    """EMA of a scalar value with time-weighted decay."""

    halflife: float
    _value: float = 0.0
    _last_time: float = 0.0

    def record(self, value: float) -> None:
        now = time.monotonic()
        if self._last_time == 0.0:
            self._value = value
            self._last_time = now
            return
        dt = now - self._last_time
        if dt <= 0:
            return
        self._last_time = now
        alpha = 1.0 - 2.0 ** (-dt / self.halflife)
        self._value = alpha * value + (1.0 - alpha) * self._value

    @property
    def value(self) -> float:
        return self._value


@dataclass
class ProviderMetrics:
    """Accumulated token and timing metrics for a (provider, model) pair."""

    call_count: int = 0
    prompt_tokens: int = 0
    completion_tokens: int = 0
    cached_tokens: int = 0
    reasoning_tokens: int = 0
    call_seconds: float = 0.0
    first_call_time: float | None = None
    in_flight_ema: float = 0.0
    output_tps_1m: _DecayingRate = field(default_factory=lambda: _DecayingRate(halflife=60.0))
    output_tps_5m: _DecayingRate = field(default_factory=lambda: _DecayingRate(halflife=300.0))
    total_tps_1m: _DecayingRate = field(default_factory=lambda: _DecayingRate(halflife=60.0))
    total_tps_5m: _DecayingRate = field(default_factory=lambda: _DecayingRate(halflife=300.0))
    call_dur_1m: _DecayingAvg = field(default_factory=lambda: _DecayingAvg(halflife=60.0))
    call_dur_5m: _DecayingAvg = field(default_factory=lambda: _DecayingAvg(halflife=300.0))

    @property
    def total_tokens(self) -> int:
        return self.prompt_tokens + self.completion_tokens


# Keyed by display string "provider/model"
_metrics: dict[str, ProviderMetrics] = {}

_IN_FLIGHT_ALPHA = 0.1

_in_flight: dict[str, int] = {}

# Maps pool-level display key → set of member deployment display keys.
# Populated by pool_in_flight(); used by _periodic_metrics_log() to
# aggregate AIMD concurrency across pool deployments.
_pool_members: dict[str, set[str]] = {}

# ── Per-label token tracking via contextvars ─────────────────────────────

#: Set this contextvar to tag LLM calls with a prompt label
#: (e.g., "interviewer", "assistant", "privacy_judge").
#: record_usage() reads it to accumulate per-label token counts.
prompt_label: ContextVar[str] = ContextVar("prompt_label", default="unknown")


@dataclass
class LabelMetrics:
    """Lightweight per-label token counters."""

    call_count: int = 0
    prompt_tokens: int = 0
    completion_tokens: int = 0

    @property
    def total_tokens(self) -> int:
        return self.prompt_tokens + self.completion_tokens


# Keyed by (display_key, label)
_label_metrics: dict[tuple[str, str], LabelMetrics] = {}


def _update_in_flight_ema(dk: str) -> None:
    """Update the in-flight EMA for display key *dk*.

    Args:
        dk: Display key in ``"provider/model"`` format.
    """
    current = _in_flight.get(dk, 0)
    if dk not in _metrics:
        _metrics[dk] = ProviderMetrics()
    m = _metrics[dk]
    m.in_flight_ema = _IN_FLIGHT_ALPHA * current + (1 - _IN_FLIGHT_ALPHA) * m.in_flight_ema


def record_usage(
    provider_key: str,
    model: str,
    prompt_tokens: int,
    completion_tokens: int,
    call_duration: float,
    cached_tokens: int = 0,
    reasoning_tokens: int = 0,
) -> None:
    """Record token usage and call duration for a (provider, model) pair.

    Args:
        provider_key: Provider identifier (e.g. ``"openai"``).
        model: Model name within the provider.
        prompt_tokens: Number of prompt tokens consumed.
        completion_tokens: Number of completion tokens generated.
        call_duration: Wall-clock duration of the call in seconds.
        cached_tokens: Number of tokens served from cache.
        reasoning_tokens: Number of reasoning/chain-of-thought tokens.
    """
    _ensure_metrics_logging()
    dk = _display_key(provider_key, model)
    if dk not in _metrics:
        _metrics[dk] = ProviderMetrics()
    m = _metrics[dk]
    if m.first_call_time is None:
        m.first_call_time = time.monotonic()
    m.call_count += 1
    m.prompt_tokens += prompt_tokens
    m.completion_tokens += completion_tokens
    m.cached_tokens += cached_tokens
    m.reasoning_tokens += reasoning_tokens
    m.call_seconds += call_duration
    total = prompt_tokens + completion_tokens
    m.output_tps_1m.record(completion_tokens)
    m.output_tps_5m.record(completion_tokens)
    m.total_tps_1m.record(total)
    m.total_tps_5m.record(total)
    m.call_dur_1m.record(call_duration)
    m.call_dur_5m.record(call_duration)

    # Per-label tracking
    label = prompt_label.get()
    lk = (dk, label)
    if lk not in _label_metrics:
        _label_metrics[lk] = LabelMetrics()
    lm = _label_metrics[lk]
    lm.call_count += 1
    lm.prompt_tokens += prompt_tokens
    lm.completion_tokens += completion_tokens


def get_metrics() -> dict[str, ProviderMetrics]:
    """Return accumulated metrics keyed by ``"provider/model"``.

    Returns:
        A dict mapping ``"provider/model"`` strings to their ``ProviderMetrics``.
    """
    return dict(_metrics)


def get_label_metrics() -> dict[str, dict[str, LabelMetrics]]:
    """Return per-label token breakdown, keyed by provider then label.

    Returns:
        ``{"provider/model": {"label": LabelMetrics, ...}, ...}``
    """
    result: dict[str, dict[str, LabelMetrics]] = {}
    for (dk, label), lm in _label_metrics.items():
        if dk not in result:
            result[dk] = {}
        result[dk][label] = lm
    return result


def has_capacity(provider_key: str, model: str) -> bool:
    """Return True if the AIMD semaphore for *(provider_key, model)* has room.

    Args:
        provider_key: Provider identifier (e.g. ``"openai"``).
        model: Model name within the provider.

    Returns:
        True if the AIMD semaphore has available capacity (or no limit is set).
    """
    controller = _get_controller(provider_key, model)
    if controller is None:
        return True
    return controller.semaphore.available


def get_aimd_state() -> dict[str, tuple[int, int]]:
    """Return AIMD state: ``{"provider/model": (concurrency, upper)}``.

    Returns:
        A dict mapping ``"provider/model"`` to ``(concurrency, upper)`` tuples.
    """
    return {
        _display_key(*key): (ctrl.concurrency, ctrl.upper)
        for key, ctrl in _aimd_controllers.items()
        if ctrl is not None
    }


# ---------------------------------------------------------------------------
# Periodic metrics logging (auto-starts on first record_usage)
# ---------------------------------------------------------------------------

_METRICS_INTERVAL = float(os.environ.get("SAGE_METRICS_INTERVAL", "120"))
_metrics_task: asyncio.Task | None = None


async def _periodic_metrics_log(interval: float) -> None:
    """Background task that logs provider throughput metrics periodically.

    Args:
        interval: Seconds between each metrics log emission.
    """
    while True:
        await asyncio.sleep(interval)
        try:
            metrics = get_metrics()
            if not metrics:
                continue
            now = time.monotonic()
            aimd_state = get_aimd_state()
            label_metrics_all = get_label_metrics()
            for key, m in sorted(metrics.items()):
                if m.call_count == 0:
                    continue
                bench_elapsed = (now - m.first_call_time) if m.first_call_time is not None else 0.0
                out_tps = m.completion_tokens / bench_elapsed if bench_elapsed > 0 else 0.0
                tot_tps = m.total_tokens / bench_elapsed if bench_elapsed > 0 else 0.0
                aimd = aimd_state.get(key)
                # Aggregate AIMD across pool member deployments
                if aimd is None and key in _pool_members:
                    agg_c = agg_u = 0
                    for member in _pool_members[key]:
                        if member in aimd_state:
                            c, u = aimd_state[member]
                            agg_c += c
                            agg_u += u
                    if agg_c or agg_u:
                        aimd = (agg_c, agg_u)
                mins, secs = divmod(m.call_seconds, 60)
                avg_dur = m.call_seconds / m.call_count if m.call_count else 0.0
                parallelism = m.call_seconds / bench_elapsed if bench_elapsed > 0 else 0.0
                label_metrics = label_metrics_all.get(key, {})
                label_lines = ""
                if label_metrics:
                    parts = []
                    for label, lm in sorted(label_metrics.items()):
                        parts.append(
                            f"    {label}: {lm.call_count:,} calls, {lm.total_tokens:,} tokens"
                        )
                    label_lines = "\n" + "\n".join(parts)

                logger.warning(
                    "Throughput %s:\n"
                    "  output tok/s : %7s  [1m: %7s  5m: %7s]\n"
                    "  total tok/s  : %7s  [1m: %7s  5m: %7s]\n"
                    "  avg call     : %5.1fs  [1m: %5.1fs  5m: %5.1fs]\n"
                    "  in_flight    : %5.1f\n"
                    "  concurrency  : %s\n"
                    "  parallelism  : %.1fx\n"
                    "  total tokens : %s\n"
                    "  input tokens : %s (%s cached)\n"
                    "  output tokens: %s (%s reasoning)\n"
                    "  calls        : %s  (%dm%04.1fs self-time)%s",
                    key,
                    f"{out_tps:,.0f}",
                    f"{m.output_tps_1m.rate:,.0f}",
                    f"{m.output_tps_5m.rate:,.0f}",
                    f"{tot_tps:,.0f}",
                    f"{m.total_tps_1m.rate:,.0f}",
                    f"{m.total_tps_5m.rate:,.0f}",
                    avg_dur,
                    m.call_dur_1m.value,
                    m.call_dur_5m.value,
                    m.in_flight_ema,
                    f"{aimd[0]}/{aimd[1]}" if aimd else "off",
                    parallelism,
                    f"{m.total_tokens:,}",
                    f"{m.prompt_tokens:,}",
                    f"{m.cached_tokens:,}",
                    f"{m.completion_tokens:,}",
                    f"{m.reasoning_tokens:,}",
                    f"{m.call_count:,}",
                    int(mins),
                    secs,
                    label_lines,
                )
        except Exception:
            logger.exception("Periodic metrics log failed")


def _ensure_metrics_logging() -> None:
    """Start the periodic metrics log task if not already running."""
    global _metrics_task  # noqa: PLW0603
    if _metrics_task is not None or _METRICS_INTERVAL <= 0:
        return
    try:
        loop = asyncio.get_running_loop()
        _metrics_task = loop.create_task(_periodic_metrics_log(_METRICS_INTERVAL))
    except RuntimeError:
        pass  # no running event loop


# ---------------------------------------------------------------------------
# Load from environment at import time
# ---------------------------------------------------------------------------


def _load_env() -> None:
    """Read concurrency settings from environment variables."""
    llm_str = os.environ.get("SAGE_LLM_SIZE")
    if llm_str:
        _config.default_llm_size = int(llm_str)

    task_str = os.environ.get("SAGE_LLM_TASK_SIZE")
    if task_str:
        _config.default_task_size = int(task_str)

    for env_key in KNOWN_PROVIDERS:
        provider_key = env_key.lower()
        llm = os.environ.get(f"SAGE_LLM_SIZE_{env_key.upper()}")
        task = os.environ.get(f"SAGE_LLM_TASK_SIZE_{env_key.upper()}")
        if llm or task:
            _config.provider_overrides[provider_key] = _ProviderLimits(
                llm_size=int(llm) if llm else None,
                task_size=int(task) if task else None,
            )


_load_env()
