"""Pooled Azure OpenAI provider — load-balances across multiple endpoints.

Uses the standard OpenAI SDK with Azure base URLs (``/openai/v1/``).
Each endpoint is a regular ``AsyncOpenAI`` client with a different
``base_url``.  Rotates round-robin, marks unhealthy on transient errors.

Configuration via ``SAGE_AZURE_POOL_PATH`` (colon-delimited, like PATH),
pointing to directories or JSON/YAML files.  Each file is named after
the model (e.g. ``gpt-4.1.json``) and contains a list of endpoints::

    [
      {"azure_endpoint": "https://eastus.openai.azure.com",
       "deployment": "gpt-4.1-endpoint-7"},
      ...
    ]

Model string: ``azure_pool/gpt-4.1``.
"""

from __future__ import annotations

import asyncio
import json
import logging
import os
import time
from contextlib import asynccontextmanager
from typing import Any, TypeVar

import openai
from openai.types.chat import (
    ChatCompletion,
    ChatCompletionToolChoiceOptionParam,
    ChatCompletionToolParam,
)
from pydantic import BaseModel

from ..concurrency import has_capacity, llm_gate, parse_retry_after, record_usage, with_llm_retry
from ..tracing import LLMTrace
from ..types import SageChatCompletionMessage, SageMessage
from .base import SageModelProvider
from .openai import (
    _pydantic_to_json_schema,
    _to_openai_message,
    _to_openai_messages,
)

logger = logging.getLogger(__name__)
T = TypeVar("T", bound=BaseModel)

POOL_PATH_ENV = "SAGE_AZURE_POOL_PATH"
COGNITIVE_SERVICES_SCOPE = "https://cognitiveservices.azure.com/.default"

# ---------------------------------------------------------------------------
# Config models
# ---------------------------------------------------------------------------


class EndpointConfig(BaseModel):
    """Configuration for a single Azure OpenAI endpoint."""

    azure_endpoint: str
    deployment: str
    api_key: str | None = None
    api_version: str = "2025-01-01-preview"


class PoolConfig(BaseModel):
    """Configuration loaded from a per-model JSON/YAML file."""

    endpoints: list[EndpointConfig]

    @classmethod
    def from_file(cls, path: Any) -> PoolConfig:
        from pathlib import Path as P

        p = P(path)
        raw = p.read_text()
        if p.suffix in (".yaml", ".yml"):
            try:
                import yaml
            except ImportError as exc:
                raise ImportError("pip install pyyaml for YAML config support") from exc
            data = yaml.safe_load(raw)
        else:
            data = json.loads(raw)

        if isinstance(data, list):
            data = {"endpoints": data}
        return cls.model_validate(data)


def _load_pool_config(raw_path: str, model: str) -> PoolConfig | None:
    """Search PATH-like *raw_path* for a config file matching *model*."""
    from pathlib import Path as P

    candidates: list[P] = []
    for entry in raw_path.split(":"):
        entry = entry.strip()
        if not entry:
            continue
        p = P(entry)
        if p.is_file():
            candidates.append(p)
        elif p.is_dir():
            candidates.extend(sorted(p.iterdir()))

    for path in candidates:
        if path.stem == model and path.suffix in (".json", ".yaml", ".yml"):
            return PoolConfig.from_file(path)
    return None


# ---------------------------------------------------------------------------
# Azure AD token provider
# ---------------------------------------------------------------------------


def _get_ad_token_provider() -> Any:
    """Return an async token provider compatible with the OpenAI SDK.

    The SDK's ``AsyncOpenAI`` expects ``api_key`` to be either a string
    or an ``async`` callable returning a string.  Azure's
    ``get_bearer_token_provider`` returns a *sync* callable, so we wrap
    it in an async wrapper.
    """
    from azure.identity import (
        AzureCliCredential,
        ChainedTokenCredential,
        DefaultAzureCredential,
        get_bearer_token_provider,
    )

    cred = ChainedTokenCredential(
        AzureCliCredential(),
        DefaultAzureCredential(
            exclude_cli_credential=True,
            exclude_environment_credential=True,
            exclude_shared_token_cache_credential=True,
            exclude_developer_cli_credential=True,
            exclude_powershell_credential=True,
            exclude_interactive_browser_credential=True,
            exclude_visual_studio_code_credentials=True,
            managed_identity_client_id=os.environ.get("DEFAULT_IDENTITY_CLIENT_ID"),
        ),
    )
    sync_provider = get_bearer_token_provider(cred, COGNITIVE_SERVICES_SCOPE)

    async def async_provider() -> str:
        return sync_provider()

    return async_provider


