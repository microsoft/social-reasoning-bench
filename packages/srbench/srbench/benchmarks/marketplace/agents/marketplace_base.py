"""Shared prompt-construction helper for marketplace agents.

The former ``MarketplaceAgent`` intermediate base class has been removed.
Both :class:`BuyerAgent` and :class:`SellerAgent` now inherit directly from
:class:`BaseAgent`. The ``add_new_messages`` injection pattern is gone (the
env's blocking ``GetMessages`` makes it unnecessary). ``add_turn_marker`` is
also gone since there are no rounds.

This module retains a single helper, :func:`build_initial_messages`, that
both concrete agents call to seed their system + user message pair.
"""

from __future__ import annotations

from srbench_llm import SRBenchInputMessage

from ..prompts.system import (
    MKT_ROLE,
    PRESETS,
    get_system_prompt,
    list_available_presets,
)

__all__ = [
    "MKT_ROLE",
    "PRESETS",
    "get_system_prompt",
    "list_available_presets",
    "build_initial_messages",
]


def build_initial_messages(
    *,
    system_prompt: str | None,
    instruction_message: str,
    malicious_prompt: str | None = None,
) -> list[SRBenchInputMessage]:
    """Construct the (system, user) message pair for a marketplace agent.

    If ``malicious_prompt`` is set, it replaces the system prompt entirely
    and no user instruction is appended (matches the previous
    ``_init_malicious`` behavior).
    """
    if malicious_prompt:
        return [{"role": "system", "content": malicious_prompt.strip()}]
    effective_system_prompt = system_prompt.strip() if system_prompt else MKT_ROLE
    return [
        {"role": "system", "content": effective_system_prompt},
        {"role": "user", "content": instruction_message.strip()},
    ]
