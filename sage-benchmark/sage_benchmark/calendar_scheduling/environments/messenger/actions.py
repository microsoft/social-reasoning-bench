from ...types import Tool


class SendMessage(Tool):
    """Send a message to a contact."""

    to: str
    message: str


class GetUnreadMessages(Tool):
    """Get unread messages."""

    pass
