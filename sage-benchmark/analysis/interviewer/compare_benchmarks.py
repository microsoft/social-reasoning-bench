#!/usr/bin/env python3
"""Compare form filling benchmark results (direct vs interview).

Usage:
    uv run analysis/interviewer/compare_benchmarks.py <direct_dir> <interview_dir> [--output <path>]

Example:
    uv run analysis/interviewer/compare_benchmarks.py \
        outputs/form_filling/1-7-forms \
        outputs/interviewer/1-13-experiment
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List, Optional

import matplotlib.pyplot as plt
import numpy as np


def find_summary_files(base_dir: Path) -> List[Path]:
    """Find all summary.json files in subdirectories."""
    return list(base_dir.rglob("**/summary.json"))


def load_direct_summary(summary_path: Path) -> Optional[Dict]:
    """Load summary from direct form filling benchmark."""
    try:
        with open(summary_path, "r") as f:
            data = json.load(f)

        summary = data.get("summary", {})
        return {
            "model": summary.get("agent_model"),
            "accuracy": summary.get("aggregate_correctness_score"),
            "privacy": summary.get("aggregate_privacy_score"),
        }
    except (json.JSONDecodeError, KeyError, FileNotFoundError) as e:
        print(f"Warning: Failed to load {summary_path}: {e}", file=sys.stderr)
        return None


def load_interview_summary(summary_path: Path) -> Optional[Dict]:
    """Load summary from interview benchmark."""
    try:
        with open(summary_path, "r") as f:
            data = json.load(f)

        summary = data.get("summary", {})
        form_tasks = summary.get("form_filling_tasks", {})
        return {
            "model": summary.get("interviewer_model"),
            "accuracy": form_tasks.get("avg_accuracy"),
            "privacy": form_tasks.get("avg_form_privacy_score"),
        }
    except (json.JSONDecodeError, KeyError, FileNotFoundError) as e:
        print(f"Warning: Failed to load {summary_path}: {e}", file=sys.stderr)
        return None


def aggregate_by_model(summary_files: List[Path], loader_func) -> Dict[str, Dict[str, List[float]]]:
    """Group results by model and collect metric values."""
    results = {}

    for summary_path in summary_files:
        data = loader_func(summary_path)
        if data is None or data.get("model") is None:
            continue

        model = data["model"]
        if model not in results:
            results[model] = {"accuracy": [], "privacy": []}

        if data.get("accuracy") is not None:
            results[model]["accuracy"].append(data["accuracy"])
        if data.get("privacy") is not None:
            results[model]["privacy"].append(data["privacy"])

    return results


def calculate_stats(values: List[float]) -> tuple:
    """Calculate mean and std for a list of values."""
    if not values:
        return 0, 0
    mean = np.mean(values)
    std = np.std(values, ddof=1) if len(values) > 1 else 0
    return mean, std


def plot_comparison(
    direct_results: Dict[str, Dict],
    interview_results: Dict[str, Dict],
    output_path: Path,
):
    """Create comparison bar chart."""
    all_models = sorted(set(direct_results.keys()) | set(interview_results.keys()))

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    metrics = [("accuracy", "Accuracy"), ("privacy", "Form Privacy")]

    for ax, (metric_key, metric_label) in zip(axes, metrics):
        x = np.arange(len(all_models))
        width = 0.35

        direct_means = []
        direct_stds = []
        interview_means = []
        interview_stds = []

        for model in all_models:
            if model in direct_results:
                mean, std = calculate_stats(direct_results[model][metric_key])
                direct_means.append(mean)
                direct_stds.append(std)
            else:
                direct_means.append(0)
                direct_stds.append(0)

            if model in interview_results:
                mean, std = calculate_stats(interview_results[model][metric_key])
                interview_means.append(mean)
                interview_stds.append(std)
            else:
                interview_means.append(0)
                interview_stds.append(0)

        bars1 = ax.bar(
            x - width / 2,
            direct_means,
            width,
            yerr=direct_stds,
            capsize=4,
            label="Direct",
            color="#2E86AB",
            alpha=0.8,
        )
        bars2 = ax.bar(
            x + width / 2,
            interview_means,
            width,
            yerr=interview_stds,
            capsize=4,
            label="Interview",
            color="#E91E63",
            alpha=0.8,
        )

        ax.set_ylabel("Score", fontsize=12)
        ax.set_title(metric_label, fontsize=14, fontweight="bold")
        ax.set_xticks(x)
        ax.set_xticklabels(all_models, rotation=15, ha="right")
        ax.legend(loc="lower right", fontsize=10)
        ax.set_ylim(0, 1.1)
        ax.grid(axis="y", alpha=0.3, linestyle="--")

        for bars, means, stds in [
            (bars1, direct_means, direct_stds),
            (bars2, interview_means, interview_stds),
        ]:
            for bar, val, std in zip(bars, means, stds):
                if val > 0:
                    ax.text(
                        bar.get_x() + bar.get_width() / 2.0,
                        val + std + 0.02,
                        f"{val:.2f}",
                        ha="center",
                        va="bottom",
                        fontsize=9,
                    )

    fig.suptitle(
        "Direct vs Interview Form Filling Comparison", fontsize=16, fontweight="bold", y=1.02
    )
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    print(f"Saved plot to: {output_path}")


def print_comparison_table(
    direct_results: Dict[str, Dict],
    interview_results: Dict[str, Dict],
):
    """Print comparison table to console."""
    all_models = sorted(set(direct_results.keys()) | set(interview_results.keys()))

    print("\n" + "=" * 80)
    print("BENCHMARK COMPARISON: Direct vs Interview")
    print("=" * 80)

    for model in all_models:
        print(f"\nModel: {model}")

        if model in direct_results:
            n_runs = len(direct_results[model]["accuracy"])
            acc_mean, acc_std = calculate_stats(direct_results[model]["accuracy"])
            priv_mean, priv_std = calculate_stats(direct_results[model]["privacy"])
            print(f"  Direct ({n_runs} runs):")
            print(f"    Accuracy: {acc_mean:.3f} +/- {acc_std:.3f}")
            print(f"    Privacy:  {priv_mean:.3f} +/- {priv_std:.3f}")
        else:
            print("  Direct: N/A")

        if model in interview_results:
            n_runs = len(interview_results[model]["accuracy"])
            acc_mean, acc_std = calculate_stats(interview_results[model]["accuracy"])
            priv_mean, priv_std = calculate_stats(interview_results[model]["privacy"])
            print(f"  Interview ({n_runs} runs):")
            print(f"    Accuracy: {acc_mean:.3f} +/- {acc_std:.3f}")
            print(f"    Privacy:  {priv_mean:.3f} +/- {priv_std:.3f}")
        else:
            print("  Interview: N/A")

        if model in direct_results and model in interview_results:
            direct_acc = np.mean(direct_results[model]["accuracy"])
            interview_acc = np.mean(interview_results[model]["accuracy"])
            direct_priv = np.mean(direct_results[model]["privacy"])
            interview_priv = np.mean(interview_results[model]["privacy"])

            acc_diff = interview_acc - direct_acc
            priv_diff = interview_priv - direct_priv

            print(f"  Delta (Interview - Direct):")
            print(f"    Accuracy: {acc_diff:+.3f}")
            print(f"    Privacy:  {priv_diff:+.3f}")


def main():
    parser = argparse.ArgumentParser(
        description="Compare direct vs interview form filling benchmark results"
    )
    parser.add_argument(
        "direct_dir",
        type=Path,
        help="Directory containing direct form filling results",
    )
    parser.add_argument(
        "interview_dir",
        type=Path,
        help="Directory containing interview benchmark results",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Output plot path (default: comparison_plot.png in interview_dir)",
    )

    args = parser.parse_args()

    for dir_path, name in [(args.direct_dir, "direct"), (args.interview_dir, "interview")]:
        if not dir_path.exists():
            print(f"Error: {name} directory {dir_path} does not exist", file=sys.stderr)
            sys.exit(1)

    output_path = args.output if args.output else args.interview_dir / "comparison_plot.png"

    print(f"Loading direct results from: {args.direct_dir}")
    direct_files = find_summary_files(args.direct_dir)
    print(f"  Found {len(direct_files)} summary file(s)")
    direct_results = aggregate_by_model(direct_files, load_direct_summary)

    print(f"Loading interview results from: {args.interview_dir}")
    interview_files = find_summary_files(args.interview_dir)
    print(f"  Found {len(interview_files)} summary file(s)")
    interview_results = aggregate_by_model(interview_files, load_interview_summary)

    if not direct_results and not interview_results:
        print("Error: No valid results found", file=sys.stderr)
        sys.exit(1)

    print(f"\nDirect models: {list(direct_results.keys())}")
    print(f"Interview models: {list(interview_results.keys())}")

    plot_comparison(direct_results, interview_results, output_path)
    print_comparison_table(direct_results, interview_results)

    print("\nDone!")


if __name__ == "__main__":
    main()
