#!/usr/bin/env python3
"""Plot duty of care results by model and expose_preferences condition.

Usage:
    uv run analysis/plot_duty_of_care.py

Output saved to analysis/duty_of_care_results.png
"""

import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

RESULTS_DIR = (
    Path(__file__).parent.parent.parent.parent
    / "outputs/calendar_scheduling/2-2-calendar_duty_of_care"
)
OUTPUT_PATH = Path(__file__).parent / "duty_of_care_results.png"


def load_results(base_dir: Path) -> dict:
    """Load experiment results, grouping by model and expose_preferences."""
    results = {}

    for json_file in base_dir.glob("*.json"):
        with open(json_file) as f:
            data = json.load(f)

        meta = data["metadata"]
        model = meta.get("assistant_model", "unknown").split("/")[-1]
        exposed = meta.get("expose_preferences", False)

        if model not in results:
            results[model] = {}

        condition = "exposed" if exposed else "not_exposed"
        results[model][condition] = {
            "assistant_duty_of_care": data["summary"]["fiduciary_avg_assistant_duty_of_care_score"],
            "task_success": data["summary"]["task_success_rate"],
            "preference_score": data["summary"]["fiduciary_avg_preference_score"],
            "task_count": meta.get("task_count", 0),
            "judge": meta.get("judge_model", "?").split("/")[-1],
        }
        print(f"Loaded {json_file.name}: {model}, exposed={exposed}")

    return results


def plot_results(results: dict, output_path: Path):
    """Create bar plot comparing duty of care with/without exposed preferences."""
    models = sorted(results.keys())
    n_models = len(models)

    # Extract data for 2 conditions (assistant only)
    asst_hidden = []
    asst_exposed = []

    for model in models:
        asst_hidden.append(
            results[model].get("not_exposed", {}).get("assistant_duty_of_care", 0) * 100
        )
        asst_exposed.append(
            results[model].get("exposed", {}).get("assistant_duty_of_care", 0) * 100
        )

    # Adaptive sizing based on number of models
    fig_width = max(8, 4 + n_models * 2)
    fig, ax = plt.subplots(figsize=(fig_width, 5))

    # 2 bars per model
    bar_labels = [
        "Hidden",
        "Exposed",
    ]
    n_bars = len(bar_labels)
    group_width = n_bars + 1  # Extra space between models

    x_positions = []
    for m in range(n_models):
        base = m * group_width
        x_positions.append([base, base + 1])

    colors = {
        "hidden": "#2D3047",
        "exposed": "#5C7ABF",
    }

    all_bars = []
    for m_idx, model in enumerate(models):
        pos = x_positions[m_idx]
        bars1 = ax.bar(pos[0], asst_hidden[m_idx], 0.9, color=colors["hidden"], edgecolor="white")
        bars2 = ax.bar(pos[1], asst_exposed[m_idx], 0.9, color=colors["exposed"], edgecolor="white")
        all_bars.extend([bars1, bars2])

    ax.set_ylabel("Duty of Care Score (%)", fontsize=11)
    ax.set_ylim(0, 115)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f"{int(y)}%"))

    # X-axis: bar labels for each position
    all_x = []
    all_labels = []
    for m_idx, model in enumerate(models):
        pos = x_positions[m_idx]
        all_x.extend(pos)
        all_labels.extend(bar_labels)

    ax.set_xticks(all_x)
    ax.set_xticklabels(all_labels, fontsize=9)

    # Add model name below bar groups
    for m_idx, model in enumerate(models):
        pos = x_positions[m_idx]
        center = (pos[0] + pos[-1]) / 2
        ax.text(center, -18, model, ha="center", fontsize=11, fontweight="semibold")

    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)
    for spine in ["left", "bottom"]:
        ax.spines[spine].set_linewidth(0.5)
    ax.tick_params(width=0.5)

    for bars in all_bars:
        ax.bar_label(bars, fmt="%.0f%%", padding=2, fontsize=9, fontweight="medium")

    # Add title and subtitle
    sample_data = next(iter(next(iter(results.values())).values()))
    n = sample_data.get("task_count", 0)
    judge = sample_data.get("judge", "?")
    subtitle = f"Judge: {judge}  ·  n={n} tasks per condition"

    fig.suptitle("Duty of Care Score by Model", fontsize=13, fontweight="semibold", y=0.97)
    fig.text(0.5, 0.91, subtitle, ha="center", fontsize=9, color="#555555", style="italic")

    plt.tight_layout(rect=[0, 0.05, 1, 0.89])
    plt.savefig(output_path, dpi=150, bbox_inches="tight", facecolor="white")
    print(f"Saved plot to {output_path}")


def main():
    if not RESULTS_DIR.exists():
        print(f"Error: Results directory {RESULTS_DIR} does not exist", file=sys.stderr)
        sys.exit(1)

    print(f"Loading results from: {RESULTS_DIR}")
    results = load_results(RESULTS_DIR)

    if not results:
        print("Error: No valid result files found", file=sys.stderr)
        sys.exit(1)

    print(f"\nFound {len(results)} model(s): {', '.join(results.keys())}")
    plot_results(results, OUTPUT_PATH)


if __name__ == "__main__":
    main()
