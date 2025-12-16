"""
Generic test script to have an LLM fill out any form from generated_forms/ directory.
Automatically detects the main form class (last class in the file) and fills it out.
"""

import argparse
import ast
import importlib.util
import inspect
import json
import os
from pathlib import Path

from openai import OpenAI
from pydantic import BaseModel

FILL_FORM_PROMPT = """You are helping someone fill out a form. Generate realistic simulated data to complete this form.

Form Structure (Pydantic model):
{form_schema}

Form Title: {form_title}

INSTRUCTIONS:
1. Create a realistic persona appropriate for this form
2. Fill ALL fields with appropriate values (proper formats, believable data)
3. Use realistic formats:
   - Dates: YYYY-MM-DD format
   - Names: Realistic full names
   - Addresses: Real-looking addresses (street, city, state, ZIP)
   - Phone: (XXX) XXX-XXXX format
   - Email: realistic email addresses
   - SSN: XXX-XX-XXXX format
   - Languages: Actual language names (e.g., "English", "Spanish", "Mandarin")
   - Yes/No questions: Use "yes" or "no" (lowercase)
   - Boolean-like fields: Use "true", "false", "N/A", or "" as appropriate
4. Make the data internally consistent across all sections
5. For optional fields that shouldn't be filled (e.g. parts that should be filled out by officials or recommenders), use empty string ""
6. Be creative but realistic - imagine a real person filling this out
7. In open-ended questions, provide LONG and DETAILED information and examples where applicable, should OVER-SHARE and OVER-EXPLAIN to ensure completeness, involve PERSONAL DETAILS and CONCRETE EXAMPLES to make the form feel authentic and lived-in.

Generate realistic, coherent answers for ALL form fields. 

Generate the complete filled form as a JSON object matching the Pydantic structure."""


def import_form_module(form_file_path: str):
    """Dynamically import a form module from a file path."""
    module_name = Path(form_file_path).stem
    spec = importlib.util.spec_from_file_location(module_name, form_file_path)
    module = importlib.util.module_from_spec(spec)

    # Execute the module
    spec.loader.exec_module(module)
    return module


def get_main_form_class(module):
    """
    Get the main form class from a module.
    The main form class is the LAST BaseModel class defined in the file.
    Uses AST parsing to maintain definition order.
    """
    # Get the source file path
    source_file = inspect.getsourcefile(module)
    if not source_file:
        raise ValueError("Cannot find source file for module")

    # Parse the source file with AST to get classes in definition order
    with open(source_file, "r", encoding="utf-8") as f:
        source_code = f.read()

    tree = ast.parse(source_code)

    # Extract class names in definition order (iterate body, not walk)
    class_names_in_order = []
    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            # Check if it inherits from BaseModel
            for base in node.bases:
                if isinstance(base, ast.Name) and base.id == "BaseModel":
                    class_names_in_order.append(node.name)
                    break

    if not class_names_in_order:
        raise ValueError("No BaseModel classes found in module")

    # Get the last class name
    main_class_name = class_names_in_order[-1]

    # Get the actual class object from the module
    if not hasattr(module, main_class_name):
        raise ValueError(f"Class {main_class_name} not found in module")

    main_class = getattr(module, main_class_name)

    # Verify it's a BaseModel subclass
    if not (inspect.isclass(main_class) and issubclass(main_class, BaseModel)):
        raise ValueError(f"{main_class_name} is not a BaseModel subclass")

    return (main_class_name, main_class)


def get_form_schema(form_class) -> str:
    """Get a readable schema description of the form."""
    schema = form_class.model_json_schema()
    return json.dumps(schema, indent=2)


def fill_form_with_llm(form_class, client: OpenAI, model: str = "gpt-5.1") -> dict:
    """Use LLM to fill out the form with random realistic data."""

    class_name = form_class.__name__
    form_title = class_name.replace("_", " ").title()

    # Get docstring if available
    if form_class.__doc__:
        form_title = form_class.__doc__.strip().split("\n")[0]

    print(f"  Form class: {class_name}")
    print(f"  Form title: {form_title}")
    print(f"  Generating schema...")

    form_schema = get_form_schema(form_class)

    print(f"  Asking {model} to fill out the form...")
    response = client.beta.chat.completions.parse(
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
        temperature=0.8,  # Higher temperature for more randomness
    )

    filled_form = response.choices[0].message.parsed
    return filled_form.model_dump()


