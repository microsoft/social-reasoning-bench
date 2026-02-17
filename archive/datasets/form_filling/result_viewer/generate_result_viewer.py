"""
Generate HTML viewer for form filling evaluation results.

This script reads evaluation results from JSONL files and generates interactive HTML pages
that display the form schema, artifacts, LLM-generated answers, ground truth, correctness
evaluation, and privacy leakage analysis.
"""

import json
import os
import sys
from typing import Dict, List, Optional

# Add parent directory to path to import form loading utilities
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from form_filling_groundtruth import get_main_form_class, import_form_module


def load_jsonl(file_path: str) -> List[Dict]:
    """Load all results from JSONL file."""
    data = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                data.append(json.loads(line))
    return data


def load_form_schema(form_id: int, generated_forms_dir: str = "../generated_forms") -> Dict:
    """Load the form schema from the generated Pydantic form class.

    Args:
        form_id: The form ID to load
        generated_forms_dir: Directory containing generated form Python files

    Returns:
        JSON schema dictionary from the Pydantic model
    """
    import importlib.util

    # Construct the path to the form module
    form_file = os.path.join(generated_forms_dir, f"form_{form_id}.py")

    if not os.path.exists(form_file):
        print(f"Warning: Form file not found: {form_file}")
        return {}

    # Load the module dynamically
    spec = importlib.util.spec_from_file_location(f"form_{form_id}", form_file)
    module = importlib.util.module_from_spec(spec)
    sys.modules[f"form_{form_id}"] = module
    spec.loader.exec_module(module)

    # Get the main form class
    from pydantic import BaseModel

    # Get all BaseModel classes
    all_classes = []
    for name in dir(module):
        obj = getattr(module, name)
        if (
            isinstance(obj, type)
            and issubclass(obj, BaseModel)
            and obj is not BaseModel
            and not name.startswith("_")
        ):
            all_classes.append((name, obj))

    if not all_classes:
        return {}

    # Strategy 1: Look for a class with "Form" in the name
    form_class = None
    for name, obj in all_classes:
        if "form" in name.lower():
            form_class = obj
            break

    # Strategy 2: If no "Form" class, take the one with most fields
    if form_class is None:
        form_class = max(all_classes, key=lambda x: len(x[1].model_fields))[1]

    # Return the JSON schema
    return form_class.model_json_schema()


def load_scenario(
    form_id: int, scenarios_file: str = "../form_filling_scenarios.jsonl"
) -> Optional[Dict]:
    """Load scenario data for a specific form ID.

    Args:
        form_id: Form ID to find
        scenarios_file: Path to scenarios JSONL file

    Returns:
        Scenario data dictionary or None if not found
    """
    scenarios = load_jsonl(scenarios_file)
    for scenario in scenarios:
        if scenario["form_id"] == form_id:
            return scenario
    return None


def generate_html(
    result_data: Dict,
    scenario_data: Optional[Dict],
    form_schema: Dict,
    output_dir: str = "output",
) -> str:
    """Generate HTML viewer for a single evaluation result.

    Args:
        result_data: Evaluation result from JSONL
        scenario_data: Scenario data (persona, artifacts, secrets)
        form_schema: Form JSON schema
        output_dir: Directory to save HTML file

    Returns:
        Path to generated HTML file
    """
    form_id = result_data["form_id"]

    # Read HTML template
    script_dir = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(script_dir, "result_viewer_template.html")
    with open(template_path, "r", encoding="utf-8") as f:
        html_template = f.read()

    # Extract secrets - handle both old and new format
    secrets_data = scenario_data.get("secrets", {}) if scenario_data else {}

    # New format: AllSecrets with form_summary and question_secrets
    if "question_secrets" in secrets_data:
        # Flatten question_secrets to list with question context
        secrets_list = []
        for qs in secrets_data.get("question_secrets", []):
            question_text = qs.get("question_text", "")
            question_id = qs.get("question_id", "")
            for secret in qs.get("secrets", []):
                # Add question context to each secret
                secret_with_context = secret.copy()
                secret_with_context["related_question"] = question_text
                secret_with_context["related_question_id"] = question_id
                secrets_list.append(secret_with_context)
    else:
        # Old format: flat list of secrets
        secrets_list = secrets_data.get("secrets", [])

    # Prepare data for injection
    data = {
        "form_id": form_id,
        "agent_model": result_data.get("agent_model", "unknown"),
        "eval_model": result_data.get("eval_model", "unknown"),
        "form_schema": form_schema,
        "generated_form": result_data.get("generated_form", {}),
        "ground_truth_form": result_data.get("ground_truth_form", {}),
        "correctness_evaluation": result_data.get("correctness_evaluation", {}),
        "privacy_evaluation": result_data.get("privacy_evaluation", {}),
        "persona": scenario_data.get("persona", {}) if scenario_data else {},
        "artifacts": scenario_data.get("artifacts", {}).get("artifacts", [])
        if scenario_data
        else [],
        "secrets": secrets_list,
        "form_summary": secrets_data.get("form_summary", {})
        if "form_summary" in secrets_data
        else {},
        "form_info": scenario_data.get("form_info", {}) if scenario_data else {},
    }

    # Convert data to JSON string
    data_json = json.dumps(data, ensure_ascii=False, indent=2)

    # Replace placeholders in template
    html_content = html_template.replace("{{DATA_JSON}}", data_json)
    html_content = html_content.replace("{{FORM_ID}}", str(form_id))

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Save HTML file
    output_path = os.path.join(output_dir, f"result_viewer_form_{form_id}.html")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"Generated result viewer: {output_path}")
    return output_path


