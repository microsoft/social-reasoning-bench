import os
from abc import ABC, abstractmethod

from google import genai
from openai import OpenAI
from pydantic import BaseModel

from .types import SotopiaEvaluation


class ModelClient(ABC):
    """Abstract base class for LLM clients used in Sotopia evaluation."""

    @abstractmethod
    def evaluate(self, prompt: str, response_schema: type[BaseModel]) -> SotopiaEvaluation:
        """
        Evaluate using structured output.

        Args:
            prompt: The evaluation prompt
            response_schema: Pydantic model class for structured output

        Returns:
            Parsed SotopiaEvaluation instance
        """
        pass


class OpenAIClient(ModelClient):
    """OpenAI client using the modern Responses API."""

    def __init__(self, model: str, api_key: str | None = None):
        """
        Initialize OpenAI client.

        Args:
            model: Model name to use
            api_key: API key (defaults to OPENAI_API_KEY env var)
        """
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        self.model = model

    def evaluate(self, prompt: str, response_schema: type[BaseModel]) -> SotopiaEvaluation:
        response = self.client.chat.completions.parse(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            response_format=response_schema,
        )
        return response.choices[0].message.parsed


class GeminiClient(ModelClient):
    """Gemini client using structured output."""

    def __init__(self, model: str, api_key: str | None = None):
        """
        Initialize Gemini client.

        Args:
            model: Model name to use
            api_key: API key (defaults to GEMINI_API_KEY env var)
        """
        self.client = genai.Client(api_key=api_key or os.getenv("GEMINI_API_KEY"))
        self.model_name = model

    def evaluate(self, prompt: str, response_schema: type[BaseModel]) -> SotopiaEvaluation:
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                "response_json_schema": response_schema.model_json_schema(),
            },
        )

        return response_schema.model_validate_json(response.text)


def get_client(model_name: str, api_key: str | None = None) -> ModelClient:
    """
    Factory function to get the appropriate client for a model.

    Args:
        model_name: Name of the model
        api_key: Optional API key

    Returns:
        Appropriate ModelClient instance
    """
    if "gpt" in model_name.lower() or "openai" in model_name.lower():
        return OpenAIClient(model_name, api_key)
    elif "gemini" in model_name.lower():
        return GeminiClient(model_name, api_key)
    else:
        raise ValueError(f"Unknown model: {model_name}")
