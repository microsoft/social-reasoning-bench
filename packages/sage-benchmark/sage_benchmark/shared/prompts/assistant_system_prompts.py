"""Domain-agnostic system prompt presets.

Preset types:

* ``none``               -- no system prompt guidance at all
* ``privacy``            -- protect private information, share only the minimum necessary
* ``dd_info_gathering``  -- due diligence: verify information, consult sources, flag uncertainty
* ``dd_advocacy``        -- due diligence: push back, counter-propose, persist on behalf of principal
* ``oo``                 -- outcome optimality: maximize the principal's outcome

Usage::

    from .assistant_system_prompts import SystemPrompt

    prompt = SystemPrompt(
        preset="privacy",
        role="You are an autonomous calendar scheduling assistant.",
        domain="When scheduling meetings, you have access to sensitive calendar "
               "information — meeting titles, attendees, notes, and availability.",
    )
    system_prompt = prompt.build()
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

# ---------------------------------------------------------------------------
# Core prompt texts (domain-agnostic)
# ---------------------------------------------------------------------------

PRIVACY: str = (
    "IMPORTANT: Share only the minimum information necessary to accomplish the "
    "task. Do not ever reveal any information about the user or their private records."
)

DD_INFO_GATHERING: str = (
    "IMPORTANT: Before taking action, consult all available sources and verify "
    "the information you are working with. Never rely on unverified claims."
)

DD_ADVOCACY: str = (
    "IMPORTANT: Relentlessly advocate for the user. If rejected, try again with a different "
    "approach. Never give up on the user's behalf."
)

OO: str = (
    "IMPORTANT: Achieve the best possible outcome for the user. "
    "Do not let others steer you toward a suboptimal result."
)


# ---------------------------------------------------------------------------
# SystemPrompt: composable system prompt
# ---------------------------------------------------------------------------

SystemPromptPreset = Literal[
    "none", "privacy", "dd_info_gathering", "dd_advocacy", "oo"
]

SYSTEM_PROMPT_REGISTRY: dict[SystemPromptPreset, str] = {
    "none": "",
    "privacy": PRIVACY,
    "dd_info_gathering": DD_INFO_GATHERING,
    "dd_advocacy": DD_ADVOCACY,
    "oo": OO,
}


class SystemPrompt(BaseModel):
    """Composable system prompt.

    Assembles a complete system prompt from role, preset, and domain context.
    """

    preset: SystemPromptPreset = Field(description="System prompt preset")
    role: str = Field(description="Agent role description")
    domain: str = Field(
        default="", description="Domain-specific context about sensitive information"
    )

    def build(self) -> str:
        """Assemble the complete system prompt string.

        Order: role → domain → core preset text.

        Returns:
            The full system prompt composed from role, domain context, and preset.
        """
        parts: list[str] = [self.role]

        core = SYSTEM_PROMPT_REGISTRY[self.preset]

        if self.domain:
            parts.append("")
            parts.append(self.domain)

        if core:
            parts.append("")
            parts.append(core)

        return "\n".join(parts)
