"""Base agent class for calendar scheduling interactions."""

from __future__ import annotations

from srbench_llm import SRBenchModelClient

from ....shared.agent import LLMAgent, RetryException
from ..environment.actions import (
    CALENDAR_TOOLS,
    SendEmail,
)
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


class CalendarAgent(LLMAgent):
    """Base agent class for calendar scheduling.

    This agent supports multi-step turns where it can call multiple tools
    before yielding with Wait or ending with EndConversation.

    Extends :class:`LLMAgent` with:
    - Default tool set (``CALENDAR_TOOLS``)
    - ``SendEmail`` recipient validation via :meth:`validate_tool_call`
    """

    def __init__(
        self,
        model: str,
        model_client: SRBenchModelClient,
        allowed_contacts: list[str],
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

        self._allowed_contacts = list(allowed_contacts)

    # ------------------------------------------------------------------ #
    # Validation hook
    # ------------------------------------------------------------------ #

    def validate_tool_call(self, tool_call: Tool) -> None:
        """Reject SendEmail calls to recipients not in the allowed contacts list.

        Args:
            tool_call: The parsed tool call to validate.

        Raises:
            RetryException: If the tool call is a ``SendEmail`` to a recipient
                not in the allowed contacts list.
        """
        if isinstance(tool_call, SendEmail) and tool_call.to not in self._allowed_contacts:
            raise RetryException(
                f"Cannot SendEmail to {tool_call.to}. "
                f"Supported recipients are: {self._allowed_contacts}"
            )
