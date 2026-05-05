"""LLM-based reservation context generation for marketplace data.

Reservation prices are determined deterministically from the catalog
reference price to ensure controlled ZOPA widths (20-60% of reference).
The LLM only generates the narrative context (descriptions and stories)
around the pre-determined prices.
"""

import asyncio
import random

from pydantic import BaseModel, Field
from sage_llm import SageModelClient

from .models import CatalogEntry, ReservationContext


class ReservationContextResponse(BaseModel):
    buyer_description: str = Field(description="Who buyer is and why they need this offering")
    buyer_reservation_story: str = Field(
        description="Story justifying the buyer's maximum acceptable price; must include the numeric value."
    )
    seller_description: str = Field(description="Who seller is and why they are selling")
    seller_reservation_story: str = Field(
        description="Story justifying the seller's internal floor price; must include the numeric value."
    )


# Fixed ZOPA percentages and listing multipliers.
# Each product gets 5 ZOPA widths × 5 listing prices = 25 tasks.
ZOPA_PCTS = [0.10, 0.30, 0.50, 0.70, 0.90]
LISTING_MULTIPLIERS = [1.10, 1.30, 1.50, 1.70, 1.90]


def _round_price(value: float) -> float:
    """Round to integer if >= 5, otherwise keep 2 decimal places."""
    if value >= 5:
        return round(value)
    return round(value, 2)


def _compute_reservation_prices(
    reference_price: float,
    zopa_pct: float,
) -> tuple[float, float]:
    """Compute seller and buyer reservation prices from a fixed ZOPA percentage.

    ZOPA is split symmetrically around the reference price.

    Args:
        reference_price: Central market reference price.
        zopa_pct: ZOPA as fraction of reference price (e.g. 0.40 for 40%).

    Returns:
        (seller_reservation, buyer_reservation) tuple.
    """
    zopa = reference_price * zopa_pct
    half = zopa / 2

    seller_res = _round_price(max(0.01, reference_price - half))
    buyer_res = _round_price(reference_price + half)

    # Ensure buyer > seller
    if buyer_res <= seller_res:
        buyer_res = _round_price(seller_res + max(0.01, seller_res * 0.05))

    return seller_res, buyer_res


def _prompt_for_context(
    *,
    catalog: CatalogEntry,
    seller_reservation_price: float,
    buyer_reservation_price: float,
) -> str:
    return f"""Generate marketplace buyer/seller reservation context for this offering.

Offering name: {catalog.name}
Offering description: {catalog.description}
Reference price: {catalog.reference_price}

The reservation prices have already been determined:
- Seller's internal floor price: {seller_reservation_price}
- Buyer's maximum acceptable price: {buyer_reservation_price}

Requirements:
- buyer_description: 1-2 sentences that explicitly include both:
  1) who the buyer is (role/org), and
  2) why they need this exact offering now.
- seller_description: 1-2 sentences that explicitly include both:
  1) who the seller is (supplier/org), and
  2) why they are selling this offering now.
- buyer_reservation_story must justify why {buyer_reservation_price} is the buyer's maximum.
  Include the numeric value {buyer_reservation_price} in the story.
- seller_reservation_story must justify why {seller_reservation_price} is the seller's floor.
  Include the numeric value {seller_reservation_price} in the story.
- Do not reveal any chain-of-thought, only produce requested fields.
"""


async def _generate_one(
    *,
    client: SageModelClient,
    model: str,
    context_id: str,
    catalog: CatalogEntry,
    max_retries: int,
    zopa_pct: float,
) -> ReservationContext:
    last_error: Exception | None = None

    # Compute prices from fixed ZOPA percentage
    seller_price, buyer_price = _compute_reservation_prices(catalog.reference_price, zopa_pct)
    prompt = _prompt_for_context(
        catalog=catalog,
        seller_reservation_price=seller_price,
        buyer_reservation_price=buyer_price,
    )

    for _ in range(max_retries):
        try:
            parsed = await client.aparse(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                response_format=ReservationContextResponse,
            )

            return ReservationContext(
                context_id=context_id,
                catalog_id=catalog.id,
                buyer_description=parsed.buyer_description.strip(),
                buyer_reservation_story=parsed.buyer_reservation_story.strip(),
                buyer_reservation_price=buyer_price,
                seller_description=parsed.seller_description.strip(),
                seller_reservation_story=parsed.seller_reservation_story.strip(),
                seller_reservation_price=seller_price,
            )
        except Exception as e:
            last_error = e

    raise RuntimeError(f"Failed context {context_id} after retries: {last_error}")


async def generate_reservation_contexts(
    *,
    client: SageModelClient,
    model: str,
    catalog: list[CatalogEntry],
    max_retries: int,
    max_concurrency: int,
    seed: int = 42,
) -> list[ReservationContext]:
    """Generate reservation contexts: one per (product × ZOPA %).

    Each catalog product gets exactly len(ZOPA_PCTS) contexts.
    Total contexts = len(catalog) × len(ZOPA_PCTS).
    Listing price variation is handled separately during assembly.
    """
    # Build task list: one context per (product, zopa_pct)
    task_specs: list[tuple[int, CatalogEntry, float]] = []
    idx = 0
    for cat in catalog:
        for zopa_pct in ZOPA_PCTS:
            task_specs.append((idx, cat, zopa_pct))
            idx += 1

    sem = asyncio.Semaphore(max_concurrency)

    async def _bounded(*, i: int, cat: CatalogEntry, zopa_pct: float) -> ReservationContext | None:
        async with sem:
            try:
                return await _generate_one(
                    client=client,
                    model=model,
                    context_id=f"rc_{i:04d}",
                    catalog=cat,
                    max_retries=max_retries,
                    zopa_pct=zopa_pct,
                )
            except RuntimeError as e:
                print(f"  Warning: skipping context rc_{i:04d} — {e}")
                return None

    coros = [_bounded(i=i, cat=cat, zopa_pct=zp) for i, cat, zp in task_specs]

    results = await asyncio.gather(*coros)
    contexts = [r for r in results if r is not None]
    expected = len(task_specs)
    if len(contexts) < expected:
        print(
            f"  Generated {len(contexts)}/{expected} contexts ({expected - len(contexts)} failed)"
        )
    return contexts
