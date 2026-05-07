"""Shared, domain-agnostic system prompt presets.

Quick start::

    from . import SystemPrompt

    prompt = SystemPrompt(
        preset="privacy",
        role="You are an assistant.",
        domain="You have access to sensitive records.",
    )
    system_prompt = prompt.build()
"""

from .assistant_system_prompts import (
    DD_ADVOCACY,
    DD_INFO_GATHERING,
    OO,
    PRIVACY,
    SYSTEM_PROMPT_REGISTRY,
    SystemPrompt,
    SystemPromptPreset,
)

__all__ = [
    "PRIVACY",
    "DD_INFO_GATHERING",
    "DD_ADVOCACY",
    "OO",
    "SYSTEM_PROMPT_REGISTRY",
    "SystemPromptPreset",
    "SystemPrompt",
]
