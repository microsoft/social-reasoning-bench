"""Stage 2b: Mask N close-ended fields in ground truth.

Applies three layers of filtering to select standalone fields for masking:
1. Keyword exclusion — skip fields with 'name', 'city', 'state', 'zip' in the key
2. Random sampling — pick N fields from the remaining eligible pool
3. LLM judge — verify each pick is truly standalone; resample if not
"""

import copy
import json
import random

from sage_llm import SageMessage, SageModelClient

from sage_data_gen.form_filling.config import FormFillingConfig
from sage_data_gen.form_filling.models import StandaloneAnalysis
from sage_data_gen.form_filling.prompts import MASK_STANDALONE_JUDGE_PROMPT

# Keywords that signal non-standalone fields (checked as substrings)
EXCLUDED_KEYWORDS = {
    "name",
    "city",
    "state",
    "zip",
    "gender",
    "race",
    "age",
    "email",
    "e_mail",
    "title",
}


def _extract_field_key(field_id: str) -> str:
    """Extract the terminal field key from a dotted/bracketed field ID.

    Args:
        field_id: Dotted or bracketed field path (e.g. ``"section.field_name"``).

    Returns:
        Terminal field key string.
    """
    return field_id.split(".")[-1].split("]")[-1].lstrip(".")


def _is_keyword_excluded(field_key: str) -> bool:
    """Check if a field key contains any excluded keyword.

    Args:
        field_key: Terminal field key (e.g. ``"zip_code"``).

    Returns:
        *True* if the key contains a keyword from :data:`EXCLUDED_KEYWORDS`.
    """
    lower = field_key.lower()
    return any(kw in lower for kw in EXCLUDED_KEYWORDS)


async def _judge_standalone(
    candidates: list[tuple[str, dict]],
    groundtruth: dict,
    client: SageModelClient,
    config: FormFillingConfig,
) -> list[str]:
    """Use LLM to identify which candidate fields are NOT standalone.

    Args:
        candidates: List of (field_id, info) tuples for candidate fields.
        groundtruth: Full ground truth dict for context.
        client: SageModelClient instance.
        config: Pipeline configuration.

    Returns:
        List of field_ids that are NOT standalone (should be removed).
    """
    # Build context: all fields with full answers
    all_fields = []
    for fid, info in groundtruth.items():
        all_fields.append({"field_id": fid, "answer": info["answer"]})

    # Build candidate list
    candidate_fields = []
    for fid, info in candidates:
        candidate_fields.append({"field_id": fid, "answer": info["answer"]})

    result = await client.aparse(
        model=config.validation_model,
        messages=[
            {
                "role": "system",
                "content": "You are an expert at analyzing form field dependencies.",
            },
            {
                "role": "user",
                "content": MASK_STANDALONE_JUDGE_PROMPT.format(
                    all_fields_json=json.dumps(all_fields, indent=2),
                    candidate_fields_json=json.dumps(candidate_fields, indent=2),
                ),
            },
        ],
        response_format=StandaloneAnalysis,
        temperature=0,
    )

    non_standalone = []
    for r in result.results:
        if not r.is_standalone:
            non_standalone.append(r.field_id)
            print(f"    Rejected '{r.field_id}': {r.reasoning}")

    return non_standalone


async def mask_groundtruth(
    groundtruth: dict,
    n: int = 5,
    seed: int = 42,
    client: SageModelClient | None = None,
    config: FormFillingConfig | None = None,
) -> tuple[dict, list[dict]]:
    """Mask n close-ended fields by setting their answers to empty string.

    Uses keyword exclusion and an LLM judge to select standalone fields.

    Args:
        groundtruth: Flat ground truth dict {field_id: {answer, is_open_ended}}.
        n: Number of close-ended fields to mask.
        seed: Random seed for reproducibility.
        client: SageModelClient for LLM judge (optional; skips judge if None).
        config: Pipeline configuration (optional; skips judge if None).

    Returns:
        Tuple of (masked_groundtruth, masked_fields_list).
        masked_fields_list contains dicts with 'field_id' and 'original_value'.
    """
    # Find eligible fields: close-ended, non-empty, non-signature, non-boolean, non-excluded-keyword
    eligible = []
    keyword_excluded = 0
    boolean_excluded = 0
    for field_id, info in groundtruth.items():
        if info["is_open_ended"]:
            continue
        if not info["answer"] or info["answer"] in ("", "N/A", "None"):
            continue
        if info["answer"].lower() in ("true", "false"):
            boolean_excluded += 1
            continue
        field_key = _extract_field_key(field_id)
        if "signature" in field_key.lower():
            continue
        if _is_keyword_excluded(field_key):
            keyword_excluded += 1
            continue
        eligible.append((field_id, info))

    if boolean_excluded:
        print(f"  Excluded {boolean_excluded} boolean fields (true/false answers)")
    if keyword_excluded:
        print(
            f"  Excluded {keyword_excluded} fields by keyword filter (name/city/state/zip/gender/race/age)"
        )

    # Randomly select fields to mask
    rng = random.Random(seed)
    num_to_mask = min(n, len(eligible))
    to_mask = rng.sample(eligible, num_to_mask) if num_to_mask > 0 else []

    # LLM judge: verify picks are standalone, resample if needed
    if client is not None and config is not None and to_mask:
        max_retries = config.max_mask_retries
        # Track fields permanently rejected by the judge
        rejected_ids: set[str] = set()

        for attempt in range(max_retries):
            print(f"  LLM standalone check (attempt {attempt + 1}/{max_retries})...")
            non_standalone = await _judge_standalone(to_mask, groundtruth, client, config)

            if not non_standalone:
                print(f"  All {len(to_mask)} fields confirmed standalone")
                break

            # Remove non-standalone fields
            rejected_ids.update(non_standalone)
            to_mask = [(fid, info) for fid, info in to_mask if fid not in non_standalone]

            # How many replacements do we need?
            needed = num_to_mask - len(to_mask)
            if needed <= 0:
                break

            # Build replacement pool: eligible minus already selected and rejected
            selected_ids = {fid for fid, _ in to_mask}
            replacement_pool = [
                (fid, info)
                for fid, info in eligible
                if fid not in selected_ids and fid not in rejected_ids
            ]

            if not replacement_pool:
                print(f"  No more eligible fields to resample from")
                break

            replacements = rng.sample(replacement_pool, min(needed, len(replacement_pool)))
            to_mask.extend(replacements)
            print(f"  Resampled {len(replacements)} replacement fields")
        else:
            # Exhausted retries; use whatever we have
            print(f"  Exhausted {max_retries} retries, proceeding with {len(to_mask)} fields")

    # Create masked copy
    masked_gt = copy.deepcopy(groundtruth)
    masked_fields = []
    for field_id, info in to_mask:
        masked_gt[field_id]["answer"] = ""
        masked_fields.append(
            {
                "field_id": field_id,
                "original_value": info["answer"],
            }
        )

    print(f"  Masked {len(to_mask)}/{len(eligible)} eligible close-ended fields")
    return masked_gt, masked_fields