# ---------------------------------------------------------------------------
# Client cache (per base_url)
# ---------------------------------------------------------------------------

_CLIENT_CACHE: dict[str, openai.AsyncOpenAI] = {}
_POOL_CACHE: dict[str, Any] = {}  # model → PooledAzureProvider


def _get_client(
    base_url: str,
    api_key: str | Any | None,
) -> openai.AsyncOpenAI:
    """Return a cached AsyncOpenAI client for the given base URL.

    *api_key* can be a string or a callable token provider — the OpenAI
    SDK accepts both.
    """
    if base_url in _CLIENT_CACHE:
        return _CLIENT_CACHE[base_url]
    client = openai.AsyncOpenAI(
        base_url=base_url,
        api_key=api_key,
        max_retries=0,
        timeout=120.0,
    )
    _CLIENT_CACHE[base_url] = client
    return client


# ---------------------------------------------------------------------------
# Endpoint state + provider
# ---------------------------------------------------------------------------


def _build_kwargs(**params: Any) -> dict[str, Any]:
    return {k: v for k, v in params.items() if v is not None}


class _EndpointState:
    """Tracks health of a single Azure endpoint."""

    def __init__(self, client: openai.AsyncOpenAI, deployment: str, label: str) -> None:
        self.client = client
        self.deployment = deployment
        self.label = label
        self.healthy_at: float = 0.0
        self.error_count: int = 0
        self._unhealthy_lock = asyncio.Lock()

    @property
    def is_healthy(self) -> bool:
        return time.monotonic() >= self.healthy_at

    async def mark_unhealthy(self, cooldown: float) -> None:
        if self._unhealthy_lock.locked():
            return  # another coroutine is already handling this
        async with self._unhealthy_lock:
            if not self.is_healthy:
                return  # already marked by someone else
            self.healthy_at = time.monotonic() + cooldown
            self.error_count += 1
            logger.info(
                "azure_pool: %s unhealthy for %.0fs (errors: %d)",
                self.label,
                cooldown,
                self.error_count,
            )


