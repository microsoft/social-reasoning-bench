#!/usr/bin/env python3
"""Plot duty-of-care heatmap for the 3-03 malicious strategy isolation experiment.

Produces a heatmap grid:
- 3 vertically stacked subplots (one per assistant model)
- Each subplot has 2 rows (hidden / exposed preferences)
- 10 columns (one per dataset)
- Green color scale: duty-of-care score 0-100 (darker = higher = better)

Usage:
    uv run python experiments/3-03-malicious-cal-more/plot_results.py
    uv run python experiments/3-03-malicious-cal-more/plot_results.py \
        --input-dir outputs/calendar_scheduling/3-03-malicious-cal-more
"""

import argparse
import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

MODELS = ["gpt4.1-cot", "gpt5.2-medium", "gemini-3-flash-medium"]
MODEL_LABELS = {
    "gpt4.1-cot": "GPT-4.1 (CoT)",
    "gpt5.2-medium": "GPT-5.2 (Medium)",
    "gemini-3-flash-medium": "Gemini 3 Flash (Medium)",
}

DATASETS = [
    "benign",
    "mal-hc-privacy",
    "mal-hc-doc",
    "mal-whim-privacy",
    "mal-whim-doc",
    "doc-strat-1",
    "doc-strat-5",
    "doc-strat-6",
    "doc-strat-7",
    "doc-strat-8",
]
DATASET_LABELS = {
    "benign": "Benign",
    "mal-hc-privacy": "Hand Craft\nPrivacy",
    "mal-hc-doc": "Hand Craft\nDoC",
    "mal-whim-privacy": "Whim.\nPrivacy",
    "mal-whim-doc": "Whim.\nDoC",
    "doc-strat-1": "DoC Whim\nStrat 1",
    "doc-strat-5": "DoC Whim\nStrat 5",
    "doc-strat-6": "DoC Whim\nStrat 6",
    "doc-strat-7": "DoC Whim\nStrat 7",
    "doc-strat-8": "DoC Whim\nStrat 8",
}

PREF_SETTINGS = ["prefs-hidden", "prefs-exposed"]
PREF_LABELS = {"prefs-hidden": "Hidden", "prefs-exposed": "Exposed"}

GREEN_CMAP = "YlGn"


def load_eval(base_dir: Path, variant: str) -> dict | None:
    path = base_dir / variant / "eval.json"
    if not path.exists():
        print(f"  Warning: missing {path}", file=sys.stderr)
        return None
    with open(path) as f:
        return json.load(f)


def plot_heatmap(data: dict[str, np.ndarray], output_path: Path, subtitle: str = ""):
    n_datasets = len(DATASETS)
    n_models = len(MODELS)

    fig, axes = plt.subplots(
        n_models,
        1,
        figsize=(max(12, 1.4 * n_datasets), 2.5 * n_models),
    )
    if n_models == 1:
        axes = [axes]

    for ax_idx, model in enumerate(MODELS):
        ax = axes[ax_idx]
        arr = data[model]

        im = ax.imshow(
            arr,
            cmap=GREEN_CMAP,
            vmin=0,
            vmax=100,
            aspect="auto",
            interpolation="nearest",
        )

        for row in range(2):
            for col in range(n_datasets):
                val = arr[row, col]
                if not np.isnan(val):
                    text_color = "white" if val > 60 else "black"
                    ax.text(
                        col,
                        row,
                        f"{val:.0f}%",
                        ha="center",
                        va="center",
                        fontsize=9,
                        fontweight="bold",
                        color=text_color,
                    )
                else:
                    ax.text(col, row, "—", ha="center", va="center", fontsize=9, color="#999")

        ax.set_yticks(range(2))
        ax.set_yticklabels([PREF_LABELS[p] for p in PREF_SETTINGS], fontsize=9)
        ax.set_xticks(range(n_datasets))
        ds_labels = [DATASET_LABELS[d] for d in DATASETS]
        if ax_idx == n_models - 1:
            ax.set_xticklabels(ds_labels, fontsize=8, ha="center")
        else:
            ax.set_xticklabels([])
        ax.set_title(MODEL_LABELS[model], fontsize=11, fontweight="semibold", pad=8)
        ax.tick_params(length=0)

    fig.subplots_adjust(top=0.85, hspace=0.45, right=0.88)
    fig.text(
        0.5,
        1.0,
        "Duty of Care by Malicious Strategy",
        ha="center",
        va="top",
        fontsize=14,
        fontweight="semibold",
    )
    sub = subtitle or "Requestor: GPT-4.1 | Small Dataset | 10 Variants | Hidden vs Exposed Prefs"
    fig.text(0.5, 0.96, sub, ha="center", va="top", fontsize=11, color="#555555")

    cbar_ax = fig.add_axes([0.90, 0.15, 0.02, 0.65])
    cbar = fig.colorbar(im, cax=cbar_ax)
    cbar.set_label("Duty of Care Score", fontsize=9)
    cbar.ax.tick_params(labelsize=8)

    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Saved heatmap to {output_path}")


def _avg_doc_score(eval_data: dict, min_free_slots: int | None = None) -> float | None:
    """Compute average duty-of-care score, optionally filtering by free_slots_count."""
    if min_free_slots is None:
        score = eval_data["summary"].get("fiduciary_avg_assistant_duty_of_care_score")
        return score if score is not None else None
    scores = []
    for r in eval_data.get("results", []):
        free_slots = r.get("execution", {}).get("task", {}).get("free_slots_count")
        if free_slots is not None and free_slots > min_free_slots:
            doc = r.get("assistant_duty_of_care_score")
            if doc is not None:
                scores.append(doc)
    return sum(scores) / len(scores) if scores else None


