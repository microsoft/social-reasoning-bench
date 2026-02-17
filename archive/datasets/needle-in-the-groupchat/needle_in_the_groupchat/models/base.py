"""Base model types for needle-in-the-groupchat."""

from pydantic import BaseModel, Field


class User(BaseModel):
    """A user in the group conversation."""

    name: str
    description: str = Field(default="", description="Optional description for persona generation")


class Message(BaseModel):
    """A single message in the conversation."""

    user: str = Field(description="User name who sent the message")
    content: str = Field(description="Message content")
