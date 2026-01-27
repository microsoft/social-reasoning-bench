"""Agent runner for managing multi-turn conversations with tool calling."""

from __future__ import annotations

import json
import os
from abc import ABC, abstractmethod
from typing import Any

from dotenv import load_dotenv

from src.agents.prompt import AGENT_SYSTEM_PROMPT
from src.agents.tools import execute_tool, get_tool_definitions
from src.simulation.state import GameState

# Load environment variables from .env file
load_dotenv()


class AgentRunner(ABC):
    """Base class for agent runners that manage conversation with tool calling."""

    def __init__(self, model: str, state: GameState, api_key: str | None = None, logger=None):
        self.model = model
        self.state = state
        self.api_key = api_key
        self.logger = logger
        self.messages: list[dict[str, Any]] = []
        self.total_input_tokens = 0
        self.total_output_tokens = 0

    @abstractmethod
    def _call_llm(
        self, messages: list[dict[str, Any]], tools: list[dict[str, Any]]
    ) -> tuple[str | None, list[dict[str, Any]] | None, int, int]:
        """Call the LLM with messages and tools.

        Args:
            messages: Conversation messages
            tools: Tool definitions

        Returns:
            Tuple of (text_response, tool_calls, input_tokens, output_tokens)
        """
        pass

    @abstractmethod
    def _format_tool_result(self, tool_call_id: str, result: str) -> dict[str, Any]:
        """Format a tool result for the specific provider.

        Args:
            tool_call_id: ID of the tool call
            result: Tool execution result

        Returns:
            Formatted message dict
        """
        pass

    def generate_text(self, prompt: str) -> str:
        """Generate a simple text response (for supplier responses etc).

        Args:
            prompt: The prompt to respond to

        Returns:
            Generated text response
        """
        messages = [{"role": "user", "content": prompt}]
        text, _, input_tokens, output_tokens = self._call_llm(messages, [])
        self.total_input_tokens += input_tokens
        self.total_output_tokens += output_tokens
        return text or ""

    @abstractmethod
    def generate_structured(self, prompt: str, response_model: type) -> Any:
        """Generate a structured response using a Pydantic model.

        Args:
            prompt: The prompt to respond to
            response_model: Pydantic model class for structured output

        Returns:
            Instance of response_model
        """
        pass

    def run_turn(
        self, user_message: str | None = None, max_iterations: int = 10, verbose: bool = False
    ) -> str:
        """Run one turn of the agent, handling tool calls.

        Args:
            user_message: Optional user message to add
            max_iterations: Maximum LLM calls per turn to prevent infinite loops
            verbose: Enable verbose logging

        Returns:
            Final text response from the agent
        """
        if user_message:
            self.messages.append({"role": "user", "content": user_message})

        tools = get_tool_definitions()
        iterations = 0

        while iterations < max_iterations:
            iterations += 1

            if verbose:
                print(f"\n[Iteration {iterations}/{max_iterations}]")

            # Prepare messages with system prompt
            full_messages = [{"role": "system", "content": AGENT_SYSTEM_PROMPT}] + self.messages

            if verbose:
                print(
                    f"Calling LLM with {len(full_messages)} messages, {len(tools)} tools available"
                )

            # Call LLM
            text_response, tool_calls, input_tokens, output_tokens = self._call_llm(
                full_messages, tools
            )
            self.total_input_tokens += input_tokens
            self.total_output_tokens += output_tokens

            if verbose:
                print(f"LLM response: {input_tokens} input tokens, {output_tokens} output tokens")
                if text_response:
                    preview = (
                        text_response[:100] + "..." if len(text_response) > 100 else text_response
                    )
                    print(f"Text: {preview}")
                if tool_calls:
                    print(f"Tool calls: {len(tool_calls)}")

            # If no tool calls, we're done
            if not tool_calls:
                if text_response:
                    self.messages.append({"role": "assistant", "content": text_response})
                return text_response or ""

            # Process tool calls
            assistant_message = self._format_assistant_tool_calls(text_response, tool_calls)
            self.messages.append(assistant_message)

            for tool_call in tool_calls:
                tool_name = tool_call["name"]
                tool_args = tool_call["arguments"]
                tool_id = tool_call["id"]

                if verbose:
                    args_preview = (
                        str(tool_args)[:80] + "..." if len(str(tool_args)) > 80 else str(tool_args)
                    )
                    print(f"{tool_name}({args_preview})")

                # Execute the tool
                result = execute_tool(self.state, tool_name, tool_args, logger=self.logger)

                if verbose:
                    result_preview = result[:100] + "..." if len(result) > 100 else result
                    print(f"{result_preview}")

                # Add tool result to messages
                tool_result_msg = self._format_tool_result(tool_id, result)
                self.messages.append(tool_result_msg)

        # If we hit max iterations, force a response
        if verbose:
            print(f"\nReached max iterations ({max_iterations})")
        return "Reached maximum tool call iterations for this turn."

    @abstractmethod
    def _format_assistant_tool_calls(
        self, text: str | None, tool_calls: list[dict[str, Any]]
    ) -> dict[str, Any]:
        """Format assistant message with tool calls.

        Args:
            text: Optional text content
            tool_calls: List of tool calls

        Returns:
            Formatted assistant message
        """
        pass

    def get_token_usage(self) -> dict[str, int]:
        """Get total token usage."""
        return {
            "input_tokens": self.total_input_tokens,
            "output_tokens": self.total_output_tokens,
            "total_tokens": self.total_input_tokens + self.total_output_tokens,
        }


