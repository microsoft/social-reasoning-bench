"""Preference-based conversation generator."""

import random

from openai import OpenAI

from ..formatting import ConversationFormatter
from ..models import (
    Conversation,
    EvaluationMode,
    Message,
    NeedlePosition,
    PreferenceConversation,
)
from ..utils import TokenCounter
from .base import ConversationGenerator


class PreferenceConversationGenerator(ConversationGenerator):
    """Generate conversations with preference statements as needles."""

    def __init__(
        self,
        formatter: ConversationFormatter,
        api_key: str | None = None,
        base_url: str | None = None,
        model: str = "gpt-4.1",
        temperature: float = 0.8,
        token_counter: TokenCounter | None = None,
    ):
        """Initialize the preference generator.

        Args:
            formatter: Formatter for conversation messages (required for token counting)
            api_key: OpenAI API key
            base_url: Custom API base URL
            model: Model name to use for generation
            temperature: Sampling temperature
            token_counter: Optional custom token counter
        """
        super().__init__(formatter=formatter, model=model, token_counter=token_counter)
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.model = model
        self.temperature = temperature

    def _get_query_for_conversation(self, conversation: Conversation) -> str:
        """Get the evaluation query for a preference conversation."""
        if isinstance(conversation, PreferenceConversation):
            return (
                f"Who prefers {conversation.preference}? "
                "Respond with ONLY the person's name, nothing else."
            )
        return super()._get_query_for_conversation(conversation)

    def _generate_topic(self) -> str:
        """Generate a random conversation topic."""
        prompt = """Generate a single casual conversation topic.

Examples: "planning a weekend trip", "discussing restaurants",
"talking about hobbies", "choosing a movie to watch"

Generate one topic (just the topic, no explanation):"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=self.temperature,
            max_tokens=30,
        )

        return (response.choices[0].message.content or "").strip()

    def _generate_preference(self, topic: str) -> tuple[str, str]:
        """Generate a preference loosely related to the topic.

        Args:
            topic: The conversation topic

        Returns:
            Tuple of (preference, category)
        """
        prompt = f"""Given topic "{topic}", generate a casual preference.

The preference should be:
- A single thing (e.g., "pizza", "blue", "hiking", "jazz music")
- Loosely related to the topic (doesn't have to be directly about it)
- Something a person might casually mention

Respond in this format:
Preference: [the preference]
Category: [food/color/activity/music/location/style/hobby/other]

Example:
Topic: "planning a weekend trip"
Preference: hiking
Category: activity"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=self.temperature,
            max_tokens=50,
        )

        content = response.choices[0].message.content or ""

        preference = ""
        category = ""
        for line in content.strip().split("\n"):
            if line.startswith("Preference:"):
                preference = line.split(":", 1)[1].strip()
            elif line.startswith("Category:"):
                category = line.split(":", 1)[1].strip()

        if not preference:
            preference = "pizza"
            category = "food"

        return preference, category

    def _calculate_needle_token_position(self, position: NeedlePosition, max_tokens: int) -> int:
        """Calculate the target token count where needle should be inserted.

        Args:
            position: Position category (early/middle/late)
            max_tokens: Maximum tokens for the conversation

        Returns:
            Target token count for needle insertion
        """
        if position == NeedlePosition.EARLY:
            # First 20%
            return random.randint(0, max_tokens // 5)
        elif position == NeedlePosition.MIDDLE:
            # Middle 20% (40-60%)
            start = max_tokens * 2 // 5
            end = max_tokens * 3 // 5
            return random.randint(start, end)
        else:  # LATE
            # Last 20%
            return random.randint(max_tokens * 4 // 5, max_tokens)

    def _generate_messages_until_limit(
        self,
        users: list,
        max_tokens: int,
        topic: str,
        needle_token_position: int,
        preference: str,
    ) -> tuple[list[Message], int]:
        """Generate conversation messages until token limit with preference injection.

        Args:
            users: List of users in conversation
            max_tokens: Maximum tokens for the conversation
            topic: Conversation topic
            needle_token_position: Target token count for needle insertion
            preference: The preference to inject

        Returns:
            Tuple of (messages, needle_index)
        """
        user_list = ", ".join(u.name for u in users)
        messages = []
        conversation_history = []
        last_speaker = None
        needle_inserted = False
        needle_index = -1

        while True:
            # Pick next speaker (avoid same speaker twice in a row)
            available_speakers = [u.name for u in users if u.name != last_speaker]
            if not available_speakers:
                available_speakers = [u.name for u in users]
            current_speaker = random.choice(available_speakers)

            # Check if this should be the needle turn
            current_tokens = self.count_conversation_tokens(messages) if messages else 0
            is_needle_turn = not needle_inserted and current_tokens >= needle_token_position

            api_messages = []

            system_prompt = (
                f"You are {current_speaker}, one of {len(users)} friends "
                f"({user_list}) in a casual group chat about {topic}.\n"
                f"Generate a short, natural message as "
                f"{current_speaker} would say it.\n"
                "- Keep it casual and friendly\n"
                "- You can use emojis occasionally\n"
                "- Respond naturally to what others said or stay on topic\n"
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

            if is_needle_turn:
                instruction = (
                    f"Continue the conversation about {topic}. "
                    f"**IMPORTANT: Mention that you prefer {preference} "
                    "in this message. Keep it casual and natural.**"
                )
            elif conversation_history:
                instruction = (
                    f"Continue the conversation about {topic}. Keep it natural and conversational."
                )
            else:
                instruction = (
                    f"Start a casual group chat conversation about {topic}. "
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
                    remaining_tokens = max_tokens - current_tokens

                    if remaining_tokens > 10:
                        chars_per_token = len(message_text) / max(1, token_count - current_tokens)
                        clip_length = int(remaining_tokens * chars_per_token * 0.8)
                        if clip_length > 10:
                            clipped_text = message_text[:clip_length]
                            clipped_message = Message(user=current_speaker, content=clipped_text)
                            messages.append(clipped_message)
                            if is_needle_turn:
                                needle_inserted = True
                                needle_index = len(messages) - 1
                break

            messages.append(new_message)
            conversation_history.append({"user": current_speaker, "content": message_text})
            last_speaker = current_speaker

            if is_needle_turn:
                needle_inserted = True
                needle_index = len(messages) - 1

        # If needle wasn't inserted (e.g., very short conversation), insert at end
        if not needle_inserted and messages:
            needle_index = len(messages) - 1

        return messages, needle_index

    def generate_conversation(
        self, num_users: int, max_tokens: int, position: NeedlePosition
    ) -> PreferenceConversation:
        """Generate a complete conversation with a preference needle."""
        users = self.generate_users(num_users)
        topic = self._generate_topic()
        preference, category = self._generate_preference(topic)

        needle_token_position = self._calculate_needle_token_position(position, max_tokens)

        messages, needle_index = self._generate_messages_until_limit(
            users, max_tokens, topic, needle_token_position, preference
        )

        if needle_index >= 0 and needle_index < len(messages):
            needle_user = messages[needle_index].user
            needle_message = messages[needle_index].content
        else:
            needle_user = users[0].name
            needle_message = ""

        # Calculate final token count
        total_tokens = self.count_conversation_tokens(messages)

        rand_id = random.randint(0, 9999)
        conversation_id = (
            f"pref_u{num_users}_k{max_tokens // 1000}k_p{position.value}_{rand_id:04d}"
        )

        return PreferenceConversation(
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
            evaluation_mode=EvaluationMode.PREFERENCE,
            topic=topic,
            preference=preference,
            preference_category=category,
        )
