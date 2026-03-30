"""Seller agent for marketplace negotiation."""

from sage_llm import ModelClient

from .marketplace_base import MarketplaceAgent


class SellerAgent(MarketplaceAgent):
    def __init__(
        self,
        *,
        model: str,
        model_client: ModelClient,
        instruction_message: str,
        explicit_cot: bool = False,
    ) -> None:
        super().__init__(
            role="seller",
            model=model,
            model_client=model_client,
            instruction_message=instruction_message,
            explicit_cot=explicit_cot,
        )
