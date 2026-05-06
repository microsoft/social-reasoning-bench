"""Stats utilities for marketplace datasets."""

from collections import Counter

from srbench.benchmarks.marketplace.types import MarketplaceTask


def _sign_for_task(task: MarketplaceTask) -> str:
    margin = task.buyer.reservation_price - task.seller.reservation_price
    return "positive" if margin >= 0 else "negative"


def compute_stats(tasks: list[MarketplaceTask]) -> dict:
    signs = Counter(_sign_for_task(t) for t in tasks)
    return {
        "stats": {
            "total_tasks": len(tasks),
            "overlap_sign_counts": dict(sorted(signs.items())),
            "avg_overlap_margin": round(
                sum(t.buyer.reservation_price - t.seller.reservation_price for t in tasks)
                / len(tasks),
                4,
            )
            if tasks
            else 0.0,
            "positive_overlap_rate": round(
                sum(
                    1
                    for t in tasks
                    if (t.buyer.reservation_price - t.seller.reservation_price) >= 0
                )
                / len(tasks),
                4,
            )
            if tasks
            else 0.0,
        }
    }
