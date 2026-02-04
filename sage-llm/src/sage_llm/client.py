import logging
import warnings
from typing import Any, TypeVar

import litellm
from litellm.types.utils import Choices, ModelResponse
from openai.types.chat import ChatCompletionMessageParam
from pydantic import BaseModel

from .trapi.provider import TrapiCustomLLM, add_allowed_params_for_trapi

T = TypeVar("T", bound=BaseModel)
logger = logging.getLogger(__name__)

# Suppress Pydantic serialization warnings (known bug: github.com/BerriAI/litellm/issues/11759)
warnings.filterwarnings("ignore", message="Pydantic serializer warnings")

# Suppress noisy logs from litellm and dependencies
logging.getLogger("LiteLLM").setLevel(logging.WARNING)
logging.getLogger("litellm").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)
logging.getLogger("asyncio").setLevel(logging.WARNING)
logging.getLogger("azure.identity").setLevel(logging.WARNING)

# Enable automatic handling of thinking blocks in multi-turn conversations
litellm.modify_params = True

# Register TRAPI as a custom LiteLLM provider
_trapi_handler = TrapiCustomLLM()
if "trapi" not in litellm._custom_providers:
    litellm._custom_providers.append("trapi")
if "trapi" not in litellm.provider_list:
    litellm.provider_list.append("trapi")
if not any(item.get("provider") == "trapi" for item in litellm.custom_provider_map):
    litellm.custom_provider_map.append(
        {
            "provider": "trapi",
            "custom_handler": _trapi_handler,
        }
    )


