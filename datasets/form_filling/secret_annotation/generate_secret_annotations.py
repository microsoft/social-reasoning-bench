"""
Generate HTML annotation files for secret evaluation.

This script reads scenario data and generates individual HTML files for each form,
allowing human annotators to evaluate the quality of generated secrets.
"""

import json
import os
from typing import Dict, List


def load_jsonl(file_path: str) -> List[Dict]:
    """Load all scenarios from JSONL file."""
    data = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                data.append(json.loads(line))
    return data


def extract_secrets(scenario: Dict) -> List[Dict]:
    """Extract secrets from scenario, handling both old and new formats.

    Args:
        scenario: Scenario data

    Returns:
        List of secrets with question context added if available
    """
    secrets_data = scenario.get("secrets", {})

    # New format: AllSecrets with form_summary and question_secrets
    if "question_secrets" in secrets_data:
        # Flatten question_secrets to list with question context
        secrets = []
        for qs in secrets_data.get("question_secrets", []):
            question_text = qs.get("question_text", "")
            question_id = qs.get("question_id", "")
            for secret in qs.get("secrets", []):
                # Add question context to each secret
                secret_with_context = secret.copy()
                secret_with_context["related_question"] = question_text
                secret_with_context["related_question_id"] = question_id
                secrets.append(secret_with_context)
        return secrets
    else:
        # Old format: flat list of secrets
        return secrets_data.get("secrets", [])


def load_form_schema(form_id: int, generated_forms_dir: str = "../generated_forms") -> Dict:
    """Load the form schema from the generated Pydantic form class.

    Args:
        form_id: The form ID to load
        generated_forms_dir: Directory containing generated form Python files

    Returns:
        JSON schema dictionary from the Pydantic model
    """
    import importlib.util
    import sys

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

    # Find the main form class (usually contains "Form" in the name and is defined last)
    # Try to find a class that inherits from BaseModel
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

    # Strategy 1: Look for a class with "Form" in the name (case-insensitive)
    form_class = None
    for name, obj in all_classes:
        if "form" in name.lower():
            form_class = obj
            break

    # Strategy 2: If no "Form" class, take the one with most fields (likely the main class)
    if form_class is None:
        form_class = max(all_classes, key=lambda x: len(x[1].model_fields))[1]

    # Return the JSON schema
    return form_class.model_json_schema()


def generate_html(scenario: Dict, all_form_ids: List[int], output_dir: str = "output"):
    """Generate HTML annotation file for a single scenario.

    Args:
        scenario: Scenario data containing persona, secrets, and form info
        all_form_ids: List of all form IDs in order (for navigation)
        output_dir: Directory to save generated HTML files (relative to secret_annotation/)
    """
    form_id = scenario["form_id"]
    persona = scenario["persona"]
    secrets = extract_secrets(scenario)
    form_info = scenario.get("form_info", {})

    # Load the original form schema
    form_schema = load_form_schema(form_id)

    # Read the HTML template (in same directory as this script)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(script_dir, "secret_annotation.html")
    with open(template_path, "r", encoding="utf-8") as f:
        html_template = f.read()

    # Prepare data for injection
    data = {
        "form_id": form_id,
        "form_schema": form_schema,
        "persona": persona,
        "secrets": secrets,
        "form_info": form_info,
    }

    # Convert data to JSON string
    data_json = json.dumps(data, ensure_ascii=False, indent=2)

    # Convert form IDs list to JSON string
    form_ids_json = json.dumps(all_form_ids)

    # Replace placeholders in template
    html_content = html_template.replace("{{DATA_JSON}}", data_json)
    html_content = html_content.replace("{{FORM_ID}}", str(form_id))
    html_content = html_content.replace("{{TOTAL_SECRETS}}", str(len(secrets)))
    html_content = html_content.replace("{{ALL_FORM_IDS}}", form_ids_json)

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Save HTML file
    output_path = os.path.join(output_dir, f"secret_annotation_form_{form_id}.html")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"Generated annotation file: {output_path}")
    return output_path


def generate_all_annotations(
    scenarios_file: str = "../new_form_filling_scenarios.jsonl",
    output_dir: str = "output",
    limit: int = None,
):
    """Generate HTML annotation files for all scenarios.

    Args:
        scenarios_file: Path to scenarios JSONL file (relative to secret_annotation/)
        output_dir: Directory to save generated HTML files (relative to secret_annotation/)
        limit: Optional limit on number of files to generate
    """
    print(f"Loading scenarios from {scenarios_file}...")
    scenarios = load_jsonl(scenarios_file)

    if limit:
        scenarios = scenarios[:limit]

    print(f"Generating {len(scenarios)} annotation files...")

    # Collect all form IDs in order for navigation
    all_form_ids = [scenario["form_id"] for scenario in scenarios]

    generated_files = []
    for i, scenario in enumerate(scenarios, 1):
        try:
            output_path = generate_html(scenario, all_form_ids, output_dir)
            generated_files.append(output_path)
            print(f"  [{i}/{len(scenarios)}] ✓ Form {scenario['form_id']}")
        except Exception as e:
            print(f"  [{i}/{len(scenarios)}] ✗ Form {scenario['form_id']}: {e}")

    print(f"\n{'=' * 60}")
    print(f"Generated {len(generated_files)} annotation files")
    print(f"Output directory: {output_dir}")
    print(f"{'=' * 60}")

    # Generate index file
    generate_index(generated_files, scenarios, output_dir)


