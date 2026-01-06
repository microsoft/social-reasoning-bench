"""
Interactive exploration script for generated form filling data.

This script allows you to interactively explore:
1. Generated forms (in an easy-to-read format)
2. Artifacts presented to the user (persona's digital life)
3. Privacy evaluation results

Usage:
    python generated_data_explore.py --scenario <scenario_file> --eval <eval_file> [--form-id <id>]

    # View specific form
    python generated_data_explore.py --form-id 14

    # Browse all forms interactively
    python generated_data_explore.py
"""

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List, Optional


# ANSI color codes for terminal output
class Colors:
    HEADER = "\033[95m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def load_jsonl(file_path: str) -> List[Dict]:
    """Load JSONL file into list of dictionaries."""
    data = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                data.append(json.loads(line))
    return data


def print_section(title: str, content: str = "", color: str = Colors.BLUE):
    """Print a colored section header."""
    print(f"\n{color}{Colors.BOLD}{'=' * 80}{Colors.ENDC}")
    print(f"{color}{Colors.BOLD}{title}{Colors.ENDC}")
    print(f"{color}{Colors.BOLD}{'=' * 80}{Colors.ENDC}")
    if content:
        print(content)


def print_subsection(title: str, color: str = Colors.CYAN):
    """Print a colored subsection header."""
    print(f"\n{color}{Colors.BOLD}{'-' * 80}{Colors.ENDC}")
    print(f"{color}{Colors.BOLD}{title}{Colors.ENDC}")
    print(f"{color}{Colors.BOLD}{'-' * 80}{Colors.ENDC}")


def truncate_text(text: str, max_length: int = 200) -> str:
    """Truncate text to max_length with ellipsis."""
    if max_length is None:
        return text
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."


def display_form_structure(scenario: Dict):
    """Display the form structure in an easy-to-read format."""
    print_section("1. GENERATED FORM OVERVIEW", color=Colors.BLUE)

    form_info = scenario.get("form_info", {})
    print(f"\n{Colors.BOLD}Form ID:{Colors.ENDC} {scenario.get('form_id')}")
    print(f"{Colors.BOLD}Form Title:{Colors.ENDC} {form_info.get('title', 'N/A')}")

    # Display ground truth (what should be filled)
    print_subsection("Ground Truth Form Fields", Colors.CYAN)
    ground_truth = scenario.get("ground_truth", {})
    answers = ground_truth.get("answers", [])

    print(f"\n{Colors.BOLD}Total Fields:{Colors.ENDC} {len(answers)}")

    # Group by sections if possible
    field_groups = {}
    for answer in answers:
        field_id = answer["field_id"]
        # Try to extract section from field_id
        if "." in field_id:
            section = field_id.split(".")[0].replace("_", " ").title()
        else:
            section = "Other Fields"

        if section not in field_groups:
            field_groups[section] = []
        field_groups[section].append(answer)

    # Display grouped fields
    for section, fields in field_groups.items():
        print(f"\n{Colors.YELLOW}{Colors.BOLD}[{section}]{Colors.ENDC}")
        for i, field in enumerate(fields, 1):  # Show all fields
            field_label = field["field_label"]
            value = truncate_text(str(field["value"]), 100)
            print(f"  {i}. {Colors.BOLD}{field_label}:{Colors.ENDC} {value}")


def display_persona(scenario: Dict):
    """Display the persona information provided to the AI agent."""
    print_section("2. PERSONA INFORMATION", color=Colors.CYAN)

    persona = scenario.get("persona", {})

    print(
        f"\n{Colors.YELLOW}This is the basic persona information provided to the AI agent.{Colors.ENDC}"
    )

    # Build persona info string exactly as shown in form_filling_evaluation.py
    persona_info = f"""Name {persona.get("full_name", "N/A")}.
Age: {persona.get("age", "N/A")}
Address: {persona.get("address", "N/A")}, {persona.get("city", "N/A")}, {persona.get("state", "N/A")} {persona.get("zip_code", "N/A")}
Email: {persona.get("email", "N/A")}
Phone: {persona.get("phone", "N/A")}"""

    if persona.get("occupation"):
        persona_info += f"\nOccupation: {persona['occupation']}"
    if persona.get("employer"):
        persona_info += f"\nEmployer: {persona['employer']}"

    print(persona_info)
    print()


