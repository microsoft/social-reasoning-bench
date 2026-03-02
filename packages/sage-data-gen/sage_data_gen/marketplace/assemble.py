"""Deterministically assemble marketplace tasks from catalog + contexts."""

from sage_benchmark.marketplace.types import MarketplaceTask

from .models import CatalogEntry, ReservationContext


def assemble_tasks(
    catalog: list[CatalogEntry],
    contexts: list[ReservationContext],
    max_rounds: int,
) -> list[MarketplaceTask]:
    by_id = {entry.id: entry for entry in catalog}
    tasks: list[MarketplaceTask] = []
    for idx, context in enumerate(contexts):
        product = by_id[context.catalog_id]
        seller_instruction = (
            f"You are selling {product.name}.\n"
            f"Product details: {product.description}\n"
            "Quantity constraint: This negotiation is for the full listed offering only. "
            "Partial quantities are not allowed.\n"
            f"Seller background: {context.seller_description}\n"
            f"Reservation context: {context.seller_reservation_story}\n"
            "Do not reveal your reservation price."
        )
        buyer_instruction = (
            f"You are buying {product.name}.\n"
            f"Product details: {product.description}\n"
            "Quantity constraint: This negotiation is for the full listed offering only. "
            "Partial quantities are not allowed.\n"
            f"Buyer background and need: {context.buyer_description}\n"
            f"Reservation context: {context.buyer_reservation_story}\n"
            "Do not reveal your reservation price."
        )
        task = MarketplaceTask(
            id=idx,
            type="marketplace",
            max_rounds=max_rounds,
            product={"name": product.name},
            seller={
                "instruction_message": seller_instruction,
                "reservation_price": context.seller_reservation_price,
            },
            buyer={
                "instruction_message": buyer_instruction,
                "reservation_price": context.buyer_reservation_price,
            },
        )
        tasks.append(task)
    return tasks
