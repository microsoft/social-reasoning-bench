import os

from dotenv import load_dotenv
from google import genai

load_dotenv()


def _get_config(key: str, default: str = "", config_override: dict = None) -> str:
    if config_override and key in config_override:
        return str(config_override[key])
    return os.getenv(key, default)

def call_llm(
    conversation: list[dict],
    config_override: dict = None,
    provider: str = None,
    model: str = None
) -> str:
    """
    Call an LLM with the given conversation.

    Args:
        conversation: List of conversation turns with "prompt" and "response" keys
        config_override: Dict to override environment variables
        provider: LLM provider ("openai", "gemini", "vllm", "trapi", "human", "human_cli"). Overrides env/config.
        model: Model name. Overrides env/config.
    """
    # Build effective config by merging parameters
    effective_config = config_override.copy() if config_override else {}

    if provider:
        effective_config["LLM_PROVIDER"] = provider
    if model:
        # Set model for all providers (we'll pick the right one later)
        effective_config["OPENAI_MODEL"] = model
        effective_config["GEMINI_MODEL"] = model
        effective_config["VLLM_MODEL"] = model
        effective_config["TRAPI_MODEL"] = model

    provider_name = _get_config("LLM_PROVIDER", "gemini", effective_config).lower()

    if provider_name == "vllm":
        return _call_vllm(conversation, effective_config)
    elif provider_name == "gemini":
        return _call_gemini(conversation, effective_config)
    elif provider_name == "openai":
        return _call_openai(conversation, effective_config)
    elif provider_name == "trapi":
        return _call_trapi(conversation, effective_config)
    elif provider_name == "human":
        return _call_human(conversation, effective_config)
    elif provider_name == "human_cli":
        return _call_human_cli(conversation, effective_config)
    else:
        raise ValueError(f"Unsupported LLM provider: {provider_name}")

def _call_gemini(conversation: list[dict], config_override: dict = None) -> str:
    client = genai.Client(api_key=_get_config("GEMINI_API_KEY", "", config_override))
    model = _get_config("GEMINI_MODEL", "gemini-2.5-flash", config_override)

    contents = []
    for turn in conversation:
        if "prompt" in turn:
            contents.append({"role": "user", "parts": [{"text": turn["prompt"]}]})
        if "response" in turn:
            contents.append({"role": "model", "parts": [{"text": turn["response"]}]})

    config = {}
    temp = _get_config("GEMINI_TEMPERATURE", "", config_override)
    if temp:
        config["temperature"] = float(temp)
    max_tok = _get_config("GEMINI_MAX_TOKENS", "", config_override)
    if max_tok:
        config["max_output_tokens"] = int(max_tok)

    return client.models.generate_content(
        model=model, contents=contents, config=config if config else None
    ).text


def _call_openai(conversation: list[dict], config_override: dict = None) -> str:
    from openai import OpenAI

    client = OpenAI(
        api_key=_get_config("OPENAI_API_KEY", "", config_override),
    )

    model = _get_config("OPENAI_MODEL", "gpt-5.1", config_override)

    messages = []
    for turn in conversation:
        if "prompt" in turn:
            messages.append({"role": "user", "content": turn["prompt"]})
        if "response" in turn:
            messages.append({"role": "assistant", "content": turn["response"]})

    return client.chat.completions.create(
        model=model, messages=messages,
        reasoning_effort="medium",
    ).choices[0].message.content

def _call_trapi(conversation: list[dict], config_override: dict = None) -> str:
    from azure.identity import (
        AzureCliCredential,
        ChainedTokenCredential,
        ManagedIdentityCredential,
        get_bearer_token_provider,
    )
    from openai import AzureOpenAI

    model = _get_config("TRAPI_MODEL", "gpt-5.1_2025-11-13", config_override)

    # Set up Azure AD authentication
    credential = get_bearer_token_provider(
        ChainedTokenCredential(
            AzureCliCredential(),
            ManagedIdentityCredential(),
        ),
        _get_config("AZURE_OPENAI_SCOPE", "api://trapi/.default", config_override),
    )

    # Create client
    client = AzureOpenAI(
        azure_endpoint=_get_config(
            "AZURE_OPENAI_ENDPOINT",
            "https://trapi.research.microsoft.com/msraif/shared",
            config_override
        ),
        azure_ad_token_provider=credential,
        api_version=_get_config("AZURE_OPENAI_API_VERSION", "2024-12-01-preview", config_override),
    )

    # Convert conversation to messages format
    messages = []
    for turn in conversation:
        if "prompt" in turn:
            messages.append({"role": "user", "content": turn["prompt"]})
        if "response" in turn:
            messages.append({"role": "assistant", "content": turn["response"]})

    # Make the call
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        max_completion_tokens=16384,
        stream=False,
    )

    return response.choices[0].message.content or ""

