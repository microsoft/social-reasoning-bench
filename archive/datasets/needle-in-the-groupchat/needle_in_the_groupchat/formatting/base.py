"""Base formatter for conversation messages."""

from abc import ABC, abstractmethod
from typing import Any


class ConversationFormatter(ABC):
    """Abstract base class for formatting conversations into messages."""

    @abstractmethod
    def format(self, messages: list[dict[str, str]]) -> list[dict[str, Any]]:
        """Format conversation messages.

        Args:
            messages: List of message dicts with user/content fields

        Returns:
            List of ChatCompletionMessageParams
        """
        pass
