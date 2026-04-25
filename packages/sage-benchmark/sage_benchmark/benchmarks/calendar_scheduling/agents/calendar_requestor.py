"""Requestor agent for iTIP-style calendar scheduling."""

from sage_llm import SageModelClient

from ..environment.actions import CALENDAR_TOOLS
from ..types import CalendarRequestor
from .assistant.prompts import CALENDAR_ROLE
from .calendar_base import CalendarAgent, format_preferences_for_prompt


class CalendarRequestorAgent(CalendarAgent):
    """Requestor agent that initiates meeting requests."""

    def __init__(
        self,
        model: str,
        model_client: SageModelClient,
        requestor: CalendarRequestor,
        allowed_contacts: list[str],
        explicit_cot: bool = False,
        expose_preferences: bool = False,
    ):
        super().__init__(
            model=model,
            model_client=model_client,
            allowed_contacts=allowed_contacts,
            tools=CALENDAR_TOOLS,
            explicit_cot=explicit_cot,
            prompt_label="cal_requestor",
        )

        # Build system prompt: base role + requestor identity + malicious injection
        identity = (
            f"You are {requestor.name}'s calendar scheduling personal assistant."
            if requestor.name
            else None
        )
        sys_parts = [CALENDAR_ROLE, identity, requestor.malicious_prompt]
        system_content = "\n\n".join(p for p in sys_parts if p)

        # Build user instruction with preferences if exposed
        instruction = requestor.instruction_message
        if requestor.preferences and expose_preferences:
            instruction += format_preferences_for_prompt(requestor.preferences)

        self._messages.extend(
            [
                {"role": "system", "content": system_content},
                {"role": "user", "content": instruction},
            ]
        )
