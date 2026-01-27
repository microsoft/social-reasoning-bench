from typing import Any, Optional, Union, cast

import httpx
from litellm.llms.custom_httpx.http_handler import AsyncHTTPHandler, HTTPHandler
from litellm.llms.custom_llm import CustomLLM
from litellm.types.utils import ModelResponse
from litellm.utils import (
    convert_to_model_response_object,  # pyright: ignore[reportPrivateImportUsage]
)
from openai import AsyncAzureOpenAI, AzureOpenAI

from ..token_manager import AzureTokenManager
from .models import TRAPI_SCOPE, TRAPI_SUPPORTED_PARAMS, get_api_version, get_deployment


def _filter_params(params: dict) -> dict:
    """Keep only TRAPI-supported params with non-None values."""
    return {k: v for k, v in params.items() if v is not None and k in TRAPI_SUPPORTED_PARAMS}


def parse_trapi_model(model: str) -> tuple[str, str]:
    """Parse TRAPI model string into (api_path, model_name).

    Model format: trapi/{apiPath}/{model} or {apiPath}/{model} (without prefix)
    Examples:
        - trapi/gcr/shared/gpt-4.1 -> ("gcr/shared", "gpt-4.1")
        - gcr/shared/gpt-4.1 -> ("gcr/shared", "gpt-4.1")
        - msraif/shared/gpt-5 -> ("msraif/shared", "gpt-5")
    """
    parts = model.split("/")
    # Handle both "trapi/..." and "..." (LiteLLM strips the prefix)
    if parts[0] == "trapi":
        parts = parts[1:]
    if len(parts) < 2:
        raise ValueError(
            f"Invalid TRAPI model format: {model}. Expected: [trapi/]{{apiPath}}/{{model}}"
        )
    # Last part is model name, everything else is apiPath
    model_name = parts[-1]
    api_path = "/".join(parts[:-1])
    return api_path, model_name


class TrapiCustomLLM(CustomLLM):
    """TRAPI provider registered with LiteLLM's custom provider system.

    Model format: trapi/{apiPath}/{model}
    Examples:
        - trapi/gcr/shared/gpt-4.1
        - trapi/msraif/shared/gpt-5

    When registered with LiteLLM, calls to litellm.completion(model="trapi/...")
    are automatically routed to this handler.

    Clients are cached by (azure_endpoint, api_version) to reuse connections.
    """

    def __init__(self):
        super().__init__()
        self._token_manager = AzureTokenManager(TRAPI_SCOPE)
        self._sync_clients: dict[tuple[str, str], AzureOpenAI] = {}
        self._async_clients: dict[tuple[str, str], AsyncAzureOpenAI] = {}

    def _get_azure_config(self, model: str) -> tuple[str, str, str, str]:
        """Get Azure configuration for a TRAPI model.

        Returns: (deployment, api_version, azure_endpoint, model_name)
        """
        api_path, model_name = parse_trapi_model(model)
        deployment = get_deployment(model_name)
        api_version = get_api_version(model_name)
        azure_endpoint = f"https://trapi.research.microsoft.com/{api_path}"
        return deployment, api_version, azure_endpoint, model_name

    def _get_sync_client(self, azure_endpoint: str, api_version: str) -> AzureOpenAI:
        """Get or create a cached sync Azure OpenAI client."""
        cache_key = (azure_endpoint, api_version)
        if cache_key not in self._sync_clients:
            self._sync_clients[cache_key] = AzureOpenAI(
                api_key=self._token_manager.get_token(),
                api_version=api_version,
                azure_endpoint=azure_endpoint,
            )
        return self._sync_clients[cache_key]

    def _get_async_client(self, azure_endpoint: str, api_version: str) -> AsyncAzureOpenAI:
        """Get or create a cached async Azure OpenAI client."""
        cache_key = (azure_endpoint, api_version)
        if cache_key not in self._async_clients:
            self._async_clients[cache_key] = AsyncAzureOpenAI(
                api_key=self._token_manager.get_token(),
                api_version=api_version,
                azure_endpoint=azure_endpoint,
            )
        return self._async_clients[cache_key]

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
        """Synchronous completion via Azure OpenAI client."""
        deployment, api_version, azure_endpoint, _ = self._get_azure_config(model)
        azure_client = self._get_sync_client(azure_endpoint, api_version)

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
        """Async completion via Azure OpenAI client."""
        deployment, api_version, azure_endpoint, _ = self._get_azure_config(model)
        azure_client = self._get_async_client(azure_endpoint, api_version)

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
