from magentic_marketplace.platform.database import queries
from magentic_marketplace.platform.database.base import BaseDatabaseController
from magentic_marketplace.platform.shared.models import (
    ActionExecutionResult,
    AgentProfile,
)

from ..actions import SendMessageToConversation


async def handle_send_message(
    request: SendMessageToConversation,
    agent: AgentProfile,
    database: BaseDatabaseController,
) -> ActionExecutionResult:
    """Handle SendMessage action.

    Validates conversation exists (contact or group) and sends message.
    """

    # First, try to find the conversation_id as a contact
    contact_rows = await database.agents.find(
        query=queries.agents.id(value=request.conversation_id, operator="LIKE")
    )

    if contact_rows:
        # It's a direct message to a contact
        return ActionExecutionResult(content="Success")

    # If not a contact, try to find it as a group
    create_group_actions = await database.actions.find(
        query=queries.actions.request_name(value="CreateGroup", operator="=")
    )

    for action_row in create_group_actions:
        if action_row.data.request.name == "CreateGroup":
            result_content = action_row.data.result.content
            if isinstance(result_content, dict):
                if result_content.get("id") == request.conversation_id:
                    # Found the group, verify agent is a member
                    group_members = result_content.get("members", [])
                    if agent.id not in group_members:
                        raise ValueError(
                            f"Agent {agent.id} is not a member of group {request.conversation_id}"
                        )
                    return ActionExecutionResult(content="Success")

    # Conversation ID doesn't match any contact or group
    raise ValueError(
        f"Invalid conversation ID: {request.conversation_id}. Must be either a valid contact ID or group ID."
    )
