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
  ``GoogleMessage``) to attach native fields. Calling ``to_input_dict()``
  produces a :class:`SRBenchAssistantMessageParam`-shaped dict ready to be
  appended into the next turn's input list.
"""

from collections.abc import Iterable, Mapping
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
    * ``thought_parts`` — Gemini 3+ thought parts. Each part's
      ``thought_signature`` value is raw ``bytes``.
    * ``tool_call_signatures`` — per-tool-call signatures from Gemini 3+,
      as raw ``bytes``.

    The signature fields hold raw bytes because they only live in-memory —
    parent result/checkpoint models strip them before JSON serialization
    (see ``strip_signatures_from_messages``).

    Providers must strip these extension keys before handing the dict to the
    underlying SDK.
    """

    completion_info: NotRequired[SRBenchChatCompletionInfo | dict[str, Any] | None]
    thinking_blocks: NotRequired[list[dict[str, Any]] | None]
    thought_parts: NotRequired[list[dict[str, Any]] | None]
    tool_call_signatures: NotRequired[list[bytes | None] | None]


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


# Extension keys whose values are raw bytes that can't be JSON-serialized.
# Parent result/checkpoint models strip these before disk write — the
# signatures only matter mid-conversation, not across restarts.
SRBENCH_SIGNATURE_KEYS: frozenset[str] = frozenset({"thought_parts", "tool_call_signatures"})


def strip_signatures_from_messages(
    messages: Iterable[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    """Return messages with bytes-bearing signature keys removed.

    Use as a ``field_serializer(..., when_used="json")`` on any pydantic field
    that holds a ``list[SRBenchInputMessage]`` and gets dumped to JSON
    (results files, checkpoints, traces). The signatures are only useful
    inside a single in-memory task lifecycle.
    """
    return [{k: v for k, v in msg.items() if k not in SRBENCH_SIGNATURE_KEYS} for msg in messages]


class SRBenchChatCompletionMessage(ChatCompletionMessage):
    """Assistant output message produced by an LLM provider.

    Role is always ``"assistant"`` (inherited from
    :class:`ChatCompletionMessage`). Provider subclasses
    (``AnthropicMessage``, ``GoogleMessage``, ``OpenAIMessage``) extend this
    with native fields like ``thinking_blocks``.

    ``completion_info`` is excluded from ``model_dump`` (response metadata,
    not part of the input conversation). The bytes-valued signature fields
    (``thought_parts`` and ``tool_call_signatures``) are dropped on JSON
    serialization — they only matter in-memory for the current task and
    are not worth round-tripping through disk.

    To feed a response into the next turn, call :meth:`to_input_dict`.
    """

    completion_info: SRBenchChatCompletionInfo | None = Field(default=None, exclude=True)

    # Google-specific fields used in-memory to round-trip thought_signature
    # values across multi-turn tool-use conversations.  Gemini 3+ models
    # reject requests that omit these.  Dropped at JSON-serialization time.
    thought_parts: list[dict[str, Any]] | None = None
    tool_call_signatures: list[bytes | None] | None = None

    @field_serializer("tool_call_signatures", when_used="json")
    def _drop_tool_call_signatures(self, _v: list[bytes | None] | None) -> None:
        return None

    @field_serializer("thought_parts", when_used="json")
    def _drop_thought_parts(self, _v: list[dict[str, Any]] | None) -> None:
        return None

    def to_input_dict(self) -> SRBenchAssistantMessageParam:
        """Dump this message as a dict ready for the next turn's input list.

        Uses ``mode="python"`` so raw bytes survive in ``thought_parts`` and
        ``tool_call_signatures`` — providers consume them directly.
        ``completion_info`` is excluded via the Field declaration.
        """
        return cast(SRBenchAssistantMessageParam, self.model_dump(mode="python", exclude_none=True))
