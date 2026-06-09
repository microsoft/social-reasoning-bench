"""Tests for the OpenAI provider."""

from typing import Literal
from unittest.mock import AsyncMock, patch

import pytest
from openai.types.chat import ChatCompletion, ChatCompletionMessage
from openai.types.chat.chat_completion import Choice
from openai.types.chat.chat_completion_message_tool_call import (
    ChatCompletionMessageToolCall,
    Function,
)
from openai.types.completion_usage import CompletionUsage
from pydantic import BaseModel
from srbench_llm.providers.openai import (
    OpenAIMessage,
    OpenAIProvider,
    _pydantic_to_json_schema,
    _to_openai_message,
    _to_openai_messages,
)
from srbench_llm.tracing import LLMTrace
from srbench_llm.types import (
    SRBenchChatCompletionInfo,
    SRBenchChatCompletionMessage,
    SRBenchInputMessage,
)


def _make_chat_completion(
    content: str = "Hello!",
    model: str = "gpt-4o",
    finish_reason: Literal[
        "stop", "length", "tool_calls", "content_filter", "function_call"
    ] = "stop",
    tool_calls=None,
    usage=None,
) -> ChatCompletion:
    msg = ChatCompletionMessage(
        role="assistant",
        content=content,
        tool_calls=tool_calls,
    )
    return ChatCompletion(
        id="chatcmpl-123",
        choices=[Choice(index=0, finish_reason=finish_reason, message=msg)],
        created=1700000000,
        model=model,
        object="chat.completion",
        usage=usage or CompletionUsage(prompt_tokens=10, completion_tokens=5, total_tokens=15),
    )


class TestToOpenAIMessage:
    def test_basic_conversion(self):
        resp = _make_chat_completion(content="hi", model="gpt-4o")
        msg = _to_openai_message(resp)

        assert isinstance(msg, OpenAIMessage)
        assert isinstance(msg, SRBenchChatCompletionMessage)
        assert msg.role == "assistant"
        assert msg.content == "hi"
        assert msg.completion_info is not None
        assert msg.completion_info.id == "chatcmpl-123"
        assert msg.completion_info.model == "gpt-4o"
        assert msg.completion_info.finish_reason == "stop"

    def test_usage_preserved(self):
        usage = CompletionUsage(prompt_tokens=100, completion_tokens=50, total_tokens=150)
        resp = _make_chat_completion(usage=usage)
        msg = _to_openai_message(resp)

        assert msg.completion_info is not None
        assert msg.completion_info.usage is not None
        assert msg.completion_info.usage.prompt_tokens == 100
        assert msg.completion_info.usage.completion_tokens == 50

    def test_tool_calls_preserved(self):
        tc = ChatCompletionMessageToolCall(
            id="call_1",
            type="function",
            function=Function(name="get_weather", arguments='{"city": "NYC"}'),
        )
        resp = _make_chat_completion(content="", tool_calls=[tc], finish_reason="tool_calls")
        msg = _to_openai_message(resp)

        assert msg.tool_calls is not None
        assert len(msg.tool_calls) == 1
        assert msg.completion_info is not None
        assert msg.completion_info.finish_reason == "tool_calls"


class TestToOpenAIMessages:
    def test_sage_message_conversion(self):
        msgs: list[SRBenchInputMessage] = [
            {"role": "system", "content": "be helpful"},
            {"role": "user", "content": "hi"},
        ]
        result = _to_openai_messages(msgs)

        assert len(result) == 2
        assert result[0]["role"] == "system"
        assert result[0]["content"] == "be helpful"
        assert "completion_info" not in result[0]

    def test_assistant_with_completion_info_excluded(self):
        info = SRBenchChatCompletionInfo(id="x", model="m", finish_reason="stop")
        msgs: list[SRBenchInputMessage] = [
            SRBenchChatCompletionMessage(
                role="assistant", content="response", completion_info=info
            ).to_input_dict()
        ]
        result = _to_openai_messages(msgs)

        assert "completion_info" not in result[0]
        assert result[0]["content"] == "response"

    def test_extension_keys_stripped_for_sdk(self):
        """SRBench extension keys (thinking_blocks, thought_parts,
        tool_call_signatures, completion_info) must be stripped — the OpenAI
        SDK rejects unknown keys."""
        msgs: list[SRBenchInputMessage] = [
            {
                "role": "assistant",
                "content": "x",
                "thinking_blocks": [{"type": "thinking", "thinking": "...", "signature": "s"}],
                "thought_parts": [{"text": "t", "thought_signature": b"sig"}],
                "tool_call_signatures": [b"sig"],
                "completion_info": {"id": "x", "model": "m", "finish_reason": "stop"},
            }
        ]
        result = _to_openai_messages(msgs)
        for forbidden in (
            "thinking_blocks",
            "thought_parts",
            "tool_call_signatures",
            "completion_info",
        ):
            assert forbidden not in result[0], f"extension key {forbidden!r} leaked into SDK input"
        assert result[0]["content"] == "x"


