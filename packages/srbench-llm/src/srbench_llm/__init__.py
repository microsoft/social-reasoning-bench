"""srbench-llm: LLM client library with direct provider implementations."""

__version__ = "0.1.0"

from . import concurrency
from .client import SRBenchModelClient
from .concurrency import (
    LabelMetrics,
    ProviderMetrics,
    get_label_metrics,
    get_metrics,
    with_llm_retry,
)
from .providers.base import SRBenchModelProvider
from .tracing import LLMTrace, LLMTracer, SRBenchRequest, tracer
from .types import SRBenchChatCompletionInfo, SRBenchChatCompletionMessage, SRBenchMessage

__all__ = [
    "SRBenchModelClient",
    "SRBenchModelProvider",
    "SRBenchMessage",
    "SRBenchChatCompletionMessage",
    "SRBenchChatCompletionInfo",
    "LLMTrace",
    "LLMTracer",
    "SRBenchRequest",
    "tracer",
    "concurrency",
    "ProviderMetrics",
    "LabelMetrics",
    "get_metrics",
    "get_label_metrics",
    "with_llm_retry",
]