class Completions:
    """Mimics openai.chat.completions interface with reasoning support.

    Features:
    - Unified `reasoning_content` on response messages (works for all providers)
    - Thinking preservation via `previous_response_id` for multi-turn conversations
    - Automatic caching of responses with reasoning content
    """

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        api_version: str | None = None,
        reasoning_effort: str | int = "none",
        response_cache: dict[str, ModelResponse] | None = None,
    ):
        self.api_key = api_key
        self.base_url = base_url
        self.api_version = api_version
        self.reasoning_effort = reasoning_effort
        # Number of retries for requests. NOTE: we do not perform retries for trapi models.
        self.num_retries = 3
        # Cache for responses with thinking content, keyed by response ID
        self._response_cache = response_cache if response_cache is not None else {}

    def _add_default_kwargs(self, kwargs: dict[str, Any]) -> dict[str, Any]:
        # Use instance defaults if not provided in kwargs
        if "api_key" not in kwargs and self.api_key is not None:
            kwargs["api_key"] = self.api_key
        if "base_url" not in kwargs and self.base_url is not None:
            kwargs["base_url"] = self.base_url
        if "api_version" not in kwargs and self.api_version is not None:
            kwargs["api_version"] = self.api_version

        return kwargs

    def _handle_model_aliases(self, model: str) -> str:
        import re

        if model.startswith("gemini-"):
            # Prefix the litellm-expected provider prefix
            model = f"gemini/{model}"
        elif model.startswith("claude-"):
            model = f"anthropic/{model}"

        # Normalize Anthropic version dots to hyphens (e.g., claude-sonnet-4.5 -> claude-sonnet-4-5)
        # LiteLLM only recognizes hyphen versions as supporting reasoning
        if model.startswith("anthropic/claude-"):
            model_name = model[len("anthropic/") :]
            normalized = re.sub(r"(\d+)\.(\d+)", r"\1-\2", model_name)
            model = f"anthropic/{normalized}"

        return model

    def _translate_reasoning_effort(self, model: str, kwargs: dict[str, Any]) -> dict[str, Any]:
        """Translate reasoning_effort to provider-specific parameters.

        Validates that the type matches what the model expects:
        - Integer budget: Anthropic (non-Opus), Gemini 2.5
        - String effort: Anthropic Opus 4.5, OpenAI o-series, Gemini 3+, TRAPI
        - "none" string: Omitted entirely (not sent to API)
        """
        reasoning_effort = kwargs.pop("reasoning_effort", None)
        if reasoning_effort is None or reasoning_effort == "none":
            # Don't send reasoning_effort to API when disabled
            return kwargs

        is_int = isinstance(reasoning_effort, int)

        if model.startswith("anthropic/"):
            if "opus-4-5" in model or "opus-4.5" in model:
                # Opus 4.5: requires string effort
                if is_int:
                    raise ValueError(
                        f"Model {model} requires string reasoning_effort ('low', 'medium', 'high'), "
                        f"got integer {reasoning_effort}"
                    )
                kwargs["reasoning_effort"] = reasoning_effort
            else:
                # Other Anthropic: requires integer budget via thinking param
                if is_int:
                    kwargs["thinking"] = {"type": "enabled", "budget_tokens": reasoning_effort}
                else:
                    raise ValueError(
                        f"Model {model} requires integer reasoning_effort (budget tokens), "
                        f"got string '{reasoning_effort}'"
                    )
        elif model.startswith("gemini/"):
            if "2.5" in model or "2-5" in model:
                # Gemini 2.5: integer budget via thinking param
                if is_int:
                    kwargs["thinking"] = {"type": "enabled", "budget_tokens": reasoning_effort}
                else:
                    raise ValueError(
                        f"Model {model} requires integer reasoning_effort (budget tokens), "
                        f"got string '{reasoning_effort}'"
                    )
            else:
                # Gemini 3+: supports both string effort and integer budget
                if is_int:
                    kwargs["thinking"] = {"type": "enabled", "budget_tokens": reasoning_effort}
                else:
                    kwargs["reasoning_effort"] = reasoning_effort
        else:
            # OpenAI and compatible providers: only o-series and gpt-5.x support reasoning_effort
            # Extract model name (handle prefixes like "trapi/", "azure/", etc.)
            model_name = model.split("/")[-1].lower()
            supports_reasoning = (
                model_name.startswith("o1")
                or model_name.startswith("o3")
                or model_name.startswith("gpt-5")
            )

            if not supports_reasoning:
                raise ValueError(
                    f"Model {model} does not support reasoning_effort. "
                    f"Only o1, o3, and gpt-5.x models support this parameter."
                )
            elif is_int:
                raise ValueError(
                    f"Model {model} requires string reasoning_effort ('low', 'medium', 'high'), "
                    f"got integer {reasoning_effort}"
                )
            else:
                kwargs["reasoning_effort"] = reasoning_effort

        return kwargs

    def _inject_anthropic_thinking(
        self,
        messages: list[ChatCompletionMessageParam],
        previous_response_id: str,
        model: str,
    ) -> list[ChatCompletionMessageParam]:
        """Inject thinking from a cached response into messages.

        For Anthropic models, injects structured thinking blocks with signature.
        For other providers, litellm.modify_params handles thinking automatically.

        The thinking blocks are retrieved from the response cache using previous_response_id,
        then injected into the last assistant message in the messages list.

        Example:
            Cached response contains:
                thinking_blocks: [{"type": "thinking", "thinking": "...", "signature": "..."}]

            Messages before:
                [{"role": "assistant", "content": "Here is my answer"}]

            Messages after:
                [{"role": "assistant", "content": [
                    {"type": "thinking", "thinking": "...", "signature": "..."},
                    {"type": "text", "text": "Here is my answer"}
                ]}]
        """
        prev_response = self._response_cache.get(previous_response_id)
        if not prev_response:
            logger.warning(f"previous_response_id '{previous_response_id}' not found in cache")
            return messages

        # Only Anthropic requires manual thinking injection
        if not model.startswith("anthropic/"):
            return messages

        if not prev_response.choices:
            return messages

        choice = prev_response.choices[0]
        if not isinstance(choice, Choices):
            return messages
        prev_message = choice.message
        thinking_blocks = getattr(prev_message, "thinking_blocks", None)

        if not thinking_blocks:
            return messages

        # Find the last assistant message and inject thinking
        messages = list(messages)  # Make a copy
        for i in range(len(messages) - 1, -1, -1):
            if messages[i].get("role") == "assistant":
                original_content = messages[i].get("content", "")
                messages[i] = {
                    "role": "assistant",
                    "content": [
                        *thinking_blocks,
                        {
                            "type": "text",
                            "text": original_content if isinstance(original_content, str) else "",
                        },
                    ],
                }
                break

        return messages

    def _cache_response(self, response: ModelResponse) -> None:
        """Cache the response by ID for potential thinking preservation."""
        if not response.id:
            import hashlib

            import pydantic_core

            response.id = hashlib.sha256(pydantic_core.to_json(response)).hexdigest()
        self._response_cache[response.id] = response

    def create(
        self,
        *,
        model: str,
        messages: list[ChatCompletionMessageParam],
        reasoning_effort: str | int | None = None,
        previous_response_id: str | None = None,
        **kwargs,
    ) -> "ModelResponse":
        """Create a chat completion.

        Args:
            model: Model identifier (e.g., "trapi/msraif/shared/gpt-4.1")
            messages: List of message dicts with "role" and "content"
            reasoning_effort: Reasoning effort level for supported models.
                Defaults to the instance's reasoning_effort if not provided.
            previous_response_id: ID of a previous response to preserve thinking from.
                The thinking content will be injected into the last assistant message.
            **kwargs: Additional arguments passed to completion

        Returns:
            ModelResponse from litellm. Access reasoning via:
            - response.choices[0].message.reasoning_content (all providers)
            - response.choices[0].message.thinking_blocks (Anthropic only)
        """
        # Use instance default if not provided
        if reasoning_effort is None:
            reasoning_effort = self.reasoning_effort
        kwargs["reasoning_effort"] = reasoning_effort

        # Resolve model aliases and translate reasoning_effort to provider-specific params
        resolved_model = self._handle_model_aliases(model)
        kwargs = self._translate_reasoning_effort(resolved_model, kwargs)

        # Inject thinking from previous response if provided
        if previous_response_id:
            messages = self._inject_anthropic_thinking(
                messages, previous_response_id, resolved_model
            )

        kwargs = self._add_default_kwargs(kwargs)
        kwargs = add_allowed_params_for_trapi(model, kwargs)

        response = litellm.completion(
            model=resolved_model, messages=messages, num_retries=self.num_retries, **kwargs
        )

        # Auto-cache if response has thinking content
        if isinstance(response, ModelResponse):
            self._cache_response(response)

        return response  # type: ignore[return-value]

    async def acreate(
        self,
        *,
        model: str,
        messages: list[ChatCompletionMessageParam],
        reasoning_effort: str | int | None = None,
        previous_response_id: str | None = None,
        **kwargs,
    ) -> ModelResponse:
        """Create a chat completion asynchronously.

        Args:
            model: Model identifier (e.g., "trapi/msraif/shared/gpt-4.1")
            messages: List of message dicts with "role" and "content"
            reasoning_effort: Reasoning effort level for supported models.
                Defaults to the instance's reasoning_effort if not provided.
            previous_response_id: ID of a previous response to preserve thinking from.
                The thinking content will be injected into the last assistant message.
            **kwargs: Additional arguments passed to acompletion

        Returns:
            ModelResponse from litellm. Access reasoning via:
            - response.choices[0].message.reasoning_content (all providers)
            - response.choices[0].message.thinking_blocks (Anthropic only)
        """
        # Use instance default if not provided
        if reasoning_effort is None:
            reasoning_effort = self.reasoning_effort
        kwargs["reasoning_effort"] = reasoning_effort

        # Resolve model aliases and translate reasoning_effort to provider-specific params
        resolved_model = self._handle_model_aliases(model)
        kwargs = self._translate_reasoning_effort(resolved_model, kwargs)

        # Inject thinking from previous response if provided
        if previous_response_id:
            messages = self._inject_anthropic_thinking(
                messages, previous_response_id, resolved_model
            )

        kwargs = self._add_default_kwargs(kwargs)
        kwargs = add_allowed_params_for_trapi(model, kwargs)

        response = await litellm.acompletion(
            model=resolved_model, messages=messages, num_retries=self.num_retries, **kwargs
        )

        # Auto-cache if response has thinking content
        if isinstance(response, ModelResponse):
            self._cache_response(response)

        return response  # type: ignore[return-value]

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
        choice = response.choices[0]
        assert isinstance(choice, Choices) and choice.message.content is not None
        return response_format.model_validate_json(choice.message.content)

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
        choice = response.choices[0]
        assert isinstance(choice, Choices) and choice.message.content is not None
        return response_format.model_validate_json(choice.message.content)


