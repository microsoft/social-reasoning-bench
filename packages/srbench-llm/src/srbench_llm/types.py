"""Core types for srbench-llm.

The message type system has two strictly separated halves:

* **Input messages** (TypedDicts): what callers pass to
  :meth:`SRBenchModelClient.acomplete`. The :data:`SRBenchInputMessage` union
  covers system / user / assistant / tool messages, plus an extended
  :class:`SRBenchAssistantMessageParam` variant that carries provider-specific
  metadata (Anthropic ``thinking_blocks``, Gemini ``thought_parts`` /
  ``tool_call_signatures``) across turns.

* **Output messages** (Pydantic BaseModel): what providers return from
  :meth:`SRBenchModelClient.acomplete`. :class:`SRBenchChatCompletionMessage`
  is the base; providers subclass it (e.g. ``AnthropicMessage``,
  ``GoogleMessage``) to attach native fields. Calling ``model_dump(mode="json",
  exclude_none=True)`` on the BaseModel produces a
  :class:`SRBenchAssistantMessageParam`-shaped dict ready to be appended into
  the next turn's input list — field serializers handle the bytes-encoding and
  ``completion_info`` exclusion automatically.
"""

import base64
from typing import Any, TypeAlias, Union, cast

from openai.types.chat import (
    ChatCompletionAssistantMessageParam,
    ChatCompletionMessage,
    ChatCompletionSystemMessageParam,
    ChatCompletionToolMessageParam,
    ChatCompletionUserMessageParam,
)
from openai.types.completion_usage import CompletionUsage
from pydantic import BaseModel, Field, SkipValidation, field_serializer
from typing_extensions import NotRequired


class SRBenchChatCompletionInfo(BaseModel):
    """Response metadata. Kept in a single field on SRBenchChatCompletionMessage
    so it's easy to exclude when building the next turn's inputs."""

    id: str
    model: str
    finish_reason: str
    usage: CompletionUsage | None = None


class SRBenchAssistantMessageParam(ChatCompletionAssistantMessageParam, total=False):
    """Extended OpenAI assistant TypedDict carrying SRBench/provider metadata.

    Inherits every field of :class:`ChatCompletionAssistantMessageParam`
    (``role``, ``content``, ``tool_calls``, ``refusal``, …) and adds four
    optional extension keys used to round-trip provider-specific information
    across turns:

    * ``completion_info`` — :class:`SRBenchChatCompletionInfo` for this turn.
    * ``thinking_blocks`` — Anthropic native thinking blocks (signatures
      included), required to round-trip extended thinking.
    * ``thought_parts`` — Gemini 3+ thought parts with ``thought_signature``
      values that must be preserved across multi-turn tool-use conversations.
    * ``tool_call_signatures`` — per-tool-call signatures from Gemini 3+.

    Providers must strip these extension keys before handing the dict to the
    underlying SDK.
    """

    completion_info: NotRequired[SRBenchChatCompletionInfo | dict[str, Any] | None]
    thinking_blocks: NotRequired[list[dict[str, Any]] | None]
    # ``thought_signature`` values inside ``thought_parts`` and entries of
    # ``tool_call_signatures`` are base64-encoded strings of the raw Gemini
    # signature bytes. Use :func:`decode_signature` to turn them back into
    # bytes before passing to the Gemini SDK.
    thought_parts: NotRequired[list[dict[str, Any]] | None]
    tool_call_signatures: NotRequired[list[str | None] | None]


SRBenchInputMessage: TypeAlias = SkipValidation[
    Union[
        ChatCompletionSystemMessageParam,
        ChatCompletionUserMessageParam,
        SRBenchAssistantMessageParam,
        ChatCompletionToolMessageParam,
    ]
]
"""Strict TypedDict union of all messages that flow *into* the LLM stack.

The assistant variant is :class:`SRBenchAssistantMessageParam`, which extends
:class:`ChatCompletionAssistantMessageParam` with optional extension keys
(``completion_info``, ``thinking_blocks``, ``thought_parts``,
``tool_call_signatures``). A plain ``ChatCompletionAssistantMessageParam`` dict
is structurally compatible — it just omits the extension keys.

The :class:`SkipValidation` wrapper is essential: OpenAI's TypedDicts declare
``tool_calls`` as ``Iterable[...]``, and pydantic eagerly validates that into a
single-consume ``ValidatorIterator`` that gets exhausted by the first reader
(provider translation, retry, eval). Skipping validation stores the dicts
verbatim. This also avoids the pydantic smart-union serializer footgun where
having both ``ChatCompletionAssistantMessageParam`` and
:class:`SRBenchAssistantMessageParam` in a union confuses dispatch and drops
``tool_calls`` from output.
"""


