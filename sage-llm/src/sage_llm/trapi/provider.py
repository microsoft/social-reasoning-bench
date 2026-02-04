import os
from typing import Any, Optional, Union, cast

import httpx
from azure.identity import (
    AzureCliCredential,
    ChainedTokenCredential,
    DefaultAzureCredential,
    get_bearer_token_provider,
)
from litellm.llms.custom_httpx.http_handler import AsyncHTTPHandler, HTTPHandler
from litellm.llms.custom_llm import CustomLLM
from litellm.types.utils import ModelResponse
from litellm.utils import (
    convert_to_model_response_object,  # pyright: ignore[reportPrivateImportUsage]
)
from openai import AsyncOpenAI, OpenAI

from .models import get_model_deployment

# Params that TRAPI supports (Azure OpenAI backend).
# Used as an allowlist in both the LiteLLM client and the TRAPI provider.
TRAPI_SUPPORTED_PARAMS = [
    "frequency_penalty",
    "logit_bias",
    "logprobs",
    "top_logprobs",
    "max_tokens",
    "max_completion_tokens",
    "n",
    "presence_penalty",
    "response_format",
    "seed",
    "stop",
    "stream",
    "stream_options",
    "temperature",
    "top_p",
    "tools",
    "tool_choice",
    "parallel_tool_calls",
    "user",
    "reasoning_effort",
    "extra_body",
]


TRAPI_SCOPE = "api://trapi/.default"


def get_azure_credential():
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
    cred = get_azure_credential()
    return get_bearer_token_provider(cred, TRAPI_SCOPE)


def get_async_token_provider():
    """Return an async token provider for AsyncOpenAI.

    AsyncOpenAI expects: () -> Awaitable[str]
    """
    sync_provider = get_token_provider()

    async def async_provider() -> str:
        return sync_provider()

    return async_provider


def add_allowed_params_for_trapi(model: str, kwargs: dict) -> dict:
    """Add allowed_openai_params for trapi models to bypass LiteLLM validation."""
    if model.startswith("trapi/"):
        kwargs["allowed_openai_params"] = TRAPI_SUPPORTED_PARAMS
    return kwargs


def _filter_params(params: dict) -> dict:
    """Keep only TRAPI-supported params with non-None values."""
    return {k: v for k, v in params.items() if v is not None and k in TRAPI_SUPPORTED_PARAMS}


def parse_trapi_model(model: str) -> tuple[str, str]:
    """Parse TRAPI model string into (api_path, model_name).

    Model format: trapi/{apiPath}/{model}

    Note: LiteLLM strips the "trapi/" prefix before calling this function.

    Examples:
        - trapi/msraif/shared/gpt-5.2 -> ("msraif/shared", "gpt-5.2")
    """
    parts = model.split("/")
    # Handle both "trapi/..." and "..." (LiteLLM strips the prefix)
    if parts[0] == "trapi":
        parts = parts[1:]
    if len(parts) < 2:
        raise ValueError(
            f"Invalid TRAPI model format: {model}. "
            f"Expected: trapi/{{apiPath}}/{{model}} (e.g., trapi/msraif/shared/gpt-5.2)"
        )
    # Last part is model name, everything else is apiPath
    model_name = parts[-1]
    api_path = "/".join(parts[:-1])
    return api_path, model_name


class TrapiCustomLLM(CustomLLM):
    """TRAPI provider registered with LiteLLM's custom provider system.

    Model format: trapi/[{apiPath}/]{model}
    If no apiPath is provided, defaults to msraif/shared.

    Examples:
        - trapi/gpt-5.2 (uses default msraif/shared)
        - trapi/msraif/shared/gpt-5

    When registered with LiteLLM, calls to litellm.completion(model="trapi/...")
    are automatically routed to this handler.

    Clients are cached by endpoint to reuse connections.
    """

    def __init__(self):
        super().__init__()
        self._sync_clients: dict[str, OpenAI] = {}
        self._async_clients: dict[str, AsyncOpenAI] = {}

    def _get_azure_config(self, model: str) -> tuple[str, str, str]:
        """Get Azure configuration for a TRAPI model.

        Returns: (deployment, azure_endpoint, model_name)
        """
        api_path, model_name = parse_trapi_model(model)
        deployment = get_model_deployment(model_name)
        azure_endpoint = f"https://trapi.research.microsoft.com/{api_path}/openai/v1"
        return deployment, azure_endpoint, model_name

    def _get_sync_client(self, azure_endpoint: str) -> OpenAI:
        """Get or create a cached sync OpenAI client."""
        if azure_endpoint not in self._sync_clients:
            self._sync_clients[azure_endpoint] = OpenAI(
                api_key=get_token_provider(),
                base_url=azure_endpoint,
            )
        return self._sync_clients[azure_endpoint]

    def _get_async_client(self, azure_endpoint: str) -> AsyncOpenAI:
        """Get or create a cached async OpenAI client."""
        if azure_endpoint not in self._async_clients:
            self._async_clients[azure_endpoint] = AsyncOpenAI(
                api_key=get_async_token_provider(),
                base_url=azure_endpoint,
            )
        return self._async_clients[azure_endpoint]

    def completion(
        self,
        model: str,
        messages: list,
        api_base: str,
        custom_prompt_dict: dict,
        model_response: ModelResponse,
        print_verbose: Any,
        encoding: Any,
        api_key: Any,
        logging_obj: Any,
        optional_params: dict,
        acompletion: Any = None,
        litellm_params: Any = None,
        logger_fn: Any = None,
        headers: dict = {},
        timeout: Optional[Union[float, httpx.Timeout]] = None,
        client: Optional[HTTPHandler] = None,
    ):
        """Synchronous completion via OpenAI client."""
        deployment, azure_endpoint, _ = self._get_azure_config(model)
        azure_client = self._get_sync_client(azure_endpoint)

        response = azure_client.chat.completions.create(
            model=deployment,
            messages=messages,
            timeout=timeout,
            **_filter_params(optional_params),
        )

        return cast(
            ModelResponse,
            convert_to_model_response_object(
                response_object=response.model_dump(),
                model_response_object=model_response,
                response_type="completion",
            ),
        )

    async def acompletion(
        self,
        model: str,
        messages: list,
        api_base: str,
        custom_prompt_dict: dict,
        model_response: ModelResponse,
        print_verbose: Any,
        encoding: Any,
        api_key: Any,
        logging_obj: Any,
        optional_params: dict,
        acompletion: Any = None,
        litellm_params: Any = None,
        logger_fn: Any = None,
        headers: dict = {},
        timeout: Optional[Union[float, httpx.Timeout]] = None,
        client: Optional[AsyncHTTPHandler] = None,
    ):
        """Async completion via OpenAI client."""
        deployment, azure_endpoint, _ = self._get_azure_config(model)
        azure_client = self._get_async_client(azure_endpoint)

        response = await azure_client.chat.completions.create(
            model=deployment,
            messages=messages,
            timeout=timeout,
            **_filter_params(optional_params),
        )

        return cast(
            ModelResponse,
            convert_to_model_response_object(
                response_object=response.model_dump(),
                model_response_object=model_response,
                response_type="completion",
            ),
        )
