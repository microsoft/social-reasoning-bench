#!/usr/bin/env python3
"""Plot comparison of leakage rates and CI violations between original and reeval.

Creates grouped bar charts showing:
- Original vs New leakage rate (by task)
- CI violations (from reeval only, since original doesn't have CI data)

Usage:
    python plot_leakage_comparison.py [--output OUTPUT_DIR]
"""

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def extract_timestamp(filepath: Path) -> str:
    """Extract timestamp from reeval filename, or empty string for base file."""
    match = re.search(r"-reeval-(\d{14})\.json", str(filepath))
    return match.group(1) if match else ""


def find_experiment_files(output_dir: Path) -> dict[str, dict]:
    """Find all experiment files and their reevals.

    Returns:
        Dict mapping experiment name to {
            'original': Path to original file,
            'reevals': List of (timestamp, Path) tuples sorted by timestamp
        }
    """
    experiments = defaultdict(lambda: {"original": None, "reevals": []})

    for json_file in output_dir.glob("*.json"):
        name = json_file.stem

        # Skip non-experiment files
        if (
            name
            in [
                "eval",
                "disagreement_data",
                "disagreement_data_full",
                "disagreement_data_full_v2",
                "disagreement_data_full_v3",
                "disagreement_data_full_v4",
            ]
            or "llm-traces" in name
        ):
            continue

        # Check if it's a reeval file
        if "-reeval" in name:
            # Extract base experiment name
            base_name = re.sub(r"-reeval(-\d{14})?$", "", name)
            timestamp = extract_timestamp(json_file)
            experiments[base_name]["reevals"].append((timestamp, json_file))
        else:
            experiments[name]["original"] = json_file

    # Sort reevals by timestamp
    for exp_data in experiments.values():
        exp_data["reevals"].sort(key=lambda x: x[0])

    return dict(experiments)


def load_leakage_data(filepath: Path) -> dict:
    """Load leakage statistics from a results file."""
    with open(filepath) as f:
        data = json.load(f)

    summary = data.get("summary", {})
    results = data.get("results", [])

    # Count tasks with leakage at result level
    tasks_with_leakage = sum(
        1 for r in results if r.get("leaked_secrets") and len(r["leaked_secrets"]) > 0
    )

    return {
        "total_tasks": summary.get("total_tasks", len(results)),
        "tasks_with_leakage": tasks_with_leakage,
        "leakage_rate": tasks_with_leakage / len(results) if results else 0,
        "avg_leakage_rate": summary.get("privacy_avg_leakage_rate", 0),
    }


def merge_reeval_results(original_path: Path, reeval_paths: list[Path]) -> dict:
    """Merge reeval results with original, newer reevals override older ones."""
    # Start with original
    with open(original_path) as f:
        merged_data = json.load(f)

    results_by_idx = {}
    for i, r in enumerate(merged_data.get("results", [])):
        execution = r.get("execution", {})
        task = execution.get("task", {})
        idx = task.get("id") if task.get("id") is not None else execution.get("task_index", i)
        results_by_idx[idx] = r

    # Apply reevals in order (older first, newer overrides)
    for reeval_path in reeval_paths:
        with open(reeval_path) as f:
            reeval_data = json.load(f)

        for i, r in enumerate(reeval_data.get("results", [])):
            execution = r.get("execution", {})
            task = execution.get("task", {})
            idx = task.get("id") if task.get("id") is not None else execution.get("task_index", i)
            if idx in results_by_idx:
                # Update leaked_secrets if present in reeval
                if "leaked_secrets" in r:
                    results_by_idx[idx]["leaked_secrets"] = r["leaked_secrets"]
                # Update ci_violations if present in reeval
                if "ci_violations" in r:
                    results_by_idx[idx]["ci_violations"] = r["ci_violations"]
                if "ci_violation_count" in r:
                    results_by_idx[idx]["ci_violation_count"] = r["ci_violation_count"]

    # Rebuild results list
    merged_data["results"] = [results_by_idx[i] for i in sorted(results_by_idx.keys())]

    return merged_data


