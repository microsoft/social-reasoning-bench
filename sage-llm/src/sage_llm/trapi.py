"""TRAPI utilities for Azure authentication, model parsing, and deployment mapping."""

import os
from typing import Any

from azure.identity import (
    AzureCliCredential,
    ChainedTokenCredential,
    DefaultAzureCredential,
    get_bearer_token_provider,
)

# Model name -> deployment name mapping
DEPLOYMENTS: dict[str, str] = {
    # GPT-4o series
    "gpt-4o": "gpt-4o_2024-11-20",
    "gpt-4o-mini": "gpt-4o-mini_2024-07-18",
    # GPT-4.1 series
    "gpt-4.1": "gpt-4.1_2025-04-14",
    "gpt-4.1-mini": "gpt-4.1-mini_2025-04-14",
    "gpt-4.1-nano": "gpt-4.1-nano_2025-04-14",
    # GPT-5 series
    "gpt-5": "gpt-5_2025-08-07",
    "gpt-5-chat": "gpt-5-chat_2025-10-03",
    "gpt-5-mini": "gpt-5-mini_2025-08-07",
    "gpt-5-nano": "gpt-5-nano_2025-08-07",
    # GPT-5.1 series
    "gpt-5.1": "gpt-5.1_2025-11-13",
    "gpt-5.1-chat": "gpt-5.1-chat_2025-11-13",
    # GPT-5.2 series
    "gpt-5.2": "gpt-5.2_2025-12-11",
    "gpt-5.2-chat": "gpt-5.2-chat_2025-12-11",
    # Reasoning models
    "o1": "o1_2024-12-17",
    "o3": "o3_2025-04-16",
    "o3-mini": "o3-mini_2025-01-31",
    "o4-mini": "o4-mini_2025-04-16",
    # Other models
    "Llama-3.3-70B-Instruct": "Llama-3.3-70B-Instruct_5",
    "Mistral-Large-3": "Mistral-Large-3_1",
    "model-router": "model-router_2025-11-18",
}

TRAPI_SCOPE = "api://trapi/.default"
DEFAULT_API_PATH = "msraif/shared"


def get_model_deployment(model: str) -> str:
    """Get Azure deployment name for a model."""
    return DEPLOYMENTS.get(model, model)


def list_models() -> list[str]:
    """List available model names."""
    return list(DEPLOYMENTS.keys())


def get_azure_credential():
    """Get Azure credential chain for TRAPI authentication."""
    return ChainedTokenCredential(
        AzureCliCredential(),
        DefaultAzureCredential(
            exclude_cli_credential=True,
            exclude_environment_credential=True,
            exclude_shared_token_cache_credential=True,
            exclude_developer_cli_credential=True,
            exclude_powershell_credential=True,
            exclude_interactive_browser_credential=True,
            exclude_visual_studio_code_credentials=True,
            managed_identity_client_id=os.environ.get("DEFAULT_IDENTITY_CLIENT_ID"),
        ),
    )


def get_token_provider():
    """Get a token provider function for TRAPI authentication."""
    cred = get_azure_credential()
    return get_bearer_token_provider(cred, TRAPI_SCOPE)


def parse_model(model: str) -> tuple[str, str]:
    """Parse TRAPI model string into (api_path, model_name).

    Model format: trapi/[{apiPath}/]{model}
    If no apiPath is provided, defaults to msraif/shared.

    Examples:
        - trapi/gpt-4.1 -> ("msraif/shared", "gpt-4.1")
        - trapi/msraif/shared/gpt-5.2 -> ("msraif/shared", "gpt-5.2")
    """
    parts = model.split("/")
    # Handle both "trapi/..." and "..." (prefix may be stripped)
    if parts[0] == "trapi":
        parts = parts[1:]
    if len(parts) < 1:
        raise ValueError(
            f"Invalid TRAPI model format: {model}. "
            f"Expected: trapi/{{model}} or trapi/{{apiPath}}/{{model}}"
        )
    # If only model name provided, use default api path
    if len(parts) == 1:
        return DEFAULT_API_PATH, parts[0]
    # Last part is model name, everything else is apiPath
    model_name = parts[-1]
    api_path = "/".join(parts[:-1])
    return api_path, model_name


def handle_model(model: str, kwargs: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    """Handle trapi models by configuring Azure OpenAI parameters.

    TRAPI models use the format: trapi/[{apiPath}/]{model}
    Example: trapi/gpt-4.1 or trapi/msraif/shared/gpt-5.2

    Returns (resolved_model, updated_kwargs).
    """
    if not model.startswith("trapi/"):
        return model, kwargs

    # Parse model path and get deployment name
    api_path, model_name = parse_model(model)
    deployment = get_model_deployment(model_name)

    # Use Azure provider with AD token provider
    kwargs["api_base"] = f"https://trapi.research.microsoft.com/{api_path}"
    kwargs["azure_ad_token_provider"] = get_token_provider()

    # Return azure/{deployment} format for litellm routing
    return f"azure/{deployment}", kwargs