class OpenAIRunner(AgentRunner):
    """Agent runner using OpenAI API."""

    def __init__(self, model: str, state: GameState, api_key: str | None = None, logger=None):
        super().__init__(model, state, api_key, logger)
        from openai import OpenAI

        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))

    def _call_llm(
        self, messages: list[dict[str, Any]], tools: list[dict[str, Any]]
    ) -> tuple[str | None, list[dict[str, Any]] | None, int, int]:
        kwargs = {
            "model": self.model,
            "messages": messages,
        }
        if tools:
            kwargs["tools"] = tools

        response = self.client.chat.completions.create(**kwargs)

        message = response.choices[0].message
        text = message.content
        tool_calls = None

        if message.tool_calls:
            tool_calls = []
            for tc in message.tool_calls:
                tool_calls.append(
                    {
                        "id": tc.id,
                        "name": tc.function.name,
                        "arguments": json.loads(tc.function.arguments),
                    }
                )

        input_tokens = response.usage.prompt_tokens if response.usage else 0
        output_tokens = response.usage.completion_tokens if response.usage else 0

        return text, tool_calls, input_tokens, output_tokens

    def _format_tool_result(self, tool_call_id: str, result: str) -> dict[str, Any]:
        return {
            "role": "tool",
            "tool_call_id": tool_call_id,
            "content": result,
        }

    def _format_assistant_tool_calls(
        self, text: str | None, tool_calls: list[dict[str, Any]]
    ) -> dict[str, Any]:
        return {
            "role": "assistant",
            "content": text,
            "tool_calls": [
                {
                    "id": tc["id"],
                    "type": "function",
                    "function": {
                        "name": tc["name"],
                        "arguments": json.dumps(tc["arguments"]),
                    },
                }
                for tc in tool_calls
            ],
        }

    def generate_structured(self, prompt: str, response_model: type) -> Any:
        """Generate a structured response using OpenAI's structured outputs.

        Args:
            prompt: The prompt to respond to
            response_model: Pydantic model class for structured output

        Returns:
            Instance of response_model
        """
        response = self.client.chat.completions.parse(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            response_format=response_model,
        )

        # Track token usage
        if response.usage:
            self.total_input_tokens += response.usage.prompt_tokens
            self.total_output_tokens += response.usage.completion_tokens

        return response.choices[0].message.parsed


