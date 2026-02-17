from typing import Literal

from magentic_marketplace.platform.shared.models import BaseAction
from pydantic import Field


class SendMessageToConversation(BaseAction):
    """Send a message to a contact or group.

    Sends a message to either a one-on-one conversation (direct message) or a
    group conversation. The conversation_id can be either:
    - A contact ID for direct messages (use ListContacts to get contact IDs)
    - A group ID for group messages (use CreateGroup to get group IDs)

    The recipient(s) will see this message when they call CheckMessages.
    """

    type: Literal["SendMessage"] = "SendMessage"
    conversation_id: str = Field(
        description=(
            "ID of the conversation - either a contact ID for direct messages or a group ID for group messages"
        )
    )
    message: str = Field(description="Text content of the message to send")
