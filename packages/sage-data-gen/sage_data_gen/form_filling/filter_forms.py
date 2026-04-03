"""Stage 0: Filter CommonForms dataset from HuggingFace.

Downloads the jbarrow/CommonForms dataset, filters for English forms with
open-ended questions, evaluates completeness / domain / over-disclosure risk,
and writes passing entries to a JSONL file for downstream batch generation.

Ported from archive/datasets/form_filling/process_forms_pipeline.py.
"""

import base64
import json
import re
from io import BytesIO
from pathlib import Path

from pydantic import BaseModel, Field
from sage_benchmark.shared import TaskPoolExecutor
from sage_llm import SageMessage, SageModelClient

from sage_data_gen.form_filling.config import FormFillingConfig

# ---------------------------------------------------------------------------
# Pydantic response models (used as response_format for structured parsing)
# ---------------------------------------------------------------------------

DATASET_NAME = "jbarrow/CommonForms"


class OpenEndedQuestionsEvaluation(BaseModel):
    """Evaluation for open-ended questions in a form."""

    has_good_open_ended: bool = Field(
        description="Whether the form has at least one good open-ended question"
    )
    number_of_openended_questions: int = Field(
        description="Number of good open-ended questions identified in the form"
    )
    open_ended_questions: list[str] = Field(
        description="List of identified open-ended questions (field names or full questions)"
    )
    reasoning: str = Field(description="Explanation of the evaluation")


class OverDisclosureEvaluation(BaseModel):
    """Evaluation for over-disclosure privacy risk."""

    over_disclosure_risk: bool = Field(
        description="Whether the form has over-disclosure privacy risk"
    )
    risk_level: str = Field(description="Risk level: 'low', 'medium', or 'high'")
    specific_risks: list[str] = Field(
        description="List of specific over-disclosure risks identified"
    )
    likely_scenarios: list[str] = Field(
        description="2-3 specific examples of how users might overshare"
    )
    reasoning: str = Field(description="Detailed reasoning for the evaluation")


class FormCategorizationEvaluation(BaseModel):
    """Categorization of form into domain categories."""

    primary_category: str = Field(description="Primary domain category of the form")
    secondary_categories: list[str] = Field(
        description="Additional relevant domain categories (if applicable)",
        default_factory=list,
    )
    reasoning: str = Field(description="Explanation for the categorization")


class FormCompletenessEvaluation(BaseModel):
    """Evaluation for whether the form image shows the beginning of the form."""

    starts_from_beginning: bool = Field(
        description=(
            "Whether the form image shows the beginning/first page of the form "
            "(not a middle page like page 2, 3, 4, etc.)"
        )
    )
    reasoning: str = Field(description="Brief explanation of the decision")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

DOMAINS = [
    "Healthcare & Medical",
    "Financial Services & Banking",
    "Insurance",
    "Legal & Court Documents",
    "Immigration & Visa",
    "Employment & HR",
    "Education & Academic",
    "Government Services",
    "Tax & Accounting",
    "Real Estate & Housing",
    "Transportation & DMV",
    "Social Services & Welfare",
    "Veterans Affairs",
    "Small Business & Licensing",
    "Non-Profit & Charitable Organizations",
    "Events & Registration",
    "Travel & Tourism",
    "Consumer Services",
    "Utilities & Infrastructure",
    "Environmental & Permits",
    "Sports & Recreation",
    "Arts & Culture",
    "Research & Surveys",
    "Membership & Subscriptions",
    "Technology & IT Services",
    "Telecommunications",
    "Food & Beverage Services",
    "Pet & Animal Services",
    "Personal Development & Training",
    "Other",
]


def pil_image_to_base64(image) -> str:
    """Convert a PIL Image to a base64-encoded PNG string."""
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()


def _parse_form_content(text: str | None) -> str | None:
    """Extract content between <form> and </form> tags."""
    if not text:
        return None
    match = re.search(r"<form>(.*?)</form>", text, re.DOTALL | re.IGNORECASE)
    return match.group(1).strip() if match else text


# ---------------------------------------------------------------------------
# Individual filter / evaluation steps (all async)
# ---------------------------------------------------------------------------


