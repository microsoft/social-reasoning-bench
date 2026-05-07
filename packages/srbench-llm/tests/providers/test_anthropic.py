"""Tests for the Anthropic provider."""

import json
from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import anthropic.types
import pytest
from openai.types.chat import (
    ChatCompletionFunctionToolParam,
    ChatCompletionToolChoiceOptionParam,
    ChatCompletionToolParam,
)
from openai.types.chat.chat_completion_message_tool_call import (
    ChatCompletionMessageToolCall,
    Function,
)
from openai.types.shared_params import FunctionDefinition
from pydantic import BaseModel
from srbench_llm.providers.anthropic import (
    AnthropicMessage,
    AnthropicProvider,
    _build_kwargs,
    _structured_output_tool,
    _to_anthropic_message,
    _translate_messages,
    _translate_tool_choice,
    _translate_tools,
)
from srbench_llm.tracing import LLMTrace
from srbench_llm.types import SRBenchChatCompletionMessage, SRBenchMessage


def _make_anthropic_response(
    content: list[anthropic.types.ContentBlock] | None = None,
    stop_reason: anthropic.types.message.StopReason = "end_turn",
    model: str = "claude-sonnet-4-5",
    input_tokens: int = 10,
    output_tokens: int = 5,
) -> anthropic.types.Message:
    if content is None:
        content = [anthropic.types.TextBlock(type="text", text="Hello!")]
    return anthropic.types.Message(
        id="msg_123",
        content=content,
        model=model,
        role="assistant",
        stop_reason=stop_reason,
        type="message",
        usage=anthropic.types.Usage(input_tokens=input_tokens, output_tokens=output_tokens),
    )


class TestTranslateMessages:
    def test_extracts_system(self):
        msgs: list[SRBenchMessage] = [
            {"role": "system", "content": "be helpful"},
            {"role": "user", "content": "hi"},
        ]
        system, out = _translate_messages(msgs)
        assert system == "be helpful"
        assert len(out) == 1
        m = out[0]
        assert isinstance(m, dict)
        assert m["role"] == "user"

    def test_user_message(self):
        msgs: list[SRBenchMessage] = [{"role": "user", "content": "hello"}]
        system, out = _translate_messages(msgs)
        assert isinstance(system, anthropic.NotGiven)
        assert out[0] == {"role": "user", "content": "hello"}

    def test_assistant_message_with_content(self):
        msgs: list[SRBenchMessage] = [
            SRBenchChatCompletionMessage(role="assistant", content="answer")
        ]
        _, out = _translate_messages(msgs)
        m = out[0]
        assert isinstance(m, dict)
        assert m["role"] == "assistant"
        blocks = m["content"]
        assert isinstance(blocks, list)
        assert any(
            isinstance(b, dict) and b.get("type") == "text" and b.get("text") == "answer"
            for b in blocks
        )

    def test_assistant_message_injects_thinking_blocks(self):
        thinking = [{"type": "thinking", "thinking": "hmm...", "signature": "sig123"}]
        msgs: list[SRBenchMessage] = [
            AnthropicMessage(role="assistant", content="answer", thinking_blocks=thinking)
        ]
        _, out = _translate_messages(msgs)

        m = out[0]
        assert isinstance(m, dict)
        blocks = m["content"]
        assert isinstance(blocks, list)
        assert blocks[0] == thinking[0]
        assert blocks[1] == {"type": "text", "text": "answer"}

    def test_assistant_with_tool_calls(self):
        tc = ChatCompletionMessageToolCall(
            id="call_1",
            type="function",
            function=Function(name="search", arguments='{"q": "test"}'),
        )
        msgs: list[SRBenchMessage] = [
            SRBenchChatCompletionMessage(role="assistant", content=None, tool_calls=[tc])
        ]
        _, out = _translate_messages(msgs)

        m = out[0]
        assert isinstance(m, dict)
        blocks = m["content"]
        assert isinstance(blocks, list)
        tool_block = next(b for b in blocks if isinstance(b, dict) and b.get("type") == "tool_use")
        assert isinstance(tool_block, dict)
        assert tool_block.get("id") == "call_1"
        assert tool_block.get("name") == "search"
        assert tool_block.get("input") == {"q": "test"}


