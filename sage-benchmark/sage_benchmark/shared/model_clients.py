import asyncio
import json
import logging
from typing import TypeVar

from pydantic import BaseModel
from sage_llm import Client as SageLLMClient
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


class AsyncModelClient:
    """Async LLM client using sage-llm for all providers."""

    def __init__(
        self,
        model: str,
        api_key: str | None = None,
        base_url: str | None = None,
        max_concurrent_requests: int = 10,
        reasoning_effort: str | None = None,
    ):
        """
        Initialize async client.

        Args:
            model: Model name (e.g., "gpt-4.1", "trapi/msraif/shared/gpt-4.1", "gemini/gemini-2.5-flash")
            api_key: Optional API key
            base_url: Optional base URL for API
            max_concurrent_requests: Maximum concurrent API requests
            reasoning_effort: Reasoning effort level for supported models (gpt-5.x, gemini)
        """
        self.model = model
        self.reasoning_effort = reasoning_effort
        self.semaphore = asyncio.Semaphore(max_concurrent_requests)
        self._client = SageLLMClient(api_key=api_key, base_url=base_url)

    @retry(
        stop=stop_after_attempt(5),
        wait=wait_exponential(multiplier=1, min=4, max=60),
        retry=retry_if_exception_type((Exception,)),
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
        """
        Call LLM with or without structured output.

        Args:
            prompt: The evaluation prompt (if using simple string prompt)
            response_schema: Pydantic model class for structured output (uses tool_choice=required)
            messages: List of chat messages (alternative to prompt)

        Returns:
            Parsed instance of the response_schema type if provided, otherwise string response
        """
        # Determine input format
        if messages is not None:
            input_messages = [message.model_dump() for message in messages]
        elif prompt is not None:
            input_messages = [{"role": "user", "content": prompt}]
        else:
            raise ValueError("Either prompt or messages must be provided")

        # If response_schema is provided, use tool calling for reliable structured output
        if response_schema is not None:
            tools = [
                {
                    "type": "function",
                    "function": {
                        "name": response_schema.__name__,
                        "description": response_schema.__doc__ or "",
                        "parameters": response_schema.model_json_schema(),
                    },
                }
            ]

            async def _call_with_tool():
                response = await self._client.chat.completions.acreate(
                    model=self.model,
                    messages=input_messages,
                    tools=tools,
                    tool_choice="required",
                    reasoning_effort=self.reasoning_effort,
                )

                # Extract tool call arguments
                message = response.choices[0].message
                if message.tool_calls and len(message.tool_calls) > 0:
                    arguments = message.tool_calls[0].function.arguments
                    if isinstance(arguments, str):
                        return response_schema.model_validate_json(arguments)
                    return response_schema.model_validate(arguments)

                raise ValueError("No tool call in response")

            return await self._call_with_retry(_call_with_tool)

        # No schema - just get text response
        async def _call():
            response = await self._client.chat.completions.acreate(
                model=self.model,
                messages=input_messages,
                reasoning_effort=self.reasoning_effort,
            )

            content = response.choices[0].message.content
            if content is None:
                content = ""
            return content

        return await self._call_with_retry(_call)

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
        # Convert tools to OpenAI format
        openai_tools = [
            {
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.parameters_schema.model_json_schema(),
                },
            }
            for tool in tools
        ]

        json_messages = [message.model_dump() for message in messages]

        async def _call():
            response = await self._client.chat.completions.acreate(
                model=self.model,
                messages=json_messages,
                tools=openai_tools,
                tool_choice="required",
                reasoning_effort=self.reasoning_effort,
            )

            # Get raw response for logging
            raw_response = json.dumps(response.model_dump())

            # Check for tool calls
            message = response.choices[0].message
            if message.tool_calls and len(message.tool_calls) > 0:
                tool_call = message.tool_calls[0]
                arguments = tool_call.function.arguments
                if isinstance(arguments, str):
                    arguments = json.loads(arguments)

                return ToolCallResult(
                    tool_call=ToolCall(
                        tool_name=tool_call.function.name,
                        arguments=arguments,
                    ),
                    raw_response=raw_response,
                )

            # No tool call found
            return ToolCallResult(
                raw_response=raw_response,
                error="No tool call in response",
            )

        return await self._call_with_retry(_call)


def get_async_client(
    model_name: str,
    api_key: str | None = None,
    base_url: str | None = None,
    max_concurrent_requests: int = 10,
    reasoning_effort: str | None = None,
) -> AsyncModelClient:
    """
    Factory function to get an async client for a model.

    Args:
        model_name: Name of the model (e.g., "gpt-4.1", "trapi/...", "gemini/...")
        api_key: Optional API key
        base_url: Optional base URL for API
        max_concurrent_requests: Maximum concurrent requests
        reasoning_effort: Reasoning effort level for supported models (gpt-5.x, gemini)

    Returns:
        AsyncModelClient instance
    """
    return AsyncModelClient(
        model=model_name,
        api_key=api_key,
        base_url=base_url,
        max_concurrent_requests=max_concurrent_requests,
        reasoning_effort=reasoning_effort,
    )
