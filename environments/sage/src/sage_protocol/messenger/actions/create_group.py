from typing import Literal

from magentic_marketplace.platform.shared.models import BaseAction
from pydantic import BaseModel, Field


class CreateGroup(BaseAction):
    """Create a new group for multi-party conversations.

    Creates a group with the specified name and members. You (the creator) will
    automatically be added to the group. If a group with the exact same set of
    members already exists, this action will fail and return the existing group ID.
    Once created, use SendGroupMessage to send messages to all group members.
    """

    type: Literal["CreateGroup"] = "CreateGroup"
    name: str = Field(description="Name for the group (e.g., 'Project Team')")
    members: list[str] = Field(
        description=(
            "List of contact IDs to include in the group. You will be automatically added as the creator."
        )
    )


class GroupInfo(BaseModel):
    id: str
    name: str
    members: list[str]
    created_by: str