def generate_index(file_paths: List[str], scenarios: List[Dict], output_dir: str):
    """Generate an index HTML file listing all annotation files.

    Args:
        file_paths: List of generated HTML file paths
        scenarios: List of scenario data
        output_dir: Directory where files are saved
    """
    index_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Secret Annotation Index</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 40px 20px;
            background-color: #f5f5f5;
        }
        h1 {
            color: #2c3e50;
            margin-bottom: 10px;
        }
        .subtitle {
            color: #7f8c8d;
            margin-bottom: 30px;
        }
        .card {
            background: white;
            padding: 20px;
            margin-bottom: 15px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            display: flex;
            justify-content: space-between;
            align-items: center;
            transition: transform 0.2s;
        }
        .card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        }
        .card-info {
            flex: 1;
        }
        .form-id {
            font-size: 18px;
            font-weight: 600;
            color: #2c3e50;
            margin-bottom: 5px;
        }
        .persona-name {
            color: #7f8c8d;
            font-size: 14px;
        }
        .secret-count {
            background-color: #e74c3c;
            color: white;
            padding: 6px 12px;
            border-radius: 4px;
            font-size: 14px;
            font-weight: 600;
            margin-right: 15px;
        }
        .btn {
            background-color: #3498db;
            color: white;
            padding: 10px 20px;
            border-radius: 6px;
            text-decoration: none;
            font-weight: 600;
            transition: background-color 0.3s;
        }
        .btn:hover {
            background-color: #2980b9;
        }
        .stats {
            background: white;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 30px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-top: 15px;
        }
        .stat-item {
            text-align: center;
        }
        .stat-value {
            font-size: 32px;
            font-weight: 600;
            color: #3498db;
        }
        .stat-label {
            color: #7f8c8d;
            font-size: 14px;
            margin-top: 5px;
        }
    </style>
</head>
<body>
    <h1>🔒 Secret Annotation Index</h1>
    <p class="subtitle">Select a form to begin annotation</p>

    <div class="stats">
        <h3 style="margin-bottom: 15px; color: #2c3e50;">Statistics</h3>
        <div class="stats-grid">
            <div class="stat-item">
                <div class="stat-value">{{TOTAL_FORMS}}</div>
                <div class="stat-label">Total Forms</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">{{TOTAL_SECRETS}}</div>
                <div class="stat-label">Total Secrets</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">{{AVG_SECRETS}}</div>
                <div class="stat-label">Avg Secrets/Form</div>
            </div>
        </div>
    </div>

    <div id="forms-list">
        {{FORMS_LIST}}
    </div>
</body>
</html>
"""

    # Calculate statistics
    total_forms = len(scenarios)
    total_secrets = sum(len(extract_secrets(s)) for s in scenarios)
    avg_secrets = f"{total_secrets / total_forms:.1f}" if total_forms > 0 else "0"

    # Generate forms list
    forms_list_html = ""
    for i, scenario in enumerate(scenarios):
        form_id = scenario["form_id"]
        persona_name = scenario["persona"].get("full_name", "Unknown")
        secret_count = len(extract_secrets(scenario))
        file_name = os.path.basename(file_paths[i])

        forms_list_html += f"""
        <div class="card">
            <div class="card-info">
                <div class="form-id">Form {form_id}</div>
                <div class="persona-name">{persona_name}</div>
            </div>
            <span class="secret-count">{secret_count} secrets</span>
            <a href="{file_name}" class="btn">Annotate →</a>
        </div>
        """

    # Replace placeholders
    index_html = index_html.replace("{{TOTAL_FORMS}}", str(total_forms))
    index_html = index_html.replace("{{TOTAL_SECRETS}}", str(total_secrets))
    index_html = index_html.replace("{{AVG_SECRETS}}", avg_secrets)
    index_html = index_html.replace("{{FORMS_LIST}}", forms_list_html)

    # Save index file
    index_path = os.path.join(output_dir, "index.html")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(index_html)

    print(f"\n✓ Generated index file: {index_path}")
    print(f"\nOpen {index_path} in your browser to begin annotation")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate HTML annotation files for secret evaluation"
    )
    parser.add_argument(
        "--input",
        type=str,
        default="../form_filling_scenarios.jsonl",
        help="Input scenarios JSONL file (relative to secret_annotation/)",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="output",
        help="Output directory for HTML files (relative to secret_annotation/)",
    )
    parser.add_argument(
        "--limit", type=int, default=None, help="Limit number of files to generate (for testing)"
    )

    args = parser.parse_args()

    generate_all_annotations(
        scenarios_file=args.input, output_dir=args.output_dir, limit=args.limit
    )
