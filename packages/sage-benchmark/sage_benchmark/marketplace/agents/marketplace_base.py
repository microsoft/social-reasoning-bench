"""Base agent class for marketplace negotiation interactions."""

from typing import Any

from openai.types.chat import (
    ChatCompletionAssistantMessageParam,
    ChatCompletionMessageToolCallParam,
    ChatCompletionToolMessageParam,
)
from pydantic_core import to_json
from sage_llm import ModelClient

from sage_benchmark.shared.agent import BaseAgent

from ..environment.actions import GETMESSAGES_TOOL_NAME, MARKETPLACE_TOOLS
from ..types import Tool


class MarketplaceAgent(BaseAgent):
    """Base LLM agent for marketplace negotiation with function/tool calling.

    Extends :class:`BaseAgent` with:
    - System prompt and instruction message setup
    - ``add_turn_marker`` for round-based deadline awareness
    - ``add_new_messages`` for injecting updates via simulated ``GetMessages``
    """

    def __init__(
        self,
        *,
        role: str,
        model: str,
        model_client: ModelClient,
        instruction_message: str,
        explicit_cot: bool = False,
    ) -> None:
        super().__init__(
            model=model,
            model_client=model_client,
            tools=list(MARKETPLACE_TOOLS),
            explicit_cot=explicit_cot,
        )

        self._role = role

        self._messages.extend(
            [
                {
                    "role": "system",
                    "content": (
                        "You are an autonomous negotiation agent in a marketplace simulation. "
                        "Use exactly one tool call per step. Use Wait to yield your turn. "
                        "Use GetMessages to read unread messages/offers. "
                        "Use EndConversation if no deal should be reached."
                    ),
                },
                {"role": "user", "content": instruction_message},
            ]
        )

    # ------------------------------------------------------------------ #
    # Marketplace-specific message helpers
    # ------------------------------------------------------------------ #

    def add_turn_marker(self, *, current_round: int, max_rounds: int) -> None:
        """Inject an explicit turn/round marker to improve deadline awareness."""
        self._messages.append(
            {
                "role": "user",
                "content": (
                    f"Round {current_round} of {max_rounds}. It is your turn as {self._role}. "
                    "Use GetMessages to read unread updates/offers, then act. "
                    "Use Wait to end your turn."
                ),
            }
        )

    def add_new_messages(self, updates: list[Any]) -> None:
        """Inject unread updates by simulating a GetMessages tool call and response."""
        tool_call_id = str(len(self._messages))
        self._messages.append(
            ChatCompletionAssistantMessageParam(
                role="assistant",
                tool_calls=[
                    ChatCompletionMessageToolCallParam(
                        id=tool_call_id,
                        type="function",
                        function={"name": GETMESSAGES_TOOL_NAME, "arguments": "{}"},
                    )
                ],
            )
        )
        self._messages.append(
            ChatCompletionToolMessageParam(
                role="tool",
                tool_call_id=tool_call_id,
                content=to_json(updates).decode(),
            )
        )
