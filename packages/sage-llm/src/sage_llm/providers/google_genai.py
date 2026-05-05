"""Google provider — Gemini models with thinking support."""

import json
import logging
import time
from typing import Any, TypeVar, cast

from google import genai
from google.genai import types
from openai.types.chat import (
    ChatCompletionMessageToolCall,
    ChatCompletionToolChoiceOptionParam,
    ChatCompletionToolMessageParam,
    ChatCompletionToolParam,
)
from openai.types.chat.chat_completion_message_tool_call import Function
from openai.types.completion_usage import CompletionUsage
from pydantic import BaseModel, TypeAdapter

_CONTENTS_ADAPTER: TypeAdapter[list[types.Content]] = TypeAdapter(list[types.Content])

_FINISH_REASON_MAP: dict[types.FinishReason, str] = {
    types.FinishReason.STOP: "stop",
    types.FinishReason.MAX_TOKENS: "length",
    types.FinishReason.UNEXPECTED_TOOL_CALL: "tool_calls",
    types.FinishReason.MALFORMED_FUNCTION_CALL: "tool_calls",
    types.FinishReason.SAFETY: "content_filter",
    types.FinishReason.BLOCKLIST: "content_filter",
    types.FinishReason.PROHIBITED_CONTENT: "content_filter",
    types.FinishReason.SPII: "content_filter",
    types.FinishReason.IMAGE_SAFETY: "content_filter",
    types.FinishReason.IMAGE_PROHIBITED_CONTENT: "content_filter",
}

from ..concurrency import record_usage, with_llm_retry
from ..tracing import LLMTrace
from ..types import (
    DEFAULT_MAX_TOKENS,
    SageChatCompletionInfo,
    SageChatCompletionMessage,
    SageMessage,
)
from .base import SageModelProvider

logger = logging.getLogger(__name__)
T = TypeVar("T", bound=BaseModel)

_CLIENT_CACHE: dict[tuple, genai.Client] = {}


def _get_google_client(api_key: str | None) -> genai.Client:
    """Return a cached genai.Client.

    Args:
        api_key: Optional Google API key. If ``None``, the SDK uses
            its default credential resolution.

    Returns:
        A cached :class:`genai.Client` instance.
    """
    cache_key = ("google", api_key)
    if cache_key in _CLIENT_CACHE:
        return _CLIENT_CACHE[cache_key]
    ck: dict[str, Any] = {}
    if api_key is not None:
        ck["api_key"] = api_key
    client = genai.Client(**ck)
    _CLIENT_CACHE[cache_key] = client
    return client


class GoogleMessage(SageChatCompletionMessage):
    """Google message with native thought part support.

    thought_parts and tool_call_signatures are inherited from
    SageChatCompletionMessage so they survive serialization round-trips
    even when the caller stores the message as the base type.
    """


