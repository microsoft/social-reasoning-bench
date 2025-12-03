"""Token counting abstraction for needle-in-the-groupchat."""

from abc import ABC, abstractmethod

import tiktoken


class TokenCounter(ABC):
    """Abstract base class for token counting."""

    @abstractmethod
    def count_tokens(self, messages: list[dict]) -> int:
        """Count tokens in a list of messages.

        Args:
            messages: List of message dicts with role/content/name

        Returns:
            Total token count
        """
        pass

    @abstractmethod
    def encode(self, text: str) -> list[int]:
        """Encode text to tokens.

        Args:
            text: Text to encode

        Returns:
            List of token IDs
        """
        pass


class TiktokenCounter(TokenCounter):
    """Token counter using tiktoken library."""

    def __init__(self, model: str = "gpt-4"):
        """Initialize the tiktoken counter.

        Args:
            model: Model name to use for tokenizer selection
        """
        try:
            self.encoding = tiktoken.encoding_for_model(model)
        except KeyError:
            # Fallback to cl100k_base if model not recognized
            self.encoding = tiktoken.get_encoding("cl100k_base")

    def count_tokens(self, messages: list[dict]) -> int:
        """Count tokens in a list of messages.

        Args:
            messages: List of message dicts with role/content/name

        Returns:
            Total token count
        """
        num_tokens = 0
        for message in messages:
            # Account for message formatting tokens
            num_tokens += 4  # Every message has <im_start>{role/name}\n
            for key, value in message.items():
                if value:
                    num_tokens += len(self.encoding.encode(str(value)))
                if key == "name":
                    num_tokens += -1  # Role is omitted if name is present
        num_tokens += 2  # Every reply is primed with <im_start>assistant
        return num_tokens

    def encode(self, text: str) -> list[int]:
        """Encode text to tokens.

        Args:
            text: Text to encode

        Returns:
            List of token IDs
        """
        return self.encoding.encode(text)
