"""Messages formatter using the standard name field."""

from typing import Any

from .base import ConversationFormatter


class MessagesFormatter(ConversationFormatter):
    """Format conversations using the standard 'name' field in user messages."""

    def format(self, messages: list[dict[str, str]]) -> list[dict[str, Any]]:
        """Format messages using the name field.

        Args:
            messages: List of message dicts with user/content fields

        Returns:
            List of user messages with name field set
        """
        formatted = []
        for msg in messages:
            formatted.append({"role": "user", "name": msg["user"], "content": msg["content"]})
        return formatted
