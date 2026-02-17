from typing import Literal

from magentic_marketplace.platform.shared.models import BaseAction
from pydantic import AwareDatetime, BaseModel, Field


class ReadMessages(BaseAction):
    """Read messages in a conversation.

    Retrieves messages from a conversation based on the specified mode:
    - "unread": Returns only unread messages (those after the last read index) and marks them as read
    - "all": Returns all messages in the conversation

    The conversation_id can be either:
    - A contact ID for direct messages
    - A group ID for group chats

    Use offset and limit for pagination of results.
    """

    type: Literal["ReadMessages"] = "ReadMessages"
    conversation_id: str = Field(
        description=(
            "The conversation ID - either a contact ID for direct messages or a group ID for group chats"
        )
    )
    offset: int | None = Field(
        default=None, description="Number of messages to skip for pagination"
    )
    limit: int | None = Field(default=None, description="Maximum number of messages to return")
    mode: Literal["unread", "all"] = Field(
        default="unread", description="Filter messages by read status"
    )


class Message(BaseModel):
    id: str
    from_: str
    conversation_id: str
    message: str
    sent_at: AwareDatetime


class ReadMessagesResponse(BaseModel):
    messages: list[Message]
