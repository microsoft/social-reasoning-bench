"""Stage 1: Parse a form image into a Pydantic model.

Reads an image, extracts text via vision API, parses fields via multi-step
LLM prompting, and generates a validated Pydantic model file.
"""

from __future__ import annotations

import json
import re
from typing import TYPE_CHECKING, List, Literal, Optional, cast

if TYPE_CHECKING:
    from sage_benchmark.benchmarks.form_filling.types import FormSummary

from pydantic import BaseModel, Field
from sage_llm import SageMessage, SageModelClient

from sage_data_gen.form_filling.config import FormFillingConfig
from sage_data_gen.form_filling.models import FormField, FormSection, ParsedForm
from sage_data_gen.form_filling.prompts import (
    EXTRACT_TEXT_PROMPT,
    PARSE_STEP1_PROMPT,
    PARSE_STEP2_PROMPT,
    PARSE_STEP3A_PROMPT,
    PARSE_STEP3B_PROMPT,
    PARSE_STEP4_PROMPT,
)
from sage_data_gen.form_filling.utils import (
    PYTHON_KEYWORDS,
    clean_json_response,
    fix_class_name_starting_with_number,
    image_mime_type,
    image_to_base64,
)

# Constants for field hints (used in generated Pydantic code)
NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you "
    '(for example, it belongs to another person or office), leave it blank (empty string "").'
)


async def _call_llm(
    client: SageModelClient, system_prompt: str, user_message: str, model: str
) -> str:
    """Helper to call LLM with system prompt and return content.

    Args:
        client: SageModelClient instance.
        system_prompt: System message for the LLM.
        user_message: User message for the LLM.
        model: Model name to use.

    Returns:
        Stripped string content from the LLM response.
    """
    response = await client.acomplete(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
        temperature=0,
    )
    content = response.content
    assert isinstance(content, str)
    return content.strip()


async def extract_text_from_image(
    image_path, client: SageModelClient, config: FormFillingConfig
) -> str:
    """Extract text from a form image using vision API.

    Args:
        image_path: Path to the form image.
        client: SageModelClient instance.
        config: Pipeline configuration.

    Returns:
        Extracted text content.
    """
    from pathlib import Path

    image_path = Path(image_path)
    b64 = image_to_base64(image_path)
    mime = image_mime_type(image_path)

    response = await client.acomplete(
        model=config.vision_model,
        messages=[
            {  # type: ignore[list-item]  # multimodal content requires dict format
                "role": "user",
                "content": [
                    {"type": "text", "text": EXTRACT_TEXT_PROMPT},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:{mime};base64,{b64}"},
                    },
                ],
            }
        ],
    )

    raw_content = response.content
    assert isinstance(raw_content, str)
    raw_text = raw_content.strip()

    # Parse content between <form> tags if present
    import re

    match = re.search(r"<form>(.*?)</form>", raw_text, re.DOTALL | re.IGNORECASE)
    return match.group(1).strip() if match else raw_text


