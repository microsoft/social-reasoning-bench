#!/usr/bin/env python3
"""
Convert form_filling_scenarios.jsonl to directory-based sage-benchmark format.

For each of the 60 tasks, creates:
  - task.json: persona, instruction, secrets
  - form_model.py: Pydantic form (copied from generated_forms/)
  - artifacts.json: Digital artifacts
  - ground_truth.json: Expected answers
"""

import argparse
import json
import shutil
from pathlib import Path


def load_jsonl(file_path: Path) -> list[dict]:
    """Load all scenarios from JSONL file."""
    data = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                data.append(json.loads(line))
    return data


def convert_scenario_to_task_directory(
    scenario: dict,
    output_base: Path,
    generated_forms_dir: Path,
) -> None:
    """Convert one JSONL scenario to task directory.

    Args:
        scenario: Scenario dict from JSONL
        output_base: Base output directory (e.g., sage-benchmark/data/form-filling/tasks/)
        generated_forms_dir: Directory containing generated_forms/*.py files
    """
    form_id = scenario["form_id"]
    task_dir = output_base / f"form_{form_id}"
    task_dir.mkdir(parents=True, exist_ok=True)

    print(f"  Converting form {form_id} -> {task_dir.name}")

    # 1. Create task.json (persona + instruction + secrets + field_coverage)
    # New format: secrets["question_secrets"] contains per-question secrets
    # Each question_secret has: question_id, question_text, secrets (list)
    # Each secret has: detail_content, why_sensitive, concrete_anchors, appears_naturally_in, subtlety_level
    secrets_data = scenario["secrets"]
    secrets_list = []
    for qs in secrets_data["question_secrets"]:
        for secret in qs["secrets"]:
            secrets_list.append(
                {
                    "detail_content": secret.get("detail_content"),
                    "why_sensitive": secret.get("why_sensitive"),
                    "concrete_anchors": secret.get("concrete_anchors"),
                    "appears_naturally_in": secret.get("appears_naturally_in"),
                    "subtlety_level": secret.get("subtlety_level"),
                    "related_question": qs.get("question_text", ""),
                    "question_id": qs.get("question_id", ""),
                }
            )

    task_data = {
        "form_id": form_id,
        "form_title": scenario["form_info"]["title"],
        "instruction": "Fill out this form for me",
        "persona": scenario["persona"],
        "secrets": secrets_list,
        "field_coverage": scenario["validation"]["field_coverage"],
    }

    with open(task_dir / "task.json", "w", encoding="utf-8") as f:
        json.dump(task_data, f, indent=2, ensure_ascii=False)

    # 2. Copy form_model.py
    src_form = generated_forms_dir / f"form_{form_id}.py"
    dst_form = task_dir / "form_model.py"

    if not src_form.exists():
        print(f"    WARNING: Form model not found: {src_form}")
        return

    shutil.copy(src_form, dst_form)

    # 3. Create artifacts.json
    with open(task_dir / "artifacts.json", "w", encoding="utf-8") as f:
        json.dump(scenario["artifacts"], f, indent=2, ensure_ascii=False)

    # 4. Create ground_truth.json
    with open(task_dir / "ground_truth.json", "w", encoding="utf-8") as f:
        json.dump(scenario["ground_truth"], f, indent=2, ensure_ascii=False)


def main():
    """Main conversion function."""
    parser = argparse.ArgumentParser(
        description="Convert form_filling_scenarios.jsonl to directory-based sage-benchmark format"
    )

    parser.add_argument(
        "--input",
        type=Path,
        default=Path("form_filling_scenarios.jsonl"),
        help="Path to input JSONL file (default: form_filling_scenarios.jsonl)",
    )

    parser.add_argument(
        "--output",
        type=Path,
        default=Path("../../sage-benchmark/data/form-filling/tasks"),
        help="Path to output directory (default: ../../sage-benchmark/data/form-filling/tasks)",
    )

    parser.add_argument(
        "--generated-forms-dir",
        type=Path,
        default=Path("generated_forms"),
        help="Directory containing generated pydantic form models (default: generated_forms)",
    )

    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Limit conversion to first N scenarios (default: None, convert all)",
    )

    args = parser.parse_args()

    # Validate input file exists
    if not args.input.exists():
        print(f"Error: Input file not found: {args.input}")
        return 1

    if not args.generated_forms_dir.exists():
        print(f"Error: Generated forms directory not found: {args.generated_forms_dir}")
        return 1

    # Load scenarios
    print(f"\nLoading scenarios from {args.input}...")
    scenarios = load_jsonl(args.input)
    print(f"Loaded {len(scenarios)} scenarios")

    # Filter scenarios if limit specified
    if args.limit:
        scenarios = scenarios[: args.limit]
        print(f"Converting first {args.limit} scenarios")

    # Create output directory
    args.output.mkdir(parents=True, exist_ok=True)
    print(f"Output directory: {args.output}")
    print(f"Generated forms: {args.generated_forms_dir}")

    # Convert each scenario
    print(f"\nConverting {len(scenarios)} scenarios...")
    success_count = 0
    failed_count = 0

    for scenario in scenarios:
        try:
            convert_scenario_to_task_directory(scenario, args.output, args.generated_forms_dir)
            success_count += 1
        except Exception as e:
            print(f"    ERROR: Failed to convert form {scenario.get('form_id', '?')}: {e}")
            failed_count += 1

    print(f"\n{'=' * 60}")
    print(f"CONVERSION SUMMARY")
    print(f"{'=' * 60}")
    print(f"Successful: {success_count}")
    print(f"Failed: {failed_count}")
    print(f"Output: {args.output}")
    print(f"{'=' * 60}")

    return 0


if __name__ == "__main__":
    exit(main())
