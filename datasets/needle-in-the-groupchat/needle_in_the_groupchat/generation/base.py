"""Base class for conversation generators."""

import json
import random
from abc import ABC, abstractmethod
from collections.abc import Callable
from pathlib import Path

from ..formatting import ConversationFormatter
from ..models import Conversation, Message, NeedlePosition, User
from ..utils import TiktokenCounter, TokenCounter


class ConversationGenerator(ABC):
    """Abstract base class for conversation generators."""

    def __init__(
        self,
        formatter: ConversationFormatter,
        model: str = "gpt-4.1",
        token_counter: TokenCounter | None = None,
    ):
        """Initialize the generator.

        Args:
            formatter: Formatter for conversation messages (required for token counting)
            model: Model name (used for tokenizer selection if no counter provided)
            token_counter: Optional custom token counter. If not provided,
                           uses TiktokenCounter with the specified model.
        """
        self.formatter = formatter
        self.token_counter = token_counter or TiktokenCounter(model=model)

    def count_tokens(self, messages: list[dict]) -> int:
        """Count tokens in a list of already-formatted messages.

        Args:
            messages: List of message dicts with role/content/name (already formatted)

        Returns:
            Total token count
        """
        return self.token_counter.count_tokens(messages)

    def count_conversation_tokens(self, messages: list[Message]) -> int:
        """Count tokens in a list of Message objects using the formatter.

        Args:
            messages: List of Message objects

        Returns:
            Total token count after formatting
        """
        # Convert to dict format expected by formatter
        msg_dicts = [{"user": msg.user, "content": msg.content} for msg in messages]
        # Format using the formatter
        formatted = self.formatter.format(msg_dicts)
        # Count tokens
        return self.token_counter.count_tokens(formatted)

    def generate_users(self, num_users: int) -> list[User]:
        """Generate diverse user personas.

        Args:
            num_users: Number of users to generate

        Returns:
            List of User instances
        """
        base_names = [
            "Alice",
            "Bob",
            "Charlie",
            "Diana",
            "Eve",
            "Frank",
            "Grace",
            "Henry",
            "Iris",
            "Jack",
        ]

        users = []
        for i in range(num_users):
            if i < len(base_names):
                # Use base names for first 10 users
                users.append(User(name=base_names[i]))
            else:
                # Generate numbered names for additional users
                users.append(User(name=f"User{i + 1}"))

        return users

    def insert_needle(
        self,
        messages: list[Message],
        needle_message: str,
        needle_user: str,
        position: NeedlePosition,
        buffer_generator: Callable[[int], str] | None = None,
        buffer_size: int = 0,
    ) -> tuple[list[Message], int]:
        """Insert needle message at specified position.

        Args:
            messages: List of messages to insert into
            needle_message: The needle message content
            needle_user: User who will send the needle
            position: Position category (early/middle/late)
            buffer_generator: Optional function to generate buffer text
            buffer_size: Size of buffer to add around needle

        Returns:
            Tuple of (modified messages list, needle index)
        """
        total = len(messages)

        # Create the full needle content (with buffer if specified)
        if buffer_size > 0 and buffer_generator:
            prefix = buffer_generator(buffer_size)
            suffix = buffer_generator(buffer_size)
            full_content = f"{prefix} {needle_message} {suffix}".strip()
        else:
            full_content = needle_message

        # Handle edge cases for very small conversations
        if total == 0:
            needle = Message(user=needle_user, content=full_content)
            messages.append(needle)
            return messages, 0

        if total == 1:
            needle = Message(user=needle_user, content=full_content)
            if position == NeedlePosition.EARLY:
                messages.insert(0, needle)
                return messages, 0
            else:
                messages.append(needle)
                return messages, 1

        # For larger conversations, use percentage-based positioning
        if position == NeedlePosition.EARLY:
            # First 20%
            end_idx = max(1, total // 5)
            index = random.randint(0, end_idx)
        elif position == NeedlePosition.MIDDLE:
            # Middle 20% (40-60%)
            start = max(0, total * 2 // 5)
            end = min(total - 1, total * 3 // 5)
            # Ensure start <= end
            if start > end:
                start, end = 0, total - 1
            index = random.randint(start, end)
        else:  # LATE
            # Last 20%
            start_idx = max(0, total * 4 // 5)
            index = random.randint(start_idx, total - 1)

        needle = Message(user=needle_user, content=full_content)
        messages.insert(index, needle)

        return messages, index

    @abstractmethod
    def generate_conversation(
        self, num_users: int, max_tokens: int, position: NeedlePosition
    ) -> Conversation:
        """Generate a complete conversation with needle.

        Args:
            num_users: Number of users in conversation
            max_tokens: Maximum tokens for the conversation
            position: Position of needle (early/middle/late)

        Returns:
            Generated Conversation
        """
        pass

    def _get_query_for_conversation(self, conversation: Conversation) -> str:
        """Get the evaluation query for a conversation.

        Override this method for different conversation types.

        Args:
            conversation: The conversation to get query for

        Returns:
            Query string
        """
        return (
            f'Who said: "{conversation.needle_message}"? '
            "Respond with ONLY the person's name, nothing else."
        )

    def generate_dataset(
        self,
        output_dir: str,
        num_users_range: list[int],
        max_tokens_range: list[int],
    ) -> list[Conversation]:
        """Generate full evaluation dataset.

        Args:
            output_dir: Directory to save conversations
            num_users_range: List of user counts to generate
            max_tokens_range: List of max token counts to generate

        Returns:
            List of generated conversations
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        conversations = []
        positions = [NeedlePosition.EARLY, NeedlePosition.MIDDLE, NeedlePosition.LATE]

        total = len(num_users_range) * len(max_tokens_range) * len(positions)
        print(f"Generating {total} conversations...")

        count = 0
        for num_users in num_users_range:
            for max_tokens in max_tokens_range:
                for position in positions:
                    count += 1

                    conv = self.generate_conversation(num_users, max_tokens, position)
                    conversations.append(conv)

                    print(
                        f"[{count}/{total}] Generated: {num_users} users, "
                        f"{conv.total_messages} messages, {position.value} position, "
                        f"tokens: {conv.total_tokens:,}/{max_tokens:,}"
                    )

                    # Save individual conversation
                    conv_file = output_path / f"{conv.id}.json"
                    with open(conv_file, "w") as f:
                        json.dump(conv.model_dump(), f, indent=2)

        print(f"Generated {len(conversations)} conversations in {output_dir}")
        return conversations
