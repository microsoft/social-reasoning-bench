"""Tests for sage_llm.concurrency — per-provider, per-task semaphore gating."""

import asyncio

import pytest
from sage_llm.concurrency import (
    MODEL_PRICING,
    _AIMDController,
    _config,
    _estimate_cost,
    _get_controller,
    _pool_members,
    _ResizableSemaphore,
    _task_state,
    configure,
    get_metrics,
    llm_gate,
    pool_in_flight,
    record_usage,
    reset,
    task_scope,
    with_llm_retry,
)


def _cap_upper(provider: str = "openai", model: str = "m") -> None:
    """Cap AIMD upper to prevent growth on a specific (provider, model).

    Args:
        provider: Provider identifier.
        model: Model name within the provider.
    """
    ctrl = _get_controller(provider, model)
    if ctrl:
        ctrl.upper = ctrl.concurrency


def _configure_fixed(llm_size: int, task_size: int | None = None) -> None:
    """Configure with a fixed concurrency (AIMD won't grow past initial).

    Call this, then use ``_cap_upper(provider, model)`` for each
    (provider, model) pair that needs a fixed limit.

    Args:
        llm_size: Initial per-(provider, model) concurrency limit.
        task_size: Optional per-task per-provider concurrency limit.
    """
    configure(llm_size=llm_size, task_size=task_size)


@pytest.fixture(autouse=True)
def _reset_concurrency():
    """Ensure every test starts with a clean concurrency state."""
    reset()
    yield
    reset()


# ---------------------------------------------------------------------------
# llm_gate with no configuration (passthrough)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_llm_gate_no_config():
    """llm_gate should pass through when nothing is configured."""
    entered = False
    async with llm_gate("openai", "m"):
        entered = True
    assert entered


# ---------------------------------------------------------------------------
# llm_gate with global semaphore only
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_llm_gate_global_only():
    """Global semaphore limits total concurrent calls for a provider."""
    _configure_fixed(llm_size=2)
    _cap_upper()

    active = 0
    max_active = 0

    async def call():
        nonlocal active, max_active
        async with llm_gate("openai", "m"):
            active += 1
            max_active = max(max_active, active)
            await asyncio.sleep(0.05)
            active -= 1

    await asyncio.gather(*[call() for _ in range(6)])
    assert max_active <= 2


# ---------------------------------------------------------------------------
# llm_gate with task semaphore only
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_llm_gate_task_only():
    """Task semaphore limits concurrent calls within a single task scope."""
    configure(task_size=2)

    active = 0
    max_active = 0

    async def call():
        nonlocal active, max_active
        async with llm_gate("openai", "m"):
            active += 1
            max_active = max(max_active, active)
            await asyncio.sleep(0.05)
            active -= 1

    async with task_scope():
        await asyncio.gather(*[call() for _ in range(6)])

    assert max_active <= 2


# ---------------------------------------------------------------------------
# llm_gate with both semaphores
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_llm_gate_both():
    """Both task and global semaphores should be enforced."""
    # Global allows 4, task allows 2 → effective limit is 2 per task
    _configure_fixed(llm_size=4, task_size=2)
    _cap_upper()

    active = 0
    max_active = 0

    async def call():
        nonlocal active, max_active
        async with llm_gate("openai", "m"):
            active += 1
            max_active = max(max_active, active)
            await asyncio.sleep(0.05)
            active -= 1

    async with task_scope():
        await asyncio.gather(*[call() for _ in range(6)])

    assert max_active <= 2


@pytest.mark.asyncio
async def test_global_limits_across_tasks():
    """Global semaphore limits total calls across multiple task scopes."""
    _configure_fixed(llm_size=3, task_size=10)  # task allows 10, global caps at 3
    _cap_upper()

    active = 0
    max_active = 0

    async def task_work():
        nonlocal active, max_active
        async with task_scope():
            calls = []
            for _ in range(4):

                async def call():
                    nonlocal active, max_active
                    async with llm_gate("openai", "m"):
                        active += 1
                        max_active = max(max_active, active)
                        await asyncio.sleep(0.05)
                        active -= 1

                calls.append(call())
            await asyncio.gather(*calls)

    await asyncio.gather(*[task_work() for _ in range(3)])
    assert max_active <= 3


