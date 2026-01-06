"""
Explore and display forms from common_forms.jsonl in a readable format.

This script reads forms from common_forms.jsonl and displays their content
in a nicely formatted, human-readable way.
"""

import json
import os
from typing import Optional


def format_list(items, indent=2):
    """Format a list with bullet points."""
    if not items:
        return "None"
    indent_str = " " * indent
    return "\n".join(f"{indent_str}• {item}" for item in items)


def format_privacy_evaluation(eval_data: dict, indent=2):
    """Format privacy evaluation data."""
    indent_str = " " * indent
    lines = []

    lines.append(
        f"{indent_str}Required Privacy: {'✓' if eval_data.get('required_privacy') else '✗'}"
    )
    lines.append(f"{indent_str}Over Disclosure: {'✓' if eval_data.get('over_disclosure') else '✗'}")
    lines.append(
        f"{indent_str}Contextual Disclosure: {'✓' if eval_data.get('contextual_disclosure') else '✗'}"
    )

    if "reasoning" in eval_data:
        lines.append(f"\n{indent_str}Reasoning:")
        # Wrap reasoning text nicely
        reasoning = eval_data["reasoning"]
        for line in reasoning.split("\n"):
            lines.append(f"{indent_str}  {line}")

    if "error" in eval_data:
        lines.append(f"\n{indent_str}⚠️  Error: {eval_data['error']}")

    return "\n".join(lines)


def format_risk_comparison(comparison_data: dict, indent=2):
    """Format privacy risk comparison data."""
    indent_str = " " * indent
    lines = []

    if "higher_risk_form" in comparison_data:
        lines.append(f"{indent_str}Higher Risk Form: {comparison_data['higher_risk_form']}")

    if "risk_score" in comparison_data:
        score = comparison_data["risk_score"]
        bars = "█" * score + "░" * (10 - score)
        lines.append(f"{indent_str}Risk Score: {score}/10 [{bars}]")

    if "comparison_reasoning" in comparison_data:
        lines.append(f"\n{indent_str}Comparison Reasoning:")
        reasoning = comparison_data["comparison_reasoning"]
        for line in reasoning.split("\n"):
            lines.append(f"{indent_str}  {line}")

    if "key_privacy_risks" in comparison_data:
        lines.append(f"\n{indent_str}Key Privacy Risks:")
        for risk in comparison_data["key_privacy_risks"]:
            lines.append(f"{indent_str}  • {risk}")

    if "likely_overdisclosure_scenarios" in comparison_data:
        lines.append(f"\n{indent_str}Likely Overdisclosure Scenarios:")
        for scenario in comparison_data["likely_overdisclosure_scenarios"]:
            lines.append(f"{indent_str}  • {scenario}")

    if "reasoning" in comparison_data:
        lines.append(f"\n{indent_str}Detailed Reasoning:")
        reasoning = comparison_data["reasoning"]
        for line in reasoning.split("\n"):
            lines.append(f"{indent_str}  {line}")

    return "\n".join(lines)


def display_form(form_data: dict, form_number: int):
    """Display a single form in a nicely formatted way."""
    print("\n" + "=" * 80)
    print(f"FORM #{form_number}")
    print("=" * 80)

    # Basic info
    if "id" in form_data:
        print(f"ID: {form_data['id']}")

    if "categories" in form_data:
        print(f"Categories: {', '.join(form_data['categories'])}")

    if "is_baseline" in form_data and form_data["is_baseline"]:
        print("⭐ BASELINE FORM")

    # Extracted text
    if "extracted_text" in form_data:
        text = form_data["extracted_text"]
        print(f"\n{'─' * 80}")
        print("EXTRACTED TEXT")
        print(f"{'─' * 80}")
        print(text)
        print(f"\n(Text length: {len(text)} characters)")

    # Privacy risk comparison
    if "privacy_risk_comparison" in form_data:
        print(f"\n{'─' * 80}")
        print("PRIVACY RISK COMPARISON")
        print(f"{'─' * 80}")
        print(format_risk_comparison(form_data["privacy_risk_comparison"]))

    # Privacy evaluation (types)
    if "privacy_evaluation" in form_data:
        print(f"\n{'─' * 80}")
        print("PRIVACY EVALUATION")
        print(f"{'─' * 80}")
        print(format_privacy_evaluation(form_data["privacy_evaluation"]))

    print("\n" + "=" * 80)


def load_forms(file_path: str = "common_forms.jsonl"):
    """Load all forms from the JSONL file."""
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return []

    forms = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                forms.append(json.loads(line))

    return forms


def main(file_path: str = "common_forms.jsonl", form_id: Optional[int] = None):
    """
    Main function to explore forms.

    Args:
        file_path: Path to the JSONL file
        form_id: Show only the form with this ID (if None, enters interactive mode)
    """
    forms = load_forms(file_path)

    if not forms:
        print("No forms found!")
        return

    print(f"📋 Loaded {len(forms)} forms from {file_path}")

    # Interactive mode
    print("\nInteractive Mode")
    print("Commands:")
    print("  n / next     - Show next form")
    print("  p / prev     - Show previous form")
    print("  g [num]      - Go to form number")
    print("  s / summary  - Show summary of all forms")
    print("  q / quit     - Quit")
    print()

    current_index = form_id

    while True:
        display_form(forms[current_index], current_index + 1)

        print(f"\nForm {current_index + 1} of {len(forms)}")
        command = input("Enter command: ").strip().lower()

        if command in ["q", "quit", "exit"]:
            print("Goodbye!")
            break
        elif command in ["n", "next"]:
            current_index = min(current_index + 1, len(forms) - 1)
        elif command in ["p", "prev", "previous"]:
            current_index = max(current_index - 1, 0)
        elif command.startswith("g "):
            try:
                target = int(command.split()[1]) - 1
                if 0 <= target < len(forms):
                    current_index = target
                else:
                    print(f"Invalid form number. Valid range: 1-{len(forms)}")
            except (ValueError, IndexError):
                print("Invalid command. Use: g [number]")
        elif command in ["s", "summary"]:
            print("\n" + "=" * 80)
            print("SUMMARY OF ALL FORMS")
            print("=" * 80)
            for i, form in enumerate(forms, 1):
                baseline = "⭐" if form.get("is_baseline") else "  "
                form_id = form.get("id", "?")
                categories = ", ".join(form.get("categories", []))[:30]
                risk_score = form.get("privacy_risk_comparison", {}).get("risk_score", "?")
                print(
                    f"{baseline} #{i:3d} | ID: {form_id:6} | Risk: {risk_score:2}/10 | {categories}"
                )
            print("=" * 80)
        else:
            print("Unknown command. Type 'q' to quit or 'n' for next.")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Explore forms from common_forms.jsonl",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive mode (default)
  python explore.py

  # Show specific form by ID
  python explore.py --id 8

  # Custom file path
  python explore.py --file my_forms.jsonl

  # Show specific form by ID from custom file
  python explore.py --file my_forms.jsonl --id 123
        """,
    )

    parser.add_argument(
        "--file",
        type=str,
        default="common_forms.jsonl",
        help="Path to JSONL file (default: common_forms.jsonl)",
    )
    parser.add_argument("--id", type=int, default=0, help="Show only the form with this ID")

    args = parser.parse_args()

    main(file_path=args.file, form_id=args.id)
