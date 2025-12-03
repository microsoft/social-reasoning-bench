import hashlib

from magentic_marketplace.platform.database import queries
from magentic_marketplace.platform.database.base import BaseDatabaseController, Query
from magentic_marketplace.platform.shared.models import (
    ActionExecutionResult,
    AgentProfile,
)

from ..actions import CreateGroup, GroupInfo


async def handle_create_group(
    request: CreateGroup,
    agent: AgentProfile,
    database: BaseDatabaseController,
) -> ActionExecutionResult:
    """Handle CreateGroup action - validate members and check for duplicates.

    The creator is automatically added to the members list.
    """
    if not request.members:
        raise ValueError("CreateGroup.members must contain at least one member.")

    # Automatically add creator to members if not already present
    all_members = list(request.members)
    if agent.id not in all_members:
        all_members.append(agent.id)

    # Verify all members exist
    query: Query | None = None
    for member_id in all_members:
        q = queries.agents.id(value=member_id, operator="LIKE")
        if query is None:
            query = q
        else:
            query = query | q

    if query is None:
        # Won't happen, but included for type checking
        raise ValueError("Query cannot be None")

    rows = await database.agents.find(query)
    invalid_members = set(all_members).difference([row.data.id for row in rows])
    if invalid_members:
        raise ValueError(f"Invalid members: {invalid_members}")

    # Create deterministic group ID based on sorted members (including creator)
    normalized_members = sorted(all_members)
    members_hash = hashlib.sha256("|".join(normalized_members).encode()).hexdigest()[:16]
    group_id = f"group_{members_hash}"

    # Check if a group with the same members already exists
    create_group_actions = await database.actions.find(
        query=queries.actions.request_name(value="CreateGroup", operator="=")
    )

    for action_row in create_group_actions:
        if action_row.data.request.name == "CreateGroup":
            # Check if this CreateGroup had the same final members
            # Use result.content.members instead of request.parameters.members
            # because request doesn't include auto-added creator
            existing_result = action_row.data.result
            if existing_result.content and isinstance(existing_result.content, dict):
                existing_group_members = existing_result.content.get("members", [])
                existing_group_members_sorted = sorted(existing_group_members)

                if existing_group_members_sorted == normalized_members:
                    # Return error with existing group ID
                    existing_group_id = existing_result.content.get("id", group_id)

                    return ActionExecutionResult(
                        content=f"Group with members {request.members} already exists with ID: {existing_group_id}",
                        is_error=True,
                        metadata={"existing_group_id": existing_group_id},
                    )

    # Create new group info (with creator automatically included)
    group_info = GroupInfo(
        id=group_id,
        name=request.name,
        members=all_members,
        created_by=agent.id,
    )

    return ActionExecutionResult(content=group_info)
