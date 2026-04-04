"""Tests for the Google provider."""

import json
from typing import cast
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from google.genai import types
from openai.types.chat import (
    ChatCompletionFunctionToolParam,
    ChatCompletionToolMessageParam,
    ChatCompletionToolParam,
)
from openai.types.chat.chat_completion_message_tool_call import (
    ChatCompletionMessageToolCall,
    Function,
)
from openai.types.shared_params import FunctionDefinition
from pydantic import BaseModel
from sage_llm.providers.google_genai import (
    GoogleMessage,
    GoogleProvider,
    _build_config,
    _json_schema_to_google_schema,
    _to_google_message,
    _translate_request,
    _translate_tool_choice,
    _translate_tool_result,
    _translate_tools,
)
from sage_llm.tracing import LLMTrace
from sage_llm.types import SageChatCompletionMessage, SageMessage


def _make_google_response(
    text: str = "Hello!",
    thought_text: str | None = None,
    function_call: types.FunctionCall | None = None,
    finish_reason: types.FinishReason = types.FinishReason.STOP,
) -> types.GenerateContentResponse:
    parts = []
    if thought_text:
        parts.append(types.Part(text=thought_text, thought=True))
    if function_call:
        parts.append(types.Part(function_call=function_call))
    if text:
        parts.append(types.Part(text=text))

    return types.GenerateContentResponse(
        candidates=[
            types.Candidate(
                content=types.Content(role="model", parts=parts),
                finish_reason=finish_reason,
            )
        ],
        usage_metadata=types.GenerateContentResponseUsageMetadata(
            prompt_token_count=10,
            candidates_token_count=5,
            total_token_count=15,
        ),
        model_version="gemini-2.0-flash",
    )


class TestTranslateRequest:
    def test_system_extracted(self):
        msgs: list[SageMessage] = [
            {"role": "system", "content": "be helpful"},
            {"role": "user", "content": "hi"},
        ]
        raw_contents, config = _translate_request(msgs)
        assert isinstance(raw_contents, list)
        assert len(raw_contents) == 1  # system not in contents
        assert config.system_instruction == "be helpful"

    def test_user_message(self):
        msgs: list[SageMessage] = [{"role": "user", "content": "hello"}]
        raw_contents, _ = _translate_request(msgs)
        assert isinstance(raw_contents, list)
        contents = cast(list[types.Content], raw_contents)
        assert len(contents) == 1
        assert contents[0].role == "user"
        assert contents[0].parts is not None
        assert contents[0].parts[0].text == "hello"

    def test_assistant_message(self):
        msgs: list[SageMessage] = [SageChatCompletionMessage(role="assistant", content="reply")]
        raw_contents, _ = _translate_request(msgs)
        assert isinstance(raw_contents, list)
        contents = cast(list[types.Content], raw_contents)
        assert contents[0].role == "model"

    def test_thought_parts_injected(self):
        msgs: list[SageMessage] = [
            GoogleMessage(
                role="assistant",
                content="answer",
                thought_parts=[{"text": "thinking...", "thought": True}],
            )
        ]
        raw_contents, _ = _translate_request(msgs)
        assert isinstance(raw_contents, list)
        contents = cast(list[types.Content], raw_contents)
        parts = contents[0].parts
        assert parts is not None
        assert parts[0].thought is True
        assert parts[1].text == "answer"


def _tool_msg(content: str, tool_call_id: str, **extra: str) -> ChatCompletionToolMessageParam:
    """Build a tool message dict with proper typing."""
    return cast(
        ChatCompletionToolMessageParam,
        {"role": "tool", "content": content, "tool_call_id": tool_call_id, **extra},
    )


def _get_fr(content: types.Content, index: int = 0) -> types.FunctionResponse:
    """Extract a FunctionResponse from Content, with assertions."""
    assert content.parts is not None
    fr = content.parts[index].function_response
    assert fr is not None
    return fr


