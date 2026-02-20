#!/usr/bin/env python3
"""Generate comparison plots for whimsical strategy experiment."""

import json
from pathlib import Path

import matplotlib.pyplot as plt


def load_result(output_dir: Path) -> dict | None:
    """Load the benchmark output JSON from a directory."""
    eval_file = output_dir / "eval.json"
    if not eval_file.exists():
        return None
    with open(eval_file) as f:
        return json.load(f)


def main():
    experiment_dir = Path(__file__).parent
    outputs_dir = experiment_dir / "outputs"

    # Load all results
    results = []

    # Baseline
    baseline = load_result(outputs_dir / "baseline")
    if baseline:
        results.append(
            {
                "name": "Baseline",
                "leakage": baseline["summary"].get("privacy_avg_leakage_rate", 0),
                "doc": baseline["summary"].get("fiduciary_avg_assistant_duty_of_care_score", 1),
                "is_baseline": True,
            }
        )

    # Strategies
    for i in range(10):
        result = load_result(outputs_dir / f"strategy_{i}")
        if result:
            results.append(
                {
                    "name": f"Strategy {i}",
                    "leakage": result["summary"].get("privacy_avg_leakage_rate", 0),
                    "doc": result["summary"].get("fiduciary_avg_assistant_duty_of_care_score", 1),
                    "is_baseline": False,
                }
            )

    # Create figure with 3 subplots
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    fig.suptitle("Whimsical Strategy Selection Experiment Results", fontsize=14, fontweight="bold")

    # Plot 1: Leakage Rate Bar Chart
    ax1 = axes[0]
    names = [r["name"] for r in results]
    leakages = [r["leakage"] * 100 for r in results]
    colors = ["#2ecc71" if r["is_baseline"] else "#e74c3c" for r in results]
    bars = ax1.bar(names, leakages, color=colors, edgecolor="black", linewidth=0.5)
    ax1.set_ylabel("Leakage Rate (%)")
    ax1.set_title("Privacy Leakage Rate by Run")
    ax1.axhline(y=results[0]["leakage"] * 100, color="#2ecc71", linestyle="--", alpha=0.7)
    ax1.set_ylim(0, max(leakages) * 1.2)
    ax1.tick_params(axis="x", rotation=45)
    for bar, val in zip(bars, leakages):
        ax1.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.5,
            f"{val:.1f}%",
            ha="center",
            va="bottom",
            fontsize=8,
        )

    # Plot 2: Duty of Care Bar Chart
    ax2 = axes[1]
    docs = [r["doc"] * 100 for r in results]
    colors = ["#2ecc71" if r["is_baseline"] else "#3498db" for r in results]
    bars = ax2.bar(names, docs, color=colors, edgecolor="black", linewidth=0.5)
    ax2.set_ylabel("Duty of Care (%)")
    ax2.set_title("Assistant Duty of Care by Run")
    ax2.axhline(y=results[0]["doc"] * 100, color="#2ecc71", linestyle="--", alpha=0.7)
    ax2.set_ylim(0, 110)
    ax2.tick_params(axis="x", rotation=45)
    for bar, val in zip(bars, docs):
        ax2.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 1,
            f"{val:.0f}%",
            ha="center",
            va="bottom",
            fontsize=8,
        )

    # Plot 3: Scatter plot - Leakage vs Duty of Care
    ax3 = axes[2]
    for r in results:
        color = "#2ecc71" if r["is_baseline"] else "#e74c3c"
        size = 200 if r["is_baseline"] else 100
        ax3.scatter(
            r["doc"] * 100,
            r["leakage"] * 100,
            c=color,
            s=size,
            edgecolors="black",
            linewidth=1,
            zorder=5,
        )
        ax3.annotate(
            r["name"].replace("Strategy ", "S"),
            (r["doc"] * 100, r["leakage"] * 100),
            textcoords="offset points",
            xytext=(5, 5),
            fontsize=8,
        )

    ax3.set_xlabel("Duty of Care (%) - Lower = Worse for User")
    ax3.set_ylabel("Leakage Rate (%) - Higher = More Privacy Violation")
    ax3.set_title("Privacy vs Duty of Care Trade-off")
    ax3.set_xlim(-5, 105)
    ax3.set_ylim(-2, max([r["leakage"] * 100 for r in results]) * 1.2)

    # Add quadrant labels
    ax3.axhline(y=results[0]["leakage"] * 100, color="gray", linestyle=":", alpha=0.5)
    ax3.axvline(x=results[0]["doc"] * 100, color="gray", linestyle=":", alpha=0.5)
    ax3.text(
        5,
        max([r["leakage"] * 100 for r in results]) * 1.1,
        "High Impact\n(bad for user)",
        fontsize=9,
        color="red",
        alpha=0.7,
    )
    ax3.text(90, 1, "Low Impact\n(good for user)", fontsize=9, color="green", alpha=0.7)

    plt.tight_layout()

    # Save plot
    output_path = experiment_dir / "results_comparison.png"
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    print(f"Saved plot to: {output_path}")

    plt.show()


if __name__ == "__main__":
    main()
