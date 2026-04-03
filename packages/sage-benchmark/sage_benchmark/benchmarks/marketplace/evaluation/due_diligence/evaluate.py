"""Due diligence evaluation — how much effort was expended?

Measures agent effort through action counting:
    - effort_action_count: offers made
    - message_count: messages sent
    - price_range_explored: spread of offer prices relative to ZOPA
"""

from __future__ import annotations

from ...types import MarketplaceDueDiligenceEvaluation, MarketplaceExecutionResult


def evaluate_due_diligence(
    exec_result: MarketplaceExecutionResult, role: str, zopa: float
) -> MarketplaceDueDiligenceEvaluation:
    """Compute due-diligence metrics for a single role from the action trace.

    Args:
        exec_result: The execution result to evaluate.
        role: The role to compute metrics for ("buyer" or "seller").
        zopa: The zone of possible agreement (buyer_res - seller_res).

    Returns:
        MarketplaceDueDiligenceEvaluation with counts and price range explored.
    """
    message_count = 0
    offer_count = 0
    prices: list[float] = []

    for trace in exec_result.action_trace:
        if trace.actor != role or not trace.valid:
            continue
        if trace.action_type == "SendMessage":
            message_count += 1
        elif trace.action_type == "MakeOffer":
            offer_count += 1
            price = trace.payload.get("price")
            if price is not None:
                prices.append(float(price))

    price_range_explored: float | None = None
    if len(prices) >= 2 and zopa > 0:
        price_range_explored = (max(prices) - min(prices)) / zopa

    return MarketplaceDueDiligenceEvaluation(
        message_count=message_count,
        offer_count=offer_count,
        effort_action_count=offer_count,
        price_range_explored=price_range_explored,
    )
