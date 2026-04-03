"""Core types for sage-llm."""

from typing import Annotated, Any, Union, cast

from openai.types.chat import ChatCompletionMessage, ChatCompletionMessageParam
from openai.types.completion_usage import CompletionUsage
from pydantic import BaseModel, PlainSerializer, PlainValidator
from pydantic_core import from_json, to_json


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


def _validate_sage_message(msg: Any) -> Any:
    """Validate and discriminate SageMessage input.

    - SageChatCompletionMessage instances pass through unchanged.
    - Dicts with ``role: "assistant"`` are promoted to SageChatCompletionMessage
      so round-tripping through JSON preserves the concrete type.
    - Other dicts (system/user/tool messages) stay as plain dicts.
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
    """
    if isinstance(msg, SageChatCompletionMessage):
        return msg.model_dump(mode="json")
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
