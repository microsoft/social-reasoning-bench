"""Stage 2: Generate ground truth by filling form with realistic data.

Fills the form with LLM-generated data, classifies fields as open-ended
or close-ended based on the filled values, and returns a flat ground truth dict.
"""

import json
from pathlib import Path

from sage_llm import SageModelClient

from sage_data_gen.form_filling.config import FormFillingConfig
from sage_data_gen.form_filling.models import OpenEndedFieldsAnalysis
from sage_data_gen.form_filling.prompts import CLASSIFY_FIELDS_PROMPT, FILL_FORM_PROMPT
from sage_data_gen.form_filling.utils import (
    clear_signature_fields,
    flatten_form_data,
    import_form_model_from_file,
)


def _get_form_schema(form_class) -> str:
    """Get form schema as a formatted string."""
    return json.dumps(form_class.model_json_schema(), indent=2)


async def _fill_form_with_llm(form_class, client: SageModelClient, model: str) -> dict:
    """Fill a form using LLM structured output."""
    class_name = form_class.__name__
    form_title = class_name.replace("_", " ").title()
    if form_class.__doc__:
        form_title = form_class.__doc__.strip().split("\n")[0]

    form_schema = _get_form_schema(form_class)

    print(f"  Filling form with {model}...")
    filled_form = await client.aparse(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "You are an expert at filling out forms with realistic data.",
            },
            {
                "role": "user",
                "content": FILL_FORM_PROMPT.format(form_schema=form_schema, form_title=form_title),
            },
        ],
        response_format=form_class,
        temperature=0.8,
    )

    filled_data = filled_form.model_dump()
    filled_data = clear_signature_fields(filled_data)
    return filled_data


async def _classify_form_fields(
    filled_data: dict, client: SageModelClient, model: str
) -> dict[str, bool]:
    """Classify each field as open-ended or not using LLM.

    Args:
        filled_data: Filled form data dict.
        client: SageModelClient instance.
        model: Model name for classification.

    Returns:
        Dict mapping field_id to is_open_ended boolean.
    """
    print("  Classifying fields as open/close-ended...")

    flattened = flatten_form_data(filled_data)
    fields_for_analysis = []
    for item in flattened:
        field_path = item["field_path"]
        value = item["value"]

        if not value or value == "":
            continue
        field_key = field_path.split(".")[-1].split("]")[-1].lstrip(".")
        if "signature" in field_key.lower():
            continue

        label = field_path.split(".")[-1].replace("_", " ").title()
        fields_for_analysis.append(
            {
                "id": field_path,
                "label": label,
                "example_value": value,
            }
        )

    analysis = await client.aparse(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "You are an expert at analyzing form fields to identify which allow open-ended responses.",
            },
            {
                "role": "user",
                "content": CLASSIFY_FIELDS_PROMPT.format(
                    fields_json=json.dumps(fields_for_analysis, indent=2)
                ),
            },
        ],
        response_format=OpenEndedFieldsAnalysis,
        temperature=0.3,
    )

    expected_ids = {f["id"] for f in fields_for_analysis}

    max_retries = 3
    for attempt in range(max_retries + 1):
        classifications: dict[str, bool] = {}
        for c in analysis.classifications:
            if c.field_id in expected_ids:
                classifications[c.field_id] = c.is_open_ended
            else:
                print(f"  Warning: LLM returned unknown field_id '{c.field_id}'")

        missing = expected_ids - set(classifications.keys())
        if not missing:
            break

        if attempt < max_retries:
            print(
                f"  Retry {attempt + 1}/{max_retries}: "
                f"{len(missing)} fields missing from classification: {missing}"
            )
            analysis = await client.aparse(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert at analyzing form fields to identify which allow open-ended responses.",
                    },
                    {
                        "role": "user",
                        "content": CLASSIFY_FIELDS_PROMPT.format(
                            fields_json=json.dumps(fields_for_analysis, indent=2)
                        ),
                    },
                ],
                response_format=OpenEndedFieldsAnalysis,
                temperature=0.3,
            )
        else:
            raise ValueError(
                f"Classification failed after {max_retries} retries. Missing field IDs: {missing}"
            )

    open_count = sum(1 for v in classifications.values() if v)
    print(f"  Classified {len(classifications)} fields ({open_count} open-ended)")
    return classifications


async def generate_groundtruth(
    form_model_path: Path,
    client: SageModelClient,
    config: FormFillingConfig,
) -> dict:
    """Fill form with realistic data and classify fields.

    This is the main entry point for Stage 2.

    Args:
        form_model_path: Path to the form_model.py file.
        client: SageModelClient instance.
        config: Pipeline configuration.

    Returns:
        Flat ground truth dict: {"field_id": {"answer": str, "is_open_ended": bool}}.
    """
    # Import the form model
    print("  Importing form module...")
    form_class = import_form_model_from_file(form_model_path)

    # Fill form with LLM
    filled_data = await _fill_form_with_llm(form_class, client, config.parsing_model)

    # Classify fields
    print("  Classifying fields...")
    classifications = await _classify_form_fields(filled_data, client, config.validation_model)

    # Flatten and build flat groundtruth
    flattened = flatten_form_data(filled_data)
    groundtruth = {}
    for item in flattened:
        field_id = item["field_path"]
        groundtruth[field_id] = {
            "answer": item["value"],
            "is_open_ended": classifications.get(field_id, False),
        }

    total = len(groundtruth)
    non_empty = sum(1 for v in groundtruth.values() if v["answer"])
    open_ended = sum(1 for v in groundtruth.values() if v["is_open_ended"])
    print(f"  Total fields: {total}, Non-empty: {non_empty}, Open-ended: {open_ended}")

    return groundtruth
