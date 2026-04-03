"""sage-llm: LLM client library with direct provider implementations."""

__version__ = "0.1.0"

from .client import SageModelClient
from .providers.base import SageModelProvider
from .tracing import LLMTrace, LLMTracer, SageRequest, tracer
from .types import SageChatCompletionInfo, SageChatCompletionMessage, SageMessage

__all__ = [
    "SageModelClient",
    "SageModelProvider",
    "SageMessage",
    "SageChatCompletionMessage",
    "SageChatCompletionInfo",
    "LLMTrace",
    "LLMTracer",
    "SageRequest",
    "tracer",
]
