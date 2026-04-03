"""System prompt templates for the marketplace benchmark.

Every benchmark defines privacy-aware system prompts using the shared
``PrivacyPrompt`` class from ``sage_benchmark.shared.prompts.privacy``.

Canonical location: ``prompts/`` subpackage (co-located with the
benchmark they configure).

The pattern:
    1. Define a role description (what the agent does)
    2. Define domain context (what sensitive information exists)
    3. Define structured examples (appropriate/inappropriate disclosures)
    4. Build a PRESETS dict mapping level names -> PrivacyPrompt instances

The CLI's ``--system-prompt {none,simple,strong,ci}`` flag selects a
preset.
"""

from .system import (
    MKT_DOMAIN,
    MKT_EXAMPLES,
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
    "MKT_EXAMPLES",
]
