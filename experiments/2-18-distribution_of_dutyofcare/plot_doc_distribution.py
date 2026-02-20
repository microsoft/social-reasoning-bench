#!/usr/bin/env python3
"""Plot distribution of duty of care scores across experimental conditions.

Tests the hypothesis that preference-exposed + negotiation yields bimodal
distributions (exploited vs not-exploited) while hidden preferences yield
unimodal distributions.

Usage:
    uv run experiments/2-18-distribution_of_dutyofcare/plot_doc_distribution.py \
        outputs/calendar_scheduling/2-4-simple-prefs \
        outputs/calendar_scheduling/2-10-negotiation

    # With per-model breakdown:
    uv run experiments/2-18-distribution_of_dutyofcare/plot_doc_distribution.py \
        outputs/calendar_scheduling/2-4-simple-prefs \
        outputs/calendar_scheduling/2-10-negotiation \
        --per-model
"""

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Optional

import matplotlib.pyplot as plt
import numpy as np

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

SCRIPT_DIR = Path(__file__).parent

CONDITIONS = ["hidden", "exposed", "negotiation_hidden", "negotiation_exposed"]
CONDITION_LABELS = {
    "hidden": "Hidden Prefs",
    "exposed": "Exposed Prefs",
    "negotiation_hidden": "Hidden + Negotiation",
    "negotiation_exposed": "Exposed + Negotiation",
}
COLORS = {
    "hidden": "#2D3047",
    "exposed": "#5C7ABF",
    "negotiation_hidden": "#E8913A",
    "negotiation_exposed": "#D64933",
}


# ---------------------------------------------------------------------------
# File discovery (adapted from plot_due_diligence.py)
# ---------------------------------------------------------------------------


def discover_eval_files(input_dirs: list[Path]) -> list[Path]:
    """Find all eval JSON files across input directories.

    Handles two layouts:
    - Direct JSON files in directory (e.g. 2-2 pattern)
    - Subdirectories each containing eval.json (e.g. 2-4/2-10 pattern)
    """
    seen: set[Path] = set()
    files: list[Path] = []
    for d in input_dirs:
        # Pattern 1: JSON files directly in directory
        for f in sorted(d.glob("*.json")):
            resolved = f.resolve()
            if resolved not in seen:
                seen.add(resolved)
                files.append(f)
        # Pattern 2: eval.json in subdirectories
        for f in sorted(d.glob("*/eval.json")):
            resolved = f.resolve()
            if resolved not in seen:
                seen.add(resolved)
                files.append(f)
    return files


# ---------------------------------------------------------------------------
# Data loading (adapted from plot_due_diligence.py)
# ---------------------------------------------------------------------------


def load_eval_file(filepath: Path) -> Optional[dict]:
    """Load an eval JSON file and extract label, metadata, and results."""
    try:
        with open(filepath, "r") as f:
            data = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"Warning: Failed to load {filepath}: {e}", file=sys.stderr)
        return None

    if not isinstance(data, dict) or "results" not in data or "metadata" not in data:
        print(f"Warning: Unexpected format in {filepath}", file=sys.stderr)
        return None

    metadata = data["metadata"]

    # Derive label and dataset from path
    if filepath.name == "eval.json":
        short_label = filepath.parent.name
        dataset = filepath.parent.parent.name
    else:
        short_label = filepath.stem
        dataset = filepath.parent.name

    # Extract model short name
    model_full = metadata.get("assistant_model", "unknown")
    model = model_full.split("/")[-1]

    return {
        "filepath": str(filepath),
        "label": f"{dataset}/{short_label}",
        "short_label": short_label,
        "dataset": dataset,
        "model": model,
        "expose_preferences": metadata.get("expose_preferences"),
        "results": data["results"],
    }


# ---------------------------------------------------------------------------
# Condition classification
# ---------------------------------------------------------------------------


