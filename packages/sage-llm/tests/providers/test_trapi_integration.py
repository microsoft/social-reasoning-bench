"""Integration tests for the TRAPI provider.

These tests make real API calls to TRAPI and require Azure CLI authentication.
Skip them with: pytest -m "not integration"
Run only these: pytest -m integration
"""

import pytest
from openai.types.chat import ChatCompletionToolParam
from openai.types.chat.chat_completion_message_tool_call import ChatCompletionMessageToolCall
from pydantic import BaseModel, ConfigDict
from sage_llm.client import SageModelClient
from sage_llm.providers.trapi import TrapiProvider
from sage_llm.tracing import LLMTrace

MODEL = "trapi/gpt-4.1-nano"


def _can_auth() -> bool:
    """Check if TRAPI authentication is available."""
    try:
        TrapiProvider()
        return True
    except Exception:
        return False


requires_trapi = pytest.mark.skipif(not _can_auth(), reason="TRAPI auth not available")
integration = pytest.mark.integration


@requires_trapi
@integration
class TestTrapiComplete:
    def test_sync_complete(self):
        provider = TrapiProvider()
        trace = LLMTrace()
        msg = provider.complete(
            "gpt-4.1-nano_2025-04-14",
            [{"role": "user", "content": "Reply with exactly: hello"}],
            trace=trace,
            max_tokens=16,
        )
        assert msg.content is not None
        assert len(msg.content) > 0
        assert msg.role == "assistant"
        assert trace.provider_name == "azure_openai"
        assert trace.prompt_tokens is not None
        assert trace.prompt_tokens > 0

    @pytest.mark.asyncio
    async def test_async_complete(self):
        provider = TrapiProvider()
        trace = LLMTrace()
        msg = await provider.acomplete(
            "gpt-4.1-nano_2025-04-14",
            [{"role": "user", "content": "Reply with exactly: hello"}],
            trace=trace,
            max_tokens=16,
        )
        assert msg.content is not None
        assert len(msg.content) > 0
        assert trace.total_tokens is not None
        assert trace.total_tokens > 0


@requires_trapi
@integration
class TestTrapiParse:
    def test_sync_parse(self):
        class Sentiment(BaseModel):
            model_config = ConfigDict(extra="forbid")
            label: str
            score: float

        provider = TrapiProvider()
        result = provider.parse(
            "gpt-4.1-nano_2025-04-14",
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

    @pytest.mark.asyncio
    async def test_async_parse(self):
        class Color(BaseModel):
            model_config = ConfigDict(extra="forbid")
            name: str
            hex: str

        provider = TrapiProvider()
        result = await provider.aparse(
            "gpt-4.1-nano_2025-04-14",
            [{"role": "user", "content": "Return the color red with its hex code."}],
            Color,
            max_tokens=64,
        )
        assert isinstance(result, Color)
        assert result.name.lower() == "red"


@requires_trapi
@integration
class TestTrapiToolCalling:
    def test_tool_call(self):
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
        provider = TrapiProvider()
        trace = LLMTrace()
        msg = provider.complete(
            "gpt-4.1-nano_2025-04-14",
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


@requires_trapi
@integration
class TestTrapiViaClient:
    def test_client_complete(self):
        client = SageModelClient()
        msg = client.complete(
            MODEL,
            [{"role": "user", "content": "Reply with exactly: ok"}],
            max_tokens=8,
        )
        assert msg.content is not None

    @pytest.mark.asyncio
    async def test_client_acomplete(self):
        client = SageModelClient()
        msg = await client.acomplete(
            MODEL,
            [{"role": "user", "content": "Reply with exactly: ok"}],
            max_tokens=8,
        )
        assert msg.content is not None
