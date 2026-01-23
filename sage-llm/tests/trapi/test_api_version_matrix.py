"""
Test matrix to determine which API version works with which model.

Run with: pytest tests/trapi/test_api_version_matrix.py -v

For each model, tries API versions from newest to oldest and stops at the first working one.

Based on Azure OpenAI API version documentation:
- https://learn.microsoft.com/en-us/azure/ai-services/openai/api-version-lifecycle
- https://learn.microsoft.com/en-us/azure/ai-services/openai/whats-new
"""

import litellm
import pytest
from sage_llm.token_manager import AzureTokenManager

# API versions to test (newest to oldest)
API_VERSIONS = [
    "2025-04-01-preview",
    "2025-03-01-preview",
    "2025-02-01-preview",
    "2025-01-01-preview",
    "2024-12-01-preview",
    "2024-10-21",  # Latest GA
    "2024-10-01-preview",
    "2024-09-01-preview",
    "2024-08-01-preview",
    "2024-07-01-preview",
    "2024-06-01",  # Previous GA
]

# Models to test (deployment_name format) - verified working models only
MODELS = [
    # GPT-4o series
    "gpt-4o_2024-11-20",
    "gpt-4o-mini_2024-07-18",
    # GPT-4.1 series
    "gpt-4.1_2025-04-14",
    "gpt-4.1-mini_2025-04-14",
    "gpt-4.1-nano_2025-04-14",
    # GPT-5 series
    "gpt-5_2025-08-07",
    "gpt-5-chat_2025-10-03",
    "gpt-5-mini_2025-08-07",
    "gpt-5-nano_2025-08-07",
    # GPT-5.1 series
    "gpt-5.1_2025-11-13",
    "gpt-5.1-chat_2025-11-13",
    # GPT-5.2 series
    "gpt-5.2_2025-12-11",
    "gpt-5.2-chat_2025-12-11",
    # Reasoning models
    "o1_2024-12-17",
    "o3_2025-04-16",
    "o3-mini_2025-01-31",
    "o4-mini_2025-04-16",
    # Grok series
    "grok-3_1",
    "grok-4_1",
    "grok-4-fast-non-reasoning_1",
    "grok-4-fast-reasoning_1",
    "grok-code-fast-1_1",
    # Other models
    "Llama-3.3-70B-Instruct_5",
    "Mistral-Large-3_1",
    "model-router_2025-11-18",
]

API_PATH = "msraif/shared"
TRAPI_SCOPE = "api://trapi/.default"


@pytest.fixture(scope="module")
def token():
    """Get Azure AD token once per module."""
    tm = AzureTokenManager(TRAPI_SCOPE)
    return tm.get_token()


@pytest.mark.parametrize("model", MODELS, ids=[m.split("_")[0] for m in MODELS])
def test_find_working_api_version(token: str, model: str):
    """Find the first working API version for each model (newest to oldest)."""
    base_url = f"https://trapi.research.microsoft.com/{API_PATH}"

    errors = []
    for api_version in API_VERSIONS:
        try:
            response = litellm.completion(
                model=f"azure/{model}",
                messages=[{"role": "user", "content": "Say 'ok'"}],
                api_key=token,
                api_base=base_url,
                api_version=api_version,
                max_tokens=5,
                timeout=10,
            )
            # Success! Report which version worked
            assert response.choices[0].message.content is not None
            print(f"\n✓ {model} works with {api_version}")
            return  # Stop trying other versions
        except Exception as e:
            error_msg = str(e)
            if "404" in error_msg:
                pytest.skip(f"404 Not Found - model/deployment does not exist at {API_PATH}")
            elif "403" in error_msg:
                pytest.skip(f"403 Forbidden - no access to {API_PATH}")
            # Otherwise, record error and try next version
            errors.append((api_version, error_msg[:100]))

    # No version worked
    pytest.fail(f"No API version worked. Errors: {errors[-1] if errors else 'none'}")
