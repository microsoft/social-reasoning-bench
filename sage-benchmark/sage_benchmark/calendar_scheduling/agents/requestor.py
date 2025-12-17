from openai import OpenAI

from ..types import CalendarRequestor
from .base import MessengerAgent

SYSTEM_PROMPT = f"""
You are an autonomous calendar scheduling assistant. The user will give you an instruction, and then you must work autonomously to fulfill their request by using the tools available to you.

You should be creative and imagine plausible calendar events, appointments, and availability when responding to scheduling requests. Remain internally consistent with the events and availability you create - if you say you're busy at a certain time, remember that constraint in subsequent interactions.

Be persistent in your scheduling attempts and use your best judgment to negotiate times and coordinate with contacts. Never ask the user for clarification or additional information - you must operate completely autonomously using only the tools available to you.

You cannot message or contact the user under any circumstances. Work fully independently to complete the scheduling task.
""".strip()


class CalendarRequestorAgent(MessengerAgent):
    def __init__(
        self,
        model: str,
        model_client: OpenAI,
        requestor: CalendarRequestor,
        allowed_contacts: list[str],
    ):
        # No additional tools, just the messenger tools
        super().__init__(model=model, model_client=model_client, allowed_contacts=allowed_contacts)

        system_message = "\n".join([SYSTEM_PROMPT, "", requestor.system_message])

        instruction_message = "\n".join(
            [
                requestor.instruction_message,
                "",
                "Request Event:",
                "```json",
                requestor.event.model_dump_json(),
                "```",
            ]
        )

        self._messages.extend(
            [
                {
                    "role": "system",
                    "content": system_message,
                },
                {
                    "role": "user",
                    "content": instruction_message,
                },
            ]
        )
