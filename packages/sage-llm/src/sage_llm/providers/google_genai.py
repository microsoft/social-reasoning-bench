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
from pydantic import BaseModel

from ..concurrency import record_usage, with_llm_retry
from ..tracing import LLMTrace
from ..types import SageChatCompletionInfo, SageChatCompletionMessage, SageMessage
from .base import SageModelProvider

logger = logging.getLogger(__name__)
T = TypeVar("T", bound=BaseModel)

_CLIENT_CACHE: dict[tuple, genai.Client] = {}


def _get_google_client(api_key: str | None) -> genai.Client:
    """Return a cached genai.Client."""
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
    """Google message with native thought part support."""

    thought_parts: list[dict[str, Any]] | None = None


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
        max_tokens: int | None = None,
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
        max_tokens: int | None = None,
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
    max_tokens: int | None = None,
    top_p: float | None = None,
    stop: str | list[str] | None = None,
    tools: list[ChatCompletionToolParam] | None = None,
    tool_choice: ChatCompletionToolChoiceOptionParam | None = None,
    reasoning_effort: str | int | None = None,
    response_format: type[BaseModel] | None = None,
) -> tuple[types.ContentListUnion, types.GenerateContentConfig]:
    system_instruction: str | None = None
    contents: list[types.Content] = []

    # Build tool_call_id → function_name lookup from assistant messages so that
    # tool-role messages (which may omit "name") can resolve the function name.
    tc_id_to_name: dict[str, str] = {}
    for msg in messages:
        if isinstance(msg, SageChatCompletionMessage) and msg.tool_calls:
            for tc in msg.tool_calls:
                if isinstance(tc, ChatCompletionMessageToolCall):
                    tc_id_to_name[tc.id] = tc.function.name

    for msg in messages:
        if isinstance(msg, SageChatCompletionMessage):
            parts = _translate_assistant_parts(msg)
            contents.append(types.Content(role="model", parts=parts))
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
    return cast(types.ContentListUnion, contents), config


def _translate_user(content: str | None) -> types.Content:
    return types.Content(role="user", parts=[types.Part(text=content or "")])


def _extract_text(content: Any) -> str:
    """Extract plain text from a message content field.

    Handles str, list of content parts (extracts text parts), and None.
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


def _translate_assistant_parts(msg: SageChatCompletionMessage) -> list[types.Part]:
    """Translate an assistant SageChatCompletionMessage to Google Part list."""
    parts: list[types.Part] = []

    # Inject thought parts from previous GoogleMessage turns
    if isinstance(msg, GoogleMessage) and msg.thought_parts:
        for tp in msg.thought_parts:
            parts.append(types.Part(text=tp.get("text", ""), thought=True))

    if msg.content:
        parts.append(types.Part(text=msg.content))

    if msg.tool_calls:
        for tc in msg.tool_calls:
            if isinstance(tc, ChatCompletionMessageToolCall):
                name = tc.function.name
                args = json.loads(tc.function.arguments)
                parts.append(types.Part(function_call=types.FunctionCall(name=name, args=args)))

    return parts


def _translate_tool_result(
    msg: ChatCompletionToolMessageParam,
    tc_id_to_name: dict[str, str] | None = None,
) -> types.Content:
    """Translate a tool-role message dict to a Google FunctionResponse Content."""
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
    max_tokens: int | None,
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
        budget = reasoning_effort if isinstance(reasoning_effort, int) else 8192
        cfg["thinking_config"] = types.ThinkingConfig(thinking_budget=budget, include_thoughts=True)

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
    """
    if defs is None:
        defs = schema.get("$defs", {})

    # Resolve $ref
    if "$ref" in schema:
        ref_name = schema["$ref"].rsplit("/", 1)[-1]
        resolved = defs.get(ref_name, {})
        # Sibling keys (e.g. description) override the resolved def
        merged = {**resolved, **{k: v for k, v in schema.items() if k != "$ref"}}
        return _json_schema_to_google_schema(merged, defs)

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
    if "properties" in schema and isinstance(schema["properties"], dict):
        kwargs["properties"] = {
            name: _json_schema_to_google_schema(prop, defs)
            for name, prop in schema["properties"].items()
            if isinstance(prop, dict)
        }

    if "items" in schema and isinstance(schema["items"], dict):
        kwargs["items"] = _json_schema_to_google_schema(schema["items"], defs)

    if "anyOf" in schema and isinstance(schema["anyOf"], list):
        kwargs["any_of"] = [
            _json_schema_to_google_schema(s, defs) for s in schema["anyOf"] if isinstance(s, dict)
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
                mode=cast(types.FunctionCallingConfigMode, "ANY")
            )
        )
    if openai_choice == "none":
        return types.ToolConfig(
            function_calling_config=types.FunctionCallingConfig(
                mode=cast(types.FunctionCallingConfigMode, "NONE")
            )
        )
    if openai_choice["type"] == "function":
        return types.ToolConfig(
            function_calling_config=types.FunctionCallingConfig(
                mode=cast(types.FunctionCallingConfigMode, "ANY"),
                allowed_function_names=[openai_choice["function"]["name"]],
            )
        )
    return None


# ---------------------------------------------------------------------------
# Response normalization (Google → GoogleMessage)
# ---------------------------------------------------------------------------


def _to_google_message(response: types.GenerateContentResponse, model: str) -> GoogleMessage:
    text_parts: list[str] = []
    thought_parts: list[dict[str, Any]] = []
    tool_calls: list[ChatCompletionMessageToolCall] = []

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
                elif part.thought:
                    thought_parts.append({"text": part.text, "thought": True})
                elif part.text:
                    text_parts.append(part.text)

    content = "\n".join(text_parts) if text_parts else None

    # Finish reason
    finish_reason = "stop"
    if response.candidates:
        reason = getattr(response.candidates[0], "finish_reason", None)
        if reason:
            reason_str = str(reason).lower()
            if "tool" in reason_str or "function" in reason_str:
                finish_reason = "tool_calls"
            elif "length" in reason_str or "max_tokens" in reason_str:
                finish_reason = "length"

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
    contents: types.ContentListUnion,
    config: types.GenerateContentConfig,
) -> dict[str, Any]:
    """Serialize request args for tracing. Best-effort dict conversion."""
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
    """Best-effort serialization of Google response for tracing."""
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
    """Fill provider-side trace fields from a Google response."""
    trace.provider_name = "google"
    trace.provider_request = sdk_kwargs
    trace.provider_response = _serialize_response(response)

    if response.usage_metadata:
        um = response.usage_metadata
        trace.prompt_tokens = getattr(um, "prompt_token_count", None)
        trace.completion_tokens = getattr(um, "candidates_token_count", None)
        if trace.prompt_tokens is not None and trace.completion_tokens is not None:
            trace.total_tokens = trace.prompt_tokens + trace.completion_tokens
