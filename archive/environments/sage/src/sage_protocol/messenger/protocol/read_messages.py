from magentic_marketplace.platform.database import queries
from magentic_marketplace.platform.database.base import BaseDatabaseController
from magentic_marketplace.platform.shared.models import (
    ActionExecutionResult,
    AgentProfile,
)

from ..actions import (
    Message,
    ReadMessages,
    ReadMessagesResponse,
    SendMessageToConversation,
)


async def handle_read_messages(
    request: ReadMessages,
    agent: AgentProfile,
    database: BaseDatabaseController,
) -> ActionExecutionResult:
    """Handle ReadMessages action - read messages in a conversation based on mode."""
    messages: list[Message] = []

    # Find the last ReadMessages action for this specific conversation to get
    # last read index
    prev_read_query = queries.actions.request_name(
        value="ReadMessages", operator="="
    ) & queries.actions.agent_id(value=agent.id, operator="=")

    previous_read_actions = await database.actions.find(query=prev_read_query)

    # Filter for the specific conversation
    last_read_index = -1
    for action_row in previous_read_actions:
        if action_row.data.request.name == "ReadMessages":
            params = action_row.data.request.parameters
            # Check if this was for the same conversation
            if params.get("conversation_id") == request.conversation_id:
                if action_row.index is not None and action_row.index > last_read_index:
                    last_read_index = action_row.index

    # Determine if this is a direct message or group conversation
    # First check if conversation_id is a contact
    contact_rows = await database.agents.find(
        query=queries.agents.id(value=request.conversation_id, operator="LIKE")
    )

    is_direct_message = bool(contact_rows)
    is_group = False

    if not is_direct_message:
        # Check if it's a group
        create_group_actions = await database.actions.find(
            query=queries.actions.request_name(value="CreateGroup", operator="=")
        )
        for action_row in create_group_actions:
            if action_row.data.request.name == "CreateGroup":
                result_content = action_row.data.result.content
                if isinstance(result_content, dict):
                    if result_content.get("id") == request.conversation_id:
                        is_group = True
                        # Verify agent is a member of the group
                        group_members = result_content.get("members", [])
                        if agent.id not in group_members:
                            raise ValueError(
                                f"Agent {agent.id} is not a member of group {request.conversation_id}"
                            )
                        break

    if not is_direct_message and not is_group:
        raise ValueError(
            f"Invalid conversation ID: {request.conversation_id}. Must be either a valid contact ID or group ID."
        )

    # Fetch messages for this conversation
    if is_direct_message:
        # For direct messages: get messages sent TO this agent FROM the contact
        # AND messages sent FROM this agent TO the contact
        incoming_query = (
            queries.actions.request_name(value=SendMessageToConversation.get_name(), operator="=")
            & queries.actions.request_parameters(
                path="conversation_id", value=agent.id, operator="="
            )
            & queries.actions.agent_id(value=request.conversation_id, operator="=")
        )
        outgoing_query = (
            queries.actions.request_name(value=SendMessageToConversation.get_name(), operator="=")
            & queries.actions.request_parameters(
                path="conversation_id", value=request.conversation_id, operator="="
            )
            & queries.actions.agent_id(value=agent.id, operator="=")
        )
        message_query = incoming_query | outgoing_query
    else:
        # For groups: get all messages in the group
        message_query = queries.actions.request_name(
            value=SendMessageToConversation.get_name(), operator="="
        ) & queries.actions.request_parameters(
            path="conversation_id", value=request.conversation_id, operator="="
        )

    message_rows = await database.actions.find(query=message_query)

    # Find the oldest unread message index (from others, not self)
    oldest_unread_index = None
    if request.mode == "unread":
        for row in message_rows:
            # Only consider messages from others
            if row.data.agent_id != agent.id:
                if row.index is not None and row.index > last_read_index:
                    if oldest_unread_index is None or row.index < oldest_unread_index:
                        oldest_unread_index = row.index

    for row in message_rows:
        # Apply filtering based on mode
        if request.mode == "unread":
            # Include messages that are:
            # - From others and newer than last_read_index, OR
            # - From self and newer than or equal to the oldest unread message
            is_own_message = row.data.agent_id == agent.id
            if is_own_message:
                # Include own messages only if they're within the unread range
                if (
                    oldest_unread_index is None
                    or row.index is None
                    or row.index < oldest_unread_index
                ):
                    continue
            else:
                # For messages from others, only include if unread
                if row.index is None or row.index <= last_read_index:
                    continue
        # mode == "all" means no filtering by read status

        msg = SendMessageToConversation.model_validate(row.data.request.parameters)
        message = Message(
            id=row.id,
            from_=row.data.agent_id,
            conversation_id=request.conversation_id,
            message=msg.message,
            sent_at=row.created_at,
        )
        messages.append(message)

    # Sort messages by sent_at timestamp
    messages.sort(key=lambda m: m.sent_at)

    # Apply pagination
    if request.offset is not None:
        messages = messages[request.offset :]
    if request.limit is not None:
        messages = messages[: request.limit]

    result = ReadMessagesResponse(messages=messages)
    return ActionExecutionResult(content=result, is_error=False)