# ---------------------------------------------------------------------------
# Task isolation
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_task_isolation():
    """Two task scopes should have independent per-task semaphores."""
    configure(task_size=1)

    active_per_task: dict[str, int] = {"a": 0, "b": 0}
    max_per_task: dict[str, int] = {"a": 0, "b": 0}

    async def task_work(task_id: str):
        async with task_scope():

            async def call():
                async with llm_gate("openai", "m"):
                    active_per_task[task_id] += 1
                    max_per_task[task_id] = max(max_per_task[task_id], active_per_task[task_id])
                    await asyncio.sleep(0.05)
                    active_per_task[task_id] -= 1

            await asyncio.gather(*[call() for _ in range(4)])

    await asyncio.gather(task_work("a"), task_work("b"))
    assert max_per_task["a"] <= 1
    assert max_per_task["b"] <= 1


# ---------------------------------------------------------------------------
# Provider isolation
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_provider_isolation():
    """Different providers should have independent global semaphores."""
    _configure_fixed(llm_size=1)
    _cap_upper("openai")
    _cap_upper("anthropic")

    active = {"openai": 0, "anthropic": 0}
    max_active = {"openai": 0, "anthropic": 0}

    async def call(provider: str):
        async with llm_gate(provider, "m"):
            active[provider] += 1
            max_active[provider] = max(max_active[provider], active[provider])
            await asyncio.sleep(0.05)
            active[provider] -= 1

    # Both providers can have 1 concurrent call each (2 total)
    await asyncio.gather(
        *[call("openai") for _ in range(3)],
        *[call("anthropic") for _ in range(3)],
    )

    assert max_active["openai"] <= 1
    assert max_active["anthropic"] <= 1


@pytest.mark.asyncio
async def test_provider_override():
    """Per-provider overrides should take precedence over defaults."""
    configure(llm_size=5, providers={"anthropic": {"llm_size": 1}})
    _cap_upper("anthropic")

    active = 0
    max_active = 0

    async def call():
        nonlocal active, max_active
        async with llm_gate("anthropic", "m"):
            active += 1
            max_active = max(max_active, active)
            await asyncio.sleep(0.05)
            active -= 1

    await asyncio.gather(*[call() for _ in range(5)])
    assert max_active <= 1


# ---------------------------------------------------------------------------
# configure() and reset()
# ---------------------------------------------------------------------------


def test_configure_sets_defaults():
    configure(llm_size=10, task_size=3)
    assert _config.default_llm_size == 10
    assert _config.default_task_size == 3


def test_configure_sets_overrides():
    configure(
        llm_size=10,
        providers={"azure": {"llm_size": 5, "task_size": 2}},
    )
    assert _config.llm_size_for("azure") == 5
    assert _config.task_size_for("azure") == 2
    # Default applies to other providers
    assert _config.llm_size_for("openai") == 10
    assert _config.task_size_for("openai") is None


def test_configure_clears_previous():
    configure(llm_size=10)
    configure(llm_size=5)
    assert _config.default_llm_size == 5


def test_reset_clears_everything():
    configure(llm_size=10, task_size=3, providers={"openai": {"llm_size": 1}})
    reset()
    assert _config.default_llm_size is None
    assert _config.default_task_size is None
    assert len(_config.provider_overrides) == 0


# ---------------------------------------------------------------------------
# task_scope with explicit override
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_task_scope_override():
    """task_scope(task_size=N) overrides default task_size."""
    configure(task_size=10)  # default is generous

    active = 0
    max_active = 0

    async def call():
        nonlocal active, max_active
        async with llm_gate("openai", "m"):
            active += 1
            max_active = max(max_active, active)
            await asyncio.sleep(0.05)
            active -= 1

    async with task_scope(task_size=1):
        await asyncio.gather(*[call() for _ in range(4)])

    assert max_active <= 1