class GoogleProvider(SageModelProvider):
    """Provider for Google Gemini models."""

    PROVIDER_KEY = "google"

    def __init__(self, api_key: str | None = None):
        self._client = _get_google_client(api_key)

    async def acomplete(
        self,
        model: str,
        messages: list[SageMessage],
        *,
        trace: LLMTrace,
        temperature: float | None = None,
        max_tokens: int = DEFAULT_MAX_TOKENS,
        top_p: float | None = None,
        stop: str | list[str] | None = None,
        tools: list[ChatCompletionToolParam] | None = None,
        tool_choice: ChatCompletionToolChoiceOptionParam | None = None,
        reasoning_effort: str | int | None = None,
    ) -> SageChatCompletionMessage:
        contents, config = _translate_request(
            messages,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            stop=stop,
            tools=tools,
            tool_choice=tool_choice,
            reasoning_effort=reasoning_effort,
        )
        sdk_kwargs = _serialize_sdk_kwargs(model, contents, config)

        async def _call(_ctx: Any) -> types.GenerateContentResponse:
            resp: types.GenerateContentResponse | None = None
            last_reason: Any = "unknown"
            for attempt in range(3):
                resp = await self._client.aio.models.generate_content(
                    model=model,
                    contents=cast(types.ContentListUnionDict, contents),
                    config=config,
                )
                try:
                    _ensure_non_empty_response(resp)
                    return resp
                except RuntimeError as exc:
                    last_reason = (
                        resp.candidates[0].finish_reason if resp.candidates else "no_candidates"
                    )
                    logger.info(
                        "Gemini empty response attempt %d/3 (finish_reason=%s): %s",
                        attempt + 1,
                        last_reason,
                        exc,
                    )
            assert resp is not None
            logger.error(
                "Gemini empty responses after 3 attempts (last finish_reason=%s)",
                last_reason,
            )
            return resp

        response, call_duration = await with_llm_retry(
            self.PROVIDER_KEY,
            model,
            _call,
        )
        if response.usage_metadata:
            um = response.usage_metadata
            record_usage(
                self.PROVIDER_KEY,
                model,
                getattr(um, "prompt_token_count", 0) or 0,
                getattr(um, "candidates_token_count", 0) or 0,
                call_duration,
                cached_tokens=getattr(um, "cached_content_token_count", 0) or 0,
                reasoning_tokens=getattr(um, "thoughts_token_count", 0) or 0,
            )
        _fill_trace(trace, sdk_kwargs, response)
        return _to_google_message(response, model)

    async def aparse(
        self,
        model: str,
        messages: list[SageMessage],
        response_format: type[T],
        *,
        temperature: float | None = None,
        max_tokens: int = DEFAULT_MAX_TOKENS,
        top_p: float | None = None,
        stop: str | list[str] | None = None,
        reasoning_effort: str | int | None = None,
    ) -> T:
        contents, config = _translate_request(
            messages,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            stop=stop,
            reasoning_effort=reasoning_effort,
            response_format=response_format,
        )
        sdk_kwargs = _serialize_sdk_kwargs(model, contents, config)
        trace = LLMTrace()
        response, call_duration = await with_llm_retry(
            self.PROVIDER_KEY,
            model,
            lambda _: self._client.aio.models.generate_content(
                model=model,
                contents=cast(types.ContentListUnionDict, contents),
                config=config,
            ),
        )
        if response.usage_metadata:
            um = response.usage_metadata
            record_usage(
                self.PROVIDER_KEY,
                model,
                getattr(um, "prompt_token_count", 0) or 0,
                getattr(um, "candidates_token_count", 0) or 0,
                call_duration,
                cached_tokens=getattr(um, "cached_content_token_count", 0) or 0,
                reasoning_tokens=getattr(um, "thoughts_token_count", 0) or 0,
            )
        _fill_trace(trace, sdk_kwargs, response)
        message = _to_google_message(response, model)
        assert message.content is not None
        return response_format.model_validate_json(message.content)


# ---------------------------------------------------------------------------
# Request translation (SageMessage → Google format)
# ---------------------------------------------------------------------------


def _translate_request(
    messages: list[SageMessage],
    *,
    temperature: float | None = None,
    max_tokens: int = DEFAULT_MAX_TOKENS,
    top_p: float | None = None,
    stop: str | list[str] | None = None,
    tools: list[ChatCompletionToolParam] | None = None,
    tool_choice: ChatCompletionToolChoiceOptionParam | None = None,
    reasoning_effort: str | int | None = None,
    response_format: type[BaseModel] | None = None,
) -> tuple[list[types.Content], types.GenerateContentConfig]:
    system_instruction: str | None = None
    contents: list[types.Content] = []

    # Build tool_call_id → function_name lookup from assistant messages so that
    # tool-role messages (which may omit "name") can resolve the function name.
    tc_id_to_name: dict[str, str] = {}
    # Track tool_call_ids whose function_call parts lack a thought_signature.
    # These synthetic/forced calls must be represented as text (not
    # function_call Parts) because Gemini 3+ rejects unsigned function calls.
    unsigned_tc_ids: set[str] = set()

    for msg in messages:
        if isinstance(msg, SageChatCompletionMessage) and msg.tool_calls:
            sigs = msg.tool_call_signatures
            for i, tc in enumerate(msg.tool_calls):
                if isinstance(tc, ChatCompletionMessageToolCall):
                    tc_id_to_name[tc.id] = tc.function.name
                    has_sig = sigs is not None and i < len(sigs) and sigs[i] is not None
                    if not has_sig:
                        unsigned_tc_ids.add(tc.id)

    # Buffer unsigned tool call descriptions so we can merge them with
    # their results into user-role messages (instead of model-role text
    # that Gemini mimics, producing text-based tool calls).
    pending_unsigned: dict[str, str] = {}  # tc_id -> "name(args)"

    for msg in messages:
        if isinstance(msg, SageChatCompletionMessage):
            parts, _text_fallback = _translate_assistant_parts(msg, unsigned_tc_ids)
            if parts:
                contents.append(types.Content(role="model", parts=parts))
            # Buffer unsigned call descriptions — don't emit as model text.
            if msg.tool_calls:
                for tc in msg.tool_calls:
                    if isinstance(tc, ChatCompletionMessageToolCall) and tc.id in unsigned_tc_ids:
                        pending_unsigned[tc.id] = f"{tc.function.name}({tc.function.arguments})"
        elif isinstance(msg, dict):
            content = msg.get("content", "")
            if msg.get("role") == "system":
                system_instruction = _extract_text(content)
            elif msg.get("role") == "assistant":
                contents.append(
                    types.Content(
                        role="model",
                        parts=[types.Part(text=_extract_text(content))],
                    )
                )
            elif msg["role"] == "tool":
                tc_id = str(msg.get("tool_call_id", ""))
                if tc_id in unsigned_tc_ids:
                    # Merge call description + result into a single user message
                    # so the model never sees model-role text resembling tool calls.
                    call_desc = pending_unsigned.pop(tc_id, "unknown action")
                    result_text = msg.get("content", "")
                    contents.append(
                        _translate_user(f"Action taken: {call_desc}\nResult: {result_text}")
                    )
                else:
                    contents.append(_translate_tool_result(msg, tc_id_to_name))
            else:
                contents.append(_translate_user(_extract_text(content)))

    config = _build_config(
        system_instruction=system_instruction,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        stop=stop,
        tools=tools,
        tool_choice=tool_choice,
        reasoning_effort=reasoning_effort,
        response_format=response_format,
    )
    return _CONTENTS_ADAPTER.validate_python(contents), config


