"""Core types for srbench-llm."""

from typing import Annotated, Any, Union, cast

from openai.types.chat import ChatCompletionMessage, ChatCompletionMessageParam
from openai.types.completion_usage import CompletionUsage
from pydantic import BaseModel, PlainSerializer, PlainValidator
from pydantic_core import from_json, to_json


class SRBenchChatCompletionInfo(BaseModel):
    """Response metadata. Kept in a single field on SRBenchChatCompletionMessage
    so it's easy to exclude when building the next turn's inputs."""

    id: str
    model: str
    finish_reason: str
    usage: CompletionUsage | None = None


class SRBenchChatCompletionMessage(ChatCompletionMessage):
    """Assistant message with response metadata.

    Role is always ``"assistant"`` (inherited from ChatCompletionMessage).
    Provider subclasses (AnthropicMessage, GoogleMessage, etc.) extend this
    with provider-specific fields like thinking_blocks.
    """

    completion_info: SRBenchChatCompletionInfo | None = None

    # Google-specific fields that must survive serialization round-trips so
    # that thought_signature values are preserved across multi-turn tool-use
    # conversations.  Gemini 3+ models reject requests that omit these.
    thought_parts: list[dict[str, Any]] | None = None
    tool_call_signatures: list[bytes | None] | None = None


def _validate_sage_message(msg: Any) -> Any:
    """Validate and discriminate SRBenchMessage input.

    - SRBenchChatCompletionMessage instances pass through unchanged.
    - Dicts with ``role: "assistant"`` are promoted to SRBenchChatCompletionMessage
      so round-tripping through JSON preserves the concrete type.
    - Other dicts (system/user/tool messages) stay as plain dicts.

    Args:
        msg: Raw message value — a :class:`BaseModel`, dict, or other type.

    Returns:
        The validated message, possibly promoted to
        :class:`SRBenchChatCompletionMessage`.

    Raises:
        ValueError: If *msg* is not a BaseModel or dict.
    """
    if isinstance(msg, SRBenchChatCompletionMessage):
        return msg
    if isinstance(msg, BaseModel):
        # Some other pydantic model (e.g. ChatCompletionMessage from openai) — convert
        return msg
    if isinstance(msg, dict):
        if msg.get("role") == "assistant":
            return SRBenchChatCompletionMessage.model_validate(msg)
        return msg
    raise ValueError(
        f"SRBenchMessage must be a BaseModel or dict, got {type(msg).__name__}: {msg!r:.200}"
    )


def _serialize_sage_message(
    msg: SRBenchChatCompletionMessage | ChatCompletionMessageParam,
) -> dict[str, Any]:
    """Serialize any SRBenchMessage variant to a JSON-safe dict.

    Handles:
    - Pydantic models (SRBenchChatCompletionMessage) → model_dump
    - TypedDicts / plain dicts (ChatCompletionMessageParam) → recursive serialization
    - Unexpected types → string fallback

    Args:
        msg: A :class:`SRBenchChatCompletionMessage` or
            :class:`ChatCompletionMessageParam` dict.

    Returns:
        JSON-safe dict representation of the message.

    Raises:
        ValueError: If *msg* is not a supported message type.
    """
    if isinstance(msg, SRBenchChatCompletionMessage):
        data = msg.model_dump(mode="json", exclude={"tool_call_signatures"})
        # Strip binary thought_signature from thought_parts dicts
        if data.get("thought_parts"):
            data["thought_parts"] = [
                {k: v for k, v in tp.items() if k != "thought_signature"}
                for tp in data["thought_parts"]
            ]
        return data
    elif isinstance(msg, dict):
        return cast(dict[str, Any], msg)
    raise ValueError(f"Cannot serialize SRBenchMessage of type {type(msg).__name__}: {msg!r:.200}")


SRBenchMessage = Annotated[
    Union[SRBenchChatCompletionMessage, ChatCompletionMessageParam],
    PlainValidator(_validate_sage_message),
    PlainSerializer(_serialize_sage_message, return_type=dict),
]
"""Union of all message types that flow through the srbench-llm stack.

- SRBenchChatCompletionMessage: assistant responses (rich, with completion_info)
- ChatCompletionMessageParam: input messages (system, user, tool dicts)

Annotated with a PlainSerializer so pydantic can round-trip the union
through JSON without choking on TypedDict validation.
"""