class TestTranslateToolResult:
    def test_dict_result(self):
        msg = _tool_msg('{"temp": 72}', "1", name="get_weather")
        content = _translate_tool_result(msg)
        fr = _get_fr(content)
        assert fr.name == "get_weather"
        assert fr.response == {"temp": 72}

    def test_string_result_wrapped(self):
        """json.loads returns a str — must be wrapped in a dict."""
        msg = _tool_msg('"sunny"', "1", name="get_weather")
        content = _translate_tool_result(msg)
        assert _get_fr(content).response == {"result": "sunny"}

    def test_list_result_wrapped(self):
        """json.loads returns a list — must be wrapped in a dict."""
        msg = _tool_msg("[1, 2, 3]", "1", name="sum")
        content = _translate_tool_result(msg)
        assert _get_fr(content).response == {"result": [1, 2, 3]}

    def test_int_result_wrapped(self):
        msg = _tool_msg("42", "1", name="compute")
        content = _translate_tool_result(msg)
        assert _get_fr(content).response == {"result": 42}

    def test_plain_text_fallback(self):
        """Non-JSON content goes through except branch."""
        msg = _tool_msg("not json", "1", name="foo")
        content = _translate_tool_result(msg)
        assert _get_fr(content).response == {"result": "not json"}

    def test_null_result_wrapped(self):
        msg = _tool_msg("null", "1", name="noop")
        content = _translate_tool_result(msg)
        assert _get_fr(content).response == {"result": None}

    def test_bool_result_wrapped(self):
        msg = _tool_msg("true", "1", name="check")
        content = _translate_tool_result(msg)
        assert _get_fr(content).response == {"result": True}

    def test_name_resolved_from_lookup(self):
        """When 'name' is absent, resolve via tc_id_to_name lookup."""
        msg = _tool_msg('{"ok": true}', "call_123")
        lookup = {"call_123": "get_weather"}
        content = _translate_tool_result(msg, lookup)
        assert _get_fr(content).name == "get_weather"

    def test_name_from_lookup_without_explicit_name(self):
        """tool_call_id present but no 'name' key at all."""
        msg = _tool_msg("result text", "call_456")
        lookup = {"call_456": "search"}
        content = _translate_tool_result(msg, lookup)
        assert _get_fr(content).name == "search"


class TestTranslateRequestToolNameResolution:
    """Test that _translate_request resolves tool names from preceding assistant messages."""

    def test_tool_name_resolved_from_assistant_tool_calls(self):
        """Tool message without 'name' gets name from the assistant's tool_calls."""
        assistant_msg = SageChatCompletionMessage(
            role="assistant",
            content=None,
            tool_calls=[
                ChatCompletionMessageToolCall(
                    id="call_abc",
                    type="function",
                    function=Function(name="get_weather", arguments='{"city": "Seattle"}'),
                )
            ],
        )
        tool_msg = _tool_msg('{"temp": 55}', "call_abc")
        msgs: list[SageMessage] = [
            {"role": "user", "content": "What's the weather?"},
            assistant_msg,
            tool_msg,
        ]
        raw_contents, _ = _translate_request(msgs)
        contents = cast(list[types.Content], raw_contents)
        # contents[0] = user, contents[1] = assistant, contents[2] = tool
        fr = _get_fr(contents[2])
        assert fr.name == "get_weather"

    def test_multiple_tool_calls_resolved(self):
        """Multiple tool calls in one assistant message all get resolved."""
        assistant_msg = SageChatCompletionMessage(
            role="assistant",
            content=None,
            tool_calls=[
                ChatCompletionMessageToolCall(
                    id="call_1",
                    type="function",
                    function=Function(name="get_weather", arguments="{}"),
                ),
                ChatCompletionMessageToolCall(
                    id="call_2",
                    type="function",
                    function=Function(name="get_time", arguments="{}"),
                ),
            ],
        )
        msgs: list[SageMessage] = [
            {"role": "user", "content": "hi"},
            assistant_msg,
            _tool_msg("sunny", "call_1"),
            _tool_msg("3pm", "call_2"),
        ]
        raw_contents, _ = _translate_request(msgs)
        contents = cast(list[types.Content], raw_contents)
        assert _get_fr(contents[2]).name == "get_weather"
        assert _get_fr(contents[3]).name == "get_time"