def _translate_user(content: str | None) -> types.Content:
    return types.Content(role="user", parts=[types.Part(text=content or "")])


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
                parts.append(str(part.get("text", "")))
            elif isinstance(part, str):
                parts.append(part)
        return "\n".join(parts)
    return ""


def _translate_assistant_parts(
    msg: SageChatCompletionMessage,
    unsigned_tc_ids: set[str] | None = None,
) -> tuple[list[types.Part], str | None]:
    """Translate an assistant SageChatCompletionMessage to Google Part list.

    Args:
        msg: An assistant-role message (possibly a :class:`GoogleMessage`
            with thought parts).
        unsigned_tc_ids: Tool call IDs that lack a thought_signature.  These
            are collapsed to a text description instead of a ``function_call``
            Part so Gemini 3+ models don't reject the request.

    Returns:
        Tuple of (parts list, text_fallback).  ``text_fallback`` is a text
        description of unsigned function calls (or ``None``).
    """
    parts: list[types.Part] = []
    unsigned_tc_ids = unsigned_tc_ids or set()

    # Inject thought parts from previous turns
    if msg.thought_parts:
        for tp in msg.thought_parts:
            sig = tp.get("thought_signature")
            parts.append(types.Part(text=tp.get("text", ""), thought=True, thought_signature=sig))

    if msg.content:
        parts.append(types.Part(text=msg.content))

    text_fallback_lines: list[str] = []

    if msg.tool_calls:
        signatures = msg.tool_call_signatures

        for i, tc in enumerate(msg.tool_calls):
            if isinstance(tc, ChatCompletionMessageToolCall):
                name = tc.function.name
                args = json.loads(tc.function.arguments)
                sig = signatures[i] if signatures and i < len(signatures) else None

                if tc.id in unsigned_tc_ids:
                    # No thought_signature — emit as text instead.
                    text_fallback_lines.append(f"[Called {name}({json.dumps(args)})]")
                else:
                    parts.append(
                        types.Part(
                            function_call=types.FunctionCall(name=name, args=args),
                            thought_signature=sig,
                        )
                    )

    text_fallback = "\n".join(text_fallback_lines) if text_fallback_lines else None
    return parts, text_fallback


