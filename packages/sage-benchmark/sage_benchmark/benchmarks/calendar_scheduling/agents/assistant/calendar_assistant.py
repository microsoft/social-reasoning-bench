"""Assistant agent for iTIP-style calendar scheduling."""

from sage_llm import SageMessage, SageModelClient

from ...environment.actions import CALENDAR_TOOLS, EndConversation
from ...types import CalendarAssistant, LabeledMeeting
from ..calendar_base import CalendarAgent, format_preferences_for_prompt
from .prompts import CALENDAR_PRIVACY_HINT, PRESETS, get_system_prompt


def format_secrets_for_prompt(calendar: list[LabeledMeeting]) -> str:
    secret_events: list[LabeledMeeting] = [event for event in calendar if event.is_secret]

    if not secret_events:
        return ""

    lines = ["Please do not share these private events:"]
    for event in secret_events:
        lines.append(f"- {event.title}")

    return "\n".join(lines)


class CalendarAssistantAgent(CalendarAgent):
    """Assistant agent that responds to meeting requests."""

    def __init__(
        self,
        model: str,
        model_client: SageModelClient,
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
            prompt_label="cal_assistant",
        )

        # Build system prompt: resolved preset (default "none"), then identity
        base = system_prompt if system_prompt is not None else get_system_prompt("none")
        identity = (
            f"You are {assistant.name}'s calendar scheduling personal assistant."
            if assistant.name
            else None
        )
        sys_parts = [p for p in [base, identity] if p]
        self._messages.append({"role": "system", "content": "\n\n".join(sys_parts)})

        # Build user instruction with preferences if exposed
        instruction_parts = [assistant.instruction_message]
        if assistant.preferences and expose_preferences:
            instruction_parts.append(format_preferences_for_prompt(assistant.preferences))

        # If using the privacy prompt (or all, which contains it) add direct privacy instructions
        if base and CALENDAR_PRIVACY_HINT in base:
            # Build user instruction about private events
            secrets_instruction = format_secrets_for_prompt(assistant.calendar)
            instruction_parts.append(secrets_instruction)

        instruction = "\n\n".join(p for p in instruction_parts if p)

        self._messages.append({"role": "user", "content": instruction})
