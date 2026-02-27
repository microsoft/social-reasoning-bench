#!/usr/bin/env python3
"""Generate comparison plots for split whimsical strategy experiment."""

import json
import re
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Must match experiment_whimsical_strategy.py
NUM_STRATEGIES = 10
TASK_TYPES = ["privacy", "duty_of_care"]


def discover_models(outputs_dir: Path) -> list[str]:
    """Discover requestor model labels from completed baseline runs."""
    models = []
    for path in sorted(outputs_dir.glob("baseline_*")):
        if (path / "eval.json").exists():
            models.append(re.sub(r"^baseline_", "", path.name))
    return models


def load_result(output_dir: Path) -> dict | None:
    """Load the benchmark output JSON from a directory."""
    eval_file = output_dir / "eval.json"
    if not eval_file.exists():
        return None
    with open(eval_file) as f:
        return json.load(f)


def plot_task_type(
    task_type: str,
    outputs_dir: Path,
    baselines: dict,
    experiment_dir: Path,
    requestor_models: list[str],
) -> None:
    """Generate bar chart for a single task type."""
    if task_type == "privacy":
        metric_key = "privacy_avg_leakage_rate"
        metric_label = "Leakage Rate"
        higher_is_worse = True
    else:
        metric_key = "fiduciary_avg_assistant_duty_of_care_score"
        metric_label = "Duty of Care Score"
        higher_is_worse = False

    fig, ax = plt.subplots(figsize=(14, 6))

    n_models = len(requestor_models)
    x = np.arange(NUM_STRATEGIES)
    width = 0.8 / n_models

    for j, model in enumerate(requestor_models):
        values = []
        for i in range(NUM_STRATEGIES):
            variant = f"{task_type}_{i}_{model}"
            result = load_result(outputs_dir / variant)
            if result:
                val = result["summary"].get(metric_key, 0 if higher_is_worse else 1)
                values.append(val)
            else:
                values.append(0)

        offset = (j - n_models / 2 + 0.5) * width
        ax.bar(x + offset, values, width, label=model, alpha=0.8)

        # Add baseline line
        baseline = baselines.get(model, {})
        base_val = baseline.get(metric_key, 0 if higher_is_worse else 1)
        ax.axhline(y=base_val, color=f"C{j}", linestyle="--", alpha=0.5, linewidth=0.8)

    ax.set_xlabel("Strategy Index")
    ax.set_ylabel(metric_label)
    ax.set_title(f"{task_type.replace('_', ' ').title()} Strategies — {metric_label} by Model")
    ax.set_xticks(x)
    ax.set_xticklabels([str(i) for i in range(NUM_STRATEGIES)])
    ax.legend()

    plt.tight_layout()
    plot_path = experiment_dir / f"{task_type}_bars.png"
    plt.savefig(plot_path, dpi=150)
    plt.close()
    print(f"Saved: {plot_path}")


