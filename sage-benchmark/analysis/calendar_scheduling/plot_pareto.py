#!/usr/bin/env python3
"""Plot Pareto front of scheduling success vs privacy preservation.

Usage:
    uv run analysis/calendar_scheduling/plot_pareto.py <input_dir> [--output <path>]

Example:
    uv run analysis/calendar_scheduling/plot_pareto.py outputs/calendar_scheduling
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Optional

import matplotlib.pyplot as plt
import numpy as np


def extract_model_from_filename(filepath: Path) -> Optional[str]:
    """Extract model name from filename.

    Supports patterns:
    - Old: calendar_scheduling_{MODEL}_{TIMESTAMP}.json
    - New: {TIMESTAMP}_calendar_scheduling_assistant_{MODEL}_requestor_{MODEL}_judge_{JUDGE}.json
    """
    # Try new pattern first (with requestor field)
    new_match = re.match(
        r"\d{8}_\d{6}_calendar_scheduling_assistant_(.+?)_requestor_.+_judge_.+\.json",
        filepath.name,
    )
    if new_match:
        return new_match.group(1)

    # Fall back to old pattern
    old_match = re.match(r"calendar_scheduling_(.+)_\d{8}_\d{6}\.json", filepath.name)
    return old_match.group(1) if old_match else None


def load_result_file(filepath: Path) -> Optional[dict]:
    """Load and extract metrics from a result JSON file."""
    try:
        with open(filepath, "r") as f:
            data = json.load(f)

        # Handle both formats: bare list or dict with 'results' key
        if isinstance(data, dict):
            results = data.get("results", [])
        elif isinstance(data, list):
            results = data
        else:
            return None

        if len(results) == 0:
            return None

        success_count = sum(
            1 for r in results if r.get("appropriately_scheduled_or_notscheduled", False)
        )
        success_rate = success_count / len(results)

        leakage_rates = [r.get("leakage_rate", 0.0) for r in results]
        avg_leakage = np.mean(leakage_rates)
        privacy_rate = 1.0 - avg_leakage

        return {
            "success_rate": success_rate,
            "privacy_rate": privacy_rate,
            "n_tasks": len(results),
        }
    except (json.JSONDecodeError, KeyError, FileNotFoundError) as e:
        print(f"Warning: Failed to load {filepath}: {e}", file=sys.stderr)
        return None


def aggregate_by_model(input_dir: Path) -> dict[str, list[dict]]:
    """Load all result files and group by model."""
    results_by_model: dict[str, list[dict]] = {}

    for filepath in input_dir.glob("*calendar_scheduling*.json"):
        model_name = extract_model_from_filename(filepath)
        if model_name is None:
            print(f"Warning: Could not extract model from {filepath.name}", file=sys.stderr)
            continue

        data = load_result_file(filepath)
        if data is None:
            continue

        if model_name not in results_by_model:
            results_by_model[model_name] = []
        results_by_model[model_name].append(data)

    return results_by_model


def calculate_stats(runs: list[dict]) -> dict:
    """Calculate mean and std for each metric across runs."""
    success_rates = [r["success_rate"] for r in runs]
    privacy_rates = [r["privacy_rate"] for r in runs]
    total_tasks = sum(r["n_tasks"] for r in runs)

    return {
        "success_mean": np.mean(success_rates),
        "success_std": np.std(success_rates, ddof=1) if len(success_rates) > 1 else 0,
        "privacy_mean": np.mean(privacy_rates),
        "privacy_std": np.std(privacy_rates, ddof=1) if len(privacy_rates) > 1 else 0,
        "n_runs": len(runs),
        "total_tasks": total_tasks,
    }


def plot_pareto(model_stats: dict[str, dict], output_path: Path):
    """Create Pareto front scatter plot."""
    fig, ax = plt.subplots(figsize=(7, 5))

    # Grayscale-friendly markers
    markers = ["o", "s", "^", "D", "v", "<", ">", "p", "h"]
    colors = ["#1a1a1a", "#4d4d4d", "#808080", "#999999", "#b3b3b3"]

    legend_handles = []
    legend_labels = []

    for i, (model_name, stats) in enumerate(sorted(model_stats.items())):
        marker = markers[i % len(markers)]
        color = colors[i % len(colors)]

        ax.errorbar(
            stats["privacy_mean"],
            stats["success_mean"],
            xerr=stats["privacy_std"],
            yerr=stats["success_std"],
            fmt=marker,
            color=color,
            markersize=8,
            capsize=4,
            capthick=1.5,
            elinewidth=1.5,
        )

        # Create clean legend entry with just the marker
        handle = ax.scatter([], [], marker=marker, color=color, s=64)
        legend_handles.append(handle)
        legend_labels.append(f"{model_name} (n={stats['n_runs']})")

    ax.set_xlabel("Privacy Preservation Rate", fontsize=11)
    ax.set_ylabel("Appropriate Scheduling Rate", fontsize=11)
    ax.set_xlim(-0.05, 1.05)
    ax.set_ylim(-0.05, 1.05)

    # Minimal grid
    ax.set_axisbelow(True)
    ax.grid(True, linestyle=":", alpha=0.5, color="#cccccc")

    # Remove top and right spines (Tufte)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # Legend with clean markers only (no error bar clutter)
    ax.legend(
        legend_handles,
        legend_labels,
        loc="upper left",
        bbox_to_anchor=(0.02, 0.98),
        frameon=True,
        fancybox=False,
        edgecolor="#cccccc",
        fontsize=9,
    )

    # Annotation for total runs
    total_runs = sum(s["n_runs"] for s in model_stats.values())
    total_tasks = sum(s["total_tasks"] for s in model_stats.values())
    ax.text(
        0.98,
        0.02,
        f"{total_runs} runs, {total_tasks} tasks",
        transform=ax.transAxes,
        fontsize=8,
        ha="right",
        va="bottom",
        color="#666666",
    )

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    print(f"Saved plot to: {output_path}")


def print_summary(model_stats: dict[str, dict]):
    """Print summary statistics to console."""
    print("\n" + "=" * 65)
    print("PARETO FRONT SUMMARY")
    print("=" * 65)
    print(f"{'Model':<20} {'Runs':>5} {'Success':>18} {'Privacy':>18}")
    print("-" * 65)

    for model_name, stats in sorted(model_stats.items()):
        success_str = f"{stats['success_mean']:.3f} +/- {stats['success_std']:.3f}"
        privacy_str = f"{stats['privacy_mean']:.3f} +/- {stats['privacy_std']:.3f}"
        print(f"{model_name:<20} {stats['n_runs']:>5} {success_str:>18} {privacy_str:>18}")

    print("=" * 65)


def main():
    parser = argparse.ArgumentParser(
        description="Plot Pareto front of scheduling success vs privacy preservation"
    )
    parser.add_argument(
        "input_dir",
        type=Path,
        help="Directory containing calendar_scheduling_*.json result files",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Output plot path (default: <input_dir>/pareto_front.png)",
    )

    args = parser.parse_args()

    if not args.input_dir.exists():
        print(f"Error: Directory {args.input_dir} does not exist", file=sys.stderr)
        sys.exit(1)

    output_path = args.output if args.output else args.input_dir / "pareto_front.png"

    print(f"Loading results from: {args.input_dir}")
    results_by_model = aggregate_by_model(args.input_dir)

    if not results_by_model:
        print("Error: No valid result files found", file=sys.stderr)
        sys.exit(1)

    print(f"Found {len(results_by_model)} model(s)")

    model_stats = {model: calculate_stats(runs) for model, runs in results_by_model.items()}

    plot_pareto(model_stats, output_path)
    print_summary(model_stats)


if __name__ == "__main__":
    main()