class Chat:
    """Mimics openai.chat interface."""

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        api_version: str | None = None,
        reasoning_effort: str | int = "none",
        response_cache: dict[str, ModelResponse] | None = None,
    ):
        self.completions = Completions(
            api_key=api_key,
            base_url=base_url,
            api_version=api_version,
            reasoning_effort=reasoning_effort,
            response_cache=response_cache,
        )


class ModelClient:
    """Simple client mimicking the OpenAI SDK interface with reasoning support.

    Usage:
        from sage_llm import ModelClient

        client = ModelClient()  # Default: reasoning_effort="none" (thinking disabled)
        client = ModelClient(reasoning_effort=8000)  # Enable thinking with budget

        # Turn 1: Get response with reasoning
        response = client.chat.completions.create(
            model="anthropic/claude-opus-4-5",
            messages=[{"role": "user", "content": "Solve step by step"}],
        )
        print(response.choices[0].message.content)           # Final answer
        print(response.choices[0].message.reasoning_content) # Reasoning (all providers!)

        # Turn 2: Preserve thinking across turns
        response2 = client.chat.completions.create(
            model="anthropic/claude-opus-4-5",
            messages=[
                {"role": "user", "content": "Solve step by step"},
                {"role": "assistant", "content": response.choices[0].message.content},
                {"role": "user", "content": "Explain step 2"},
            ],
            previous_response_id=response.id,  # Automatic thinking injection
        )
    """

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        api_version: str | None = None,
        reasoning_effort: str | int = "none",
    ):
        # Shared cache for responses with thinking content
        self._response_cache: dict[str, ModelResponse] = {}

        self.chat = Chat(
            api_key=api_key,
            base_url=base_url,
            api_version=api_version,
            reasoning_effort=reasoning_effort,
            response_cache=self._response_cache,
        )

    def clear_response_cache(self) -> None:
        """Clear all cached thinking responses."""
        self._response_cache.clear()

    def get_response_cache_size(self) -> int:
        """Get the number of cached thinking responses."""
        return len(self._response_cache)
