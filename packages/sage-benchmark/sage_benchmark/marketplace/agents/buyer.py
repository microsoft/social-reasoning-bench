"""Buyer agent for marketplace negotiation."""

from sage_llm import ModelClient

from .marketplace_base import MarketplaceAgent


class BuyerAgent(MarketplaceAgent):
    def __init__(self, *, model: str, model_client: ModelClient, instruction_message: str) -> None:
        super().__init__(
            role="buyer",
            model=model,
            model_client=model_client,
            instruction_message=instruction_message,
        )
