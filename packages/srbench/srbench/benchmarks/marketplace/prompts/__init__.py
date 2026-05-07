"""System prompt templates for the marketplace benchmark.

Every benchmark defines system prompts using the shared
``SystemPrompt`` class from ``srbench.shared.prompts.assistant_system_prompts``.

Canonical location: ``prompts/`` subpackage (co-located with the
benchmark they configure).

The pattern:
    1. Define a role description (what the agent does)
    2. Define domain context (what sensitive information exists)
    3. Define structured examples (appropriate/inappropriate actions)
    4. Build a PRESETS dict mapping preset names -> SystemPrompt instances

The CLI's ``--system-prompt`` flag selects a preset.
"""

from .system import (
    MKT_DOMAIN,
    MKT_ROLE,
    PRESETS,
    get_system_prompt,
    list_available_presets,
)

__all__ = [
    "PRESETS",
    "get_system_prompt",
    "list_available_presets",
    "MKT_ROLE",
    "MKT_DOMAIN",
]
