"""System prompt presets for calendar scheduling assistant.

Each preset is defined in its own module file. Use get_system_prompt() to
retrieve a prompt by name, or list_available_presets() to see all options.
"""

from .default import SYSTEM_PROMPT as DEFAULT_SYSTEM_PROMPT
from .privacy_ci import SYSTEM_PROMPT as PRIVACY_CI_SYSTEM_PROMPT
from .privacy_simple import SYSTEM_PROMPT as PRIVACY_SIMPLE_SYSTEM_PROMPT
from .privacy_strong import SYSTEM_PROMPT as PRIVACY_STRONG_SYSTEM_PROMPT
from .privacy_tom import SYSTEM_PROMPT as PRIVACY_TOM_SYSTEM_PROMPT
from .privacy_tom_dual import SYSTEM_PROMPT as PRIVACY_TOM_DUAL_SYSTEM_PROMPT

SYSTEM_PROMPT_PRESETS: dict[str, str | None] = {
    "none": None,
    "default": DEFAULT_SYSTEM_PROMPT,
    "privacy-simple": PRIVACY_SIMPLE_SYSTEM_PROMPT,
    "privacy-strong": PRIVACY_STRONG_SYSTEM_PROMPT,
    "privacy-ci": PRIVACY_CI_SYSTEM_PROMPT,
    "privacy-tom": PRIVACY_TOM_SYSTEM_PROMPT,
    "privacy-tom-dual": PRIVACY_TOM_DUAL_SYSTEM_PROMPT,
}


def get_system_prompt(preset_name: str = "default") -> str | None:
    """Get a system prompt by preset name.

    Args:
        preset_name: Name of the preset.
            Use "none" to omit the system message entirely.

    Returns:
        The system prompt string, or None if preset is "none"

    Raises:
        ValueError: If preset_name is not recognized
    """
    if preset_name not in SYSTEM_PROMPT_PRESETS:
        available = ", ".join(sorted(SYSTEM_PROMPT_PRESETS.keys()))
        raise ValueError(f"Unknown system prompt preset '{preset_name}'. Available: {available}")
    return SYSTEM_PROMPT_PRESETS[preset_name]


def list_available_presets() -> list[str]:
    """Return list of available preset names."""
    return list(SYSTEM_PROMPT_PRESETS.keys())
