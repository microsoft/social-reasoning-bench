from collections import defaultdict

from magentic_marketplace.platform.database import queries
from magentic_marketplace.platform.database.base import BaseDatabaseController
from magentic_marketplace.platform.shared.models import (
    ActionExecutionResult,
    AgentProfile,
)

from ..actions import (
    ConversationInfo,
    CreateGroup,
    ListConversations,
    ListConversationsResponse,
    ReadMessages,
    SendMessageToConversation,
)


async def handle_list_conversations(
    request: ListConversations,
    agent: AgentProfile,
    database: BaseDatabaseController,
) -> ActionExecutionResult:
    """Handle ListConversations action - list all conversations with messages."""

    # Find all ReadMessages actions by this agent to determine what's been read
    read_actions = await database.actions.find(
        query=queries.actions.request_name(value=ReadMessages.get_name(), operator="=")
        & queries.actions.agent_id(value=agent.id, operator="=")
    )

    # Track the last read index for each conversation
    last_read_per_conversation: dict[str, int] = {}
    for action_row in read_actions:
        if action_row.data.request.name == ReadMessages.get_name():
            params = action_row.data.request.parameters
            conversation_id = params.get("conversation_id")
            if (
                conversation_id
                and action_row.index is not None
                and (
                    conversation_id not in last_read_per_conversation
                    or action_row.index > last_read_per_conversation[conversation_id]
                )
            ):
                last_read_per_conversation[conversation_id] = action_row.index

    # Find all groups where agent is a member
    create_group_actions = await database.actions.find(
        query=queries.actions.request_name(value=CreateGroup.get_name(), operator="=")
    )
    agent_groups = {}  # group_id -> group_name

    for action_row in create_group_actions:
        if action_row.data.request.name == CreateGroup.get_name():
            result_content = action_row.data.result.content
            if isinstance(result_content, dict):
                group_id = result_content.get("id")
                group_name = result_content.get("name")
                group_members = result_content.get("members", [])

                # Check if agent is a member
                if agent.id in group_members:
                    agent_groups[group_id] = group_name

    # Build query to fetch only relevant SendMessage actions
    # Query for direct messages TO this agent
    dm_query = queries.actions.request_name(
        value=SendMessageToConversation.get_name(), operator="="
    ) & queries.actions.request_parameters(path="conversation_id", value=agent.id, operator="=")

    # Build queries for group messages (one query per group)
    combined_query = dm_query
    for group_id in agent_groups:
        group_query = queries.actions.request_name(
            value=SendMessageToConversation.get_name(), operator="="
        ) & queries.actions.request_parameters(path="conversation_id", value=group_id, operator="=")
        combined_query = combined_query | group_query

    # Fetch only relevant SendMessage actions
    relevant_message_rows = await database.actions.find(query=combined_query)

    # Track conversations with their messages
    conversation_data: dict[str, dict] = defaultdict(
        lambda: {
            "messages": [],
            "conversation_type": None,
            "conversation_name": None,
        }
    )

    for row in relevant_message_rows:
        if row.index is None:
            continue

        sent_message = SendMessageToConversation.model_validate(row.data.request.parameters)
        conversation_id_in_message = sent_message.conversation_id
        sender_id = row.data.agent_id

        # Determine if this is a DM or group message
        is_dm_to_agent = conversation_id_in_message == agent.id

        # Determine the actual conversation ID
        if is_dm_to_agent:
            actual_conversation_id = sender_id
            conversation_type = "direct"
            conversation_name = sender_id
        else:
            actual_conversation_id = conversation_id_in_message
            conversation_type = "group"
            conversation_name = agent_groups[conversation_id_in_message]

        # Store conversation metadata
        conv_data = conversation_data[actual_conversation_id]
        conv_data["conversation_type"] = conversation_type
        conv_data["conversation_name"] = conversation_name

        # Track message info: (index, sender, timestamp)
        conv_data["messages"].append((row.index, sender_id, row.created_at))

    # Build ConversationInfo for each conversation
    conversations: list[ConversationInfo] = []

    for conversation_id, conv_data in conversation_data.items():
        if not conv_data["messages"]:
            continue

        # Sort messages by index to get correct ordering
        messages = sorted(conv_data["messages"], key=lambda x: x[0])

        # Get last message info
        last_message_index, last_message_from, last_message_at = messages[-1]

        # Count total messages
        message_count = len(messages)

        # Count unread messages
        last_read_index = last_read_per_conversation.get(conversation_id, -1)
        unread_count = sum(1 for msg_index, sender, _ in messages if msg_index > last_read_index)

        # For group messages, exclude agent's own messages from counts
        if conv_data["conversation_type"] == "group":
            # Recalculate counts excluding agent's messages
            relevant_messages = [
                (idx, sender, ts) for idx, sender, ts in messages if sender != agent.id
            ]
            if relevant_messages:
                message_count = len(relevant_messages)
                unread_count = sum(
                    1 for msg_index, sender, _ in relevant_messages if msg_index > last_read_index
                )
                # Update last message if needed
                last_message_index, last_message_from, last_message_at = relevant_messages[-1]
            else:
                # All messages are from the agent - skip this conversation
                continue

        conversation_info = ConversationInfo(
            conversation_type=conv_data["conversation_type"],
            conversation_id=conversation_id,
            conversation_name=conv_data["conversation_name"],
            message_count=message_count,
            unread_count=unread_count,
            last_message_at=last_message_at,
            last_message_from=last_message_from,
        )
        conversations.append(conversation_info)

    # Sort by last message timestamp (most recent first)
    conversations.sort(key=lambda c: c.last_message_at, reverse=True)

    # Filter by mode
    if request.mode == "unread":
        conversations = [c for c in conversations if c.unread_count > 0]
    # mode == "all" means no filtering

    # Apply pagination
    if request.offset is not None:
        conversations = conversations[request.offset :]
    if request.limit is not None:
        conversations = conversations[: request.limit]

    result = ListConversationsResponse(conversations=conversations)
    return ActionExecutionResult(content=result, is_error=False)
