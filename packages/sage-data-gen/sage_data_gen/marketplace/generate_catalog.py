"""LLM-based catalog generation for marketplace data."""

import re

from pydantic import BaseModel, Field
from sage_llm import SageMessage, SageModelClient

from .models import CatalogEntry


class RawCatalogEntry(BaseModel):
    name: str = Field(description="Short item name")
    description: str = Field(description="Detailed product/service description")
    reference_price: float = Field(gt=0, description="Reasonable central market reference price")


class CatalogResponse(BaseModel):
    entries: list[RawCatalogEntry]


def _slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")
    return slug[:48] if slug else "item"


PRICE_BUCKETS = [
    ("$10–$30", 10, 30),
    ("$30–$100", 30, 100),
    ("$100–$500", 100, 500),
    ("$500–$5000", 500, 5000),
]


def _catalog_prompt(count: int, price_range: str, existing_names: list[str]) -> str:
    avoid_clause = ""
    if existing_names:
        avoid_list = "\n".join(f"- {name}" for name in existing_names[:40])
        avoid_clause = (
            f"\nAvoid repeating these existing offering names (or near-duplicates):\n{avoid_list}\n"
        )
    return f"""Generate a benchmark catalog of {count} negotiable offerings.

Requirements:
- Focus on mostly commodity-like offerings with stable, comparable specs.
- Include a mix of goods and services.
- All reference_price values MUST be in the range {price_range}.
- For each offering, provide:
  1) name
  2) detailed description (2-3 sentences)
  3) a positive reference_price within {price_range}
- Avoid duplicates and near-duplicates.
- Make the offering concrete enough that a buyer can compare an alternative for the exact same offering.
{avoid_clause}"""


async def generate_catalog(
    client: SageModelClient,
    model: str,
    catalog_size: int,
    max_retries: int,
) -> list[CatalogEntry]:
    # Distribute catalog_size evenly across price buckets
    per_bucket = catalog_size // len(PRICE_BUCKETS)
    remainder = catalog_size - per_bucket * len(PRICE_BUCKETS)

    raw_entries: list[RawCatalogEntry] = []
    seen_names: set[str] = set()

    for bucket_idx, (price_range, lo, hi) in enumerate(PRICE_BUCKETS):
        target = per_bucket + (1 if bucket_idx < remainder else 0)
        if target == 0:
            continue

        stalled_batches = 0
        last_error: Exception | None = None

        while len([e for e in raw_entries if lo <= e.reference_price <= hi]) < target:
            needed = target - len([e for e in raw_entries if lo <= e.reference_price <= hi])
            request_size = min(40, needed + 2)  # request a few extra for dedup headroom
            prompt = _catalog_prompt(request_size, price_range, [r.name for r in raw_entries])

            batch: list[RawCatalogEntry] = []
            for _ in range(max_retries):
                try:
                    result = await client.aparse(
                        model=model,
                        messages=[{"role": "user", "content": prompt}],
                        response_format=CatalogResponse,
                    )
                    if not result.entries:
                        raise ValueError("Model returned 0 catalog entries in batch")
                    batch = result.entries
                    break
                except Exception as e:
                    last_error = e

            if not batch:
                raise RuntimeError(
                    f"Failed to generate catalog batch for {price_range} after {max_retries} retries: {last_error}"
                )

            before = len(raw_entries)
            for item in batch:
                key = item.name.strip().lower()
                if not key or key in seen_names:
                    continue
                # Clamp price to bucket range
                price = float(item.reference_price)
                if price < lo:
                    price = lo
                elif price > hi:
                    price = hi
                item.reference_price = price
                seen_names.add(key)
                raw_entries.append(item)
                if len([e for e in raw_entries if lo <= e.reference_price <= hi]) >= target:
                    break

            if len(raw_entries) == before:
                stalled_batches += 1
            else:
                stalled_batches = 0

            if stalled_batches >= max_retries:
                print(f"  Warning: catalog generation stalled for {price_range}; got {len([e for e in raw_entries if lo <= e.reference_price <= hi])}/{target}")
                break

    seen_ids: set[str] = set()
    catalog: list[CatalogEntry] = []
    for i, raw in enumerate(raw_entries[:catalog_size]):
        base = _slugify(raw.name)
        entry_id = f"cat_{base}"
        if entry_id in seen_ids:
            entry_id = f"{entry_id}_{i:02d}"
        seen_ids.add(entry_id)
        ref = float(raw.reference_price)
        ref = round(ref) if ref >= 5 else round(ref, 2)
        catalog.append(
            CatalogEntry(
                id=entry_id,
                name=raw.name.strip(),
                description=raw.description.strip(),
                reference_price=ref,
            )
        )
    return catalog