@pytest.mark.asyncio
async def test_task_scope_provider_override_wins():
    """Per-provider task_size from configure() beats task_scope override."""
    configure(providers={"openai": {"task_size": 1}})

    active = 0
    max_active = 0

    async def call():
        nonlocal active, max_active
        async with llm_gate("openai", "m"):
            active += 1
            max_active = max(max_active, active)
            await asyncio.sleep(0.05)
            active -= 1

    async with task_scope(task_size=10):  # would allow 10, but override says 1
        await asyncio.gather(*[call() for _ in range(4)])

    assert max_active <= 1


# ---------------------------------------------------------------------------
# llm_gate outside task_scope (no task semaphore)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_llm_gate_outside_task_scope():
    """llm_gate works without task_scope — only global sem applies."""
    configure(llm_size=2, task_size=1)
    _cap_upper()

    active = 0
    max_active = 0

    async def call():
        nonlocal active, max_active
        async with llm_gate("openai", "m"):
            active += 1
            max_active = max(max_active, active)
            await asyncio.sleep(0.05)
            active -= 1

    # No task_scope → no task semaphore, only global
    await asyncio.gather(*[call() for _ in range(5)])
    assert max_active <= 2


# ---------------------------------------------------------------------------
# Nested task_scope
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_nested_task_scope():
    """Inner task_scope should create a fresh set of task semaphores."""
    configure(task_size=5)

    active = 0
    max_active = 0

    async def call():
        nonlocal active, max_active
        async with llm_gate("openai", "m"):
            active += 1
            max_active = max(max_active, active)
            await asyncio.sleep(0.05)
            active -= 1

    async with task_scope():
        # Inner scope with tighter limit
        async with task_scope(task_size=1):
            await asyncio.gather(*[call() for _ in range(4)])

    assert max_active <= 1


# ---------------------------------------------------------------------------
# Usage metrics
# ---------------------------------------------------------------------------


def test_metrics_accumulate():
    """record_usage should accumulate totals for a provider."""
    record_usage("openai", "m", 100, 50, 1.0)
    record_usage("openai", "m", 200, 80, 0.5)

    metrics = get_metrics()
    assert "openai/m" in metrics
    m = metrics["openai/m"]
    assert m.call_count == 2
    assert m.prompt_tokens == 300
    assert m.completion_tokens == 130
    assert m.total_tokens == 430
    assert m.call_seconds == pytest.approx(1.5)
    assert m.first_call_time is not None


def test_metrics_per_provider():
    """Different providers should accumulate independently."""
    record_usage("openai", "m", 100, 50, 1.0)
    record_usage("anthropic", "m", 200, 80, 0.5)

    metrics = get_metrics()
    assert metrics["openai/m"].prompt_tokens == 100
    assert metrics["anthropic/m"].prompt_tokens == 200
    assert metrics["openai/m"].call_count == 1
    assert metrics["anthropic/m"].call_count == 1


def test_metrics_reset():
    """reset() should clear accumulated metrics."""
    record_usage("openai", "m", 100, 50, 1.0)
    assert len(get_metrics()) == 1

    reset()
    assert len(get_metrics()) == 0


# ---------------------------------------------------------------------------
# In-flight EMA
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_in_flight_ema_tracks_concurrency():
    """in_flight_ema should reflect actual concurrent gate holders."""
    configure(llm_size=10)

    async def call():
        async with llm_gate("openai", "m"):
            await asyncio.sleep(0.05)

    await asyncio.gather(*[call() for _ in range(5)])

    # EMA should be positive — it tracked concurrent in-flight calls
    m = get_metrics()["openai/m"]
    assert m.in_flight_ema > 0


# ---------------------------------------------------------------------------
# pool_in_flight
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_pool_in_flight_tracks_aggregate():
    """pool_in_flight should update pool-level in_flight_ema."""
    configure(llm_size=10)

    async def call(deployment: str):
        async with llm_gate("azure_pool", deployment):
            async with pool_in_flight("azure_pool", "gpt-4.1", deployment):
                await asyncio.sleep(0.05)

    await asyncio.gather(*[call(f"deploy-{i % 3}") for i in range(6)])

    metrics = get_metrics()
    # Pool-level key should have positive in_flight_ema
    assert "azure_pool/gpt-4.1" in metrics
    assert metrics["azure_pool/gpt-4.1"].in_flight_ema > 0