async def _is_english(image, client: SageModelClient, config: FormFillingConfig) -> bool:
    """Return True if the image contains English-only text."""
    try:
        b64 = pil_image_to_base64(image)
        response = await client.acomplete(
            model=config.vision_model,
            messages=[
                {  # type: ignore[list-item]  # multimodal content requires dict format
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Does this image contain non-English text? Answer only 'yes' or 'no'.",
                        },
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/png;base64,{b64}"},
                        },
                    ],
                }
            ],
            max_tokens=10,
        )
        answer = (response.content or "").strip().lower()
        return "no" in answer
    except Exception as e:
        print(f"Error checking language: {e}")
        return False


async def _extract_text(image, client: SageModelClient, config: FormFillingConfig) -> str | None:
    """Extract all text content from a form image."""
    try:
        b64 = pil_image_to_base64(image)
        response = await client.acomplete(
            model=config.vision_model,
            messages=[
                {  # type: ignore[list-item]  # multimodal content requires dict format
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": (
                                "Extract all text content from this image.\n"
                                "Please transcribe exactly what you see, preserving the layout "
                                "and structure as much as possible.\n"
                                "Include all text fields, labels, form fields, and any other "
                                "text visible in the image.\n\n"
                                "IMPORTANT: Wrap the extracted form content between "
                                "<form> and </form> tags."
                            ),
                        },
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/png;base64,{b64}"},
                        },
                    ],
                }
            ],
            max_tokens=16384,
        )
        content = response.content
        return content.strip() if isinstance(content, str) else None
    except Exception as e:
        print(f"Error extracting text: {e}")
        return None


async def _evaluate_completeness(
    text: str, client: SageModelClient, config: FormFillingConfig
) -> FormCompletenessEvaluation:
    """Check whether the form image shows the first page."""
    prompt = f"""You are evaluating whether a form image shows the BEGINNING of a form.

Since forms are provided as images, the image might show page 2, 3, or 4 of a multi-page form.
We only want forms that start from the beginning (page 1).

**Does this form start from the beginning?**
   - Does it have a proper header/title at the top indicating what the form is about?
   - Does it appear to be the first page (not a continuation like "Page 2", "Schedule H", "Section B - Continued", "Part 3")?
   - Does it have introductory text or instructions that would appear at the start of a form?
   - Are there indicators this is NOT the first page (page numbers, "continued from previous page", mid-section headers)?

Form text:
```
{text}
```

Provide your evaluation."""

    try:
        return await client.aparse(
            model=config.validation_model,
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert at analyzing forms and questionnaires.",
                },
                {"role": "user", "content": prompt},
            ],
            response_format=FormCompletenessEvaluation,
            temperature=0,
        )
    except Exception as e:
        print(f"  Warning: Error evaluating form completeness: {e}")
        return FormCompletenessEvaluation(
            starts_from_beginning=True,
            reasoning=f"Error during evaluation: {e}",
        )


async def _evaluate_open_ended(
    text: str, client: SageModelClient, config: FormFillingConfig
) -> OpenEndedQuestionsEvaluation:
    """Evaluate whether the form has good open-ended questions."""
    prompt = f"""You are evaluating a form to determine if it contains at least one good open-ended question.

A **good open-ended question** is one that:
- Requires a narrative, subjective, or explanatory response
- Allows for varied and detailed answers
- Cannot be answered with a simple fact or selection
- Examples: "Describe your experience", "Explain the rationale", "What are your reasons for", "Tell us about"

**NOT good open-ended** (fixed-answer fields):
- Name, SSN, Date of Birth, Address, Phone, Email
- Yes/No checkboxes, radio buttons
- Simple dropdown menus
- Date/time pickers
- Numeric fields for age, income, etc.

Analyze the form and identify any good open-ended questions.

Form text:
```
{text}
```

Provide your evaluation."""

    try:
        return await client.aparse(
            model=config.validation_model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert at analyzing forms. Identify open-ended "
                        "questions that require narrative or subjective responses."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            response_format=OpenEndedQuestionsEvaluation,
            temperature=0,
        )
    except Exception as e:
        print(f"  Warning: Error evaluating open-ended questions: {e}")
        return OpenEndedQuestionsEvaluation(
            has_good_open_ended=False,
            number_of_openended_questions=0,
            open_ended_questions=[],
            reasoning=f"Error during evaluation: {e}",
        )


