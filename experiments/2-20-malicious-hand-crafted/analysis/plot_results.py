#!/usr/bin/env python3
"""Plot privacy leakage: benign vs malicious hand-crafted, per model and dataset size.

Generates a grouped bar chart with one subplot per dataset size (small, large),
showing privacy leakage rate for each model comparing benign and malicious requestors.

Usage:
    uv run python experiments/2-20-malicious-hand-crafted/analysis/plot_results.py
"""

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

SCRIPT_DIR = Path(__file__).parent
OUTPUT_BASE = (
    SCRIPT_DIR.parent.parent.parent / "outputs/calendar_scheduling/2-20-malicious-hand-crafted"
)

MODELS = ["gpt-4.1", "gpt-5.1"]
SIZES = ["small", "large"]
SIZE_LABELS = {"small": "Small (n=21)", "large": "Large (n=140)"}

COLORS = {
    "benign": "#2D3047",
    "malicious": "#C44E52",
}


def load_eval(model: str, dataset: str) -> dict:
    path = OUTPUT_BASE / model / dataset / "eval.json"
    with open(path) as f:
        return json.load(f)


def style_axis(ax):
    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)
    for spine in ["left", "bottom"]:
        ax.spines[spine].set_linewidth(0.5)
    ax.tick_params(width=0.5)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f"{int(y)}%"))


def plot_privacy_leakage(output_path: Path):
    """Grouped bar chart: privacy leakage rate, one subplot per dataset size."""
    fig, axes = plt.subplots(1, len(SIZES), figsize=(5 * len(SIZES), 5), sharey=True)

    x = np.arange(len(MODELS))
    width = 0.3

    all_rates = []

    for idx, size in enumerate(SIZES):
        ax = axes[idx]

        benign_rates = []
        malicious_rates = []

        for model in MODELS:
            benign = load_eval(model, f"{size}-benign")
            malicious = load_eval(model, f"{size}-malicious-hand-crafted")
            benign_rates.append(benign["summary"]["privacy_leakage_rate"] * 100)
            malicious_rates.append(malicious["summary"]["privacy_leakage_rate"] * 100)

        all_rates.extend(benign_rates + malicious_rates)

        bars_benign = ax.bar(
            x - width / 2,
            benign_rates,
            width,
            label="Benign" if idx == 0 else None,
            color=COLORS["benign"],
            edgecolor="white",
        )
        bars_malicious = ax.bar(
            x + width / 2,
            malicious_rates,
            width,
            label="Malicious" if idx == 0 else None,
            color=COLORS["malicious"],
            edgecolor="white",
        )

        ax.set_xticks(x)
        ax.set_xticklabels(MODELS, fontsize=11)
        ax.set_title(SIZE_LABELS[size], fontsize=12, fontweight="semibold")

        if idx == 0:
            ax.set_ylabel("Privacy Leakage Rate (%)", fontsize=11)

        style_axis(ax)

        ax.bar_label(bars_benign, fmt="%.1f%%", padding=2, fontsize=10, fontweight="medium")
        ax.bar_label(bars_malicious, fmt="%.1f%%", padding=2, fontsize=10, fontweight="medium")

    # Set shared y-limit
    y_max = max(all_rates) * 1.3 + 5
    for ax in axes:
        ax.set_ylim(0, y_max)

    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(
        handles,
        labels,
        loc="upper center",
        bbox_to_anchor=(0.5, 0.97),
        ncol=2,
        frameon=False,
        fontsize=10,
    )

    fig.suptitle(
        "Privacy Leakage: Benign vs Malicious Requestor\n(hidden preferences)",
        fontsize=13,
        fontweight="semibold",
        y=1.03,
    )

    plt.tight_layout(rect=[0, 0, 1, 0.90])
    plt.savefig(output_path, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close()
    print(f"Saved: {output_path}")


def print_summary():
    print("=" * 60)
    print("Privacy Leakage Summary (hidden preferences)")
    print("=" * 60)
    for size in SIZES:
        print(f"\n--- {SIZE_LABELS[size]} ---")
        for model in MODELS:
            benign = load_eval(model, f"{size}-benign")
            malicious = load_eval(model, f"{size}-malicious-hand-crafted")
            b_rate = benign["summary"]["privacy_leakage_rate"] * 100
            m_rate = malicious["summary"]["privacy_leakage_rate"] * 100
            n = benign["metadata"]["task_count"]
            print(
                f"  {model} (n={n}): benign={b_rate:.1f}%  malicious={m_rate:.1f}%  Δ={m_rate - b_rate:+.1f}pp"
            )


def main():
    if not OUTPUT_BASE.exists():
        print(f"Output directory not found: {OUTPUT_BASE}")
        print("Run the experiment first: ./experiments/2-20-malicious-hand-crafted/run.sh")
        return

    print("Loading results...")
    print_summary()

    print("\nGenerating plot...")
    plot_privacy_leakage(SCRIPT_DIR / "privacy_leakage_benign_vs_malicious.png")


if __name__ == "__main__":
    main()
