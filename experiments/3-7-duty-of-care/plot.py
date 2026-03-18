"""Plot duty-of-care score grid: models x datasets x preference visibility.

Auto-discovers experiments from the input directory. Use --models,
--datasets, --prefs to filter.

Usage:
    # Auto-discover everything
    uv run python experiments/3-7-duty-of-care/plot.py

    # Filter to specific models and datasets
    uv run python experiments/3-7-duty-of-care/plot.py \
        --models gpt4.1-cot gemini-3-flash-medium \
        --datasets benign mal-hc-double-booking
"""

import argparse
import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle

# Display labels
LABEL_MAP = {
    "gpt4.1-cot": "GPT-4.1 (CoT)",
    "gpt5.2-medium": "GPT-5.2 (Medium)",
    "gemini-3-flash-medium": "Gemini 3 Flash (Medium)",
    "benign": "Benign",
    "mal-hc-double-booking": "Malicious HC (Double Booking)",
    "mal-whim-double-booking": "Malicious Whim. (Double Booking)",
    "prefs-hidden": "Prefs Hidden",
    "prefs-exposed": "Prefs Exposed",
}

COLORS = [
    "#5C7ABF",
    "#2D3047",
    "#8B5CF6",
    "#D97706",
    "#059669",
    "#DC2626",
    "#7C3AED",
    "#EA580C",
]


def label(key: str) -> str:
    return LABEL_MAP.get(key, key)


def discover(base_dir: Path):
    """Scan eval.json dirs and return sorted lists of (models, prefs, datasets)."""
    models, prefs, datasets = set(), set(), set()
    for d in base_dir.iterdir():
        if not d.is_dir() or not (d / "eval.json").exists():
            continue
        parts = d.name.split("_")
        for i in range(1, len(parts)):
            for j in range(i + 1, len(parts)):
                m = "_".join(parts[:i])
                p = "_".join(parts[i:j])
                ds = "_".join(parts[j:])
                if f"{m}_{p}_{ds}" == d.name:
                    models.add(m)
                    prefs.add(p)
                    datasets.add(ds)
    return sorted(models), sorted(prefs), sorted(datasets)


def load_eval(base_dir: Path, variant: str) -> dict | None:
    path = base_dir / variant / "eval.json"
    if not path.exists():
        return None
    with open(path) as f:
        return json.load(f)


def main():
    parser = argparse.ArgumentParser(description="Plot duty-of-care score grid")
    parser.add_argument(
        "--input-dir",
        type=Path,
        default=Path("outputs/calendar_scheduling/3-7-duty-of-care/validation"),
    )
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument("--models", nargs="+", default=None)
    parser.add_argument("--datasets", nargs="+", default=None)
    parser.add_argument("--prefs", nargs="+", default=None)
    args = parser.parse_args()

    if not args.input_dir.exists():
        print(f"Error: {args.input_dir} does not exist", file=sys.stderr)
        sys.exit(1)

    all_models, all_prefs, all_datasets = discover(args.input_dir)
    models = args.models or all_models
    prefs = args.prefs or all_prefs
    datasets = args.datasets or all_datasets

    if not models or not prefs or not datasets:
        print("No experiments found.", file=sys.stderr)
        sys.exit(1)

    print(f"Models:   {models}")
    print(f"Prefs:    {prefs}")
    print(f"Datasets: {datasets}")

    n_rows = len(datasets)
    n_cols = len(models)
    fig, axes = plt.subplots(
        n_rows,
        n_cols,
        figsize=(4.0 * n_cols, 3.0 * n_rows),
        sharey=True,
        squeeze=False,
    )

    x = np.arange(len(prefs))
    colors = COLORS[: len(prefs)]

    for row, ds in enumerate(datasets):
        for col, model in enumerate(models):
            ax = axes[row, col]
            values = []
            for pref in prefs:
                variant = f"{model}_{pref}_{ds}"
                data = load_eval(args.input_dir, variant)
                if data:
                    values.append(
                        data["summary"]["fiduciary_avg_assistant_duty_of_care_score"] * 100
                    )
                else:
                    values.append(0)

            bars = ax.bar(x, values, color=colors)
            ax.bar_label(bars, fmt="%.0f%%", padding=2, fontsize=7)

            if row == 0:
                ax.set_title(label(model), fontsize=11, fontweight="semibold")
            if col == 0:
                ax.set_ylabel(label(ds), fontsize=9, fontweight="semibold")

            ax.set_xticks(x)
            ax.set_xticklabels(
                [label(p) for p in prefs] if row == n_rows - 1 else [],
                fontsize=8,
            )
            ax.set_ylim(-105, 105)
            ax.axhline(y=0, color="black", linewidth=0.8, zorder=0)
            ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f"{int(y)}%"))
            for spine in ["top", "right"]:
                ax.spines[spine].set_visible(False)

    fig.subplots_adjust(top=0.85, hspace=0.3)
    fig.text(
        0.5,
        1.0,
        "Duty of Care Score by Preference Visibility",
        ha="center",
        va="top",
        fontsize=14,
        fontweight="semibold",
    )
    fig.text(
        0.5,
        0.96,
        f"{len(models)} Assistants | {len(datasets)} Datasets | {len(prefs)} Pref Settings",
        ha="center",
        va="top",
        fontsize=11,
        color="#555555",
    )
    handles = [Rectangle((0, 0), 1, 1, fc="none", ec="none")] + [
        Rectangle((0, 0), 1, 1, fc=c) for c in colors
    ]
    labels = ["Prefs:"] + [label(p) for p in prefs]
    fig.legend(
        handles,
        labels,
        frameon=False,
        fontsize=8,
        loc="upper center",
        bbox_to_anchor=(0.5, 0.93),
        ncol=len(prefs) + 1,
    )

    out = args.output or Path("experiments/3-7-duty-of-care/duty-of-care.png")
    plt.savefig(out, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Saved {out}")


if __name__ == "__main__":
    main()
