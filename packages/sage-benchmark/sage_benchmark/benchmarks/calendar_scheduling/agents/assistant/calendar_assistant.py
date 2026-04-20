"""Assistant agent for iTIP-style calendar scheduling."""

from sage_llm import SageMessage, SageModelClient

from ...environment.actions import CALENDAR_TOOLS, EndConversation
from ...types import CalendarAssistant
from ..calendar_base import CalendarAgent, format_preferences_for_prompt


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

        # Build system prompt: preset prompt + assistant identity
        identity = (
            f"You are {assistant.name}'s calendar scheduling personal assistant."
            if assistant.name
            else None
        )
        sys_parts = [p for p in [system_prompt, identity] if p]
        if sys_parts:
            self._messages.append({"role": "system", "content": "\n\n".join(sys_parts)})

        # Build user instruction with preferences if exposed
        instruction = assistant.instruction_message
        if assistant.preferences and expose_preferences:
            instruction += format_preferences_for_prompt(assistant.preferences)

        self._messages.append({"role": "user", "content": instruction})
