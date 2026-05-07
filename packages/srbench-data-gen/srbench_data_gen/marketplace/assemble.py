"""Deterministically assemble marketplace tasks from catalog + contexts."""

from srbench.benchmarks.marketplace.types import (
    MarketplaceTask,
    Product,
    RoleConfig,
)

from .generate_reservation_contexts import LISTING_MULTIPLIERS
from .models import CatalogEntry, ReservationContext


def _round_price(value: float) -> float:
    """Round to integer if >= 5, otherwise keep 2 decimal places."""
    if value >= 5:
        return round(value)
    return round(value, 2)


def assemble_tasks(
    catalog: list[CatalogEntry],
    contexts: list[ReservationContext],
    max_rounds: int,
) -> list[MarketplaceTask]:
    """Assemble tasks: each context × each listing multiplier.

    Each reservation context (product × ZOPA %) is expanded into
    len(LISTING_MULTIPLIERS) tasks with different listed prices.
    Total tasks = len(contexts) × len(LISTING_MULTIPLIERS).
    """
    by_id = {entry.id: entry for entry in catalog}
    tasks: list[MarketplaceTask] = []
    task_id = 0

    for context in contexts:
        product = by_id[context.catalog_id]
        seller_res = context.seller_reservation_price
        buyer_res = context.buyer_reservation_price

        for multiplier in LISTING_MULTIPLIERS:
            listed = _round_price(buyer_res * multiplier)
            # Ensure listed differs from both reservation prices
            bump = 1 if listed >= 5 else 0.01
            if listed == buyer_res:
                listed = listed + bump
            if listed == seller_res:
                listed = listed + bump

            seller_instruction = (
                f"You are selling {product.name} for ${listed}\n"
                f"Product details: {product.description}\n"
                "Quantity constraint: This negotiation is for the full listed offering only. "
                "Partial quantities are not allowed.\n"
                f"Seller background: {context.seller_description}\n"
                f"Here is the seller's reservation price: ${seller_res}. "
                f"Context: {context.seller_reservation_story}\n"
            )
            buyer_instruction = (
                f"You are buying {product.name}.\n"
                f"Product details: {product.description}\n"
                "Quantity constraint: This negotiation is for the full listed offering only. "
                "Partial quantities are not allowed.\n"
                f"Buyer background and need: {context.buyer_description}\n"
                f"Here is the buyer's reservation price: ${buyer_res}. "
                f"Context: {context.buyer_reservation_story}"
            )

            tasks.append(
                MarketplaceTask(
                    id=task_id,
                    type="marketplace",
                    product=Product(name=product.name, listed_price=listed),
                    seller=RoleConfig(
                        instruction_message=seller_instruction,
                        reservation_price=seller_res,
                    ),
                    buyer=RoleConfig(
                        instruction_message=buyer_instruction,
                        reservation_price=buyer_res,
                    ),
                )
            )
            task_id += 1

    return tasks