def load_data(
    base_dir: Path,
    min_free_slots: int | None = None,
) -> dict[str, np.ndarray]:
    """Load all data into {model: (2, n_datasets)} arrays."""
    n_datasets = len(DATASETS)
    data = {}
    for model in MODELS:
        arr = np.full((2, n_datasets), np.nan)
        for row, pref in enumerate(PREF_SETTINGS):
            for col, ds in enumerate(DATASETS):
                variant = f"{model}_{pref}_{ds}"
                result = load_eval(base_dir, variant)
                if result:
                    score = _avg_doc_score(result, min_free_slots)
                    if score is not None:
                        arr[row, col] = score * 100
        data[model] = arr
    return data


def load_leakage_data(base_dir: Path) -> dict[str, np.ndarray]:
    """Load privacy leakage rate (% of tasks with any leak) into {model: (2, n_datasets)}."""
    n_datasets = len(DATASETS)
    data = {}
    for model in MODELS:
        arr = np.full((2, n_datasets), np.nan)
        for row, pref in enumerate(PREF_SETTINGS):
            for col, ds in enumerate(DATASETS):
                variant = f"{model}_{pref}_{ds}"
                result = load_eval(base_dir, variant)
                if result:
                    rate = result["summary"].get("privacy_leakage_rate")
                    if rate is not None:
                        arr[row, col] = rate * 100
        data[model] = arr
    return data


def plot_bars(
    data: dict[str, np.ndarray],
    output_path: Path,
    subtitle: str = "",
    title: str = "Duty of Care by Malicious Strategy",
    ylabel: str = "Duty of Care %",
):
    n_datasets = len(DATASETS)
    n_models = len(MODELS)
    bar_width = 0.35
    x = np.arange(n_datasets)

    fig, axes = plt.subplots(
        n_models,
        1,
        figsize=(max(12, 1.4 * n_datasets), 3.0 * n_models),
    )
    if n_models == 1:
        axes = [axes]

    for ax_idx, model in enumerate(MODELS):
        ax = axes[ax_idx]
        arr = data[model]
        hidden = arr[0]
        exposed = arr[1]

        bars_h = ax.bar(x - bar_width / 2, hidden, bar_width, label="Hidden", color="#1f77b4")
        bars_e = ax.bar(x + bar_width / 2, exposed, bar_width, label="Exposed", color="#e67e22")

        for bar in bars_h:
            h = bar.get_height()
            if not np.isnan(h):
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    h + 1,
                    f"{h:.0f}%",
                    ha="center",
                    va="bottom",
                    fontsize=7,
                    fontweight="bold",
                )
        for bar in bars_e:
            h = bar.get_height()
            if not np.isnan(h):
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    h + 1,
                    f"{h:.0f}%",
                    ha="center",
                    va="bottom",
                    fontsize=7,
                    fontweight="bold",
                )

        ax.set_ylim(0, 115)
        ax.set_ylabel(ylabel, fontsize=9)
        ax.set_xticks(x)
        ds_labels = [DATASET_LABELS[d] for d in DATASETS]
        ax.set_xticklabels(ds_labels, fontsize=8, ha="center")
        ax.set_title(MODEL_LABELS[model], fontsize=11, fontweight="semibold", pad=8)
        if ax_idx == 0:
            ax.legend(fontsize=9, loc="upper right")

    fig.subplots_adjust(top=0.85, hspace=0.45)
    fig.text(
        0.5,
        1.0,
        title,
        ha="center",
        va="top",
        fontsize=14,
        fontweight="semibold",
    )
    sub = subtitle or "Requestor: GPT-4.1 | Small Dataset | 10 Variants | Hidden vs Exposed Prefs"
    fig.text(0.5, 0.96, sub, ha="center", va="top", fontsize=11, color="#555555")

    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Saved bar chart to {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Plot 3-03 malicious strategy heatmap")
    parser.add_argument(
        "--input-dir",
        type=Path,
        default=Path("outputs/calendar_scheduling/3-03-malicious-cal-more"),
        help="Base directory with eval results",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Output image path (default: <input-dir>/duty_of_care_heatmap.png)",
    )
    args = parser.parse_args()

    if not args.input_dir.exists():
        print(f"Error: {args.input_dir} does not exist", file=sys.stderr)
        sys.exit(1)

    output_path = args.output or args.input_dir / "duty_of_care_heatmap.png"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # All tasks
    data_all = load_data(args.input_dir)
    plot_heatmap(data_all, output_path)
    plot_bars(data_all, output_path.with_name("duty_of_care_bars.png"))

    # Privacy leakage (all tasks)
    leakage_data = load_leakage_data(args.input_dir)
    plot_bars(
        leakage_data,
        output_path.with_name("privacy_leakage_bars.png"),
        title="Privacy Leakage by Malicious Strategy",
        ylabel="% Tasks with Leakage",
    )

    # Filtered: only tasks with free_slots > 1 (15 of 21 tasks)
    filtered_subtitle = (
        "Requestor: GPT-4.1 | Small Dataset | 10 Variants | "
        "Hidden vs Exposed | free_slots > 1 (15/21 tasks)"
    )
    data_filtered = load_data(args.input_dir, min_free_slots=1)
    plot_heatmap(
        data_filtered,
        output_path.with_name("duty_of_care_heatmap_filtered.png"),
        subtitle=filtered_subtitle,
    )
    plot_bars(
        data_filtered,
        output_path.with_name("duty_of_care_bars_filtered.png"),
        subtitle=filtered_subtitle,
    )


if __name__ == "__main__":
    main()
