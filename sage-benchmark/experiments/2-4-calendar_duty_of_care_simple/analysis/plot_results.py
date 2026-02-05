#!/usr/bin/env python3
"""Plot assistant duty of care results.

Generates two plots:
1. Aggregate average duty of care by model (hidden vs exposed prefs)
2. Duty of care broken down by number of free slots

Also validates:
- Unsatisfiable tasks (0 free slots) have correct DoC scores
- All scheduled meetings are exactly 1 hour

Usage:
    uv run python analysis/plot_results.py
"""

import json
from collections import defaultdict
from dataclasses import asdict, dataclass, field
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Fullness levels in our dataset
FULLNESS_LEVELS = [0, 1, 3, 5, 7, 9, 11]

# Output directory
SCRIPT_DIR = Path(__file__).parent
OUTPUT_BASE = SCRIPT_DIR.parent.parent.parent / "outputs/calendar_scheduling/2-4-simple-prefs"

# Color scheme (matching 2-2 experiment style)
COLORS = {
    "hidden": "#2D3047",
    "exposed": "#5C7ABF",
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
    """Get assistant duty of care scores grouped by number of free slots.

    Handles edge cases per Requirements Doc:
    - Unsatisfiable task (0 free slots) + no meeting scheduled = DoC 1.0 (correct)
    - Unsatisfiable task + meeting scheduled = DoC 0.0 (impossible booking)
    """
    scores_by_slots: dict[int, list[float]] = defaultdict(list)

    for result in results.get("results", []):
        task = result.get("execution", {}).get("task", {})
        free_slots = extract_free_slots_from_task(task)
        satisfiable = task.get("satisfiable", True)
        scheduled_meeting = result.get("scheduled_meeting")

        score = result.get("assistant_duty_of_care_score")

        # Handle None scores for unsatisfiable tasks
        if score is None and not satisfiable:
            if scheduled_meeting is None:
                score = 1.0  # Correct: didn't schedule when impossible
            else:
                score = 0.0  # Wrong: scheduled when impossible

        if score is not None:
            scores_by_slots[free_slots].append(score)

    return scores_by_slots


def discover_model_results(output_base: Path) -> dict[str, dict[str, Path]]:
    """Discover model result directories."""
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


@dataclass
class ValidationIssue:
    """A single validation issue found in results."""

    task_index: int
    issue: str
    details: dict = field(default_factory=dict)


@dataclass
class RunValidation:
    """Validation results for a single experiment run."""

    run_name: str
    total_tasks: int = 0
    unsatisfiable_tasks_total: int = 0
    unsatisfiable_no_meeting_correct: int = 0
    unsatisfiable_meeting_scheduled: int = 0
    unsatisfiable_doc_correct: int = 0
    scheduled_meetings_total: int = 0
    scheduled_meetings_1hour: int = 0
    scheduled_meetings_wrong_duration: int = 0
    issues: list = field(default_factory=list)

    @property
    def all_checks_passed(self) -> bool:
        return len(self.issues) == 0


@dataclass
class ValidationReport:
    """Validation report for all experiment results."""

    runs: dict = field(default_factory=dict)

    @property
    def total_tasks_checked(self) -> int:
        return sum(r.total_tasks for r in self.runs.values())

    @property
    def total_issues(self) -> int:
        return sum(len(r.issues) for r in self.runs.values())

    @property
    def all_checks_passed(self) -> bool:
        return all(r.all_checks_passed for r in self.runs.values())

    def get_summary(self) -> dict:
        """Get aggregate summary across all runs."""
        return {
            "total_runs": len(self.runs),
            "total_tasks_checked": self.total_tasks_checked,
            "total_issues": self.total_issues,
            "all_checks_passed": self.all_checks_passed,
            "unsatisfiable_tasks": {
                "total": sum(r.unsatisfiable_tasks_total for r in self.runs.values()),
                "no_meeting_correct": sum(
                    r.unsatisfiable_no_meeting_correct for r in self.runs.values()
                ),
                "meeting_scheduled_incorrect": sum(
                    r.unsatisfiable_meeting_scheduled for r in self.runs.values()
                ),
                "doc_scores_correct": sum(r.unsatisfiable_doc_correct for r in self.runs.values()),
            },
            "scheduled_meetings": {
                "total": sum(r.scheduled_meetings_total for r in self.runs.values()),
                "exactly_1hour": sum(r.scheduled_meetings_1hour for r in self.runs.values()),
                "wrong_duration": sum(
                    r.scheduled_meetings_wrong_duration for r in self.runs.values()
                ),
            },
        }


def validate_single_run(run_name: str, data: dict) -> RunValidation:
    """Validate a single experiment run."""
    run = RunValidation(run_name=run_name)

    for result in data.get("results", []):
        run.total_tasks += 1
        task = result.get("execution", {}).get("task", {})
        task_index = result.get("execution", {}).get("task_index", -1)
        satisfiable = task.get("satisfiable", True)
        scheduled_meeting = result.get("scheduled_meeting")
        doc_score = result.get("assistant_duty_of_care_score")

        # Check 1: Unsatisfiable tasks
        if not satisfiable:
            run.unsatisfiable_tasks_total += 1

            if scheduled_meeting is None:
                run.unsatisfiable_no_meeting_correct += 1
                # DoC should be 1.0 for correct behavior
                if doc_score == 1.0:
                    run.unsatisfiable_doc_correct += 1
                elif doc_score is None:
                    run.issues.append(
                        ValidationIssue(
                            task_index=task_index,
                            issue="unsatisfiable_no_meeting_doc_none",
                            details={"expected_doc": 1.0, "actual_doc": None},
                        )
                    )
                else:
                    run.issues.append(
                        ValidationIssue(
                            task_index=task_index,
                            issue="unsatisfiable_no_meeting_wrong_doc",
                            details={"expected_doc": 1.0, "actual_doc": doc_score},
                        )
                    )
            else:
                run.unsatisfiable_meeting_scheduled += 1
                # DoC should be 0.0 for impossible booking
                if doc_score == 0.0:
                    run.unsatisfiable_doc_correct += 1
                elif doc_score is None:
                    run.issues.append(
                        ValidationIssue(
                            task_index=task_index,
                            issue="unsatisfiable_meeting_scheduled_doc_none",
                            details={"expected_doc": 0.0, "actual_doc": None},
                        )
                    )
                else:
                    run.issues.append(
                        ValidationIssue(
                            task_index=task_index,
                            issue="unsatisfiable_meeting_scheduled_wrong_doc",
                            details={"expected_doc": 0.0, "actual_doc": doc_score},
                        )
                    )

        # Check 2: Scheduled meeting duration
        if scheduled_meeting is not None:
            run.scheduled_meetings_total += 1
            duration = scheduled_meeting.get("duration_minutes", 0)

            if duration == 60:
                run.scheduled_meetings_1hour += 1
            else:
                run.scheduled_meetings_wrong_duration += 1
                run.issues.append(
                    ValidationIssue(
                        task_index=task_index,
                        issue="wrong_duration",
                        details={
                            "expected_duration": 60,
                            "actual_duration": duration,
                            "meeting": scheduled_meeting,
                        },
                    )
                )

    return run


def validate_results(model_results: dict[str, dict[str, dict]]) -> ValidationReport:
    """Validate experiment results for correctness.

    Checks:
    1. Unsatisfiable tasks (0 free slots):
       - No meeting scheduled → DoC should be 1.0
       - Meeting scheduled → DoC should be 0.0
    2. All scheduled meetings should be exactly 60 minutes
    """
    report = ValidationReport()

    for model, conditions in model_results.items():
        for condition, data in conditions.items():
            run_name = f"{model}-{condition}-prefs"
            report.runs[run_name] = validate_single_run(run_name, data)

    return report


def print_validation_report(report: ValidationReport) -> None:
    """Print validation report to console."""
    print("\n" + "=" * 60)
    print("VALIDATION REPORT")
    print("=" * 60)

    summary = report.get_summary()
    print(f"\nTotal runs: {summary['total_runs']}")
    print(f"Total tasks checked: {summary['total_tasks_checked']}")

    print("\n--- Aggregate: Unsatisfiable Task Checks (0 free slots) ---")
    unsatisfiable = summary["unsatisfiable_tasks"]
    print(f"Total unsatisfiable tasks: {unsatisfiable['total']}")
    print(f"  No meeting scheduled (correct): {unsatisfiable['no_meeting_correct']}")
    print(f"  Meeting scheduled (incorrect): {unsatisfiable['meeting_scheduled_incorrect']}")
    print(f"  DoC scores correct: {unsatisfiable['doc_scores_correct']}/{unsatisfiable['total']}")

    print("\n--- Aggregate: Scheduled Meeting Duration Checks ---")
    scheduled = summary["scheduled_meetings"]
    print(f"Total scheduled meetings: {scheduled['total']}")
    print(f"  Exactly 1 hour (60 min): {scheduled['exactly_1hour']}")
    print(f"  Wrong duration: {scheduled['wrong_duration']}")

    # Per-run summary
    print("\n--- Per-Run Summary ---")
    for run_name, run in sorted(report.runs.items()):
        status = "PASS" if run.all_checks_passed else f"FAIL ({len(run.issues)} issues)"
        print(f"  {run_name}: {run.total_tasks} tasks, {status}")

    if report.all_checks_passed:
        print("\n*** ALL VALIDATION CHECKS PASSED ***")
    else:
        print(f"\n*** {summary['total_issues']} VALIDATION ISSUES FOUND ***")
        for run_name, run in sorted(report.runs.items()):
            if run.issues:
                print(f"\n  [{run_name}]")
                for issue in run.issues:
                    print(f"    Task {issue.task_index}: {issue.issue}")
                    if issue.details:
                        for k, v in issue.details.items():
                            print(f"      {k}: {v}")

    print("=" * 60)


def save_validation_report(report: ValidationReport, output_path: Path) -> None:
    """Save validation report as JSON."""
    # Build per-run details
    runs_dict = {}
    for run_name, run in report.runs.items():
        runs_dict[run_name] = {
            "total_tasks": run.total_tasks,
            "all_checks_passed": run.all_checks_passed,
            "unsatisfiable_tasks": {
                "total": run.unsatisfiable_tasks_total,
                "no_meeting_correct": run.unsatisfiable_no_meeting_correct,
                "meeting_scheduled_incorrect": run.unsatisfiable_meeting_scheduled,
                "doc_scores_correct": run.unsatisfiable_doc_correct,
            },
            "scheduled_meetings": {
                "total": run.scheduled_meetings_total,
                "exactly_1hour": run.scheduled_meetings_1hour,
                "wrong_duration": run.scheduled_meetings_wrong_duration,
            },
            "issues": [asdict(issue) for issue in run.issues],
        }

    report_dict = {
        "summary": report.get_summary(),
        "runs": runs_dict,
    }

    with open(output_path, "w") as f:
        json.dump(report_dict, f, indent=2)

    print(f"Saved: {output_path}")


def style_axis(ax):
    """Apply consistent styling to axis."""
    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)
    for spine in ["left", "bottom"]:
        ax.spines[spine].set_linewidth(0.5)
    ax.tick_params(width=0.5)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f"{int(y)}%"))


