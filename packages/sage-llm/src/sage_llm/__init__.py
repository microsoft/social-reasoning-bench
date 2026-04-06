"""sage-llm: LLM client library with direct provider implementations."""

__version__ = "0.1.0"

from . import concurrency
from .client import SageModelClient
from .concurrency import (
    LabelMetrics,
    ProviderMetrics,
    get_label_metrics,
    get_metrics,
    with_llm_retry,
)
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
    "concurrency",
    "ProviderMetrics",
    "LabelMetrics",
    "get_metrics",
    "get_label_metrics",
    "with_llm_retry",
]
