"""Shared utilities for form filling data generation."""

import base64
import re
from pathlib import Path

from sage_benchmark.benchmarks.form_filling.utils import import_form_model_from_file  # noqa: F401


def extract_form_id(image_path: str | Path) -> str:
    """Extract a numeric form ID from an image filename.

    Handles patterns like:
        form_123.png -> 123
        123.png -> 123
        image_456.jpg -> 456
        my_form.png -> hash-based fallback

    Args:
        image_path: Path to the form image.

    Returns:
        String form ID (numeric).
    """
    stem = Path(image_path).stem
    # Try to extract digits from common patterns
    match = re.search(r"(\d+)", stem)
    if match:
        return match.group(1)
    # Fallback: use hash of filename
    return str(abs(hash(stem)) % 100000)


def image_to_base64(image_path: Path) -> str:
    """Read an image file and return its base64-encoded string.

    Args:
        image_path: Path to a PNG or JPEG image.

    Returns:
        Base64-encoded string of the image bytes.
    """
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode()


def image_mime_type(image_path: Path) -> str:
    """Return the MIME type for an image based on its extension."""
    suffix = image_path.suffix.lower()
    if suffix in (".jpg", ".jpeg"):
        return "image/jpeg"
    return "image/png"


def clean_json_response(text: str) -> str:
    """Strip markdown code fences from an LLM JSON response."""
    text = text.strip()
    if text.startswith("```json"):
        text = text[7:]
    elif text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]
    return text.strip()


def clean_html_response(text: str) -> str:
    """Strip markdown code fences from an LLM HTML response."""
    text = text.strip()
    if text.startswith("```html"):
        text = text[7:]
    elif text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]
    return text.strip()


def flatten_form_data(form_data: dict, prefix: str = "") -> list[dict]:
    """Flatten hierarchical form data into a list of field-value pairs.

    Args:
        form_data: Nested dict from a Pydantic model dump.
        prefix: Current key prefix for recursion.

    Returns:
        List of dicts with 'field_path' and 'value' keys.
    """
    flattened = []

    for key, value in form_data.items():
        full_key = f"{prefix}.{key}" if prefix else key

        if isinstance(value, dict):
            flattened.extend(flatten_form_data(value, full_key))
        elif isinstance(value, list):
            for i, item in enumerate(value):
                if isinstance(item, dict):
                    flattened.extend(flatten_form_data(item, f"{full_key}[{i}]"))
                else:
                    flattened.append({"field_path": f"{full_key}[{i}]", "value": str(item)})
        else:
            flattened.append({"field_path": full_key, "value": str(value)})

    return flattened


def clear_signature_fields(data: dict) -> dict:
    """Recursively set any field whose name contains 'signature' to empty string."""
    result = {}
    for key, value in data.items():
        if isinstance(value, dict):
            result[key] = clear_signature_fields(value)
        elif isinstance(value, list):
            result[key] = [
                clear_signature_fields(item) if isinstance(item, dict) else item for item in value
            ]
        elif "signature" in key.lower():
            result[key] = ""
        else:
            result[key] = value
    return result


def translate_persona2text(persona) -> str:
    """Convert persona dict or ExpandedPersona to text format, excluding background_context.

    Args:
        persona: Persona information (dict or Pydantic model).

    Returns:
        Formatted persona string.
    """
    if isinstance(persona, dict):
        get_field = lambda key, default="N/A": persona.get(key, default)
    else:
        get_field = lambda key, default="N/A": (
            getattr(persona, key, default) if getattr(persona, key, None) is not None else default
        )

    persona_info = f"""Name: {get_field("full_name")}
Age: {get_field("age")}
Gender: {get_field("gender")}
Race: {get_field("race")}
Address: {get_field("address")}, {get_field("city")}, {get_field("state")} {get_field("zip_code")}
Email: {get_field("email")}
Phone: {get_field("phone")}
SSN: {get_field("ssn")}"""

    occupation = get_field("occupation", None)
    if occupation:
        persona_info += f"\nOccupation: {occupation}"

    employer = get_field("employer", None)
    if employer:
        persona_info += f"\nEmployer: {employer}"

    education = get_field("education", None)
    if education:
        persona_info += f"\nEducation: {education}"

    family_members = get_field("family_members", None)
    if family_members and isinstance(family_members, list) and len(family_members) > 0:
        persona_info += f"\nFamily Members: {', '.join(family_members)}"

    return persona_info


# Python reserved keywords (for form field ID sanitization)
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


def fix_html(html: str) -> tuple[str, list[str]]:
    """Apply CSS fixes to generated HTML forms.

    Fixes the white page background not covering full form content caused by
    body using display:flex without align-items:flex-start, and .page having
    overflow:hidden.

    Args:
        html: Raw HTML string.

    Returns:
        Tuple of (fixed_html, list_of_changes_made).
    """
    changes = []

    # 1. Add align-items:flex-start to the body rule that contains display:flex
    for body_match in re.finditer(r"body\s*\{[^}]+\}", html):
        block = body_match.group(0)
        if "display" not in block or "flex" not in block:
            continue
        if "align-items" in block:
            break

        patched = re.sub(
            r"(justify-content\s*:\s*center\s*;)",
            r"\1align-items:flex-start;",
            block,
            count=1,
        )
        if patched == block:
            patched = re.sub(
                r"(display\s*:\s*flex\s*;)",
                r"\1align-items:flex-start;",
                block,
                count=1,
            )
        if patched != block:
            html = html.replace(block, patched, 1)
            changes.append("added align-items:flex-start to body")
        break

    # 2. Remove overflow:hidden from .page rule
    page_match = re.search(r"\.page\s*\{[^}]+\}", html)
    if page_match and "overflow" in page_match.group(0):
        original_page = page_match.group(0)
        cleaned_page = re.sub(r"\s*overflow\s*:\s*hidden\s*;?", "", original_page)
        if cleaned_page != original_page:
            html = html.replace(original_page, cleaned_page)
            changes.append("removed overflow:hidden from .page")

    return html, changes


def fix_class_name_starting_with_number(class_name: str) -> str:
    """Fix class names that start with numbers by moving digits to the end.

    Examples:
        "123Application" -> "Application123"
        "2025TaxForm" -> "TaxForm2025"
        "ValidName" -> "ValidName"
    """
    if not class_name or not class_name[0].isdigit():
        return class_name

    leading_digits = ""
    rest = ""
    for char in class_name:
        if char.isdigit() and rest == "":
            leading_digits += char
        else:
            rest += char

    if not rest:
        return f"Form{leading_digits}"
    return f"{rest}{leading_digits}"
