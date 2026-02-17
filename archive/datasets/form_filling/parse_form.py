"""
Multi-step LLM-based form parsing to Pydantic models.

This script uses a multi-step approach:
1. Extract form title
2. Extract form description/purpose (for docstring)
3. Extract all fields with type and required status
4. Generate Pydantic model with proper field annotations
"""

import json
import os
from typing import Any, Dict, List, Literal, Optional

import openai
from pydantic import BaseModel, Field

# Constants for field hints
NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you "
    '(for example, it belongs to another person or office), leave it blank (empty string "").'
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]

# Python reserved keywords that cannot be used as field names
PYTHON_KEYWORDS = {
    "False",
    "None",
    "True",
    "and",
    "as",
    "assert",
    "async",
    "await",
    "break",
    "class",
    "continue",
    "def",
    "del",
    "elif",
    "else",
    "except",
    "finally",
    "for",
    "from",
    "global",
    "if",
    "import",
    "in",
    "is",
    "lambda",
    "nonlocal",
    "not",
    "or",
    "pass",
    "raise",
    "return",
    "try",
    "while",
    "with",
    "yield",
}


# Pydantic models for parsing steps
class FormField(BaseModel):
    """Represents a single field in a form."""

    id: str
    label: str
    type: str  # "text", "date", "signature", "checkbox", "boolean", "select", "number", "email", "phone", "textarea", "table", etc.
    required: bool
    options: List[str]  # For select/checkbox fields
    help_text: str
    raw_snippet: str
    table_columns: Optional[List[str]] = None  # For table fields: list of column names


class FormSection(BaseModel):
    """Represents a section containing multiple fields."""

    name: str
    description: Optional[str] = None
    fields: List[FormField]


class ParsedForm(BaseModel):
    """Represents a parsed form with all metadata."""

    form_title: str
    form_description: Optional[str] = None
    sections: List[FormSection]


# Step 1: Extract form title
STEP1_PROMPT = """You are extracting the title from a blank form.

Your task:
- Read the form text and identify the main title/name of the form
- This is typically at the top of the form in all caps or bold
- Return ONLY the title as plain text, no extra formatting

Examples:
Form: "TEXAS DIVISION OF EMERGENCY MANAGEMENT\nSTATE RACES APPLICATION\n\nAttach a current copy..."
Output: TEXAS DIVISION OF EMERGENCY MANAGEMENT\nSTATE RACES APPLICATION

Form: "ACTION SHEET\n\n| DATE | DETAILS..."
Output: ACTION SHEET

Form: "Centerville City Schools\nEMERGENCY MEDICAL AUTHORIZATION FORM..."
Output: Centerville City Schools\nEMERGENCY MEDICAL AUTHORIZATION FORM

Form: "Attachment D\nCENTERVILLE CITY SCHOOLS\nHome Language Survey\n\nParents: We ask the questions below to make sure your child receives the education services he or she needs. The answers to the questions in Section A will tell your child's school staff if they need to check your child's proficiency in English. This makes sure your child has every opportunity to succeed in school. The answers to Section B will help school staff communicate with you in the language you prefer..."
Output: Attachment D\nCENTERVILLE CITY SCHOOLS\nHome Language Survey
"""

# Step 2: Extract form description
STEP2_PROMPT = """You are extracting the purpose/description from a blank form.

Your task:
- Read the form text and identify any explanatory text, purpose statements, or instructions at the beginning
- This will become the docstring for the Pydantic model
- Include all relevant context that helps understand what the form is for
- Return ONLY the description text, or '' if there is no clear description

Examples:
Form: "Home Language Survey\n\nParents: We ask the questions below to make sure your child receives..."
Output: Parents: We ask the questions below to make sure your child receives the education services he or she needs. The answers to the questions in Section A will tell your child's school staff if they need to check your child's proficiency in English.

Form: "ACTION SHEET\n\n| DATE | DETAILS..."
Output: ''

Form: "EMERGENCY MEDICAL AUTHORIZATION FORM\n\nPurpose: To enable parents and guardians to authorize..."
Output: Purpose: To enable parents and guardians to authorize the provision of emergency treatment for children who become ill or injured while under school authority, when parents or guardians cannot be reached."""


