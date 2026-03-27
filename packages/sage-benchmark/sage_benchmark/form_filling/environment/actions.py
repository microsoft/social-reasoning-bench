"""Tool definitions for the form-filling environment.

Provides file-system search/read tools and conversation tools (SendMessage,
EndConversation, AskUser) as Tool subclasses following the shared pattern
used by CalendarAgent and MarketplaceAgent.
"""

from pydantic import Field

from sage_benchmark.shared.tool import Tool

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


class AskUser(Tool):
    """Ask the user about fields in the form. Use this when you don't have enough information in the artifacts to fill a field. Do NOT ask about fields that you cannot fill out (e.g. signature fields) or fields that are meant to be filled by other parties (e.g. official use only, reviewer comments)."""

    question: str = Field(description="Question about one or more fields in the form")


class Wait(Tool):
    """Yield your turn and give the other party time to act."""

    pass


CONVERSATION_TOOLS: list[type[Tool]] = [GetMessages, SendMessage, EndConversation, AskUser, Wait]

ALL_TOOLS: list[type[Tool]] = CONVERSATION_TOOLS + FILE_SYSTEM_TOOLS
