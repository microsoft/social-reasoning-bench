# Model name -> deployment name mapping
# Reference: models.tsv
# Note: Only includes models verified to work via test_api_version_matrix.py
DEPLOYMENTS: dict[str, str] = {
    # GPT-4o series
    "gpt-4o": "gpt-4o_2024-11-20",
    "gpt-4o-mini": "gpt-4o-mini_2024-07-18",
    # GPT-4.1 series
    "gpt-4.1": "gpt-4.1_2025-04-14",
    "gpt-4.1-mini": "gpt-4.1-mini_2025-04-14",
    "gpt-4.1-nano": "gpt-4.1-nano_2025-04-14",
    # GPT-5 series
    "gpt-5": "gpt-5_2025-08-07",
    "gpt-5-chat": "gpt-5-chat_2025-10-03",
    "gpt-5-mini": "gpt-5-mini_2025-08-07",
    "gpt-5-nano": "gpt-5-nano_2025-08-07",
    # GPT-5.1 series
    "gpt-5.1": "gpt-5.1_2025-11-13",
    "gpt-5.1-chat": "gpt-5.1-chat_2025-11-13",
    # GPT-5.2 series
    "gpt-5.2": "gpt-5.2_2025-12-11",
    "gpt-5.2-chat": "gpt-5.2-chat_2025-12-11",
    # Reasoning models
    "o1": "o1_2024-12-17",
    "o3": "o3_2025-04-16",
    "o3-mini": "o3-mini_2025-01-31",
    "o4-mini": "o4-mini_2025-04-16",
    # Grok series
    # "grok-3": "grok-3_1",
    # "grok-4": "grok-4_1",
    # "grok-4-fast-non-reasoning": "grok-4-fast-non-reasoning_1",
    # "grok-4-fast-reasoning": "grok-4-fast-reasoning_1",
    # "grok-code-fast-1": "grok-code-fast-1_1",
    # Other models
    "Llama-3.3-70B-Instruct": "Llama-3.3-70B-Instruct_5",
    "Mistral-Large-3": "Mistral-Large-3_1",
    "model-router": "model-router_2025-11-18",
}


def get_model_deployment(model: str) -> str:
    """Get Azure deployment name for a model."""
    return DEPLOYMENTS.get(model, model)
