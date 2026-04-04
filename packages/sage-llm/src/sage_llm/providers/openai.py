"""OpenAI provider — direct API and OpenAI-compatible gateways (e.g. phyagi)."""

import asyncio
import logging
import os
import threading
from typing import Any, TypeVar, cast

import openai
from openai.types.chat import (
    ChatCompletion,
    ChatCompletionMessageParam,
    ChatCompletionToolChoiceOptionParam,
    ChatCompletionToolParam,
)
from pydantic import BaseModel

from ..tracing import LLMTrace
from ..types import SageChatCompletionInfo, SageChatCompletionMessage, SageMessage
from .base import SageModelProvider

logger = logging.getLogger(__name__)
T = TypeVar("T", bound=BaseModel)

_thread_local = threading.local()

_MAX_CONCURRENT = int(
    os.environ.get("SAGE_LLM_MAX_CONCURRENT_OPENAI", os.environ.get("SAGE_LLM_MAX_CONCURRENT", "0"))
)
_async_semaphore: asyncio.Semaphore | None = None
_sync_semaphore: threading.Semaphore | None = (
    threading.Semaphore(_MAX_CONCURRENT) if _MAX_CONCURRENT > 0 else None
)


def _get_async_semaphore() -> asyncio.Semaphore | None:
    """Return a module-level async semaphore for throttling concurrent OpenAI calls."""
    global _async_semaphore
    if _MAX_CONCURRENT <= 0:
        return None
    if _async_semaphore is None:
        _async_semaphore = asyncio.Semaphore(_MAX_CONCURRENT)
    return _async_semaphore


def _get_openai_clients(
    api_key: str | None, base_url: str | None
) -> tuple[openai.OpenAI, openai.AsyncOpenAI]:
    """Return a cached (sync, async) OpenAI client pair for this thread."""
    cache_key = ("openai", api_key, base_url)
    cache = getattr(_thread_local, "openai_clients", None)
    if cache is None:
        cache = {}
        _thread_local.openai_clients = cache
    if cache_key in cache:
        return cache[cache_key]
    ck: dict[str, Any] = {}
    if api_key is not None:
        ck["api_key"] = api_key
    if base_url is not None:
        ck["base_url"] = base_url
    pair = (openai.OpenAI(**ck), openai.AsyncOpenAI(**ck))
    cache[cache_key] = pair
    return pair


class OpenAIMessage(SageChatCompletionMessage):
    """OpenAI message. Reasoning is opaque for o-series/GPT-5.x (only token counts)."""

    pass


class OpenAIProvider(SageModelProvider):
    """Provider for OpenAI and OpenAI-compatible APIs."""

    def __init__(self, api_key: str | None = None, base_url: str | None = None):
        self._client, self._async_client = _get_openai_clients(api_key, base_url)

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
        kwargs = self._build_kwargs(
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
        if _sync_semaphore:
            _sync_semaphore.acquire()
        try:
            response = self._client.chat.completions.create(**sdk_kwargs)  # ty:ignore[no-matching-overload]
        finally:
            if _sync_semaphore:
                _sync_semaphore.release()
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
        kwargs = self._build_kwargs(
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
        sem = _get_semaphore()
        if sem:
            async with sem:
                response = await self._async_client.chat.completions.create(**sdk_kwargs)  # ty:ignore[no-matching-overload]
        else:
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
        kwargs = self._build_kwargs(
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
        if _sync_semaphore:
            _sync_semaphore.acquire()
        try:
            response = self._client.chat.completions.create(**sdk_kwargs)  # ty:ignore[no-matching-overload]
        finally:
            if _sync_semaphore:
                _sync_semaphore.release()
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
        kwargs = self._build_kwargs(
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
        sem = _get_async_semaphore()
        if sem:
            async with sem:
                response = await self._async_client.chat.completions.create(**sdk_kwargs)  # ty:ignore[no-matching-overload]
        else:
            response = await self._async_client.chat.completions.create(**sdk_kwargs)  # ty:ignore[no-matching-overload]
        _fill_trace(trace, sdk_kwargs, response)
        message = _to_openai_message(response)
        assert message.content is not None
        return response_format.model_validate_json(message.content)

    # -- internals --

    @staticmethod
    def _build_kwargs(**params: Any) -> dict[str, Any]:
        """Build OpenAI SDK kwargs, dropping Nones."""
        return {k: v for k, v in params.items() if v is not None}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _to_openai_messages(messages: list[SageMessage]) -> list[ChatCompletionMessageParam]:
    """Convert SageMessages to OpenAI-format message params."""
    out: list[ChatCompletionMessageParam] = []
    for msg in messages:
        if isinstance(msg, SageChatCompletionMessage):
            out.append(msg.model_dump(exclude_none=True, exclude={"completion_info"}))
        else:
            out.append(msg)
    return out


def _to_openai_message(response: ChatCompletion) -> OpenAIMessage:
    """Convert a ChatCompletion to an OpenAIMessage."""
    choice = response.choices[0]
    m = choice.message
    return OpenAIMessage(
        role=m.role,
        content=m.content,
        tool_calls=m.tool_calls,
        refusal=m.refusal,
        completion_info=SageChatCompletionInfo(
            id=response.id,
            model=response.model,
            finish_reason=choice.finish_reason,
            usage=response.usage,
        ),
    )


def _fill_trace(trace: LLMTrace, sdk_kwargs: dict[str, Any], response: ChatCompletion) -> None:
    """Fill provider-side trace fields from an OpenAI ChatCompletion."""
    trace.provider_name = "openai"
    trace.provider_request = sdk_kwargs
    trace.provider_response = response.model_dump(mode="json")

    if response.usage:
        trace.prompt_tokens = response.usage.prompt_tokens
        trace.completion_tokens = response.usage.completion_tokens
        trace.total_tokens = response.usage.total_tokens
        if response.usage.completion_tokens_details:
            trace.reasoning_tokens = response.usage.completion_tokens_details.reasoning_tokens


def _pydantic_to_json_schema(model_class: type[BaseModel]) -> dict[str, Any]:
    """Convert a Pydantic model class to an OpenAI response_format dict.

    Uses :func:`~sage_llm.schema_utils.ensure_strict_openai_schema` to
    inline ``$ref`` nodes, add ``additionalProperties: false``, and ensure
    complete ``required`` arrays on every object.
    """
    from ..schema_utils import ensure_strict_openai_schema

    raw = model_class.model_json_schema()
    cleaned = ensure_strict_openai_schema(raw)
    return {
        "type": "json_schema",
        "json_schema": {
            "name": model_class.__name__,
            "schema": cleaned,
            "strict": True,
        },
    }
