"""Pytest configuration and fixtures for privacy-judge tests."""

import pytest
from srbench_llm import SRBenchModelClient


@pytest.fixture(scope="session")
def model_client() -> SRBenchModelClient:
    """Shared model client for all tests.

    Returns:
        A SRBenchModelClient instance shared across the test session.
    """
    return SRBenchModelClient()


@pytest.fixture(scope="session")
def default_model() -> str:
    """Default model for functional tests.

    Returns:
        Model identifier string for functional tests.
    """
    return "azure_pool/gpt-4.1"
