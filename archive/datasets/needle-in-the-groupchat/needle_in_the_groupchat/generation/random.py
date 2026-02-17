"""Random string conversation generator (no LLM needed)."""

import random
import string

from ..formatting import ConversationFormatter
from ..models import Conversation, Message, NeedlePosition
from ..utils import TokenCounter
from .base import ConversationGenerator


class RandomConversationGenerator(ConversationGenerator):
    """Generate synthetic conversations using random strings (no LLM needed)."""

    def __init__(
        self,
        formatter: ConversationFormatter,
        message_length: int = 50,
        seed: int | None = None,
        buffer: int = 0,
        token_counter: TokenCounter | None = None,
    ):
        """Initialize the random string generator.

        Args:
            formatter: Formatter for conversation messages (required for token counting)
            message_length: Average length of generated messages
            seed: Random seed for reproducibility
            buffer: Chars to add around needle (0 = entire message)
            token_counter: Optional custom token counter
        """
        super().__init__(formatter=formatter, token_counter=token_counter)
        if seed is not None:
            random.seed(seed)
        self.message_length = message_length
        self.buffer = buffer

    def _generate_random_string(self, length: int | None = None) -> str:
        """Generate a random string of characters.

        Args:
            length: Length of string to generate. If None, uses random length
                    around message_length.

        Returns:
            Generated random string
        """
        if length is None:
            length = random.randint(self.message_length // 2, self.message_length * 2)

        chars = string.ascii_letters + string.digits + " " * 5
        return "".join(random.choice(chars) for _ in range(length))

    def _generate_messages_until_limit(self, users: list, max_tokens: int) -> list[Message]:
        """Generate random messages until token limit is reached.

        Args:
            users: List of users in conversation
            max_tokens: Maximum tokens for the conversation

        Returns:
            List of messages within token limit
        """
        messages = []
        last_speaker = None

        while True:
            # Pick next speaker (avoid same speaker twice in a row)
            available_speakers = [u.name for u in users if u.name != last_speaker]
            if not available_speakers:
                available_speakers = [u.name for u in users]
            next_speaker = random.choice(available_speakers)

            # Generate and add message
            message_text = self._generate_random_string()
            messages.append(Message(user=next_speaker, content=message_text))
            last_speaker = next_speaker

            # If we exceeded the limit, drop the last message and stop
            if self.count_conversation_tokens(messages) > max_tokens:
                messages.pop()
                break

        return messages

    def _create_needle_message(self) -> str:
        """Create a distinctive needle message (random string)."""
        return self._generate_random_string(self.message_length)

    def generate_conversation(
        self, num_users: int, max_tokens: int, position: NeedlePosition
    ) -> Conversation:
        """Generate a complete conversation with needle."""
        users = self.generate_users(num_users)
        messages = self._generate_messages_until_limit(users, max_tokens)

        needle_message = self._create_needle_message()
        needle_user = random.choice(users).name

        # Use buffer generator if buffer is set
        buffer_gen = self._generate_random_string if self.buffer > 0 else None

        messages, needle_index = self.insert_needle(
            messages,
            needle_message,
            needle_user,
            position,
            buffer_generator=buffer_gen,
            buffer_size=self.buffer,
        )

        # Calculate final token count
        total_tokens = self.count_conversation_tokens(messages)

        rand_suffix = random.randint(0, 9999)
        conversation_id = f"u{num_users}_k{max_tokens // 1000}k_p{position.value}_{rand_suffix:04d}"

        return Conversation(
            id=conversation_id,
            users=users,
            messages=messages,
            needle_message=needle_message,
            needle_user=needle_user,
            needle_position=position,
            needle_index=needle_index,
            num_users=num_users,
            max_tokens=max_tokens,
            total_messages=len(messages),
            total_tokens=total_tokens,
        )
