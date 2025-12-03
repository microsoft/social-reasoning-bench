import math

from magentic_marketplace.platform.database import queries
from magentic_marketplace.platform.database.base import BaseDatabaseController
from magentic_marketplace.platform.shared.models import (
    ActionExecutionResult,
    AgentProfile,
)

from ..actions import Contact, ListContacts, ListContactsResponse


async def handle_list_contacts(
    request: ListContacts,
    agent: AgentProfile,
    database: BaseDatabaseController,
) -> ActionExecutionResult:
    """Handle ListContacts action - list all contacts with pagination."""
    # Get all agents
    rows = await database.agents.find(query=queries.agents.id(value="%", operator="LIKE"))

    # Build all contacts
    all_contacts = []
    for row in rows:
        # Try to get full_name from profile, fallback to id
        full_name = getattr(row.data, "full_name", row.data.id)
        all_contacts.append(Contact(full_name=full_name, contact_id=row.data.id))

    # Calculate pagination
    total_contacts = len(all_contacts)
    total_pages = math.ceil(total_contacts / request.limit) if total_contacts > 0 else 1

    # Ensure page is within bounds
    page = min(request.page, total_pages)

    # Get the slice for this page
    start_idx = (page - 1) * request.limit
    end_idx = start_idx + request.limit
    page_contacts = all_contacts[start_idx:end_idx]

    return ActionExecutionResult(
        content=ListContactsResponse(contacts=page_contacts, page=page, total_pages=total_pages)
    )
