"""Anthropic provider — Claude models with thinking support."""

import json
import logging
from typing import Any, TypeVar, cast

import anthropic
from anthropic.types import MessageParam
from openai.types.chat import (
    ChatCompletionMessageToolCall,
    ChatCompletionToolChoiceOptionParam,
    ChatCompletionToolMessageParam,
    ChatCompletionToolParam,
)
from openai.types.chat.chat_completion_message_tool_call import Function
from openai.types.completion_usage import CompletionUsage
from pydantic import BaseModel

from ..concurrency import record_usage, with_llm_retry
from ..tracing import LLMTrace
from ..types import (
    SRBenchAssistantMessageParam,
    SRBenchChatCompletionInfo,
    SRBenchChatCompletionMessage,
    SRBenchInputMessage,
)
from .base import SRBenchModelProvider

logger = logging.getLogger(__name__)
T = TypeVar("T", bound=BaseModel)

_CLIENT_CACHE: dict[tuple, anthropic.AsyncAnthropic] = {}


def _get_anthropic_client(api_key: str | None) -> anthropic.AsyncAnthropic:
    """Return a cached AsyncAnthropic client.

    Args:
        api_key: Optional Anthropic API key. If ``None``, the SDK uses
            its default credential resolution.

    Returns:
        A cached :class:`anthropic.AsyncAnthropic` instance.
    """
    cache_key = ("anthropic", api_key)
    if cache_key in _CLIENT_CACHE:
        return _CLIENT_CACHE[cache_key]
    ck: dict[str, Any] = {}
    if api_key is not None:
        ck["api_key"] = api_key
    ck["max_retries"] = 0
    client = anthropic.AsyncAnthropic(**ck)
    _CLIENT_CACHE[cache_key] = client
    return client


class AnthropicMessage(SRBenchChatCompletionMessage):
    """Anthropic message with native thinking block support.

    thinking_blocks carries the raw blocks (including cryptographic signatures)
    needed for multi-turn thinking preservation. The field is included
    automatically by ``model_dump`` so no custom serializer is needed.
    """

    thinking_blocks: list[dict[str, Any]] | None = None