def get_new_leakage_data(original_path: Path, reeval_paths: list[Path]) -> dict:
    """Get leakage and CI violation data from merged original + reevals."""
    if not reeval_paths:
        data = load_leakage_data(original_path)
        data["tasks_with_ci_violations"] = 0  # Original doesn't have CI data
        data["ci_violation_rate"] = 0
        return data

    merged = merge_reeval_results(original_path, reeval_paths)
    results = merged.get("results", [])

    tasks_with_leakage = sum(
        1 for r in results if r.get("leaked_secrets") and len(r["leaked_secrets"]) > 0
    )

    # Count tasks with CI violations
    tasks_with_ci_violations = sum(
        1 for r in results if r.get("ci_violations") and len(r["ci_violations"]) > 0
    )

    return {
        "total_tasks": len(results),
        "tasks_with_leakage": tasks_with_leakage,
        "leakage_rate": tasks_with_leakage / len(results) if results else 0,
        "tasks_with_ci_violations": tasks_with_ci_violations,
        "ci_violation_rate": tasks_with_ci_violations / len(results) if results else 0,
    }


def parse_experiment_name(name: str) -> tuple[str, str, str]:
    """Parse experiment name into (model, requestor_type, prompt_type).

    Examples:
        gpt-5.1-normal-default -> (gpt-5.1, normal, default)
        gpt-4o-malicious-privacy-ci -> (gpt-4o, malicious, privacy-ci)
    """
    parts = name.split("-")

    # Find where model ends and requestor type begins
    if "normal" in parts:
        idx = parts.index("normal")
    elif "malicious" in parts:
        idx = parts.index("malicious")
    else:
        return name, "unknown", "unknown"

    model = "-".join(parts[:idx])
    requestor = parts[idx]
    prompt = "-".join(parts[idx + 1 :]) if idx + 1 < len(parts) else "default"

    return model, requestor, prompt