class TestTranslateTools:
    def test_function_tools(self):
        params: dict[str, object] = {
            "type": "object",
            "properties": {"city": {"type": "string"}},
        }
        openai_tools: list[ChatCompletionToolParam] = [
            ChatCompletionFunctionToolParam(
                type="function",
                function=FunctionDefinition(
                    name="get_weather",
                    description="Get weather",
                    parameters=params,
                ),
            )
        ]
        result = _translate_tools(openai_tools)
        assert len(result) == 1
        assert result[0]["name"] == "get_weather"
        assert result[0]["description"] == "Get weather"
        assert "input_schema" in result[0]


class TestTranslateToolChoice:
    def test_auto(self):
        assert _translate_tool_choice("auto") == {"type": "auto"}

    def test_required(self):
        assert _translate_tool_choice("required") == {"type": "any"}

    def test_specific_function(self):
        choice: ChatCompletionToolChoiceOptionParam = {
            "type": "function",
            "function": {"name": "my_tool"},
        }
        assert _translate_tool_choice(choice) == {"type": "tool", "name": "my_tool"}


class TestBuildKwargs:
    def test_basic_params(self):
        result = _build_kwargs(
            system="sys",
            temperature=0.5,
            max_tokens=1000,
            top_p=None,
            stop=None,
            tools=None,
            tool_choice=None,
            reasoning_effort=None,
            model="claude-sonnet-4-5",
        )
        assert result["system"] == "sys"
        assert result["temperature"] == 0.5
        assert result["max_tokens"] == 1000
        assert "top_p" not in result

    def test_reasoning_effort_int(self):
        result = _build_kwargs(
            system=anthropic.NOT_GIVEN,
            temperature=None,
            max_tokens=8192,
            top_p=None,
            stop=None,
            tools=None,
            tool_choice=None,
            reasoning_effort=4000,
            model="claude-sonnet-4-5",
        )
        assert result["thinking"] == {"type": "enabled", "budget_tokens": 4000}

    def test_reasoning_effort_string(self):
        result = _build_kwargs(
            system=anthropic.NOT_GIVEN,
            temperature=None,
            max_tokens=8192,
            top_p=None,
            stop=None,
            tools=None,
            tool_choice=None,
            reasoning_effort="high",
            model="claude-opus-4-5",
        )
        assert result["reasoning_effort"] == "high"

    def test_stop_string_becomes_list(self):
        result = _build_kwargs(
            system=anthropic.NOT_GIVEN,
            temperature=None,
            max_tokens=8192,
            top_p=None,
            stop="END",
            tools=None,
            tool_choice=None,
            reasoning_effort=None,
            model="claude-sonnet-4-5",
        )
        assert result["stop_sequences"] == ["END"]


class TestToAnthropicMessage:
    def test_text_response(self):
        resp = _make_anthropic_response()
        msg = _to_anthropic_message(resp, "claude-sonnet-4-5")

        assert isinstance(msg, AnthropicMessage)
        assert isinstance(msg, SRBenchChatCompletionMessage)
        assert msg.role == "assistant"
        assert msg.content == "Hello!"
        assert msg.thinking_blocks is None
        assert msg.completion_info is not None
        assert msg.completion_info.id == "msg_123"
        assert msg.completion_info.finish_reason == "stop"

    def test_thinking_blocks_preserved(self):
        content: list[anthropic.types.ContentBlock] = [
            anthropic.types.ThinkingBlock(
                type="thinking", thinking="Let me think...", signature="sig"
            ),
            anthropic.types.TextBlock(type="text", text="The answer"),
        ]
        resp = _make_anthropic_response(content=content)
        msg = _to_anthropic_message(resp, "claude-sonnet-4-5")

        assert msg.content == "The answer"
        assert msg.thinking_blocks is not None
        assert len(msg.thinking_blocks) == 1
        assert msg.thinking_blocks[0]["thinking"] == "Let me think..."
        assert msg.thinking_blocks[0]["signature"] == "sig"

    def test_tool_use_response(self):
        content: list[anthropic.types.ContentBlock] = [
            anthropic.types.ToolUseBlock(
                type="tool_use", id="tu_1", name="search", input={"q": "test"}
            ),
        ]
        resp = _make_anthropic_response(content=content, stop_reason="tool_use")
        msg = _to_anthropic_message(resp, "claude-sonnet-4-5")

        assert msg.tool_calls is not None
        assert len(msg.tool_calls) == 1
        tc = msg.tool_calls[0]
        assert isinstance(tc, ChatCompletionMessageToolCall)
        assert tc.function.name == "search"
        assert json.loads(tc.function.arguments) == {"q": "test"}
        assert msg.completion_info is not None
        assert msg.completion_info.finish_reason == "tool_calls"

    def test_usage_mapped(self):
        resp = _make_anthropic_response(input_tokens=100, output_tokens=50)
        msg = _to_anthropic_message(resp, "claude-sonnet-4-5")

        assert msg.completion_info is not None
        assert msg.completion_info.usage is not None
        assert msg.completion_info.usage.prompt_tokens == 100
        assert msg.completion_info.usage.completion_tokens == 50
        assert msg.completion_info.usage.total_tokens == 150