def classify_condition(eval_data: dict) -> Optional[str]:
    """Classify an eval file into one of the 4 primary conditions.

    Returns one of: 'hidden', 'exposed', 'negotiation_hidden', 'negotiation_exposed'
    or None if it doesn't fit the 4-condition schema.
    """
    dataset = eval_data["dataset"]
    exposed = eval_data["expose_preferences"]

    if "simple-prefs" in dataset or "duty_of_care" in dataset:
        # 2-4 baseline (no negotiation)
        return "exposed" if exposed else "hidden"
    elif "negotiation" in dataset:
        # 2-10 negotiation
        return "negotiation_exposed" if exposed else "negotiation_hidden"
    return None


# ---------------------------------------------------------------------------
# Score extraction
# ---------------------------------------------------------------------------


def extract_scores(results: list[dict]) -> list[float]:
    """Extract per-sample duty of care scores with null handling.

    Null handling rules (consistent with existing codebase):
    - score=None + unsatisfiable + no meeting -> 1.0
    - score=None + unsatisfiable + meeting -> 0.0
    - score=None + satisfiable + no meeting -> 0.0
    """
    scores = []
    for r in results:
        task = r.get("execution", {}).get("task", {})
        satisfiable = task.get("satisfiable", True)
        scheduled_meeting = r.get("scheduled_meeting")
        score = r.get("assistant_duty_of_care_score")

        if score is None:
            if not satisfiable:
                score = 1.0 if scheduled_meeting is None else 0.0
            elif satisfiable and scheduled_meeting is None:
                score = 0.0

        if score is not None:
            scores.append(score)
    return scores


# ---------------------------------------------------------------------------
# Bimodality coefficient
# ---------------------------------------------------------------------------


def bimodality_coefficient(scores: list[float]) -> float:
    """Compute Sarle's bimodality coefficient.

    BC = (skewness^2 + 1) / (kurtosis_excess + 3 * (n-1)^2 / ((n-2)*(n-3)))

    BC > 0.555 suggests bimodality (uniform distribution threshold).
    Uses only numpy (no scipy needed).
    """
    n = len(scores)
    if n < 4:
        return float("nan")
    arr = np.array(scores)
    m2 = np.mean((arr - arr.mean()) ** 2)
    if m2 == 0:
        return float("nan")
    m3 = np.mean((arr - arr.mean()) ** 3)
    m4 = np.mean((arr - arr.mean()) ** 4)
    skew = m3 / (m2**1.5)
    kurt_excess = (m4 / (m2**2)) - 3
    bc = (skew**2 + 1) / (kurt_excess + 3 * (n - 1) ** 2 / ((n - 2) * (n - 3)))
    return bc


# ---------------------------------------------------------------------------
# Styling
# ---------------------------------------------------------------------------


def style_axis(ax):
    """Apply Tufte-style axis formatting."""
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_linewidth(0.5)
    ax.spines["bottom"].set_linewidth(0.5)
    ax.tick_params(width=0.5)
    ax.set_axisbelow(True)
    ax.grid(True, axis="y", linestyle=":", alpha=0.4, color="#cccccc")


# ---------------------------------------------------------------------------
# Plotting
# ---------------------------------------------------------------------------


