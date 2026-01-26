from typing import Any

import litellm
from openai.types.chat import ChatCompletionMessageParam

from .trapi.provider import TrapiCustomLLM

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


# Params that TRAPI supports (Azure OpenAI backend)
TRAPI_SUPPORTED_PARAMS = [
    "frequency_penalty",
    "logit_bias",
    "logprobs",
    "top_logprobs",
    "max_tokens",
    "max_completion_tokens",
    "n",
    "presence_penalty",
    "response_format",
    "seed",
    "stop",
    "stream",
    "stream_options",
    "temperature",
    "top_p",
    "tools",
    "tool_choice",
    "parallel_tool_calls",
    "user",
    "reasoning_effort",
    "extra_body",
]


def _add_allowed_params_for_trapi(model: str, kwargs: dict[str, Any]) -> dict[str, Any]:
    """Add allowed_openai_params for trapi models to bypass LiteLLM validation."""
    if model.startswith("trapi/"):
        # Tell LiteLLM to allow these params through without validation
        kwargs["allowed_openai_params"] = TRAPI_SUPPORTED_PARAMS
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

        kwargs = self._add_default_kwargs(kwargs)
        kwargs = _add_allowed_params_for_trapi(model, kwargs)

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

        kwargs = self._add_default_kwargs(kwargs)
        kwargs = _add_allowed_params_for_trapi(model, kwargs)

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
