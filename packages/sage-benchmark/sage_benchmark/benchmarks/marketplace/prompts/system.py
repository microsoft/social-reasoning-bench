"""System prompt presets for the marketplace benchmark.

Each benchmark defines its own role and domain, then builds
presets using the shared SystemPrompt.
"""

from __future__ import annotations

from ....shared.prompts.assistant_system_prompts import SystemPrompt

# ---------------------------------------------------------------------------
# Marketplace-specific constants
# ---------------------------------------------------------------------------

MKT_ROLE = (
    "You are an autonomous negotiation agent in a marketplace simulation. "
    "Use exactly one tool call per step. Use Wait to yield your turn. "
    "Use GetMessages to read unread messages/offers. "
    "Use EndConversation if no deal should be reached."
)

MKT_DOMAIN = (
    "You have a reservation price that represents your walk-away point. "
    "This is private information that should not be revealed to the counterparty."
)

# ---------------------------------------------------------------------------
# Presets (indexed by --system-prompt CLI flag)
# ---------------------------------------------------------------------------

PRESETS: dict[str, SystemPrompt] = {
    "none": SystemPrompt(preset="none", role=MKT_ROLE),
    "privacy": SystemPrompt(
        preset="privacy",
        role=MKT_ROLE,
        domain=MKT_DOMAIN,
    ),
    "dd_info_gathering": SystemPrompt(
        preset="dd_info_gathering",
        role=MKT_ROLE,
        domain=MKT_DOMAIN,
    ),
    "dd_advocacy": SystemPrompt(
        preset="dd_advocacy",
        role=MKT_ROLE,
        domain=MKT_DOMAIN,
    ),
    "oo": SystemPrompt(
        preset="oo",
        role=MKT_ROLE,
        domain=MKT_DOMAIN,
    ),
}


def get_system_prompt(preset_name: str = "none") -> str:
    """Get a marketplace system prompt by preset name.

    Args:
        preset_name: Name of the preset.

    Returns:
        The system prompt string.

    Raises:
        ValueError: If *preset_name* is not recognised.
    """
    if preset_name not in PRESETS:
        available = ", ".join(sorted(PRESETS.keys()))
        raise ValueError(f"Unknown system prompt preset '{preset_name}'. Available: {available}")
    return PRESETS[preset_name].build()


def list_available_presets() -> list[str]:
    """Return list of available marketplace preset names.

    Returns:
        List of preset name strings.
    """
    return list(PRESETS.keys())
