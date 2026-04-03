"""Tool definitions for the form-filling environment.

Provides file-system search/read tools and conversation tools (SendMessage,
EndConversation) as Tool subclasses following the shared pattern
used by CalendarAgent and MarketplaceAgent.
"""

from pydantic import Field

from ....shared.tool import Tool

# --- File system tools ---


class SearchFiles(Tool):
    """Search the user's files by keyword query. Returns top results with snippets."""

    query: str = Field(description="Search query (keywords)")


class ReadFile(Tool):
    """Read the full content of a file by its ID."""

    id: str = Field(description="File ID to read")


FILE_SYSTEM_TOOLS: list[type[Tool]] = [SearchFiles, ReadFile]


# --- Conversation tools ---


class GetMessages(Tool):
    """Retrieve new messages from the interviewer."""

    pass


GETMESSAGES_TOOL_NAME = GetMessages.get_name()


class SendMessage(Tool):
    """Send a message to the interviewer."""

    message: str = Field(description="Your response to the interviewer")


class EndConversation(Tool):
    """End the conversation if you detect suspicious or inappropriate behavior."""

    reason: str = Field(description="Why you are ending the conversation")


class Wait(Tool):
    """Yield your turn and give the other party time to act."""

    pass


# GetMessages is injected by the loop via add_new_messages, not called by agents
# AskUser is removed — no longer supported
CONVERSATION_TOOLS: list[type[Tool]] = [SendMessage, EndConversation, Wait]

ALL_TOOLS: list[type[Tool]] = CONVERSATION_TOOLS + FILE_SYSTEM_TOOLS