# Step 3a: Extract field names/labels
STEP3A_PROMPT = """You are identifying fillable fields in a blank form.

Your task:
- Find every place where a human would write or fill in information
- Return a simple list of field labels/names
- Include ALL fields: text inputs, checkboxes, dropdowns, signature lines, etc.
- For table rows, list each column as a separate field

Rules:
1. Look for underscores (___), blank lines, checkboxes [ ], dropdown indicators
2. Extract the label text that describes what goes in each field
3. Return ONLY a JSON array of strings (the labels)

Output format: JSON array of strings

Example:
Input: "Name: _____________  Date of Birth: __________\n\nEmail: ________________\n\n[ ] I agree to terms"
Output:
["Name", "Date of Birth", "Email", "I agree to terms"]

Example with table:
Input: "| DATE | PROBLEM | ACTION | INITIALS |\n|      |         |        |          |"
Output:
["DATE", "PROBLEM", "ACTION", "INITIALS"]"""


# Step 3b: Extract field details
STEP3B_PROMPT = """You are creating detailed field metadata for a form.

Your task:
- Given a list of field labels and the original form text
- For each field, create a detailed field object with:
  * id: snake_case identifier (MUST be valid Python identifier)
  * label: The original label from the list
  * type: Field type (see list below)
  * required: Is this field required? (true/false)
  * options: List of options for select/checkbox fields (empty array otherwise)
  * help_text: Brief description of what goes here
  * raw_snippet: Exact text from form showing this field
  * table_columns: For table fields ONLY - array of column names (null otherwise)

IMPORTANT: Field IDs must be valid Python identifiers:
- Only use lowercase letters, numbers, and underscores
- Must start with a letter
- Replace spaces with underscores
- Remove special characters like /, -, (, ), etc.
- Examples: "DRO/DC" -> "dro_dc", "Phone (Home)" -> "phone_home"

Field types:
- "text": General text input
- "textarea": Long text input
- "date": Date fields
- "signature": Signature fields
- "boolean": Yes/No or checkbox fields
- "select": Multiple choice with specific options
- "number": Numeric input
- "email": Email address
- "phone": Phone number
- "ssn": Social security number
- "address": Address fields
- "state": US state
- "zip": Zip code
- "table": Repeating table rows (if multiple table columns, create ONE table field)

Rules:
1. Infer field type from the label and context
2. Yes/No questions or checkboxes are "boolean" type
3. If a field appears essential or labeled "required", mark required=true
4. For tables with multiple columns, create a SINGLE "table" field (not one per column)
5. For table fields, populate table_columns with the list of column names
6. Extract the actual text snippet showing the field from the form

Output format: JSON array of field objects

Example 1 (simple fields):
Input labels: ["Name", "Date of Birth", "Email"]
Form text: "Name: _____________  Date of Birth: __________\n\nEmail: ________________"
Output:
[
  {
    "id": "name",
    "label": "Name",
    "type": "text",
    "required": true,
    "options": [],
    "help_text": "Full name",
    "raw_snippet": "Name: _____________",
    "table_columns": null
  },
  {
    "id": "date_of_birth",
    "label": "Date of Birth",
    "type": "date",
    "required": true,
    "options": [],
    "help_text": "Date of birth",
    "raw_snippet": "Date of Birth: __________",
    "table_columns": null
  },
  {
    "id": "email",
    "label": "Email",
    "type": "email",
    "required": true,
    "options": [],
    "help_text": "Email address",
    "raw_snippet": "Email: ________________",
    "table_columns": null
  }
]

Example 2 (table field):
Input labels: ["Action Log Table"]
Form text: "| DATE | PROBLEM | ACTION | INITIALS |\n|______|_________|________|__________|"
Output:
[
  {
    "id": "action_log_table",
    "label": "Action Log Table",
    "type": "table",
    "required": false,
    "options": [],
    "help_text": "Table to record date, problem, action taken, and initials",
    "raw_snippet": "| DATE | PROBLEM | ACTION | INITIALS |",
    "table_columns": ["date", "problem", "action", "initials"]
  }
]"""