class TestBuildConfig:
    def test_basic_params(self):
        config = _build_config(
            system_instruction="sys",
            temperature=0.5,
            max_tokens=1000,
            top_p=None,
            stop=None,
            tools=None,
            tool_choice=None,
            reasoning_effort=None,
            response_format=None,
        )
        assert config.system_instruction == "sys"
        assert config.temperature == 0.5
        assert config.max_output_tokens == 1000

    def test_thinking_config(self):
        config = _build_config(
            system_instruction=None,
            temperature=None,
            max_tokens=None,
            top_p=None,
            stop=None,
            tools=None,
            tool_choice=None,
            reasoning_effort=4000,
            response_format=None,
        )
        assert config.thinking_config is not None
        assert config.thinking_config.thinking_budget == 4000

    def test_response_format(self):
        class MyModel(BaseModel):
            name: str

        config = _build_config(
            system_instruction=None,
            temperature=None,
            max_tokens=None,
            top_p=None,
            stop=None,
            tools=None,
            tool_choice=None,
            reasoning_effort=None,
            response_format=MyModel,
        )
        assert config.response_mime_type == "application/json"
        assert config.response_schema is not None


class TestTranslateTools:
    def test_function_tools(self):
        params: dict[str, object] = {
            "type": "object",
            "properties": {"q": {"type": "string"}},
        }
        openai_tools: list[ChatCompletionToolParam] = [
            ChatCompletionFunctionToolParam(
                type="function",
                function=FunctionDefinition(
                    name="search",
                    description="Search the web",
                    parameters=params,
                ),
            )
        ]
        result = _translate_tools(openai_tools)
        assert len(result) == 1
        decls = result[0].function_declarations
        assert decls is not None
        assert len(decls) == 1
        assert decls[0].name == "search"


class TestJsonSchemaToGoogleSchema:
    def test_basic_object(self):
        schema = {
            "type": "object",
            "properties": {"x": {"type": "string"}},
            "required": ["x"],
        }
        result = _json_schema_to_google_schema(schema)
        assert isinstance(result, types.Schema)
        assert result.type == types.Type.OBJECT
        assert result.properties is not None
        assert "x" in result.properties
        assert result.required == ["x"]

    def test_strips_unsupported_keys(self):
        schema = {
            "type": "object",
            "properties": {"x": {"type": "string"}},
            "additionalProperties": False,
            "exclusiveMinimum": 0,
        }
        # Should not raise — unsupported keys are silently dropped
        result = _json_schema_to_google_schema(schema)
        assert result.type == types.Type.OBJECT

    def test_inlines_refs(self):
        schema = {
            "type": "object",
            "properties": {
                "addr": {"$ref": "#/$defs/Address"},
            },
            "$defs": {
                "Address": {
                    "type": "object",
                    "properties": {"city": {"type": "string"}},
                }
            },
        }
        result = _json_schema_to_google_schema(schema)
        assert result.properties is not None
        addr = result.properties["addr"]
        assert addr.type == types.Type.OBJECT
        assert addr.properties is not None
        assert "city" in addr.properties

    def test_nested_refs(self):
        schema = {
            "type": "object",
            "properties": {"person": {"$ref": "#/$defs/Person"}},
            "$defs": {
                "Person": {
                    "type": "object",
                    "properties": {"addr": {"$ref": "#/$defs/Address"}},
                },
                "Address": {
                    "type": "object",
                    "properties": {"zip": {"type": "string"}},
                },
            },
        }
        result = _json_schema_to_google_schema(schema)
        assert result.properties is not None
        person = result.properties["person"]
        assert person.properties is not None
        addr = person.properties["addr"]
        assert addr.properties is not None
        assert "zip" in addr.properties

    def test_filters_empty_enum_strings(self):
        schema = {"type": "string", "enum": ["yes", "", "no", ""]}
        result = _json_schema_to_google_schema(schema)
        assert result.enum == ["yes", "no"]

    def test_anyof(self):
        schema = {
            "anyOf": [
                {"type": "string"},
                {"type": "null"},
            ]
        }
        result = _json_schema_to_google_schema(schema)
        assert result.any_of is not None
        assert len(result.any_of) == 2

    def test_numeric_constraints(self):
        schema = {
            "type": "number",
            "minimum": 0,
            "maximum": 100,
            "exclusiveMinimum": 0,  # unsupported — dropped
        }
        result = _json_schema_to_google_schema(schema)
        assert result.minimum == 0
        assert result.maximum == 100

    def test_array_with_items(self):
        schema = {
            "type": "array",
            "items": {"type": "string"},
        }
        result = _json_schema_to_google_schema(schema)
        assert result.type == types.Type.ARRAY
        assert result.items is not None
        assert result.items.type == types.Type.STRING


