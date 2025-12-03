"""Prefix formatter that includes user name in message content."""

from typing import Any

from .base import ConversationFormatter


class PrefixFormatter(ConversationFormatter):
    """Format conversations with user name as content prefix."""

    def format(self, messages: list[dict[str, str]]) -> list[dict[str, Any]]:
        """Format messages with user name prefixed to content.

        Args:
            messages: List of message dicts with user/content fields

        Returns:
            List of user messages with name prefixed to content
        """
        formatted = []
        for msg in messages:
            formatted.append({"role": "user", "content": f"{msg['user']}: {msg['content']}"})
        return formatted