# Step 4: Group into sections
STEP4_PROMPT = """You are organizing form fields into logical sections.

Your task:
- Given a list of field IDs/labels and the original form text
- Group fields into sections that make logical sense
- Sections should be based on headers in the form (e.g., "Section A", "Part I", "STUDENT INFORMATION")
- If there are no clear sections, create one section called "Main"
- Output a list of field IDs for each section (not the full field objects)

Output format: JSON object with sections array containing field_ids

Example:
{
  "sections": [
    {
      "name": "Student Information",
      "description": "Basic information about the student",
      "field_ids": ["student_name", "date_of_birth", "grade"]
    },
    {
      "name": "Emergency Contacts",
      "description": "People to contact in case of emergency",
      "field_ids": ["emergency_contact_1", "emergency_contact_2"]
    }
  ]
}"""


def call_llm(
    client: openai.OpenAI, system_prompt: str, user_message: str, model: str = "gpt-5.1"
) -> str:
    """Helper to call LLM with system prompt."""
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
        temperature=0,
    )
    return response.choices[0].message.content.strip()


def parse_form_multistep(
    form_text: str, client: openai.OpenAI, model: str = "gpt-5.1"
) -> ParsedForm:
    """
    Parse a form using multi-step prompting.

    Args:
        form_text: Raw form text
        client: OpenAI client
        model: Model to use

    Returns:
        ParsedForm object
    """

    # Step 1: Extract title
    print("  Step 1: Extracting title...")
    title = call_llm(client, STEP1_PROMPT, f"Form:\n{form_text}", model)
    print(f"    → Title: {title}")

    # Step 2: Extract description
    print("  Step 2: Extracting description...")
    description = call_llm(client, STEP2_PROMPT, f"Form:\n{form_text}", model)
    if description == "NONE":
        description = None
    print(f"    → Description: {description[:100] if description else 'None'}...")

    # Step 3a: Extract field labels
    print("  Step 3a: Extracting field labels...")
    labels_json = call_llm(
        client, STEP3A_PROMPT, f"Form:\n{form_text}\n\nOutput JSON array of field labels:", model
    )

    # Clean JSON if wrapped in code blocks
    if labels_json.startswith("```"):
        lines = labels_json.split("\n")
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        labels_json = "\n".join(lines)

    field_labels = json.loads(labels_json)
    print(f"    → Found {len(field_labels)} field labels")

    # Step 3b: Extract field details
    print("  Step 3b: Extracting field details...")
    details_prompt = f"""Form text:
{form_text}

Field labels to create metadata for:
{json.dumps(field_labels, indent=2)}

Create a detailed field object for each label. Output JSON array of field objects:"""

    fields_json = call_llm(client, STEP3B_PROMPT, details_prompt, model)

    # Clean JSON if wrapped in code blocks
    if fields_json.startswith("```"):
        lines = fields_json.split("\n")
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        fields_json = "\n".join(lines)

    fields_list = json.loads(fields_json)

    # Sanitize field IDs to ensure they're valid Python identifiers
    for field in fields_list:
        original_id = field["id"]
        # Remove special characters and replace with underscores
        sanitized_id = (
            original_id.replace("/", "_")
            .replace("-", "_")
            .replace("(", "")
            .replace(")", "")
            .replace(" ", "_")
        )
        # Remove any remaining non-alphanumeric/underscore characters
        sanitized_id = "".join(c if c.isalnum() or c == "_" else "_" for c in sanitized_id)
        # Remove leading/trailing underscores and collapse multiple underscores
        sanitized_id = "_".join(part for part in sanitized_id.split("_") if part)
        # Ensure it starts with a letter (prepend 'field_' if it doesn't)
        if not sanitized_id or not sanitized_id[0].isalpha():
            sanitized_id = f"field_{sanitized_id}" if sanitized_id else f"field_{len(fields_list)}"
        # Convert to lowercase
        sanitized_id = sanitized_id.lower()

        # Check if it's a Python keyword and append underscore if needed
        if sanitized_id in PYTHON_KEYWORDS:
            sanitized_id = f"{sanitized_id}_"
            print(f"    ⚠ Field ID is Python keyword: '{original_id}' -> '{sanitized_id}'")

        if original_id != sanitized_id:
            print(f"    ⚠ Sanitized field ID: '{original_id}' -> '{sanitized_id}'")

        field["id"] = sanitized_id

    print(f"    → Created {len(fields_list)} field objects")

    # Step 4: Group into sections
    print("  Step 4: Grouping into sections...")

    # Create a mapping of field IDs to field objects for lookup
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
    }},
    {{
      "name": "Contact Information",
      "description": "Emergency contacts",
      "field_ids": ["phone", "email", "address"]
    }}
  ]
}}"""

    sections_json = call_llm(client, STEP4_PROMPT, sections_prompt, model)

    # Clean JSON
    if sections_json.startswith("```"):
        lines = sections_json.split("\n")
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        sections_json = "\n".join(lines)

    sections_data = json.loads(sections_json)
    print(f"    → Created {len(sections_data['sections'])} sections")

    # Build ParsedForm
    sections = []
    for section_data in sections_data["sections"]:
        # Handle both field_ids and fields keys for backward compatibility
        if "field_ids" in section_data:
            field_ids = section_data["field_ids"]
            section_fields = [FormField(**field_map[fid]) for fid in field_ids if fid in field_map]
        elif "fields" in section_data:
            # If fields are already full objects
            if section_data["fields"] and isinstance(section_data["fields"][0], dict):
                section_fields = [FormField(**f) for f in section_data["fields"]]
            # If fields are just IDs
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


def fix_class_name_starting_with_number(class_name: str) -> str:
    """
    Fix class names that start with numbers by moving digits to the end.

    Args:
        class_name: Original class name that may start with numbers

    Returns:
        Fixed class name that is a valid Python identifier

    Examples:
        "123Application" -> "Application123"
        "2025TaxForm" -> "TaxForm2025"
        "ValidName" -> "ValidName"
    """
    if not class_name or not class_name[0].isdigit():
        return class_name

    # Separate leading digits from the rest
    leading_digits = ""
    rest = ""

    for char in class_name:
        if char.isdigit() and rest == "":
            leading_digits += char
        else:
            rest += char

    # If rest is empty (all digits), prepend "Form"
    if not rest:
        return f"Form{leading_digits}"

    # Move leading digits to the end
    return f"{rest}{leading_digits}"


def generate_pydantic_code(parsed_form: ParsedForm, class_name: str = "GeneratedForm") -> str:
    """
    Generate Pydantic model code from parsed form.

    Args:
        parsed_form: ParsedForm object
        class_name: Name for the generated class

    Returns:
        Python code as string
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

    # First, generate table row classes for any table fields
    table_row_classes = {}  # Maps field_id to row class name
    for section in parsed_form.sections:
        for field in section.fields:
            if field.type == "table" and field.table_columns:
                # Create a row class for this table
                row_class_name = f"{field.id.title().replace('_', '')}Row"
                table_row_classes[field.id] = row_class_name

                lines.append(f"class {row_class_name}(BaseModel):")
                lines.append(f'    """Single row in {field.label}"""')
                lines.append("")

                # Generate fields for each column
                for col in field.table_columns:
                    # Sanitize column name
                    col_id = col.lower().replace(" ", "_").replace("/", "_").replace("-", "_")
                    col_id = "".join(c if c.isalnum() or c == "_" else "_" for c in col_id)
                    col_id = "_".join(part for part in col_id.split("_") if part)
                    if not col_id or not col_id[0].isalpha():
                        col_id = f"col_{col_id}"

                    # Check for Python keywords
                    if col_id in PYTHON_KEYWORDS:
                        col_id = f"{col_id}_"

                    lines.append(f"    {col_id}: str = Field(")
                    lines.append(f'        default="",')
                    lines.append(f'        description="{col.title()}"')
                    lines.append(f"    )")

                lines.append("")
                lines.append("")

    # Generate section classes if multiple sections
    section_classes = []
    if len(parsed_form.sections) > 1:
        for i, section in enumerate(parsed_form.sections):
            # Sanitize section name to valid Python class name
            section_class_name = section.name
            # Remove or replace invalid characters
            section_class_name = (
                section_class_name.replace(" ", "")
                .replace("-", "")
                .replace("–", "")
                .replace("/", "")
                .replace("\\", "")
            )
            # Remove any remaining non-alphanumeric characters
            section_class_name = "".join(c for c in section_class_name if c.isalnum())
            # Fix if it starts with a number
            section_class_name = fix_class_name_starting_with_number(section_class_name)
            # Ensure we have a valid name
            if not section_class_name or not section_class_name[0].isalpha():
                section_class_name = f"Section{i + 1}"
            section_classes.append((section_class_name, section))

            lines.append(f"class {section_class_name}(BaseModel):")

            # Section docstring
            if section.description:
                lines.append(f'    """{section.description}"""')
                lines.append("")

            # Fields
            for field in section.fields:
                # Pass table row class if this is a table field
                table_row_class = table_row_classes.get(field.id)
                field_code = generate_field_code(field, table_row_class)
                lines.extend([f"    {line}" for line in field_code])
                lines.append("")

            lines.append("")

    # Main form class
    lines.append(f"class {class_name}(BaseModel):")

    # Docstring with title and description
    if parsed_form.form_description:
        lines.append(f'    """')
        lines.append(f"    {parsed_form.form_title}")
        lines.append("")
        # Split description into lines
        desc_lines = parsed_form.form_description.split("\n")
        for desc_line in desc_lines:
            if desc_line.strip():
                lines.append(f"    {desc_line}")
        lines.append('    """')
    else:
        lines.append(f'    """{parsed_form.form_title}"""')
    lines.append("")

    # Fields or section references
    if len(parsed_form.sections) > 1:
        # Use section classes
        for section_class_name, section in section_classes:
            field_name = section.name.lower().replace(" ", "_").replace("-", "_").replace("–", "_")
            field_name = "".join(c for c in field_name if c.isalnum() or c == "_")
            lines.append(f"    {field_name}: {section_class_name} = Field(")
            lines.append(f"        ...,")
            lines.append(f'        description="{section.name}"')
            lines.append(f"    )")
    else:
        # Single section - inline fields
        for field in parsed_form.sections[0].fields:
            # Pass table row class if this is a table field
            table_row_class = table_row_classes.get(field.id)
            field_code = generate_field_code(field, table_row_class)
            lines.extend([f"    {line}" for line in field_code])
            lines.append("")

    return "\n".join(lines)