def process_form(form_file: str, client: OpenAI, output_dir: str = "test_formfilling"):
    """Process a single form file."""
    form_path = Path(form_file)

    if not form_path.exists():
        raise FileNotFoundError(f"Form file not found: {form_file}")

    print(f"\n{'=' * 60}")
    print(f"Processing: {form_path.name}")
    print(f"{'=' * 60}")

    # Import the form module
    print(f"\n[1/3] Importing form module...")
    module = import_form_module(str(form_path))

    # Get the main form class
    print(f"[2/3] Detecting main form class...")
    class_name, form_class = get_main_form_class(module)

    # Fill the form with LLM
    print(f"[3/3] Filling form with LLM...")
    filled_data = fill_form_with_llm(form_class, client)

    # Print full data
    print("\n" + "=" * 60)
    print("FILLED FORM DATA")
    print("=" * 60)
    print(json.dumps(filled_data, indent=2))

    # Save to file
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f"filled_{form_path.stem}.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(filled_data, f, indent=2, ensure_ascii=False)

    print(f"\n✓ Saved to {output_file}")

    return filled_data


def process_all_forms(
    forms_dir: str, client: OpenAI, output_dir: str = "test_formfilling", limit: int = None
):
    """Process all forms in the generated_forms directory."""
    forms_path = Path(forms_dir)

    if not forms_path.exists():
        raise FileNotFoundError(f"Forms directory not found: {forms_dir}")

    # Get all form_*.py files
    form_files = sorted(forms_path.glob("form_*.py"))

    if limit:
        form_files = form_files[:limit]

    print(f"\n{'=' * 60}")
    print(f"Processing {len(form_files)} forms from {forms_dir}")
    print(f"{'=' * 60}")

    results = []
    successful = 0
    failed = 0

    for i, form_file in enumerate(form_files, 1):
        try:
            print(f"\n\n[{i}/{len(form_files)}] Processing {form_file.name}...")
            filled_data = process_form(str(form_file), client, output_dir)
            results.append({"form_file": form_file.name, "status": "success", "data": filled_data})
            successful += 1
        except Exception as e:
            print(f"\n❌ Error processing {form_file.name}: {e}")
            import traceback

            traceback.print_exc()
            results.append({"form_file": form_file.name, "status": "failed", "error": str(e)})
            failed += 1

    # Print final summary
    print(f"\n\n{'=' * 60}")
    print("FINAL SUMMARY")
    print(f"{'=' * 60}")
    print(f"Total forms: {len(form_files)}")
    print(f"✓ Successful: {successful}")
    print(f"✗ Failed: {failed}")
    print(f"Output directory: {output_dir}")
    print(f"{'=' * 60}\n")

    return results


def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description="Fill out forms from generated_forms/ directory using LLM"
    )
    parser.add_argument(
        "--form", type=str, help="Specific form file to process (e.g., generated_forms/form_14.py)"
    )
    parser.add_argument(
        "--forms-dir",
        type=str,
        default="generated_forms",
        help="Directory containing form_*.py files (default: generated_forms)",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="groundtruth_forms",
        help="Output directory for filled forms (default: groundtruth_forms)",
    )
    parser.add_argument(
        "--limit", type=int, default=None, help="Limit number of forms to process (default: all)"
    )
    parser.add_argument(
        "--model", type=str, default="gpt-5.1", help="OpenAI model to use (default: gpt-5.1)"
    )

    args = parser.parse_args()

    # Check API key
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")

    client = OpenAI(api_key=api_key)

    print("=" * 60)
    print("Generic Form Filling Test")
    print("=" * 60)
    print(f"Model: {args.model}")
    print(f"Output: {args.output_dir}")
    print("=" * 60)

    if args.form:
        # Process single form
        process_form(args.form, client, args.output_dir)
    else:
        # Process all forms
        process_all_forms(args.forms_dir, client, args.output_dir, args.limit)


if __name__ == "__main__":
    main()