def _translate_tool_result(
    msg: ChatCompletionToolMessageParam,
    tc_id_to_name: dict[str, str] | None = None,
) -> types.Content:
    """Translate a tool-role message dict to a Google FunctionResponse Content.

    Args:
        msg: OpenAI-format tool message dict with ``content`` and
            ``tool_call_id``.
        tc_id_to_name: Optional mapping from tool_call_id to function name
            for resolving names when the ``name`` field is absent.

    Returns:
        A :class:`types.Content` with role ``"user"`` wrapping a
        ``FunctionResponse`` part.
    """
    content = str(msg.get("content", ""))
    # Resolve function name: explicit "name" field, or look up via tool_call_id.
    name = str(msg.get("name", ""))
    if not name and tc_id_to_name:
        tool_call_id = str(msg.get("tool_call_id", ""))
        name = tc_id_to_name.get(tool_call_id, "")

    try:
        result = json.loads(content)
    except (json.JSONDecodeError, TypeError):
        result = {"result": content}

    # FunctionResponse.response must be a dict — wrap scalars/lists
    if not isinstance(result, dict):
        result = {"result": result}

    return types.Content(
        role="user",
        parts=[types.Part(function_response=types.FunctionResponse(name=name, response=result))],
    )


# ---------------------------------------------------------------------------
# Config building
# ---------------------------------------------------------------------------


def _build_config(
    *,
    system_instruction: str | None,
    temperature: float | None,
    max_tokens: int,
    top_p: float | None,
    stop: str | list[str] | None,
    tools: list[ChatCompletionToolParam] | None,
    tool_choice: ChatCompletionToolChoiceOptionParam | None,
    reasoning_effort: str | int | None,
    response_format: type[BaseModel] | None,
) -> types.GenerateContentConfig:
    cfg: dict[str, Any] = {}

    if system_instruction:
        cfg["system_instruction"] = system_instruction
    if temperature is not None:
        cfg["temperature"] = temperature
    if max_tokens is not None:
        cfg["max_output_tokens"] = max_tokens
    if top_p is not None:
        cfg["top_p"] = top_p
    if stop is not None:
        cfg["stop_sequences"] = [stop] if isinstance(stop, str) else stop

    if tools is not None:
        cfg["tools"] = _translate_tools(tools)
    if tool_choice is not None:
        tc = _translate_tool_choice(tool_choice)
        if tc:
            cfg["tool_config"] = tc

    # Thinking
    if reasoning_effort is not None:
        if not isinstance(reasoning_effort, int):
            raise TypeError(f"Gemini requires an integer thinking_budget; got {reasoning_effort!r}")
        cfg["thinking_config"] = types.ThinkingConfig(
            thinking_budget=reasoning_effort, include_thoughts=True
        )

    # Structured output
    if response_format is not None:
        cfg["response_mime_type"] = "application/json"
        cfg["response_schema"] = _json_schema_to_google_schema(response_format.model_json_schema())

    return types.GenerateContentConfig(**cfg)


def _translate_tools(openai_tools: list[ChatCompletionToolParam]) -> list[types.Tool]:
    declarations = []
    for tool in openai_tools:
        if tool["type"] == "function":
            fn = tool["function"]
            name: str = fn["name"]
            description: str = fn.get("description") or ""
            parameters = fn.get("parameters")
            google_params: types.Schema | None = None
            if parameters is not None:
                google_params = _json_schema_to_google_schema(parameters)
            declarations.append(
                types.FunctionDeclaration(
                    name=name,
                    description=description,
                    parameters=google_params,
                )
            )
    return [types.Tool(function_declarations=declarations)] if declarations else []


# ---------------------------------------------------------------------------
# JSON Schema → Google Schema conversion
# ---------------------------------------------------------------------------

# JSON Schema type string → Google Type enum value
_TYPE_MAP: dict[str, str] = {
    "string": "STRING",
    "number": "NUMBER",
    "integer": "INTEGER",
    "boolean": "BOOLEAN",
    "array": "ARRAY",
    "object": "OBJECT",
    "null": "NULL",
}


