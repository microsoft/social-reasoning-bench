#!/usr/bin/env python3
"""Plot negotiation experiment results.

Generates two plots:
1. Aggregate average duty of care by model (4 bars)
2. Duty of care broken down by number of free slots

Pulls hidden/exposed baselines from the 2-4 experiment and negotiation
results from the 2-10 experiment.

Usage:
    uv run python analysis/plot_results.py
"""

import json
from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Fullness levels in our dataset
FULLNESS_LEVELS = [0, 1, 3, 5, 7, 9, 11]

# Directories
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent.parent
BASELINE_OUTPUT = PROJECT_ROOT / "outputs/calendar_scheduling/2-4-simple-prefs"
NEGOTIATION_OUTPUT = PROJECT_ROOT / "outputs/calendar_scheduling/2-10-negotiation"

# 4 conditions in order
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


def load_results(results_dir: Path) -> dict:
    """Load evaluation results from a directory."""
    eval_file = results_dir / "eval.json"
    if not eval_file.exists():
        raise FileNotFoundError(f"Results file not found: {eval_file}")
    with open(eval_file) as f:
        return json.load(f)


def extract_free_slots_from_task(task: dict) -> int:
    """Extract number of free slots from a task's calendar."""
    calendar = task["assistant"]["calendar"]
    working_events = [
        e
        for e in calendar
        if "sleep" not in e.get("uid", "") and "personal" not in e.get("uid", "")
    ]
    return 11 - len(working_events)


def get_duty_of_care_by_slots(results: dict) -> dict[int, list[float]]:
    """Get assistant duty of care scores grouped by number of free slots."""
    scores_by_slots: dict[int, list[float]] = defaultdict(list)

    for result in results.get("results", []):
        task = result.get("execution", {}).get("task", {})
        free_slots = extract_free_slots_from_task(task)
        satisfiable = task.get("satisfiable", True)
        scheduled_meeting = result.get("scheduled_meeting")
        score = result.get("assistant_duty_of_care_score")

        if score is None:
            if not satisfiable:
                # Unsatisfiable: no meeting = correct (1.0), meeting = wrong (0.0)
                score = 1.0 if scheduled_meeting is None else 0.0
            elif satisfiable and scheduled_meeting is None:
                # Satisfiable but no meeting scheduled = failed to serve user
                score = 0.0

        if score is not None:
            scores_by_slots[free_slots].append(score)

    return scores_by_slots


def get_avg_doc(data: dict) -> float:
    """Compute average duty of care, treating satisfiable+no-meeting as 0."""
    scores = []
    for r in data.get("results", []):
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
    return sum(scores) / len(scores) if scores else 0.0


def discover_baseline_models(output_base: Path) -> dict[str, dict[str, Path]]:
    """Discover model result directories from the 2-4 baseline experiment."""
    model_dirs: dict[str, dict[str, Path]] = {}

    for subdir in output_base.iterdir():
        if subdir.is_dir():
            name = subdir.name
            if name.endswith("-hidden-prefs"):
                model = name.replace("-hidden-prefs", "")
                if model not in model_dirs:
                    model_dirs[model] = {}
                model_dirs[model]["hidden"] = subdir
            elif name.endswith("-exposed-prefs"):
                model = name.replace("-exposed-prefs", "")
                if model not in model_dirs:
                    model_dirs[model] = {}
                model_dirs[model]["exposed"] = subdir

    return model_dirs


def discover_negotiation_models(output_base: Path) -> dict[str, dict[str, Path]]:
    """Discover negotiation result directories (only those with eval.json)."""
    model_dirs: dict[str, dict[str, Path]] = {}

    for subdir in output_base.iterdir():
        if not subdir.is_dir():
            continue
        if not (subdir / "eval.json").exists():
            continue
        name = subdir.name
        if name.endswith("-negotiation-hidden"):
            model = name.replace("-negotiation-hidden", "")
            if model not in model_dirs:
                model_dirs[model] = {}
            model_dirs[model]["negotiation_hidden"] = subdir
        elif name.endswith("-negotiation"):
            model = name.replace("-negotiation", "")
            if model not in model_dirs:
                model_dirs[model] = {}
            model_dirs[model]["negotiation_exposed"] = subdir

    return model_dirs


