#!/usr/bin/env python3
"""Plot privacy and duty of care results from the 2-23 calendar requestor sweep.

Usage:
    uv run experiments/2-23-calendar-sweep-request-sweep/analysis/plot_results.py [--input-dir <path>] [--output-dir <path>]
"""

import argparse
import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle

MODELS = ["gpt4.1-cot", "gpt5.2-medium"]
MODEL_LABELS = {"gpt4.1-cot": "GPT-4.1 (CoT)", "gpt5.2-medium": "GPT-5.2 (Medium)"}

REQUESTOR_MODELS = {
    "gpt4.1": "GPT-4.1",
    "gpt5.1": "GPT-5.1",
}

REQUESTOR_TYPES = ["benign", "malicious-hc", "malicious-whimsical"]
REQUESTOR_LABELS = {
    "benign": "Benign",
    "malicious-hc": "Malicious\n(Hand-Crafted)",
    "malicious-whimsical": "Malicious\n(Whimsical)",
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


def load_eval(input_dir: Path, variant: str) -> dict | None:
    path = input_dir / variant / "eval.json"
    if not path.exists():
        print(f"  Warning: missing {path}", file=sys.stderr)
        return None
    with open(path) as f:
        return json.load(f)


def resolve_privacy_variant(
    model: str, requestor_name: str, prompt: str, req: str, input_dir: Path, requestor_dir: Path
) -> dict | None:
    """Load privacy result, using duty_of_care dir for the base (no-privacy-prompt) case."""
    if prompt == "base":
        variant = f"{model}_{requestor_name}_prefs-hidden_{req}"
        return load_eval(requestor_dir / "duty_of_care", variant)
    variant = f"{model}_{requestor_name}_{prompt}_{req}"
    return load_eval(input_dir, variant)


def plot_privacy(input_dir: Path, output_path: Path, requestor_name: str, requestor_dir: Path):
    fig, axes = plt.subplots(1, 3, figsize=(14, 6.5), sharey=True)

    for ax, req_type in zip(axes, REQUESTOR_TYPES):
        x = np.arange(len(MODELS))
        n_bars = len(PRIVACY_PROMPTS)
        width = 0.8 / n_bars

        for i, prompt in enumerate(PRIVACY_PROMPTS):
            values = []
            for model in MODELS:
                data = resolve_privacy_variant(
                    model, requestor_name, prompt, req_type, input_dir, requestor_dir
                )
                if data:
                    values.append(data["summary"]["privacy_leakage_rate"] * 100)
                else:
                    values.append(0)

            offset = (i - (n_bars - 1) / 2) * width
            bars = ax.bar(
                x + offset,
                values,
                width,
                label=PRIVACY_PROMPT_LABELS[prompt],
                color=COLORS[i],
            )
            ax.bar_label(bars, fmt="%.0f%%", padding=2, fontsize=7)

        ax.set_title(REQUESTOR_LABELS[req_type], fontsize=11, fontweight="semibold")
        ax.set_xticks(x)
        ax.set_xticklabels([MODEL_LABELS[m] for m in MODELS], fontsize=9)
        ax.set_ylim(0, 105)
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f"{int(y)}%"))
        for spine in ["top", "right"]:
            ax.spines[spine].set_visible(False)

    axes[0].set_ylabel("% Tasks with Privacy Leakage", fontsize=10)

    fig.subplots_adjust(top=0.78)
    fig.text(
        0.5,
        1,
        "Privacy Leakage by Prompt Strategy",
        ha="center",
        va="top",
        fontsize=14,
        fontweight="semibold",
    )
    fig.text(
        0.5,
        0.95,
        f"Requestor: {REQUESTOR_MODELS[requestor_name]}",
        ha="center",
        va="top",
        fontsize=11,
        color="#555555",
    )
    handles, labels = axes[0].get_legend_handles_labels()
    handles = [Rectangle((0, 0), 1, 1, fc="none", ec="none")] + list(handles)
    labels = ["Prompt:"] + list(labels)
    fig.legend(
        handles,
        labels,
        frameon=False,
        fontsize=8,
        loc="upper center",
        bbox_to_anchor=(0.5, 0.92),
        ncol=len(PRIVACY_PROMPTS) + 1,
    )
    # plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    print(f"Saved privacy plot to {output_path}")


def plot_duty_of_care(input_dir: Path, output_path: Path, requestor_name: str):
    fig, axes = plt.subplots(1, 3, figsize=(14, 6.5), sharey=True)

    for ax, req_type in zip(axes, REQUESTOR_TYPES):
        x = np.arange(len(MODELS))
        n_bars = len(DOC_PREFS)
        width = 0.8 / n_bars

        for i, pref in enumerate(DOC_PREFS):
            values = []
            for model in MODELS:
                variant = f"{model}_{requestor_name}_{pref}_{req_type}"
                data = load_eval(input_dir, variant)
                if data:
                    score = data["summary"].get("fiduciary_avg_assistant_duty_of_care_score")
                    values.append((score or 0) * 100)
                else:
                    values.append(0)

            offset = (i - (n_bars - 1) / 2) * width
            bars = ax.bar(
                x + offset,
                values,
                width,
                label=DOC_PREF_LABELS[pref],
                color=COLORS[i],
            )
            ax.bar_label(bars, fmt="%.0f%%", padding=2, fontsize=7)

        ax.set_title(REQUESTOR_LABELS[req_type], fontsize=11, fontweight="semibold")
        ax.set_xticks(x)
        ax.set_xticklabels([MODEL_LABELS[m] for m in MODELS], fontsize=9)
        ax.set_ylim(0, 105)
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f"{int(y)}%"))
        for spine in ["top", "right"]:
            ax.spines[spine].set_visible(False)

    axes[0].set_ylabel("Duty of Care Score (%)", fontsize=10)

    fig.subplots_adjust(top=0.78)
    fig.text(
        0.5,
        1,
        "Duty of Care by Preference Visibility",
        ha="center",
        va="top",
        fontsize=14,
        fontweight="semibold",
    )
    fig.text(
        0.5,
        0.95,
        f"Requestor: {REQUESTOR_MODELS[requestor_name]}",
        ha="center",
        va="top",
        fontsize=11,
        color="#555555",
    )
    handles, labels = axes[0].get_legend_handles_labels()
    handles = [Rectangle((0, 0), 1, 1, fc="none", ec="none")] + list(handles)
    labels = ["Preferences:"] + list(labels)
    fig.legend(
        handles,
        labels,
        frameon=False,
        fontsize=8,
        loc="upper center",
        bbox_to_anchor=(0.5, 0.92),
        ncol=len(DOC_PREFS) + 1,
    )
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    print(f"Saved duty of care plot to {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Plot calendar requestor sweep results")
    parser.add_argument(
        "--input-dir",
        type=Path,
        required=True,
        help="Directory containing variant subdirectories with eval.json files",
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

    for requestor_name in REQUESTOR_MODELS:
        requestor_dir = args.input_dir / f"requestor_{requestor_name}"
        plot_privacy(
            requestor_dir / "privacy",
            output_dir / f"privacy_{requestor_name}.png",
            requestor_name,
            requestor_dir,
        )
        plot_duty_of_care(
            requestor_dir / "duty_of_care",
            output_dir / f"duty_of_care_{requestor_name}.png",
            requestor_name,
        )


if __name__ == "__main__":
    main()