def generate_field_code(field: FormField, table_row_class: str = None) -> List[str]:
    """Generate code lines for a single field.

    Args:
        field: FormField object
        table_row_class: If this field is a table, name of the row class to use
    """
    lines = []

    # Determine Python type annotation
    # Note: Don't add comments in type annotations as they break syntax
    if field.type == "boolean":
        type_annotation = "BooleanLike"
        comment = ""
    elif field.type == "select" and field.options:
        # Create literal with options + N/A + blank
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
        # Use List of row class if provided, otherwise str
        if table_row_class:
            type_annotation = f"List[{table_row_class}]"
            comment = "  # List of table rows"
        else:
            type_annotation = "str"
            comment = "  # Table data - describe each row"
    else:
        # text, textarea, email, phone, signature, etc.
        type_annotation = "str"
        comment = ""

    # Build description
    desc_parts = [field.help_text]

    # Add hints for text/textarea fields
    if field.type in ["text", "textarea", "email", "phone", "address", "signature"]:
        desc_parts.append(NA_HINT)
        desc_parts.append(BLANK_HINT)

    description = " ".join(desc_parts)

    # Escape quotes in description
    description = description.replace('"', r"\"")

    # Field definition with comment AFTER Field()
    field_header = f"{field.id}: {type_annotation}"

    lines.append(f"{field_header} = Field(")
    if field.required:
        lines.append("    ...,")
    else:
        lines.append('    default="",')

    # Add description (handle long descriptions)
    if len(description) < 80:
        lines.append(f'    description="{description}"')
    else:
        lines.append("    description=(")
        # Split into words and wrap
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

    # Add closing paren with comment
    if comment:
        lines.append(f"){comment}")
    else:
        lines.append(")")

    return lines