class AnthropicProvider(SRBenchModelProvider):
    """Provider for Anthropic Claude models."""

    PROVIDER_KEY = "anthropic"

    def __init__(self, api_key: str | None = None):
        self._client = _get_anthropic_client(api_key)

    async def _sdk_call(self, **kwargs):
        async with self._client.messages.stream(**kwargs) as stream:
            message = await stream.get_final_message()
        return message

    async def acomplete(
        self,
        model: str,
        messages: list[SRBenchInputMessage],
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
        system, anthropic_msgs = _translate_messages(messages)
        kwargs = _build_kwargs(
            system=system,
            temperature=temperature,
            max_tokens=max_tokens or 8192,
            top_p=top_p,
            stop=stop,
            tools=tools,
            tool_choice=tool_choice,
            reasoning_effort=reasoning_effort,
            model=model,
        )
        sdk_kwargs = {"model": model, "messages": anthropic_msgs, **kwargs}
        response, call_duration = await with_llm_retry(
            self.PROVIDER_KEY,
            model,
            lambda _: self._sdk_call(**sdk_kwargs),
        )
        record_usage(
            self.PROVIDER_KEY,
            model,
            response.usage.input_tokens,
            response.usage.output_tokens,
            call_duration,
            cached_tokens=getattr(response.usage, "cache_read_input_tokens", 0) or 0,
        )
        _fill_trace(trace, sdk_kwargs, response)
        return _to_anthropic_message(response, model)

    async def aparse(
        self,
        model: str,
        messages: list[SRBenchInputMessage],
        response_format: type[T],
        *,
        temperature: float | None = None,
        max_tokens: int | None = None,
        top_p: float | None = None,
        stop: str | list[str] | None = None,
        reasoning_effort: str | int | None = None,
    ) -> T:
        system, anthropic_msgs = _translate_messages(messages)
        tool, tool_name = _structured_output_tool(response_format)
        kwargs = _build_kwargs(
            system=system,
            temperature=temperature,
            max_tokens=max_tokens or 8192,
            top_p=top_p,
            stop=stop,
            tools=None,
            tool_choice=None,
            reasoning_effort=reasoning_effort,
            model=model,
        )
        kwargs["tools"] = [tool]
        kwargs["tool_choice"] = {"type": "tool", "name": tool_name}
        sdk_kwargs = {"model": model, "messages": anthropic_msgs, **kwargs}
        trace = LLMTrace()
        response, call_duration = await with_llm_retry(
            self.PROVIDER_KEY,
            model,
            lambda _: self._sdk_call(**sdk_kwargs),
        )
        record_usage(
            self.PROVIDER_KEY,
            model,
            response.usage.input_tokens,
            response.usage.output_tokens,
            call_duration,
            cached_tokens=getattr(response.usage, "cache_read_input_tokens", 0) or 0,
        )
        _fill_trace(trace, sdk_kwargs, response)
        message = _to_anthropic_message(response, model)
        return _extract_structured_output(message, response_format)


# ---------------------------------------------------------------------------
# Message translation (SRBenchInputMessage → Anthropic format)
# ---------------------------------------------------------------------------


def _translate_messages(
    messages: list[SRBenchInputMessage],
) -> tuple[str | anthropic.NotGiven, list[MessageParam]]:
    """Convert SRBench input messages to Anthropic format.

    Returns (system, messages). For assistant messages, ``thinking_blocks``
    extension keys (left behind by :meth:`AnthropicMessage.to_input_dict`)
    are injected into the assistant content so extended-thinking signatures
    survive across turns.

    Args:
        messages: List of SRBench input messages to translate.

    Returns:
        Tuple of ``(system, anthropic_messages)`` where *system* is the
        system prompt (or ``NOT_GIVEN``) and *anthropic_messages* is the
        translated message list.
    """
    system: str | anthropic.NotGiven = anthropic.NOT_GIVEN
    out: list[dict[str, Any]] = []

    for msg in messages:
        role = msg.get("role")
        content = msg.get("content", "")
        if role == "system":
            system = _extract_text(content)
        elif role == "assistant":
            out.append(_translate_assistant(cast(SRBenchAssistantMessageParam, msg)))
        elif role == "tool":
            out.append(_translate_tool(cast(ChatCompletionToolMessageParam, msg)))
        else:
            out.append({"role": "user", "content": _extract_text(content)})

    return system, cast(list[MessageParam], out)


def _extract_text(content: Any) -> str:
    """Extract plain text from a message content field.

    Handles str, list of content parts (extracts text parts), and None.

    Args:
        content: Message content — a string, list of content-part dicts,
            or ``None``.

    Returns:
        Extracted plain text string (empty string for ``None``).
    """
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for part in content:
            if isinstance(part, dict) and part.get("type") == "text":
                parts.append(part.get("text", ""))
            elif isinstance(part, str):
                parts.append(part)
        return "\n".join(parts)
    return ""


def _translate_assistant(msg: SRBenchAssistantMessageParam) -> dict[str, Any]:
    """Translate an assistant input dict, injecting thinking blocks and tool_use.

    Reads ``thinking_blocks`` from the extension key (set by
    :meth:`AnthropicMessage.to_input_dict`) so extended-thinking signatures
    survive across turns.

    Args:
        msg: Assistant-role TypedDict, possibly carrying SRBench extension
            keys (``thinking_blocks``, ``completion_info``, …).

    Returns:
        Anthropic-format message dict with role ``"assistant"``.
    """
    blocks: list[dict[str, Any]] = []

    thinking_blocks = msg.get("thinking_blocks")
    if thinking_blocks:
        blocks.extend(thinking_blocks)

    content = msg.get("content")
    text = _extract_text(content) if content is not None else ""
    if text:
        blocks.append({"type": "text", "text": text})

    for tc in msg.get("tool_calls") or []:
        if tc.get("type") != "function":
            continue
        fn = tc["function"]  # ty: ignore[invalid-key]
        tc_args = fn.get("arguments", "{}")
        blocks.append(
            {
                "type": "tool_use",
                "id": tc["id"],
                "name": fn["name"],
                "input": json.loads(tc_args) if tc_args else {},
            }
        )

    return {"role": "assistant", "content": blocks}


def _translate_tool(msg: ChatCompletionToolMessageParam) -> dict[str, Any]:
    """Translate a tool-role message to Anthropic tool_result.

    Args:
        msg: OpenAI-format tool message dict containing ``content``
            and ``tool_call_id``.

    Returns:
        Anthropic-format user message dict wrapping a ``tool_result`` block.
    """
    content = str(msg.get("content", ""))
    tool_call_id = str(msg.get("tool_call_id", ""))

    return {
        "role": "user",
        "content": [
            {
                "type": "tool_result",
                "tool_use_id": tool_call_id,
                "content": content if isinstance(content, str) else json.dumps(content),
            }
        ],
    }


# ---------------------------------------------------------------------------
# Kwargs translation
# ---------------------------------------------------------------------------


def _build_kwargs(
    *,
    system: str | anthropic.NotGiven,
    temperature: float | None,
    max_tokens: int,
    top_p: float | None,
    stop: str | list[str] | None,
    tools: list[ChatCompletionToolParam] | None,
    tool_choice: ChatCompletionToolChoiceOptionParam | None,
    reasoning_effort: str | int | None,
    model: str,
) -> dict[str, Any]:
    kwargs: dict[str, Any] = {"max_tokens": max_tokens}

    if system is not anthropic.NOT_GIVEN:
        kwargs["system"] = system
    if temperature is not None:
        kwargs["temperature"] = temperature
    if top_p is not None:
        kwargs["top_p"] = top_p
    if stop is not None:
        kwargs["stop_sequences"] = [stop] if isinstance(stop, str) else stop

    # Tools
    if tools is not None:
        kwargs["tools"] = _translate_tools(tools)
    if tool_choice is not None:
        kwargs["tool_choice"] = _translate_tool_choice(tool_choice)

    # Reasoning
    if reasoning_effort is not None:
        if isinstance(reasoning_effort, int):
            kwargs["thinking"] = {"type": "enabled", "budget_tokens": reasoning_effort}
            kwargs["max_tokens"] = 2 * reasoning_effort
        else:
            # String effort (e.g. for Opus 4.5)
            kwargs["reasoning_effort"] = reasoning_effort

    return kwargs


def _translate_tools(openai_tools: list[ChatCompletionToolParam]) -> list[dict[str, Any]]:
    out = []
    for tool in openai_tools:
        if tool["type"] == "function":
            fn = tool["function"]
            name: str = fn["name"]
            description: str = fn.get("description") or ""
            parameters = fn.get("parameters") or {"type": "object", "properties": {}}
            out.append(
                {
                    "name": name,
                    "description": description,
                    "input_schema": parameters,
                }
            )
    return out


def _translate_tool_choice(openai_choice: ChatCompletionToolChoiceOptionParam) -> dict[str, Any]:
    if openai_choice == "auto" or openai_choice is None:
        return {"type": "auto"}
    if openai_choice == "required":
        return {"type": "any"}
    if openai_choice == "none":
        return {"type": "auto"}
    if openai_choice["type"] == "function":
        return {"type": "tool", "name": openai_choice["function"]["name"]}
    return {"type": "auto"}


# ---------------------------------------------------------------------------
# Structured output via tool-use trick
# ---------------------------------------------------------------------------


def _structured_output_tool(model_class: type[BaseModel]) -> tuple[dict, str]:
    """Create a synthetic tool for structured output. Returns (tool_def, tool_name).

    Args:
        model_class: Pydantic model whose JSON schema defines the tool input.

    Returns:
        Tuple of ``(tool_definition_dict, tool_name)``.
    """
    name = f"output_{model_class.__name__}"
    return {
        "name": name,
        "description": f"Output structured data as {model_class.__name__}",
        "input_schema": model_class.model_json_schema(),
    }, name


def _extract_structured_output(msg: SRBenchChatCompletionMessage, response_format: type[T]) -> T:
    """Extract structured output from a tool-use response.

    Args:
        msg: Assistant message that may contain a tool call with the
            structured output payload.
        response_format: Pydantic model class to validate the output against.

    Returns:
        Validated instance of *response_format*.
    """
    if msg.tool_calls:
        tc = msg.tool_calls[0]
        if isinstance(tc, ChatCompletionMessageToolCall):
            return response_format.model_validate_json(tc.function.arguments)
    # Fallback: try parsing content directly
    assert msg.content is not None
    return response_format.model_validate_json(msg.content)


# ---------------------------------------------------------------------------
# Response normalization (Anthropic → AnthropicMessage)
# ---------------------------------------------------------------------------


def _to_anthropic_message(response: anthropic.types.Message, model: str) -> AnthropicMessage:
    text_parts: list[str] = []
    thinking_blocks: list[dict[str, Any]] = []
    tool_calls: list[ChatCompletionMessageToolCall] = []

    for block in response.content:
        if isinstance(block, anthropic.types.TextBlock):
            text_parts.append(block.text)
        elif isinstance(block, anthropic.types.ThinkingBlock):
            thinking_blocks.append(
                {
                    "type": "thinking",
                    "thinking": block.thinking,
                    "signature": block.signature,
                }
            )
        elif isinstance(block, anthropic.types.ToolUseBlock):
            tool_calls.append(
                ChatCompletionMessageToolCall(
                    id=block.id,
                    type="function",
                    function=Function(
                        name=block.name,
                        arguments=json.dumps(block.input)
                        if not isinstance(block.input, str)
                        else block.input,
                    ),
                )
            )

    content = "\n".join(text_parts) if text_parts else None

    finish_reason_map = {
        "end_turn": "stop",
        "stop_sequence": "stop",
        "tool_use": "tool_calls",
        "max_tokens": "length",
    }

    return AnthropicMessage(
        role="assistant",
        content=content,
        tool_calls=cast(list, tool_calls) if tool_calls else None,
        thinking_blocks=thinking_blocks if thinking_blocks else None,
        completion_info=SRBenchChatCompletionInfo(
            id=response.id,
            model=model,
            finish_reason=finish_reason_map.get(response.stop_reason or "", "stop"),
            usage=CompletionUsage(
                prompt_tokens=response.usage.input_tokens,
                completion_tokens=response.usage.output_tokens,
                total_tokens=response.usage.input_tokens + response.usage.output_tokens,
            ),
        ),
    )


# ---------------------------------------------------------------------------
# Trace filling
# ---------------------------------------------------------------------------


def _fill_trace(
    trace: LLMTrace,
    sdk_kwargs: dict[str, Any],
    response: anthropic.types.Message,
) -> None:
    """Fill provider-side trace fields from an Anthropic Message.

    Args:
        trace: Trace object to populate with provider-specific data.
        sdk_kwargs: The keyword arguments passed to the Anthropic SDK call.
        response: Raw Anthropic :class:`Message` response.
    """
    trace.provider_name = "anthropic"
    trace.provider_request = sdk_kwargs
    trace.provider_response = response.model_dump(mode="json")

    trace.prompt_tokens = response.usage.input_tokens
    trace.completion_tokens = response.usage.output_tokens
    trace.total_tokens = response.usage.input_tokens + response.usage.output_tokens
