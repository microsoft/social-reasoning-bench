"""Tests for per-thread SDK client caching.

Each provider should cache one SDK client per unique config per thread,
avoiding connection pool exhaustion under concurrent load.
"""

from unittest.mock import MagicMock, patch

from sage_llm.providers.anthropic import AnthropicProvider
from sage_llm.providers.azure_openai import AzureProvider
from sage_llm.providers.google_genai import GoogleProvider
from sage_llm.providers.openai import OpenAIProvider


def _unique(**_kw: object) -> MagicMock:
    return MagicMock()


class TestOpenAICaching:
    @patch("sage_llm.providers.openai.openai.OpenAI")
    @patch("sage_llm.providers.openai.openai.AsyncOpenAI")
    def test_same_params_reuse_client(self, _mock_async, _mock_sync):
        p1 = OpenAIProvider(api_key="k1")
        p2 = OpenAIProvider(api_key="k1")
        assert p1._client is p2._client
        assert p1._async_client is p2._async_client
        assert _mock_sync.call_count == 1

    @patch("sage_llm.providers.openai.openai.OpenAI", side_effect=_unique)
    @patch("sage_llm.providers.openai.openai.AsyncOpenAI", side_effect=_unique)
    def test_different_params_separate_clients(self, _mock_async, _mock_sync):
        p1 = OpenAIProvider(api_key="k1")
        p2 = OpenAIProvider(api_key="k2")
        assert p1._client is not p2._client

    @patch("sage_llm.providers.openai.openai.OpenAI")
    @patch("sage_llm.providers.openai.openai.AsyncOpenAI")
    def test_many_providers_one_client(self, _mock_async, _mock_sync):
        providers = [OpenAIProvider(api_key="shared") for _ in range(100)]
        for p in providers:
            assert p._client is providers[0]._client
        assert _mock_sync.call_count == 1


class TestAzureCaching:
    @patch("sage_llm.providers.azure_openai.openai.AzureOpenAI")
    @patch("sage_llm.providers.azure_openai.openai.AsyncAzureOpenAI")
    def test_same_params_reuse_client(self, _mock_async, _mock_sync):
        p1 = AzureProvider(azure_endpoint="https://a.openai.azure.com", api_key="k")
        p2 = AzureProvider(azure_endpoint="https://a.openai.azure.com", api_key="k")
        assert p1._client is p2._client
        assert _mock_sync.call_count == 1

    @patch("sage_llm.providers.azure_openai.openai.AzureOpenAI", side_effect=_unique)
    @patch("sage_llm.providers.azure_openai.openai.AsyncAzureOpenAI", side_effect=_unique)
    def test_different_params_separate_clients(self, _mock_async, _mock_sync):
        p1 = AzureProvider(azure_endpoint="https://a.openai.azure.com")
        p2 = AzureProvider(azure_endpoint="https://b.openai.azure.com")
        assert p1._client is not p2._client

    @patch("sage_llm.providers.azure_openai.openai.AzureOpenAI")
    @patch("sage_llm.providers.azure_openai.openai.AsyncAzureOpenAI")
    def test_same_token_provider_reuses(self, _mock_async, _mock_sync):
        token_fn = lambda: "token"  # noqa: E731
        p1 = AzureProvider(
            azure_endpoint="https://a.openai.azure.com", azure_ad_token_provider=token_fn
        )
        p2 = AzureProvider(
            azure_endpoint="https://a.openai.azure.com", azure_ad_token_provider=token_fn
        )
        assert p1._client is p2._client
        assert _mock_sync.call_count == 1


class TestAnthropicCaching:
    def test_same_params_reuse_client(self):
        p1 = AnthropicProvider(api_key="k1")
        p2 = AnthropicProvider(api_key="k1")
        assert p1._client is p2._client
        assert p1._async_client is p2._async_client

    def test_different_params_separate_clients(self):
        p1 = AnthropicProvider(api_key="k1")
        p2 = AnthropicProvider(api_key="k2")
        assert p1._client is not p2._client


class TestGoogleCaching:
    @patch("sage_llm.providers.google_genai.genai.Client")
    def test_same_params_reuse_client(self, mock_cls):
        p1 = GoogleProvider(api_key="k1")
        p2 = GoogleProvider(api_key="k1")
        assert p1._client is p2._client
        assert mock_cls.call_count == 1

    @patch("sage_llm.providers.google_genai.genai.Client", side_effect=_unique)
    def test_different_params_separate_clients(self, mock_cls):
        p1 = GoogleProvider(api_key="k1")
        p2 = GoogleProvider(api_key="k2")
        assert p1._client is not p2._client

    @patch("sage_llm.providers.google_genai.genai.Client")
    def test_many_providers_one_client(self, mock_cls):
        providers = [GoogleProvider(api_key="shared") for _ in range(100)]
        for p in providers:
            assert p._client is providers[0]._client
        assert mock_cls.call_count == 1


class TestResolveProviderCaching:
    @patch("sage_llm.providers.openai.openai.OpenAI")
    @patch("sage_llm.providers.openai.openai.AsyncOpenAI")
    def test_resolve_reuses_client(self, _mock_async, _mock_sync):
        from sage_llm.providers import resolve_provider

        p1, _ = resolve_provider("openai/gpt-4o", api_key="test")
        p2, _ = resolve_provider("openai/gpt-4o", api_key="test")
        assert isinstance(p1, OpenAIProvider) and isinstance(p2, OpenAIProvider)
        assert p1._client is p2._client
        assert _mock_sync.call_count == 1
