"""Base agent class for marketplace negotiation interactions."""

from srbench_llm import SRBenchModelClient

from ....shared.agent import LLMAgent
from ..prompts.system import (
    MKT_ROLE,
    PRESETS,
    get_system_prompt,
    list_available_presets,
)

# Re-export for backwards compatibility
__all__ = [
    "MarketplaceAgent",
    "MKT_ROLE",
    "PRESETS",
    "get_system_prompt",
    "list_available_presets",
]


class MarketplaceAgent(LLMAgent):
    """Base LLM agent for marketplace negotiation with function/tool calling.

    Extends :class:`LLMAgent` with:
    - System prompt and instruction message setup
    - ``add_turn_marker`` for round-based deadline awareness
    """

    def __init__(
        self,
        *,
        role: str,
        model: str,
        model_client: SRBenchModelClient,
        instruction_message: str,
        explicit_cot: bool = False,
        system_prompt: str | None = None,
        malicious_prompt: str | None = None,
        max_actions: int = 50,
    ) -> None:
        super().__init__(
            model=model,
            model_client=model_client,
            explicit_cot=explicit_cot,
            prompt_label=f"mkt_{role}",
            max_actions=max_actions,
        )

        self._role = role
        if malicious_prompt:
            self._init_malicious(malicious_prompt)
        else:
            self._init_benign(system_prompt=system_prompt, instruction_message=instruction_message)

    def _init_benign(self, system_prompt: str | None, instruction_message: str):
        # Use provided system prompt or fall back to MKT_ROLE
        effective_system_prompt = system_prompt.strip() if system_prompt else MKT_ROLE

        self._messages.extend(
            [
                {"role": "system", "content": effective_system_prompt},
                {"role": "user", "content": instruction_message.strip()},
            ]
        )

    def _init_malicious(self, malicious_prompt: str):
        self._messages.append({"role": "system", "content": malicious_prompt.strip()})

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