def _call_vllm(conversation: list[dict], config_override: dict = None) -> str:
    from openai import OpenAI

    client = OpenAI(
        base_url=_get_config("VLLM_BASE_URL", "http://localhost:8000/v1", config_override),
        api_key=_get_config("VLLM_API_KEY", "EMPTY", config_override),
    )

    model = _get_config("VLLM_MODEL", "Qwen/Qwen3-8B", config_override)
    temp = float(_get_config("VLLM_TEMPERATURE", "0.7", config_override))
    max_tok_str = _get_config("VLLM_MAX_TOKENS", "2048", config_override)
    max_tok = int(max_tok_str) if max_tok_str else None

    messages = []
    for turn in conversation:
        if "prompt" in turn:
            messages.append({"role": "user", "content": turn["prompt"]})
        if "response" in turn:
            messages.append({"role": "assistant", "content": turn["response"]})

    return client.chat.completions.create(
        model=model, messages=messages, temperature=temp, max_tokens=max_tok
    ).choices[0].message.content

def _call_human_cli(conversation: list[dict], config_override: dict = None) -> str:
    """
    Interactive CLI version with menus and validation.
    Provides a user-friendly guided experience for human players.
    """
    from .human_cli_interactive import interactive_cli
    return interactive_cli(conversation)

def _call_human(conversation: list[dict], config_override: dict = None) -> str:
    """
    Display the conversation and wait for human input.

    Args:
        conversation: List of conversation turns with "prompt" and "response" keys
        config_override: Not used, kept for consistency

    Returns:
        Human's response as a string
    """
    print("\n" + "="*60)
    print("HUMAN INPUT REQUIRED")
    print("="*60)

    # Display conversation history
    if conversation:
        print("\n--- Conversation History ---")
        for i, turn in enumerate(conversation, 1):
            if "prompt" in turn:
                print(f"\nUser (turn {i}):")
                print(turn["prompt"])
            if "response" in turn:
                print(f"\nAssistant (turn {i}):")
                print(turn["response"])

    # Get the latest prompt to respond to
    latest_prompt = None
    for turn in reversed(conversation):
        if "prompt" in turn and "response" not in turn:
            latest_prompt = turn["prompt"]
            break
        elif "prompt" in turn:
            # If we found a prompt that already has a response, we're looking for the next one
            continue

    if latest_prompt:
        print("\n" + "="*60)
        print("Current Prompt:")
        print(latest_prompt)

    print("\n" + "="*60)
    print("Enter your response (press Enter twice when done):")
    print("="*60)

    # Read multi-line input
    lines = []
    empty_line_count = 0
    while True:
        try:
            line = input()
            if line == "":
                empty_line_count += 1
                if empty_line_count >= 2:
                    break
                lines.append(line)
            else:
                empty_line_count = 0
                lines.append(line)
        except EOFError:
            break

    response = "\n".join(lines).strip()

    print("\n" + "="*60)
    print("Response recorded. Continuing...")
    print("="*60 + "\n")

    return response

if __name__ == "__main__":
    import sys

    # Parse command-line arguments
    provider = sys.argv[1] if len(sys.argv) > 1 else None
    model = sys.argv[2] if len(sys.argv) > 2 else None

    # Determine what we're testing with
    if provider:
        print(f"Testing with provider: {provider}" + (f", model: {model}" if model else ""))
    else:
        print(f"Testing with provider: {os.getenv('LLM_PROVIDER', 'gemini')}\n")

    print("\nTest 1: Single prompt")
    response1 = call_llm([{"prompt": "Hello, how are you?"}], provider=provider, model=model)
    print(f"Response: {response1}\n")

    print("Test 2: Multi-turn conversation")
    response2 = call_llm([
        {"prompt": "What is 2+2?", "response": "2+2 equals 4."},
        {"prompt": "What about 3+3?"}
    ], provider=provider, model=model)
    print(f"Response: {response2}\n")