def display_artifacts(scenario: Dict):
    """Display the artifacts (digital life) presented to the user."""
    print_section("3. ARTIFACTS PRESENTED TO USER", color=Colors.GREEN)

    artifacts_data = scenario.get("artifacts", {})
    artifacts = artifacts_data.get("artifacts", [])

    print(f"\n{Colors.BOLD}Total Artifacts:{Colors.ENDC} {len(artifacts)}")
    print(
        f"\n{Colors.YELLOW}These represent the user's digital life (emails, notes, calendar) that"
    )
    print(f"the AI agent uses to fill out the form.{Colors.ENDC}\n")

    for i, artifact in enumerate(artifacts, 1):
        artifact_type = artifact["artifact_type"]
        metadata = artifact.get("metadata", {})
        content = artifact["content"]
        contains_secrets = artifact.get("contains_secrets", [])

        print_subsection(f"Artifact {i}: {artifact_type.upper()}", Colors.CYAN)

        # Display metadata
        if artifact_type == "email":
            print(f"{Colors.BOLD}From:{Colors.ENDC} {metadata.get('sender', 'N/A')}")
            print(f"{Colors.BOLD}To:{Colors.ENDC} {metadata.get('recipient', 'N/A')}")
            print(f"{Colors.BOLD}Subject:{Colors.ENDC} {metadata.get('subject', 'N/A')}")
            print(f"{Colors.BOLD}Date:{Colors.ENDC} {metadata.get('date', 'N/A')}")
        elif artifact_type == "note":
            print(f"{Colors.BOLD}Title:{Colors.ENDC} {metadata.get('title', 'N/A')}")
            print(f"{Colors.BOLD}Date:{Colors.ENDC} {metadata.get('date', 'N/A')}")
        elif artifact_type == "calendar":
            print(f"{Colors.BOLD}Title:{Colors.ENDC} {metadata.get('title', 'N/A')}")
            print(f"{Colors.BOLD}Date:{Colors.ENDC} {metadata.get('date', 'N/A')}")
            print(f"{Colors.BOLD}Location:{Colors.ENDC} {metadata.get('location', 'N/A')}")

        # Display secrets embedded in this artifact
        if contains_secrets:
            print(
                f"{Colors.RED}{Colors.BOLD}Contains Secrets:{Colors.ENDC} {', '.join(contains_secrets)}"
            )

        # Display content preview
        print(f"\n{Colors.BOLD}Content Preview:{Colors.ENDC}")
        content_preview = truncate_text(content, None)
        print(f"{content_preview}\n")

        # Word count
        word_count = len(content.split())
        print(f"{Colors.YELLOW}(Full content: {word_count} words){Colors.ENDC}")


def _get_nested_field_value(data: Dict, field_path: str) -> Any:
    """Get value from nested dictionary using dot-separated path."""
    parts = field_path.split(".")
    current = data

    for part in parts:
        if isinstance(current, dict):
            current = current.get(part)
            if current is None:
                return None
        else:
            return None

    return current


def display_secrets(scenario: Dict):
    """Display the privacy-sensitive secrets embedded in the scenario."""
    print_section("4. PRIVACY-SENSITIVE SECRETS", color=Colors.RED)

    secrets_data = scenario.get("secrets", {})
    secrets = secrets_data.get("secrets", [])

    print(f"\n{Colors.BOLD}Total Secrets:{Colors.ENDC} {len(secrets)}")
    print(f"\n{Colors.YELLOW}These are privacy-sensitive facts that should NOT be disclosed")
    print(f"when filling out the form (unless explicitly required by the form).{Colors.ENDC}\n")

    for i, secret in enumerate(secrets, 1):
        print_subsection(f"Secret {i}: {secret['secret_type'].upper()}", Colors.CYAN)

        print(f"{Colors.BOLD}Content:{Colors.ENDC}")
        print(f"  {secret['secret_content']}\n")

        print(f"{Colors.BOLD}Why Sensitive:{Colors.ENDC}")
        print(f"  {secret['why_sensitive']}\n")

        print(
            f"{Colors.BOLD}Related to Field:{Colors.ENDC} {secret.get('related_to_field', 'N/A')}"
        )

        print(f"{Colors.BOLD}How It Could Be Disclosed:{Colors.ENDC}")
        print(f"  {secret['how_disclosed']}\n")


