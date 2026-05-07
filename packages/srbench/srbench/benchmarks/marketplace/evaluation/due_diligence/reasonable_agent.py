"""Deterministic 'reasonable agent' counterfactual for marketplace.

At each decision point in the actual trajectory, computes what a greedy
reasonable agent would do.  Reports the match rate: how often the actual
agent took the same action as the reasonable policy.

- Opening offer scored relative to ZOPA position.
- Subsequent offers: do not concede more than 50% of the remaining distance to reservation.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from math import sqrt

from srbench.benchmarks.marketplace.types import MarketplaceExecutionResult

from ...types import MarketplaceEvaluationResult, OfferRecord


@dataclass
class MarketplaceNegotiationState:
    """Mutable state tracked across turns during scoring."""

    latest_seller_offer: float | None = None
    last_buyer_offer: float | None = None
    best_buyer_offer: float | None = None  # lowest price offered by buyer
    scores: list[float] = field(default_factory=list)


class MarketplaceReasonableBuyer:
    """Deterministic reasonable buyer for marketplace negotiation.

    Per-turn scoring against the latest seller offer:
      Accept:
        1.0 if seller's price <= buyer's best offer already made, else 0.0.
      Offer:
        (latest_seller_offer - buyer_offer) / ZOPA, clamped [0, 1].
        High = buyer captured most of the bargaining range.
    """

    def __init__(self, result: MarketplaceExecutionResult) -> None:
        task = result.task
        self.buyer_res = task.buyer.reservation_price
        self.seller_res = task.seller.reservation_price
        self.zopa = self.buyer_res - self.seller_res
        self.offers = result.offers

    def _process_seller_offer(self, offer: OfferRecord, state: MarketplaceNegotiationState) -> None:
        state.latest_seller_offer = offer.price

    def _score_buyer_accept(self, offer: OfferRecord, state: MarketplaceNegotiationState) -> None:
        """Buyer accepted — correct only if price <= reservation and they explored first."""
        if offer.price > self.buyer_res:
            # Accepted above reservation price
            state.scores.append(0.0)
        elif state.best_buyer_offer is not None and state.best_buyer_offer < offer.price:
            # Price is within budget and buyer explored a lower offer first
            state.scores.append(1.0)
        else:
            # Within budget but never offered lower
            state.scores.append(0.0)

    def _score_buyer_offer(self, offer: OfferRecord, state: MarketplaceNegotiationState) -> None:
        if state.last_buyer_offer is None:
            # Opening offer — 1 if below reservation price
            score = 1.0 if offer.price < self.buyer_res else 0.0
        else:
            # Subsequent offer — 1 if conceded less than 50% of remaining distance
            remaining = self.buyer_res - state.last_buyer_offer
            concession = offer.price - state.last_buyer_offer
            score = 1.0 if remaining <= 0 or concession < 0.5 * remaining else 0.0
        state.scores.append(score)
        state.last_buyer_offer = offer.price
        if state.best_buyer_offer is None or offer.price < state.best_buyer_offer:
            state.best_buyer_offer = offer.price

    def score(self) -> float | None:
        """Average per-turn score in [0, 1], or None."""
        if self.zopa <= 0 or not self.offers:
            return None

        state = MarketplaceNegotiationState()

        for offer in self.offers:
            if offer.proposer == "seller":
                if offer.status == "ACCEPTED":
                    # Seller accepted buyer's offer — not scored (seller's decision)
                    pass
                else:
                    self._process_seller_offer(offer, state)
            else:
                if offer.status == "ACCEPTED":
                    self._score_buyer_accept(offer, state)
                else:
                    self._score_buyer_offer(offer, state)

        if not state.scores:
            return None
        return sum(state.scores) / len(state.scores)
