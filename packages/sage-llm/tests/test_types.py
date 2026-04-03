"""Tests for SageChatCompletionMessage and SageChatCompletionInfo types."""

import pytest
from openai.types.completion_usage import CompletionUsage
from sage_llm.types import SageChatCompletionInfo, SageChatCompletionMessage


class TestSageChatCompletionMessage:
    def test_assistant_message(self):
        msg = SageChatCompletionMessage(role="assistant", content="hi there")
        assert msg.role == "assistant"
        assert msg.content == "hi there"
        assert msg.completion_info is None
        assert msg.tool_calls is None

    def test_rejects_non_assistant_role(self):
        with pytest.raises(Exception):
            SageChatCompletionMessage(role="user", content="hello")  # ty:ignore[invalid-argument-type]

    def test_completion_info_populated(self):
        info = SageChatCompletionInfo(
            id="resp_123",
            model="gpt-4o",
            finish_reason="stop",
            usage=CompletionUsage(prompt_tokens=10, completion_tokens=5, total_tokens=15),
        )
        msg = SageChatCompletionMessage(role="assistant", content="answer", completion_info=info)
        assert msg.completion_info is not None
        assert msg.completion_info.id == "resp_123"
        assert msg.completion_info.model == "gpt-4o"
        assert msg.completion_info.finish_reason == "stop"
        assert msg.completion_info.usage is not None
        assert msg.completion_info.usage.prompt_tokens == 10

    def test_model_dump_excludes_completion_info(self):
        info = SageChatCompletionInfo(id="x", model="m", finish_reason="stop")
        msg = SageChatCompletionMessage(role="assistant", content="hi", completion_info=info)
        d = msg.model_dump(exclude_none=True, exclude={"completion_info"})
        assert "completion_info" not in d
        assert d["role"] == "assistant"
        assert d["content"] == "hi"

    def test_model_dump_excludes_none_fields(self):
        msg = SageChatCompletionMessage(role="assistant", content="hello")
        d = msg.model_dump(exclude_none=True)
        assert "tool_calls" not in d
        assert "refusal" not in d

    def test_validate_from_dict(self):
        msg = SageChatCompletionMessage.model_validate(
            {"role": "assistant", "content": "from dict"}
        )
        assert msg.role == "assistant"
        assert msg.content == "from dict"
        assert msg.completion_info is None

    def test_isinstance_chain(self):
        from sage_llm.providers.anthropic import AnthropicMessage
        from sage_llm.providers.google_genai import GoogleMessage
        from sage_llm.providers.openai import OpenAIMessage

        openai_msg = OpenAIMessage(role="assistant", content="hi")
        anthropic_msg = AnthropicMessage(role="assistant", content="hi")
        google_msg = GoogleMessage(role="assistant", content="hi")

        assert isinstance(openai_msg, SageChatCompletionMessage)
        assert isinstance(anthropic_msg, SageChatCompletionMessage)
        assert isinstance(google_msg, SageChatCompletionMessage)


class TestSageChatCompletionInfo:
    def test_basic_creation(self):
        info = SageChatCompletionInfo(id="abc", model="gpt-4o", finish_reason="stop")
        assert info.id == "abc"
        assert info.model == "gpt-4o"
        assert info.finish_reason == "stop"
        assert info.usage is None

    def test_with_usage(self):
        usage = CompletionUsage(prompt_tokens=100, completion_tokens=50, total_tokens=150)
        info = SageChatCompletionInfo(id="abc", model="gpt-4o", finish_reason="stop", usage=usage)
        assert info.usage is not None
        assert info.usage.total_tokens == 150


class TestInputMessages:
    """Input messages (user/system/tool) are plain dicts (ChatCompletionMessageParam)."""

    def test_user_message_is_dict(self):
        msg = {"role": "user", "content": "hello"}
        assert msg["role"] == "user"

    def test_tool_message_has_tool_call_id(self):
        msg = {"role": "tool", "content": '{"result": 42}', "tool_call_id": "call_1"}
        assert msg["tool_call_id"] == "call_1"
