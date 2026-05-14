"""Base agent class for calendar scheduling interactions."""

from __future__ import annotations

from srbench_llm import SRBenchModelClient

from ....shared.agent import BaseAgent
from ..environment.actions import CALENDAR_TOOLS
from ..types import TimeSlotPreference, Tool


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

    # Sort by score descending to present strongest preferences first
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


class CalendarAgent(BaseAgent):
    """Base agent class for calendar scheduling.

    Thin :class:`BaseAgent` subclass that defaults the tool registry to
    :data:`CALENDAR_TOOLS` and labels the prompt-tracking bucket.

    Recipient allow-listing for ``SendEmail`` now lives env-side on
    :class:`AgentResources` (via the ``allowed_recipients`` ctor param);
    this class no longer stores or enforces an allow-list.
    """

    def __init__(
        self,
        model: str,
        model_client: SRBenchModelClient,
        tools: list[type[Tool]] | None = None,
        explicit_cot: bool = False,
        prompt_label: str = "cal_agent",
        max_actions: int = 50,
    ):
        # Default to all calendar tools if none specified
        tool_list: list[type[Tool]] = list(tools) if tools is not None else list(CALENDAR_TOOLS)

        super().__init__(
            model=model,
            model_client=model_client,
            tools=tool_list,
            explicit_cot=explicit_cot,
            prompt_label=prompt_label,
            max_actions=max_actions,
        )