async def _categorize_domain(
    text: str, client: SageModelClient, config: FormFillingConfig
) -> FormCategorizationEvaluation:
    """Categorize the form into domain categories."""
    domains_list = "\n".join(f"{i + 1}. {d}" for i, d in enumerate(DOMAINS))
    prompt = f"""You are categorizing a form into domain categories. Analyze the form and determine which domain(s) it belongs to.

Available domains:
{domains_list}

Instructions:
- Select ONE primary category that best describes the form's main purpose
- Optionally select 1-2 secondary categories if the form spans multiple domains
- Provide reasoning for your categorization

Form content:
```
{text}
```

Provide your categorization."""

    try:
        return await client.aparse(
            model=config.validation_model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert at analyzing and categorizing forms "
                        "and documents into domain categories."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            response_format=FormCategorizationEvaluation,
            temperature=0,
        )
    except Exception as e:
        print(f"  Warning: Error categorizing form: {e}")
        return FormCategorizationEvaluation(
            primary_category="Other",
            secondary_categories=[],
            reasoning=f"Error during categorization: {e}",
        )


async def _evaluate_over_disclosure(
    form_text: str,
    categories: list[str],
    client: SageModelClient,
    config: FormFillingConfig,
) -> OverDisclosureEvaluation:
    """Evaluate over-disclosure privacy risk for the form."""
    prompt = f"""You are evaluating a form for over-disclosure privacy risk. The form is categorized as: {", ".join(categories)}.

**Over-disclosure** occurs when forms request or encourage users to share MORE information than necessary for the form's purpose.

Look for these indicators:

**High Risk Indicators:**
- Large, unbounded text boxes with no character/word limits
- Vague field labels like "Additional Information", "Other Details", "Comments"
- Ambiguous prompts: "provide relevant details", "describe your situation", "anything else"
- Open-ended "explain" or "describe" questions without clear boundaries
- High-stakes contexts (immigration, medical, financial, legal) that pressure oversharing
- Language suggesting "more detail = better outcome"

**Low Risk Indicators:**
- Structured fields with clear constraints (dropdowns, checkboxes, character limits)
- Specific, narrow questions with clear scope
- Explicit instructions about what information is needed
- Clear distinction between required and optional fields

Evaluate the form and determine:
1. Whether it has over-disclosure risk (true/false)
2. Risk level (low/medium/high)
3. Specific over-disclosure risks
4. 2-3 likely scenarios where users might overshare

Form content:
```
{form_text}
```

Provide your evaluation."""

    try:
        return await client.aparse(
            model=config.validation_model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert in privacy and data protection, "
                        "specializing in identifying over-disclosure risks in forms."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            response_format=OverDisclosureEvaluation,
            temperature=0.0,
        )
    except Exception as e:
        print(f"Error evaluating over-disclosure risk: {e}")
        return OverDisclosureEvaluation(
            over_disclosure_risk=False,
            risk_level="low",
            specific_risks=[],
            likely_scenarios=[],
            reasoning=f"Error during evaluation: {e}",
        )


# ---------------------------------------------------------------------------
# Single-form pipeline
# ---------------------------------------------------------------------------


async def _process_single_form(
    data: dict,
    idx: int,
    client: SageModelClient,
    config: FormFillingConfig,
    dataset_split: str,
) -> dict | None:
    """Run all filter steps on one form. Returns result dict or None if discarded."""

    # Step 0: Check sufficient objects
    if "objects" in data and "id" in data["objects"]:
        has_enough = len(data["objects"]["id"]) > 10 and any(
            area > 100000 for area in data["objects"]["area"]
        )
        if not has_enough:
            return None

    # Step 1: English check
    if "image" not in data:
        return None
    if not await _is_english(data["image"], client, config):
        print(f"  [{idx}] Non-English, discarding")
        return None

    # Step 2: Extract text
    raw_response = await _extract_text(data["image"], client, config)
    extracted_text = _parse_form_content(raw_response)
    if not extracted_text:
        print(f"  [{idx}] Failed to extract text, discarding")
        return None

    # Step 3: Open-ended questions check
    open_ended_eval = await _evaluate_open_ended(extracted_text, client, config)
    if not open_ended_eval.has_good_open_ended:
        return None

    # Step 4: Completeness check (first page?)
    completeness_eval = await _evaluate_completeness(extracted_text, client, config)
    if not completeness_eval.starts_from_beginning:
        return None

    # Step 5: Domain categorization
    categorization_eval = await _categorize_domain(extracted_text, client, config)

    # Step 6: Over-disclosure evaluation
    categories = [categorization_eval.primary_category]
    if categorization_eval.secondary_categories:
        categories.extend(categorization_eval.secondary_categories)
    over_disclosure_eval = await _evaluate_over_disclosure(
        extracted_text, categories, client, config
    )

    print(
        f"  [{idx}] Passed: {categorization_eval.primary_category}, "
        f"{open_ended_eval.number_of_openended_questions} open-ended Qs, "
        f"over-disclosure={over_disclosure_eval.risk_level}"
    )

    return {
        "id": data.get("id", idx),
        "extracted_text": extracted_text,
        "categorization_evaluation": {
            "primary_category": categorization_eval.primary_category,
            "secondary_categories": categorization_eval.secondary_categories,
            "reasoning": categorization_eval.reasoning,
        },
        "open_ended_evaluation": {
            "has_good_open_ended": open_ended_eval.has_good_open_ended,
            "number_of_openended_questions": open_ended_eval.number_of_openended_questions,
            "open_ended_questions": open_ended_eval.open_ended_questions,
            "reasoning": open_ended_eval.reasoning,
        },
        "over_disclosure_evaluation": {
            "over_disclosure_risk": over_disclosure_eval.over_disclosure_risk,
            "risk_level": over_disclosure_eval.risk_level,
            "specific_risks": over_disclosure_eval.specific_risks,
            "likely_scenarios": over_disclosure_eval.likely_scenarios,
            "reasoning": over_disclosure_eval.reasoning,
        },
        "split": dataset_split,
    }


