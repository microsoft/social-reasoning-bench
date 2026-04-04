"""Azure OpenAI provider — TRAPI and direct Azure deployments."""

import logging
import threading
from typing import Any, Callable, TypeVar

import openai
from openai.types.chat import (
    ChatCompletion,
    ChatCompletionToolChoiceOptionParam,
    ChatCompletionToolParam,
)
from pydantic import BaseModel

from ..tracing import LLMTrace
from ..types import SageChatCompletionMessage, SageMessage
from .base import SageModelProvider
from .openai import (
    OpenAIMessage,
    _pydantic_to_json_schema,
    _to_openai_message,
    _to_openai_messages,
)

logger = logging.getLogger(__name__)
T = TypeVar("T", bound=BaseModel)

DEFAULT_API_VERSION = "2025-04-01-preview"

_thread_local = threading.local()


def _get_azure_clients(
    azure_endpoint: str | None,
    api_key: str | None,
    azure_ad_token_provider: Callable[[], str] | None,
    api_version: str | None,
) -> tuple[openai.AzureOpenAI, openai.AsyncAzureOpenAI]:
    """Return a cached (sync, async) Azure client pair for this thread."""
    cache_key = ("azure", azure_endpoint, api_key, id(azure_ad_token_provider), api_version)
    cache = getattr(_thread_local, "azure_clients", None)
    if cache is None:
        cache = {}
        _thread_local.azure_clients = cache
    if cache_key in cache:
        return cache[cache_key]
    ck: dict[str, Any] = {"api_version": api_version or DEFAULT_API_VERSION}
    if azure_endpoint is not None:
        ck["azure_endpoint"] = azure_endpoint
    if api_key is not None:
        ck["api_key"] = api_key
    if azure_ad_token_provider is not None:
        ck["azure_ad_token_provider"] = azure_ad_token_provider
    pair = (openai.AzureOpenAI(**ck), openai.AsyncAzureOpenAI(**ck))
    cache[cache_key] = pair
    return pair


class AzureProvider(SageModelProvider):
    """Provider for Azure OpenAI deployments (including TRAPI)."""

    def __init__(
        self,
        azure_endpoint: str | None = None,
        api_key: str | None = None,
        azure_ad_token_provider: Callable[[], str] | None = None,
        api_version: str | None = None,
    ):
        self._client, self._async_client = _get_azure_clients(
            azure_endpoint, api_key, azure_ad_token_provider, api_version
        )

    # -- public API --

    def complete(
        self,
        model: str,
        messages: list[SageMessage],
        *,
        trace: LLMTrace,
        temperature: float | None = None,
        max_tokens: int | None = None,
        top_p: float | None = None,
        stop: str | list[str] | None = None,
        tools: list[ChatCompletionToolParam] | None = None,
        tool_choice: ChatCompletionToolChoiceOptionParam | None = None,
        reasoning_effort: str | int | None = None,
    ) -> SageChatCompletionMessage:
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
        response = self._client.chat.completions.create(**sdk_kwargs)  # ty:ignore[no-matching-overload]
        _fill_trace(trace, sdk_kwargs, response)
        return _to_openai_message(response)

    async def acomplete(
        self,
        model: str,
        messages: list[SageMessage],
        *,
        trace: LLMTrace,
        temperature: float | None = None,
        max_tokens: int | None = None,
        top_p: float | None = None,
        stop: str | list[str] | None = None,
        tools: list[ChatCompletionToolParam] | None = None,
        tool_choice: ChatCompletionToolChoiceOptionParam | None = None,
        reasoning_effort: str | int | None = None,
    ) -> SageChatCompletionMessage:
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
        response = await self._async_client.chat.completions.create(**sdk_kwargs)  # ty:ignore[no-matching-overload]
        _fill_trace(trace, sdk_kwargs, response)
        return _to_openai_message(response)

    def parse(
        self,
        model: str,
        messages: list[SageMessage],
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
        response = self._client.chat.completions.create(**sdk_kwargs)  # ty:ignore[no-matching-overload]
        _fill_trace(trace, sdk_kwargs, response)
        message = _to_openai_message(response)
        assert message.content is not None
        return response_format.model_validate_json(message.content)

    async def aparse(
        self,
        model: str,
        messages: list[SageMessage],
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
        response = await self._async_client.chat.completions.create(**sdk_kwargs)  # ty:ignore[no-matching-overload]
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
    """Fill provider-side trace fields for Azure OpenAI."""
    trace.provider_name = "azure_openai"
    trace.provider_request = sdk_kwargs
    trace.provider_response = response.model_dump(mode="json")

    if response.usage:
        trace.prompt_tokens = response.usage.prompt_tokens
        trace.completion_tokens = response.usage.completion_tokens
        trace.total_tokens = response.usage.total_tokens
        if response.usage.completion_tokens_details:
            trace.reasoning_tokens = response.usage.completion_tokens_details.reasoning_tokens
