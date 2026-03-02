#!/usr/bin/env python3
"""Plot privacy and duty of care results from the 2-26 full sweep.

Usage:
    uv run experiments/2-26-full-sweep/analysis/plot_results.py \
        --input-dir outputs/calendar_scheduling/2-26-full-sweep
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

DATASETS = [
    "benign",
    "mal-hc-privacy",
    "mal-whim-privacy",
    "mal-hc-doc",
    "mal-whim-doc",
]
DATASET_LABELS = {
    "benign": "Benign",
    "mal-hc-privacy": "Malicious HC (Privacy)",
    "mal-hc-doc": "Malicious HC (Duty of Care)",
    "mal-whim-privacy": "Malicious Whim. (Privacy)",
    "mal-whim-doc": "Malicious Whim. (Duty of Care)",
}

PRIVACY_PROMPTS = ["base", "privacy-aware", "privacy-strong", "privacy-ci"]
PRIVACY_PROMPT_LABELS = {
    "base": "Base",
    "privacy-aware": "Aware",
    "privacy-strong": "Strong",
    "privacy-ci": "CI",
}

DOC_PREFS = ["prefs-hidden", "prefs-exposed"]
DOC_PREF_LABELS = {"prefs-hidden": "Hidden", "prefs-exposed": "Exposed"}

COLORS = ["#5C7ABF", "#2D3047", "#8B5CF6", "#D97706"]


def load_eval(dir_path: Path, variant: str) -> dict | None:
    path = dir_path / variant / "eval.json"
    if not path.exists():
        print(f"  Warning: missing {path}", file=sys.stderr)
        return None
    with open(path) as f:
        return json.load(f)


def resolve_privacy_variant(
    model: str, prompt: str, dataset: str, privacy_dir: Path, doc_dir: Path
) -> dict | None:
    if prompt == "base":
        variant = f"{model}_prefs-hidden_{dataset}"
        return load_eval(doc_dir, variant)
    variant = f"{model}_{prompt}_{dataset}"
    return load_eval(privacy_dir, variant)


def plot_privacy(privacy_dir: Path, doc_dir: Path, output_path: Path):
    n_rows = len(DATASETS)
    n_cols = len(MODELS)
    fig, axes = plt.subplots(
        n_rows,
        n_cols,
        figsize=(4.0 * n_cols, 3.0 * n_rows),
        sharey=True,
    )

    x = np.arange(len(PRIVACY_PROMPTS))
    prompt_labels = [PRIVACY_PROMPT_LABELS[p] for p in PRIVACY_PROMPTS]

    for row, ds in enumerate(DATASETS):
        for col, model in enumerate(MODELS):
            ax = axes[row, col]
            values = []
            for prompt in PRIVACY_PROMPTS:
                data = resolve_privacy_variant(model, prompt, ds, privacy_dir, doc_dir)
                if data:
                    values.append(data["summary"]["privacy_leakage_rate"] * 100)
                else:
                    values.append(0)

            bars = ax.bar(x, values, color=COLORS[: len(PRIVACY_PROMPTS)])
            ax.bar_label(bars, fmt="%.0f%%", padding=2, fontsize=7)

            if row == 0:
                ax.set_title(MODEL_LABELS[model], fontsize=11, fontweight="semibold")
            if col == 0:
                ax.set_ylabel(DATASET_LABELS[ds], fontsize=9, fontweight="semibold")

            ax.set_xticks(x)
            ax.set_xticklabels(prompt_labels if row == n_rows - 1 else [], fontsize=8)
            ax.set_ylim(0, 105)
            ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f"{int(y)}%"))
            for spine in ["top", "right"]:
                ax.spines[spine].set_visible(False)

    fig.subplots_adjust(top=0.85, hspace=0.3)
    fig.text(
        0.5,
        1.0,
        "Privacy Leakage by Prompt Strategy",
        ha="center",
        va="top",
        fontsize=14,
        fontweight="semibold",
    )
    fig.text(
        0.5,
        0.96,
        "Requestor: GPT-4.1 | 3 Assistants | 5 Datasets",
        ha="center",
        va="top",
        fontsize=11,
        color="#555555",
    )
    handles = [Rectangle((0, 0), 1, 1, fc=c) for c in COLORS[: len(PRIVACY_PROMPTS)]]
    labels = [PRIVACY_PROMPT_LABELS[p] for p in PRIVACY_PROMPTS]
    handles = [Rectangle((0, 0), 1, 1, fc="none", ec="none")] + handles
    labels = ["Prompt:"] + labels
    fig.legend(
        handles,
        labels,
        frameon=False,
        fontsize=8,
        loc="upper center",
        bbox_to_anchor=(0.5, 0.93),
        ncol=len(PRIVACY_PROMPTS) + 1,
    )
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Saved privacy plot to {output_path}")


def plot_duty_of_care(doc_dir: Path, output_path: Path):
    n_rows = len(DATASETS)
    n_cols = len(MODELS)
    fig, axes = plt.subplots(
        n_rows,
        n_cols,
        figsize=(4.0 * n_cols, 3.0 * n_rows),
        sharey=True,
    )

    x = np.arange(len(DOC_PREFS))
    pref_labels = [DOC_PREF_LABELS[p] for p in DOC_PREFS]

    for row, ds in enumerate(DATASETS):
        for col, model in enumerate(MODELS):
            ax = axes[row, col]
            values = []
            for pref in DOC_PREFS:
                variant = f"{model}_{pref}_{ds}"
                data = load_eval(doc_dir, variant)
                if data:
                    score = data["summary"].get("fiduciary_avg_assistant_duty_of_care_score")
                    values.append((score or 0) * 100)
                else:
                    values.append(0)

            bars = ax.bar(x, values, color=COLORS[: len(DOC_PREFS)])
            ax.bar_label(bars, fmt="%.0f%%", padding=2, fontsize=7)

            if row == 0:
                ax.set_title(MODEL_LABELS[model], fontsize=11, fontweight="semibold")
            if col == 0:
                ax.set_ylabel(DATASET_LABELS[ds], fontsize=9, fontweight="semibold")

            ax.set_xticks(x)
            ax.set_xticklabels(pref_labels if row == n_rows - 1 else [], fontsize=8)
            ax.set_ylim(0, 105)
            ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f"{int(y)}%"))
            for spine in ["top", "right"]:
                ax.spines[spine].set_visible(False)

    fig.subplots_adjust(top=0.85, hspace=0.3)
    fig.text(
        0.5,
        1.0,
        "Duty of Care by Preference Visibility",
        ha="center",
        va="top",
        fontsize=14,
        fontweight="semibold",
    )
    fig.text(
        0.5,
        0.96,
        "Requestor: GPT-4.1 | 3 Assistants | 5 Datasets",
        ha="center",
        va="top",
        fontsize=11,
        color="#555555",
    )
    handles = [Rectangle((0, 0), 1, 1, fc=c) for c in COLORS[: len(DOC_PREFS)]]
    labels = [DOC_PREF_LABELS[p] for p in DOC_PREFS]
    handles = [Rectangle((0, 0), 1, 1, fc="none", ec="none")] + handles
    labels = ["Preferences:"] + labels
    fig.legend(
        handles,
        labels,
        frameon=False,
        fontsize=8,
        loc="upper center",
        bbox_to_anchor=(0.5, 0.93),
        ncol=len(DOC_PREFS) + 1,
    )
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Saved duty of care plot to {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Plot 2-26 full sweep results")
    parser.add_argument(
        "--input-dir",
        type=Path,
        required=True,
        help="Base directory (e.g. outputs/calendar_scheduling/2-26-full-sweep)",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Output directory for plots (default: same as input-dir)",
    )
    args = parser.parse_args()

    if not args.input_dir.exists():
        print(f"Error: {args.input_dir} does not exist", file=sys.stderr)
        sys.exit(1)

    output_dir = args.output_dir or args.input_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    doc_dir = args.input_dir / "duty_of_care"
    privacy_dir = args.input_dir / "privacy"

    plot_privacy(privacy_dir, doc_dir, output_dir / "privacy.png")
    plot_duty_of_care(doc_dir, output_dir / "duty_of_care.png")

    # Print total wall-clock sweep time from sweep_metadata.json
    sweep_meta_path = args.input_dir / "sweep_metadata.json"
    if sweep_meta_path.exists():
        with open(sweep_meta_path) as f:
            sweep_meta = json.load(f)
        total_seconds = sweep_meta["total_sweep_seconds"]
        exp_count = sweep_meta["experiment_count"]
        mins, secs = divmod(total_seconds, 60)
        hrs, mins = divmod(int(mins), 60)
        print(
            f"\nTotal wall-clock sweep time ({exp_count} experiments): {hrs}h{mins:02d}m{secs:04.1f}s"
        )
    else:
        print(f"\nWarning: {sweep_meta_path} not found, cannot report sweep time", file=sys.stderr)


if __name__ == "__main__":
    main()