def plot_aggregate_histograms(
    grouped_scores: dict[str, list[float]],
    output_path: Path,
):
    """Create vertically stacked histograms for each condition (all models pooled)."""
    fig, axes = plt.subplots(4, 1, figsize=(8, 10), sharex=True, sharey=True)

    bins = np.linspace(0, 1.0, 11)  # 10 bins over [0, 1]

    for ax, condition in zip(axes, CONDITIONS):
        scores = grouped_scores.get(condition, [])
        if not scores:
            ax.set_title(f"{CONDITION_LABELS[condition]} (no data)", fontsize=11, loc="left")
            style_axis(ax)
            continue

        arr = np.array(scores)
        ax.hist(
            scores,
            bins=bins,
            color=COLORS[condition],
            edgecolor="white",
            alpha=0.85,
        )
        ax.set_ylabel("Count", fontsize=10)
        ax.set_title(CONDITION_LABELS[condition], fontsize=11, fontweight="semibold", loc="left")
        style_axis(ax)

        # Annotate with statistics
        bc = bimodality_coefficient(scores)
        bc_str = f"{bc:.3f}" if not np.isnan(bc) else "N/A"
        bc_flag = " *" if not np.isnan(bc) and bc > 0.555 else ""
        ax.text(
            0.98,
            0.85,
            f"n={len(scores)}  mean={arr.mean():.2f}  median={np.median(arr):.2f}  BC={bc_str}{bc_flag}",
            transform=ax.transAxes,
            ha="right",
            fontsize=8.5,
            color="#444444",
        )

    axes[-1].set_xlabel("Duty of Care Score", fontsize=11)
    axes[-1].set_xlim(-0.02, 1.05)

    fig.suptitle(
        "Distribution of Duty of Care Scores by Condition",
        fontsize=13,
        fontweight="semibold",
        y=0.98,
    )
    fig.text(
        0.5,
        0.945,
        "* BC > 0.555 suggests bimodal distribution",
        ha="center",
        fontsize=8,
        color="#888888",
        style="italic",
    )

    plt.tight_layout(rect=[0, 0, 1, 0.93])
    plt.savefig(output_path, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close()
    print(f"Saved: {output_path}")


def plot_per_model_grid(
    model_scores: dict[str, dict[str, list[float]]],
    output_path: Path,
):
    """Create a grid of histograms: rows=conditions, cols=models."""
    models = sorted(model_scores.keys())
    n_models = len(models)
    if n_models == 0:
        print("No per-model data to plot.", file=sys.stderr)
        return

    fig, axes = plt.subplots(
        len(CONDITIONS),
        n_models,
        figsize=(5 * n_models, 2.5 * len(CONDITIONS)),
        sharex=True,
        sharey="row",
    )

    # Handle single-model case
    if n_models == 1:
        axes = axes.reshape(-1, 1)

    bins = np.linspace(0, 1.0, 11)

    for row, condition in enumerate(CONDITIONS):
        for col, model in enumerate(models):
            ax = axes[row, col]
            scores = model_scores[model].get(condition, [])

            if scores:
                ax.hist(
                    scores,
                    bins=bins,
                    color=COLORS[condition],
                    edgecolor="white",
                    alpha=0.85,
                )
                arr = np.array(scores)
                ax.text(
                    0.95,
                    0.85,
                    f"n={len(scores)}\nmean={arr.mean():.2f}",
                    transform=ax.transAxes,
                    ha="right",
                    fontsize=7.5,
                    color="#444444",
                )
            else:
                ax.text(
                    0.5,
                    0.5,
                    "no data",
                    transform=ax.transAxes,
                    ha="center",
                    va="center",
                    fontsize=9,
                    color="#999999",
                )

            if row == 0:
                ax.set_title(model, fontsize=11, fontweight="semibold")
            if col == 0:
                ax.set_ylabel(CONDITION_LABELS[condition], fontsize=9)

            style_axis(ax)

    # Label bottom row
    for col in range(n_models):
        axes[-1, col].set_xlabel("Duty of Care Score", fontsize=9)
        axes[-1, col].set_xlim(-0.02, 1.05)

    fig.suptitle(
        "Duty of Care Distribution by Model and Condition",
        fontsize=13,
        fontweight="semibold",
        y=1.01,
    )

    plt.tight_layout()
    plt.savefig(output_path, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close()
    print(f"Saved: {output_path}")


# ---------------------------------------------------------------------------
# Console summary
# ---------------------------------------------------------------------------


def print_summary(
    grouped_scores: dict[str, list[float]],
    model_scores: dict[str, dict[str, list[float]]],
):
    """Print per-condition distribution statistics."""
    print(f"\n{'=' * 85}")
    print("DUTY OF CARE DISTRIBUTION SUMMARY (all models pooled)")
    print(f"{'=' * 85}")
    print(
        f"{'Condition':<25} {'N':>5} {'Mean':>7} {'Median':>7} "
        f"{'Std':>7} {'Min':>7} {'Max':>7} {'BC':>7}"
    )
    print("-" * 85)

    for condition in CONDITIONS:
        scores = grouped_scores.get(condition, [])
        if not scores:
            print(f"{CONDITION_LABELS[condition]:<25} {'N/A':>5}")
            continue
        arr = np.array(scores)
        bc = bimodality_coefficient(scores)
        bc_str = f"{bc:.3f}" if not np.isnan(bc) else "N/A"
        bc_flag = " *" if not np.isnan(bc) and bc > 0.555 else ""
        print(
            f"{CONDITION_LABELS[condition]:<25} {len(scores):>5} "
            f"{arr.mean():>7.3f} {np.median(arr):>7.3f} "
            f"{arr.std():>7.3f} {arr.min():>7.3f} {arr.max():>7.3f} "
            f"{bc_str:>7}{bc_flag}"
        )

    print(f"\n* BC > 0.555 suggests bimodal distribution")

    # Per-model breakdown
    models = sorted(model_scores.keys())
    if models:
        print(f"\n{'=' * 85}")
        print("PER-MODEL BREAKDOWN")
        print(f"{'=' * 85}")
        print(f"{'Model':<12} {'Condition':<25} {'N':>5} {'Mean':>7} {'Median':>7} {'BC':>7}")
        print("-" * 85)

        for model in models:
            for condition in CONDITIONS:
                scores = model_scores[model].get(condition, [])
                if not scores:
                    continue
                arr = np.array(scores)
                bc = bimodality_coefficient(scores)
                bc_str = f"{bc:.3f}" if not np.isnan(bc) else "N/A"
                bc_flag = " *" if not np.isnan(bc) and bc > 0.555 else ""
                print(
                    f"{model:<12} {CONDITION_LABELS[condition]:<25} {len(scores):>5} "
                    f"{arr.mean():>7.3f} {np.median(arr):>7.3f} {bc_str:>7}{bc_flag}"
                )

    print(f"{'=' * 85}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main():
    parser = argparse.ArgumentParser(
        description="Plot distribution of duty of care scores across conditions."
    )
    parser.add_argument(
        "input_dirs",
        nargs="+",
        help="Directories containing eval JSON files (e.g. 2-4-simple-prefs, 2-10-negotiation)",
    )
    parser.add_argument(
        "--per-model",
        action="store_true",
        help="Generate per-model faceted grid in addition to the aggregate plot",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Output path for the aggregate plot (default: doc_distribution.png in script dir)",
    )
    args = parser.parse_args()

    input_dirs = [Path(d) for d in args.input_dirs]
    for d in input_dirs:
        if not d.exists():
            print(f"Error: Directory {d} does not exist", file=sys.stderr)
            sys.exit(1)

    output_path = Path(args.output) if args.output else SCRIPT_DIR / "doc_distribution.png"

    # Discover and load eval files
    eval_files = discover_eval_files(input_dirs)
    if not eval_files:
        print("Error: No eval JSON files found", file=sys.stderr)
        sys.exit(1)
    print(f"Found {len(eval_files)} eval file(s)")

    eval_data_list = []
    for f in eval_files:
        data = load_eval_file(f)
        if data is not None:
            eval_data_list.append(data)
    print(f"Loaded {len(eval_data_list)} valid eval file(s)")

    # Group scores by condition and by model+condition
    grouped_scores: dict[str, list[float]] = defaultdict(list)
    model_scores: dict[str, dict[str, list[float]]] = defaultdict(lambda: defaultdict(list))

    for eval_data in eval_data_list:
        condition = classify_condition(eval_data)
        if condition is None:
            print(f"  Skipping {eval_data['label']} (unrecognized dataset)")
            continue

        scores = extract_scores(eval_data["results"])
        model = eval_data["model"]

        print(f"  {eval_data['label']}: condition={condition}, model={model}, n={len(scores)}")

        grouped_scores[condition].extend(scores)
        model_scores[model][condition].extend(scores)

    # Check we have data
    total = sum(len(s) for s in grouped_scores.values())
    if total == 0:
        print("Error: No duty of care scores found", file=sys.stderr)
        sys.exit(1)
    print(f"\nTotal scores: {total}")

    # Print summary
    print_summary(dict(grouped_scores), dict(model_scores))

    # Plot aggregate histograms
    plot_aggregate_histograms(dict(grouped_scores), output_path)

    # Plot per-model grid if requested
    if args.per_model:
        per_model_path = output_path.with_name(output_path.stem + "_per_model" + output_path.suffix)
        plot_per_model_grid(dict(model_scores), per_model_path)


if __name__ == "__main__":
    main()
