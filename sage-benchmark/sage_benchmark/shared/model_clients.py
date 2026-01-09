import asyncio
import json
import logging
import os
from abc import ABC, abstractmethod
from typing import TypeVar

from google import genai
from openai import APITimeoutError, AsyncOpenAI, RateLimitError
from pydantic import BaseModel
from tenacity import (
    before_sleep_log,
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from .schemas import ChatMessage, ToolCall, ToolCallResult, ToolDefinition

T = TypeVar("T", bound=BaseModel)

logger = logging.getLogger(__name__)


def _clean_schema_for_gemini(schema: dict) -> dict:
    """Remove 'title' fields from JSON schema for Gemini compatibility.

    Pydantic auto-generates 'title' fields from field/class names, but Gemini
    doesn't support them and returns MALFORMED_FUNCTION_CALL errors.
    """
    if isinstance(schema, dict):
        return {k: _clean_schema_for_gemini(v) for k, v in schema.items() if k != "title"}
    if isinstance(schema, list):
        return [_clean_schema_for_gemini(item) for item in schema]
    return schema


class AsyncModelClient(ABC):
    """Abstract base class for async LLM clients."""

    def __init__(self, max_concurrent_requests: int = 10):
        """
        Initialize async client with rate limiting.

        Args:
            max_concurrent_requests: Maximum number of concurrent API requests
        """
        self.semaphore = asyncio.Semaphore(max_concurrent_requests)

    @abstractmethod
    async def call_llm(
        self,
        prompt: str | None = None,
        response_schema: type[T] | None = None,
        messages: list[ChatMessage] | None = None,
    ) -> T | str:
        """
        Call LLM with or without structured output.

        Args:
            prompt: The evaluation prompt (if using simple string prompt)
            response_schema: Pydantic model class for structured output (optional)
            messages: List of chat messages (alternative to prompt)

        Returns:
            Parsed instance of the response_schema type if provided, otherwise string response
        """
        pass

    @abstractmethod
    async def call_llm_with_tools(
        self,
        messages: list[ChatMessage],
        tools: list[ToolDefinition],
    ) -> ToolCallResult:
        """
        Call LLM with tool definitions and return the tool call.

        Args:
            messages: List of chat messages
            tools: List of available tools

        Returns:
            ToolCallResult containing the tool call or error
        """
        pass


class AsyncOpenAIClient(AsyncModelClient):
    """Async OpenAI client with retry and rate limiting."""

    def __init__(
        self,
        model: str,
        api_key: str | None = None,
        base_url: str | None = None,
        max_concurrent_requests: int = 10,
        max_retries: int = 5,
    ):
        """
        Initialize async OpenAI client.

        Args:
            model: Model name to use
            api_key: API key (defaults to OPENAI_API_KEY env var)
            base_url: Base URL for API (useful for vLLM-hosted models)
            max_concurrent_requests: Maximum concurrent API requests
            max_retries: Maximum number of retries for failed requests
        """
        super().__init__(max_concurrent_requests)
        self.client = AsyncOpenAI(
            api_key=api_key or os.getenv("OPENAI_API_KEY"),
            base_url=base_url,
        )
        self.model = model
        self.max_retries = max_retries

    @retry(
        stop=stop_after_attempt(5),
        wait=wait_exponential(multiplier=1, min=4, max=60),
        retry=retry_if_exception_type((RateLimitError, APITimeoutError)),
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    async def _call_with_retry(self, call_fn):
        """Wrapper to add retry logic with exponential backoff."""
        async with self.semaphore:
            return await call_fn()

    async def call_llm(
        self,
        prompt: str | None = None,
        response_schema: type[T] | None = None,
        messages: list[ChatMessage] | None = None,
    ) -> T | str:
        # Determine input format
        if messages is not None:
            input_data = [message.model_dump() for message in messages]
        elif prompt is not None:
            input_data = prompt
        else:
            raise ValueError("Either prompt or messages must be provided")

        # Call with or without structured output
        async def _call():
            if response_schema is not None:
                response = await self.client.responses.parse(
                    model=self.model,
                    input=input_data,
                    text_format=response_schema,
                )
                return response.output_parsed
            else:
                response = await self.client.responses.create(
                    model=self.model,
                    input=input_data,
                )
                # Extract text from response output
                text_parts = []
                for item in response.output:
                    if item.type == "text":
                        text_parts.append(item.text)
                return "".join(text_parts)

        return await self._call_with_retry(_call)

    async def call_llm_with_tools(
        self,
        messages: list[ChatMessage],
        tools: list[ToolDefinition],
    ) -> ToolCallResult:
        openai_tools = [
            {
                "type": "function",
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.parameters_schema.model_json_schema(),
            }
            for tool in tools
        ]

        json_messages = [message.model_dump() for message in messages]

        async def _call():
            response = await self.client.responses.create(
                model=self.model,
                input=json_messages,
                tools=openai_tools,
                tool_choice="required",
            )

            # get string for logging
            raw_response = response.model_dump_json()

            # Find first function_call in output array
            for item in response.output:
                if item.type == "function_call":
                    arguments = item.arguments
                    if isinstance(arguments, str):
                        arguments = json.loads(arguments)

                    return ToolCallResult(
                        tool_call=ToolCall(
                            tool_name=item.name,
                            arguments=arguments,
                        ),
                        raw_response=raw_response,
                    )

            # No function call found
            return ToolCallResult(
                raw_response=raw_response,
                error="No tool call in response",
            )

        return await self._call_with_retry(_call)


class AsyncGeminiClient(AsyncModelClient):
    """Async Gemini client with retry and rate limiting."""

    def __init__(
        self,
        model: str,
        api_key: str | None = None,
        max_concurrent_requests: int = 10,
        max_retries: int = 5,
    ):
        """
        Initialize async Gemini client.

        Args:
            model: Model name to use
            api_key: API key (defaults to GEMINI_API_KEY env var)
            max_concurrent_requests: Maximum concurrent API requests
            max_retries: Maximum number of retries for failed requests
        """
        super().__init__(max_concurrent_requests)
        self.client = genai.Client(api_key=api_key or os.getenv("GEMINI_API_KEY"))
        self.model_name = model
        self.max_retries = max_retries

    @retry(
        stop=stop_after_attempt(5),
        wait=wait_exponential(multiplier=1, min=4, max=60),
        retry=retry_if_exception_type((Exception,)),  # Catch Gemini-specific errors
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    async def _call_with_retry(self, call_fn):
        """Wrapper to add retry logic with exponential backoff."""
        async with self.semaphore:
            return await call_fn()

    def _convert_to_gemini_format(
        self, messages: list[ChatMessage]
    ) -> tuple[str | None, list[genai.types.Content]]:
        """Convert ChatMessage list to Gemini's format."""
        system_instruction = None
        contents = []

        for message in messages:
            if message.role == "system":
                system_instruction = message.content
                continue

            role = "model" if message.role == "assistant" else "user"
            contents.append(
                genai.types.Content(
                    role=role,
                    parts=[genai.types.Part.from_text(text=message.content)],
                )
            )

        return system_instruction, contents

    async def call_llm(
        self,
        prompt: str | None = None,
        response_schema: type[T] | None = None,
        messages: list[ChatMessage] | None = None,
    ) -> T | str:
        # Determine input format
        if messages is not None:
            system_instruction, contents = self._convert_to_gemini_format(messages)
        elif prompt is not None:
            system_instruction = None
            contents = prompt
        else:
            raise ValueError("Either prompt or messages must be provided")

        # Build config
        config = {}
        if response_schema is not None:
            config["response_mime_type"] = "application/json"
            config["response_json_schema"] = response_schema.model_json_schema()

        # Call Gemini
        async def _call():
            # Note: Gemini's Python client doesn't have async methods yet
            # We'll use asyncio.to_thread to run sync code in a thread pool
            if messages is not None:
                response = await asyncio.to_thread(
                    self.client.models.generate_content,
                    model=self.model_name,
                    contents=contents,
                    config=genai.types.GenerateContentConfig(
                        system_instruction=system_instruction,
                        **config,
                    ),
                )
            else:
                response = await asyncio.to_thread(
                    self.client.models.generate_content,
                    model=self.model_name,
                    contents=contents,
                    config=config,
                )

            # Parse response
            if response_schema is not None:
                return response_schema.model_validate_json(response.text)
            else:
                return response.text

        return await self._call_with_retry(_call)

    async def call_llm_with_tools(
        self,
        messages: list[ChatMessage],
        tools: list[ToolDefinition],
    ) -> ToolCallResult:
        function_declarations = [
            genai.types.FunctionDeclaration(
                name=tool.name,
                description=tool.description,
                parameters_json_schema=_clean_schema_for_gemini(
                    tool.parameters_schema.model_json_schema()
                ),
            )
            for tool in tools
        ]

        system_instruction, contents = self._convert_to_gemini_format(messages)

        async def _call():
            # Use asyncio.to_thread for sync Gemini API
            response = await asyncio.to_thread(
                self.client.models.generate_content,
                model=self.model_name,
                contents=contents,
                config=genai.types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    tools=[genai.types.Tool(function_declarations=function_declarations)],
                    tool_config=genai.types.ToolConfig(
                        function_calling_config=genai.types.FunctionCallingConfig(mode="ANY")
                    ),
                ),
            )

            # get string for logging
            raw_response = response.model_dump_json()

            # Check if response has candidates and content
            if not response.candidates:
                return ToolCallResult(raw_response=raw_response, error="No candidates in response")

            candidate = response.candidates[0]
            if not candidate.content:
                finish_reason = getattr(candidate, "finish_reason", None)
                safety_ratings = getattr(candidate, "safety_ratings", None)
                error_msg = f"No content in response. Finish reason: {finish_reason}"
                if safety_ratings:
                    error_msg += f", Safety ratings: {safety_ratings}"
                return ToolCallResult(raw_response=raw_response, error=error_msg)

            if candidate.content.parts:
                for part in candidate.content.parts:
                    if hasattr(part, "function_call"):
                        fc = part.function_call
                        return ToolCallResult(
                            tool_call=ToolCall(
                                tool_name=fc.name,
                                arguments=dict(fc.args),
                            ),
                            raw_response=raw_response,
                        )
            return ToolCallResult(raw_response=raw_response, error="No function call in response")

        return await self._call_with_retry(_call)


def get_async_client(
    model_name: str,
    api_key: str | None = None,
    base_url: str | None = None,
    max_concurrent_requests: int = 10,
) -> AsyncModelClient:
    """
    Factory function to get the appropriate async client for a model.

    Args:
        model_name: Name of the model
        api_key: Optional API key
        base_url: Optional base URL for API (OpenAI-compatible only)
        max_concurrent_requests: Maximum concurrent requests

    Returns:
        Appropriate AsyncModelClient instance
    """
    if "gpt" in model_name.lower() or "openai" in model_name.lower() or base_url is not None:
        return AsyncOpenAIClient(model_name, api_key, base_url, max_concurrent_requests)
    elif "gemini" in model_name.lower():
        return AsyncGeminiClient(model_name, api_key, max_concurrent_requests)
    else:
        raise ValueError(f"Unknown model: {model_name}")