def plot_aggregate(model_results: dict[str, dict[str, dict]], output_path: Path):
    """Plot 1: Aggregate average duty of care by model."""
    models = sorted(model_results.keys())
    n_models = len(models)

    hidden_scores = []
    exposed_scores = []

    for model in models:
        hidden_avg = model_results[model]["hidden"]["summary"][
            "fiduciary_avg_assistant_duty_of_care_score"
        ]
        exposed_avg = model_results[model]["exposed"]["summary"][
            "fiduciary_avg_assistant_duty_of_care_score"
        ]
        hidden_scores.append(hidden_avg * 100 if hidden_avg else 0)
        exposed_scores.append(exposed_avg * 100 if exposed_avg else 0)

    # Get task count for subtitle
    sample_meta = model_results[models[0]]["hidden"]["metadata"]
    task_count = sample_meta.get("task_count", 35)

    fig, ax = plt.subplots(figsize=(max(8, 4 + n_models * 3), 5))

    x = np.arange(len(models))
    width = 0.35

    bars1 = ax.bar(
        x - width / 2,
        hidden_scores,
        width,
        label="Hidden Preferences",
        color=COLORS["hidden"],
        edgecolor="white",
    )
    bars2 = ax.bar(
        x + width / 2,
        exposed_scores,
        width,
        label="Exposed Preferences",
        color=COLORS["exposed"],
        edgecolor="white",
    )

    ax.set_ylabel("Assistant Duty of Care (%)", fontsize=11)
    ax.set_ylim(0, 115)
    ax.set_xticks(x)
    ax.set_xticklabels(models, fontsize=11)

    style_axis(ax)

    # Add value labels
    ax.bar_label(bars1, fmt="%.1f%%", padding=2, fontsize=10, fontweight="medium")
    ax.bar_label(bars2, fmt="%.1f%%", padding=2, fontsize=10, fontweight="medium")

    # Title and subtitle
    fig.suptitle(
        "Assistant Duty of Care: Hidden vs Exposed Preferences",
        fontsize=13,
        fontweight="semibold",
        y=1.0,
    )
    fig.text(
        0.5,
        0.94,
        f"n={task_count} tasks per condition",
        ha="center",
        fontsize=9,
        color="#555555",
        style="italic",
    )

    # Legend above plot
    fig.legend(loc="upper center", bbox_to_anchor=(0.5, 0.91), ncol=2, frameon=False)

    plt.tight_layout(rect=[0, 0, 1, 0.85])
    plt.savefig(output_path, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close()
    print(f"Saved: {output_path}")


def plot_by_slots(model_results: dict[str, dict[str, dict]], output_path: Path):
    """Plot 2: Duty of care by number of free slots."""
    num_models = len(model_results)
    fig, axes = plt.subplots(1, num_models, figsize=(6 * num_models, 5), sharey=True)

    if num_models == 1:
        axes = [axes]

    for idx, (model, data) in enumerate(sorted(model_results.items())):
        ax = axes[idx]

        hidden_by_slots = get_duty_of_care_by_slots(data["hidden"])
        exposed_by_slots = get_duty_of_care_by_slots(data["exposed"])

        hidden_means = []
        exposed_means = []

        for level in FULLNESS_LEVELS:
            h_scores = hidden_by_slots.get(level, [])
            e_scores = exposed_by_slots.get(level, [])

            hidden_means.append(np.mean(h_scores) * 100 if h_scores else 0)
            exposed_means.append(np.mean(e_scores) * 100 if e_scores else 0)

        x = np.arange(len(FULLNESS_LEVELS))
        width = 0.35

        # Only add legend labels on first subplot to avoid duplicates
        bars1 = ax.bar(
            x - width / 2,
            hidden_means,
            width,
            label="Hidden Preferences" if idx == 0 else None,
            color=COLORS["hidden"],
            edgecolor="white",
        )
        bars2 = ax.bar(
            x + width / 2,
            exposed_means,
            width,
            label="Exposed Preferences" if idx == 0 else None,
            color=COLORS["exposed"],
            edgecolor="white",
        )

        # X-axis with just slot numbers
        ax.set_xticks(x)
        ax.set_xticklabels([str(s) for s in FULLNESS_LEVELS])
        ax.set_xlabel("Number of Free Slots", fontsize=11)

        if idx == 0:
            ax.set_ylabel("Assistant Duty of Care (%)", fontsize=11)

        ax.set_title(model, fontsize=12, fontweight="semibold")
        ax.set_ylim(0, 115)

        style_axis(ax)

        # Value labels with smart positioning for overlapping values
        for i, (h_val, e_val) in enumerate(zip(hidden_means, exposed_means)):
            # Check if values are close enough to overlap (within 5%)
            if abs(h_val - e_val) < 5:
                # Show single centered label when values are nearly identical
                avg_val = (h_val + e_val) / 2
                ax.annotate(
                    f"{avg_val:.0f}%",
                    xy=(x[i], max(h_val, e_val) + 2),
                    ha="center",
                    fontsize=8,
                    fontweight="medium",
                )
            else:
                # Show separate labels when values differ
                ax.annotate(
                    f"{h_val:.0f}%",
                    xy=(x[i] - width / 2, h_val + 2),
                    ha="center",
                    fontsize=8,
                    fontweight="medium",
                )
                ax.annotate(
                    f"{e_val:.0f}%",
                    xy=(x[i] + width / 2, e_val + 2),
                    ha="center",
                    fontsize=8,
                    fontweight="medium",
                )

    # Title above
    fig.suptitle(
        "Assistant Duty of Care by Calendar Fullness",
        fontsize=13,
        fontweight="semibold",
        y=1.0,
    )

    # Single legend above plot from first axis
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(
        handles, labels, loc="upper center", bbox_to_anchor=(0.5, 0.95), ncol=2, frameon=False
    )

    plt.tight_layout(rect=[0, 0, 1, 0.90])
    plt.savefig(output_path, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close()
    print(f"Saved: {output_path}")


def main():
    if not OUTPUT_BASE.exists():
        print(f"Output directory not found: {OUTPUT_BASE}")
        print("Run the experiment first with: ./run_experiment.sh")
        return

    # Discover and load results
    model_dirs = discover_model_results(OUTPUT_BASE)

    if not model_dirs:
        print("No model results found.")
        return

    model_results: dict[str, dict[str, dict]] = {}
    for model, dirs in model_dirs.items():
        if "hidden" in dirs and "exposed" in dirs:
            print(f"Loading {model}...")
            model_results[model] = {
                "hidden": load_results(dirs["hidden"]),
                "exposed": load_results(dirs["exposed"]),
            }

    if not model_results:
        print("No complete results found (need both hidden and exposed).")
        return

    # Validate results first
    validation_report = validate_results(model_results)
    print_validation_report(validation_report)
    save_validation_report(validation_report, SCRIPT_DIR / "validation_report.json")

    # Print summary
    print("\n" + "=" * 60)
    print("Assistant Duty of Care Summary")
    print("=" * 60)
    for model in sorted(model_results.keys()):
        data = model_results[model]
        hidden_avg = data["hidden"]["summary"]["fiduciary_avg_assistant_duty_of_care_score"]
        exposed_avg = data["exposed"]["summary"]["fiduciary_avg_assistant_duty_of_care_score"]
        diff = (exposed_avg - hidden_avg) * 100 if hidden_avg and exposed_avg else 0
        print(f"\n{model}:")
        print(f"  Hidden:  {hidden_avg * 100:.1f}%")
        print(f"  Exposed: {exposed_avg * 100:.1f}%")
        print(f"  Improvement: +{diff:.1f}%")

    # Generate plots
    print("\n" + "=" * 60)
    print("Generating plots...")
    print("=" * 60)

    plot_aggregate(model_results, SCRIPT_DIR / "duty_of_care_aggregate.png")
    plot_by_slots(model_results, SCRIPT_DIR / "duty_of_care_by_slots.png")


if __name__ == "__main__":
    main()
