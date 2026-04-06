"""Shared test fixtures."""

import pytest
from sage_llm.providers import anthropic as anthropic_mod
from sage_llm.providers import azure_openai, google_genai, openai


@pytest.fixture(autouse=True)
def _clear_provider_caches():
    """Reset module-level client caches so tests are isolated."""
    _clear()
    yield
    _clear()


def _clear():
    for mod in (openai, azure_openai, anthropic_mod, google_genai):
        cache = getattr(mod, "_CLIENT_CACHE", None)
        if cache is not None:
            cache.clear()
