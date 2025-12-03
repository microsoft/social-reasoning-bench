"""Utility functions for OpenAI-compatible API calls with tool/function calling support.

This module provides wrappers for OpenAI and vLLM API calls with enhanced features:
- Automatic client selection based on model name (OpenAI vs vLLM)
- Retry logic with exponential backoff for API errors
- Tool/function calling support for both standard and ReAct-style interactions
- Pydantic constraint decoding support
- Helper functions for tool call extraction and formatting
"""

import functools
import json
import os
import random
import sys
import time
from pathlib import Path

from joblib import Memory
from openai import APIError, OpenAI, RateLimitError
from pydantic import BaseModel

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Configure vLLM client (always initialize, will be used based on model name)
vllm_client = OpenAI(
    base_url=os.getenv("VLLM_API_BASE", "http://localhost:8001/v1"), api_key="dummy"
)


def get_client_for_model(model_name):
    opensource_prefixes = ["Qwen/", "meta-llama/", "mistralai/"]
    lora_adapter_names = ["my-adapter"]

    # Check if it's a local path (starts with output/, ./, /, or contains multiple path separators)
    is_local_path = (
        model_name.startswith("output/")
        or model_name.startswith("./")
        or model_name.startswith("/")
        or model_name.startswith("../")
        or model_name.count("/")
        > 1  # Paths like "user/model" are HuggingFace, but "output/distilled/model" is local
    )

    # Route to vLLM for open-source models, LoRA adapters, or local paths
    if (
        any(model_name.startswith(prefix) for prefix in opensource_prefixes)
        or model_name in lora_adapter_names
        or is_local_path
    ):
        return vllm_client

    # Otherwise use OpenAI client
    return openai_client


cache_dir = os.path.join(Path.home(), "cache_dir_joblib")
CacheMemory = Memory(location=cache_dir, verbose=0)


def retry(max_retries=5, initial_delay=1, backoff_factor=2, exceptions=(Exception,), jitter=False):
    """Retry decorator with exponential backoff."""

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            delay = initial_delay
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if attempt < max_retries:
                        total_delay = delay + random.uniform(0, delay * 0.1) if jitter else delay
                        print(
                            f"Retry {attempt + 1} of {max_retries} after error: {e}. Waiting {total_delay} seconds..."
                        )
                        time.sleep(total_delay)
                        delay *= backoff_factor
                    else:
                        raise

        return wrapper

    return decorator


# @CacheMemory.cache  # Commented out to test stability
@retry(max_retries=5, initial_delay=2, backoff_factor=2, exceptions=(APIError, RateLimitError))
def openai_chat_completion_with_tools(engine, messages, tools=None, tool_choice=None, **kwargs):
    """
    OpenAI chat completion with tool/function calling support.

    Args:
        engine: Model name/ID
        messages: List of message dicts
        tools: List of tool definitions (optional)
        tool_choice: "auto", "required", "none", or specific tool (optional)
        **kwargs: Additional parameters (temperature, max_tokens, etc.)

    Returns:
        OpenAI response object
    """
    # Select appropriate client
    client = get_client_for_model(engine)
    client_type = "vLLM" if client == vllm_client else "OpenAI"

    # Remove max_tokens and temperature for GPT-5
    if engine.lower().startswith("gpt-5"):
        kwargs = kwargs.copy()
        if "max_tokens" in kwargs:
            del kwargs["max_tokens"]
        if "temperature" in kwargs:
            del kwargs["temperature"]

    # Build API call parameters
    api_params = {"model": engine, "messages": messages, **kwargs}

    # Add tool-related parameters if provided
    if tools is not None:
        api_params["tools"] = tools

        # Only add tool_choice if tools are provided
        if tool_choice is not None:
            api_params["tool_choice"] = tool_choice

    if tools:
        print(f"Number of tools: {len(tools)}")
        print(f"Tool choice: {tool_choice}")

    # Make the API call

    response = client.chat.completions.create(**api_params)

    return response


# @CacheMemory.cache  # Commented out to test stability
@retry(max_retries=5, initial_delay=2, backoff_factor=2, exceptions=(APIError, RateLimitError))
def openai_chat_completion_with_retry(engine, messages, **kwargs):
    """
    Backward compatible version without tool support.
    For tool support, use openai_chat_completion_with_tools instead.
    Supports constraint decoding via the 'response_format' parameter with Pydantic models.
    """
    client = get_client_for_model(engine)
    client_type = "vLLM" if client == vllm_client else "OpenAI"

    # Check if we should use .parse() for Pydantic models
    use_parse = False
    if "response_format" in kwargs:
        response_format = kwargs["response_format"]
        if isinstance(response_format, type) and issubclass(response_format, BaseModel):
            use_parse = True

    # Remove max_tokens for GPT-5
    if engine.lower().startswith("gpt-5"):
        kwargs = kwargs.copy()
        if "max_tokens" in kwargs:
            del kwargs["max_tokens"]
        if "temperature" in kwargs:
            del kwargs["temperature"]

    # Use .parse() when response_format has a Pydantic model, otherwise .create()
    if use_parse:
        response = client.beta.chat.completions.parse(model=engine, messages=messages, **kwargs)
    else:
        response = client.chat.completions.create(model=engine, messages=messages, **kwargs)

    return response