@pytest.mark.asyncio
async def test_pool_in_flight_registers_members():
    """pool_in_flight should register deployments in _pool_members."""
    configure(llm_size=10)

    async with llm_gate("azure_pool", "deploy-0"):
        async with pool_in_flight("azure_pool", "gpt-4.1", "deploy-0"):
            pass
    async with llm_gate("azure_pool", "deploy-1"):
        async with pool_in_flight("azure_pool", "gpt-4.1", "deploy-1"):
            pass

    assert "azure_pool/gpt-4.1" in _pool_members
    assert _pool_members["azure_pool/gpt-4.1"] == {
        "azure_pool/deploy-0",
        "azure_pool/deploy-1",
    }


# ---------------------------------------------------------------------------
# Resizable semaphore
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_resizable_semaphore_limits_concurrency():
    """Capacity limits the number of concurrent holders."""
    sem = _ResizableSemaphore(2)

    active = 0
    max_active = 0

    async def work():
        nonlocal active, max_active
        async with sem:
            active += 1
            max_active = max(max_active, active)
            await asyncio.sleep(0.05)
            active -= 1

    await asyncio.gather(*[work() for _ in range(6)])
    assert max_active <= 2


@pytest.mark.asyncio
async def test_resizable_semaphore_resize():
    """set_capacity changes the effective limit."""
    sem = _ResizableSemaphore(1)

    active = 0
    max_active = 0

    async def work():
        nonlocal active, max_active
        async with sem:
            active += 1
            max_active = max(max_active, active)
            await asyncio.sleep(0.05)
            active -= 1

    # Start with capacity 1, increase to 3 mid-flight
    tasks = [asyncio.create_task(work()) for _ in range(6)]
    await asyncio.sleep(0.01)
    await sem.set_capacity(3)
    await asyncio.gather(*tasks)
    assert max_active >= 2  # should have allowed more after resize


# ---------------------------------------------------------------------------
# AIMD controller
# ---------------------------------------------------------------------------


def test_aimd_increases_on_success():
    """All-success window should increase concurrency."""
    ctrl = _AIMDController(initial=8)
    for _ in range(ctrl.n):
        ctrl.record(True)
    assert ctrl.concurrency == 12  # 8 + 4


def test_aimd_decreases_on_failure():
    """Any failure in window should halve concurrency and set ceiling."""
    ctrl = _AIMDController(initial=16)
    # Fill window with mostly successes + one failure
    for i in range(ctrl.n):
        ctrl.record(i != 0)  # first is failure
    assert ctrl.concurrency == 8  # 16 // 2
    assert ctrl.upper == 16  # first failure establishes EMA baseline


def test_aimd_upper_ema_converges():
    """Repeated failures at the same level should converge upper there."""
    ctrl = _AIMDController(initial=100)
    # First failure at 100
    ctrl.n = 4
    for i in range(4):
        ctrl.record(i != 0)
    assert ctrl.upper == 100  # first failure baseline

    # Recover to 60, fail again repeatedly
    for _ in range(5):
        ctrl.concurrency = 60
        ctrl.n = 4
        ctrl._skip = 0
        for i in range(4):
            ctrl.record(i != 0)

    # Upper should have converged toward 60
    assert ctrl.upper < 70
    assert ctrl.upper >= 55


def test_aimd_upper_ema_resists_outlier():
    """Single failure at low level should barely move upper."""
    ctrl = _AIMDController(initial=100)
    # First failure at 100 — establishes baseline
    ctrl.n = 4
    for i in range(4):
        ctrl.record(i != 0)
    assert ctrl.upper == 100

    # One failure at 20 — outlier
    ctrl.concurrency = 20
    ctrl.n = 4
    ctrl._skip = 0
    for i in range(4):
        ctrl.record(i != 0)

    # Upper should still be close to 100 (EMA barely moved)
    assert ctrl.upper >= 70  # 0.3*20 + 0.7*100 = 76


