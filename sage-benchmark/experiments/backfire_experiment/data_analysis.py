#!/usr/bin/env python3
"""
Backfire Analysis Script for Privacy-CI Evaluation

Analyzes two JSON files (default vs CI) to compute:
1. Datapoint-wise backfire rate
2. Net change of secrets preserved
3. Top 10 strategies that backfire the most
"""

import json
import sys
from collections import defaultdict
from typing import Dict, List, Tuple


def load_json(filepath: str) -> dict:
    """Load JSON file."""
    with open(filepath, "r") as f:
        return json.load(f)


def extract_strategy_name(instruction: str) -> str:
    """Extract strategy name from instruction message."""
    import re

    # Look for **Strategy: Name** pattern anywhere in the text
    match = re.search(r"\*\*Strategy:\s*(.*?)\*\*", instruction)
    if match:
        return match.group(1).strip()

    # Fallback: look for any bold text after "Strategy:"
    if "Strategy:" in instruction:
        after = instruction.split("Strategy:")[-1]
        match = re.search(r"\*\*(.*?)\*\*", after)
        if match:
            return match.group(1).strip()
        # Fallback to first line
        first_line = after.strip().split("\n")[0].strip()
        return first_line[:100]

    return "Unknown Strategy"


def analyze_backfire(default_file: str, ci_file: str) -> Dict:
    """
    Analyze backfire between default and CI prompts.

    Returns:
        Dictionary containing:
        - backfire_rate: percentage of tasks where CI leaked more
        - net_secrets_preserved: total secrets saved - total extra leaked
        - top_backfires: list of top 10 worst backfire cases
        - detailed_stats: comprehensive statistics
    """
    # Load data
    default_data = load_json(default_file)
    ci_data = load_json(ci_file)

    # Build lookup by task_index for each file
    default_by_index = {}
    for result in default_data["results"]:
        idx = result["execution"]["task_index"]
        default_by_index[idx] = result

    ci_by_index = {}
    for result in ci_data["results"]:
        idx = result["execution"]["task_index"]
        ci_by_index[idx] = result

    # Find comparable datapoints by iterating over task indices 0-49
    comparisons = []

    for i in range(50):
        if i not in default_by_index or i not in ci_by_index:
            continue

        default_result = default_by_index[i]
        ci_result = ci_by_index[i]

        # Check if both are valid
        default_valid = default_result["execution"].get("is_valid", False)
        ci_valid = ci_result["execution"].get("is_valid", False)

        if not (default_valid and ci_valid):
            continue

        # Get task info
        task = default_result["execution"]["task"]
        task_id = task.get("task_id", f"task_{i}")

        # Extract strategy name
        instruction = task["requestor"].get("instruction_message", "")
        strategy_name = extract_strategy_name(instruction)

        # Count leaked secrets
        default_leaked = len(default_result.get("leaked_secrets", []))
        ci_leaked = len(ci_result.get("leaked_secrets", []))

        # Calculate difference
        difference = ci_leaked - default_leaked

        comparisons.append(
            {
                "task_index": i,
                "task_id": task_id,
                "strategy": strategy_name,
                "default_leaked": default_leaked,
                "ci_leaked": ci_leaked,
                "difference": difference,
                "is_backfire": difference > 0,
                "is_improvement": difference < 0,
                "is_same": difference == 0,
            }
        )

    # Calculate statistics
    total_tasks = len(comparisons)
    backfires = [c for c in comparisons if c["is_backfire"]]
    improvements = [c for c in comparisons if c["is_improvement"]]
    same = [c for c in comparisons if c["is_same"]]

    # (1) Datapoint-wise backfire rate
    backfire_rate = len(backfires) / total_tasks if total_tasks > 0 else 0

    # (2) Net change of secrets preserved
    total_saved = sum(abs(c["difference"]) for c in improvements)
    total_extra = sum(c["difference"] for c in backfires)
    net_preserved = total_saved - total_extra

    # (3) Top 10 strategies that backfire the most
    # Sort by difference (most positive = worst backfire)
    top_backfires = sorted(backfires, key=lambda x: x["difference"], reverse=True)[:10]

    # Additional statistics
    avg_improvement = (
        sum(abs(c["difference"]) for c in improvements) / len(improvements) if improvements else 0
    )
    avg_backfire = sum(c["difference"] for c in backfires) / len(backfires) if backfires else 0

    benefit_ratio = total_saved / total_extra if total_extra > 0 else float("inf")

    return {
        "total_tasks": total_tasks,
        "backfire_rate": backfire_rate,
        "backfire_count": len(backfires),
        "improvement_count": len(improvements),
        "same_count": len(same),
        "net_secrets_preserved": net_preserved,
        "total_saved": total_saved,
        "total_extra_leaked": total_extra,
        "benefit_ratio": benefit_ratio,
        "avg_improvement": avg_improvement,
        "avg_backfire": avg_backfire,
        "top_backfires": top_backfires,
        "all_comparisons": comparisons,
    }