async def parse_form_multistep(form_text: str, client: SageModelClient, model: str) -> ParsedForm:
    """Parse a form using multi-step prompting.

    Args:
        form_text: Extracted form text.
        client: SageModelClient instance.
        model: Model name to use.

    Returns:
        ParsedForm object.
    """
    # Step 1: Extract title
    print("  Step 1: Extracting title...")
    title = await _call_llm(client, PARSE_STEP1_PROMPT, f"Form:\n{form_text}", model)
    print(f"    Title: {title}")

    # Step 2: Extract description
    print("  Step 2: Extracting description...")
    description = await _call_llm(client, PARSE_STEP2_PROMPT, f"Form:\n{form_text}", model)
    if description == "NONE":
        description = None
    print(f"    Description: {description[:100] if description else 'None'}...")

    # Step 3a: Extract field labels
    print("  Step 3a: Extracting field labels...")
    labels_json = await _call_llm(
        client,
        PARSE_STEP3A_PROMPT,
        f"Form:\n{form_text}\n\nOutput JSON array of field labels:",
        model,
    )
    labels_json = clean_json_response(labels_json)
    field_labels = json.loads(labels_json, strict=False)
    print(f"    Found {len(field_labels)} field labels")

    # Step 3b: Extract field details
    print("  Step 3b: Extracting field details...")
    details_prompt = f"""Form text:
{form_text}

Field labels to create metadata for:
{json.dumps(field_labels, indent=2)}

Create a detailed field object for each label. Output JSON array of field objects:"""

    fields_json = await _call_llm(client, PARSE_STEP3B_PROMPT, details_prompt, model)
    fields_json = clean_json_response(fields_json)
    fields_list = json.loads(fields_json, strict=False)

    # Sanitize field IDs
    for field in fields_list:
        original_id = field["id"]
        sanitized_id = (
            original_id.replace("/", "_")
            .replace("-", "_")
            .replace("(", "")
            .replace(")", "")
            .replace(" ", "_")
        )
        sanitized_id = "".join(c if c.isalnum() or c == "_" else "_" for c in sanitized_id)
        sanitized_id = "_".join(part for part in sanitized_id.split("_") if part)
        if not sanitized_id or not sanitized_id[0].isalpha():
            sanitized_id = f"field_{sanitized_id}" if sanitized_id else f"field_{len(fields_list)}"
        sanitized_id = sanitized_id.lower()
        if sanitized_id in PYTHON_KEYWORDS:
            sanitized_id = f"{sanitized_id}_"
        field["id"] = sanitized_id

    print(f"    Created {len(fields_list)} field objects")

    # Step 4: Group into sections
    print("  Step 4: Grouping into sections...")
    field_map = {f["id"]: f for f in fields_list}

    sections_prompt = f"""Form text:
{form_text}

Fields extracted (with IDs):
{json.dumps([{"id": f["id"], "label": f["label"]} for f in fields_list], indent=2)}

Organize these fields into logical sections based on the form structure.
For each section, provide a list of field IDs (not the full field objects).

Example output:
{{
  "sections": [
    {{
      "name": "Student Information",
      "description": "Basic student details",
      "field_ids": ["student_name", "date_of_birth", "grade"]
    }}
  ]
}}"""

    sections_json = await _call_llm(client, PARSE_STEP4_PROMPT, sections_prompt, model)
    sections_json = clean_json_response(sections_json)
    sections_data = json.loads(sections_json, strict=False)
    print(f"    Created {len(sections_data['sections'])} sections")

    # Build ParsedForm
    sections = []
    for section_data in sections_data["sections"]:
        if "field_ids" in section_data:
            field_ids = section_data["field_ids"]
            section_fields = [FormField(**field_map[fid]) for fid in field_ids if fid in field_map]
        elif "fields" in section_data:
            if section_data["fields"] and isinstance(section_data["fields"][0], dict):
                section_fields = [FormField(**f) for f in section_data["fields"]]
            else:
                section_fields = [
                    FormField(**field_map[fid])
                    for fid in section_data["fields"]
                    if fid in field_map
                ]
        else:
            section_fields = []

        sections.append(
            FormSection(
                name=section_data["name"],
                description=section_data.get("description"),
                fields=section_fields,
            )
        )

    return ParsedForm(form_title=title, form_description=description, sections=sections)


