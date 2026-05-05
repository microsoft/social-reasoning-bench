"""SageModelClient — thin wrapper over providers."""

import logging
import re
from datetime import datetime
from typing import TypeVar

from openai.types.chat import ChatCompletionToolChoiceOptionParam, ChatCompletionToolParam
from pydantic import BaseModel

from .providers import resolve_provider
from .tracing import LLMTrace, SageRequest, tracer
from .types import DEFAULT_MAX_TOKENS, SageChatCompletionMessage, SageMessage

logger = logging.getLogger(__name__)
T = TypeVar("T", bound=BaseModel)


class SageModelClient:
    """Simple client that dispatches to the right provider.

    Usage::

        import asyncio
        from sage_llm import SageModelClient

        client = SageModelClient()

        async def main():
            msg = await client.acomplete(
                model="anthropic/claude-sonnet-4-5",
                messages=[SageMessage(role="user", content="Hello")],
            )
            print(msg.content)

        asyncio.run(main())
    """

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        api_version: str | None = None,
        reasoning_effort: str | int | None = None,
        max_tokens: int = DEFAULT_MAX_TOKENS,
    ):
        self.api_key = api_key
        self.base_url = base_url
        self.api_version = api_version
        self.reasoning_effort = reasoning_effort
        self.max_tokens = max_tokens

    async def acomplete(
        self,
        model: str,
        messages: list[SageMessage],
        *,
        temperature: float | None = None,
        max_tokens: int | None = None,
        top_p: float | None = None,
        stop: str | list[str] | None = None,
        tools: list[ChatCompletionToolParam] | None = None,
        tool_choice: ChatCompletionToolChoiceOptionParam | None = None,
        reasoning_effort: str | int | None = None,
    ) -> SageChatCompletionMessage:
        resolved = _handle_model_aliases(model)
        provider, provider_model = resolve_provider(
            resolved,
            api_key=self.api_key,
            base_url=self.base_url,
            api_version=self.api_version,
        )
        effort = reasoning_effort if reasoning_effort is not None else self.reasoning_effort
        tokens = max_tokens if max_tokens is not None else self.max_tokens

        trace = LLMTrace(
            sage_request=SageRequest(
                model=resolved,
                messages=messages,
                temperature=temperature,
                max_tokens=tokens,
                top_p=top_p,
                stop=stop,
                tools=tools,
                tool_choice=tool_choice,
                reasoning_effort=effort,
            ),
            start_time=datetime.now(),
        )

        try:
            msg = await provider.acomplete(
                provider_model,
                messages,
                trace=trace,
                temperature=temperature,
                max_tokens=tokens,
                top_p=top_p,
                stop=stop,
                tools=tools,
                tool_choice=tool_choice,
                reasoning_effort=effort,
            )
            trace.sage_response = msg
            trace.status = "success"
        except Exception as e:
            trace.status = "failure"
            trace.error = str(e)
            raise
        finally:
            trace.end_time = datetime.now()
            if trace.start_time and trace.end_time:
                trace.duration_ms = (trace.end_time - trace.start_time).total_seconds() * 1000
            tracer.record(trace)

        return msg

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
    ) -> T:
        resolved = _handle_model_aliases(model)
        provider, provider_model = resolve_provider(
            resolved,
            api_key=self.api_key,
            base_url=self.base_url,
            api_version=self.api_version,
        )
        effort = reasoning_effort if reasoning_effort is not None else self.reasoning_effort
        tokens = max_tokens if max_tokens is not None else self.max_tokens
        return await provider.aparse(
            provider_model,
            messages,
            response_format,
            temperature=temperature,
            max_tokens=tokens,
            top_p=top_p,
            stop=stop,
            reasoning_effort=effort,
        )


def _handle_model_aliases(model: str) -> str:
    """Resolve convenience model aliases to provider-prefixed form.

    Args:
        model: Model string, possibly a bare alias like ``"gemini-2.5-flash"``
            or ``"claude-sonnet-4-5"``.

    Returns:
        Provider-prefixed model string (e.g. ``"gemini/gemini-2.5-flash"``).
    """
    if model.startswith("gemini-"):
        return f"gemini/{model}"
    if model.startswith("claude-"):
        model = f"anthropic/{model}"

    # Normalize Anthropic version dots to hyphens (e.g., claude-sonnet-4.5 → claude-sonnet-4-5)
    if model.startswith("anthropic/claude-"):
        name = model[len("anthropic/") :]
        normalized = re.sub(r"(\d+)\.(\d+)", r"\1-\2", name)
        model = f"anthropic/{normalized}"

    return model
