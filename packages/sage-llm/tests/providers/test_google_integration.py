"""Integration tests for the Google Gemini provider.

These tests make real API calls to Gemini and require a GOOGLE_API_KEY.
Skip them with: pytest -m "not integration"
Run only these: pytest -m integration -k google
"""

import json

import pytest
from openai.types.chat import ChatCompletionToolParam
from openai.types.chat.chat_completion_message_tool_call import ChatCompletionMessageToolCall
from pydantic import BaseModel
from sage_llm.client import SageModelClient
from sage_llm.providers.google_genai import GoogleMessage, GoogleProvider
from sage_llm.tracing import LLMTrace
from sage_llm.types import SageMessage

MODEL = "gemini-2.5-flash"
PROVIDER_MODEL = "gemini-2.5-flash"


def _can_auth() -> bool:
    """Check if Google authentication is available.

    Returns:
        ``True`` if a :class:`GoogleProvider` can be instantiated
        without errors.
    """
    try:
        GoogleProvider()
        return True
    except Exception:
        return False


requires_google = pytest.mark.skipif(not _can_auth(), reason="Google API key not available")
integration = pytest.mark.integration


WEATHER_TOOL: ChatCompletionToolParam = {
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get the current weather for a city",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "City name"},
            },
            "required": ["city"],
        },
    },
}


@requires_google
@integration
class TestGoogleComplete:
    @pytest.mark.asyncio
    async def test_sync_complete(self):
        provider = GoogleProvider()
        trace = LLMTrace()
        msg = await provider.acomplete(
            PROVIDER_MODEL,
            [{"role": "user", "content": "Reply with exactly: hello"}],
            trace=trace,
            max_tokens=256,
        )
        assert isinstance(msg, GoogleMessage)
        assert msg.content is not None
        assert len(msg.content) > 0
        assert msg.role == "assistant"
        assert trace.provider_name == "google"
        assert trace.prompt_tokens is not None
        assert trace.prompt_tokens > 0

    @pytest.mark.asyncio
    async def test_async_complete(self):
        provider = GoogleProvider()
        trace = LLMTrace()
        msg = await provider.acomplete(
            PROVIDER_MODEL,
            [{"role": "user", "content": "Reply with exactly: hello"}],
            trace=trace,
            max_tokens=256,
        )
        assert isinstance(msg, GoogleMessage)
        assert msg.content is not None
        assert len(msg.content) > 0
        assert trace.total_tokens is not None
        assert trace.total_tokens > 0


@requires_google
@integration
class TestGoogleParse:
    @pytest.mark.asyncio
    async def test_sync_parse(self):
        class Sentiment(BaseModel):
            label: str
            score: float

        provider = GoogleProvider()
        result = await provider.aparse(
            PROVIDER_MODEL,
            [
                {
                    "role": "user",
                    "content": "Classify sentiment: 'I love this!' Return label and score.",
                }
            ],
            Sentiment,
            max_tokens=256,
        )
        assert isinstance(result, Sentiment)
        assert result.label != ""

    @pytest.mark.asyncio
    async def test_async_parse(self):
        class Color(BaseModel):
            name: str
            hex: str

        provider = GoogleProvider()
        result = await provider.aparse(
            PROVIDER_MODEL,
            [{"role": "user", "content": "Return the color red with its hex code."}],
            Color,
            max_tokens=256,
        )
        assert isinstance(result, Color)
        assert result.name.lower() == "red"