class AnthropicRunner(AgentRunner):
    """Agent runner using Anthropic API."""

    def __init__(self, model: str, state: GameState, api_key: str | None = None, logger=None):
        super().__init__(model, state, api_key, logger)
        from anthropic import Anthropic

        self.client = Anthropic(api_key=api_key or os.getenv("ANTHROPIC_API_KEY"))

    def _call_llm(
        self, messages: list[dict[str, Any]], tools: list[dict[str, Any]]
    ) -> tuple[str | None, list[dict[str, Any]] | None, int, int]:
        # Extract system message
        system = None
        conv_messages = []
        for msg in messages:
            if msg["role"] == "system":
                system = msg["content"]
            else:
                conv_messages.append(msg)

        # Convert tools to Anthropic format
        anthropic_tools = []
        for tool in tools:
            anthropic_tools.append(
                {
                    "name": tool["function"]["name"],
                    "description": tool["function"]["description"],
                    "input_schema": tool["function"]["parameters"],
                }
            )

        kwargs = {
            "model": self.model,
            "max_tokens": 4096,
            "messages": conv_messages,
        }
        if system:
            kwargs["system"] = system
        if anthropic_tools:
            kwargs["tools"] = anthropic_tools

        response = self.client.messages.create(**kwargs)

        text = None
        tool_calls = None

        for block in response.content:
            if block.type == "text":
                text = block.text
            elif block.type == "tool_use":
                if tool_calls is None:
                    tool_calls = []
                tool_calls.append(
                    {
                        "id": block.id,
                        "name": block.name,
                        "arguments": block.input,
                    }
                )

        input_tokens = response.usage.input_tokens
        output_tokens = response.usage.output_tokens

        return text, tool_calls, input_tokens, output_tokens

    def _format_tool_result(self, tool_call_id: str, result: str) -> dict[str, Any]:
        return {
            "role": "user",
            "content": [
                {
                    "type": "tool_result",
                    "tool_use_id": tool_call_id,
                    "content": result,
                }
            ],
        }

    def _format_assistant_tool_calls(
        self, text: str | None, tool_calls: list[dict[str, Any]]
    ) -> dict[str, Any]:
        content = []
        if text:
            content.append({"type": "text", "text": text})
        for tc in tool_calls:
            content.append(
                {
                    "type": "tool_use",
                    "id": tc["id"],
                    "name": tc["name"],
                    "input": tc["arguments"],
                }
            )
        return {"role": "assistant", "content": content}

    def generate_structured(self, prompt: str, response_model: type) -> Any:
        """Generate a structured response using Anthropic's prompt caching.

        Args:
            prompt: The prompt to respond to
            response_model: Pydantic model class for structured output

        Returns:
            Instance of response_model
        """
        import json

        # Anthropic doesn't have native structured output, so we use JSON mode
        system_msg = f"""You must respond with valid JSON matching this schema:
{json.dumps(response_model.model_json_schema(), indent=2)}

Respond ONLY with the JSON object, no additional text."""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=4096,
            system=system_msg,
            messages=[{"role": "user", "content": prompt}],
        )

        # Track token usage
        self.total_input_tokens += response.usage.input_tokens
        self.total_output_tokens += response.usage.output_tokens

        # Parse the JSON response
        text_content = ""
        for block in response.content:
            if block.type == "text":
                text_content += block.text

        return response_model.model_validate_json(text_content)


