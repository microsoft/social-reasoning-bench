"""Prompts for form filling benchmark."""

from .formatting import format_artifacts_as_context, translate_persona_to_text
from .interactive import INTERACTIVE_INSTRUCTION
from .privacy import PRIVACY_AWARE_SUFFIX, PRIVACY_CI_SUFFIX, PRIVACY_EXPLAINED_SUFFIX
from .system import (
    INTERVIEWER_BASE_SYSTEM_PROMPT,
    INTERVIEWER_DETAIL_SYSTEM_PROMPT,
    construct_interactive_system_prompt,
    get_interviewer_system_prompt,
)

__all__ = [
    # Formatting
    "translate_persona_to_text",
    "format_artifacts_as_context",
    # System prompts
    "construct_interactive_system_prompt",
    "get_interviewer_system_prompt",
    "INTERVIEWER_BASE_SYSTEM_PROMPT",
    "INTERVIEWER_DETAIL_SYSTEM_PROMPT",
    # Privacy
    "PRIVACY_AWARE_SUFFIX",
    "PRIVACY_EXPLAINED_SUFFIX",
    "PRIVACY_CI_SUFFIX",
    # Interactive
    "INTERACTIVE_INSTRUCTION",
]