@requires_google
@integration
class TestGoogleToolCalling:
    @pytest.mark.asyncio
    async def test_tool_call_generated(self):
        """Model generates a tool call when given tools."""
        provider = GoogleProvider()
        trace = LLMTrace()
        msg = await provider.acomplete(
            PROVIDER_MODEL,
            [{"role": "user", "content": "What's the weather in Seattle?"}],
            trace=trace,
            tools=[WEATHER_TOOL],
            max_tokens=256,
        )
        assert msg.tool_calls is not None
        assert len(msg.tool_calls) > 0
        tc = msg.tool_calls[0]
        assert isinstance(tc, ChatCompletionMessageToolCall)
        assert tc.function.name == "get_weather"

    @pytest.mark.asyncio
    async def test_multi_turn_tool_use_dict_result(self):
        """Full tool-use loop: model calls tool, we return dict result, model responds."""
        provider = GoogleProvider()

        # Turn 1: model generates a tool call
        trace1 = LLMTrace()
        msg1 = await provider.acomplete(
            PROVIDER_MODEL,
            [{"role": "user", "content": "What's the weather in Seattle?"}],
            trace=trace1,
            tools=[WEATHER_TOOL],
            max_tokens=256,
        )
        assert msg1.tool_calls is not None
        tc = msg1.tool_calls[0]

        # Turn 2: provide tool result (dict content) and get final answer
        messages: list[SageMessage] = [
            {"role": "user", "content": "What's the weather in Seattle?"},
            msg1,
            {
                "role": "tool",
                "tool_call_id": tc.id,
                "content": json.dumps({"temperature": 55, "condition": "cloudy"}),
            },
        ]
        trace2 = LLMTrace()
        msg2 = await provider.acomplete(
            PROVIDER_MODEL,
            messages,
            trace=trace2,
            tools=[WEATHER_TOOL],
            max_tokens=512,
        )
        assert msg2.content is not None
        assert len(msg2.content) > 0

    @pytest.mark.asyncio
    async def test_multi_turn_tool_use_string_result(self):
        """Tool result is a plain string (non-JSON) — should not crash.

        This is the scenario that caused the original FunctionResponse
        ValidationError when the result wasn't wrapped in a dict.
        """
        provider = GoogleProvider()

        trace1 = LLMTrace()
        msg1 = await provider.acomplete(
            PROVIDER_MODEL,
            [{"role": "user", "content": "What's the weather in Seattle?"}],
            trace=trace1,
            tools=[WEATHER_TOOL],
            max_tokens=256,
        )
        assert msg1.tool_calls is not None
        tc = msg1.tool_calls[0]

        messages: list[SageMessage] = [
            {"role": "user", "content": "What's the weather in Seattle?"},
            msg1,
            {
                "role": "tool",
                "tool_call_id": tc.id,
                "content": "55 degrees and cloudy",
            },
        ]
        trace2 = LLMTrace()
        msg2 = await provider.acomplete(
            PROVIDER_MODEL,
            messages,
            trace=trace2,
            tools=[WEATHER_TOOL],
            max_tokens=512,
        )
        assert msg2.content is not None

    @pytest.mark.asyncio
    async def test_multi_turn_tool_use_json_string_result(self):
        """Tool result is a JSON-encoded string (e.g. '"sunny"') — should not crash.

        json.loads('"sunny"') returns 'sunny' (a str, not a dict).
        """
        provider = GoogleProvider()

        trace1 = LLMTrace()
        msg1 = await provider.acomplete(
            PROVIDER_MODEL,
            [{"role": "user", "content": "What's the weather in Seattle?"}],
            trace=trace1,
            tools=[WEATHER_TOOL],
            max_tokens=256,
        )
        assert msg1.tool_calls is not None
        tc = msg1.tool_calls[0]

        messages: list[SageMessage] = [
            {"role": "user", "content": "What's the weather in Seattle?"},
            msg1,
            {
                "role": "tool",
                "tool_call_id": tc.id,
                "content": '"sunny"',
            },
        ]
        trace2 = LLMTrace()
        msg2 = await provider.acomplete(
            PROVIDER_MODEL,
            messages,
            trace=trace2,
            tools=[WEATHER_TOOL],
            max_tokens=512,
        )
        assert msg2.content is not None

    @pytest.mark.asyncio
    async def test_async_multi_turn_tool_use(self):
        """Async version of the multi-turn tool-use loop."""
        provider = GoogleProvider()

        trace1 = LLMTrace()
        msg1 = await provider.acomplete(
            PROVIDER_MODEL,
            [{"role": "user", "content": "What's the weather in Seattle?"}],
            trace=trace1,
            tools=[WEATHER_TOOL],
            max_tokens=256,
        )
        assert msg1.tool_calls is not None
        tc = msg1.tool_calls[0]

        messages: list[SageMessage] = [
            {"role": "user", "content": "What's the weather in Seattle?"},
            msg1,
            {
                "role": "tool",
                "tool_call_id": tc.id,
                "content": json.dumps({"temperature": 55, "condition": "cloudy"}),
            },
        ]
        trace2 = LLMTrace()
        msg2 = await provider.acomplete(
            PROVIDER_MODEL,
            messages,
            trace=trace2,
            tools=[WEATHER_TOOL],
            max_tokens=512,
        )
        assert msg2.content is not None


GEMINI3_MODEL = "gemini-3-flash-preview"