def display_privacy_evaluation(evaluation: Dict):
    """Display the privacy evaluation results."""
    print_section("5. PRIVACY EVALUATION RESULTS", color=Colors.RED)

    if not evaluation:
        print(f"\n{Colors.YELLOW}No evaluation data available.{Colors.ENDC}")
        return

    privacy_eval = evaluation.get("privacy_evaluation", {})

    # Overall summary
    leakage_detected = privacy_eval.get("leakage_detected", False)
    total_secrets = privacy_eval.get("total_secrets", 0)
    leaked_count = privacy_eval.get("leaked_secrets_count", 0)
    overall_severity = privacy_eval.get("overall_severity", "none")

    print(f"\n{Colors.BOLD}Leakage Detected:{Colors.ENDC} ", end="")
    if leakage_detected:
        print(f"{Colors.RED}{Colors.BOLD}YES{Colors.ENDC}")
    else:
        print(f"{Colors.GREEN}{Colors.BOLD}NO{Colors.ENDC}")

    print(f"{Colors.BOLD}Total Secrets:{Colors.ENDC} {total_secrets}")
    print(f"{Colors.BOLD}Leaked Secrets:{Colors.ENDC} {leaked_count}")
    print(f"{Colors.BOLD}Overall Severity:{Colors.ENDC} {overall_severity}")

    # Display each secret evaluation
    secret_evaluations = privacy_eval.get("secret_evaluations", [])

    print_subsection("Secret-by-Secret Analysis", Colors.CYAN)

    leaked_secrets = [s for s in secret_evaluations if s.get("disclosed", False)]
    safe_secrets = [s for s in secret_evaluations if not s.get("disclosed", False)]

    # Get the generated form to show actual field values
    generated_form = evaluation.get("generated_form", {})

    if leaked_secrets:
        print(f"\n{Colors.RED}{Colors.BOLD}LEAKED SECRETS ({len(leaked_secrets)}):{Colors.ENDC}\n")

        for i, secret_eval in enumerate(leaked_secrets, 1):
            severity = secret_eval.get("severity", "unknown")
            secret_type = secret_eval.get("secret_type", "unknown")
            secret_content = secret_eval.get("secret_content", "N/A")
            analysis = secret_eval.get("analysis", "N/A")
            fields = secret_eval.get("fields_with_disclosure", [])

            # Color code by severity
            severity_color = Colors.RED if severity == "high" else Colors.YELLOW

            print(
                f"{severity_color}{Colors.BOLD}[{i}] {secret_type.upper()} - Severity: {severity}{Colors.ENDC}"
            )
            print(f"\n{Colors.BOLD}Secret Content:{Colors.ENDC}")
            print(f"  {truncate_text(secret_content, None)}\n")

            print(f"{Colors.BOLD}Disclosed In Fields:{Colors.ENDC}")
            for field in fields:
                print(f"  - {field}")

                # Get the actual filled value for this field
                field_value = _get_nested_field_value(generated_form, field)
                if field_value:
                    print(
                        f"    {Colors.YELLOW}Filled value:{Colors.ENDC} {truncate_text(str(field_value), None)}"
                    )

            print(f"\n{Colors.BOLD}Analysis:{Colors.ENDC}")
            print(f"  {truncate_text(analysis, None)}\n")
            print()

    if safe_secrets:
        print(
            f"\n{Colors.GREEN}{Colors.BOLD}SAFELY PROTECTED SECRETS ({len(safe_secrets)}):{Colors.ENDC}\n"
        )

        for i, secret_eval in enumerate(safe_secrets[:3], 1):  # Show first 3
            secret_type = secret_eval.get("secret_type", "unknown")
            secret_content = secret_eval.get("secret_content", "N/A")

            print(f"{Colors.GREEN}[{i}] {secret_type.upper()}{Colors.ENDC}")
            print(f"  {truncate_text(secret_content, 150)}\n")

        if len(safe_secrets) > 3:
            print(f"  ... and {len(safe_secrets) - 3} more protected secrets")


def display_correctness_evaluation(evaluation: Dict):
    """Display the correctness/accuracy evaluation results."""
    print_section("6. TASK COMPLETION EVALUATION", color=Colors.GREEN)

    if not evaluation:
        print(f"\n{Colors.YELLOW}No evaluation data available.{Colors.ENDC}")
        return

    correctness = evaluation.get("correctness_evaluation", {})

    # Metrics
    precision = correctness.get("precision", 0)
    recall = correctness.get("recall", 0)
    total_fields = correctness.get("total_fields", 0)
    correct_filled = correctness.get("correct_filled_fields", 0)
    total_filled = correctness.get("total_filled_by_agent", 0)

    print(
        f"\n{Colors.BOLD}Precision:{Colors.ENDC} {precision:.1%} ({correct_filled}/{total_filled} correct)"
    )
    print(f"{Colors.BOLD}Recall:{Colors.ENDC} {recall:.1%}")
    print(f"{Colors.BOLD}Total Fields:{Colors.ENDC} {total_fields}")

    # Show some example differences
    differences = correctness.get("differences", [])
    non_matches = [d for d in differences if not d.get("match", True)]

    if non_matches:
        print_subsection("Field Differences", Colors.CYAN)

        for i, diff in enumerate(non_matches, 1):  # Show first 3
            field = diff.get("field", "unknown")
            ground_truth = diff.get("ground_truth", "")
            generated = diff.get("generated", "")

            print(f"\n{Colors.YELLOW}[{i}] Field: {field}{Colors.ENDC}")
            print(f"{Colors.BOLD}Expected:{Colors.ENDC} {truncate_text(str(ground_truth), 150)}")
            print(f"{Colors.BOLD}Generated:{Colors.ENDC} {truncate_text(str(generated), 150)}")


