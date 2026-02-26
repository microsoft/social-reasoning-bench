"""Stage 1: Parse a form image into a Pydantic model.

Reads an image, extracts text via vision API, parses fields via multi-step
LLM prompting, and generates a validated Pydantic model file.
"""

import json
from typing import List, Literal, Optional

from pydantic import BaseModel, Field
from sage_llm import ModelClient

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


def _call_llm(client: ModelClient, system_prompt: str, user_message: str, model: str) -> str:
    """Helper to call LLM with system prompt and return content."""
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
        temperature=0,
    )
    return response.choices[0].message.content.strip()


def extract_text_from_image(image_path, client: ModelClient, config: FormFillingConfig) -> str:
    """Extract text from a form image using vision API.

    Args:
        image_path: Path to the form image.
        client: ModelClient instance.
        config: Pipeline configuration.

    Returns:
        Extracted text content.
    """
    from pathlib import Path

    image_path = Path(image_path)
    b64 = image_to_base64(image_path)
    mime = image_mime_type(image_path)

    response = client.chat.completions.create(
        model=config.vision_model,
        messages=[
            {
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

    raw_text = response.choices[0].message.content.strip()

    # Parse content between <form> tags if present
    import re

    match = re.search(r"<form>(.*?)</form>", raw_text, re.DOTALL | re.IGNORECASE)
    return match.group(1).strip() if match else raw_text


def parse_form_multistep(form_text: str, client: ModelClient, model: str) -> ParsedForm:
    """Parse a form using multi-step prompting.

    Args:
        form_text: Extracted form text.
        client: ModelClient instance.
        model: Model name to use.

    Returns:
        ParsedForm object.
    """
    # Step 1: Extract title
    print("  Step 1: Extracting title...")
    title = _call_llm(client, PARSE_STEP1_PROMPT, f"Form:\n{form_text}", model)
    print(f"    Title: {title}")

    # Step 2: Extract description
    print("  Step 2: Extracting description...")
    description = _call_llm(client, PARSE_STEP2_PROMPT, f"Form:\n{form_text}", model)
    if description == "NONE":
        description = None
    print(f"    Description: {description[:100] if description else 'None'}...")

    # Step 3a: Extract field labels
    print("  Step 3a: Extracting field labels...")
    labels_json = _call_llm(
        client,
        PARSE_STEP3A_PROMPT,
        f"Form:\n{form_text}\n\nOutput JSON array of field labels:",
        model,
    )
    labels_json = clean_json_response(labels_json)
    field_labels = json.loads(labels_json)
    print(f"    Found {len(field_labels)} field labels")

    # Step 3b: Extract field details
    print("  Step 3b: Extracting field details...")
    details_prompt = f"""Form text:
{form_text}

Field labels to create metadata for:
{json.dumps(field_labels, indent=2)}

Create a detailed field object for each label. Output JSON array of field objects:"""

    fields_json = _call_llm(client, PARSE_STEP3B_PROMPT, details_prompt, model)
    fields_json = clean_json_response(fields_json)
    fields_list = json.loads(fields_json)

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

    sections_json = _call_llm(client, PARSE_STEP4_PROMPT, sections_prompt, model)
    sections_json = clean_json_response(sections_json)
    sections_data = json.loads(sections_json)
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


def _generate_field_code(field: FormField, table_row_class: str | None = None) -> list[str]:
    """Generate code lines for a single Pydantic field."""
    lines = []

    if field.type == "boolean":
        type_annotation = "BooleanLike"
        comment = ""
    elif field.type == "select" and field.options:
        options_str = ", ".join([f'"{opt}"' for opt in field.options + ["N/A", ""]])
        type_annotation = f"Literal[{options_str}]"
        comment = ""
    elif field.type == "number":
        type_annotation = 'Union[float, Literal["N/A", ""]]'
        comment = ""
    elif field.type == "date":
        type_annotation = "str"
        comment = "  # YYYY-MM-DD format"
    elif field.type == "table":
        if table_row_class:
            type_annotation = f"List[{table_row_class}]"
            comment = "  # List of table rows"
        else:
            type_annotation = "str"
            comment = "  # Table data - describe each row"
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
    if field.required:
        lines.append("    ...,")
    else:
        lines.append('    default="",')

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
    lines.append("from typing import Literal, Optional, List, Union")
    lines.append("from pydantic import BaseModel, Field")
    lines.append("")
    lines.append("")

    # Constants
    lines.append(f"NA_HINT = '{NA_HINT}'")
    lines.append("BLANK_HINT = (")
    lines.append(f'    "{BLANK_HINT}"')
    lines.append(")")
    lines.append("")
    lines.append("# Type alias for boolean-like fields")
    lines.append('BooleanLike = Literal["true", "false", "N/A", ""]')
    lines.append("")
    lines.append("")

    # Table row classes
    table_row_classes = {}
    for section in parsed_form.sections:
        for field in section.fields:
            if field.type == "table" and field.table_columns:
                row_class_name = f"{field.id.title().replace('_', '')}Row"
                table_row_classes[field.id] = row_class_name

                lines.append(f"class {row_class_name}(BaseModel):")
                lines.append(f'    """Single row in {field.label}"""')
                lines.append("")

                for col in field.table_columns:
                    col_id = col.lower().replace(" ", "_").replace("/", "_").replace("-", "_")
                    col_id = "".join(c if c.isalnum() or c == "_" else "_" for c in col_id)
                    col_id = "_".join(part for part in col_id.split("_") if part)
                    if not col_id or not col_id[0].isalpha():
                        col_id = f"col_{col_id}"
                    if col_id in PYTHON_KEYWORDS:
                        col_id = f"{col_id}_"

                    lines.append(f"    {col_id}: str = Field(")
                    lines.append(f'        default="",')
                    lines.append(f'        description="{col.title()}"')
                    lines.append(f"    )")

                lines.append("")
                lines.append("")

    # Section classes if multiple sections
    section_classes = []
    if len(parsed_form.sections) > 1:
        for i, section in enumerate(parsed_form.sections):
            section_class_name = section.name
            section_class_name = (
                section_class_name.replace(" ", "")
                .replace("-", "")
                .replace("\u2013", "")
                .replace("/", "")
                .replace("\\", "")
            )
            section_class_name = "".join(c for c in section_class_name if c.isalnum())
            section_class_name = fix_class_name_starting_with_number(section_class_name)
            if not section_class_name or not section_class_name[0].isalpha():
                section_class_name = f"Section{i + 1}"
            section_classes.append((section_class_name, section))

            lines.append(f"class {section_class_name}(BaseModel):")
            if section.description:
                lines.append(f'    """{section.description}"""')
                lines.append("")

            for field in section.fields:
                table_row_class = table_row_classes.get(field.id)
                field_code = _generate_field_code(field, table_row_class)
                lines.extend([f"    {line}" for line in field_code])
                lines.append("")

            lines.append("")

    # Main form class
    lines.append(f"class {class_name}(BaseModel):")
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

    if len(parsed_form.sections) > 1:
        for section_class_name, section in section_classes:
            field_name = (
                section.name.lower().replace(" ", "_").replace("-", "_").replace("\u2013", "_")
            )
            field_name = "".join(c for c in field_name if c.isalnum() or c == "_")
            lines.append(f"    {field_name}: {section_class_name} = Field(")
            lines.append(f"        ...,")
            lines.append(f'        description="{section.name}"')
            lines.append(f"    )")
    else:
        for field in parsed_form.sections[0].fields:
            table_row_class = table_row_classes.get(field.id)
            field_code = _generate_field_code(field, table_row_class)
            lines.extend([f"    {line}" for line in field_code])
            lines.append("")

    return "\n".join(lines)


def validate_generated_code(code: str) -> bool:
    """Validate that generated Python code is syntactically correct."""
    import ast

    try:
        ast.parse(code)
        return True
    except SyntaxError as e:
        print(f"  Syntax error in generated code: Line {e.lineno}: {e.msg}")
        return False


def shorten_class_name_with_llm(long_name: str, client: ModelClient, model: str) -> str:
    """Use LLM to generate a shorter class name (max 64 chars)."""
    prompt = f"""Given this long class name: "{long_name}"

Generate a shorter, meaningful class name that:
1. Is maximum 64 characters
2. Still conveys the main purpose/identity
3. Uses PascalCase format
4. Is a valid Python class name

Return ONLY the shortened class name, nothing else."""

    response = client.chat.completions.create(
        model=model, messages=[{"role": "user", "content": prompt}], temperature=0
    )

    shortened = response.choices[0].message.content.strip()
    shortened = "".join(c for c in shortened if c.isalnum())[:64]
    return shortened


def parse_form_image(
    image_path, client: ModelClient, config: FormFillingConfig
) -> tuple[str, str, str, str]:
    """Parse a form image into extracted text and Pydantic model code.

    This is the main entry point for Stage 1.

    Args:
        image_path: Path to the form image.
        client: ModelClient instance.
        config: Pipeline configuration.

    Returns:
        Tuple of (extracted_text, form_model_code, class_name, form_title).
    """
    from pathlib import Path

    image_path = Path(image_path)

    # Step 1: Extract text from image
    print("  Extracting text from image...")
    extracted_text = extract_text_from_image(image_path, client, config)
    print(f"  Extracted {len(extracted_text)} characters")

    # Step 2: Parse form via multi-step prompting
    parsed_form = parse_form_multistep(extracted_text, client, config.parsing_model)

    # Step 3: Generate class name
    class_name = parsed_form.form_title
    class_name = "".join(word.capitalize() for word in class_name.split())
    class_name = "".join(c for c in class_name if c.isalnum())
    class_name = fix_class_name_starting_with_number(class_name)
    if not class_name:
        class_name = f"Form{extract_form_id(image_path)}"

    # Shorten if too long
    if len(class_name) > 64:
        print(f"  Class name too long ({len(class_name)} chars), shortening...")
        class_name = shorten_class_name_with_llm(class_name, client, config.parsing_model)

    # Step 4: Generate Pydantic code
    print("  Generating Pydantic code...")
    pydantic_code = generate_pydantic_code(parsed_form, class_name)

    # Step 5: Validate
    print("  Validating generated code...")
    is_valid = validate_generated_code(pydantic_code)
    if not is_valid:
        print("  Warning: Code validation failed, but continuing...")

    return extracted_text, pydantic_code, class_name, parsed_form.form_title


def extract_form_id(image_path) -> str:
    """Extract form ID from image path (local import to avoid circular)."""
    from pathlib import Path

    from sage_data_gen.form_filling.utils import extract_form_id as _extract_form_id

    return _extract_form_id(Path(image_path))
