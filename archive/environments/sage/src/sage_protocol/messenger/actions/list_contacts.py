from typing import Literal

from magentic_marketplace.platform.shared.models import BaseAction
from pydantic import BaseModel, Field


class ListContacts(BaseAction):
    """List all available contacts in the system.

    Returns a paginated list of all contacts you can communicate with, including
    their full names and contact IDs. Use the contact IDs to send direct messages
    or create groups. The list includes all agents registered in the marketplace.
    """

    type: Literal["ListContacts"] = "ListContacts"
    page: int = Field(
        default=1,
        ge=1,
        description=(
            "Page number to retrieve (starts at 1). Use total_pages to know how many pages exist."
        ),
    )
    limit: int = Field(
        default=100,
        ge=1,
        le=1000,
        description=("Maximum number of contacts to return per page (1-1000). Default is 100."),
    )


class Contact(BaseModel):
    full_name: str
    contact_id: str


class ListContactsResponse(BaseModel):
    contacts: list[Contact]
    page: int
    total_pages: int
