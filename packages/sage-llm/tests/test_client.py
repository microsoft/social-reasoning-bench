"""Tests for SageModelClient."""

from unittest.mock import MagicMock, patch

from pydantic import BaseModel
from sage_llm.client import SageModelClient, _handle_model_aliases
from sage_llm.providers.openai import OpenAIMessage
from sage_llm.tracing import tracer as _tracer
from sage_llm.types import (
    SageChatCompletionInfo,
    SageChatCompletionMessage,
    SageMessage,
)


class TestHandleModelAliases:
    def test_gemini_prefix(self):
        assert _handle_model_aliases("gemini-2.0-flash") == "gemini/gemini-2.0-flash"

    def test_claude_prefix(self):
        assert _handle_model_aliases("claude-sonnet-4-5") == "anthropic/claude-sonnet-4-5"

    def test_claude_dot_normalization(self):
        assert _handle_model_aliases("claude-sonnet-4.5") == "anthropic/claude-sonnet-4-5"

    def test_already_prefixed_unchanged(self):
        assert _handle_model_aliases("anthropic/claude-sonnet-4-5") == "anthropic/claude-sonnet-4-5"
        assert _handle_model_aliases("openai/gpt-4o") == "openai/gpt-4o"
        assert _handle_model_aliases("gemini/gemini-2.0-flash") == "gemini/gemini-2.0-flash"

    def test_trapi_unchanged(self):
        assert _handle_model_aliases("trapi/gpt-4.1") == "trapi/gpt-4.1"


def _make_mock_provider():
    provider = MagicMock()
    msg = OpenAIMessage(
        role="assistant",
        content="hi",
        completion_info=SageChatCompletionInfo(id="x", model="m", finish_reason="stop"),
    )
    provider.complete.return_value = msg
    provider.acomplete.return_value = msg
    return provider, msg


class TestSageModelClientComplete:
    @patch("sage_llm.client.resolve_provider")
    def test_complete_dispatches(self, mock_resolve):
        _tracer.clear()
        provider, expected_msg = _make_mock_provider()
        mock_resolve.return_value = (provider, "gpt-4o")

        client = SageModelClient()
        msg = client.complete("openai/gpt-4o", [{"role": "user", "content": "hi"}])

        assert msg is expected_msg
        provider.complete.assert_called_once()
        # Trace should have been recorded
        traces = _tracer.get_traces()
        assert len(traces) == 1
        assert traces[0].status == "success"

    @patch("sage_llm.client.resolve_provider")
    def test_complete_applies_default_reasoning_effort(self, mock_resolve):
        _tracer.clear()
        provider, _ = _make_mock_provider()
        mock_resolve.return_value = (provider, "gpt-4o")

        client = SageModelClient(reasoning_effort="high")
        client.complete("openai/gpt-4o", [{"role": "user", "content": "hi"}])

        call_kwargs = provider.complete.call_args
        assert call_kwargs.kwargs["reasoning_effort"] == "high"

    @patch("sage_llm.client.resolve_provider")
    def test_complete_override_reasoning_effort(self, mock_resolve):
        _tracer.clear()
        provider, _ = _make_mock_provider()
        mock_resolve.return_value = (provider, "gpt-4o")

        client = SageModelClient(reasoning_effort="high")
        client.complete(
            "openai/gpt-4o",
            [{"role": "user", "content": "hi"}],
            reasoning_effort="low",
        )

        call_kwargs = provider.complete.call_args
        assert call_kwargs.kwargs["reasoning_effort"] == "low"

    @patch("sage_llm.client.resolve_provider")
    def test_complete_traces_failure(self, mock_resolve):
        _tracer.clear()
        provider = MagicMock()
        provider.complete.side_effect = RuntimeError("boom")
        mock_resolve.return_value = (provider, "gpt-4o")

        client = SageModelClient()
        try:
            client.complete("openai/gpt-4o", [{"role": "user", "content": "hi"}])
        except RuntimeError:
            pass

        traces = _tracer.get_traces()
        assert len(traces) == 1
        assert traces[0].status == "failure"
        assert traces[0].error == "boom"

    @patch("sage_llm.client.resolve_provider")
    def test_complete_resolves_aliases(self, mock_resolve):
        _tracer.clear()
        provider, _ = _make_mock_provider()
        mock_resolve.return_value = (provider, "claude-sonnet-4-5")

        client = SageModelClient()
        client.complete("claude-sonnet-4.5", [{"role": "user", "content": "hi"}])

        resolved_model = mock_resolve.call_args.args[0]
        assert resolved_model == "anthropic/claude-sonnet-4-5"

    @patch("sage_llm.client.resolve_provider")
    def test_complete_records_sage_request(self, mock_resolve):
        _tracer.clear()
        provider, _ = _make_mock_provider()
        mock_resolve.return_value = (provider, "gpt-4o")

        client = SageModelClient()
        client.complete(
            "openai/gpt-4o",
            [{"role": "user", "content": "hi"}],
            temperature=0.5,
        )

        traces = _tracer.get_traces()
        assert len(traces) == 1
        assert traces[0].sage_request is not None
        assert traces[0].sage_request.model == "openai/gpt-4o"
        assert traces[0].sage_request.temperature == 0.5

    @patch("sage_llm.client.resolve_provider")
    def test_complete_records_sage_response(self, mock_resolve):
        _tracer.clear()
        provider, expected_msg = _make_mock_provider()
        mock_resolve.return_value = (provider, "gpt-4o")

        client = SageModelClient()
        client.complete("openai/gpt-4o", [{"role": "user", "content": "hi"}])

        traces = _tracer.get_traces()
        assert traces[0].sage_response is not None
        assert traces[0].sage_response.content == "hi"


class TestSageModelClientParse:
    @patch("sage_llm.client.resolve_provider")
    def test_parse_delegates(self, mock_resolve):
        class Answer(BaseModel):
            text: str

        provider = MagicMock()
        provider.parse.return_value = Answer(text="hello")
        mock_resolve.return_value = (provider, "gpt-4o")

        client = SageModelClient()
        result = client.parse(
            "openai/gpt-4o",
            [{"role": "user", "content": "hi"}],
            Answer,
        )

        assert isinstance(result, Answer)
        assert result.text == "hello"
        provider.parse.assert_called_once()
