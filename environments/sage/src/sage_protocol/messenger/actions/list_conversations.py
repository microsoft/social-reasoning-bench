from typing import Literal

from magentic_marketplace.platform.shared.models import BaseAction
from pydantic import AwareDatetime, BaseModel, Field


class ListConversations(BaseAction):
    """List conversations the agent is part of that have at least one message.

    Returns a list of direct message conversations and group chats where
    there is at least one message. Each conversation includes metadata like
    the most recent message timestamp and unread count.

    The mode parameter filters which conversations are returned:
    - "unread": Only conversations with unread messages (unread_count > 0)
    - "all": All conversations regardless of unread status

    Use offset and limit for pagination of results.
    """

    type: Literal["ListConversations"] = "ListConversations"
    offset: int | None = Field(
        default=None, description="Number of conversations to skip for pagination"
    )
    limit: int | None = Field(default=None, description="Maximum number of conversations to return")
    mode: Literal["unread", "all"] = Field(
        default="unread", description="Filter conversations by read status"
    )


class ConversationInfo(BaseModel):
    """Information about a conversation."""

    conversation_type: Literal["direct", "group"]
    conversation_id: str  # Contact ID for direct, group ID for groups
    conversation_name: str  # Contact name for direct, group name for groups
    message_count: int  # Total number of messages in this conversation
    unread_count: int  # Number of unread messages
    last_message_at: AwareDatetime  # Timestamp of most recent message
    last_message_from: str  # Sender of most recent message


class ListConversationsResponse(BaseModel):
    conversations: list[ConversationInfo]
