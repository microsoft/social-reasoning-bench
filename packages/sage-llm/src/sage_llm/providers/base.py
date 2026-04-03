"""Provider ABC."""

from abc import ABC, abstractmethod
from typing import Any, TypeVar

from openai.types.chat import ChatCompletionToolChoiceOptionParam, ChatCompletionToolParam
from pydantic import BaseModel

from ..tracing import LLMTrace
from ..types import SageChatCompletionMessage, SageMessage

T = TypeVar("T", bound=BaseModel)


class SageModelProvider(ABC):
    """Abstract base for LLM providers.

    Providers receive an ``LLMTrace`` and fill layers 2/3 (provider
    request/response) and usage fields. The client handles layers 1/4.
    """

    @abstractmethod
    def complete(
        self,
        model: str,
        messages: list[SageMessage],
        *,
        trace: LLMTrace,
        temperature: float | None = None,
        max_tokens: int | None = None,
        top_p: float | None = None,
        stop: str | list[str] | None = None,
        tools: list[ChatCompletionToolParam] | None = None,
        tool_choice: ChatCompletionToolChoiceOptionParam | None = None,
        reasoning_effort: str | int | None = None,
        num_retries: int = 3,
    ) -> SageChatCompletionMessage: ...

    @abstractmethod
    async def acomplete(
        self,
        model: str,
        messages: list[SageMessage],
        *,
        trace: LLMTrace,
        temperature: float | None = None,
        max_tokens: int | None = None,
        top_p: float | None = None,
        stop: str | list[str] | None = None,
        tools: list[ChatCompletionToolParam] | None = None,
        tool_choice: ChatCompletionToolChoiceOptionParam | None = None,
        reasoning_effort: str | int | None = None,
        num_retries: int = 3,
    ) -> SageChatCompletionMessage: ...

    @abstractmethod
    def parse(
        self,
        model: str,
        messages: list[SageMessage],
        response_format: type[T],
        *,
        temperature: float | None = None,
        max_tokens: int | None = None,
        top_p: float | None = None,
        stop: str | list[str] | None = None,
        reasoning_effort: str | int | None = None,
        num_retries: int = 3,
    ) -> T: ...

    @abstractmethod
    async def aparse(
        self,
        model: str,
        messages: list[SageMessage],
        response_format: type[T],
        *,
        temperature: float | None = None,
        max_tokens: int | None = None,
        top_p: float | None = None,
        stop: str | list[str] | None = None,
        reasoning_effort: str | int | None = None,
        num_retries: int = 3,
    ) -> T: ...
