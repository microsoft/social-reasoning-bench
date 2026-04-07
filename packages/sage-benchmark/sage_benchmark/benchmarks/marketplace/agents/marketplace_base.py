"""Base agent class for marketplace negotiation interactions."""

from typing import Any

from openai.types.chat.chat_completion_message_tool_call import (
    ChatCompletionMessageToolCall,
    Function,
)
from pydantic_core import to_json
from sage_llm import SageChatCompletionMessage, SageMessage, SageModelClient

from ....shared.agent import BaseAgent
from ..environment.actions import GETMESSAGES_TOOL_NAME, MARKETPLACE_TOOLS
from ..prompts.system import (
    MKT_ROLE,
    PRESETS,
    get_system_prompt,
    list_available_presets,
)
from ..types import Tool

# Re-export for backwards compatibility
__all__ = [
    "MarketplaceAgent",
    "MKT_ROLE",
    "PRESETS",
    "get_system_prompt",
    "list_available_presets",
]


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
        model_client: SageModelClient,
        instruction_message: str,
        explicit_cot: bool = False,
        system_prompt: str | None = None,
        malicious_prompt: str | None = None,
    ) -> None:
        super().__init__(
            model=model,
            model_client=model_client,
            tools=list(MARKETPLACE_TOOLS),
            explicit_cot=explicit_cot,
            prompt_label=f"mkt_{role}",
        )

        self._role = role

        # Use provided system prompt or fall back to MKT_ROLE
        effective_prompt = system_prompt if system_prompt is not None else MKT_ROLE
        if malicious_prompt:
            effective_prompt += "\n\n" + malicious_prompt

        self._messages.extend(
            [
                {"role": "system", "content": effective_prompt},
                {"role": "user", "content": instruction_message},
            ]
        )

    # ------------------------------------------------------------------ #
    # Marketplace-specific message helpers
    # ------------------------------------------------------------------ #

    def add_turn_marker(self, *, current_round: int, max_rounds: int) -> None:
        """Inject an explicit turn/round marker to improve deadline awareness.

        Args:
            current_round: The current round number in the negotiation.
            max_rounds: The maximum number of rounds allowed.
        """
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
        """Inject unread updates by simulating a GetMessages tool call and response.

        Args:
            updates: List of unread update dicts (messages and offers) to inject
                into the conversation as a simulated GetMessages result.
        """
        tool_call_id = str(len(self._messages))
        self._messages.append(
            SageChatCompletionMessage(
                role="assistant",
                tool_calls=[
                    ChatCompletionMessageToolCall(
                        id=tool_call_id,
                        type="function",
                        function=Function(name=GETMESSAGES_TOOL_NAME, arguments="{}"),
                    )
                ],
            )
        )
        self._messages.append(
            {
                "role": "tool",
                "tool_call_id": tool_call_id,
                "content": to_json(updates).decode(),
            }
        )