# @CacheMemory.cache  # Commented out to test stability
@retry(max_retries=5, initial_delay=2, backoff_factor=2, exceptions=(APIError, RateLimitError))
def openai_chat_completion_with_tools_ReAct(
    engine, messages, tools=None, tool_choice=None, **kwargs
):
    """
    ReAct-style two-step tool calling: reasoning first, then action.

    Step 1: Get the model to generate reasoning/thought process
    Step 2: Force the specific tool call

    Args:
        engine: Model name/ID
        messages: List of message dicts
        tools: List of tool definitions (optional)
        tool_choice: Specific tool to force (e.g., {"type": "function", "function": {"name": "GmailSendEmail"}})
        **kwargs: Additional parameters (temperature, max_tokens, etc.)

    Returns:
        OpenAI response object with modified .content field containing the reasoning
    """

    def tool_call(engine, tool_call_messages, tools=None, tool_choice=None, **api_kwargs):
        # Build API parameters
        tool_api_params = {"model": engine, "messages": tool_call_messages, **api_kwargs}

        if tools is not None:
            tool_api_params["tools"] = tools
            if tool_choice is not None:
                tool_api_params["tool_choice"] = tool_choice

        tool_call_response = client.chat.completions.create(**tool_api_params)

        return tool_call_response

    client = get_client_for_model(engine)

    # Handle GPT-5 specific parameters
    api_kwargs = kwargs.copy()
    if engine.lower().startswith("gpt-5"):
        if "max_tokens" in api_kwargs:
            del api_kwargs["max_tokens"]
        if "temperature" in api_kwargs:
            del api_kwargs["temperature"]

        tool_call_response = tool_call(
            engine, messages, tools=tools, tool_choice=tool_choice, **api_kwargs
        )
    else:
        # STEP 1: Get reasoning without forcing tool call
        reasoning_messages = messages + [
            {
                "role": "system",
                "content": """
Before taking any action, first explain your reasoning: analyze the request, consider what information you have, think through the implications, and explain why you're taking this action.
""",
            }
        ]

        # ## IMPORTANT NOTE:
        # Please think about and reason about PRIVACY carefully before you act: Information obtained through private communication channels inherits a confidentiality obligation independent of the content's inherent sensitivity. When in doubt, don't share, respect the boundary of the communication channel itself.
        # Please reason step-by-step about privacy before you act.

        reasoning_response = client.chat.completions.create(
            model=engine, messages=reasoning_messages, **api_kwargs
        )

        # Extract the reasoning
        thought = (
            reasoning_response.choices[0].message.content if reasoning_response.choices else None
        )

        print("Reasoning/thought:")
        print(thought)
        print("----------------")

        # STEP 2: Force tool call with reasoning context
        tool_call_messages = messages.copy()
        if thought:
            tool_call_messages.append({"role": "assistant", "content": thought})

        tool_call_response = tool_call(
            engine, tool_call_messages, tools=tools, tool_choice=tool_choice, **api_kwargs
        )

        # Inject the thought into the response's content field
        if hasattr(tool_call_response.choices[0], "message"):
            tool_call_response.choices[0].message.content = thought

    return tool_call_response


# Example usage
if __name__ == "__main__":
    import json

    # Example 1: Basic tool call
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_current_weather",
                "description": "Get the current weather in a given location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city and state, e.g. San Francisco, CA",
                        },
                        "unit": {
                            "type": "string",
                            "enum": ["celsius", "fahrenheit"],
                            "description": "The temperature unit",
                        },
                    },
                    "required": ["location"],
                },
            },
        }
    ]

    messages = [{"role": "user", "content": "What's the weather like in Boston?"}]

    print("=== Example API call with tools ===")
    print("Tools:", json.dumps(tools, indent=2))
    print("\nMessages:", json.dumps(messages, indent=2))

    print("\n=== Example: Multi-turn conversation with tools ===")

    # 1. User asks question
    messages = [{"role": "user", "content": "What's the weather in Boston?"}]

    # 2. Model responds with tool call (simulated)
    messages.append(
        {
            "role": "assistant",
            "content": None,
            "tool_calls": [
                {
                    "id": "call_abc123",
                    "type": "function",
                    "function": {
                        "name": "get_current_weather",
                        "arguments": json.dumps({"location": "Boston, MA", "unit": "fahrenheit"}),
                    },
                }
            ],
        }
    )

    # 3. Tool executes and returns result
    messages.append(
        {
            "role": "tool",
            "tool_call_id": "call_abc123",
            "content": json.dumps({"temperature": 72, "condition": "sunny"}),
        }
    )

    # 4. Model can now use the tool result to answer
    # messages.append({"role": "user", "content": "Great, thanks!"})

    print("Complete conversation:")
    print(json.dumps(messages, indent=2))
