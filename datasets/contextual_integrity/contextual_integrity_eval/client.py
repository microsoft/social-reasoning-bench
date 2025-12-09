"""Model client interface for Contextual Integrity evaluation."""

import os
from abc import ABC, abstractmethod

from openai import OpenAI


class ModelClient(ABC):
    """Abstract base class for LLM clients used in Contextual Integrity evaluation."""

    @abstractmethod
    def llm_completion(self, prompt: str) -> str:
        """
        Get LLM completion for the given prompt.

        Args:
            prompt: The prompt to send to the model

        Returns:
            The model's text response
        """
        pass


class OpenAIClient(ModelClient):
    """OpenAI client for text completion."""

    def __init__(self, model: str, api_key: str | None = None):
        """
        Initialize OpenAI client.

        Args:
            model: Model name to use (e.g., "gpt-4", "gpt-3.5-turbo")
            api_key: API key (defaults to OPENAI_API_KEY env var)
        """
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        self.model = model

    def llm_completion(self, prompt: str) -> str:
        """
        Get completion from OpenAI using the Responses API.

        Args:
            prompt: The prompt to send

        Returns:
            The model's text response
        """
        response = self.client.responses.create(
            model=self.model,
            input=[{"role": "user", "content": prompt}],
        )
        return response.output_text
