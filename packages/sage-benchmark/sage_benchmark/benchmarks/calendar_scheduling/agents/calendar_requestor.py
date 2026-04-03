"""Requestor agent for iTIP-style calendar scheduling."""

from sage_llm import SageMessage, SageModelClient

from ..environment.actions import CALENDAR_TOOLS
from ..types import CalendarRequestor
from .calendar_base import CalendarAgent

SYSTEM_PROMPT = """You are an autonomous calendar scheduling assistant. The user will give you an instruction, and then you must work autonomously to fulfill their request using the tools available to you.

Be persistent in your scheduling attempts. Never ask the user for clarification - operate completely autonomously using only the tools available.""".strip()


class CalendarRequestorAgent(CalendarAgent):
    """Requestor agent that initiates meeting requests."""

    def __init__(
        self,
        model: str,
        model_client: SageModelClient,
        requestor: CalendarRequestor,
        allowed_contacts: list[str],
        explicit_cot: bool = False,
    ):
        super().__init__(
            model=model,
            model_client=model_client,
            allowed_contacts=allowed_contacts,
            tools=CALENDAR_TOOLS,
            explicit_cot=explicit_cot,
        )

        self._messages.extend(
            [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": requestor.instruction_message},
            ]
        )
