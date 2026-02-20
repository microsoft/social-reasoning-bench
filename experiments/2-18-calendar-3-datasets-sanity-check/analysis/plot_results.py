#!/usr/bin/env python3
"""Plot sanity check results across 3 dataset sizes.

Generates two plots:
1. Aggregate duty of care by dataset size, per model (hidden vs exposed prefs)
2. Duty of care broken down by number of free slots (2 models × 3 datasets grid)

Usage:
    uv run python experiments/2-18-calendar-3-datasets-sanity-check/analysis/plot_results.py
"""

import json
from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

SCRIPT_DIR = Path(__file__).parent
OUTPUT_BASE = SCRIPT_DIR.parent.parent.parent / "outputs/calendar_scheduling/2-18-sanity"

MODELS = ["gpt-4.1", "gpt-5.1"]
DATASETS = ["small", "medium", "large"]
DATASET_LABELS = {"small": "Small\n(n=21)", "medium": "Medium\n(n=70)", "large": "Large\n(n=140)"}
FREE_SLOT_LEVELS = [0, 1, 3, 5, 7, 9, 11]

COLORS = {
    "hidden": "#2D3047",
    "exposed": "#E07B39",
}


def load_eval(model: str, dataset: str, expose_prefs: bool) -> dict:
    prefs_dir = f"expose_prefs_{str(expose_prefs).lower()}"
    path = OUTPUT_BASE / model / dataset / prefs_dir / "eval.json"
    with open(path) as f:
        return json.load(f)


def load_all_results() -> dict[str, dict[str, dict[str, dict]]]:
    """Load all results keyed by [model][dataset][condition]."""
    all_results = {}
    for model in MODELS:
        all_results[model] = {}
        for dataset in DATASETS:
            all_results[model][dataset] = {
                "hidden": load_eval(model, dataset, expose_prefs=False),
                "exposed": load_eval(model, dataset, expose_prefs=True),
            }
    return all_results


def get_doc_by_slots(data: dict) -> dict[int, list[float]]:
    """Get duty of care scores grouped by free slot count."""
    scores: dict[int, list[float]] = defaultdict(list)
    for result in data.get("results", []):
        task = result["execution"]["task"]
        free_slots = task["free_slots_count"]
        score = result.get("assistant_duty_of_care_score")
        if score is not None:
            scores[free_slots].append(score)
    return scores


def style_axis(ax):
    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)
    for spine in ["left", "bottom"]:
        ax.spines[spine].set_linewidth(0.5)
    ax.tick_params(width=0.5)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f"{int(y)}%"))