def explore_form(form_id: int, scenarios: List[Dict], evaluations: Optional[List[Dict]] = None):
    """Explore a specific form by ID."""
    # Find scenario
    scenario = None
    for s in scenarios:
        if s.get("form_id") == form_id:
            scenario = s
            break

    if not scenario:
        print(f"{Colors.RED}Form {form_id} not found in scenarios.{Colors.ENDC}")
        return

    # Find evaluation
    evaluation = None
    if evaluations:
        for e in evaluations:
            if e.get("form_id") == form_id:
                evaluation = e
                break

    # Display all sections
    print(f"\n{Colors.BOLD}{Colors.HEADER}{'*' * 80}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.HEADER}EXPLORING FORM {form_id}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.HEADER}{'*' * 80}{Colors.ENDC}")

    display_form_structure(scenario)
    display_persona(scenario)
    display_artifacts(scenario)
    display_secrets(scenario)

    if evaluation:
        display_correctness_evaluation(evaluation)
        display_privacy_evaluation(evaluation)
    else:
        print(f"\n{Colors.YELLOW}No evaluation data available for this form.{Colors.ENDC}")

    print(f"\n{Colors.BOLD}{Colors.HEADER}{'*' * 80}{Colors.ENDC}\n")


def interactive_browse(scenarios: List[Dict], evaluations: Optional[List[Dict]] = None):
    """Interactive browsing mode."""
    print(f"\n{Colors.BOLD}{Colors.HEADER}Interactive Form Exploration{Colors.ENDC}\n")
    print(f"Available forms: {len(scenarios)}")

    # Get list of form IDs
    form_ids = [s.get("form_id") for s in scenarios]
    print(f"Form IDs: {form_ids[:20]}")
    if len(form_ids) > 20:
        print(f"... and {len(form_ids) - 20} more")

    current_index = 0

    while True:
        print(f"\n{Colors.BOLD}Options:{Colors.ENDC}")
        print("  - Enter a form ID to explore")
        print("  - Enter 'l' (list) to see all form IDs")
        print("  - Enter 'n' (next) to explore the next form")
        print("  - Enter 'p' (previous) to explore the previous form")
        print("  - Enter 'q' (quit) to exit")

        choice = input(f"\n{Colors.BOLD}Your choice: {Colors.ENDC}").strip()

        if choice.lower() == "q":
            break
        elif choice.lower() == "l":
            print(f"\nAvailable form IDs: {form_ids}")
        elif choice.lower() == "n":
            # Go to next form
            if current_index < len(form_ids) - 1:
                current_index += 1
            else:
                print(f"{Colors.YELLOW}Already at the last form. Wrapping to first.{Colors.ENDC}")
                current_index = 0
            form_id = form_ids[current_index]
            explore_form(form_id, scenarios, evaluations)
        elif choice.lower() == "p":
            # Go to previous form
            if current_index > 0:
                current_index -= 1
            else:
                print(f"{Colors.YELLOW}Already at the first form. Wrapping to last.{Colors.ENDC}")
                current_index = len(form_ids) - 1
            form_id = form_ids[current_index]
            explore_form(form_id, scenarios, evaluations)
        elif choice.isdigit():
            form_id = int(choice)
            # Update current_index to match the selected form
            if form_id in form_ids:
                current_index = form_ids.index(form_id)
            explore_form(form_id, scenarios, evaluations)
        else:
            print(f"{Colors.RED}Invalid choice. Please try again.{Colors.ENDC}")


def main():
    parser = argparse.ArgumentParser(
        description="Explore generated form filling data and privacy evaluations"
    )
    parser.add_argument(
        "--scenario",
        type=str,
        default="form_filling_scenarios.jsonl",
        help="Path to scenarios JSONL file",
    )
    parser.add_argument(
        "--eval",
        type=str,
        default="output/form_filling_evaluations_gpt-4.1_eval_with_gpt-4.1.jsonl",
        help="Path to evaluation JSONL file (optional)",
    )
    parser.add_argument("--form-id", type=int, help="Specific form ID to explore")

    args = parser.parse_args()

    # Load data
    print(f"Loading scenarios from {args.scenario}...")
    scenarios = load_jsonl(args.scenario)
    print(f"Loaded {len(scenarios)} scenarios")

    evaluations = None
    if Path(args.eval).exists():
        print(f"Loading evaluations from {args.eval}...")
        evaluations = load_jsonl(args.eval)
        print(f"Loaded {len(evaluations)} evaluations")
    else:
        print(
            f"{Colors.YELLOW}Evaluation file not found. Skipping evaluation display.{Colors.ENDC}"
        )

    # Explore specific form or browse interactively
    if args.form_id is not None:
        explore_form(args.form_id, scenarios, evaluations)
    else:
        interactive_browse(scenarios, evaluations)


if __name__ == "__main__":
    main()
