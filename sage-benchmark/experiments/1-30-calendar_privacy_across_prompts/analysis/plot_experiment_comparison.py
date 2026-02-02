#!/usr/bin/env python3
"""Plot experiment results comparing conditions and system prompts.

Usage:
    uv run analysis/calendar_scheduling/plot_experiment_comparison.py <input_dir> [--output <path>]

Example:
    uv run analysis/calendar_scheduling/plot_experiment_comparison.py outputs/calendar_scheduling/1-30-experiment
"""

import argparse
import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

CONDITIONS = ["normal", "malicious"]
SYSTEM_PROMPTS = ["default", "simple", "strong", "ci"]
PROMPT_NORMALIZE = {"privacy-simple": "simple", "privacy-strong": "strong", "privacy-ci": "ci"}


def load_experiment_results(base_dir: Path) -> tuple[dict, dict, dict]:
    """Load all experiment JSON files from the directory."""
    privacy_results = {}
    success_results = {}
    metadata = {}

    for json_file in base_dir.glob("*.json"):
        with open(json_file) as f:
            data = json.load(f)

        name = json_file.stem
        parts = name.split("-")

        # Find condition (normal or malicious)
        condition = next((c for c in CONDITIONS if c in parts), None)
        if not condition:
            print(f"Skipping {name}: no condition found", file=sys.stderr)
            continue

        # System prompt is everything after condition
        condition_idx = parts.index(condition)
        prompt_raw = "-".join(parts[condition_idx + 1 :]) or "default"
        prompt = PROMPT_NORMALIZE.get(prompt_raw, prompt_raw)

        privacy_results[(condition, prompt)] = data["summary"]["privacy_leakage_rate"]
        success_results[(condition, prompt)] = data["summary"]["task_success_rate"]

        # Extract metadata from first file
        if not metadata and "metadata" in data:
            meta = data["metadata"]
            metadata["assistant"] = meta.get("assistant_model", "?").split("/")[-1]
            metadata["requestor"] = meta.get("requestor_model", "?").split("/")[-1]
            metadata["judge"] = meta.get("judge_model", "?").split("/")[-1]
            metadata["task_count"] = meta.get("task_count", 0)

        print(f"Loaded {json_file.name}: {condition}, {prompt}")

    return privacy_results, success_results, metadata


def plot_results(privacy_results: dict, success_results: dict, metadata: dict, output_path: Path):
    """Create bar plots for privacy leakage rate and task success rate."""
    # Build data arrays (as percentages)
    leakage = {
        c: [privacy_results.get((c, p), 0) * 100 for p in SYSTEM_PROMPTS] for c in CONDITIONS
    }
    success = {
        c: [success_results.get((c, p), 0) * 100 for p in SYSTEM_PROMPTS] for c in CONDITIONS
    }

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6, 8))
    x = np.arange(len(SYSTEM_PROMPTS))
    width = 0.35
    colors = {"normal": "#5C7ABF", "malicious": "#2D3047"}

    # Plot 1: Privacy Leakage Rate
    bars1 = {
        c: ax1.bar(
            x + (0.5 if c == "malicious" else -0.5) * width,
            leakage[c],
            width,
            label=c.capitalize(),
            color=colors[c],
        )
        for c in CONDITIONS
    }

    ax1.set_ylabel("% of Tasks with Privacy Leakage", fontsize=10)
    ax1.set_xlabel("System Prompt", fontsize=10)
    ax1.set_xticks(x)
    ax1.set_xticklabels([p.capitalize() for p in SYSTEM_PROMPTS], fontsize=10)
    ax1.set_ylim(0, 100)
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f"{int(y)}%"))

    for spine in ["top", "right"]:
        ax1.spines[spine].set_visible(False)
    for spine in ["left", "bottom"]:
        ax1.spines[spine].set_linewidth(0.5)
    ax1.tick_params(width=0.5)
    ax1.legend(frameon=False, fontsize=9, loc="upper right")
    ax1.set_title("Privacy Leakage Rate", fontsize=11, fontweight="semibold", pad=10)

    for bar_group in bars1.values():
        ax1.bar_label(bar_group, fmt="%.0f%%", padding=2, fontsize=8)

    # Plot 2: Task Success Rate
    bars2 = {
        c: ax2.bar(
            x + (0.5 if c == "malicious" else -0.5) * width,
            success[c],
            width,
            label=c.capitalize(),
            color=colors[c],
        )
        for c in CONDITIONS
    }

    ax2.set_ylabel("% of Tasks Successful", fontsize=10)
    ax2.set_xlabel("System Prompt", fontsize=10)
    ax2.set_xticks(x)
    ax2.set_xticklabels([p.capitalize() for p in SYSTEM_PROMPTS], fontsize=10)
    ax2.set_ylim(0, 100)
    ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f"{int(y)}%"))

    for spine in ["top", "right"]:
        ax2.spines[spine].set_visible(False)
    for spine in ["left", "bottom"]:
        ax2.spines[spine].set_linewidth(0.5)
    ax2.tick_params(width=0.5)
    ax2.legend(frameon=False, fontsize=9, loc="upper right")
    ax2.set_title("Task Success Rate", fontsize=11, fontweight="semibold", pad=10)

    for bar_group in bars2.values():
        ax2.bar_label(bar_group, fmt="%.0f%%", padding=2, fontsize=8)

    # Figure title and subtitle
    assistant, requestor = metadata.get("assistant", "?"), metadata.get("requestor", "?")
    judge, n = metadata.get("judge", "?"), metadata.get("task_count", 0)
    fig.suptitle(
        "Privacy vs Task Performance by System Prompt", fontsize=13, fontweight="semibold", y=0.98
    )
    if assistant == requestor:
        subtitle = f"Assistant/Requestor: {assistant}  ·  Judge: {judge}  ·  n={n}"
    else:
        subtitle = f"Assistant: {assistant}  ·  Requestor: {requestor}  ·  Judge: {judge}  ·  n={n}"
    fig.text(0.5, 0.94, subtitle, ha="center", fontsize=9, color="#555555", style="italic")

    plt.tight_layout(rect=[0, 0, 1, 0.93])
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    print(f"Saved plot to {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Plot experiment results comparing conditions and system prompts"
    )
    parser.add_argument("input_dir", type=Path, help="Directory containing experiment JSON files")
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Output plot path (default: <input_dir>/experiment_comparison.png)",
    )
    args = parser.parse_args()

    if not args.input_dir.exists():
        print(f"Error: Directory {args.input_dir} does not exist", file=sys.stderr)
        sys.exit(1)

    output_path = args.output or args.input_dir / "experiment_comparison.png"

    print(f"Loading results from: {args.input_dir}")
    privacy_results, success_results, metadata = load_experiment_results(args.input_dir)

    if not privacy_results:
        print("Error: No valid result files found", file=sys.stderr)
        sys.exit(1)

    print(f"Found {len(privacy_results)} experiment configurations")
    plot_results(privacy_results, success_results, metadata, output_path)


if __name__ == "__main__":
    main()
