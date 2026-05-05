"""LLM trace collector.

Every trace captures four layers of the request/response lifecycle:
1. sage_request    — the Sage-typed request (model, SageMessages, kwargs)
2. provider_request  — the translated provider-specific request (SDK kwargs)
3. provider_response — the raw provider-specific response (SDK object, serialized)
4. sage_response   — the transformed Sage-typed response (SageMessage)

A single ``LLMTrace`` object is created by the client, passed to the
provider (which fills layers 2/3 and usage), then finalized by the
client (layer 4, timing, status). The completed trace is recorded on
the module-level ``tracer`` instance.

Usage:
    from sage_llm.tracing import tracer

    traces = tracer.get_traces()
    tracer.save("traces.json")
    tracer.clear()
"""

import json
import threading
from datetime import datetime
from pathlib import Path
from typing import Any

from openai.types.chat import ChatCompletionToolChoiceOptionParam, ChatCompletionToolParam
from pydantic import BaseModel, Field

from .types import DEFAULT_MAX_TOKENS, SageChatCompletionMessage, SageMessage

# ---------------------------------------------------------------------------
# Trace
# ---------------------------------------------------------------------------


class SageRequest(BaseModel):
    """Layer 1: Sage-typed request."""

    model: str
    messages: list[SageMessage] = Field(default_factory=list)
    temperature: float | None = None
    max_tokens: int = DEFAULT_MAX_TOKENS
    top_p: float | None = None
    stop: str | list[str] | None = None
    tools: list[ChatCompletionToolParam] | None = None
    tool_choice: ChatCompletionToolChoiceOptionParam | None = None
    reasoning_effort: str | int | None = None


class LLMTrace(BaseModel):
    """A single LLM call trace, built up as it flows through the stack."""

    # Timing (client fills)
    start_time: datetime | None = None
    end_time: datetime | None = None
    duration_ms: float | None = None

    # Layer 1: Sage request (client fills)
    sage_request: SageRequest | None = None

    # Layer 2: Provider request (provider fills)
    provider_name: str | None = None
    provider_request: dict[str, Any] = Field(default_factory=dict)

    # Layer 3: Provider response (provider fills)
    provider_response: dict[str, Any] = Field(default_factory=dict)

    # Layer 4: Sage response (client fills — always an assistant message)
    sage_response: SageChatCompletionMessage | None = None

    # Usage (provider fills from its native response)
    prompt_tokens: int | None = None
    completion_tokens: int | None = None
    total_tokens: int | None = None
    reasoning_tokens: int | None = None

    # Status (client fills)
    status: str | None = None  # "success" or "failure"
    error: str | None = None


# ---------------------------------------------------------------------------
# Tracer
# ---------------------------------------------------------------------------


class LLMTracer:
    """Thread-safe trace collector."""

    def __init__(self) -> None:
        self._traces: list[LLMTrace] = []
        self._lock = threading.Lock()

    def record(self, trace: LLMTrace) -> None:
        with self._lock:
            self._traces.append(trace)

    def get_traces(self) -> list[LLMTrace]:
        with self._lock:
            return list(self._traces)

    def clear(self) -> None:
        with self._lock:
            self._traces.clear()

    def count(self) -> int:
        with self._lock:
            return len(self._traces)

    def save(self, path: str | Path, indent: int = 2) -> None:
        """Save all traces to a JSON file.

        Args:
            path: Destination file path.
            indent: JSON indentation level.
        """
        data = [t.model_dump(mode="json") for t in self.get_traces()]
        Path(path).write_text(json.dumps(data, indent=indent, cls=_TraceEncoder))

    @staticmethod
    def load(path: str | Path) -> list[LLMTrace]:
        """Load traces from a JSON file.

        Args:
            path: Path to a JSON file previously written by :meth:`save`.

        Returns:
            List of :class:`LLMTrace` instances.
        """
        data = json.loads(Path(path).read_text())
        return [LLMTrace.model_validate(d) for d in data]


# Module-level instance — Python module init is thread-safe.
tracer = LLMTracer()


# ---------------------------------------------------------------------------
# Serialization
# ---------------------------------------------------------------------------


class _TraceEncoder(json.JSONEncoder):
    def default(self, o: object) -> str:
        if isinstance(o, datetime):
            return o.isoformat()
        if callable(o):
            return f"<function {getattr(o, '__name__', repr(o))}>"
        if isinstance(o, BaseModel):
            return o.model_dump(mode="json")  # type: ignore[return-value]
        return f"<non-serializable: {type(o).__name__}>"
