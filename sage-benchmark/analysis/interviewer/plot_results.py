#!/usr/bin/env python3
"""Plot interviewer experiment results from summary.json files.

Usage:
    uv run analysis/interviewer/plot_results.py <input_dir> [--output <path>]

Example:
    uv run analysis/interviewer/plot_results.py outputs/interviewer/experiments
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


def load_summary_data(summary_path: Path) -> Optional[Dict]:
    """Load and extract relevant data from a summary.json file."""
    try:
        with open(summary_path, "r") as f:
            data = json.load(f)

        summary = data.get("summary", {})
        form_tasks = summary.get("form_filling_tasks", {})
        return {
            "interviewer_model": summary.get("interviewer_model"),
            "avg_accuracy": form_tasks.get("avg_accuracy"),
            "avg_form_privacy": form_tasks.get("avg_form_privacy_score"),
            "avg_conv_privacy": form_tasks.get("avg_conversation_privacy_score"),
            # "avg_validation_rate": form_tasks.get("avg_validation_rate"),
            "perfect_accuracy_rate": form_tasks.get("perfect_accuracy_rate"),
            "perfect_privacy_rate": form_tasks.get("perfect_privacy_rate"),
            "total_tasks": summary.get("total_tasks"),
            "successful": summary.get("successful_executions"),
        }
    except (json.JSONDecodeError, KeyError, FileNotFoundError) as e:
        print(f"Warning: Failed to load {summary_path}: {e}", file=sys.stderr)
        return None


def aggregate_results(summary_files: List[Path]) -> Dict[str, List[Dict]]:
    """Group results by model name."""
    results_by_model = {}

    for summary_path in summary_files:
        data = load_summary_data(summary_path)
        if data is None:
            continue

        model_name = data.get("interviewer_model")
        if model_name is None:
            print(f"Warning: No interviewer_model found in {summary_path}", file=sys.stderr)
            continue

        if model_name not in results_by_model:
            results_by_model[model_name] = []
        results_by_model[model_name].append(data)

    return results_by_model


def calculate_stats(runs: List[Dict]) -> Dict:
    """Calculate mean and standard deviation for each metric."""
    metrics = [
        "avg_accuracy",
        "avg_form_privacy",
        "avg_conv_privacy",
        # "avg_validation_rate",
        "perfect_accuracy_rate",
        "perfect_privacy_rate",
    ]

    stats = {"n_runs": len(runs)}

    for metric in metrics:
        values = [run[metric] for run in runs if run.get(metric) is not None]
        if values:
            stats[f"{metric}_mean"] = np.mean(values)
            stats[f"{metric}_std"] = np.std(values, ddof=1) if len(values) > 1 else 0
        else:
            stats[f"{metric}_mean"] = 0
            stats[f"{metric}_std"] = 0

    stats["success_rate"] = np.mean(
        [run["successful"] / run["total_tasks"] for run in runs if run["total_tasks"] > 0]
    )

    return stats


def plot_results(model_stats: Dict[str, Dict], output_path: Path):
    """Create grouped bar chart with error bars for all metrics."""

    metrics_config = [
        ("avg_accuracy", "Accuracy", "#2E86AB"),
        ("avg_form_privacy", "Form Privacy", "#E91E63"),
        ("avg_conv_privacy", "Conv Privacy", "#F18F01"),
        # ("avg_validation_rate", "Validation Rate", "#4CAF50"),
        ("perfect_accuracy_rate", "Perfect Accuracy", "#00BCD4"),
        ("perfect_privacy_rate", "Perfect Privacy", "#795548"),
    ]

    model_names = []
    model_labels = []
    for model_name, stats in sorted(model_stats.items()):
        model_names.append(model_name)
        n_runs = stats["n_runs"]
        run_label = "run" if n_runs == 1 else "runs"
        model_labels.append(f"{model_name}\n({n_runs} {run_label})")

    x = np.arange(len(model_names))
    n_metrics = len(metrics_config)
    width = 0.8 / n_metrics

    fig, ax = plt.subplots(figsize=(14, 7))

    all_bars = []
    for i, (metric_key, metric_label, color) in enumerate(metrics_config):
        means = [model_stats[m][f"{metric_key}_mean"] for m in sorted(model_stats.keys())]
        stds = [model_stats[m][f"{metric_key}_std"] for m in sorted(model_stats.keys())]
        offset = (i - n_metrics / 2 + 0.5) * width
        bars = ax.bar(
            x + offset,
            means,
            width,
            yerr=stds,
            capsize=3,
            label=metric_label,
            color=color,
            alpha=0.8,
        )
        all_bars.append((bars, means, stds))

    ax.set_ylabel("Score", fontsize=12)
    ax.set_title("Interviewer Benchmark Results", fontsize=14, fontweight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels(model_labels)
    ax.legend(loc="upper right", fontsize=9, ncol=2)
    ax.set_ylim(0, 1.15)
    ax.grid(axis="y", alpha=0.3, linestyle="--")

    for bars, means, stds in all_bars:
        for bar, val, std in zip(bars, means, stds):
            height = bar.get_height()
            if height > 0:
                ax.text(
                    bar.get_x() + bar.get_width() / 2.0,
                    height + std + 0.02,
                    f"{val:.2f}",
                    ha="center",
                    va="bottom",
                    fontsize=6,
                    rotation=0,
                )

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    print(f"Saved plot to: {output_path}")


def print_summary_statistics(model_stats: Dict[str, Dict]):
    """Print formatted summary statistics to console."""
    print("\n" + "=" * 60)
    print("SUMMARY STATISTICS")
    print("=" * 60)

    metrics_display = [
        ("avg_accuracy", "Accuracy"),
        ("avg_form_privacy", "Form Privacy"),
        ("avg_conv_privacy", "Conv Privacy"),
        # ("avg_validation_rate", "Validation Rate"),
        ("perfect_accuracy_rate", "Perfect Accuracy Rate"),
        ("perfect_privacy_rate", "Perfect Privacy Rate"),
    ]

    for model_name, stats in sorted(model_stats.items()):
        print(f"\nModel: {model_name}")
        print(f"  Number of runs: {stats['n_runs']}")
        print(f"  Success rate: {stats['success_rate']:.1%}")
        for metric_key, metric_label in metrics_display:
            mean = stats.get(f"{metric_key}_mean", 0)
            std = stats.get(f"{metric_key}_std", 0)
            print(f"  {metric_label}: {mean:.3f} +/- {std:.3f}")


def main():
    parser = argparse.ArgumentParser(
        description="Plot interviewer experiment results from summary.json files"
    )
    parser.add_argument(
        "input_dir",
        type=Path,
        help="Directory containing run_* subdirectories with summary.json files",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Output plot path (default: <input_dir>/results_plot.png)",
    )

    args = parser.parse_args()

    if not args.input_dir.exists():
        print(f"Error: Directory {args.input_dir} does not exist", file=sys.stderr)
        sys.exit(1)

    if not args.input_dir.is_dir():
        print(f"Error: {args.input_dir} is not a directory", file=sys.stderr)
        sys.exit(1)

    output_path = args.output if args.output else args.input_dir / "results_plot.png"

    print(f"Finding summary files in: {args.input_dir}")
    summary_files = find_summary_files(args.input_dir)

    if not summary_files:
        print(f"Error: No summary.json files found in {args.input_dir}", file=sys.stderr)
        sys.exit(1)

    print(f"Found {len(summary_files)} summary file(s)")

    results_by_model = aggregate_results(summary_files)

    if not results_by_model:
        print("Error: No valid results found", file=sys.stderr)
        sys.exit(1)

    model_stats = {
        model_name: calculate_stats(runs) for model_name, runs in results_by_model.items()
    }

    print(f"Plotting results for {len(model_stats)} model(s)...")
    plot_results(model_stats, output_path)

    print_summary_statistics(model_stats)

    print("\nDone!")


if __name__ == "__main__":
    main()
