"""Evaluator for single conversations."""

from openai import OpenAI

from ..formatting import ConversationFormatter
from ..models import Conversation, PreferenceConversation
from ..utils import TiktokenCounter, TokenCounter
from .results import ConversationEvaluation


class ConversationEvaluator:
    """Evaluate a single conversation for needle recall."""

    def __init__(
        self,
        model: str,
        client: OpenAI,
        formatter: ConversationFormatter,
        max_completion_tokens: int = 4000,
        token_counter: TokenCounter | None = None,
    ):
        """Initialize the conversation evaluator.

        Args:
            model: Model name to use for evaluation
            client: OpenAI client instance
            formatter: Formatter for conversation messages
            max_completion_tokens: Maximum tokens for model completion
            token_counter: Optional custom token counter. If not provided,
                           uses TiktokenCounter with the specified model.
        """
        self.model = model
        self.client = client
        self.formatter = formatter
        self.max_completion_tokens = max_completion_tokens
        self.token_counter = token_counter or TiktokenCounter(model=model)

    def count_tokens(self, messages: list[dict]) -> int:
        """Count tokens in a list of already-formatted messages.

        Args:
            messages: List of message dicts with role/content/name (already formatted)

        Returns:
            Total token count
        """
        return self.token_counter.count_tokens(messages)

    def count_conversation_tokens(self, messages: list[dict]) -> int:
        """Count tokens in conversation messages using the formatter.

        Args:
            messages: List of message dicts with user/content fields

        Returns:
            Total token count after formatting
        """
        formatted = self.formatter.format(messages)
        return self.token_counter.count_tokens(formatted)

    def evaluate(
        self, conversation: Conversation | PreferenceConversation
    ) -> ConversationEvaluation:
        """Evaluate model on a single conversation.

        Routes to appropriate evaluation method based on conversation type.

        Args:
            conversation: Conversation to evaluate

        Returns:
            ConversationEvaluation with results
        """
        if isinstance(conversation, PreferenceConversation):
            return self._evaluate_preference(conversation)
        return self._evaluate_exact_match(conversation)

    def _evaluate_exact_match(self, conversation: Conversation) -> ConversationEvaluation:
        """Evaluate model on exact-match conversation.

        Args:
            conversation: Conversation to evaluate

        Returns:
            ConversationEvaluation with results
        """
        try:
            # Format conversation messages using the formatter
            conversation_msgs = [
                {"user": msg.user, "content": msg.content} for msg in conversation.messages
            ]
            messages = self.formatter.format(conversation_msgs)

            # Add query message asking who said the needle
            query = (
                f'Who said: "{conversation.needle_message}"? '
                "Respond with ONLY the person's name, nothing else."
            )
            messages.append({"role": "user", "content": query})

            # Get model response
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,  # type: ignore[arg-type]
                temperature=0.0,
                max_tokens=self.max_completion_tokens,
            )

            model_response = response.choices[0].message.content or ""

            # Treat empty responses as exceptions (excluded from accuracy)
            if not model_response.strip():
                return ConversationEvaluation(
                    conversation_id=conversation.id,
                    num_users=conversation.num_users,
                    max_tokens=conversation.max_tokens,
                    needle_position=conversation.needle_position,
                    needle_user=conversation.needle_user,
                    needle_message=conversation.needle_message,
                    predicted_user=None,
                    correct=False,
                    model_response=model_response,
                    error="empty_response",
                )

            predicted_user = model_response.strip()

            # Check if correct (exact match or substring match)
            correct = (
                predicted_user.lower() == conversation.needle_user.lower()
                or conversation.needle_user.lower() in predicted_user.lower()
            )

            return ConversationEvaluation(
                conversation_id=conversation.id,
                num_users=conversation.num_users,
                max_tokens=conversation.max_tokens,
                needle_position=conversation.needle_position,
                needle_user=conversation.needle_user,
                needle_message=conversation.needle_message,
                predicted_user=predicted_user,
                correct=correct,
                model_response=model_response,
                error=None,
            )

        except Exception as e:
            return ConversationEvaluation(
                conversation_id=conversation.id,
                num_users=conversation.num_users,
                max_tokens=conversation.max_tokens,
                needle_position=conversation.needle_position,
                needle_user=conversation.needle_user,
                needle_message=conversation.needle_message,
                predicted_user=None,
                correct=False,
                model_response="",
                error=str(e),
            )

    def _evaluate_preference(self, conversation: PreferenceConversation) -> ConversationEvaluation:
        """Evaluate model on a preference-based conversation.

        Args:
            conversation: PreferenceConversation to evaluate

        Returns:
            ConversationEvaluation with preference-based evaluation
        """
        try:
            # Format conversation messages using the formatter
            conversation_msgs = [
                {"user": msg.user, "content": msg.content} for msg in conversation.messages
            ]
            messages = self.formatter.format(conversation_msgs)

            # Add query asking who prefers the preference (no name mentioned)
            query = (
                f"Who prefers {conversation.preference}? "
                "Respond with ONLY the person's name, nothing else."
            )
            messages.append({"role": "user", "content": query})

            # Get model response
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,  # type: ignore[arg-type]
                max_tokens=self.max_completion_tokens,
            )

            model_response = response.choices[0].message.content or ""

            # Treat empty responses as exceptions (excluded from accuracy)
            if not model_response.strip():
                return ConversationEvaluation(
                    conversation_id=conversation.id,
                    num_users=conversation.num_users,
                    max_tokens=conversation.max_tokens,
                    needle_position=conversation.needle_position,
                    needle_user=conversation.needle_user,
                    needle_message=conversation.needle_message,
                    predicted_user=None,
                    correct=False,
                    model_response=model_response,
                    error="empty_response",
                )

            predicted_user = model_response.strip()

            # Check if correct (exact match or substring match)
            correct = (
                predicted_user.lower() == conversation.needle_user.lower()
                or conversation.needle_user.lower() in predicted_user.lower()
            )

            return ConversationEvaluation(
                conversation_id=conversation.id,
                num_users=conversation.num_users,
                max_tokens=conversation.max_tokens,
                needle_position=conversation.needle_position,
                needle_user=conversation.needle_user,
                needle_message=conversation.needle_message,
                predicted_user=predicted_user,
                correct=correct,
                model_response=model_response,
                error=None,
            )

        except Exception as e:
            return ConversationEvaluation(
                conversation_id=conversation.id,
                num_users=conversation.num_users,
                max_tokens=conversation.max_tokens,
                needle_position=conversation.needle_position,
                needle_user=conversation.needle_user,
                needle_message=conversation.needle_message,
                predicted_user=None,
                correct=False,
                model_response="",
                error=str(e),
            )
