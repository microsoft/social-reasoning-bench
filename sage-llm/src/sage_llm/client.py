import logging
import warnings
from typing import Any, TypeVar

import litellm
from openai.types.chat import ChatCompletionMessageParam
from pydantic import BaseModel

from .trapi.models import add_allowed_params_for_trapi
from .trapi.provider import TrapiCustomLLM

T = TypeVar("T", bound=BaseModel)

# Suppress Pydantic serialization warnings (known bug: github.com/BerriAI/litellm/issues/11759)
warnings.filterwarnings("ignore", message="Pydantic serializer warnings")

# Suppress noisy logs from litellm and dependencies
logging.getLogger("LiteLLM").setLevel(logging.WARNING)
logging.getLogger("litellm").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)
logging.getLogger("asyncio").setLevel(logging.WARNING)

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


class Completions:
    """Mimics openai.chat.completions interface."""

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        api_version: str | None = None,
        reasoning_effort: str | None = None,
    ):
        self.api_key = api_key
        self.base_url = base_url
        self.api_version = api_version
        self.reasoning_effort = reasoning_effort
        # Number of retries for requests. NOTE: we do not perform retries for trapi models.
        self.num_retries = 3

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
        effort = reasoning_effort if reasoning_effort is not None else self.reasoning_effort
        if effort is not None:
            kwargs["reasoning_effort"] = effort

        kwargs = self._add_default_kwargs(kwargs)
        kwargs = add_allowed_params_for_trapi(model, kwargs)

        model = self._handle_model_aliases(model)

        return litellm.completion(
            model=model, messages=messages, num_retries=self.num_retries, **kwargs
        )

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
        effort = reasoning_effort if reasoning_effort is not None else self.reasoning_effort
        if effort is not None:
            kwargs["reasoning_effort"] = effort

        kwargs = self._add_default_kwargs(kwargs)
        kwargs = add_allowed_params_for_trapi(model, kwargs)

        model = self._handle_model_aliases(model)

        return await litellm.acompletion(
            model=model, messages=messages, num_retries=self.num_retries, **kwargs
        )

    def parse(
        self,
        *,
        model: str,
        messages: list[ChatCompletionMessageParam],
        response_format: type[T],
        **kwargs,
    ) -> T:
        """Create a chat completion and parse the response into a Pydantic model.

        Args:
            model: Model identifier
            messages: List of message dicts with "role" and "content"
            response_format: Pydantic model class for the expected response
            **kwargs: Additional arguments passed to create

        Returns:
            Parsed instance of response_format
        """
        response = self.create(
            model=model, messages=messages, response_format=response_format, **kwargs
        )
        return response_format.model_validate_json(response.choices[0].message.content)

    async def aparse(
        self,
        *,
        model: str,
        messages: list[ChatCompletionMessageParam],
        response_format: type[T],
        **kwargs,
    ) -> T:
        """Create a chat completion and parse the response into a Pydantic model (async).

        Args:
            model: Model identifier
            messages: List of message dicts with "role" and "content"
            response_format: Pydantic model class for the expected response
            **kwargs: Additional arguments passed to acreate

        Returns:
            Parsed instance of response_format
        """
        response = await self.acreate(
            model=model, messages=messages, response_format=response_format, **kwargs
        )
        return response_format.model_validate_json(response.choices[0].message.content)


class Chat:
    """Mimics openai.chat interface."""

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        api_version: str | None = None,
        reasoning_effort: str | None = None,
    ):
        self.completions = Completions(
            api_key=api_key,
            base_url=base_url,
            api_version=api_version,
            reasoning_effort=reasoning_effort,
        )


class ModelClient:
    """Simple client mimicking the OpenAI SDK interface.

    Usage:
        from sage_llm import ModelClient

        client = ModelClient()
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
        reasoning_effort: str | None = None,
    ):
        self.chat = Chat(
            api_key=api_key,
            base_url=base_url,
            api_version=api_version,
            reasoning_effort=reasoning_effort,
        )
