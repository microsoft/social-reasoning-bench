"""Base generator class for LLM-based content generation."""

from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar, cast

from openai import AsyncOpenAI
from openai.types.chat import ChatCompletionMessageParam
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class BaseLLMGenerator(ABC, Generic[T]):
    """Base class for LLM-based generators.

    Provides common infrastructure for:
    - OpenAI client management
    - Prompt building (subclass responsibility)
    - Response format specification (subclass responsibility)
    - LLM calling with error handling
    - Message history management

    Subclasses must implement:
    - build_prompt(): Construct the prompt for generation
    - get_response_format(): Specify the Pydantic model for structured output
    """

    def __init__(self, client: AsyncOpenAI, model: str = "gpt-4-turbo-preview"):
        """
        Initialize the generator.

        Args:
            client: OpenAI async client
            model: Model to use for generation
        """
        self.client = client
        self.model = model

    @abstractmethod
    def build_prompt(self, context: Any, **kwargs: Any) -> str:
        """Build the prompt for this generator.

        Args:
            context: Generation context (type varies by generator)
            **kwargs: Additional keyword arguments for prompt customization

        Returns:
            Complete prompt string
        """
        pass

    @abstractmethod
    def get_response_format(self) -> type[T]:
        """Get the Pydantic model for structured output.

        Returns:
            Pydantic model class
        """
        pass

    async def generate(
        self,
        context: Any,
        messages: list[dict[str, Any]],
        **kwargs: Any,
    ) -> T:
        """Generic generation logic.

        Args:
            context: Generation context
            messages: Shared LLM conversation history (will be appended to)
            **kwargs: Additional keyword arguments passed to build_prompt

        Returns:
            Generated result of type T

        Raises:
            ValueError: If LLM fails to parse response
        """
        # Build and append prompt
        prompt = self.build_prompt(context, **kwargs)
        messages.append({"role": "user", "content": prompt})

        # Call LLM with structured output
        response = await self.client.beta.chat.completions.parse(
            model=self.model,
            messages=cast(list[ChatCompletionMessageParam], messages),
            response_format=self.get_response_format(),
        )

        # Extract and validate result
        result = response.choices[0].message.parsed
        if result is None:
            raise ValueError(f"Failed to parse {self.__class__.__name__} response from LLM")

        # Append response to history
        messages.append(response.choices[0].message.model_dump(mode="json"))

        return result
