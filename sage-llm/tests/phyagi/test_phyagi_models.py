"""
Test TRAPI models connectivity via the custom LiteLLM provider.

Run with: pytest tests/trapi/test_trapi_models.py -v

Tests that models are accessible through the TRAPI provider using the /v1 endpoint.
"""

import os

import pytest
from sage_llm.client import ModelClient
from sage_llm.phyagi import API_KEY_ENV

# Models to test (model name format, not deployment names)
MODELS = ["gpt-4o", "gpt-5"]

# Skip all tests if API key is not set
pytestmark = pytest.mark.skipif(
    os.getenv(API_KEY_ENV) is None, reason=f"{API_KEY_ENV} environment variable not set"
)


@pytest.fixture(scope="module")
def client():
    """Create a ModelClient once per module."""
    return ModelClient()


@pytest.mark.parametrize("model", MODELS)
def test_phyagi_models(client: ModelClient, model: str):
    """Test that each TRAPI model is accessible via the custom provider with the API path"""
    try:
        response = client.chat.completions.create(
            model=f"phyagi/{model}",
            messages=[{"role": "user", "content": "Say 'ok'"}],
            timeout=10,
        )
        assert response.choices[0].message.content is not None
        print(f"\n✓ {model} works")
    except Exception as e:
        error_msg = str(e)
        pytest.fail(f"Failed: {error_msg[:200]}")
