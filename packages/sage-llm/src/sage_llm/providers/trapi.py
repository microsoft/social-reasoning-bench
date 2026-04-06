"""TRAPI provider — Azure OpenAI with AD token auth and deployment mapping."""

import os

from azure.identity import (
    AzureCliCredential,
    ChainedTokenCredential,
    DefaultAzureCredential,
    get_bearer_token_provider,
)

from .azure_openai import AzureProvider

# Model name → Azure deployment name
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


def _get_token_provider():
    """Get a bearer token provider for TRAPI authentication."""
    cred = ChainedTokenCredential(
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
    return get_bearer_token_provider(cred, TRAPI_SCOPE)


def _parse_model(model: str) -> tuple[str, str]:
    """Parse trapi/[apiPath/]model → (api_path, model_name)."""
    parts = model.split("/")
    if parts[0] == "trapi":
        parts = parts[1:]
    if len(parts) < 1:
        raise ValueError(f"Invalid TRAPI model format: {model}")
    if len(parts) == 1:
        return DEFAULT_API_PATH, parts[0]
    return "/".join(parts[:-1]), parts[-1]


def _get_deployment(model_name: str) -> str:
    """Map model name to Azure deployment name."""
    return DEPLOYMENTS.get(model_name, model_name)


class TrapiProvider(AzureProvider):
    """Provider for Microsoft TRAPI (Azure OpenAI with AD token auth)."""

    PROVIDER_KEY = "trapi"

    def __init__(self, api_path: str = DEFAULT_API_PATH):
        super().__init__(
            azure_endpoint=f"https://trapi.research.microsoft.com/{api_path}",
            azure_ad_token_provider=_get_token_provider(),
        )

    @staticmethod
    def resolve_model(model: str) -> tuple[str, str]:
        """Parse trapi model string and resolve deployment name.

        Returns (api_path, deployment_name).
        """
        api_path, model_name = _parse_model(model)
        return api_path, _get_deployment(model_name)