def _generate_field_code(field: FormField) -> list[str]:
    """Generate code lines for a single Pydantic field.

    Args:
        field: FormField describing the field metadata.

    Returns:
        List of Python code lines (without leading indentation for the class body).
    """
    lines = []

    if field.type == "boolean":
        type_annotation = "bool | None"
        comment = ""
    elif field.type == "select" and field.options:
        type_annotation = "str"
        comment = f"  # Options: {', '.join(field.options)}"
    elif field.type == "number":
        type_annotation = "float | None"
        comment = ""
    elif field.type == "date":
        type_annotation = "str"
        comment = "  # YYYY-MM-DD format"
    elif field.type == "table":
        cols = ", ".join(field.table_columns or [])
        type_annotation = "list[list[str]]"
        comment = f"  # Columns: {cols}" if cols else ""
    else:
        type_annotation = "str"
        comment = ""

    desc_parts = [field.help_text]
    if field.type in ["text", "textarea", "email", "phone", "address", "signature"]:
        desc_parts.append(NA_HINT)
        desc_parts.append(BLANK_HINT)
    description = " ".join(desc_parts).replace('"', r"\"")

    field_header = f"{field.id}: {type_annotation}"
    lines.append(f"{field_header} = Field(")
    # All fields are required (no defaults) so the JSON schema puts every
    # property in ``required`` — needed for OpenAI structured output.
    lines.append("    ...,")

    if len(description) < 80:
        lines.append(f'    description="{description}"')
    else:
        lines.append("    description=(")
        words = description.split()
        current_line = '        "'
        for word in words:
            if len(current_line) + len(word) + 1 > 88:
                lines.append(current_line + '"')
                current_line = '        "' + word + " "
            else:
                current_line += word + " "
        lines.append(current_line.rstrip() + '"')
        lines.append("    )")

    if comment:
        lines.append(f"){comment}")
    else:
        lines.append(")")

    return lines


def generate_pydantic_code(parsed_form: ParsedForm, class_name: str = "GeneratedForm") -> str:
    """Generate Pydantic model code from parsed form.

    Args:
        parsed_form: ParsedForm object.
        class_name: Name for the generated class.

    Returns:
        Python code as string.
    """
    lines = []

    # Imports
    lines.append("from pydantic import BaseModel, ConfigDict, Field")
    lines.append("")
    lines.append("")

    # Constants
    lines.append(f"NA_HINT = '{NA_HINT}'")
    lines.append("BLANK_HINT = (")
    lines.append(f'    "{BLANK_HINT}"')
    lines.append(")")
    lines.append("")
    lines.append("")

    # Single flat form class — all fields at top level, no nested section models
    lines.append(f"class {class_name}(BaseModel):")
    lines.append('    model_config = ConfigDict(extra="forbid")')
    if parsed_form.form_description:
        lines.append(f'    """')
        lines.append(f"    {parsed_form.form_title}")
        lines.append("")
        desc_lines = parsed_form.form_description.split("\n")
        for desc_line in desc_lines:
            if desc_line.strip():
                lines.append(f"    {desc_line}")
        lines.append('    """')
    else:
        lines.append(f'    """{parsed_form.form_title}"""')
    lines.append("")

    seen_ids: set[str] = set()
    for section in parsed_form.sections:
        # Build section prefix from section name
        section_prefix = ""
        if section.name and len(parsed_form.sections) > 1:
            section_prefix = (
                section.name.lower().replace(" ", "_").replace("-", "_").replace("\u2013", "_")
            )
            section_prefix = "".join(c for c in section_prefix if c.isalnum() or c == "_")
            section_prefix = "_".join(part for part in section_prefix.split("_") if part)

        for field in section.fields:
            # Prefix field ID with section name to avoid collisions
            if section_prefix:
                original_id = field.id
                field = field.model_copy(update={"id": f"{section_prefix}_{original_id}"})
            # Deduplicate field IDs
            base_id = field.id
            counter = 2
            while field.id in seen_ids:
                field = field.model_copy(update={"id": f"{base_id}_{counter}"})
                counter += 1
            seen_ids.add(field.id)

            field_code = _generate_field_code(field)
            lines.extend([f"    {line}" for line in field_code])
            lines.append("")

    return "\n".join(lines)


def validate_generated_code(code: str) -> bool:
    """Validate that generated Python code is syntactically correct.

    Args:
        code: Python source code string.

    Returns:
        *True* if the code parses without syntax errors.
    """
    import ast

    try:
        ast.parse(code)
        return True
    except SyntaxError as e:
        print(f"  Syntax error in generated code: Line {e.lineno}: {e.msg}")
        return False


