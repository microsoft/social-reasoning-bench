from dataclasses import dataclass, field

from ..types import FinalOutcome, MessageRecord, OfferRecord


@dataclass
class MarketplaceState:
    messages: list[MessageRecord] = field(default_factory=list)
    offers: list[OfferRecord] = field(default_factory=list)
    next_offer_id: int = 1
    outcome: FinalOutcome = field(default_factory=lambda: FinalOutcome(deal_reached=False))
    current_round: int = 1

    def get_offer(self, offer_id: int) -> OfferRecord | None:
        for offer in self.offers:
            if offer.id == offer_id:
                return offer
        return None

    def expire_end_of_round_offers(self, round_number: int) -> None:
        for offer in self.offers:
            if offer.status == "OPEN" and offer.round_created <= round_number:
                offer.status = "EXPIRED"
