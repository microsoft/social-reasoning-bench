"""OpenAI provider — direct API and OpenAI-compatible gateways."""

import logging
from typing import Any, TypeVar, cast

import openai
from openai.types.chat import (
    ChatCompletion,
    ChatCompletionMessageParam,
    ChatCompletionToolChoiceOptionParam,
    ChatCompletionToolParam,
)
from pydantic import BaseModel

from ..concurrency import record_usage, with_llm_retry
from ..tracing import LLMTrace
from ..types import SageChatCompletionInfo, SageChatCompletionMessage, SageMessage
from .base import SageModelProvider

logger = logging.getLogger(__name__)
T = TypeVar("T", bound=BaseModel)

_CLIENT_CACHE: dict[tuple, openai.AsyncOpenAI] = {}


def _get_openai_client(api_key: str | None, base_url: str | None) -> openai.AsyncOpenAI:
    """Return a cached AsyncOpenAI client.

    Args:
        api_key: Optional OpenAI API key.
        base_url: Optional base URL for OpenAI-compatible gateways.

    Returns:
        A cached :class:`openai.AsyncOpenAI` instance.
    """
    cache_key = ("openai", api_key, base_url)
    if cache_key in _CLIENT_CACHE:
        return _CLIENT_CACHE[cache_key]
    ck: dict[str, Any] = {}
    if api_key is not None:
        ck["api_key"] = api_key
    if base_url is not None:
        ck["base_url"] = base_url
    ck["max_retries"] = 0
    client = openai.AsyncOpenAI(**ck)
    _CLIENT_CACHE[cache_key] = client
    return client


class OpenAIMessage(SageChatCompletionMessage):
    """OpenAI message. Reasoning is opaque for o-series/GPT-5.x (only token counts)."""

    pass


class OpenAIProvider(SageModelProvider):
    """Provider for OpenAI and OpenAI-compatible APIs."""

    PROVIDER_KEY = "openai"

    def __init__(self, api_key: str | None = None, base_url: str | None = None):
        self._client = _get_openai_client(api_key, base_url)

    # -- public API --

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

    # -- internals --

    @staticmethod
    def _build_kwargs(**params: Any) -> dict[str, Any]:
        """Build OpenAI SDK kwargs, dropping Nones.

        Args:
            **params: Arbitrary keyword arguments; ``None``-valued entries
                are omitted from the result.

        Returns:
            Filtered dict of non-``None`` keyword arguments.
        """
        return {k: v for k, v in params.items() if v is not None}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _to_openai_messages(messages: list[SageMessage]) -> list[ChatCompletionMessageParam]:
    """Convert SageMessages to OpenAI-format message params.

    Args:
        messages: List of Sage-typed messages to translate.

    Returns:
        List of OpenAI :class:`ChatCompletionMessageParam` dicts.
    """
    out: list[ChatCompletionMessageParam] = []
    for msg in messages:
        if isinstance(msg, SageChatCompletionMessage):
            out.append(msg.model_dump(exclude_none=True, exclude={"completion_info"}))
        else:
            out.append(msg)
    return out


def _to_openai_message(response: ChatCompletion) -> OpenAIMessage:
    """Convert a ChatCompletion to an OpenAIMessage.

    Args:
        response: Raw :class:`ChatCompletion` from the OpenAI SDK.

    Returns:
        An :class:`OpenAIMessage` with content, tool calls, and metadata.
    """
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
    """Fill provider-side trace fields from an OpenAI ChatCompletion.

    Args:
        trace: Trace object to populate with provider-specific data.
        sdk_kwargs: The keyword arguments passed to the OpenAI SDK call.
        response: Raw :class:`ChatCompletion` response from the SDK.
    """
    trace.provider_name = "openai"
    trace.provider_request = sdk_kwargs
    trace.provider_response = response.model_dump(mode="json")

    if response.usage:
        trace.prompt_tokens = response.usage.prompt_tokens
        trace.completion_tokens = response.usage.completion_tokens
        trace.total_tokens = response.usage.total_tokens
        if response.usage.completion_tokens_details:
            trace.reasoning_tokens = response.usage.completion_tokens_details.reasoning_tokens


def _extract_token_details(response: ChatCompletion) -> tuple[int, int]:
    """Extract (cached_tokens, reasoning_tokens) from an OpenAI response.

    Args:
        response: A :class:`ChatCompletion` with usage metadata.

    Returns:
        Tuple of ``(cached_tokens, reasoning_tokens)``, defaulting to
        ``0`` when the respective detail is unavailable.
    """
    cached = 0
    reasoning = 0
    if response.usage:
        if response.usage.prompt_tokens_details:
            cached = response.usage.prompt_tokens_details.cached_tokens or 0
        if response.usage.completion_tokens_details:
            reasoning = response.usage.completion_tokens_details.reasoning_tokens or 0
    return cached, reasoning


def _pydantic_to_json_schema(model_class: type[BaseModel]) -> dict[str, Any]:
    """Convert a Pydantic model class to an OpenAI response_format dict.

    Uses :func:`~sage_llm.schema_utils.ensure_strict_openai_schema` to
    inline ``$ref`` nodes, add ``additionalProperties: false``, and ensure
    complete ``required`` arrays on every object.

    Args:
        model_class: Pydantic model whose JSON schema defines the output
            structure.

    Returns:
        An OpenAI ``response_format`` dict with ``type: "json_schema"``.
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
