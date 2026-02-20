#!/usr/bin/env python3
"""Generate plots for large malicious whimsical sanity check with baseline comparison."""

import json
from pathlib import Path

import matplotlib.pyplot as plt


def load_result(output_dir: Path) -> dict | None:
    """Load the benchmark output JSON from a directory."""
    eval_file = output_dir / "eval.json"
    if not eval_file.exists():
        # Try to find eval.json in subdirectories
        for subdir in output_dir.iterdir():
            if subdir.is_dir():
                eval_file = subdir / "eval.json"
                if eval_file.exists():
                    break
    if not eval_file.exists():
        return None
    with open(eval_file) as f:
        return json.load(f)


def main():
    experiment_dir = Path(__file__).parent
    outputs_dir = experiment_dir / "outputs"

    # Load baseline result
    baseline = load_result(outputs_dir / "baseline")
    if not baseline:
        print("WARNING: Baseline results not found")
        baseline_summary = None
    else:
        baseline_summary = baseline["summary"]

    # Load malicious result
    malicious = load_result(outputs_dir / "malicious")
    if not malicious:
        print("ERROR: Malicious results not found")
        return

    malicious_summary = malicious["summary"]

    # Extract data
    mal_leakage = malicious_summary.get("privacy_avg_leakage_rate", 0) * 100
    mal_doc = malicious_summary.get("fiduciary_avg_assistant_duty_of_care_score", 0) * 100
    mal_tasks_with_leakage = malicious_summary.get("privacy_tasks_with_leakage", 0)
    total_tasks = malicious_summary.get("total_tasks", 140)

    if baseline_summary:
        base_leakage = baseline_summary.get("privacy_avg_leakage_rate", 0) * 100
        base_doc = baseline_summary.get("fiduciary_avg_assistant_duty_of_care_score", 0) * 100
        base_tasks_with_leakage = baseline_summary.get("privacy_tasks_with_leakage", 0)
    else:
        base_leakage = 0
        base_doc = 0
        base_tasks_with_leakage = 0

    # Per-task data for distributions
    mal_leakage_rates = []
    mal_doc_scores = []
    for task in malicious["results"]:
        leakage = task.get("leakage_rate", 0) or 0
        mal_leakage_rates.append(leakage * 100)
        doc = task.get("assistant_duty_of_care_score")
        if doc is not None:
            mal_doc_scores.append(doc * 100)

    # Create figure
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    fig.suptitle("Large Malicious Whimsical Sanity Check (140 tasks, GPT-5.1)", fontsize=14, fontweight="bold")

    # Plot 1: Leakage rate distribution with baseline marker
    ax1 = axes[0]
    ax1.hist(mal_leakage_rates, bins=20, color="#e74c3c", edgecolor="black", alpha=0.7, label="Malicious")
    ax1.axvline(x=mal_leakage, color="#e74c3c", linestyle="--", linewidth=2, label=f"Mal Avg: {mal_leakage:.1f}%")
    if baseline_summary:
        ax1.axvline(x=base_leakage, color="#2ecc71", linestyle="--", linewidth=2, label=f"Baseline: {base_leakage:.1f}%")
    ax1.set_xlabel("Leakage Rate (%)")
    ax1.set_ylabel("Number of Tasks")
    ax1.set_title("Privacy Leakage Distribution")
    ax1.legend()

    # Plot 2: Duty of care distribution with baseline marker
    ax2 = axes[1]
    ax2.hist(mal_doc_scores, bins=20, color="#3498db", edgecolor="black", alpha=0.7, label="Malicious")
    ax2.axvline(x=mal_doc, color="#3498db", linestyle="--", linewidth=2, label=f"Mal Avg: {mal_doc:.1f}%")
    if baseline_summary:
        ax2.axvline(x=base_doc, color="#2ecc71", linestyle="--", linewidth=2, label=f"Baseline: {base_doc:.1f}%")
    ax2.set_xlabel("Duty of Care (%)")
    ax2.set_ylabel("Number of Tasks")
    ax2.set_title("Duty of Care Distribution")
    ax2.legend()

    # Plot 3: Baseline vs Malicious comparison bar chart
    ax3 = axes[2]
    metrics = ["Leakage\nRate", "Duty of\nCare", "Tasks w/\nLeakage"]
    baseline_values = [base_leakage, base_doc, (base_tasks_with_leakage / total_tasks) * 100]
    malicious_values = [mal_leakage, mal_doc, (mal_tasks_with_leakage / total_tasks) * 100]

    x = range(len(metrics))
    width = 0.35

    bars1 = ax3.bar([i - width/2 for i in x], baseline_values, width, label="Baseline", color="#2ecc71", edgecolor="black")
    bars2 = ax3.bar([i + width/2 for i in x], malicious_values, width, label="Malicious", color="#e74c3c", edgecolor="black")

    ax3.set_ylabel("Percentage (%)")
    ax3.set_title("Baseline vs Malicious Comparison")
    ax3.set_xticks(x)
    ax3.set_xticklabels(metrics)
    ax3.set_ylim(0, 100)
    ax3.legend()

    # Add value labels
    for bar, val in zip(bars1, baseline_values):
        ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2, f"{val:.1f}%", ha="center", fontsize=9)
    for bar, val in zip(bars2, malicious_values):
        ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2, f"{val:.1f}%", ha="center", fontsize=9)

    plt.tight_layout()

    # Save plot
    output_path = experiment_dir / "results.png"
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    print(f"Saved plot to: {output_path}")

    plt.show()


if __name__ == "__main__":
    main()
