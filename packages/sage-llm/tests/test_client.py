"""Tests for SageModelClient."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
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


def _make_mock_provider():
    provider = MagicMock()
    msg = OpenAIMessage(
        role="assistant",
        content="hi",
        completion_info=SageChatCompletionInfo(id="x", model="m", finish_reason="stop"),
    )
    provider.acomplete = AsyncMock(return_value=msg)
    provider.aparse = AsyncMock()
    return provider, msg


class TestSageModelClientComplete:
    @pytest.mark.asyncio
    @patch("sage_llm.client.resolve_provider")
    async def test_complete_dispatches(self, mock_resolve):
        _tracer.clear()
        provider, expected_msg = _make_mock_provider()
        mock_resolve.return_value = (provider, "gpt-4o")

        client = SageModelClient()
        msg = await client.acomplete("openai/gpt-4o", [{"role": "user", "content": "hi"}])

        assert msg is expected_msg
        provider.acomplete.assert_called_once()
        traces = _tracer.get_traces()
        assert len(traces) == 1
        assert traces[0].status == "success"

    @pytest.mark.asyncio
    @patch("sage_llm.client.resolve_provider")
    async def test_complete_applies_default_reasoning_effort(self, mock_resolve):
        _tracer.clear()
        provider, _ = _make_mock_provider()
        mock_resolve.return_value = (provider, "gpt-4o")

        client = SageModelClient(reasoning_effort="high")
        await client.acomplete("openai/gpt-4o", [{"role": "user", "content": "hi"}])

        call_kwargs = provider.acomplete.call_args
        assert call_kwargs.kwargs["reasoning_effort"] == "high"

    @pytest.mark.asyncio
    @patch("sage_llm.client.resolve_provider")
    async def test_complete_override_reasoning_effort(self, mock_resolve):
        _tracer.clear()
        provider, _ = _make_mock_provider()
        mock_resolve.return_value = (provider, "gpt-4o")

        client = SageModelClient(reasoning_effort="high")
        await client.acomplete(
            "openai/gpt-4o",
            [{"role": "user", "content": "hi"}],
            reasoning_effort="low",
        )

        call_kwargs = provider.acomplete.call_args
        assert call_kwargs.kwargs["reasoning_effort"] == "low"

    @pytest.mark.asyncio
    @patch("sage_llm.client.resolve_provider")
    async def test_complete_traces_failure(self, mock_resolve):
        _tracer.clear()
        provider = MagicMock()
        provider.acomplete = AsyncMock(side_effect=RuntimeError("boom"))
        mock_resolve.return_value = (provider, "gpt-4o")

        client = SageModelClient()
        try:
            await client.acomplete("openai/gpt-4o", [{"role": "user", "content": "hi"}])
        except RuntimeError:
            pass

        traces = _tracer.get_traces()
        assert len(traces) == 1
        assert traces[0].status == "failure"
        assert traces[0].error == "boom"

    @pytest.mark.asyncio
    @patch("sage_llm.client.resolve_provider")
    async def test_complete_resolves_aliases(self, mock_resolve):
        _tracer.clear()
        provider, _ = _make_mock_provider()
        mock_resolve.return_value = (provider, "claude-sonnet-4-5")

        client = SageModelClient()
        await client.acomplete("claude-sonnet-4.5", [{"role": "user", "content": "hi"}])

        resolved_model = mock_resolve.call_args.args[0]
        assert resolved_model == "anthropic/claude-sonnet-4-5"

    @pytest.mark.asyncio
    @patch("sage_llm.client.resolve_provider")
    async def test_complete_records_sage_request(self, mock_resolve):
        _tracer.clear()
        provider, _ = _make_mock_provider()
        mock_resolve.return_value = (provider, "gpt-4o")

        client = SageModelClient()
        await client.acomplete(
            "openai/gpt-4o",
            [{"role": "user", "content": "hi"}],
            temperature=0.5,
        )

        traces = _tracer.get_traces()
        assert len(traces) == 1
        assert traces[0].sage_request is not None
        assert traces[0].sage_request.model == "openai/gpt-4o"
        assert traces[0].sage_request.temperature == 0.5

    @pytest.mark.asyncio
    @patch("sage_llm.client.resolve_provider")
    async def test_complete_records_sage_response(self, mock_resolve):
        _tracer.clear()
        provider, expected_msg = _make_mock_provider()
        mock_resolve.return_value = (provider, "gpt-4o")

        client = SageModelClient()
        await client.acomplete("openai/gpt-4o", [{"role": "user", "content": "hi"}])

        traces = _tracer.get_traces()
        assert traces[0].sage_response is not None
        assert traces[0].sage_response.content == "hi"


class TestSageModelClientParse:
    @pytest.mark.asyncio
    @patch("sage_llm.client.resolve_provider")
    async def test_parse_delegates(self, mock_resolve):
        class Answer(BaseModel):
            text: str

        provider = MagicMock()
        provider.aparse = AsyncMock(return_value=Answer(text="hello"))
        mock_resolve.return_value = (provider, "gpt-4o")

        client = SageModelClient()
        result = await client.aparse(
            "openai/gpt-4o",
            [{"role": "user", "content": "hi"}],
            Answer,
        )

        assert isinstance(result, Answer)
        assert result.text == "hello"
        provider.aparse.assert_called_once()