class GeminiRunner(AgentRunner):
    """Agent runner using Google Gemini API."""

    def __init__(self, model: str, state: GameState, api_key: str | None = None, logger=None):
        super().__init__(model, state, api_key, logger)
        from google import genai
        from google.genai import types

        self.genai = genai
        self.types = types
        self.client = genai.Client(api_key=api_key or os.getenv("GEMINI_API_KEY"))

    def _call_llm(
        self, messages: list[dict[str, Any]], tools: list[dict[str, Any]]
    ) -> tuple[str | None, list[dict[str, Any]] | None, int, int]:
        # Extract system instruction
        system_instruction = None
        contents = []

        for msg in messages:
            if msg["role"] == "system":
                system_instruction = msg["content"]
            elif msg["role"] == "user":
                contents.append(
                    self.types.Content(
                        role="user",
                        parts=[self.types.Part.from_text(msg["content"])]
                        if isinstance(msg["content"], str)
                        else self._convert_content_parts(msg["content"]),
                    )
                )
            elif msg["role"] == "assistant":
                parts = []
                if isinstance(msg.get("content"), str) and msg["content"]:
                    parts.append(self.types.Part.from_text(msg["content"]))
                if "tool_calls" in msg:
                    for tc in msg["tool_calls"]:
                        parts.append(
                            self.types.Part.from_function_call(
                                name=tc["function"]["name"],
                                args=json.loads(tc["function"]["arguments"]),
                            )
                        )
                if parts:
                    contents.append(self.types.Content(role="model", parts=parts))
            elif msg["role"] == "tool":
                contents.append(
                    self.types.Content(
                        role="user",
                        parts=[
                            self.types.Part.from_function_response(
                                name="tool_response",
                                response={"result": msg["content"]},
                            )
                        ],
                    )
                )

        # Convert tools to Gemini format
        gemini_tools = None
        if tools:
            function_declarations = []
            for tool in tools:
                func = tool["function"]
                function_declarations.append(
                    self.types.FunctionDeclaration(
                        name=func["name"],
                        description=func["description"],
                        parameters=func["parameters"],
                    )
                )
            gemini_tools = [self.types.Tool(function_declarations=function_declarations)]

        config = {}
        if system_instruction:
            config["system_instruction"] = system_instruction

        response = self.client.models.generate_content(
            model=self.model,
            contents=contents,
            config=self.types.GenerateContentConfig(
                tools=gemini_tools,
                **config,
            ),
        )

        text = None
        tool_calls = None

        if response.candidates and response.candidates[0].content:
            for part in response.candidates[0].content.parts:
                if part.text:
                    text = part.text
                elif part.function_call:
                    if tool_calls is None:
                        tool_calls = []
                    tool_calls.append(
                        {
                            "id": f"call_{len(tool_calls)}",
                            "name": part.function_call.name,
                            "arguments": dict(part.function_call.args),
                        }
                    )

        # Gemini doesn't always provide token counts
        input_tokens = (
            getattr(response.usage_metadata, "prompt_token_count", 0)
            if response.usage_metadata
            else 0
        )
        output_tokens = (
            getattr(response.usage_metadata, "candidates_token_count", 0)
            if response.usage_metadata
            else 0
        )

        return text, tool_calls, input_tokens, output_tokens

    def _convert_content_parts(self, content: list[dict]) -> list:
        """Convert content parts to Gemini format."""
        parts = []
        for item in content:
            if item.get("type") == "text":
                parts.append(self.types.Part.from_text(item["text"]))
            elif item.get("type") == "tool_result":
                parts.append(
                    self.types.Part.from_function_response(
                        name="tool_response",
                        response={"result": item["content"]},
                    )
                )
        return parts

    def _format_tool_result(self, tool_call_id: str, result: str) -> dict[str, Any]:
        return {
            "role": "tool",
            "tool_call_id": tool_call_id,
            "content": result,
        }

    def _format_assistant_tool_calls(
        self, text: str | None, tool_calls: list[dict[str, Any]]
    ) -> dict[str, Any]:
        # Use OpenAI-like format for internal storage
        return {
            "role": "assistant",
            "content": text,
            "tool_calls": [
                {
                    "id": tc["id"],
                    "type": "function",
                    "function": {
                        "name": tc["name"],
                        "arguments": json.dumps(tc["arguments"]),
                    },
                }
                for tc in tool_calls
            ],
        }

    def generate_structured(self, prompt: str, response_model: type) -> Any:
        """Generate a structured response using Gemini's structured output.

        Args:
            prompt: The prompt to respond to
            response_model: Pydantic model class for structured output

        Returns:
            Instance of response_model
        """
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                "response_json_schema": response_model.model_json_schema(),
            },
        )

        # Track token usage
        if response.usage_metadata:
            input_tokens = getattr(response.usage_metadata, "prompt_token_count", 0)
            output_tokens = getattr(response.usage_metadata, "candidates_token_count", 0)
            self.total_input_tokens += input_tokens
            self.total_output_tokens += output_tokens

        return response_model.model_validate_json(response.text)


def get_runner(
    provider: str, model: str, state: GameState, api_key: str | None = None, logger=None
) -> AgentRunner:
    """Factory function to get the appropriate runner.

    Args:
        provider: Provider name ("openai", "anthropic", "gemini")
        model: Model name
        state: Game state
        api_key: Optional API key

    Returns:
        AgentRunner instance

    Raises:
        ValueError: If provider is unknown
    """
    provider = provider.lower()

    if provider == "openai":
        return OpenAIRunner(model, state, api_key, logger)
    elif provider == "anthropic":
        return AnthropicRunner(model, state, api_key, logger)
    elif provider == "gemini":
        return GeminiRunner(model, state, api_key, logger)
    else:
        raise ValueError(
            f"Unknown provider: {provider}. Must be 'openai', 'anthropic', or 'gemini'"
        )
