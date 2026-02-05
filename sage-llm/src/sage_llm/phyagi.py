"""Phyagi configuration for OpenAI-compatible gateway."""

import os
from typing import Any

BASE_URL = "https://gateway.phyagi.net/api"
API_KEY_ENV = "PHYAGI_API_KEY"


def get_api_key() -> str:
    """Get API key from environment variable."""
    api_key = os.environ.get(API_KEY_ENV)
    if not api_key:
        raise ValueError(f"Set {API_KEY_ENV} environment variable for phyagi models")
    return api_key


def handle_model(model: str, kwargs: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    """Handle phyagi models by configuring base_url and api_key.

    Phyagi models use the format: phyagi/{model}
    Example: phyagi/gpt-4o -> routes to https://gateway.phyagi.net/api

    Returns (resolved_model, updated_kwargs).
    """
    if not model.startswith("phyagi/"):
        return model, kwargs

    # Strip prefix: phyagi/gpt-4o -> gpt-4o
    resolved_model = model[len("phyagi/") :]

    # Set OpenAI-compatible endpoint
    kwargs["base_url"] = BASE_URL
    kwargs["api_key"] = get_api_key()

    # Prepend openai/ so litellm routes to the OpenAI provider
    return f"openai/{resolved_model}", kwargs
