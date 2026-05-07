"""Integration tests for the PooledAzureProvider.

These tests make real API calls to Azure OpenAI endpoints and require:
  - Azure CLI authentication (``az login``)
  - SRBENCH_AZURE_POOL_PATH pointing to config directory with gpt-4.1.json

Skip them with: pytest -m "not integration"
Run only these: pytest -m integration tests/providers/test_azure_pool_integration.py
"""

import os

import pytest
from openai.types.chat import ChatCompletionToolParam
from openai.types.chat.chat_completion_message_tool_call import ChatCompletionMessageToolCall
from pydantic import BaseModel, ConfigDict
from srbench_llm.client import SRBenchModelClient
from srbench_llm.concurrency import configure, get_metrics, reset
from srbench_llm.providers.azure_pool import PooledAzureProvider
from srbench_llm.tracing import LLMTrace

MODEL_NAME = "gpt-4.1"
CLIENT_MODEL = f"azure_pool/{MODEL_NAME}"


def _can_create_provider() -> bool:
    """Check if pool config and Azure auth are available.

    Returns:
        ``True`` if ``SRBENCH_AZURE_POOL_PATH`` is set and a provider can
        be instantiated.
    """
    if not os.environ.get("SRBENCH_AZURE_POOL_PATH"):
        return False
    try:
        PooledAzureProvider.from_env(MODEL_NAME)
        return True
    except Exception:
        return False


requires_pool = pytest.mark.skipif(not _can_create_provider(), reason="Azure pool not configured")
integration = pytest.mark.integration


@pytest.fixture(autouse=True)
def _reset_state():
    configure(llm_size=8)
    yield
    reset()


@requires_pool
@integration
class TestPooledAzureComplete:
    @pytest.mark.asyncio
    async def test_acomplete(self):
        provider = PooledAzureProvider.from_env(MODEL_NAME)
        trace = LLMTrace()
        msg = await provider.acomplete(
            MODEL_NAME,
            [{"role": "user", "content": "Reply with exactly: hello"}],
            trace=trace,
            max_tokens=16,
        )
        assert msg.content is not None
        assert len(msg.content) > 0
        assert msg.role == "assistant"
        assert trace.provider_name == "azure_pool"
        assert trace.prompt_tokens is not None
        assert trace.prompt_tokens > 0

    @pytest.mark.asyncio
    async def test_acomplete_tokens_recorded(self):
        provider = PooledAzureProvider.from_env(MODEL_NAME)
        trace = LLMTrace()
        msg = await provider.acomplete(
            MODEL_NAME,
            [{"role": "user", "content": "Reply with exactly: hello"}],
            trace=trace,
            max_tokens=16,
        )
        assert msg.content is not None
        assert trace.total_tokens is not None
        assert trace.total_tokens > 0

    @pytest.mark.asyncio
    async def test_acomplete_metrics(self):
        """Metrics should be recorded after a successful call."""
        provider = PooledAzureProvider.from_env(MODEL_NAME)
        trace = LLMTrace()
        await provider.acomplete(
            MODEL_NAME,
            [{"role": "user", "content": "Reply with exactly: hello"}],
            trace=trace,
            max_tokens=16,
        )
        metrics = get_metrics()
        key = f"azure_pool/{MODEL_NAME}"
        assert key in metrics
        m = metrics[key]
        assert m.call_count >= 1
        assert m.completion_tokens > 0
        assert m.call_seconds > 0


@requires_pool
@integration
class TestPooledAzureParse:
    @pytest.mark.asyncio
    async def test_aparse(self):
        class Sentiment(BaseModel):
            model_config = ConfigDict(extra="forbid")
            label: str
            score: float

        provider = PooledAzureProvider.from_env(MODEL_NAME)
        result = await provider.aparse(
            MODEL_NAME,
            [
                {
                    "role": "user",
                    "content": "Classify sentiment: 'I love this!' Return label and score.",
                }
            ],
            Sentiment,
            max_tokens=64,
        )
        assert isinstance(result, Sentiment)
        assert result.label != ""
        assert 0.0 <= result.score <= 1.0


@requires_pool
@integration
class TestPooledAzureToolCalling:
    @pytest.mark.asyncio
    async def test_tool_call(self):
        tools: list[ChatCompletionToolParam] = [
            {
                "type": "function",
                "function": {
                    "name": "get_weather",
                    "description": "Get the weather for a city",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "city": {"type": "string"},
                        },
                        "required": ["city"],
                    },
                },
            }
        ]
        provider = PooledAzureProvider.from_env(MODEL_NAME)
        trace = LLMTrace()
        msg = await provider.acomplete(
            MODEL_NAME,
            [{"role": "user", "content": "What's the weather in Seattle?"}],
            trace=trace,
            tools=tools,
            max_tokens=64,
        )
        assert msg.tool_calls is not None
        assert len(msg.tool_calls) > 0
        tc = msg.tool_calls[0]
        assert isinstance(tc, ChatCompletionMessageToolCall)
        assert tc.function.name == "get_weather"


@requires_pool
@integration
class TestPooledAzureViaClient:
    @pytest.mark.asyncio
    async def test_client_acomplete(self):
        client = SRBenchModelClient()
        msg = await client.acomplete(
            CLIENT_MODEL,
            [{"role": "user", "content": "Reply with exactly: ok"}],
            max_tokens=8,
        )
        assert msg.content is not None

    @pytest.mark.asyncio
    async def test_multiple_calls_distribute(self):
        """Multiple calls should hit different endpoints (round-robin)."""
        provider = PooledAzureProvider.from_env(MODEL_NAME)
        for _ in range(3):
            trace = LLMTrace()
            msg = await provider.acomplete(
                MODEL_NAME,
                [{"role": "user", "content": "Reply with exactly: ok"}],
                trace=trace,
                max_tokens=8,
            )
            assert msg.content is not None
        # Verify round-robin advanced
        assert provider._next >= 3