def style_axis(ax):
    """Apply consistent styling to axis."""
    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)
    for spine in ["left", "bottom"]:
        ax.spines[spine].set_linewidth(0.5)
    ax.tick_params(width=0.5)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f"{int(y)}%"))


def plot_aggregate(model_results: dict[str, dict[str, dict]], output_path: Path):
    """Plot 1: Aggregate average duty of care by model (4 bars)."""
    models = sorted(model_results.keys())
    n_models = len(models)

    scores = {cond: [] for cond in CONDITIONS}
    for model in models:
        for cond in CONDITIONS:
            avg = get_avg_doc(model_results[model][cond])
            scores[cond].append(avg * 100 if avg else 0)

    sample_meta = model_results[models[0]]["hidden"]["metadata"]
    task_count = sample_meta.get("task_count", 35)

    fig, ax = plt.subplots(figsize=(max(10, 4 + n_models * 4), 5))

    x = np.arange(len(models))
    width = 0.19
    offsets = [-1.5 * width, -0.5 * width, 0.5 * width, 1.5 * width]

    bars_list = []
    for cond, offset in zip(CONDITIONS, offsets):
        bars = ax.bar(
            x + offset,
            scores[cond],
            width,
            label=CONDITION_LABELS[cond],
            color=COLORS[cond],
            edgecolor="white",
        )
        bars_list.append(bars)

    ax.set_ylabel("Assistant Duty of Care (%)", fontsize=11)
    ax.set_ylim(0, 115)
    ax.set_xticks(x)
    ax.set_xticklabels(models, fontsize=11)

    style_axis(ax)

    for bars in bars_list:
        ax.bar_label(bars, fmt="%.1f%%", padding=2, fontsize=8, fontweight="medium")

    fig.suptitle(
        "Assistant Duty of Care: Baseline vs Negotiation Requestor",
        fontsize=13,
        fontweight="semibold",
        y=1.0,
    )
    fig.text(
        0.5,
        0.94,
        f"n={task_count} tasks per condition | Negotiation requestor: gemini-3-flash-preview (thinking=high)",
        ha="center",
        fontsize=9,
        color="#555555",
        style="italic",
    )

    fig.legend(loc="upper center", bbox_to_anchor=(0.5, 0.91), ncol=4, frameon=False)

    plt.tight_layout(rect=[0, 0, 1, 0.85])
    plt.savefig(output_path, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close()
    print(f"Saved: {output_path}")


def plot_by_slots(model_results: dict[str, dict[str, dict]], output_path: Path):
    """Plot 2: Duty of care by number of free slots (4 bars)."""
    num_models = len(model_results)
    fig, axes = plt.subplots(1, num_models, figsize=(7 * num_models, 5), sharey=True)

    if num_models == 1:
        axes = [axes]

    width = 0.19
    offsets = [-1.5 * width, -0.5 * width, 0.5 * width, 1.5 * width]

    for idx, (model, data) in enumerate(sorted(model_results.items())):
        ax = axes[idx]

        by_slots = {}
        for cond in CONDITIONS:
            by_slots[cond] = get_duty_of_care_by_slots(data[cond])

        means = {cond: [] for cond in CONDITIONS}
        for level in FULLNESS_LEVELS:
            for cond in CONDITIONS:
                s = by_slots[cond].get(level, [])
                means[cond].append(np.mean(s) * 100 if s else 0)

        x = np.arange(len(FULLNESS_LEVELS))

        for cond, offset in zip(CONDITIONS, offsets):
            ax.bar(
                x + offset,
                means[cond],
                width,
                label=CONDITION_LABELS[cond] if idx == 0 else None,
                color=COLORS[cond],
                edgecolor="white",
            )

        ax.set_xticks(x)
        ax.set_xticklabels([str(s) for s in FULLNESS_LEVELS])
        ax.set_xlabel("Number of Free Slots", fontsize=11)

        if idx == 0:
            ax.set_ylabel("Assistant Duty of Care (%)", fontsize=11)

        ax.set_title(model, fontsize=12, fontweight="semibold")
        ax.set_ylim(0, 115)

        style_axis(ax)

        # Value labels
        for i in range(len(FULLNESS_LEVELS)):
            vals = [means[cond][i] for cond in CONDITIONS]
            if max(vals) - min(vals) < 5:
                avg_val = np.mean(vals)
                ax.annotate(
                    f"{avg_val:.0f}%",
                    xy=(x[i], max(vals) + 2),
                    ha="center",
                    fontsize=6,
                    fontweight="medium",
                )
            else:
                for cond, offset in zip(CONDITIONS, offsets):
                    val = means[cond][i]
                    ax.annotate(
                        f"{val:.0f}%",
                        xy=(x[i] + offset, val + 2),
                        ha="center",
                        fontsize=6,
                        fontweight="medium",
                    )

    fig.suptitle(
        "Assistant Duty of Care by Calendar Fullness",
        fontsize=13,
        fontweight="semibold",
        y=1.0,
    )

    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(
        handles,
        labels,
        loc="upper center",
        bbox_to_anchor=(0.5, 0.95),
        ncol=4,
        frameon=False,
    )

    plt.tight_layout(rect=[0, 0, 1, 0.90])
    plt.savefig(output_path, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close()
    print(f"Saved: {output_path}")


def main():
    if not BASELINE_OUTPUT.exists():
        print(f"Baseline output directory not found: {BASELINE_OUTPUT}")
        print("Run the 2-4 experiment first.")
        return

    if not NEGOTIATION_OUTPUT.exists():
        print(f"Negotiation output directory not found: {NEGOTIATION_OUTPUT}")
        print("Run the 2-10 experiment first with: ./run_experiment.sh")
        return

    # Discover results
    baseline_dirs = discover_baseline_models(BASELINE_OUTPUT)
    negotiation_dirs = discover_negotiation_models(NEGOTIATION_OUTPUT)

    if not baseline_dirs:
        print("No baseline results found in 2-4 experiment.")
        return

    if not negotiation_dirs:
        print("No negotiation results found in 2-10 experiment.")
        return

    # Find models that have all four conditions
    model_results: dict[str, dict[str, dict]] = {}
    for model in baseline_dirs:
        has_baseline = "hidden" in baseline_dirs[model] and "exposed" in baseline_dirs[model]
        has_neg_exposed = (
            model in negotiation_dirs and "negotiation_exposed" in negotiation_dirs.get(model, {})
        )
        has_neg_hidden = model in negotiation_dirs and "negotiation_hidden" in negotiation_dirs.get(
            model, {}
        )

        if has_baseline and has_neg_exposed and has_neg_hidden:
            print(f"Loading {model}...")
            model_results[model] = {
                "hidden": load_results(baseline_dirs[model]["hidden"]),
                "exposed": load_results(baseline_dirs[model]["exposed"]),
                "negotiation_exposed": load_results(negotiation_dirs[model]["negotiation_exposed"]),
                "negotiation_hidden": load_results(negotiation_dirs[model]["negotiation_hidden"]),
            }
        else:
            missing = []
            if not has_baseline:
                missing.append("baseline")
            if not has_neg_exposed:
                missing.append("negotiation_exposed")
            if not has_neg_hidden:
                missing.append("negotiation_hidden")
            print(f"Skipping {model} (missing: {', '.join(missing)})")

    if not model_results:
        print("No models found with all four conditions.")
        return

    # Print summary
    print("\n" + "=" * 60)
    print("Assistant Duty of Care Summary")
    print("=" * 60)
    for model in sorted(model_results.keys()):
        data = model_results[model]
        print(f"\n{model}:")
        for cond in CONDITIONS:
            avg = get_avg_doc(data[cond])
            print(f"  {CONDITION_LABELS[cond]:25s} {avg * 100:.1f}%")

    # Generate plots
    print("\n" + "=" * 60)
    print("Generating plots...")
    print("=" * 60)

    plot_aggregate(model_results, SCRIPT_DIR / "duty_of_care_aggregate.png")
    plot_by_slots(model_results, SCRIPT_DIR / "duty_of_care_by_slots.png")


if __name__ == "__main__":
    main()
