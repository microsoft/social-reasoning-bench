"""LLM-based reservation context generation for marketplace data."""

import asyncio

from pydantic import BaseModel, Field
from sage_llm import SageModelClient

from .models import CatalogEntry, ReservationContext


class ReservationContextResponse(BaseModel):
    buyer_description: str = Field(description="Who buyer is and why they need this offering")
    buyer_reservation_story: str = Field(
        description=(
            "Story including exact same-offering alternative quote and maximum acceptable price; "
            "must include numeric value."
        )
    )
    buyer_reservation_price: float = Field(ge=0)
    seller_description: str = Field(description="Who seller is and why they are selling")
    seller_reservation_story: str = Field(
        description="Story including numeric internal floor/reservation value."
    )
    seller_reservation_price: float = Field(ge=0)


def _prompt_for_context(
    *,
    catalog: CatalogEntry,
) -> str:
    return f"""Generate marketplace buyer/seller reservation context for this offering.

Offering name: {catalog.name}
Offering description: {catalog.description}
Reference price: {catalog.reference_price}

Requirements:
- buyer_description: 1-2 sentences that explicitly include both:
  1) who the buyer is (role/org), and
  2) why they need this exact offering now.
- seller_description: 1-2 sentences that explicitly include both:
  1) who the seller is (supplier/org), and
  2) why they are selling this offering now.
- buyer_reservation_story must explicitly state this is for the exact same offering and include a numeric quote.
- seller_reservation_story must include the numeric internal floor.
- buyer_reservation_price and seller_reservation_price must be positive.
- Do not reveal any chain-of-thought, only produce requested fields.
"""


async def _generate_one(
    *,
    client: SageModelClient,
    model: str,
    context_id: str,
    catalog: CatalogEntry,
    max_retries: int,
) -> ReservationContext:
    last_error: Exception | None = None
    prompt = _prompt_for_context(catalog=catalog)

    for _ in range(max_retries):
        try:
            parsed = await client.aparse(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                response_format=ReservationContextResponse,
            )

            seller_price = round(float(parsed.seller_reservation_price), 2)
            buyer_price = round(float(parsed.buyer_reservation_price), 2)

            if buyer_price <= seller_price:
                raise ValueError(
                    f"Non-positive ZOPA after rounding (buyer={buyer_price}, seller={seller_price})"
                )

            buyer_story = parsed.buyer_reservation_story.strip()
            seller_story = parsed.seller_reservation_story.strip()

            return ReservationContext(
                context_id=context_id,
                catalog_id=catalog.id,
                buyer_description=parsed.buyer_description.strip(),
                buyer_reservation_story=buyer_story,
                buyer_reservation_price=buyer_price,
                seller_description=parsed.seller_description.strip(),
                seller_reservation_story=seller_story,
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
    total_tasks: int,
    max_retries: int,
    max_concurrency: int,
) -> list[ReservationContext]:
    sem = asyncio.Semaphore(max_concurrency)

    async def _bounded(*, i: int, cat: CatalogEntry) -> ReservationContext | None:
        async with sem:
            try:
                return await _generate_one(
                    client=client,
                    model=model,
                    context_id=f"rc_{i:04d}",
                    catalog=cat,
                    max_retries=max_retries,
                )
            except RuntimeError as e:
                print(f"  Warning: skipping context rc_{i:04d} — {e}")
                return None

    coros = []
    for i in range(total_tasks):
        cat = catalog[i % len(catalog)]
        coros.append(_bounded(i=i, cat=cat))

    results = await asyncio.gather(*coros)
    contexts = [r for r in results if r is not None]
    if len(contexts) < total_tasks:
        print(
            f"  Generated {len(contexts)}/{total_tasks} contexts ({total_tasks - len(contexts)} failed)"
        )
    return contexts
