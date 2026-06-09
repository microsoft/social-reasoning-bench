"""Tests for the Azure provider."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from openai.types.chat import ChatCompletion, ChatCompletionMessage
from openai.types.chat.chat_completion import Choice
from openai.types.completion_usage import CompletionUsage
from srbench_llm.providers.azure_openai import AzureProvider
from srbench_llm.providers.openai import OpenAIMessage
from srbench_llm.tracing import LLMTrace


def _make_chat_completion(content="Hello!") -> ChatCompletion:
    return ChatCompletion(
        id="chatcmpl-az-123",
        choices=[
            Choice(
                index=0,
                finish_reason="stop",
                message=ChatCompletionMessage(role="assistant", content=content),
            )
        ],
        created=1700000000,
        model="gpt-4.1",
        object="chat.completion",
        usage=CompletionUsage(prompt_tokens=10, completion_tokens=5, total_tokens=15),
    )


class TestAzureProviderComplete:
    @pytest.mark.asyncio
    @patch("srbench_llm.providers.azure_openai.openai.AsyncAzureOpenAI")
    async def test_complete_basic(self, mock_cls):
        mock_client = AsyncMock()
        mock_cls.return_value = mock_client
        mock_client.chat.completions.create.return_value = _make_chat_completion("hi")

        provider = AzureProvider(
            azure_endpoint="https://test.openai.azure.com",
            api_key="test-key",
        )
        trace = LLMTrace()
        msg = await provider.acomplete(
            "gpt-4.1",
            [{"role": "user", "content": "hello"}],
            trace=trace,
        )

        assert isinstance(msg, OpenAIMessage)
        assert msg.content == "hi"
        assert trace.provider_name == "azure_openai"

    @pytest.mark.asyncio
    @patch("srbench_llm.providers.azure_openai.openai.AsyncAzureOpenAI")
    async def test_default_no_retries(self, mock_cls):
        mock_client = AsyncMock()
        mock_cls.return_value = mock_client
        mock_client.chat.completions.create.return_value = _make_chat_completion()

        provider = AzureProvider(azure_endpoint="https://test.openai.azure.com")
        trace = LLMTrace()
        await provider.acomplete("gpt-4.1", [{"role": "user", "content": "hi"}], trace=trace)
        assert mock_client.chat.completions.create.call_count == 1

    @patch("srbench_llm.providers.azure_openai.openai.AsyncAzureOpenAI")
    def test_api_version_default(self, mock_async_cls):
        AzureProvider(azure_endpoint="https://test.openai.azure.com")
        call_kwargs = mock_async_cls.call_args.kwargs
        assert "api_version" in call_kwargs

    @patch("srbench_llm.providers.azure_openai.openai.AsyncAzureOpenAI")
    def test_token_provider_passed(self, mock_async_cls):
        token_fn = lambda: "token123"  # noqa: E731
        AzureProvider(
            azure_endpoint="https://test.openai.azure.com",
            azure_ad_token_provider=token_fn,
        )
        call_kwargs = mock_async_cls.call_args.kwargs
        assert call_kwargs["azure_ad_token_provider"] is token_fn
