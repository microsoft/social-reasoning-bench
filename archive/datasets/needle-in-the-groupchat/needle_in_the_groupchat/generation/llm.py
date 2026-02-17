"""LLM-based conversation generator."""

import random

from openai import OpenAI

from ..formatting import ConversationFormatter
from ..models import Conversation, Message, NeedlePosition
from ..utils import TokenCounter
from .base import ConversationGenerator


class LLMConversationGenerator(ConversationGenerator):
    """Generate synthetic group conversations using an LLM."""

    def __init__(
        self,
        formatter: ConversationFormatter,
        api_key: str | None = None,
        base_url: str | None = None,
        model: str = "gpt-4.1",
        temperature: float = 0.8,
        buffer: int = 0,
        token_counter: TokenCounter | None = None,
    ):
        """Initialize the generator with OpenAI client.

        Args:
            formatter: Formatter for conversation messages (required for token counting)
            api_key: OpenAI API key
            base_url: Custom API base URL
            model: Model name to use for generation
            temperature: Sampling temperature
            buffer: Chars to add around needle (0 = entire message)
            token_counter: Optional custom token counter
        """
        super().__init__(formatter=formatter, model=model, token_counter=token_counter)
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.model = model
        self.temperature = temperature
        self.buffer = buffer

    def _generate_messages_until_limit(self, users: list, max_tokens: int) -> list[Message]:
        """Generate realistic conversation until token limit is reached."""
        user_list = ", ".join(u.name for u in users)
        messages = []
        conversation_history = []
        last_speaker = None

        while True:
            # Pick next speaker (avoid same speaker twice in a row)
            available_speakers = [u.name for u in users if u.name != last_speaker]
            if not available_speakers:
                available_speakers = [u.name for u in users]
            current_speaker = random.choice(available_speakers)

            api_messages = []

            num_users = len(users)
            system_prompt = (
                f"You are {current_speaker}, one of {num_users} "
                f"friends ({user_list}).\n"
                f"Generate a short, natural message as {current_speaker} "
                "would say it.\n"
                "- Keep it casual and friendly\n"
                "- You can use emojis occasionally\n"
                "- Respond naturally to what others said or introduce a topic\n"
                "- Output ONLY the message text, no name prefix or labels"
            )

            api_messages.append({"role": "system", "content": system_prompt})

            for msg in conversation_history[-10:]:
                api_messages.append(
                    {
                        "role": "user",
                        "name": msg["user"],
                        "content": msg["content"],
                    }
                )

            if conversation_history:
                instruction = (
                    "Generate the next message in this casual group chat. "
                    "Keep it natural and conversational."
                )
            else:
                instruction = (
                    "Start a casual group chat conversation. "
                    "Generate the first message (a greeting or opening)."
                )

            api_messages.append({"role": "user", "content": instruction})

            response = self.client.chat.completions.create(
                model=self.model,
                messages=api_messages,
                temperature=self.temperature,
                max_tokens=100,
            )

            message_text = (response.choices[0].message.content or "").strip()

            for name in [u.name for u in users]:
                if message_text.startswith(f"{name}:"):
                    message_text = message_text[len(name) + 1 :].strip()

            if not message_text:
                continue

            new_message = Message(user=current_speaker, content=message_text)

            # Check if adding this message exceeds limit
            candidate_messages = messages + [new_message]
            token_count = self.count_conversation_tokens(candidate_messages)

            if token_count > max_tokens:
                # Try to clip the message to fit
                if messages:
                    current_tokens = self.count_conversation_tokens(messages)
                    remaining_tokens = max_tokens - current_tokens

                    if remaining_tokens > 10:
                        # Estimate chars per token and clip
                        chars_per_token = len(message_text) / max(1, token_count - current_tokens)
                        clip_length = int(remaining_tokens * chars_per_token * 0.8)
                        if clip_length > 10:
                            clipped_text = message_text[:clip_length]
                            clipped_message = Message(user=current_speaker, content=clipped_text)
                            messages.append(clipped_message)
                break

            messages.append(new_message)
            conversation_history.append({"user": current_speaker, "content": message_text})
            last_speaker = current_speaker

        return messages

    def _generate_buffer_text(self, length: int) -> str:
        """Generate buffer text to surround the needle.

        Args:
            length: Number of characters to generate

        Returns:
            Generated buffer text
        """
        if length <= 0:
            return ""

        prompt = (
            f"Generate approximately {length} characters of casual, "
            "natural conversational text. Just text, no formatting."
        )

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=self.temperature,
            max_tokens=max(50, length // 2),
        )

        return (response.choices[0].message.content or "").strip()

    def _create_needle_message(self) -> str:
        """Create a distinctive needle message."""
        needles = [
            "I just found out that penguins have knees!",
            "My neighbor's cat learned to open the refrigerator door.",
            "I accidentally put my phone in the freezer last night.",
            "There's a statue made entirely of cheese in Wisconsin.",
            "I once met someone who had never tried chocolate.",
            "My grandfather claims he invented the high-five.",
            "I can whistle with my eyes closed, which is apparently rare.",
            "I found a pearl in my oyster at dinner last week!",
            "My plants grow better when I play them jazz music.",
            "I've been learning to juggle chainsaws (foam ones, don't worry!).",
        ]
        return random.choice(needles)

    def generate_conversation(
        self, num_users: int, max_tokens: int, position: NeedlePosition
    ) -> Conversation:
        """Generate a complete conversation with needle."""
        users = self.generate_users(num_users)
        messages = self._generate_messages_until_limit(users, max_tokens)

        needle_message = self._create_needle_message()
        needle_user = random.choice(users).name

        # Use buffer generator if buffer is set
        buffer_gen = self._generate_buffer_text if self.buffer > 0 else None

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
