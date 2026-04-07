"""Pytest configuration and fixtures for privacy-judge tests."""

import pytest
from sage_llm import SageModelClient


@pytest.fixture(scope="session")
def model_client() -> SageModelClient:
    """Shared model client for all tests.

    Returns:
        A SageModelClient instance shared across the test session.
    """
    return SageModelClient()


@pytest.fixture(scope="session")
def default_model() -> str:
    """Default model for functional tests.

    Returns:
        Model identifier string for functional tests.
    """
    return "trapi/gpt-4.1"