def test_aimd_respects_upper():
    """Additive increase should not exceed upper bound."""
    ctrl = _AIMDController(initial=8)
    ctrl.upper = 10
    for _ in range(ctrl.n):
        ctrl.record(True)
    assert ctrl.concurrency == 10  # min(8 + 4, 10)
    # Another round — should stay at 10
    for _ in range(ctrl.n):
        ctrl.record(True)
    assert ctrl.concurrency == 10


# ---------------------------------------------------------------------------
# with_llm_retry
# ---------------------------------------------------------------------------


class _FakeError(Exception):
    def __init__(self, status_code, headers=None):
        self.status_code = status_code
        self.response = type("R", (), {"headers": headers or {}})() if headers else None


@pytest.mark.asyncio
async def test_with_llm_retry_success():
    """Successful call returns (result, duration).

    Returns:
        None. Asserts that a successful SDK call returns a result and positive duration.
    """
    configure(llm_size=4)

    async def sdk_call(_ctx):
        return "ok"

    result, duration = await with_llm_retry("openai", "m", sdk_call)
    assert result == "ok"
    assert duration > 0


@pytest.mark.asyncio
async def test_with_llm_retry_429_retries():
    """429 triggers retry and AIMD decrease.

    Returns:
        None. Asserts that a 429 error triggers a retry and eventually succeeds.
    """
    configure(llm_size=8)
    attempts = 0

    async def sdk_call(_ctx):
        nonlocal attempts
        attempts += 1
        if attempts == 1:
            raise _FakeError(429, headers={"retry-after": "0"})
        return "ok"

    result, _ = await with_llm_retry("openai", "m", sdk_call)
    assert result == "ok"
    assert attempts == 2


@pytest.mark.asyncio
async def test_with_llm_retry_exhausts_retries():
    """Persistent errors exhaust retries and raise."""
    configure(llm_size=4)
    attempts = 0

    async def sdk_call(_ctx):
        nonlocal attempts
        attempts += 1
        raise _FakeError(429, headers={"retry-after": "0"})

    with pytest.raises(_FakeError):
        await with_llm_retry("openai", "m", sdk_call, max_retries=2)
    assert attempts == 3  # initial + 2 retries


# ---------------------------------------------------------------------------
# Cost estimation
# ---------------------------------------------------------------------------


def test_estimate_cost_known_model():
    """Known model returns correct cost."""
    # 1M prompt, 100K completion for claude-sonnet-4-6
    # input: $3/M, output: $15/M
    # input_cost = 1_000_000 * 3.0 / 1_000_000 = 3.00
    # output_cost = 100_000 * 15.0 / 1_000_000 = 1.50
    cost = _estimate_cost("anthropic/claude-sonnet-4-6", 1_000_000, 100_000)
    assert cost == pytest.approx(4.50)


def test_estimate_cost_gemini():
    """Gemini model returns correct cost."""
    cost = _estimate_cost("google/gemini-2.5-flash", 1_000_000, 1_000_000)
    # input: 1M * $0.30/M = $0.30, output: 1M * $2.50/M = $2.50
    assert cost == pytest.approx(2.80)


def test_estimate_cost_unknown_model():
    """Unknown model returns None."""
    assert _estimate_cost("unknown/model-x", 1_000_000, 100_000) is None


def test_model_pricing_has_expected_keys():
    """Pricing table includes all expected models."""
    expected = {
        "claude-opus-4-7",
        "claude-opus-4-6",
        "claude-opus-4-5",
        "claude-sonnet-4-6",
        "claude-haiku-4-5",
        "gemini-3-pro-preview",
        "gemini-3-flash-preview",
        "gemini-2.5-flash",
        "gpt-5.4",
        "gpt-5.2",
        "gpt-4.1",
    }
    assert expected == set(MODEL_PRICING.keys())