class PooledAzureProvider(SageModelProvider):
    """Azure OpenAI provider that load-balances across multiple endpoints.

    Uses the standard OpenAI SDK with Azure ``/openai/v1/`` base URLs.
    """

    PROVIDER_KEY = "azure_pool"

    def __init__(self, config: PoolConfig) -> None:
        if not config.endpoints:
            raise ValueError("PooledAzureProvider requires at least one endpoint")
        self._endpoints: list[_EndpointState] = []
        ad_token_provider = None
        for ep in config.endpoints:
            api_key: Any = ep.api_key
            if not api_key:
                if ad_token_provider is None:
                    ad_token_provider = _get_ad_token_provider()
                api_key = ad_token_provider
            base = ep.azure_endpoint.rstrip("/")
            base_url = f"{base}/openai/v1/"
            client = _get_client(base_url, api_key)
            label = f"{ep.azure_endpoint}/{ep.deployment}"
            self._endpoints.append(_EndpointState(client, ep.deployment, label))
        self._next = 0
        logger.info("azure_pool: %d endpoints configured", len(self._endpoints))

    @classmethod
    def from_env(cls, model: str) -> PooledAzureProvider:
        if model in _POOL_CACHE:
            return _POOL_CACHE[model]
        raw_path = os.environ.get(POOL_PATH_ENV, "")
        if not raw_path:
            raise ValueError(f"Set {POOL_PATH_ENV} for azure_pool models")
        config = _load_pool_config(raw_path, model)
        if not config:
            raise ValueError(f"No config found for model '{model}' in {POOL_PATH_ENV}={raw_path}")
        instance = cls(config)
        _POOL_CACHE[model] = instance
        return instance

    # -- public API --

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
    ) -> SageChatCompletionMessage:
        kwargs = _build_kwargs(
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            stop=stop,
            tools=tools,
            tool_choice=tool_choice,
            reasoning_effort=reasoning_effort,
        )
        openai_msgs = _to_openai_messages(messages)
        base_kwargs = {"messages": openai_msgs, **kwargs}
        response, call_duration = await with_llm_retry(
            self.PROVIDER_KEY,
            model,
            lambda ep: ep.client.chat.completions.create(model=ep.deployment, **base_kwargs),  # ty:ignore[no-matching-overload]
            gate=self._endpoint_gate,
            max_retries=len(self._endpoints),
        )
        if response.usage:
            record_usage(
                self.PROVIDER_KEY,
                model,
                response.usage.prompt_tokens or 0,
                response.usage.completion_tokens or 0,
                call_duration,
            )
        _fill_trace(trace, {"model": model, **base_kwargs}, response)
        return _to_openai_message(response)

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
        kwargs = _build_kwargs(
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            stop=stop,
            reasoning_effort=reasoning_effort,
        )
        kwargs["response_format"] = _pydantic_to_json_schema(response_format)
        openai_msgs = _to_openai_messages(messages)
        base_kwargs = {"messages": openai_msgs, **kwargs}
        trace = LLMTrace()
        response, call_duration = await with_llm_retry(
            self.PROVIDER_KEY,
            model,
            lambda ep: ep.client.chat.completions.create(model=ep.deployment, **base_kwargs),  # ty:ignore[no-matching-overload]
            gate=self._endpoint_gate,
            max_retries=len(self._endpoints),
        )
        if response.usage:
            record_usage(
                self.PROVIDER_KEY,
                model,
                response.usage.prompt_tokens or 0,
                response.usage.completion_tokens or 0,
                call_duration,
            )
        _fill_trace(trace, {"model": model, **base_kwargs}, response)
        message = _to_openai_message(response)
        assert message.content is not None
        return response_format.model_validate_json(message.content)

    # -- internals --

    def _pick_healthy(self) -> _EndpointState | None:
        """Return next healthy endpoint with available capacity.

        Two-pass: first prefer endpoints with free semaphore slots,
        then fall back to any healthy endpoint (may block on semaphore).
        """
        n = len(self._endpoints)
        start = self._next
        # Pass 1: healthy AND has capacity
        for _ in range(n):
            ep = self._endpoints[self._next % n]
            self._next += 1
            if ep.is_healthy and has_capacity(self.PROVIDER_KEY, ep.deployment):
                return ep
        # Pass 2: any healthy (will block but won't skip all)
        self._next = start
        for _ in range(n):
            ep = self._endpoints[self._next % n]
            self._next += 1
            if ep.is_healthy:
                return ep
        return None

    @asynccontextmanager
    async def _endpoint_gate(self, provider_key: str, model: str):  # noqa: ARG002
        """Custom gate: pick healthy endpoint, acquire per-endpoint AIMD semaphore."""
        ep = self._pick_healthy()
        if ep is None:
            raise RuntimeError(f"azure_pool: all {len(self._endpoints)} endpoints unhealthy")
        try:
            async with llm_gate(provider_key, ep.deployment):
                yield ep
        except Exception as exc:
            cooldown = parse_retry_after(exc) or 5.0
            await ep.mark_unhealthy(cooldown)
            raise


def _fill_trace(trace: LLMTrace, sdk_kwargs: dict[str, Any], response: ChatCompletion) -> None:
    trace.provider_name = "azure_pool"
    trace.provider_request = sdk_kwargs
    trace.provider_response = response.model_dump(mode="json")
    if response.usage:
        trace.prompt_tokens = response.usage.prompt_tokens
        trace.completion_tokens = response.usage.completion_tokens
        trace.total_tokens = response.usage.total_tokens
        if response.usage.completion_tokens_details:
            trace.reasoning_tokens = response.usage.completion_tokens_details.reasoning_tokens
