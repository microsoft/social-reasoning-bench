"""Buyer agent for marketplace negotiation."""

from srbench_llm import SRBenchModelClient

from ..environment.actions import EndConversation
from .marketplace_base import MarketplaceAgent


class BuyerAgent(MarketplaceAgent):
    def __init__(
        self,
        *,
        model: str,
        model_client: SRBenchModelClient,
        instruction_message: str,
        explicit_cot: bool = False,
        system_prompt: str | None = None,
        malicious_prompt: str | None = None,
    ) -> None:
        super().__init__(
            role="buyer",
            model=model,
            model_client=model_client,
            instruction_message=instruction_message,
            # Buyer can end the conversation
            additional_tools=[EndConversation],
            explicit_cot=explicit_cot,
            system_prompt=system_prompt,
            malicious_prompt=malicious_prompt,
        )
