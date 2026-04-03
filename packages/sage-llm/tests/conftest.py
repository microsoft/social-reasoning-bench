"""Shared test fixtures."""

import pytest
from sage_llm.providers import anthropic as anthropic_mod
from sage_llm.providers import azure_openai, google_genai, openai


@pytest.fixture(autouse=True)
def _clear_provider_caches():
    """Reset per-thread client caches so tests are isolated."""
    _clear()
    yield
    _clear()


def _clear():
    for attr in ("openai_clients",):
        tl = getattr(openai, "_thread_local", None)
        if tl is not None and hasattr(tl, attr):
            delattr(tl, attr)
    for attr in ("azure_clients",):
        tl = getattr(azure_openai, "_thread_local", None)
        if tl is not None and hasattr(tl, attr):
            delattr(tl, attr)
    for attr in ("anthropic_clients",):
        tl = getattr(anthropic_mod, "_thread_local", None)
        if tl is not None and hasattr(tl, attr):
            delattr(tl, attr)
    for attr in ("google_clients",):
        tl = getattr(google_genai, "_thread_local", None)
        if tl is not None and hasattr(tl, attr):
            delattr(tl, attr)
