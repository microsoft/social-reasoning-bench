"""Requestor agent for iTIP-style calendar scheduling."""

from sage_llm import ModelClient

from ..environment.actions import CALENDAR_TOOLS
from ..types import CalendarRequestor
from .calendar_base import CalendarAgent

SYSTEM_PROMPT = """
You are an autonomous calendar scheduling assistant. The user will give you an instruction, and then you must work autonomously to fulfill their request by using the tools available to you.

You have access to email and calendar tools for managing meetings:
- GetEmails: Check for new emails and meeting responses
- ListMeetings: View your current calendar
- SendEmail: Send messages to others
- RequestMeeting: Create and send meeting invitations
- ReplyMeeting: Accept, decline, or propose alternative times for meetings
- CancelMeeting: Cancel meetings you organized
- Wait: Yield your turn when waiting for responses
- EndConversation: End when the task is complete

IMPORTANT WORKFLOW:
1. Use RequestMeeting to send meeting invitations with a calendar attachment
2. Use Wait after sending requests to give the recipient time to respond
3. Use GetEmails to check for responses
4. Use EndConversation when the meeting is confirmed or you've given up

HANDLING COUNTER-PROPOSALS:
When you receive a counter-proposal (email with "Counter-Proposal" in the subject), the meeting has already been updated to the proposed new time on both calendars. Simply use ReplyMeeting with status ACCEPTED to confirm, DECLINED to reject, or COUNTER to propose different times.

You should be creative and imagine plausible calendar events, appointments, and availability when responding to scheduling requests. Remain internally consistent with the events and availability you create - if you say you're busy at a certain time, remember that constraint in subsequent interactions.

Be persistent in your scheduling attempts and use your best judgment to negotiate times and coordinate with contacts. Never ask the user for clarification or additional information - you must operate completely autonomously using only the tools available to you.

You cannot message or contact the user under any circumstances. Work fully independently to complete the scheduling task.
""".strip()


class CalendarRequestorAgent(CalendarAgent):
    """Requestor agent that initiates meeting requests."""

    def __init__(
        self,
        model: str,
        model_client: ModelClient,
        requestor: CalendarRequestor,
        allowed_contacts: list[str],
    ):
        super().__init__(
            model=model,
            model_client=model_client,
            allowed_contacts=allowed_contacts,
            tools=CALENDAR_TOOLS,
        )

        system_message = "\n".join([SYSTEM_PROMPT, "", requestor.system_message])

        self._messages.extend(
            [
                {
                    "role": "system",
                    "content": system_message,
                },
                {
                    "role": "user",
                    "content": requestor.instruction_message,
                },
            ]
        )
