"""Conversation model types for needle-in-the-groupchat."""

from pydantic import BaseModel, Field

from .base import Message, User
from .enums import EvaluationMode, NeedlePosition


class Conversation(BaseModel):
    """A complete group conversation with a needle message."""

    id: str = Field(description="Unique conversation ID")
    users: list[User] = Field(description="List of users in the conversation")
    messages: list[Message] = Field(description="All messages in the conversation")
    needle_message: str = Field(description="The needle message to find")
    needle_user: str = Field(description="User who sent the needle message")
    needle_position: NeedlePosition = Field(description="Position category of the needle")
    needle_index: int = Field(description="Exact index of the needle message")
    num_users: int = Field(description="Number of users in conversation")
    max_tokens: int = Field(description="Target max tokens for conversation")
    total_messages: int = Field(description="Total number of messages")
    total_tokens: int = Field(description="Actual token count of conversation")
    evaluation_mode: EvaluationMode = Field(
        default=EvaluationMode.EXACT_MATCH,
        description="Evaluation mode for this conversation",
    )


class PreferenceConversation(Conversation):
    """A conversation with a preference needle for semantic evaluation."""

    topic: str = Field(description="Conversation topic")
    preference: str = Field(description="The preference to recall (e.g., 'pizza', 'blue')")
    preference_category: str = Field(
        description="Category of preference (food, color, activity, etc.)"
    )
