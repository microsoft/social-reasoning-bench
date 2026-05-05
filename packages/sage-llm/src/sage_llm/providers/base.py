"""Provider ABC."""

from abc import ABC, abstractmethod
from typing import Any, TypeVar

from openai.types.chat import ChatCompletionToolChoiceOptionParam, ChatCompletionToolParam
from pydantic import BaseModel

from ..tracing import LLMTrace
from ..types import DEFAULT_MAX_TOKENS, SageChatCompletionMessage, SageMessage

T = TypeVar("T", bound=BaseModel)


class SageModelProvider(ABC):
    """Abstract base for LLM providers.

    Providers receive an ``LLMTrace`` and fill layers 2/3 (provider
    request/response) and usage fields. The client handles layers 1/4.

    Subclasses **must** set ``PROVIDER_KEY`` to a unique string identifier
    (e.g. ``"openai"``, ``"azure"``).  This key is used by the concurrency
    module to maintain independent semaphore pools per provider.
    """

    PROVIDER_KEY: str

    @abstractmethod
    async def acomplete(
        self,
        model: str,
        messages: list[SageMessage],
        *,
        trace: LLMTrace,
        temperature: float | None = None,
        max_tokens: int = DEFAULT_MAX_TOKENS,
        top_p: float | None = None,
        stop: str | list[str] | None = None,
        tools: list[ChatCompletionToolParam] | None = None,
        tool_choice: ChatCompletionToolChoiceOptionParam | None = None,
        reasoning_effort: str | int | None = None,
    ) -> SageChatCompletionMessage: ...

    @abstractmethod
    async def aparse(
        self,
        model: str,
        messages: list[SageMessage],
        response_format: type[T],
        *,
        temperature: float | None = None,
        max_tokens: int = DEFAULT_MAX_TOKENS,
        top_p: float | None = None,
        stop: str | list[str] | None = None,
        reasoning_effort: str | int | None = None,
    ) -> T: ...