class TestTranslateToolChoice:
    def test_auto(self):
        assert _translate_tool_choice("auto") is None

    def test_none(self):
        result = _translate_tool_choice("none")
        assert result is not None


class TestToGoogleMessage:
    def test_text_response(self):
        resp = _make_google_response(text="Hello!")
        msg = _to_google_message(resp, "gemini-2.0-flash")

        assert isinstance(msg, GoogleMessage)
        assert isinstance(msg, SageChatCompletionMessage)
        assert msg.role == "assistant"
        assert msg.content == "Hello!"
        assert msg.thought_parts is None
        assert msg.completion_info is not None

    def test_thought_parts_preserved(self):
        resp = _make_google_response(text="answer", thought_text="let me think")
        msg = _to_google_message(resp, "gemini-2.0-flash")

        assert msg.content == "answer"
        assert msg.thought_parts is not None
        assert len(msg.thought_parts) == 1
        assert msg.thought_parts[0]["text"] == "let me think"
        assert msg.thought_parts[0]["thought"] is True

    def test_function_call_response(self):
        fc = types.FunctionCall(name="search", args={"q": "test"})
        resp = _make_google_response(text="", function_call=fc)
        msg = _to_google_message(resp, "gemini-2.0-flash")

        assert msg.tool_calls is not None
        assert len(msg.tool_calls) == 1
        tc = msg.tool_calls[0]
        assert isinstance(tc, ChatCompletionMessageToolCall)
        assert tc.function.name == "search"
        assert json.loads(tc.function.arguments) == {"q": "test"}

    def test_usage_mapped(self):
        resp = _make_google_response()
        msg = _to_google_message(resp, "gemini-2.0-flash")

        assert msg.completion_info is not None
        assert msg.completion_info.usage is not None
        assert msg.completion_info.usage.prompt_tokens == 10
        assert msg.completion_info.usage.completion_tokens == 5


class TestGoogleProviderComplete:
    @patch("sage_llm.providers.google_genai.genai.Client")
    def test_complete_basic(self, mock_cls):
        mock_client = MagicMock()
        mock_cls.return_value = mock_client
        mock_client.models.generate_content.return_value = _make_google_response(text="hi")

        provider = GoogleProvider(api_key="test-key")
        trace = LLMTrace()
        msg = provider.complete(
            "gemini-2.0-flash",
            [{"role": "user", "content": "hello"}],
            trace=trace,
            temperature=0.5,
        )

        assert isinstance(msg, GoogleMessage)
        assert msg.content == "hi"
        assert trace.provider_name == "google"

    @patch("sage_llm.providers.google_genai.genai.Client")
    def test_parse_uses_json_mode(self, mock_cls):
        class Answer(BaseModel):
            text: str

        mock_client = MagicMock()
        mock_cls.return_value = mock_client
        mock_client.models.generate_content.return_value = _make_google_response(
            text='{"text": "hello"}'
        )

        provider = GoogleProvider()
        result = provider.parse(
            "gemini-2.0-flash",
            [{"role": "user", "content": "hi"}],
            Answer,
        )

        assert isinstance(result, Answer)
        assert result.text == "hello"
        call_kwargs = mock_client.models.generate_content.call_args
        config = call_kwargs.kwargs["config"]
        assert config.response_mime_type == "application/json"
