"""Stage 2: Generate ground truth by filling form with realistic data.

Imports the form model, fills it with LLM-generated data, classifies fields
as open-ended or close-ended, and returns a flat ground truth dict.
"""

import json
from pathlib import Path

from sage_llm import ModelClient

from sage_data_gen.form_filling.config import FormFillingConfig
from sage_data_gen.form_filling.models import FieldClassification, OpenEndedFieldsAnalysis
from sage_data_gen.form_filling.prompts import CLASSIFY_FIELDS_PROMPT, FILL_FORM_PROMPT
from sage_data_gen.form_filling.utils import (
    clear_signature_fields,
    flatten_form_data,
    import_form_model_from_file,
)


def _get_form_schema(form_class) -> str:
    """Get a readable JSON schema description of the form."""
    schema = form_class.model_json_schema()
    return json.dumps(schema, indent=2)


def _fill_form_with_llm(form_class, client: ModelClient, model: str) -> dict:
    """Use LLM to fill out the form with realistic data.

    Args:
        form_class: Pydantic BaseModel class for the form.
        client: ModelClient instance.
        model: Model name for structured output.

    Returns:
        Filled form data as a dict.
    """
    class_name = form_class.__name__
    form_title = class_name.replace("_", " ").title()

    if form_class.__doc__:
        form_title = form_class.__doc__.strip().split("\n")[0]

    print(f"  Form class: {class_name}")
    print(f"  Form title: {form_title}")

    form_schema = _get_form_schema(form_class)

    print(f"  Filling form with {model}...")
    filled_form = client.chat.completions.parse(
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


def _classify_form_fields(filled_data: dict, client: ModelClient, model: str) -> dict[str, bool]:
    """Classify each field as open-ended or not using LLM.

    Args:
        filled_data: Filled form data dict.
        client: ModelClient instance.
        model: Model name for classification.

    Returns:
        Dict mapping field_id to is_open_ended boolean.
    """
    print(f"  Classifying fields as open/close-ended...")

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
                "example_value": value[:100] + "..." if len(value) > 100 else value,
            }
        )

    analysis = client.chat.completions.parse(
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

    classifications = {c.field_id: c.is_open_ended for c in analysis.classifications}
    open_count = sum(1 for v in classifications.values() if v)
    print(f"  Classified {len(classifications)} fields ({open_count} open-ended)")
    return classifications


def generate_groundtruth(
    form_model_path: Path,
    client: ModelClient,
    config: FormFillingConfig,
) -> dict:
    """Fill form with realistic data and classify fields.

    This is the main entry point for Stage 2.

    Args:
        form_model_path: Path to the form_model.py file.
        client: ModelClient instance.
        config: Pipeline configuration.

    Returns:
        Flat ground truth dict: {"field_id": {"answer": str, "is_open_ended": bool}}.
    """

    # Import the form model
    print("  Importing form module...")
    _, form_class = import_form_model_from_file(form_model_path)

    # Fill form with LLM
    print("  Filling form with LLM...")
    filled_data = _fill_form_with_llm(form_class, client, config.parsing_model)

    # Classify fields
    print("  Classifying fields...")
    classifications = _classify_form_fields(filled_data, client, config.validation_model)

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