async def shorten_class_name_with_llm(long_name: str, client: SageModelClient, model: str) -> str:
    """Use LLM to generate a shorter class name (max 64 chars).

    Args:
        long_name: The overly long class name to shorten.
        client: SageModelClient instance.
        model: Model name to use.

    Returns:
        Shortened PascalCase class name (max 64 characters).
    """
    prompt = f"""Given this long class name: "{long_name}"

Generate a shorter, meaningful class name that:
1. Is maximum 64 characters
2. Still conveys the main purpose/identity
3. Uses PascalCase format
4. Is a valid Python class name

Return ONLY the shortened class name, nothing else."""

    response = await client.acomplete(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )

    raw = response.content
    assert isinstance(raw, str)
    shortened = raw.strip()
    shortened = "".join(c for c in shortened if c.isalnum())[:64]
    return shortened


GENERATE_MODEL_PROMPT = """\
You are generating a Pydantic model for a form. Given the OCR text of a blank form \
and a summary of its purpose and audience, produce a single flat BaseModel class \
that captures every fillable field.

## Form Summary
{form_summary}

## Rules

1. **One flat class** — no nested models, no inheritance beyond BaseModel.
2. **Simple types only:**
   - `str` for text, dates (YYYY-MM-DD), select/dropdown, addresses, phone, email, SSN
   - `bool | None` for checkboxes and yes/no fields
   - `float | None` for numeric fields
   - `list[list[str]]` for table fields (describe columns in the description)
3. **Field IDs** must be valid Python snake_case identifiers. If the form has sections, \
prefix field IDs with the section name (e.g. `contact_info_phone`).
4. **Descriptions** should be a short phrase (under 60 chars), not a full sentence.
5. All fields use `Field(...)` (required, no defaults).
6. For text-like fields, append this to the description: \
'.If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
7. The class docstring MUST include the form title on the first line, followed by \
a natural-language paragraph describing what the form is for, who submits it, \
who reads/evaluates it, and what decisions are made based on it. Write it like \
you're explaining the form to a colleague, not like a database entry.
8. Include `model_config = ConfigDict(extra="forbid")` after the docstring.
9. Class name MUST be PascalCase, MAXIMUM 64 characters, derived from the form title. Abbreviate if needed.

## Output

Return ONLY valid Python code. No markdown fences, no explanation. The code must start with imports.

Example output:
```
from pydantic import BaseModel, ConfigDict, Field


class ScholarshipApp(BaseModel):
    \"\"\"National Merit Scholarship Application

    High school seniors submit this application to be considered for merit-based
    financial aid. A university scholarship committee reviews each applicant's
    academic record, personal essay, and financial circumstances to decide who
    receives awards covering tuition, books, and living expenses.
    \"\"\"

    model_config = ConfigDict(extra="forbid")

    full_name: str = Field(..., description='Applicant full name. If you cannot fill this, write "N/A".')
    gpa: float | None = Field(..., description="Cumulative GPA")
    essay_goals: str = Field(..., description='Career goals essay. If you cannot fill this, write "N/A".')
    has_financial_need: bool | None = Field(..., description="Demonstrates financial need?")
```"""