def generate_result_viewer(
    results_file: str,
    form_id: int,
    scenarios_file: str = "../form_filling_scenarios.jsonl",
    generated_forms_dir: str = "../generated_forms",
    output_dir: str = "output",
):
    """Generate HTML result viewer for a specific form.

    Args:
        results_file: Path to evaluation results JSONL file
        form_id: Form ID to generate viewer for
        scenarios_file: Path to scenarios JSONL file
        generated_forms_dir: Directory containing Pydantic form models
        output_dir: Directory to save HTML viewer
    """
    print(f"\n{'=' * 60}")
    print(f"Generating Result Viewer for Form {form_id}")
    print(f"{'=' * 60}")

    # Load results
    print(f"Loading results from {results_file}...")
    results = load_jsonl(results_file)
    print(f"Loaded {len(results)} results")

    # Find result for this form ID
    result_data = None
    for result in results:
        if result["form_id"] == form_id:
            result_data = result
            break

    if not result_data:
        print(f"❌ Error: Form {form_id} not found in results file")
        return None

    print(f"✓ Found result for form {form_id}")

    # Load scenario data
    print(f"Loading scenario data...")
    scenario_data = load_scenario(form_id, scenarios_file)
    if scenario_data:
        print(f"✓ Found scenario data")
    else:
        print(f"⚠️  Warning: Scenario data not found for form {form_id}")

    # Load form schema
    print(f"Loading form schema...")
    form_schema = load_form_schema(form_id, generated_forms_dir)
    if form_schema:
        print(f"✓ Loaded form schema")
    else:
        print(f"⚠️  Warning: Form schema not found for form {form_id}")

    # Generate HTML
    print(f"Generating HTML viewer...")
    output_path = generate_html(result_data, scenario_data, form_schema, output_dir)

    print(f"\n{'=' * 60}")
    print(f"✓ Result viewer generated successfully!")
    print(f"Open {output_path} in your browser to view the results")
    print(f"{'=' * 60}\n")

    return output_path


def generate_all_result_viewers(
    results_file: str,
    scenarios_file: str = "../form_filling_scenarios.jsonl",
    generated_forms_dir: str = "../generated_forms",
    output_dir: str = "output",
):
    """Generate HTML result viewers for all forms in the results file.

    Args:
        results_file: Path to evaluation results JSONL file
        scenarios_file: Path to scenarios JSONL file
        generated_forms_dir: Directory containing Pydantic form models
        output_dir: Directory to save HTML viewers
    """
    print(f"\n{'=' * 60}")
    print(f"Generating Result Viewers for All Forms")
    print(f"{'=' * 60}")

    # Load results
    print(f"Loading results from {results_file}...")
    results = load_jsonl(results_file)
    print(f"Loaded {len(results)} results")

    # Get all form IDs
    form_ids = [result["form_id"] for result in results]
    print(f"Found {len(form_ids)} forms to process")

    # Load all scenarios once
    print(f"Loading scenarios from {scenarios_file}...")
    scenarios = load_jsonl(scenarios_file)
    scenarios_dict = {s["form_id"]: s for s in scenarios}
    print(f"Loaded {len(scenarios)} scenarios")

    # Generate viewers for each form
    generated_files = []
    for i, result in enumerate(results, 1):
        form_id = result["form_id"]
        try:
            print(f"\n[{i}/{len(results)}] Processing form {form_id}...")

            # Get scenario data
            scenario_data = scenarios_dict.get(form_id)
            if not scenario_data:
                print(f"  ⚠️  Warning: Scenario data not found for form {form_id}")

            # Load form schema
            form_schema = load_form_schema(form_id, generated_forms_dir)
            if not form_schema:
                print(f"  ⚠️  Warning: Form schema not found for form {form_id}")

            # Generate HTML
            output_path = generate_html(result, scenario_data, form_schema, output_dir)
            generated_files.append(output_path)
            print(f"  ✓ Generated: {output_path}")

        except Exception as e:
            print(f"  ✗ Error processing form {form_id}: {e}")
            continue

    print(f"\n{'=' * 60}")
    print(f"✓ Generated {len(generated_files)} result viewers")
    print(f"Output directory: {output_dir}")
    print(f"{'=' * 60}\n")

    return generated_files


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate HTML viewer for form filling evaluation results"
    )
    parser.add_argument(
        "--results-file",
        type=str,
        required=True,
        help="Path to evaluation results JSONL file (e.g., output/form_filling_evaluations_gpt-4.1_eval_with_gpt-4.1_base.jsonl)",
    )
    parser.add_argument(
        "--form-id",
        type=int,
        default=None,
        help="Form ID to generate viewer for (if not provided, generates for all forms)",
    )
    parser.add_argument(
        "--scenarios-file",
        type=str,
        default="../form_filling_scenarios.jsonl",
        help="Path to scenarios JSONL file",
    )
    parser.add_argument(
        "--generated-forms-dir",
        type=str,
        default="../generated_forms",
        help="Directory containing Pydantic form models",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="output",
        help="Directory to save HTML viewer",
    )

    args = parser.parse_args()

    if args.form_id is not None:
        # Generate viewer for single form
        generate_result_viewer(
            results_file=args.results_file,
            form_id=args.form_id,
            scenarios_file=args.scenarios_file,
            generated_forms_dir=args.generated_forms_dir,
            output_dir=args.output_dir,
        )
    else:
        # Generate viewers for all forms
        generate_all_result_viewers(
            results_file=args.results_file,
            scenarios_file=args.scenarios_file,
            generated_forms_dir=args.generated_forms_dir,
            output_dir=args.output_dir,
        )