def plot_leakage_comparison(experiments: dict[str, dict], output_dir: Path):
    """Create grouped bar chart comparing original leakage, new leakage, and CI violations."""
    # Collect data
    data = []
    for exp_name, exp_files in sorted(experiments.items()):
        if not exp_files["original"]:
            continue

        # Skip experiments with no valid tasks (e.g., failed gemini runs)
        original_data = load_leakage_data(exp_files["original"])
        if original_data["total_tasks"] == 0:
            continue
        reeval_paths = [p for _, p in exp_files["reevals"]]
        new_data = get_new_leakage_data(exp_files["original"], reeval_paths)

        model, requestor, prompt = parse_experiment_name(exp_name)

        has_reeval = len(reeval_paths) > 0

        data.append(
            {
                "name": exp_name,
                "model": model,
                "requestor": requestor,
                "prompt": prompt,
                "total_tasks": new_data["total_tasks"],
                "original_rate": original_data["leakage_rate"],
                "new_rate": new_data["leakage_rate"],
                "change": new_data["leakage_rate"] - original_data["leakage_rate"],
                "has_reeval": has_reeval,
                "tasks_with_ci_violations": new_data.get("tasks_with_ci_violations", 0),
                "ci_violation_rate": new_data.get("ci_violation_rate", 0),
            }
        )

    if not data:
        print("No experiments found with both original and reeval data")
        return

    # Sort by model, then requestor, then prompt
    data.sort(key=lambda x: (x["model"], x["requestor"], x["prompt"]))

    # Create figure with three bars per experiment
    fig, ax = plt.subplots(figsize=(20, 10))

    x = np.arange(len(data))
    width = 0.25  # Width of each bar

    # For experiments without reeval data, show 100% for all bars to indicate "no data"
    original_rates = [d["original_rate"] * 100 if d["has_reeval"] else 100 for d in data]
    new_rates = [d["new_rate"] * 100 if d["has_reeval"] else 100 for d in data]
    ci_rates = [d["ci_violation_rate"] * 100 if d["has_reeval"] else 100 for d in data]

    # Plot three side-by-side bars
    # Use gray for experiments without reeval data
    colors1 = ["#3498db" if d["has_reeval"] else "#999999" for d in data]
    colors2 = ["#e74c3c" if d["has_reeval"] else "#999999" for d in data]
    colors3 = ["#9b59b6" if d["has_reeval"] else "#999999" for d in data]

    bars1 = ax.bar(
        x - width, original_rates, width, label="Original Leakage", color=colors1, alpha=0.85
    )
    bars2 = ax.bar(x, new_rates, width, label="New Leakage (reeval)", color=colors2, alpha=0.85)
    bars3 = ax.bar(
        x + width, ci_rates, width, label="CI Violations (reeval)", color=colors3, alpha=0.85
    )

    # Labels
    labels = [f"{d['model']}\n{d['requestor']}\n{d['prompt']}" for d in data]
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=45, ha="right", fontsize=8)

    ax.set_ylabel("Tasks (%)")
    ax.set_title("Privacy Evaluation by Task: Leakage (Original vs New Judge) + CI Violations")
    ax.legend(loc="upper right")

    max_rate = max(max(original_rates), max(new_rates), max(ci_rates)) if data else 10
    ax.set_ylim(0, max_rate * 1.15 + 5)
    ax.yaxis.grid(True, linestyle="--", alpha=0.7)
    ax.set_axisbelow(True)

    # Add value labels on bars
    def add_labels(bars, rates):
        for bar, rate in zip(bars, rates):
            height = bar.get_height()
            ax.annotate(
                f"{rate:.1f}%",
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 3),
                textcoords="offset points",
                ha="center",
                va="bottom",
                fontsize=6,
                rotation=90,
            )

    add_labels(bars1, original_rates)
    add_labels(bars2, new_rates)
    add_labels(bars3, ci_rates)

    plt.tight_layout()

    # Save
    output_path = output_dir / "leakage_comparison.png"
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    print(f"Saved plot to {output_path}")

    # Also save as PDF
    pdf_path = output_dir / "leakage_comparison.pdf"
    plt.savefig(pdf_path, bbox_inches="tight")
    print(f"Saved plot to {pdf_path}")

    plt.close()

    # Print summary table
    print("\nSummary:")
    print(
        f"{'Experiment':<45} {'Tasks':>6} {'Orig Leak':>10} {'New Leak':>10} {'Change':>8} {'CI Viol%':>9} {'Reeval?':>8}"
    )
    print("-" * 110)
    for d in data:
        reeval_str = "Yes" if d["has_reeval"] else "No"
        ci_str = f"{d['ci_violation_rate'] * 100:.1f}%" if d["has_reeval"] else "N/A"
        print(
            f"{d['name']:<45} {d['total_tasks']:>6} {d['original_rate'] * 100:>9.1f}% {d['new_rate'] * 100:>9.1f}% {d['change'] * 100:>+7.1f}% {ci_str:>9} {reeval_str:>8}"
        )


def main():
    parser = argparse.ArgumentParser(description="Plot leakage comparison")
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        default=Path("outputs/calendar_scheduling/1-30-privacy_across_prompts/analysis"),
        help="Output directory for plots",
    )
    parser.add_argument(
        "--input",
        "-i",
        type=Path,
        default=Path("outputs/calendar_scheduling/1-30-privacy_across_prompts"),
        help="Input directory with experiment results",
    )
    args = parser.parse_args()

    args.output.mkdir(parents=True, exist_ok=True)

    experiments = find_experiment_files(args.input)
    print(f"Found {len(experiments)} experiments")

    for name, files in sorted(experiments.items()):
        reevals = len(files["reevals"])
        print(f"  {name}: original={'yes' if files['original'] else 'no'}, reevals={reevals}")

    plot_leakage_comparison(experiments, args.output)


if __name__ == "__main__":
    main()
