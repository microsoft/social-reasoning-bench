#!/usr/bin/env python3
"""Plot form filling experiment results from summary.json files.

Usage:
    uv run -m sage_benchmark.form_filling.analysis.plot_results <input_dir> [--output <path>]

Example:
    uv run -m sage_benchmark.form_filling.analysis.plot_results outputs/form_filling/1-7-forms
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
        return {
            "agent_model": summary.get("agent_model"),
            "correctness": summary.get("aggregate_correctness_score"),
            "privacy": summary.get("aggregate_privacy_score"),
            "validation": summary.get("aggregate_validation_rate"),
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

        model_name = data.get("agent_model")
        if model_name is None:
            print(f"Warning: No agent_model found in {summary_path}", file=sys.stderr)
            continue

        if model_name not in results_by_model:
            results_by_model[model_name] = []
        results_by_model[model_name].append(data)

    return results_by_model


def calculate_stats(runs: List[Dict]) -> Dict:
    """Calculate mean and standard deviation for each metric."""
    correctness_scores = [run["correctness"] for run in runs]
    privacy_scores = [run["privacy"] for run in runs]
    validation_rates = [run["validation"] for run in runs]

    return {
        "correctness_mean": np.mean(correctness_scores),
        "correctness_std": np.std(correctness_scores, ddof=1) if len(correctness_scores) > 1 else 0,
        "privacy_mean": np.mean(privacy_scores),
        "privacy_std": np.std(privacy_scores, ddof=1) if len(privacy_scores) > 1 else 0,
        "validation_mean": np.mean(validation_rates),
        "validation_std": np.std(validation_rates, ddof=1) if len(validation_rates) > 1 else 0,
        "n_runs": len(runs),
    }


def plot_results(model_stats: Dict[str, Dict], output_path: Path):
    """Create grouped bar chart with error bars."""

    model_names = []
    model_labels = []
    correctness_means = []
    correctness_stds = []
    privacy_means = []
    privacy_stds = []

    for model_name, stats in sorted(model_stats.items()):
        model_names.append(model_name)
        n_runs = stats["n_runs"]
        run_label = "run" if n_runs == 1 else "runs"
        model_labels.append(f"{model_name} ({n_runs} {run_label})")
        correctness_means.append(stats["correctness_mean"])
        correctness_stds.append(stats["correctness_std"])
        privacy_means.append(stats["privacy_mean"])
        privacy_stds.append(stats["privacy_std"])

    x = np.arange(len(model_names))
    width = 0.35

    fig, ax = plt.subplots(figsize=(10, 6))

    bars1 = ax.bar(
        x - width / 2,
        correctness_means,
        width,
        yerr=correctness_stds,
        capsize=5,
        label="Correctness",
        color="#2E86AB",
        alpha=0.8,
    )
    bars2 = ax.bar(
        x + width / 2,
        privacy_means,
        width,
        yerr=privacy_stds,
        capsize=5,
        label="Privacy",
        color="#A23B72",
        alpha=0.8,
    )

    ax.set_ylabel("Score", fontsize=12)
    ax.set_title("Form Filling Experiment Results", fontsize=14, fontweight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels(model_labels)
    ax.legend(loc="upper right", fontsize=10)
    ax.set_ylim(0, 1.1)
    ax.grid(axis="y", alpha=0.3, linestyle="--")

    def add_value_labels(bars, values, stds):
        for bar, val, std in zip(bars, values, stds):
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2.0,
                height + std + 0.02,
                f"{val:.3f}",
                ha="center",
                va="bottom",
                fontsize=9,
            )

    add_value_labels(bars1, correctness_means, correctness_stds)
    add_value_labels(bars2, privacy_means, privacy_stds)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    print(f"Saved plot to: {output_path}")


def print_summary_statistics(model_stats: Dict[str, Dict]):
    """Print formatted summary statistics to console."""
    print("\n" + "=" * 60)
    print("SUMMARY STATISTICS")
    print("=" * 60)

    for model_name, stats in sorted(model_stats.items()):
        print(f"\nModel: {model_name}")
        print(f"  Number of runs: {stats['n_runs']}")
        print(f"  Correctness: {stats['correctness_mean']:.3f} ± {stats['correctness_std']:.3f}")
        print(f"  Privacy: {stats['privacy_mean']:.3f} ± {stats['privacy_std']:.3f}")
        print(f"  Validation: {stats['validation_mean']:.3f} ± {stats['validation_std']:.3f}")


def main():
    parser = argparse.ArgumentParser(
        description="Plot form filling experiment results from summary.json files"
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
