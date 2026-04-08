"""Tests for PooledAzureProvider endpoint rotation and health tracking."""

import asyncio
from unittest.mock import AsyncMock, MagicMock

import pytest
from sage_llm.concurrency import configure, get_metrics, reset
from sage_llm.providers.azure_pool import PooledAzureProvider, _EndpointState


class _FakeError(Exception):
    def __init__(self, status_code, headers=None):
        self.status_code = status_code
        self.response = MagicMock(headers=headers or {}) if headers else None


def _make_response(prompt_tokens=10, completion_tokens=5):
    """Create a minimal mock ChatCompletion.

    Args:
        prompt_tokens: Number of prompt tokens for the mock usage.
        completion_tokens: Number of completion tokens for the mock usage.

    Returns:
        A :class:`MagicMock` mimicking a ChatCompletion response.
    """
    usage = MagicMock()
    usage.prompt_tokens = prompt_tokens
    usage.completion_tokens = completion_tokens
    usage.total_tokens = prompt_tokens + completion_tokens
    usage.completion_tokens_details = None

    choice = MagicMock()
    choice.message.role = "assistant"
    choice.message.content = "ok"
    choice.message.tool_calls = None
    choice.message.refusal = None
    choice.finish_reason = "stop"

    resp = MagicMock()
    resp.id = "test-id"
    resp.model = "gpt-4.1"
    resp.choices = [choice]
    resp.usage = usage
    resp.model_dump.return_value = {}
    return resp


def _make_provider(n_endpoints=3):
    """Create a PooledAzureProvider with mock clients.

    Args:
        n_endpoints: Number of mock endpoints to create.

    Returns:
        A :class:`PooledAzureProvider` with mock endpoint states.
    """
    provider = PooledAzureProvider.__new__(PooledAzureProvider)
    provider._endpoints = []
    provider._next = 0
    for i in range(n_endpoints):
        client = MagicMock()
        client.chat.completions.create = AsyncMock(return_value=_make_response())
        ep = _EndpointState(client, deployment=f"deploy-{i}", label=f"endpoint-{i}")
        provider._endpoints.append(ep)
    return provider


@pytest.fixture(autouse=True)
def _reset_state():
    configure(llm_size=32)
    yield
    reset()


@pytest.mark.asyncio
async def test_pick_healthy_round_robins():
    """_pick_healthy should cycle through endpoints."""
    provider = _make_provider(3)
    eps = [provider._pick_healthy() for _ in range(6)]
    # Should cycle: 0, 1, 2, 0, 1, 2
    deployments = [ep.deployment for ep in eps]
    assert deployments == ["deploy-0", "deploy-1", "deploy-2", "deploy-0", "deploy-1", "deploy-2"]


@pytest.mark.asyncio
async def test_pick_healthy_skips_unhealthy():
    """_pick_healthy should skip unhealthy endpoints."""
    provider = _make_provider(3)
    await provider._endpoints[0].mark_unhealthy(10.0)

    ep = provider._pick_healthy()
    assert ep.deployment == "deploy-1"


@pytest.mark.asyncio
async def test_pick_healthy_returns_none_when_all_unhealthy():
    """_pick_healthy returns None when all endpoints are down."""
    provider = _make_provider(2)
    for ep in provider._endpoints:
        await ep.mark_unhealthy(10.0)
    assert provider._pick_healthy() is None


@pytest.mark.asyncio
async def test_endpoint_gate_yields_endpoint():
    """_endpoint_gate should yield the selected endpoint."""
    provider = _make_provider(3)
    async with provider._endpoint_gate("azure_pool", "gpt-4.1") as ep:
        assert ep is not None
        assert ep.deployment.startswith("deploy-")


@pytest.mark.asyncio
async def test_endpoint_gate_marks_unhealthy_on_error():
    """Errors inside the gate should mark the endpoint unhealthy."""
    provider = _make_provider(3)
    with pytest.raises(_FakeError):
        async with provider._endpoint_gate("azure_pool", "gpt-4.1") as ep:
            raise _FakeError(429, headers={"retry-after": "10"})
    assert not ep.is_healthy


@pytest.mark.asyncio
async def test_endpoint_gate_all_unhealthy_raises():
    """Gate should raise RuntimeError when all endpoints are down."""
    provider = _make_provider(2)
    for ep in provider._endpoints:
        await ep.mark_unhealthy(10.0)

    with pytest.raises(RuntimeError, match="all 2 endpoints unhealthy"):
        async with provider._endpoint_gate("azure_pool", "gpt-4.1"):
            pass


@pytest.mark.asyncio
async def test_endpoint_recovers():
    """Endpoint should be usable again after cooldown expires."""
    provider = _make_provider(2)
    await provider._endpoints[0].mark_unhealthy(0.01)
    assert not provider._endpoints[0].is_healthy

    await asyncio.sleep(0.02)
    assert provider._endpoints[0].is_healthy

    provider._next = 0
    ep = provider._pick_healthy()
    assert ep.deployment == "deploy-0"


@pytest.mark.asyncio
async def test_mark_unhealthy_logs_once():
    """mark_unhealthy should only log on the first call (lock dedup)."""
    provider = _make_provider(1)
    ep = provider._endpoints[0]

    await ep.mark_unhealthy(10.0)
    assert ep.error_count == 1

    # Second call while still unhealthy — no-op
    await ep.mark_unhealthy(10.0)
    assert ep.error_count == 1


@pytest.mark.asyncio
async def test_endpoint_gate_tracks_pool_in_flight():
    """_endpoint_gate should update pool-level in_flight_ema for the model key."""
    provider = _make_provider(3)

    async def call():
        async with provider._endpoint_gate("azure_pool", "gpt-4.1") as ep:
            await asyncio.sleep(0.05)

    await asyncio.gather(*[call() for _ in range(6)])

    metrics = get_metrics()
    # Pool-level key "azure_pool/gpt-4.1" should have tracked in-flight
    assert "azure_pool/gpt-4.1" in metrics
    assert metrics["azure_pool/gpt-4.1"].in_flight_ema > 0