def plot_heatmap(
    task_type: str,
    outputs_dir: Path,
    baselines: dict,
    experiment_dir: Path,
    requestor_models: list[str],
) -> None:
    """Generate a 2×2 heatmap: absolute values (top) and deltas from baseline (bottom)."""
    if task_type == "privacy":
        metric_key = "privacy_avg_leakage_rate"
        metric_label = "Privacy Leakage Rate"
        # For leakage: higher = worse. Colormap: white→red (absolute), diverging (delta).
        abs_cmap = "YlOrRd"
        delta_cmap = "RdYlGn_r"  # red = more leakage (bad)
        abs_vmin, abs_vmax = 0.0, 1.0
        delta_vmin, delta_vmax = -1.0, 1.0
    else:
        metric_key = "fiduciary_avg_assistant_duty_of_care_score"
        metric_label = "Duty of Care"
        # For DoC: higher = better. Colormap: white→green (absolute), diverging (delta).
        abs_cmap = "YlGn"
        delta_cmap = "RdYlGn"  # green = higher DoC (good)
        abs_vmin, abs_vmax = 0.0, 1.0
        delta_vmin, delta_vmax = -1.0, 1.0

    n_strategies = NUM_STRATEGIES
    n_models = len(requestor_models)

    # Build data matrices: row 0 = baseline, rows 1..n = strategies
    abs_core = np.full((1 + n_strategies, n_models), np.nan)
    delta_core = np.full((1 + n_strategies, n_models), np.nan)

    for j, model in enumerate(requestor_models):
        base_val = baselines.get(model, {}).get(metric_key, np.nan)
        abs_core[0, j] = base_val
        delta_core[0, j] = 0.0
        for i in range(n_strategies):
            result = load_result(outputs_dir / f"{task_type}_{i}_{model}")
            if result:
                val = result["summary"].get(metric_key)
                if val is not None:
                    abs_core[i + 1, j] = val
                    if not np.isnan(base_val):
                        delta_core[i + 1, j] = val - base_val

    # Append average column (mean across models per row)
    avg_col_abs = np.nanmean(abs_core, axis=1, keepdims=True)
    avg_col_delta = np.nanmean(delta_core, axis=1, keepdims=True)
    abs_with_avg_col = np.hstack([abs_core, avg_col_abs])
    delta_with_avg_col = np.hstack([delta_core, avg_col_delta])

    # Sort strategy rows (1..n) by their average column value
    strategy_avgs = avg_col_abs[1:, 0]  # average metric per strategy
    sort_order = (
        np.argsort(strategy_avgs)[::-1] if task_type == "privacy" else np.argsort(strategy_avgs)
    )
    strategy_indices = list(sort_order)  # original strategy indices in sorted order
    abs_strategies_sorted = abs_with_avg_col[1:][sort_order]
    delta_strategies_sorted = delta_with_avg_col[1:][sort_order]

    abs_with_avg_col = np.vstack([abs_with_avg_col[:1], abs_strategies_sorted])
    delta_with_avg_col = np.vstack([delta_with_avg_col[:1], delta_strategies_sorted])

    # Append average row (mean across strategy rows only, not baseline)
    avg_row_abs = np.nanmean(abs_with_avg_col[1:], axis=0, keepdims=True)
    avg_row_delta = np.nanmean(delta_with_avg_col[1:], axis=0, keepdims=True)
    abs_data = np.vstack([abs_with_avg_col, avg_row_abs])
    delta_data = np.vstack([delta_with_avg_col, avg_row_delta])

    n_cols = n_models + 1  # models + avg column
    n_rows = 1 + n_strategies + 1  # baseline + strategies + avg row
    row_labels = ["Baseline"] + [f"Strategy {i}" for i in strategy_indices] + ["Average"]
    col_labels = requestor_models + ["Average"]

    fig, axes = plt.subplots(1, 2, figsize=(4 + 2 * n_cols, 1.5 + 0.6 * n_rows))
    fig.suptitle(
        f"Split Whimsical: {metric_label} ({task_type.replace('_', ' ').title()} Strategies)\n"
        "Assistant: gpt-4.1 · no-cot · exposed prefs · privacy-ci",
        fontsize=13,
        fontweight="bold",
    )

    def _draw_heatmap(ax, data, cmap, vmin, vmax, title, fmt=".0%"):
        masked = np.ma.masked_invalid(data)
        im = ax.imshow(masked, cmap=cmap, vmin=vmin, vmax=vmax, aspect="auto")
        ax.set_xticks(range(n_cols))
        ax.set_xticklabels(col_labels, fontsize=9)
        ax.xaxis.set_label_position("top")
        ax.xaxis.tick_top()
        ax.set_yticks(range(n_rows))
        ax.set_yticklabels(row_labels, fontsize=8)
        # Separator after baseline row and before average row
        ax.axhline(0.5, color="black", linewidth=1.5)
        ax.axhline(n_rows - 1.5, color="black", linewidth=1.5)
        # Separator before average column
        ax.axvline(n_cols - 1.5, color="black", linewidth=1.5)
        ax.set_title(title, fontsize=10, fontweight="semibold", pad=28)
        plt.colorbar(im, ax=ax, fraction=0.03, pad=0.04)
        for i in range(n_rows):
            for j in range(n_cols):
                val = data[i, j]
                if not np.isnan(val):
                    text = format(val, fmt) if fmt == ".0%" else f"{val:+.0%}"
                    ax.text(
                        j,
                        i,
                        text,
                        ha="center",
                        va="center",
                        fontsize=8,
                        color="black"
                        if 0.2 < abs(val) < 0.8
                        else "white"
                        if abs(val) >= 0.8
                        else "black",
                    )

    _draw_heatmap(axes[0], abs_data, abs_cmap, abs_vmin, abs_vmax, metric_label, fmt=".0%")
    _draw_heatmap(
        axes[1],
        delta_data,
        delta_cmap,
        delta_vmin,
        delta_vmax,
        f"Δ from Baseline\n(red = worse)",
        fmt="delta",
    )

    plt.tight_layout()
    plot_path = experiment_dir / f"{task_type}_heatmap.png"
    plt.savefig(plot_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Saved: {plot_path}")


def main():
    experiment_dir = Path(__file__).parent
    outputs_dir = experiment_dir / "outputs"

    requestor_models = discover_models(outputs_dir)

    # Load baselines
    baselines = {}
    for model in requestor_models:
        result = load_result(outputs_dir / f"baseline_{model}")
        if result:
            baselines[model] = {
                "privacy_avg_leakage_rate": result["summary"].get("privacy_avg_leakage_rate", 0),
                "fiduciary_avg_assistant_duty_of_care_score": result["summary"].get(
                    "fiduciary_avg_assistant_duty_of_care_score", 1
                ),
            }

    for task_type in TASK_TYPES:
        plot_task_type(task_type, outputs_dir, baselines, experiment_dir, requestor_models)
        plot_heatmap(task_type, outputs_dir, baselines, experiment_dir, requestor_models)


if __name__ == "__main__":
    main()