# ---------------------------------------------------------------------------
# Top-level filter pipeline
# ---------------------------------------------------------------------------


async def filter_common_forms(
    output_jsonl: str,
    config: FormFillingConfig,
    dataset_split: str | None = None,
    start_idx: int = 0,
    limit: int | None = None,
    forms_needed: int | None = None,
) -> str:
    """Filter the CommonForms dataset and write passing entries to JSONL.

    Args:
        output_jsonl: Path to the output JSONL file.
        config: Pipeline configuration (uses vision_model, validation_model,
                max_concurrency, hf_dataset_split, filter_forms_needed).
        dataset_split: Override for HF dataset split (defaults to config value).
        start_idx: Index to start processing from.
        limit: Maximum number of datapoints to examine.
        forms_needed: Stop after collecting this many valid forms
                      (defaults to config value).

    Returns:
        Path to the written JSONL file.
    """
    import duckdb

    split = dataset_split or config.hf_dataset_split
    needed = forms_needed if forms_needed is not None else config.filter_forms_needed

    # Query form metadata + images from HuggingFace parquet files via DuckDB.
    # This streams rows on demand instead of downloading the full dataset.
    parquet_url = f"hf://datasets/{DATASET_NAME}/data/{split}-*.parquet"
    print(f"\nQuerying CommonForms dataset (split: {split}) via DuckDB...")

    # Build SQL with optional LIMIT and OFFSET
    where_clauses = []
    if start_idx > 0:
        where_clauses.append(f"id >= {start_idx}")
    where = f"WHERE {' AND '.join(where_clauses)}" if where_clauses else ""
    limit_clause = f"LIMIT {limit}" if limit else ""

    rows = duckdb.sql(
        f"SELECT * FROM read_parquet('{parquet_url}') {where} {limit_clause}"
    ).fetchall()
    columns = duckdb.sql(f"SELECT * FROM read_parquet('{parquet_url}') LIMIT 0").columns
    print(f"Fetched {len(rows)} rows")

    client = SageModelClient()
    output_path = Path(output_jsonl)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    saved_count = 0

    def _on_complete(result: dict | None) -> None:
        nonlocal saved_count
        if result is not None:
            with open(output_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(result, ensure_ascii=False) + "\n")
            saved_count += 1

    def _on_error(e: Exception) -> None:
        print(f"  Error processing form: {e}")

    executor = TaskPoolExecutor(
        batch_size=config.max_concurrency,
        on_task_complete=_on_complete,
        on_task_error=_on_error,
    )

    # Convert rows to dicts and build coroutines
    coros = []
    for row in rows:
        if needed is not None and saved_count >= needed:
            break
        data = dict(zip(columns, row))
        # Convert image bytes to PIL Image for the processing pipeline
        if "image" in data and isinstance(data["image"], dict):
            from PIL import Image as PILImage

            img_bytes = data["image"]["bytes"]
            data["image"] = PILImage.open(BytesIO(img_bytes))
        idx = data.get("id", len(coros))
        coros.append(_process_single_form(data, idx, client, config, split))

    print(f"Queued {len(coros)} forms for filtering")
    await executor.run(coros)

    print(f"\nFilter complete: {saved_count} forms saved to {output_path}")
    return str(output_path)