def validate_generated_code(code: str, form_id: int) -> bool:
    """
    Validate that the generated Python code is syntactically correct.

    Args:
        code: Generated Python code
        form_id: Form ID for error reporting

    Returns:
        True if valid, False otherwise
    """
    import ast
    import re

    try:
        # Try to parse the code as valid Python
        ast.parse(code)

        # Check for common issues
        issues = []

        # Check for unescaped quotes in strings
        # Look for patterns like description="...text with "quotes"..."
        string_pattern = r'description=\s*(?:\()?["\']([^"\']*)["\']'
        matches = re.finditer(string_pattern, code, re.MULTILINE | re.DOTALL)
        for match in matches:
            content = match.group(1)
            # Check if there are unescaped quotes
            if '"' in content and r"\"" not in content:
                issues.append(f"Unescaped quotes in description: {content[:50]}...")

        # Check for comments in type annotations
        # Pattern: field_name: Type # comment = Field(
        type_annotation_pattern = r"^\s*\w+:\s+[\w\[\],\s\"]+\s+#[^=]+=\s+Field\("
        if re.search(type_annotation_pattern, code, re.MULTILINE):
            issues.append("Comment found in type annotation (breaks syntax)")

        # Check for invalid Python identifiers in field/class names
        # Look for class names and field names
        class_pattern = r"^class\s+([^\(]+)\("
        field_pattern = r"^\s*([a-zA-Z_][a-zA-Z0-9_]*):\s+"

        for match in re.finditer(class_pattern, code, re.MULTILINE):
            class_name = match.group(1).strip()
            # Check if valid identifier
            if not class_name.isidentifier():
                issues.append(f"Invalid class name: '{class_name}' (contains special characters)")

        for match in re.finditer(field_pattern, code, re.MULTILINE):
            field_name = match.group(1)
            # This regex already ensures valid format, but double-check
            if not field_name.isidentifier():
                issues.append(f"Invalid field name: '{field_name}'")

        if issues:
            print(f"  ⚠ Validation warnings for form {form_id}:")
            for issue in issues:
                print(f"    - {issue}")
            return False

        return True

    except SyntaxError as e:
        print(f"  ✗ Syntax error in generated code for form {form_id}:")
        print(f"    Line {e.lineno}: {e.msg}")
        print(f"    {e.text}")
        return False
    except Exception as e:
        print(f"  ✗ Validation error for form {form_id}: {e}")
        return False


