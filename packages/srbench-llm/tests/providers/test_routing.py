"""Tests for provider routing."""

from unittest.mock import patch

from srbench_llm.providers import resolve_provider
from srbench_llm.providers.anthropic import AnthropicProvider
from srbench_llm.providers.azure_openai import AzureProvider
from srbench_llm.providers.google_genai import GoogleProvider
from srbench_llm.providers.openai import OpenAIProvider


class TestResolveProvider:
    def test_anthropic_prefix(self):
        provider, model = resolve_provider("anthropic/claude-sonnet-4-5")
        assert isinstance(provider, AnthropicProvider)
        assert model == "claude-sonnet-4-5"

    @patch("srbench_llm.providers.google_genai.genai.Client")
    def test_gemini_prefix(self, _mock_client):
        provider, model = resolve_provider("gemini/gemini-2.0-flash")
        assert isinstance(provider, GoogleProvider)
        assert model == "gemini-2.0-flash"

    @patch("srbench_llm.providers.openai.openai.OpenAI")
    @patch("srbench_llm.providers.openai.openai.AsyncOpenAI")
    def test_openai_prefix(self, _mock_async, _mock_sync):
        provider, model = resolve_provider("openai/gpt-4o")
        assert isinstance(provider, OpenAIProvider)
        assert model == "gpt-4o"

    @patch("srbench_llm.providers.openai.openai.OpenAI")
    @patch("srbench_llm.providers.openai.openai.AsyncOpenAI")
    def test_bare_model_defaults_to_openai(self, _mock_async, _mock_sync):
        provider, model = resolve_provider("gpt-4o")
        assert isinstance(provider, OpenAIProvider)
        assert model == "gpt-4o"

    @patch("srbench_llm.providers.azure_openai.openai.AzureOpenAI")
    @patch("srbench_llm.providers.azure_openai.openai.AsyncAzureOpenAI")
    def test_azure_prefix(self, _mock_async, _mock_sync):
        provider, model = resolve_provider(
            "azure/my-deployment", base_url="https://x.openai.azure.com"
        )
        assert isinstance(provider, AzureProvider)
        assert model == "my-deployment"

    def test_api_key_forwarded_to_anthropic(self):
        provider, _ = resolve_provider("anthropic/claude-sonnet-4-5", api_key="sk-test")
        assert isinstance(provider, AnthropicProvider)

    @patch("srbench_llm.providers.openai.openai.OpenAI")
    @patch("srbench_llm.providers.openai.openai.AsyncOpenAI")
    def test_api_key_forwarded_to_openai(self, _mock_async, _mock_sync):
        provider, _ = resolve_provider("openai/gpt-4o", api_key="sk-test")
        assert isinstance(provider, OpenAIProvider)
