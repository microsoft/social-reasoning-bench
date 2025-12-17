from openai import OpenAI

from ..environments.calendar import CALENDAR_TOOLS
from ..types import CalendarAssistant, Tool
from .base import MessengerAgent


class EndConversation(Tool):
    """End the conversation."""


SYSTEM_PROMPT = f"""
You are an autonomous calendar scheduling assistant. The user will give you an instruction, and then you must work autonomously to fulfill their request by using the tools available to you. 

You have access to messaging and calendaring tools, as well as a "{EndConversation.get_name()}" tool that you should call when you are confident you have handled all requests fully.
""".strip()


class CalendarAssistantAgent(MessengerAgent):
    def __init__(
        self,
        model: str,
        model_client: OpenAI,
        assistant: CalendarAssistant,
        allowed_contacts: list[str],
    ):
        super().__init__(
            model=model,
            model_client=model_client,
            allowed_contacts=allowed_contacts,
            tools=[EndConversation] + CALENDAR_TOOLS,
        )

        system_message = "\n".join([SYSTEM_PROMPT, "", assistant.system_message])

        self._messages.extend(
            [
                {
                    "role": "system",
                    "content": system_message,
                },
                {
                    "role": "user",
                    "content": assistant.instruction_message,
                },
            ]
        )
