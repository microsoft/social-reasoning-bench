"""
Test TRAPI models connectivity via the custom LiteLLM provider.

Run with: pytest tests/trapi/test_trapi_models.py -v

Tests that models are accessible through the TRAPI provider using the /v1 endpoint.
"""

import pytest
from sage_llm.client import ModelClient
from sage_llm.trapi import DEPLOYMENTS

# Models to test (model name format, not deployment names)
MODELS = list(DEPLOYMENTS.keys())

API_PATH = "msraif/shared"


@pytest.fixture(scope="module")
def client():
    """Create a ModelClient once per module."""
    return ModelClient()


@pytest.mark.parametrize("model", MODELS)
def test_trapi_model_fullname(client: ModelClient, model: str):
    """Test that each TRAPI model is accessible via the custom provider with the API path"""
    try:
        response = client.chat.completions.create(
            model=f"trapi/{API_PATH}/{model}",
            messages=[{"role": "user", "content": "Say 'ok'"}],
            timeout=10,
        )
        assert response.choices[0].message.content is not None
        print(f"\n✓ {model} works")
    except Exception as e:
        error_msg = str(e)
        pytest.fail(f"Failed: {error_msg[:200]}")


@pytest.mark.parametrize("model", MODELS)
def test_trapi_model_shortname(client: ModelClient, model: str):
    """Test that each TRAPI model is accessible via the custom provider without the API path"""
    try:
        response = client.chat.completions.create(
            model=f"trapi/{model}",
            messages=[{"role": "user", "content": "Say 'ok'"}],
            timeout=10,
        )
        assert response.choices[0].message.content is not None
        print(f"\n✓ {model} works")
    except Exception as e:
        error_msg = str(e)
        pytest.fail(f"Failed: {error_msg[:200]}")