def _json_schema_to_google_schema(
    schema: dict[str, Any],
    defs: dict[str, Any] | None = None,
) -> types.Schema:
    """Convert a JSON Schema dict to a ``types.Schema``.

    Handles $ref/$defs inlining, strips unsupported keys, and sanitises
    values (e.g. empty enum strings) so the result is always valid for
    the Gemini API.

    Args:
        schema: JSON Schema dict (e.g. from ``BaseModel.model_json_schema()``).
        defs: Definitions dict. If ``None``, extracted from ``schema["$defs"]``.

    Returns:
        A :class:`types.Schema` instance suitable for the Gemini API.
    """
    resolved_defs: dict[str, Any] = defs if defs is not None else schema.get("$defs", {})

    # Resolve $ref
    if "$ref" in schema:
        ref_name = schema["$ref"].rsplit("/", 1)[-1]
        if ref_name not in resolved_defs:
            raise KeyError(f"$ref {schema['$ref']!r} not found in $defs")
        resolved = resolved_defs[ref_name]
        # Sibling keys (e.g. description) override the resolved def
        merged = {**resolved, **{k: v for k, v in schema.items() if k != "$ref"}}
        return _json_schema_to_google_schema(merged, resolved_defs)

    kwargs: dict[str, Any] = {}

    # type
    if "type" in schema:
        mapped = _TYPE_MAP.get(schema["type"])
        if mapped:
            kwargs["type"] = mapped

    # Simple scalar fields — skip "title" to reduce schema size (Gemini
    # rejects large schemas with MALFORMED_FUNCTION_CALL).
    for key in ("description", "format", "pattern"):
        if key in schema and schema[key] is not None:
            kwargs[key] = str(schema[key])

    for key in ("minimum", "maximum"):
        if key in schema:
            kwargs[key] = float(schema[key])

    for src, dst in (
        ("minItems", "min_items"),
        ("maxItems", "max_items"),
        ("minLength", "min_length"),
        ("maxLength", "max_length"),
        ("minProperties", "min_properties"),
        ("maxProperties", "max_properties"),
    ):
        if src in schema:
            kwargs[dst] = int(schema[src])

    if "nullable" in schema:
        kwargs["nullable"] = bool(schema["nullable"])

    # enum — filter empty strings (Gemini rejects them)
    if "enum" in schema:
        filtered = [str(e) for e in schema["enum"] if e != "" and e is not None]
        if filtered:
            kwargs["enum"] = filtered

    for key in ("default", "example"):
        if key in schema:
            kwargs[key] = schema[key]

    if "required" in schema:
        kwargs["required"] = list(schema["required"])

    if "propertyOrdering" in schema:
        kwargs["property_ordering"] = list(schema["propertyOrdering"])

    # Recursive fields
    if "properties" in schema:
        kwargs["properties"] = {
            name: _json_schema_to_google_schema(prop, resolved_defs)
            for name, prop in schema["properties"].items()
        }

    if "items" in schema:
        kwargs["items"] = _json_schema_to_google_schema(schema["items"], resolved_defs)

    if "anyOf" in schema:
        kwargs["any_of"] = [
            _json_schema_to_google_schema(s, resolved_defs) for s in schema["anyOf"]
        ]

    return types.Schema(**kwargs)


def _translate_tool_choice(
    openai_choice: ChatCompletionToolChoiceOptionParam | None,
) -> types.ToolConfig | None:
    if openai_choice == "auto" or openai_choice is None:
        return None
    if openai_choice == "required":
        return types.ToolConfig(
            function_calling_config=types.FunctionCallingConfig(
                mode=types.FunctionCallingConfigMode.ANY
            )
        )
    if openai_choice == "none":
        return types.ToolConfig(
            function_calling_config=types.FunctionCallingConfig(
                mode=types.FunctionCallingConfigMode.NONE
            )
        )
    if openai_choice["type"] == "function":
        return types.ToolConfig(
            function_calling_config=types.FunctionCallingConfig(
                mode=types.FunctionCallingConfigMode.ANY,
                allowed_function_names=[openai_choice["function"]["name"]],
            )
        )
    return None


# ---------------------------------------------------------------------------
# Response validation
# ---------------------------------------------------------------------------


def _ensure_non_empty_response(response: types.GenerateContentResponse) -> None:
    """Raise on completely empty Gemini responses so retries kick in.

    Gemini can return empty responses (no content, no tool calls) with
    finish reasons like MALFORMED_FUNCTION_CALL.  Treating these as
    transient errors lets the retry loop re-attempt the call.
    """
    if not response.candidates:
        raise RuntimeError("Gemini returned no candidates")
    candidate = response.candidates[0]
    if not candidate.content or not candidate.content.parts:
        reason = getattr(candidate, "finish_reason", "unknown")
        raise RuntimeError(f"Gemini returned empty response (finish_reason={reason})")


# ---------------------------------------------------------------------------
# Response normalization (Google → GoogleMessage)
# ---------------------------------------------------------------------------


