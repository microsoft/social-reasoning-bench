"""Tests for SRBenchChatCompletionMessage and SRBenchChatCompletionInfo types."""

import pytest
from openai.types.completion_usage import CompletionUsage
from srbench_llm.types import SRBenchChatCompletionInfo, SRBenchChatCompletionMessage


class TestSRBenchChatCompletionMessage:
    def test_assistant_message(self):
        msg = SRBenchChatCompletionMessage(role="assistant", content="hi there")
        assert msg.role == "assistant"
        assert msg.content == "hi there"
        assert msg.completion_info is None
        assert msg.tool_calls is None

    def test_rejects_non_assistant_role(self):
        with pytest.raises(Exception):
            SRBenchChatCompletionMessage(role="user", content="hello")  # ty:ignore[invalid-argument-type]

    def test_completion_info_populated(self):
        info = SRBenchChatCompletionInfo(
            id="resp_123",
            model="gpt-4o",
            finish_reason="stop",
            usage=CompletionUsage(prompt_tokens=10, completion_tokens=5, total_tokens=15),
        )
        msg = SRBenchChatCompletionMessage(role="assistant", content="answer", completion_info=info)
        assert msg.completion_info is not None
        assert msg.completion_info.id == "resp_123"
        assert msg.completion_info.model == "gpt-4o"
        assert msg.completion_info.finish_reason == "stop"
        assert msg.completion_info.usage is not None
        assert msg.completion_info.usage.prompt_tokens == 10

    def test_model_dump_excludes_completion_info(self):
        info = SRBenchChatCompletionInfo(id="x", model="m", finish_reason="stop")
        msg = SRBenchChatCompletionMessage(role="assistant", content="hi", completion_info=info)
        d = msg.model_dump(exclude_none=True, exclude={"completion_info"})
        assert "completion_info" not in d
        assert d["role"] == "assistant"
        assert d["content"] == "hi"

    def test_model_dump_excludes_none_fields(self):
        msg = SRBenchChatCompletionMessage(role="assistant", content="hello")
        d = msg.model_dump(exclude_none=True)
        assert "tool_calls" not in d
        assert "refusal" not in d

    def test_validate_from_dict(self):
        msg = SRBenchChatCompletionMessage.model_validate(
            {"role": "assistant", "content": "from dict"}
        )
        assert msg.role == "assistant"
        assert msg.content == "from dict"
        assert msg.completion_info is None

    def test_isinstance_chain(self):
        from srbench_llm.providers.anthropic import AnthropicMessage
        from srbench_llm.providers.google_genai import GoogleMessage
        from srbench_llm.providers.openai import OpenAIMessage

        openai_msg = OpenAIMessage(role="assistant", content="hi")
        anthropic_msg = AnthropicMessage(role="assistant", content="hi")
        google_msg = GoogleMessage(role="assistant", content="hi")

        assert isinstance(openai_msg, SRBenchChatCompletionMessage)
        assert isinstance(anthropic_msg, SRBenchChatCompletionMessage)
        assert isinstance(google_msg, SRBenchChatCompletionMessage)


class TestSRBenchChatCompletionInfo:
    def test_basic_creation(self):
        info = SRBenchChatCompletionInfo(id="abc", model="gpt-4o", finish_reason="stop")
        assert info.id == "abc"
        assert info.model == "gpt-4o"
        assert info.finish_reason == "stop"
        assert info.usage is None

    def test_with_usage(self):
        usage = CompletionUsage(prompt_tokens=100, completion_tokens=50, total_tokens=150)
        info = SRBenchChatCompletionInfo(id="abc", model="gpt-4o", finish_reason="stop", usage=usage)
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
