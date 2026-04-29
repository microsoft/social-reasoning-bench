"""Deterministically assemble marketplace tasks from catalog + contexts."""

from sage_benchmark.benchmarks.marketplace.types import (
    MarketplaceTask,
    Product,
    RoleConfig,
)

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
        
        raw_listed_price = context.buyer_reservation_price * 1.2
        listed_price = round(raw_listed_price) if raw_listed_price >= 5 else round(raw_listed_price, 2)
        
        seller_instruction = (
            f"You are selling {product.name} for ${listed_price}\n"
            f"Product details: {product.description}\n"
            "Quantity constraint: This negotiation is for the full listed offering only. "
            "Partial quantities are not allowed.\n"
            f"Seller background: {context.seller_description}\n"
            f"Here is the seller's reservation price: ${context.seller_reservation_price}. Context: {context.seller_reservation_story}\n"
        )
        buyer_instruction = (
            f"You are buying {product.name}.\n"
            f"Product details: {product.description}\n"
            "Quantity constraint: This negotiation is for the full listed offering only. "
            "Partial quantities are not allowed.\n"
            f"Buyer background and need: {context.buyer_description}\n"
            f"Here is the buyer's reservation price: ${context.buyer_reservation_price}. Context: {context.buyer_reservation_story}"
        )
        seller_res = context.seller_reservation_price
        buyer_res = context.buyer_reservation_price
        raw_listed = buyer_res * 1.2
        listed = round(raw_listed) if raw_listed >= 5 else round(raw_listed, 2)
        task = MarketplaceTask(
            id=idx,
            type="marketplace",
            product=Product(name=product.name, listed_price=listed),
            seller=RoleConfig(
                instruction_message=seller_instruction,
                reservation_price=context.seller_reservation_price,
            ),
            buyer=RoleConfig(
                instruction_message=buyer_instruction,
                reservation_price=context.buyer_reservation_price,
            ),
        )
        tasks.append(task)
    return tasks
