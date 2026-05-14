"""Prompt-formatting helpers shared by calendar agents.

The former ``CalendarAgent`` intermediate base class has been removed; both
:class:`CalendarAssistantAgent` and :class:`CalendarRequestorAgent` now
inherit directly from :class:`BaseAgent`. Recipient allow-list enforcement
moved to :class:`AgentResources` (env-side), so the agents no longer need a
shared base class.

This module retains only the prompt-formatting helpers that both agent
classes use, plus exports for downstream consumers (conftest, etc.).
"""

from __future__ import annotations

from ..types import TimeSlotPreference


def format_preferences_for_prompt(preferences: list[TimeSlotPreference]) -> str:
    """Format scheduling preferences as natural language for the LLM.

    Args:
        preferences: List of time slot preferences with scores indicating
            desirability. Each preference is sorted by score descending and
            mapped to a human-readable strength label.

    Returns:
        A newline-separated string of formatted preferences, or an empty
        string if no preferences are provided.
    """
    if not preferences:
        return ""

    sorted_prefs = sorted(preferences, key=lambda p: p.score, reverse=True)

    lines = ["\nHere are my scheduling preferences:"]
    for pref in sorted_prefs:
        if pref.score >= 0.8:
            strength = "Strongly preferred"
        elif pref.score >= 0.5:
            strength = "Moderately preferred"
        elif pref.score >= 0.25:
            strength = "Slightly preferred"
        else:
            strength = "Not preferred"

        lines.append(f"- {pref.start_time}-{pref.end_time}: {strength}")

    return "\n".join(lines)