async def generate_form_model(
    extracted_text: str,
    client: SageModelClient,
    config: FormFillingConfig,
    form_id: str = "",
    form_summary: "FormSummary | None" = None,
) -> "tuple[str, str, str, FormSummary]":
    """Generate Pydantic model code from extracted form text.

    First extracts a FormSummary (purpose + recipient) if not provided,
    then generates the Pydantic model with the summary as docstring context.

    Args:
        extracted_text: OCR text from the form image.
        client: SageModelClient instance.
        config: Pipeline configuration.
        form_id: Form identifier (fallback for class name).
        form_summary: Optional FormSummary (purpose + recipient). If None,
            it will be extracted from the text.

    Returns:
        Tuple of (form_model_code, class_name, form_title, form_summary).
    """
    from sage_data_gen.form_filling.models import FormSummary as _FormSummaryModel
    from sage_data_gen.form_filling.prompts import FORM_SUMMARY_PROMPT

    # Step 1: Extract form summary (purpose + recipient) if not provided
    if form_summary is None:
        print("  Extracting form summary...")
        parsed_summary = await client.aparse(
            model=config.parsing_model,
            messages=[
                {
                    "role": "system",
                    "content": "You are analyzing a form to understand its context and audience.",
                },
                {
                    "role": "user",
                    "content": FORM_SUMMARY_PROMPT.format(form_content=extracted_text),
                },
            ],
            response_format=_FormSummaryModel,
            temperature=0.3,
        )
        form_summary = cast("FormSummary", parsed_summary)
        print(f"  Purpose: {form_summary.form_purpose[:80]}...")
        print(f"  Recipient: {form_summary.intended_recipient[:80]}...")

    # Step 2: Generate Pydantic model with summary as context
    summary_text = (
        f"Purpose: {form_summary.form_purpose}\n"
        f"Intended Recipient: {form_summary.intended_recipient}"
    )
    print("  Generating Pydantic model from OCR text...")
    gen_messages: list[SageMessage] = [
        {"role": "system", "content": GENERATE_MODEL_PROMPT.format(form_summary=summary_text)},
        {"role": "user", "content": f"Form text:\n\n{extracted_text}"},
    ]

    max_retries = 5
    for attempt in range(max_retries):
        response = await client.acomplete(
            model=config.parsing_model,
            messages=gen_messages,
            temperature=0,
        )

        raw = response.content
        assert isinstance(raw, str)
        code = raw.strip()

        # Strip markdown fences if present
        if code.startswith("```"):
            code = code.split("\n", 1)[1] if "\n" in code else code[3:]
        if code.endswith("```"):
            code = code.rsplit("```", 1)[0]
        code = code.strip()

        # Validate
        errors = []
        if not validate_generated_code(code):
            errors.append("Code has syntax errors.")

        classes = re.findall(r"^class (\w+)\(BaseModel\):", code, re.MULTILINE)
        if not classes:
            errors.append("No BaseModel class found.")
        elif len(classes[-1]) > 64:
            errors.append(
                f"Class name '{classes[-1]}' is {len(classes[-1])} chars — max 64. Abbreviate it."
            )

        if not errors:
            break

        # Retry: feed errors back to the LLM
        error_msg = "Fix these issues and regenerate:\n" + "\n".join(f"- {e}" for e in errors)
        print(f"  Attempt {attempt + 1}: {error_msg}")
        gen_messages.append({"role": "assistant", "content": raw})
        gen_messages.append({"role": "user", "content": error_msg})
    else:
        print(f"  Warning: Could not fix issues after {max_retries} attempts, using last output")

    # Extract class name
    classes = re.findall(r"^class (\w+)\(BaseModel\):", code, re.MULTILINE)
    class_name = classes[-1] if classes else f"Form{form_id}"

    # Extract form title from docstring
    form_title = class_name
    docstring_match = re.search(r'"""(.+?)"""', code, re.DOTALL)
    if docstring_match:
        form_title = docstring_match.group(1).strip().split("\n")[0]

    return code, class_name, form_title, form_summary


async def parse_form_image(
    image_path, client: SageModelClient, config: FormFillingConfig
) -> tuple[str, str, str, str]:
    """Parse a form image into extracted text and Pydantic model code.

    This is the main entry point for Stage 1. Prefer using
    extract_text_from_image() + generate_form_model() separately
    for independent caching.

    Args:
        image_path: Path to the form image (PNG/JPEG).
        client: SageModelClient instance.
        config: Pipeline configuration.

    Returns:
        Tuple of (extracted_text, form_model_code, class_name, form_title).
    """
    from pathlib import Path

    image_path = Path(image_path)

    print("  Extracting text from image...")
    extracted_text = await extract_text_from_image(image_path, client, config)
    print(f"  Extracted {len(extracted_text)} characters")

    form_model_code, class_name, form_title, _form_summary = await generate_form_model(
        extracted_text, client, config, form_id=extract_form_id(image_path)
    )

    return extracted_text, form_model_code, class_name, form_title


def extract_form_id(image_path) -> str:
    """Extract form ID from image path (local import to avoid circular).

    Args:
        image_path: Path to the form image file.

    Returns:
        String form ID extracted from the filename.
    """
    from pathlib import Path

    from sage_data_gen.form_filling.utils import extract_form_id as _extract_form_id

    return _extract_form_id(Path(image_path))