def plot_aggregate(all_results: dict, output_path: Path):
    """Plot 1: Aggregate DoC by dataset size, one subplot per model."""
    fig, axes = plt.subplots(1, len(MODELS), figsize=(5 * len(MODELS), 5), sharey=True)

    x = np.arange(len(DATASETS))
    width = 0.35

    for idx, model in enumerate(MODELS):
        ax = axes[idx]

        hidden_scores = [
            all_results[model][ds]["hidden"]["summary"][
                "fiduciary_avg_assistant_duty_of_care_score"
            ]
            * 100
            for ds in DATASETS
        ]
        exposed_scores = [
            all_results[model][ds]["exposed"]["summary"][
                "fiduciary_avg_assistant_duty_of_care_score"
            ]
            * 100
            for ds in DATASETS
        ]

        bars1 = ax.bar(
            x - width / 2,
            hidden_scores,
            width,
            label="Hidden Preferences" if idx == 0 else None,
            color=COLORS["hidden"],
            edgecolor="white",
        )
        bars2 = ax.bar(
            x + width / 2,
            exposed_scores,
            width,
            label="Exposed Preferences" if idx == 0 else None,
            color=COLORS["exposed"],
            edgecolor="white",
        )

        ax.set_title(model, fontsize=12, fontweight="semibold")
        ax.set_xticks(x)
        ax.set_xticklabels([DATASET_LABELS[ds] for ds in DATASETS], fontsize=10)
        ax.set_ylim(0, 115)

        if idx == 0:
            ax.set_ylabel("Assistant Duty of Care (%)", fontsize=11)

        style_axis(ax)

        ax.bar_label(bars1, fmt="%.1f%%", padding=2, fontsize=9, fontweight="medium")
        ax.bar_label(bars2, fmt="%.1f%%", padding=2, fontsize=9, fontweight="medium")

    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(
        handles, labels, loc="upper center", bbox_to_anchor=(0.5, 0.97), ncol=2, frameon=False
    )

    fig.suptitle(
        "Assistant Duty of Care by Dataset Size",
        fontsize=13,
        fontweight="semibold",
        y=1.03,
    )

    plt.tight_layout(rect=[0, 0, 1, 0.90])
    plt.savefig(output_path, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close()
    print(f"Saved: {output_path}")


def plot_by_slots(all_results: dict, output_path: Path):
    """Plot 2: DoC by free slots — 2 models × 3 datasets grid, as line charts."""
    n_rows = len(MODELS)
    n_cols = len(DATASETS)
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(5 * n_cols, 4.5 * n_rows), sharey=True)

    x = np.arange(len(FREE_SLOT_LEVELS))

    for row, model in enumerate(MODELS):
        for col, dataset in enumerate(DATASETS):
            ax = axes[row][col]

            hidden_by_slots = get_doc_by_slots(all_results[model][dataset]["hidden"])
            exposed_by_slots = get_doc_by_slots(all_results[model][dataset]["exposed"])

            hidden_means = [
                np.mean(hidden_by_slots[s]) * 100 if hidden_by_slots.get(s) else 0
                for s in FREE_SLOT_LEVELS
            ]
            exposed_means = [
                np.mean(exposed_by_slots[s]) * 100 if exposed_by_slots.get(s) else 0
                for s in FREE_SLOT_LEVELS
            ]

            show_legend = row == 0 and col == 0
            ax.plot(
                x,
                hidden_means,
                color=COLORS["hidden"],
                marker="o",
                linewidth=1.5,
                markersize=5,
                label="Hidden Preferences" if show_legend else None,
            )
            ax.plot(
                x,
                exposed_means,
                color=COLORS["exposed"],
                marker="o",
                linewidth=1.5,
                markersize=5,
                label="Exposed Preferences" if show_legend else None,
            )

            ax.set_xticks(x)
            ax.set_xticklabels([str(s) for s in FREE_SLOT_LEVELS])
            ax.set_ylim(0, 115)
            style_axis(ax)

            if col == 0:
                ax.set_ylabel(f"{model}\nDuty of Care (%)", fontsize=10)
            if row == n_rows - 1:
                ax.set_xlabel("Number of Free Slots", fontsize=10)
            if row == 0:
                ax.set_title(
                    DATASET_LABELS[dataset].replace("\n", " "), fontsize=11, fontweight="semibold"
                )

            # Value labels — offset above/below to avoid overlap
            for i, (h_val, e_val) in enumerate(zip(hidden_means, exposed_means)):
                if abs(h_val - e_val) < 5:
                    ax.annotate(
                        f"{(h_val + e_val) / 2:.0f}%",
                        xy=(x[i], max(h_val, e_val) + 3),
                        ha="center",
                        fontsize=7,
                        fontweight="medium",
                    )
                else:
                    # Label the lower line below, higher line above
                    h_offset = 3 if h_val >= e_val else -8
                    e_offset = 3 if e_val >= h_val else -8
                    ax.annotate(
                        f"{h_val:.0f}%",
                        xy=(x[i], h_val + h_offset),
                        ha="center",
                        fontsize=7,
                        fontweight="medium",
                        color=COLORS["hidden"],
                    )
                    ax.annotate(
                        f"{e_val:.0f}%",
                        xy=(x[i], e_val + e_offset),
                        ha="center",
                        fontsize=7,
                        fontweight="medium",
                        color=COLORS["exposed"],
                    )

    handles, labels = axes[0][0].get_legend_handles_labels()
    fig.legend(
        handles, labels, loc="upper center", bbox_to_anchor=(0.5, 1.01), ncol=2, frameon=False
    )

    fig.suptitle(
        "Assistant Duty of Care by Free Slots",
        fontsize=13,
        fontweight="semibold",
        y=1.04,
    )

    plt.tight_layout(rect=[0, 0, 1, 0.97])
    plt.savefig(output_path, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close()
    print(f"Saved: {output_path}")


def plot_privacy_leakage(all_results: dict, output_path: Path):
    """Plot: Aggregate privacy leakage rate by dataset size, one subplot per model."""
    fig, axes = plt.subplots(1, len(MODELS), figsize=(5 * len(MODELS), 5), sharey=True)

    x = np.arange(len(DATASETS))
    width = 0.35

    for idx, model in enumerate(MODELS):
        ax = axes[idx]

        hidden_rates = [
            all_results[model][ds]["hidden"]["summary"]["privacy_leakage_rate"] * 100
            for ds in DATASETS
        ]
        exposed_rates = [
            all_results[model][ds]["exposed"]["summary"]["privacy_leakage_rate"] * 100
            for ds in DATASETS
        ]

        bars1 = ax.bar(
            x - width / 2,
            hidden_rates,
            width,
            label="Hidden Preferences" if idx == 0 else None,
            color=COLORS["hidden"],
            edgecolor="white",
        )
        bars2 = ax.bar(
            x + width / 2,
            exposed_rates,
            width,
            label="Exposed Preferences" if idx == 0 else None,
            color=COLORS["exposed"],
            edgecolor="white",
        )

        ax.set_title(model, fontsize=12, fontweight="semibold")
        ax.set_xticks(x)
        ax.set_xticklabels([DATASET_LABELS[ds] for ds in DATASETS], fontsize=10)
        ax.set_ylim(0, 35)

        if idx == 0:
            ax.set_ylabel("Privacy Leakage Rate (%)", fontsize=11)

        style_axis(ax)
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f"{int(y)}%"))

        ax.bar_label(bars1, fmt="%.1f%%", padding=2, fontsize=9, fontweight="medium")
        ax.bar_label(bars2, fmt="%.1f%%", padding=2, fontsize=9, fontweight="medium")

    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(
        handles, labels, loc="upper center", bbox_to_anchor=(0.5, 0.97), ncol=2, frameon=False
    )

    fig.suptitle(
        "Privacy Leakage Rate by Dataset Size",
        fontsize=13,
        fontweight="semibold",
        y=1.03,
    )

    plt.tight_layout(rect=[0, 0, 1, 0.90])
    plt.savefig(output_path, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close()
    print(f"Saved: {output_path}")


def print_summary(all_results: dict):
    print("\n" + "=" * 60)
    print("Assistant Duty of Care Summary")
    print("=" * 60)
    for model in MODELS:
        print(f"\n{model}:")
        for dataset in DATASETS:
            hidden = all_results[model][dataset]["hidden"]["summary"][
                "fiduciary_avg_assistant_duty_of_care_score"
            ]
            exposed = all_results[model][dataset]["exposed"]["summary"][
                "fiduciary_avg_assistant_duty_of_care_score"
            ]
            diff = (exposed - hidden) * 100
            n = all_results[model][dataset]["hidden"]["metadata"]["task_count"]
            print(
                f"  {dataset:8s} (n={n:3d})  hidden={hidden * 100:.1f}%  exposed={exposed * 100:.1f}%  Δ={diff:+.1f}%"
            )


def print_duration_errors(all_results: dict):
    """Print summary of meetings scheduled with wrong duration."""
    from collections import Counter

    print("\n" + "=" * 60)
    print("Duration Error Summary")
    print("=" * 60)

    total_scheduled = 0
    total_wrong = 0

    for model in MODELS:
        wrong_durations: list[int] = []
        model_scheduled = 0
        for dataset in DATASETS:
            for condition in ["hidden", "exposed"]:
                for result in all_results[model][dataset][condition].get("results", []):
                    if result.get("scheduled_meeting") is not None:
                        model_scheduled += 1
                        if result.get("scheduled_duration_error") not in (0, None):
                            wrong_durations.append(result["scheduled_meeting"]["duration_minutes"])

        total_scheduled += model_scheduled
        total_wrong += len(wrong_durations)

        pct = len(wrong_durations) / model_scheduled * 100 if model_scheduled else 0
        if wrong_durations:
            counts = sorted(Counter(wrong_durations).items())
            dur_str = ", ".join(f"{dur}min×{n}" for dur, n in counts)
            print(
                f"\n{model}: {len(wrong_durations)}/{model_scheduled} ({pct:.1f}%) wrong duration — {dur_str}"
            )
        else:
            print(f"\n{model}: 0/{model_scheduled} wrong duration (all correct)")

    overall_pct = total_wrong / total_scheduled * 100 if total_scheduled else 0
    print(
        f"\nOverall: {total_wrong}/{total_scheduled} ({overall_pct:.1f}%) scheduled meetings had wrong duration"
    )


def print_zero_slot_behavior(all_results: dict):
    """Print how often models schedule meetings when the calendar is fully booked."""
    print("\n" + "=" * 60)
    print("0 Free Slots — Incorrect Scheduling Rate")
    print("=" * 60)

    total_scheduled = 0
    total_tasks = 0

    for model in MODELS:
        model_scheduled = 0
        model_tasks = 0
        for dataset in DATASETS:
            for condition in ["hidden", "exposed"]:
                for result in all_results[model][dataset][condition].get("results", []):
                    if result["execution"]["task"]["free_slots_count"] == 0:
                        model_tasks += 1
                        if result.get("scheduled_meeting") is not None:
                            model_scheduled += 1

        total_scheduled += model_scheduled
        total_tasks += model_tasks
        pct = model_scheduled / model_tasks * 100 if model_tasks else 0
        print(
            f"\n{model}: {model_scheduled}/{model_tasks} ({pct:.1f}%) scheduled a meeting when calendar was fully booked"
        )

    overall_pct = total_scheduled / total_tasks * 100 if total_tasks else 0
    print(
        f"\nOverall: {total_scheduled}/{total_tasks} ({overall_pct:.1f}%) incorrectly scheduled when fully booked"
    )


def main():
    if not OUTPUT_BASE.exists():
        print(f"Output directory not found: {OUTPUT_BASE}")
        return

    print("Loading results...")
    all_results = load_all_results()

    print_summary(all_results)
    print_duration_errors(all_results)
    print_zero_slot_behavior(all_results)

    print("\nGenerating plots...")
    plot_aggregate(all_results, SCRIPT_DIR / "duty_of_care_aggregate.png")
    plot_by_slots(all_results, SCRIPT_DIR / "duty_of_care_by_slots.png")
    plot_privacy_leakage(all_results, SCRIPT_DIR / "privacy_leakage.png")


if __name__ == "__main__":
    main()