class TestPydanticToJsonSchema:
    def test_conversion(self):
        class MyModel(BaseModel):
            name: str
            age: int

        result = _pydantic_to_json_schema(MyModel)
        assert result["type"] == "json_schema"
        assert result["json_schema"]["name"] == "MyModel"
        assert result["json_schema"]["strict"] is True
        assert "properties" in result["json_schema"]["schema"]


class TestOpenAIProviderComplete:
    @pytest.mark.asyncio
    @patch("srbench_llm.providers.openai.openai.AsyncOpenAI")
    async def test_complete_returns_sage_message(self, mock_cls):
        mock_client = AsyncMock()
        mock_cls.return_value = mock_client
        mock_client.chat.completions.create.return_value = _make_chat_completion(content="hi")

        provider = OpenAIProvider(api_key="test-key")
        trace = LLMTrace()
        msg = await provider.acomplete(
            "gpt-4o",
            [{"role": "user", "content": "hello"}],
            trace=trace,
            temperature=0.5,
        )

        assert isinstance(msg, OpenAIMessage)
        assert msg.content == "hi"

    @pytest.mark.asyncio
    @patch("srbench_llm.providers.openai.openai.AsyncOpenAI")
    async def test_complete_fills_trace(self, mock_cls):
        mock_client = AsyncMock()
        mock_cls.return_value = mock_client
        mock_client.chat.completions.create.return_value = _make_chat_completion(content="hi")

        provider = OpenAIProvider(api_key="test-key")
        trace = LLMTrace()
        await provider.acomplete("gpt-4o", [{"role": "user", "content": "hello"}], trace=trace)

        assert trace.provider_name == "openai"
        assert trace.provider_request != {}
        assert trace.provider_response != {}
        assert trace.prompt_tokens == 10
        assert trace.completion_tokens == 5
        assert trace.total_tokens == 15

    @pytest.mark.asyncio
    @patch("srbench_llm.providers.openai.openai.AsyncOpenAI")
    async def test_parse_adds_response_format(self, mock_cls):
        class Answer(BaseModel):
            text: str

        mock_client = AsyncMock()
        mock_cls.return_value = mock_client
        mock_client.chat.completions.create.return_value = _make_chat_completion(
            content='{"text": "hello"}'
        )

        provider = OpenAIProvider()
        result = await provider.aparse("gpt-4o", [{"role": "user", "content": "hi"}], Answer)

        assert isinstance(result, Answer)
        assert result.text == "hello"


class TestOpenAIProviderAsync:
    @pytest.mark.asyncio
    @patch("srbench_llm.providers.openai.openai.AsyncOpenAI")
    async def test_acomplete_returns_sage_message(self, mock_async_cls):
        mock_async_client = AsyncMock()
        mock_async_cls.return_value = mock_async_client
        mock_async_client.chat.completions.create.return_value = _make_chat_completion(
            content="async hi"
        )

        provider = OpenAIProvider()
        trace = LLMTrace()
        msg = await provider.acomplete(
            "gpt-4o",
            [{"role": "user", "content": "hello"}],
            trace=trace,
        )

        assert isinstance(msg, OpenAIMessage)
        assert msg.content == "async hi"
        assert trace.provider_name == "openai"
