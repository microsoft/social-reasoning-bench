"""OpenAI provider — direct API and OpenAI-compatible gateways (e.g. phyagi)."""

import asyncio
import logging
import threading
import time
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
        num_retries: int = 3,
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
        return self._call_with_retries(
            lambda: self._client.chat.completions.create(**sdk_kwargs),  # ty:ignore[no-matching-overload]
            sdk_kwargs,
            trace,
            num_retries,
        )

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
        num_retries: int = 3,
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
        return await self._acall_with_retries(
            lambda: self._async_client.chat.completions.create(**sdk_kwargs),  # ty:ignore[no-matching-overload]
            sdk_kwargs,
            trace,
            num_retries,
        )

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
        num_retries: int = 3,
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
        message = self._call_with_retries(
            lambda: self._client.chat.completions.create(**sdk_kwargs),  # ty:ignore[no-matching-overload]
            sdk_kwargs,
            trace,
            num_retries,
        )
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
        num_retries: int = 3,
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
        message = await self._acall_with_retries(
            lambda: self._async_client.chat.completions.create(**sdk_kwargs),  # ty:ignore[no-matching-overload]
            sdk_kwargs,
            trace,
            num_retries,
        )
        assert message.content is not None
        return response_format.model_validate_json(message.content)

    # -- internals --

    @staticmethod
    def _build_kwargs(**params: Any) -> dict[str, Any]:
        """Build OpenAI SDK kwargs, dropping Nones."""
        return {k: v for k, v in params.items() if v is not None}

    def _call_with_retries(
        self,
        call,
        sdk_kwargs: dict[str, Any],
        trace: LLMTrace,
        num_retries: int,
    ) -> OpenAIMessage:
        last_error: Exception | None = None
        for attempt in range(max(1, num_retries + 1)):
            try:
                response = call()
                _fill_trace(trace, sdk_kwargs, response)
                return _to_openai_message(response)
            except openai.APIStatusError as e:
                last_error = e
                if _is_retryable(e) and attempt < num_retries:
                    time.sleep(min(2**attempt, 8))
                    continue
                raise
            except (openai.APITimeoutError, openai.APIConnectionError) as e:
                last_error = e
                if attempt < num_retries:
                    time.sleep(min(2**attempt, 8))
                    continue
                raise
        assert last_error is not None
        raise last_error

    async def _acall_with_retries(
        self,
        call,
        sdk_kwargs: dict[str, Any],
        trace: LLMTrace,
        num_retries: int,
    ) -> OpenAIMessage:
        last_error: Exception | None = None
        for attempt in range(max(1, num_retries + 1)):
            try:
                response = await call()
                _fill_trace(trace, sdk_kwargs, response)
                return _to_openai_message(response)
            except openai.APIStatusError as e:
                last_error = e
                if _is_retryable(e) and attempt < num_retries:
                    await asyncio.sleep(min(2**attempt, 8))
                    continue
                raise
            except (openai.APITimeoutError, openai.APIConnectionError) as e:
                last_error = e
                if attempt < num_retries:
                    await asyncio.sleep(min(2**attempt, 8))
                    continue
                raise
        assert last_error is not None
        raise last_error


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


def _is_retryable(e: openai.APIStatusError) -> bool:
    return e.status_code in (429, 500, 502, 503, 504)
