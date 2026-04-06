"""Phyagi provider — OpenAI-compatible gateway."""

import os

from .openai import OpenAIProvider

BASE_URL = "https://gateway.phyagi.net/api"
API_KEY_ENV = "PHYAGI_API_KEY"


class PhyagiProvider(OpenAIProvider):
    """Provider for Phyagi OpenAI-compatible gateway."""

    PROVIDER_KEY = "phyagi"

    def __init__(self):
        api_key = os.environ.get(API_KEY_ENV)
        if not api_key:
            raise ValueError(f"Set {API_KEY_ENV} environment variable for phyagi models")
        super().__init__(base_url=BASE_URL, api_key=api_key)
