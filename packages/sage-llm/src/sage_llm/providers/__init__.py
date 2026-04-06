"""Provider routing."""

from .base import SageModelProvider


def resolve_provider(
    model: str,
    *,
    api_key: str | None = None,
    base_url: str | None = None,
    api_version: str | None = None,
) -> tuple[SageModelProvider, str]:
    """Route a model string to the correct provider instance.

    Returns (provider, resolved_model_name).
    """
    # TRAPI: trapi/[apiPath/]model → Azure with AD auth
    if model.startswith("trapi/"):
        from .trapi import TrapiProvider

        api_path, deployment = TrapiProvider.resolve_model(model)
        return TrapiProvider(api_path=api_path), deployment

    # Phyagi: phyagi/model → OpenAI-compatible gateway
    if model.startswith("phyagi/"):
        from .phyagi import PhyagiProvider

        return PhyagiProvider(), model.removeprefix("phyagi/")

    # Anthropic: anthropic/model
    if model.startswith("anthropic/"):
        from .anthropic import AnthropicProvider

        return AnthropicProvider(api_key=api_key), model.removeprefix("anthropic/")

    # Google: gemini/model
    if model.startswith("gemini/"):
        from .google_genai import GoogleProvider

        return GoogleProvider(api_key=api_key), model.removeprefix("gemini/")

    # Azure pool: azure_pool/model → load-balanced across endpoints
    if model.startswith("azure_pool/"):
        from .azure_pool import PooledAzureProvider

        model_name = model.removeprefix("azure_pool/")
        return PooledAzureProvider.from_env(model=model_name), model_name

    # Azure: azure/deployment
    if model.startswith("azure/"):
        from .azure_openai import AzureProvider

        return AzureProvider(
            azure_endpoint=base_url, api_key=api_key, api_version=api_version
        ), model.removeprefix("azure/")

    # OpenAI: openai/model or bare model name
    from .openai import OpenAIProvider

    return OpenAIProvider(api_key=api_key, base_url=base_url), model.removeprefix("openai/")


__all__ = ["SageModelProvider", "resolve_provider"]
