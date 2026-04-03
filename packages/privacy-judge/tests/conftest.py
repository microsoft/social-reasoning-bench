"""Pytest configuration and fixtures for privacy-judge tests."""

import pytest
from sage_llm import SageModelClient


@pytest.fixture(scope="session")
def model_client() -> SageModelClient:
    """Shared model client for all tests."""
    return SageModelClient()


@pytest.fixture(scope="session")
def default_model() -> str:
    """Default model for functional tests."""
    return "trapi/gpt-4.1"
