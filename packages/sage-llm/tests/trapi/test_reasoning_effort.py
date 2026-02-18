"""
Test TRAPI models connectivity via the custom LiteLLM provider.

Run with: pytest tests/trapi/test_trapi_models.py -v

Tests that models are accessible through the TRAPI provider using the /v1 endpoint.
"""

import pytest
from sage_llm.client import ModelClient
from sage_llm.trapi import DEPLOYMENTS


@pytest.fixture(scope="module")
def client():
    """Create a ModelClient once per module."""
    return ModelClient()


def test_reasoning_effort_returns_thinking_tokens(client: ModelClient):
    """Test that reasoning_effort param returns usage with thinking/reasoning tokens."""
    response = client.chat.completions.create(
        model=f"trapi/gpt-5.2",
        messages=[{"role": "user", "content": "Prove 2+2 from the axioms of set theory."}],
        reasoning_effort="low",
        timeout=30,
    )

    assert response.choices[0].message.content is not None
    assert response.usage is not None

    # Check for reasoning/thinking tokens in usage
    usage = response.usage
    if hasattr(usage, "completion_tokens_details") and usage.completion_tokens_details:
        details = usage.completion_tokens_details
        reasoning_tokens = getattr(details, "reasoning_tokens", None)
        assert reasoning_tokens is not None and reasoning_tokens > 0, (
            f"Expected reasoning_tokens > 0, got: {reasoning_tokens}"
        )
        print(f"\n✓ reasoning_tokens: {reasoning_tokens}")
    else:
        pytest.fail(f"No reasoning tokens in usage: {usage}")