def _to_google_message(response: types.GenerateContentResponse, model: str) -> GoogleMessage:
    text_parts: list[str] = []
    thought_parts: list[dict[str, Any]] = []
    tool_calls: list[ChatCompletionMessageToolCall] = []
    tool_call_signatures: list[bytes | None] = []

    if response.candidates:
        candidate = response.candidates[0]
        if candidate.content and candidate.content.parts:
            for part in candidate.content.parts:
                if part.function_call:
                    fc = part.function_call
                    tool_calls.append(
                        ChatCompletionMessageToolCall(
                            id=f"call_{fc.name}_{int(time.time() * 1000)}",
                            type="function",
                            function=Function(
                                name=fc.name or "",
                                arguments=json.dumps(fc.args) if fc.args else "{}",
                            ),
                        )
                    )
                    tool_call_signatures.append(part.thought_signature)
                elif part.thought:
                    tp: dict[str, Any] = {"text": part.text, "thought": True}
                    if part.thought_signature is not None:
                        tp["thought_signature"] = part.thought_signature
                    thought_parts.append(tp)
                elif part.text:
                    text_parts.append(part.text)

    content = "\n".join(text_parts) if text_parts else None

    # Finish reason
    finish_reason = "stop"
    if response.candidates:
        reason = response.candidates[0].finish_reason
        if reason is None or reason in _FINISH_REASON_MAP:
            finish_reason = _FINISH_REASON_MAP.get(reason, "stop") if reason else "stop"
        else:
            logger.warning("unknown Gemini finish_reason %r; defaulting to 'stop'", reason)

    # Usage
    usage = None
    if response.usage_metadata:
        um = response.usage_metadata
        pt = getattr(um, "prompt_token_count", 0) or 0
        ct = getattr(um, "candidates_token_count", 0) or 0
        usage = CompletionUsage(prompt_tokens=pt, completion_tokens=ct, total_tokens=pt + ct)

    return GoogleMessage(
        role="assistant",
        content=content,
        tool_calls=cast(list, tool_calls) if tool_calls else None,
        thought_parts=thought_parts if thought_parts else None,
        tool_call_signatures=tool_call_signatures if tool_call_signatures else None,
        completion_info=SageChatCompletionInfo(
            id=f"google-{int(time.time() * 1000)}",
            model=model,
            finish_reason=finish_reason,
            usage=usage,
        ),
    )


# ---------------------------------------------------------------------------
# SDK kwargs serialization
# ---------------------------------------------------------------------------


def _serialize_sdk_kwargs(
    model: str,
    contents: list[types.Content],
    config: types.GenerateContentConfig,
) -> dict[str, Any]:
    """Serialize request args for tracing. Best-effort dict conversion.

    Args:
        model: Model name string.
        contents: Google-format content list sent to the API.
        config: Generation configuration object.

    Returns:
        Dict with ``model``, ``contents``, and ``config`` keys suitable
        for JSON tracing.
    """
    try:
        if isinstance(contents, list):
            contents_serialized = [str(c) for c in contents]
        else:
            contents_serialized = [str(contents)] if contents else []
    except Exception:
        contents_serialized = [repr(contents)]
    try:
        config_serialized = str(config)
    except Exception:
        config_serialized = repr(config)
    return {
        "model": model,
        "contents": contents_serialized,
        "config": config_serialized,
    }


def _serialize_response(response: types.GenerateContentResponse) -> dict[str, Any]:
    """Best-effort serialization of Google response for tracing.

    Args:
        response: Raw :class:`types.GenerateContentResponse` from the API.

    Returns:
        JSON-safe dict representation of the response.
    """
    try:
        if hasattr(response, "model_dump"):
            return response.model_dump(mode="json")
    except Exception:
        pass
    try:
        return {"raw": str(response)}
    except Exception:
        return {"raw": repr(response)}


# ---------------------------------------------------------------------------
# Trace filling
# ---------------------------------------------------------------------------


def _fill_trace(
    trace: LLMTrace,
    sdk_kwargs: dict[str, Any],
    response: types.GenerateContentResponse,
) -> None:
    """Fill provider-side trace fields from a Google response.

    Args:
        trace: Trace object to populate with provider-specific data.
        sdk_kwargs: Serialized SDK keyword arguments for the request.
        response: Raw :class:`types.GenerateContentResponse` from the API.
    """
    trace.provider_name = "google"
    trace.provider_request = sdk_kwargs
    trace.provider_response = _serialize_response(response)

    if response.usage_metadata:
        um = response.usage_metadata
        trace.prompt_tokens = getattr(um, "prompt_token_count", None)
        trace.completion_tokens = getattr(um, "candidates_token_count", None)
        if trace.prompt_tokens is not None and trace.completion_tokens is not None:
            trace.total_tokens = trace.prompt_tokens + trace.completion_tokens
