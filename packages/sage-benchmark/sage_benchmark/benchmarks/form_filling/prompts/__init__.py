"""Prompts for form filling benchmark."""

from .formatting import format_artifacts_as_context, translate_persona_to_text
from .interactive import INTERACTIVE_INSTRUCTION
from .system import (
    FF_DOMAIN,
    FF_EXAMPLES,
    FF_ROLE,
    PRESETS,
    construct_system_prompt,
)

__all__ = [
    # Formatting
    "translate_persona_to_text",
    "format_artifacts_as_context",
    # System prompts
    "construct_system_prompt",
    # Domain constants
    "FF_ROLE",
    "FF_DOMAIN",
    "FF_EXAMPLES",
    "PRESETS",
    # Interactive
    "INTERACTIVE_INSTRUCTION",
]
