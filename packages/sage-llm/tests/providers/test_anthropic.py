"""Tests for the Anthropic provider."""

import json
from typing import Any, cast
from unittest.mock import AsyncMock, MagicMock, patch

import anthropic.types
import pytest
from openai.types.chat import (
    ChatCompletionFunctionToolParam,
    ChatCompletionToolChoiceOptionParam,
    ChatCompletionToolMessageParam,
    ChatCompletionToolParam,
)
from openai.types.chat.chat_completion_message_tool_call import (
    ChatCompletionMessageToolCall,
    Function,
)
from openai.types.shared_params import FunctionDefinition
from pydantic import BaseModel
from sage_llm.providers.anthropic import (
    AnthropicMessage,
    AnthropicProvider,
    _build_kwargs,
    _extract_text,
    _structured_output_tool,
    _to_anthropic_message,
    _translate_messages,
    _translate_tool,
    _translate_tool_choice,
    _translate_tools,
)
from sage_llm.tracing import LLMTrace
from sage_llm.types import SageChatCompletionMessage, SageMessage


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
        msgs: list[SageMessage] = [
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
        msgs: list[SageMessage] = [{"role": "user", "content": "hello"}]
        system, out = _translate_messages(msgs)
        assert isinstance(system, anthropic.NotGiven)
        assert out[0] == {"role": "user", "content": "hello"}

    def test_assistant_message_with_content(self):
        msgs: list[SageMessage] = [SageChatCompletionMessage(role="assistant", content="answer")]
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
        msgs: list[SageMessage] = [
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
        msgs: list[SageMessage] = [
            SageChatCompletionMessage(role="assistant", content=None, tool_calls=[tc])
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
        assert isinstance(msg, SageChatCompletionMessage)
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


class TestAnthropicProviderComplete:
    @pytest.mark.asyncio
    @patch("sage_llm.providers.anthropic.anthropic.AsyncAnthropic")
    async def test_complete_basic(self, mock_cls):
        mock_client = AsyncMock()
        mock_cls.return_value = mock_client
        response = _make_anthropic_response(
            content=[
                anthropic.types.TextBlock(type="text", text="hi"),
            ]
        )
        stream_ctx = MagicMock()
        stream_ctx.__aenter__ = AsyncMock(
            return_value=MagicMock(get_final_message=AsyncMock(return_value=response))
        )
        stream_ctx.__aexit__ = AsyncMock(return_value=None)
        mock_client.messages.stream = MagicMock(return_value=stream_ctx)

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
    @patch("sage_llm.providers.anthropic.anthropic.AsyncAnthropic")
    async def test_parse_uses_tool_trick(self, mock_cls):
        class Answer(BaseModel):
            text: str

        mock_client = AsyncMock()
        mock_cls.return_value = mock_client
        response = _make_anthropic_response(
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
        stream_ctx = MagicMock()
        stream_ctx.__aenter__ = AsyncMock(
            return_value=MagicMock(get_final_message=AsyncMock(return_value=response))
        )
        stream_ctx.__aexit__ = AsyncMock(return_value=None)
        mock_client.messages.stream = MagicMock(return_value=stream_ctx)

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


class TestStrictBoundaryRaises:
    """Behaviors we tightened: malformed inputs raise instead of silently defaulting."""

    def test_tool_choice_none_raises(self):
        with pytest.raises(ValueError, match="tool_choice='none'"):
            _translate_tool_choice("none")

    def test_extract_text_raises_on_unsupported_type(self):
        with pytest.raises(TypeError, match="unsupported content type"):
            _extract_text(42)
        with pytest.raises(TypeError, match="unsupported content type"):
            _extract_text(None)

    def test_extract_text_raises_on_text_part_missing_text_field(self):
        with pytest.raises(KeyError):
            _extract_text([{"type": "text"}])  # missing "text" key

    def test_translate_tool_raises_on_missing_content(self):
        msg: dict = {"role": "tool", "tool_call_id": "abc"}
        with pytest.raises(KeyError):
            _translate_tool(cast(ChatCompletionToolMessageParam, msg))

    def test_translate_tool_raises_on_missing_tool_call_id(self):
        msg: dict = {"role": "tool", "content": "result"}
        with pytest.raises(KeyError):
            _translate_tool(cast(ChatCompletionToolMessageParam, msg))


class TestReasoningEffortDoesNotOverrideMaxTokens:
    """Caller's max_tokens must survive when reasoning_effort is also set."""

    def test_int_reasoning_effort_preserves_max_tokens(self):
        result = _build_kwargs(
            system=anthropic.NOT_GIVEN,
            temperature=None,
            max_tokens=10000,
            top_p=None,
            stop=None,
            tools=None,
            tool_choice=None,
            reasoning_effort=4000,
            model="claude-sonnet-4-5",
        )
        assert result["max_tokens"] == 10000  # not silently set to 2*4000=8000
        assert result["thinking"] == {"type": "enabled", "budget_tokens": 4000}


class TestFinishReasonMapping:
    def test_known_reason_mapped(self):
        resp = _make_anthropic_response(stop_reason="max_tokens")
        msg = _to_anthropic_message(resp, "claude-sonnet-4-5")
        assert msg.completion_info is not None
        assert msg.completion_info.finish_reason == "length"

    def test_unknown_reason_warns_and_defaults_to_stop(self, caplog):
        # "pause_turn" is a valid Anthropic stop_reason but not in our map.
        resp = _make_anthropic_response(stop_reason="pause_turn")
        with caplog.at_level("WARNING", logger="sage_llm.providers.anthropic"):
            msg = _to_anthropic_message(resp, "claude-sonnet-4-5")
        assert msg.completion_info is not None
        assert msg.completion_info.finish_reason == "stop"
        assert any("pause_turn" in r.message for r in caplog.records)


class TestMaxTokensDefault:
    """max_tokens default propagates from acomplete signature into SDK call."""

    @pytest.mark.asyncio
    @patch("sage_llm.providers.anthropic.anthropic.AsyncAnthropic")
    async def test_acomplete_default_max_tokens_reaches_sdk(self, mock_cls):
        mock_client = AsyncMock()
        mock_cls.return_value = mock_client
        response = _make_anthropic_response()
        stream_ctx = MagicMock()
        stream_ctx.__aenter__ = AsyncMock(
            return_value=MagicMock(get_final_message=AsyncMock(return_value=response))
        )
        stream_ctx.__aexit__ = AsyncMock(return_value=None)
        mock_client.messages.stream = MagicMock(return_value=stream_ctx)

        provider = AnthropicProvider(api_key="test-key")
        # Caller omits max_tokens
        await provider.acomplete(
            "claude-sonnet-4-5",
            [{"role": "user", "content": "hi"}],
            trace=LLMTrace(),
        )
        assert mock_client.messages.stream.call_args.kwargs["max_tokens"] == 65536