def print_results(results: Dict, model_name: str = "Model"):
    """Print analysis results in a formatted way."""
    print("=" * 80)
    print(f"BACKFIRE ANALYSIS: {model_name}")
    print("=" * 80)

    print(f"\nTotal comparable tasks: {results['total_tasks']}")

    print("\n" + "-" * 80)
    print("(1) DATAPOINT-WISE BACKFIRE RATE")
    print("-" * 80)
    print(
        f"Backfire rate: {results['backfire_rate']:.1%} ({results['backfire_count']}/{results['total_tasks']} tasks)"
    )
    print(
        f"  CI better:  {results['improvement_count']} tasks ({100 * results['improvement_count'] / results['total_tasks']:.1f}%)"
    )
    print(
        f"  CI worse:   {results['backfire_count']} tasks ({100 * results['backfire_count'] / results['total_tasks']:.1f}%)"
    )
    print(
        f"  Same:       {results['same_count']} tasks ({100 * results['same_count'] / results['total_tasks']:.1f}%)"
    )

    print("\n" + "-" * 80)
    print("(2) NET CHANGE OF SECRETS PRESERVED")
    print("-" * 80)
    print(f"Total secrets saved (improvements): {results['total_saved']}")
    print(f"Total secrets lost (backfires):     {results['total_extra_leaked']}")
    print(f"Net secrets preserved:              {results['net_secrets_preserved']:+d}")

    if results["benefit_ratio"] != float("inf"):
        print(f"Benefit-to-cost ratio:              {results['benefit_ratio']:.1f}:1")
    else:
        print(f"Benefit-to-cost ratio:              ∞ (no backfires)")

    print(f"\nAverage improvement (when CI helps): {results['avg_improvement']:.1f} secrets")
    print(f"Average backfire (when CI hurts):    {results['avg_backfire']:.1f} secrets")

    print("\n" + "-" * 80)
    print("(3) TOP 10 STRATEGIES THAT BACKFIRE THE MOST")
    print("-" * 80)

    if not results["top_backfires"]:
        print("\n✓ No backfires found - CI never performed worse than default!")
    else:
        print(f"\n{'Rank':<6}{'Task':<8}{'Default→CI':<15}{'Backfire':<12}{'Strategy':<50}")
        print("-" * 80)
        for i, backfire in enumerate(results["top_backfires"], 1):
            task_str = f"#{backfire['task_index']}"
            leak_str = f"{backfire['default_leaked']}→{backfire['ci_leaked']}"
            backfire_str = f"+{backfire['difference']}"
            strategy_str = (
                backfire["strategy"][:47] + "..."
                if len(backfire["strategy"]) > 50
                else backfire["strategy"]
            )
            print(f"{i:<6}{task_str:<8}{leak_str:<15}{backfire_str:<12}{strategy_str}")

    print("\n" + "=" * 80)


def main():
    """Main function."""
    if len(sys.argv) < 3:
        print("Usage: python analyze_backfire.py <default_file.json> <ci_file.json> [model_name]")
        print("\nExample:")
        print("  python analyze_backfire.py qwen-default.json qwen-ci.json 'Qwen 2.5 7B'")
        sys.exit(1)

    default_file = sys.argv[1]
    ci_file = sys.argv[2]
    model_name = sys.argv[3] if len(sys.argv) > 3 else "Model"

    # Run analysis
    results = analyze_backfire(default_file, ci_file)

    # Print results
    print_results(results, model_name)

    # Optionally save detailed results to JSON
    if len(sys.argv) > 4 and sys.argv[4] == "--save":
        output_file = f"{model_name.lower().replace(' ', '_')}_backfire_analysis.json"
        with open(output_file, "w") as f:
            # Convert to JSON-serializable format
            output_data = {
                "model": model_name,
                "statistics": {
                    "total_tasks": results["total_tasks"],
                    "backfire_rate": results["backfire_rate"],
                    "backfire_count": results["backfire_count"],
                    "improvement_count": results["improvement_count"],
                    "same_count": results["same_count"],
                    "net_secrets_preserved": results["net_secrets_preserved"],
                    "total_saved": results["total_saved"],
                    "total_extra_leaked": results["total_extra_leaked"],
                    "benefit_ratio": results["benefit_ratio"]
                    if results["benefit_ratio"] != float("inf")
                    else None,
                    "avg_improvement": results["avg_improvement"],
                    "avg_backfire": results["avg_backfire"],
                },
                "top_backfires": results["top_backfires"],
                "all_comparisons": results["all_comparisons"],
            }
            json.dump(output_data, f, indent=2)
        print(f"\nDetailed results saved to: {output_file}")


if __name__ == "__main__":
    main()
