"""Plot privacy leakage grid: 3 models × 3 datasets × 4 prompts.

Usage:
    uv run python experiments/3-6-refactor/plot.py \
        --input-dir outputs/calendar_scheduling/3-6-refactor/validation
"""

import argparse
import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle

MODELS = ["gpt4.1-cot", "gpt5.2-medium", "gemini-3-flash-medium"]
MODEL_LABELS = {
    "gpt4.1-cot": "GPT-4.1 (CoT)",
    "gpt5.2-medium": "GPT-5.2 (Medium)",
    "gemini-3-flash-medium": "Gemini 3 Flash (Medium)",
}

DATASETS = ["benign", "mal-hc-privacy", "mal-whim-privacy"]
DATASET_LABELS = {
    "benign": "Benign",
    "mal-hc-privacy": "Malicious HC (Privacy)",
    "mal-whim-privacy": "Malicious Whim. (Privacy)",
}

PROMPTS = ["base", "privacy-aware", "privacy-strong", "privacy-ci"]
PROMPT_LABELS = {
    "base": "Base",
    "privacy-aware": "Aware",
    "privacy-strong": "Strong",
    "privacy-ci": "CI",
}

COLORS = ["#5C7ABF", "#2D3047", "#8B5CF6", "#D97706"]


def load_eval(base_dir: Path, variant: str) -> dict | None:
    path = base_dir / variant / "eval.json"
    if not path.exists():
        print(f"  Warning: missing {path}", file=sys.stderr)
        return None
    with open(path) as f:
        return json.load(f)


def main():
    parser = argparse.ArgumentParser(description="Plot 3-6 privacy leakage grid")
    parser.add_argument(
        "--input-dir",
        type=Path,
        default=Path("outputs/calendar_scheduling/3-6-refactor/validation"),
        help="Base directory with variant subdirs",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Output PNG (default: <input-dir>/privacy.png)",
    )
    args = parser.parse_args()

    if not args.input_dir.exists():
        print(f"Error: {args.input_dir} does not exist", file=sys.stderr)
        sys.exit(1)

    n_rows = len(DATASETS)
    n_cols = len(MODELS)
    fig, axes = plt.subplots(
        n_rows, n_cols,
        figsize=(4.0 * n_cols, 3.0 * n_rows),
        sharey=True,
    )

    x = np.arange(len(PROMPTS))

    for row, ds in enumerate(DATASETS):
        for col, model in enumerate(MODELS):
            ax = axes[row, col]
            values = []
            for prompt in PROMPTS:
                variant = f"{model}_{prompt}_{ds}"
                data = load_eval(args.input_dir, variant)
                if data:
                    values.append(data["summary"]["privacy_leakage_rate"] * 100)
                else:
                    values.append(0)

            bars = ax.bar(x, values, color=COLORS[:len(PROMPTS)])
            ax.bar_label(bars, fmt="%.0f%%", padding=2, fontsize=7)

            if row == 0:
                ax.set_title(MODEL_LABELS[model], fontsize=11, fontweight="semibold")
            if col == 0:
                ax.set_ylabel(DATASET_LABELS[ds], fontsize=9, fontweight="semibold")

            ax.set_xticks(x)
            ax.set_xticklabels(
                [PROMPT_LABELS[p] for p in PROMPTS] if row == n_rows - 1 else [],
                fontsize=8,
            )
            ax.set_ylim(0, 105)
            ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f"{int(y)}%"))
            for spine in ["top", "right"]:
                ax.spines[spine].set_visible(False)

    fig.subplots_adjust(top=0.85, hspace=0.3)
    fig.text(
        0.5, 1.0,
        "Privacy Leakage by Prompt Strategy",
        ha="center", va="top", fontsize=14, fontweight="semibold",
    )
    fig.text(
        0.5, 0.96,
        "Requestor: Gemini 3 Flash | 3 Assistants | 3 Datasets",
        ha="center", va="top", fontsize=11, color="#555555",
    )
    handles = [Rectangle((0, 0), 1, 1, fc="none", ec="none")] + [
        Rectangle((0, 0), 1, 1, fc=c) for c in COLORS[:len(PROMPTS)]
    ]
    labels = ["Prompt:"] + [PROMPT_LABELS[p] for p in PROMPTS]
    fig.legend(
        handles, labels,
        frameon=False, fontsize=8,
        loc="upper center", bbox_to_anchor=(0.5, 0.93),
        ncol=len(PROMPTS) + 1,
    )

    out = args.output or Path("experiments/3-6-refactor/privacy.png")
    plt.savefig(out, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Saved {out}")


if __name__ == "__main__":
    main()