@requires_google
@integration
class TestGemini3FlashToolCalling:
    """Tests targeting Gemini 3 Flash which requires thought_signature on
    function-call parts in multi-turn conversations."""

    @pytest.mark.asyncio
    async def test_tool_call_generated(self):
        provider = GoogleProvider()
        trace = LLMTrace()
        msg = await provider.acomplete(
            GEMINI3_MODEL,
            [{"role": "user", "content": "What's the weather in Seattle?"}],
            trace=trace,
            tools=[WEATHER_TOOL],
            max_tokens=256,
        )
        assert msg.tool_calls is not None
        assert len(msg.tool_calls) > 0
        assert msg.tool_calls[0].function.name == "get_weather"

    @pytest.mark.asyncio
    async def test_multi_turn_tool_use(self):
        """Full tool-use loop on Gemini 3 Flash — the scenario that fails
        without thought_signature preservation."""
        provider = GoogleProvider()

        trace1 = LLMTrace()
        msg1 = await provider.acomplete(
            GEMINI3_MODEL,
            [{"role": "user", "content": "What's the weather in Seattle?"}],
            trace=trace1,
            tools=[WEATHER_TOOL],
            max_tokens=256,
        )
        assert msg1.tool_calls is not None
        tc = msg1.tool_calls[0]

        # Verify signature was captured
        assert isinstance(msg1, GoogleMessage)
        # (signature may be None on some models, but the field should exist)

        messages: list[SageMessage] = [
            {"role": "user", "content": "What's the weather in Seattle?"},
            msg1,
            {
                "role": "tool",
                "tool_call_id": tc.id,
                "content": json.dumps({"temperature": 55, "condition": "cloudy"}),
            },
        ]
        trace2 = LLMTrace()
        msg2 = await provider.acomplete(
            GEMINI3_MODEL,
            messages,
            trace=trace2,
            tools=[WEATHER_TOOL],
            max_tokens=512,
        )
        assert msg2.content is not None
        assert len(msg2.content) > 0

    @pytest.mark.asyncio
    async def test_multi_turn_tool_use_string_result(self):
        """Plain-string tool result on Gemini 3 Flash."""
        provider = GoogleProvider()

        trace1 = LLMTrace()
        msg1 = await provider.acomplete(
            GEMINI3_MODEL,
            [{"role": "user", "content": "What's the weather in Seattle?"}],
            trace=trace1,
            tools=[WEATHER_TOOL],
            max_tokens=256,
        )
        assert msg1.tool_calls is not None
        tc = msg1.tool_calls[0]

        messages: list[SageMessage] = [
            {"role": "user", "content": "What's the weather in Seattle?"},
            msg1,
            {
                "role": "tool",
                "tool_call_id": tc.id,
                "content": "55 degrees and cloudy",
            },
        ]
        trace2 = LLMTrace()
        msg2 = await provider.acomplete(
            GEMINI3_MODEL,
            messages,
            trace=trace2,
            tools=[WEATHER_TOOL],
            max_tokens=512,
        )
        assert msg2.content is not None

    @pytest.mark.asyncio
    async def test_sequential_multi_step_tool_use(self):
        """Two sequential tool calls — both require thought_signature."""
        provider = GoogleProvider()
        tools: list[ChatCompletionToolParam] = [
            WEATHER_TOOL,
            {
                "type": "function",
                "function": {
                    "name": "get_time",
                    "description": "Get the current time for a city",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "city": {"type": "string", "description": "City name"},
                        },
                        "required": ["city"],
                    },
                },
            },
        ]

        # Step 1: ask about weather AND time
        trace1 = LLMTrace()
        msg1 = await provider.acomplete(
            GEMINI3_MODEL,
            [{"role": "user", "content": "What's the weather and current time in Seattle?"}],
            trace=trace1,
            tools=tools,
            max_tokens=256,
        )
        assert msg1.tool_calls is not None
        tc1 = msg1.tool_calls[0]

        # Step 2: return first tool result
        messages: list[SageMessage] = [
            {"role": "user", "content": "What's the weather and current time in Seattle?"},
            msg1,
            {
                "role": "tool",
                "tool_call_id": tc1.id,
                "content": json.dumps({"temperature": 55, "condition": "cloudy"}),
            },
        ]

        # If there were parallel calls, respond to all of them
        for tc in msg1.tool_calls[1:]:
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tc.id,
                    "content": json.dumps({"time": "3:00 PM PST"}),
                }
            )

        trace2 = LLMTrace()
        msg2 = await provider.acomplete(
            GEMINI3_MODEL,
            messages,
            trace=trace2,
            tools=tools,
            max_tokens=512,
        )
        # Model may respond with text or request another tool call
        assert msg2.content is not None or msg2.tool_calls is not None


@requires_google
@integration
class TestGoogleViaClient:
    @pytest.mark.asyncio
    async def test_client_complete(self):
        client = SageModelClient()
        msg = await client.acomplete(
            f"gemini/{MODEL}",
            [{"role": "user", "content": "Reply with exactly: ok"}],
            max_tokens=256,
        )
        assert msg.content is not None

    @pytest.mark.asyncio
    async def test_client_acomplete(self):
        client = SageModelClient()
        msg = await client.acomplete(
            f"gemini/{MODEL}",
            [{"role": "user", "content": "Reply with exactly: ok"}],
            max_tokens=256,
        )
        assert msg.content is not None

    @pytest.mark.asyncio
    async def test_client_alias_complete(self):
        """Bare 'gemini-*' alias should route correctly."""
        client = SageModelClient()
        msg = await client.acomplete(
            MODEL,
            [{"role": "user", "content": "Reply with exactly: ok"}],
            max_tokens=256,
        )
        assert msg.content is not None