class TestStructuredOutputTool:
    def test_creates_tool(self):
        class Weather(BaseModel):
            city: str
            temp: float

        tool, name = _structured_output_tool(Weather)
        assert name == "output_Weather"
        assert tool["name"] == "output_Weather"
        assert "input_schema" in tool


def _mock_stream_returning(response: anthropic.types.Message) -> MagicMock:
    """Build a mock for ``client.messages.stream(**kwargs)``.

    The provider uses ``async with client.messages.stream(...) as stream`` then
    ``await stream.get_final_message()``, so the mock must return an async
    context manager (not a coroutine, which is what AsyncMock would produce).
    """
    stream_obj = MagicMock()
    stream_obj.get_final_message = AsyncMock(return_value=response)
    cm = MagicMock()
    cm.__aenter__ = AsyncMock(return_value=stream_obj)
    cm.__aexit__ = AsyncMock(return_value=None)
    return MagicMock(return_value=cm)


class TestAnthropicProviderComplete:
    @pytest.mark.asyncio
    @patch("srbench_llm.providers.anthropic.anthropic.AsyncAnthropic")
    async def test_complete_basic(self, mock_cls):
        mock_client = MagicMock()
        mock_cls.return_value = mock_client
        mock_client.messages.stream = _mock_stream_returning(
            _make_anthropic_response(content=[anthropic.types.TextBlock(type="text", text="hi")])
        )

        provider = AnthropicProvider(api_key="test-key")
        trace = LLMTrace()
        msg = await provider.acomplete(
            "claude-sonnet-4-5",
            [{"role": "user", "content": "hello"}],
            trace=trace,
            temperature=0.5,
            max_tokens=1000,
        )

        assert isinstance(msg, AnthropicMessage)
        assert msg.content == "hi"
        assert trace.provider_name == "anthropic"

    @pytest.mark.asyncio
    @patch("srbench_llm.providers.anthropic.anthropic.AsyncAnthropic")
    async def test_parse_uses_tool_trick(self, mock_cls):
        class Answer(BaseModel):
            text: str

        mock_client = MagicMock()
        mock_cls.return_value = mock_client
        mock_client.messages.stream = _mock_stream_returning(
            _make_anthropic_response(
                content=[
                    anthropic.types.ToolUseBlock(
                        type="tool_use",
                        id="tu_1",
                        name="output_Answer",
                        input={"text": "hello"},
                    ),
                ],
                stop_reason="tool_use",
            )
        )

        provider = AnthropicProvider()
        result = await provider.aparse(
            "claude-sonnet-4-5",
            [{"role": "user", "content": "hi"}],
            Answer,
        )

        assert isinstance(result, Answer)
        assert result.text == "hello"
        call_kwargs = mock_client.messages.stream.call_args.kwargs
        assert call_kwargs["tool_choice"]["type"] == "tool"
        assert call_kwargs["tool_choice"]["name"] == "output_Answer"
