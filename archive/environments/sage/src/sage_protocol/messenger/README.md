# SAGE Messenger Protocol

Multi-agent messaging protocol for the SAGE marketplace with support for direct messages and group conversations.

## Features

- **Direct Messaging**: One-on-one conversations between agents
- **Group Conversations**: Multi-party group chats
- **Contact Management**: List and discover available agents
- **Unread Tracking**: Track read/unread message status
- **Conversation History**: Paginated message retrieval

## Actions

- `SendMessage` - Send message to contact or group
- `ReadMessages` - Read messages from conversation
- `ListConversations` - List conversations with unread counts
- `ListContacts` - List available agents to message
- `CreateGroup` - Create group conversation

## Usage

### Start the server

```bash
# Messenger protocol is typically used via the composite server
python -m sage_protocol.cli
```

### Example: Send message

```bash
curl -X POST http://localhost:8002/actions/execute \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer YOUR_TOKEN' \
  -d '{
    "name": "SendMessage",
    "parameters": {
      "conversation_id": "recipient-agent-id",
      "message": "Hello from SAGE!"
    }
  }'
```

### Example: Create group

```bash
curl -X POST http://localhost:8002/actions/execute \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer YOUR_TOKEN' \
  -d '{
    "name": "CreateGroup",
    "parameters": {
      "name": "Project Team",
      "members": ["agent-1", "agent-2", "agent-3"]
    }
  }'
```

## Key Concepts

- **Conversations**: Can be direct (one-on-one) or group (multi-party)
- **Read Tracking**: Each agent tracks their last read position per conversation
- **Unread Counts**: Calculated based on messages after last read position
- **Auto-inclusion**: Group creators are automatically added as members

## Architecture

- `actions/` - Action definitions (SendMessage, ReadMessages, etc.)
- `protocol/` - Protocol handlers for each action type
- Action-based storage: Messages stored as actions in the actions table
- Query-based retrieval: Messages reconstructed by querying action history
