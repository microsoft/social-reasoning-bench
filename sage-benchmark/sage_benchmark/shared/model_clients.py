import json
import os
from abc import ABC, abstractmethod
from typing import TypeVar

from google import genai
from openai import OpenAI
from pydantic import BaseModel

from .schemas import ChatMessage, ToolCall, ToolCallResult, ToolDefinition

T = TypeVar("T", bound=BaseModel)


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


class ModelClient(ABC):
    """Abstract base class for LLM clients used in evaluation."""

    @abstractmethod
    def call_llm(self, prompt: str, response_schema: type[T]) -> T:
        """
        Evaluate using structured output.

        Args:
            prompt: The evaluation prompt
            response_schema: Pydantic model class for structured output

        Returns:
            Parsed instance of the response_schema type
        """
        pass

    @abstractmethod
    def call_llm_with_tools(
        self,
        messages: list[ChatMessage],
        tools: list[ToolDefinition],
    ) -> ToolCallResult:
        """
        Call LLM with tool definitions and return the tool call.

        Args:
            system_message: System prompt
            user_message: User message content
            tools: List of available tools

        Returns:
            ToolCallResult containing the tool call or error
        """
        pass


class OpenAIClient(ModelClient):
    """OpenAI client using the modern Responses API."""

    def __init__(self, model: str, api_key: str | None = None, base_url: str | None = None):
        """
        Initialize OpenAI client.

        Args:
            model: Model name to use
            api_key: API key (defaults to OPENAI_API_KEY env var)
            base_url: Base URL for API (useful for vLLM-hosted models)
        """
        self.client = OpenAI(
            api_key=api_key or os.getenv("OPENAI_API_KEY"),
            base_url=base_url,
        )
        self.model = model

    def call_llm(self, prompt: str, response_schema: type[T]) -> T:
        response = self.client.responses.parse(
            model=self.model,
            input=prompt,
            text_format=response_schema,
        )
        return response.output_parsed

    def call_llm_with_tools(
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

        response = self.client.responses.create(
            model=self.model,
            input=json_messages,
            tools=openai_tools,
            tool_choice="required",
        )

        # get string for logging
        raw_response = response.model_dump_json()

        # Find first function_call in output array
        # TODO: in future should warn if multiple function calls exist
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

    def call_llm(self, prompt: str, response_schema: type[T]) -> T:
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                "response_json_schema": response_schema.model_json_schema(),
            },
        )

        return response_schema.model_validate_json(response.text)

    def call_llm_with_tools(
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

        response = self.client.models.generate_content(
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
            # Check for finish_reason or safety ratings
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


def get_client(
    model_name: str, api_key: str | None = None, base_url: str | None = None
) -> ModelClient:
    """
    Factory function to get the appropriate client for a model.

    Args:
        model_name: Name of the model
        api_key: Optional API key
        base_url: Optional base URL for API (OpenAI-compatible only)

    Returns:
        Appropriate ModelClient instance
    """
    # use openai client for gpt models or if we specify base_url for vllm models
    if "gpt" in model_name.lower() or "openai" in model_name.lower() or base_url is not None:
        return OpenAIClient(model_name, api_key, base_url)
    elif "gemini" in model_name.lower():
        return GeminiClient(model_name, api_key)
    else:
        raise ValueError(f"Unknown model: {model_name}")
