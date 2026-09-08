"""Buyer agent for marketplace negotiation."""

from srbench_llm import SRBenchModelClient

from ....shared.agent import BaseAssistantAgent
from ..types import MarketplaceBuyerTask
from .marketplace_base import MarketplaceAgent


class BuyerAgent(MarketplaceAgent, BaseAssistantAgent[MarketplaceBuyerTask]):
    """Built-in buyer agent, the assistant side of the negotiation."""

    def __init__(
        self,
        *,
        model: str,
        model_client: SRBenchModelClient,
        task: MarketplaceBuyerTask,
        explicit_cot: bool = False,
        system_prompt: str | None = None,
        malicious_prompt: str | None = None,
    ) -> None:
        super().__init__(
            role="buyer",
            model=model,
            model_client=model_client,
            instruction_message=task.instruction_message,
            explicit_cot=explicit_cot,
            system_prompt=system_prompt,
            malicious_prompt=malicious_prompt,
            max_actions=task.max_actions,
        )
