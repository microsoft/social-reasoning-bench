import logging
from typing import Any

import litellm
from openai.types.chat import ChatCompletionMessageParam

from .trapi.provider import TrapiCustomLLM

logger = logging.getLogger(__name__)

# Register TRAPI as a custom LiteLLM provider
_trapi_handler = TrapiCustomLLM()
if "trapi" not in litellm._custom_providers:
    litellm._custom_providers.append("trapi")
    litellm.custom_provider_map.append(
        {
            "provider": "trapi",
            "custom_handler": _trapi_handler,
        }
    )


def _drop_unsupported_params(model: str, kwargs: dict[str, Any]) -> dict[str, Any]:
    """Drop params not supported by certain providers."""
    if model.startswith("azure/") or model.startswith("trapi/"):
        if "tool_choice" in kwargs:
            logger.warning(f"Dropping unsupported 'tool_choice' parameter for model {model}")
            kwargs = kwargs.copy()
            kwargs.pop("tool_choice")
    return kwargs


class Completions:
    """Mimics openai.chat.completions interface."""

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        api_version: str | None = None,
    ):
        self.api_key = api_key
        self.base_url = base_url
        self.api_version = api_version

    def _add_default_kwargs(self, kwargs: dict[str, Any]):
        # Use instance defaults if not provided in kwargs
        if "api_key" not in kwargs and self.api_key is not None:
            kwargs["api_key"] = self.api_key
        if "base_url" not in kwargs and self.base_url is not None:
            kwargs["base_url"] = self.base_url
        if "api_version" not in kwargs and self.api_version is not None:
            kwargs["api_version"] = self.api_version

        return kwargs

    def _handle_model_aliases(self, model: str) -> str:
        if model.startswith("gemini-"):
            # Prefix the litellm-expected provider prefix
            return f"gemini/{model}"
        elif model.startswith("claude-"):
            return f"anthropic/{model}"
        else:
            return model

    def create(
        self,
        *,
        model: str,
        messages: list[ChatCompletionMessageParam],
        reasoning_effort: str | None = None,
        **kwargs,
    ) -> Any:
        """Create a chat completion.

        Args:
            model: Model identifier (e.g., "trapi/gcr/shared/gpt-4.1")
            messages: List of message dicts with "role" and "content"
            reasoning_effort: Reasoning effort level for supported models (gpt-5.x, gemini)
            **kwargs: Additional arguments passed to completion

        Returns:
            ModelResponse from litellm
        """
        if reasoning_effort is not None:
            kwargs["reasoning_effort"] = reasoning_effort

        kwargs = _drop_unsupported_params(model, kwargs)
        kwargs = self._add_default_kwargs(kwargs)

        model = self._handle_model_aliases(model)

        return litellm.completion(model=model, messages=messages, **kwargs)

    async def acreate(
        self,
        *,
        model: str,
        messages: list[ChatCompletionMessageParam],
        reasoning_effort: str | None = None,
        **kwargs,
    ) -> Any:
        """Create a chat completion asynchronously.

        Args:
            model: Model identifier (e.g., "trapi/gcr/shared/gpt-4.1")
            messages: List of message dicts with "role" and "content"
            reasoning_effort: Reasoning effort level for supported models (gpt-5.x, gemini)
            **kwargs: Additional arguments passed to acompletion

        Returns:
            ModelResponse from litellm
        """
        if reasoning_effort is not None:
            kwargs["reasoning_effort"] = reasoning_effort

        kwargs = _drop_unsupported_params(model, kwargs)
        kwargs = self._add_default_kwargs(kwargs)

        model = self._handle_model_aliases(model)

        return await litellm.acompletion(model=model, messages=messages, **kwargs)


class Chat:
    """Mimics openai.chat interface."""

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        api_version: str | None = None,
    ):
        self.completions = Completions(api_key=api_key, base_url=base_url, api_version=api_version)


class Client:
    """Simple client mimicking the OpenAI SDK interface.

    Usage:
        from sage_llm import Client

        client = Client()
        response = client.chat.completions.create(
            model="trapi/gcr/shared/gpt-4.1",
            messages=[{"role": "user", "content": "Hello"}]
        )
        print(response.choices[0].message.content)
    """

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        api_version: str | None = None,
    ):
        self.chat = Chat(api_key=api_key, base_url=base_url, api_version=api_version)