def shorten_class_name_with_llm(long_name: str, client: openai.OpenAI) -> str:
    """Use GPT-4o to generate a shorter class name (max 64 chars)."""
    prompt = f"""Given this long class name: "{long_name}"

Generate a shorter, meaningful class name that:
1. Is maximum 64 characters
2. Still conveys the main purpose/identity
3. Uses PascalCase format
4. Is a valid Python class name

Return ONLY the shortened class name, nothing else."""

    response = client.chat.completions.create(
        model="gpt-4o", messages=[{"role": "user", "content": prompt}], temperature=0
    )

    shortened = response.choices[0].message.content.strip()
    # Ensure it's valid and within limit
    shortened = "".join(c for c in shortened if c.isalnum())[:64]
    return shortened


def process_common_forms(
    input_file: str,
    output_dir: str,
    limit: Optional[int] = None,
    model: str = "gpt-5.1",
    validate: bool = True,
):
    """
    Process common_forms.jsonl and generate Pydantic models.

    Args:
        input_file: Path to common_forms.jsonl
        output_dir: Directory to save generated Python files
        limit: Optional limit on number of forms to process
        model: Model to use
    """

    # Initialize OpenAI client
    api_key = os.environ.get("OPENAI_API_KEY")

    if not api_key:
        raise ValueError("API key required. Set OPENAI_API_KEY or pass api_key parameter")

    client = openai.OpenAI(api_key=api_key)

    os.makedirs(output_dir, exist_ok=True)

    # Also save metadata
    metadata_file = os.path.join(output_dir, "forms_metadata.jsonl")
    metadata_f = open(metadata_file, "w", encoding="utf-8")

    processed = 0
    errors = []

    with open(input_file, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            if limit and i >= limit:
                break

            try:
                data = json.loads(line)
                form_id = data.get("id")
                extracted_text = data.get("extracted_text", "")

                if not extracted_text:
                    print(f"Skipping form {form_id}: no extracted text")
                    continue

                print(f"\n{'=' * 60}")
                print(f"Processing form {form_id} ({i + 1}/{limit or '?'})...")
                print(f"{'=' * 60}")

                # Parse the form
                parsed_form = parse_form_multistep(extracted_text, client, model)

                # Generate class name
                class_name = parsed_form.form_title
                class_name = "".join(word.capitalize() for word in class_name.split())
                class_name = "".join(c for c in class_name if c.isalnum())
                # Fix if it starts with a number
                class_name = fix_class_name_starting_with_number(class_name)
                if not class_name:
                    class_name = f"Form{form_id}"

                # Check if class name exceeds OpenAI's 64 character limit for JSON schema names
                if len(class_name) > 64:
                    print(f"  ⚠ Class name too long ({len(class_name)} chars): {class_name}")
                    print(f"  → Using GPT-4o to generate shorter name...")
                    shortened_class_name = shorten_class_name_with_llm(class_name, client)
                    print(
                        f"  → Shortened to ({len(shortened_class_name)} chars): {shortened_class_name}"
                    )
                    class_name = shortened_class_name

                # Generate Pydantic code
                print("  Step 5: Generating Pydantic code...")
                pydantic_code = generate_pydantic_code(parsed_form, class_name)

                # Validate generated code
                if validate:
                    print("  Step 6: Validating generated code...")
                    is_valid = validate_generated_code(pydantic_code, form_id)
                    if not is_valid:
                        print(f"  ⚠ Code validation failed, but saving anyway...")

                # Save to file
                output_file = os.path.join(output_dir, f"form_{form_id}.py")
                with open(output_file, "w", encoding="utf-8") as out_f:
                    out_f.write(pydantic_code)

                print(f"  ✓ Saved to {output_file}")

                # Save metadata
                metadata = {
                    "id": form_id,
                    "form_title": parsed_form.form_title,
                    "class_name": class_name,
                    "sections": len(parsed_form.sections),
                    "total_fields": sum(len(s.fields) for s in parsed_form.sections),
                    "output_file": output_file,
                    "original_categories": data.get("categories", []),
                }
                metadata_f.write(json.dumps(metadata, ensure_ascii=False) + "\n")

                processed += 1

            except Exception as e:
                print(f"  ✗ Error processing form {form_id}: {e}")
                import traceback

                traceback.print_exc()
                errors.append({"id": form_id, "error": str(e)})
                continue

    metadata_f.close()

    print(f"\n{'=' * 60}")
    print(f"Processed {processed} forms successfully")
    print(f"Errors: {len(errors)}")
    if errors:
        print(f"Failed forms: {[e['id'] for e in errors]}")
    print(f"Output directory: {output_dir}")
    print(f"Metadata: {metadata_file}")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Parse forms using multi-step LLM prompting")
    parser.add_argument("--input", default="common_forms.jsonl", help="Input JSONL file")
    parser.add_argument(
        "--output", default="generated_forms", help="Output directory for generated Python files"
    )
    parser.add_argument(
        "--limit", type=int, default=60, help="Number of forms to process (default: 5)"
    )
    parser.add_argument("--model", default="gpt-5.1", help="Model to use")
    parser.add_argument(
        "--no-validate", action="store_true", help="Skip validation of generated code"
    )

    args = parser.parse_args()

    process_common_forms(
        input_file=args.input,
        output_dir=args.output,
        limit=args.limit,
        model=args.model,
        validate=not args.no_validate,
    )
