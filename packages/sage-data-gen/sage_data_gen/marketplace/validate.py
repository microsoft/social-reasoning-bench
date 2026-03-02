"""Deterministic validation for generated marketplace tasks."""

from sage_benchmark.marketplace.types import MarketplaceTask


def validate_tasks(tasks: list[MarketplaceTask]) -> dict:
    errors: list[str] = []
    ids = [task.id for task in tasks]
    if len(ids) != len(set(ids)):
        errors.append("Duplicate task IDs detected")

    for task in tasks:
        if task.seller.reservation_price < 0 or task.buyer.reservation_price < 0:
            errors.append(f"Task {task.id}: negative reservation price")

    return {
        "validation": {
            "total_tasks": len(tasks),
            "passed": len(errors) == 0,
            "errors": errors,
            "checks": {
                "unique_ids": len(ids) == len(set(ids)),
                "reservation_nonnegative": all(
                    t.seller.reservation_price >= 0 and t.buyer.reservation_price >= 0
                    for t in tasks
                ),
            },
        }
    }
