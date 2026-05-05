"""Core types for sage-llm."""

from typing import Annotated, Any, Union, cast

from openai.types.chat import ChatCompletionMessage, ChatCompletionMessageParam
from openai.types.completion_usage import CompletionUsage
from pydantic import BaseModel, PlainSerializer, PlainValidator
from pydantic_core import from_json, to_json

# Default max output tokens used by the client and providers when the caller
# doesn't specify one. Sized below GPT-4.1's output-token cap so the same
# default works across all currently-supported providers.
DEFAULT_MAX_TOKENS = 32_000


class SageChatCompletionInfo(BaseModel):
    """Response metadata. Kept in a single field on SageChatCompletionMessage
    so it's easy to exclude when building the next turn's inputs."""

    id: str
    model: str
    finish_reason: str
    usage: CompletionUsage | None = None


class SageChatCompletionMessage(ChatCompletionMessage):
    """Assistant message with response metadata.

    Role is always ``"assistant"`` (inherited from ChatCompletionMessage).
    Provider subclasses (AnthropicMessage, GoogleMessage, etc.) extend this
    with provider-specific fields like thinking_blocks.
    """

    completion_info: SageChatCompletionInfo | None = None

    # Google-specific fields that must survive serialization round-trips so
    # that thought_signature values are preserved across multi-turn tool-use
    # conversations.  Gemini 3+ models reject requests that omit these.
    thought_parts: list[dict[str, Any]] | None = None
    tool_call_signatures: list[bytes | None] | None = None


def _validate_sage_message(msg: Any) -> Any:
    """Validate and discriminate SageMessage input.

    - SageChatCompletionMessage instances pass through unchanged.
    - Dicts with ``role: "assistant"`` are promoted to SageChatCompletionMessage
      so round-tripping through JSON preserves the concrete type.
    - Other dicts (system/user/tool messages) stay as plain dicts.

    Args:
        msg: Raw message value — a :class:`BaseModel`, dict, or other type.

    Returns:
        The validated message, possibly promoted to
        :class:`SageChatCompletionMessage`.

    Raises:
        ValueError: If *msg* is not a BaseModel or dict.
    """
    if isinstance(msg, SageChatCompletionMessage):
        return msg
    if isinstance(msg, BaseModel):
        # Some other pydantic model (e.g. ChatCompletionMessage from openai) — convert
        return msg
    if isinstance(msg, dict):
        if msg.get("role") == "assistant":
            return SageChatCompletionMessage.model_validate(msg)
        return msg
    raise ValueError(
        f"SageMessage must be a BaseModel or dict, got {type(msg).__name__}: {msg!r:.200}"
    )


def _serialize_sage_message(
    msg: SageChatCompletionMessage | ChatCompletionMessageParam,
) -> dict[str, Any]:
    """Serialize any SageMessage variant to a JSON-safe dict.

    Handles:
    - Pydantic models (SageChatCompletionMessage) → model_dump
    - TypedDicts / plain dicts (ChatCompletionMessageParam) → recursive serialization
    - Unexpected types → string fallback

    Args:
        msg: A :class:`SageChatCompletionMessage` or
            :class:`ChatCompletionMessageParam` dict.

    Returns:
        JSON-safe dict representation of the message.

    Raises:
        ValueError: If *msg* is not a supported message type.
    """
    if isinstance(msg, SageChatCompletionMessage):
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
    raise ValueError(f"Cannot serialize SageMessage of type {type(msg).__name__}: {msg!r:.200}")


SageMessage = Annotated[
    Union[SageChatCompletionMessage, ChatCompletionMessageParam],
    PlainValidator(_validate_sage_message),
    PlainSerializer(_serialize_sage_message, return_type=dict),
]
"""Union of all message types that flow through the sage-llm stack.

- SageChatCompletionMessage: assistant responses (rich, with completion_info)
- ChatCompletionMessageParam: input messages (system, user, tool dicts)

Annotated with a PlainSerializer so pydantic can round-trip the union
through JSON without choking on TypedDict validation.
"""
