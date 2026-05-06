"""Azure OpenAI provider — direct Azure deployments."""

import logging
from typing import Any, Callable, TypeVar

import openai
from openai.types.chat import (
    ChatCompletion,
    ChatCompletionToolChoiceOptionParam,
    ChatCompletionToolParam,
)
from pydantic import BaseModel

from ..concurrency import record_usage, with_llm_retry
from ..tracing import LLMTrace
from ..types import SRBenchChatCompletionMessage, SRBenchMessage
from .base import SRBenchModelProvider
from .openai import (
    OpenAIMessage,
    _extract_token_details,
    _pydantic_to_json_schema,
    _to_openai_message,
    _to_openai_messages,
)

logger = logging.getLogger(__name__)
T = TypeVar("T", bound=BaseModel)

DEFAULT_API_VERSION = "2025-04-01-preview"

_CLIENT_CACHE: dict[tuple, openai.AsyncAzureOpenAI] = {}


def _get_azure_client(
    azure_endpoint: str | None,
    api_key: str | None,
    azure_ad_token_provider: Callable[[], str] | None,
    api_version: str | None,
) -> openai.AsyncAzureOpenAI:
    """Return a cached AsyncAzureOpenAI client.

    Args:
        azure_endpoint: Azure OpenAI endpoint URL.
        api_key: Optional API key for key-based auth.
        azure_ad_token_provider: Optional callable returning an Azure AD
            bearer token for token-based auth.
        api_version: Azure API version string.

    Returns:
        A cached :class:`openai.AsyncAzureOpenAI` instance.
    """
    cache_key = ("azure", azure_endpoint, api_key, id(azure_ad_token_provider), api_version)
    if cache_key in _CLIENT_CACHE:
        return _CLIENT_CACHE[cache_key]
    ck: dict[str, Any] = {"api_version": api_version or DEFAULT_API_VERSION}
    if azure_endpoint is not None:
        ck["azure_endpoint"] = azure_endpoint
    if api_key is not None:
        ck["api_key"] = api_key
    if azure_ad_token_provider is not None:
        ck["azure_ad_token_provider"] = azure_ad_token_provider
    ck["max_retries"] = 0
    ck["timeout"] = 120.0
    client = openai.AsyncAzureOpenAI(**ck)
    _CLIENT_CACHE[cache_key] = client
    return client


class AzureProvider(SRBenchModelProvider):
    """Provider for Azure OpenAI deployments."""

    PROVIDER_KEY = "azure"

    def __init__(
        self,
        azure_endpoint: str | None = None,
        api_key: str | None = None,
        azure_ad_token_provider: Callable[[], str] | None = None,
        api_version: str | None = None,
    ):
        self._client = _get_azure_client(
            azure_endpoint, api_key, azure_ad_token_provider, api_version
        )

    # -- public API --

    async def acomplete(
        self,
        model: str,
        messages: list[SRBenchMessage],
        *,
        trace: LLMTrace,
        temperature: float | None = None,
        max_tokens: int | None = None,
        top_p: float | None = None,
        stop: str | list[str] | None = None,
        tools: list[ChatCompletionToolParam] | None = None,
        tool_choice: ChatCompletionToolChoiceOptionParam | None = None,
        reasoning_effort: str | int | None = None,
    ) -> SRBenchChatCompletionMessage:
        kwargs = _build_kwargs(
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            stop=stop,
            tools=tools,
            tool_choice=tool_choice,
            reasoning_effort=reasoning_effort,
        )
        openai_msgs = _to_openai_messages(messages)
        sdk_kwargs = {"model": model, "messages": openai_msgs, **kwargs}
        response, call_duration = await with_llm_retry(
            self.PROVIDER_KEY,
            model,
            lambda _: self._client.chat.completions.create(**sdk_kwargs),  # ty:ignore[no-matching-overload]
        )
        if response.usage:
            cached, reasoning = _extract_token_details(response)
            record_usage(
                self.PROVIDER_KEY,
                model,
                response.usage.prompt_tokens or 0,
                response.usage.completion_tokens or 0,
                call_duration,
                cached_tokens=cached,
                reasoning_tokens=reasoning,
            )
        _fill_trace(trace, sdk_kwargs, response)
        return _to_openai_message(response)

    async def aparse(
        self,
        model: str,
        messages: list[SRBenchMessage],
        response_format: type[T],
        *,
        temperature: float | None = None,
        max_tokens: int | None = None,
        top_p: float | None = None,
        stop: str | list[str] | None = None,
        reasoning_effort: str | int | None = None,
    ) -> T:
        kwargs = _build_kwargs(
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            stop=stop,
            reasoning_effort=reasoning_effort,
        )
        kwargs["response_format"] = _pydantic_to_json_schema(response_format)
        openai_msgs = _to_openai_messages(messages)
        sdk_kwargs = {"model": model, "messages": openai_msgs, **kwargs}
        trace = LLMTrace()
        response, call_duration = await with_llm_retry(
            self.PROVIDER_KEY,
            model,
            lambda _: self._client.chat.completions.create(**sdk_kwargs),  # ty:ignore[no-matching-overload]
        )
        if response.usage:
            cached, reasoning = _extract_token_details(response)
            record_usage(
                self.PROVIDER_KEY,
                model,
                response.usage.prompt_tokens or 0,
                response.usage.completion_tokens or 0,
                call_duration,
                cached_tokens=cached,
                reasoning_tokens=reasoning,
            )
        _fill_trace(trace, sdk_kwargs, response)
        message = _to_openai_message(response)
        assert message.content is not None
        return response_format.model_validate_json(message.content)


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------


def _build_kwargs(**params: Any) -> dict[str, Any]:
    return {k: v for k, v in params.items() if v is not None}


def _fill_trace(trace: LLMTrace, sdk_kwargs: dict[str, Any], response: ChatCompletion) -> None:
    """Fill provider-side trace fields for Azure OpenAI.

    Args:
        trace: Trace object to populate with provider-specific data.
        sdk_kwargs: The keyword arguments passed to the Azure OpenAI SDK call.
        response: Raw :class:`ChatCompletion` response from the SDK.
    """
    trace.provider_name = "azure_openai"
    trace.provider_request = sdk_kwargs
    trace.provider_response = response.model_dump(mode="json")

    if response.usage:
        trace.prompt_tokens = response.usage.prompt_tokens
        trace.completion_tokens = response.usage.completion_tokens
        trace.total_tokens = response.usage.total_tokens
        if response.usage.completion_tokens_details:
            trace.reasoning_tokens = response.usage.completion_tokens_details.reasoning_tokens
