from dataclasses import dataclass, field

from ..types import ActionTrace, FinalOutcome, MessageRecord, OfferRecord


@dataclass
class MarketplaceState:
    messages: list[MessageRecord] = field(default_factory=list)
    offers: list[OfferRecord] = field(default_factory=list)
    action_trace: list[ActionTrace] = field(default_factory=list)
    next_offer_id: int = 1
    outcome: FinalOutcome = field(default_factory=lambda: FinalOutcome(deal_reached=False))
    # Legacy round counter, kept for back-compat (always 0 in the agent-driven
    # design). action_count is the monotonic action index assigned by the env.
    current_round: int = 0
    action_count: int = 0

    def get_offer(self, offer_id: int) -> OfferRecord | None:
        for offer in self.offers:
            if offer.id == offer_id:
                return offer
        return None

    def expire_offers_from(self, proposer: str) -> None:
        """Expire all OPEN offers made by *proposer* (superseded by a new offer).

        Args:
            proposer: The role (``"buyer"`` or ``"seller"``) whose open offers
                should be marked as ``"EXPIRED"``.
        """
        for offer in self.offers:
            if offer.status == "OPEN" and offer.proposer == proposer:
                offer.status = "EXPIRED"