# Keys produced by :meth:`SRBenchChatCompletionMessage.to_input_dict` that are
# NOT part of the standard OpenAI assistant message. Providers strip these
# before handing the dict to the underlying SDK.
SRBENCH_ASSISTANT_EXTENSION_KEYS: frozenset[str] = frozenset(
    {"completion_info", "thinking_blocks", "thought_parts", "tool_call_signatures"}
)


def encode_signature(sig: bytes | str | None) -> str | None:
    """Base64-encode a Gemini signature for storage in a TypedDict.

    The TypedDict shape is JSON-friendly; raw bytes inside ``dict[str, Any]``
    fields trip pydantic's serializer (UTF-8 decode error on binary). Strings
    pass through unchanged (they are presumed already-encoded, e.g. when a
    BaseModel was reconstructed from a JSON dump that stored the field inside
    a ``dict[str, Any]`` typed parent).
    """
    if sig is None:
        return None
    if isinstance(sig, str):
        return sig
    return base64.b64encode(sig).decode("ascii")


def decode_signature(sig: str | bytes | None) -> bytes | None:
    """Inverse of :func:`encode_signature`. Tolerates raw bytes for back-compat."""
    if sig is None:
        return None
    if isinstance(sig, bytes):
        return sig
    return base64.b64decode(sig)


class SRBenchChatCompletionMessage(ChatCompletionMessage):
    """Assistant output message produced by an LLM provider.

    Role is always ``"assistant"`` (inherited from
    :class:`ChatCompletionMessage`). Provider subclasses
    (``AnthropicMessage``, ``GoogleMessage``, ``OpenAIMessage``) extend this
    with native fields like ``thinking_blocks``.

    Field serializers shape ``model_dump`` output into a
    :class:`SRBenchAssistantMessageParam` dict:

    * ``completion_info`` is excluded (provider response metadata, not part of
      the input conversation).
    * ``tool_call_signatures`` is base64-encoded (raw bytes can't survive
      JSON serialization).
    * ``thought_parts`` has its inner ``thought_signature`` bytes
      base64-encoded.

    To feed a response into the next turn, call
    ``msg.model_dump(mode="json", exclude_none=True)`` — the result is
    structurally a :class:`SRBenchAssistantMessageParam`. The Gemini provider
    uses :func:`decode_signature` to recover the raw bytes before handing
    them to the SDK.
    """

    completion_info: SRBenchChatCompletionInfo | None = Field(default=None, exclude=True)

    # Google-specific fields that must survive serialization round-trips so
    # that thought_signature values are preserved across multi-turn tool-use
    # conversations.  Gemini 3+ models reject requests that omit these.
    thought_parts: list[dict[str, Any]] | None = None
    tool_call_signatures: list[bytes | None] | None = None

    @field_serializer("tool_call_signatures")
    def _ser_tool_call_signatures(self, v: list[bytes | None] | None) -> list[str | None] | None:
        if v is None:
            return None
        return [encode_signature(s) for s in v]

    @field_serializer("thought_parts")
    def _ser_thought_parts(self, v: list[dict[str, Any]] | None) -> list[dict[str, Any]] | None:
        """Base64-encode the bytes-valued ``thought_signature`` inside each part.

        Pydantic's default serializer doesn't know to encode bytes that sit
        inside a ``dict[str, Any]`` typed field; we do it explicitly so the
        resulting dict is JSON-safe.
        """
        if v is None:
            return None
        out: list[dict[str, Any]] = []
        for tp in v:
            encoded: dict[str, Any] = {k: val for k, val in tp.items() if k != "thought_signature"}
            sig = tp.get("thought_signature")
            if sig is not None:
                encoded["thought_signature"] = encode_signature(sig)
            out.append(encoded)
        return out

    def to_input_dict(self) -> SRBenchAssistantMessageParam:
        """Typed shim over :meth:`model_dump` for next-turn input lists.

        Field serializers (above) do the actual transformation:
        ``completion_info`` is excluded, byte-valued signatures are
        base64-encoded. This helper just narrows the return type from
        ``dict[str, Any]`` to :class:`SRBenchAssistantMessageParam`.
        """
        return cast(SRBenchAssistantMessageParam, self.model_dump(mode="json", exclude_none=True))
