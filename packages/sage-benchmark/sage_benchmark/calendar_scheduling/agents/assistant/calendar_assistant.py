"""Assistant agent for iTIP-style calendar scheduling."""

from sage_llm import ModelClient

from ...environment.actions import CALENDAR_TOOLS, EndConversation
from ...types import CalendarAssistant, TimeSlotPreference
from ..calendar_base import CalendarAgent
from .prompts import DEFAULT_SYSTEM_PROMPT

# Backward compatibility alias
SYSTEM_PROMPT = DEFAULT_SYSTEM_PROMPT


def format_preferences_for_prompt(preferences: list[TimeSlotPreference]) -> str:
    """Format scheduling preferences as natural language for the LLM."""
    if not preferences:
        return ""

    # Sort by score descending to present strongest preferences first
    sorted_prefs = sorted(preferences, key=lambda p: p.score, reverse=True)

    lines = ["\nScheduling preferences:"]
    for pref in sorted_prefs:
        if pref.score >= 0.8:
            strength = "Strongly prefer"
        elif pref.score >= 0.5:
            strength = "Prefer"
        elif pref.score >= 0.3:
            strength = "Acceptable but not ideal"
        else:
            strength = "Avoid if possible"

        lines.append(f"- {pref.start_time}-{pref.end_time}: {strength}")

    return "\n".join(lines)


class CalendarAssistantAgent(CalendarAgent):
    """Assistant agent that responds to meeting requests."""

    def __init__(
        self,
        model: str,
        model_client: ModelClient,
        assistant: CalendarAssistant,
        allowed_contacts: list[str],
        system_prompt: str | None = None,
        explicit_cot: bool = False,
        expose_preferences: bool = False,
    ):
        super().__init__(
            model=model,
            model_client=model_client,
            allowed_contacts=allowed_contacts,
            tools=CALENDAR_TOOLS + [EndConversation],
            explicit_cot=explicit_cot,
        )

        # Only add system message if a prompt is provided
        if system_prompt is not None:
            self._messages.append({"role": "system", "content": system_prompt})

        # Build instruction with preferences if exposed
        instruction = assistant.instruction_message
        if assistant.preferences and expose_preferences:
            instruction += format_preferences_for_prompt(assistant.preferences)

        self._messages.append({"role": "user", "content": instruction})
