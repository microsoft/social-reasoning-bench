"""Pytest configuration and fixtures for privacy-judge tests."""

import pytest
from sage_llm import ModelClient


@pytest.fixture(scope="session")
def model_client() -> ModelClient:
    """Shared model client for all tests."""
    return ModelClient()


@pytest.fixture(scope="session")
def default_model() -> str:
    """Default model for functional tests."""
    return "trapi/gpt-4.1"
