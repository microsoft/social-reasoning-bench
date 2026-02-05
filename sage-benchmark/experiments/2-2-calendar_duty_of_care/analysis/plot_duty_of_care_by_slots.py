#!/usr/bin/env python3
"""Plot assistant duty of care by number of available calendar slots.

Compares hidden vs exposed preferences for gpt-4.1 model.

Usage:
    uv run analysis/plot_duty_of_care_by_slots.py

Output saved to analysis/duty_of_care_by_slots.png
"""

import json
from collections import defaultdict
from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

RESULTS_DIR = (
    Path(__file__).parent.parent.parent.parent
    / "outputs/calendar_scheduling/2-2-calendar_duty_of_care"
)
OUTPUT_PATH = Path(__file__).parent / "duty_of_care_by_slots.png"

MODEL = "gpt-4.1"


def parse_time(time_str: str) -> datetime:
    """Parse time string to datetime object."""
    time_str = str(time_str).zfill(5)
    return datetime.strptime(time_str, "%H:%M")


def get_meeting_duration_minutes(meeting: dict) -> int:
    """Get meeting duration in minutes."""
    return meeting.get("duration_minutes", 60)


def find_free_slots(
    calendar: list, day_start: str = "00:00", day_end: str = "23:59"
) -> list[tuple[datetime, datetime]]:
    """Find all free slots in a calendar for a given day."""
    if not calendar:
        return [(parse_time(day_start), parse_time(day_end))]

    events = sorted(calendar, key=lambda e: parse_time(e["start_time"]))
    free_slots = []
    current_time = parse_time(day_start)

    for event in events:
        event_start = parse_time(event["start_time"])
        event_end = parse_time(event["end_time"])

        if event_start > current_time:
            free_slots.append((current_time, event_start))
        if event_end > current_time:
            current_time = event_end

    day_end_time = parse_time(day_end)
    if current_time < day_end_time:
        free_slots.append((current_time, day_end_time))

    return free_slots


def count_fitting_slots(free_slots: list[tuple[datetime, datetime]], duration_minutes: int) -> int:
    """Count how many slots of given duration fit in the free time."""
    total_slots = 0
    for start, end in free_slots:
        slot_minutes = int((end - start).total_seconds() / 60)
        total_slots += slot_minutes // duration_minutes
    return total_slots


def load_results_with_slots(base_dir: Path, model: str) -> dict:
    """Load experiment results for a specific model, computing slots for each task."""
    results = {"hidden": [], "exposed": []}

    for json_file in base_dir.glob("*.json"):
        with open(json_file) as f:
            data = json.load(f)

        meta = data["metadata"]
        file_model = meta.get("assistant_model", "unknown").split("/")[-1]

        if file_model != model:
            continue

        exposed = meta.get("expose_preferences", False)
        condition = "exposed" if exposed else "hidden"

        for result in data["results"]:
            task = result["execution"]["task"]

            # Calculate available slots
            meeting = task["requestor"]["requested_meeting"]
            calendar = task["assistant"]["calendar"]
            duration = get_meeting_duration_minutes(meeting)
            free_slots = find_free_slots(calendar)
            num_slots = count_fitting_slots(free_slots, duration)

            # Get duty of care score
            duty_of_care = result.get("assistant_duty_of_care_score")

            if duty_of_care is not None:
                results[condition].append(
                    {
                        "task_id": task["id"],
                        "num_slots": num_slots,
                        "duty_of_care": duty_of_care,
                        "satisfiable": task.get("satisfiable", True),
                    }
                )

        print(
            f"Loaded {json_file.name}: {file_model}, exposed={exposed}, {len(results[condition])} tasks"
        )

    return results


def aggregate_by_slots(results: list[dict]) -> dict:
    """Aggregate duty of care scores by number of slots."""
    by_slots = defaultdict(list)

    for r in results:
        by_slots[r["num_slots"]].append(r["duty_of_care"])

    return {
        slots: {
            "mean": np.mean(scores) * 100,
            "std": np.std(scores) * 100,
            "count": len(scores),
        }
        for slots, scores in by_slots.items()
    }


def plot_results(hidden_by_slots: dict, exposed_by_slots: dict, output_path: Path):
    """Create grouped bar plot comparing duty of care by slot count."""
    # Get all slot values present in either dataset
    all_slots = sorted(set(hidden_by_slots.keys()) | set(exposed_by_slots.keys()))

    fig, ax = plt.subplots(figsize=(12, 5))

    x = np.arange(len(all_slots))
    width = 0.35

    hidden_means = [hidden_by_slots.get(s, {}).get("mean", 0) for s in all_slots]
    exposed_means = [exposed_by_slots.get(s, {}).get("mean", 0) for s in all_slots]
    hidden_counts = [hidden_by_slots.get(s, {}).get("count", 0) for s in all_slots]
    exposed_counts = [exposed_by_slots.get(s, {}).get("count", 0) for s in all_slots]

    colors = {
        "hidden": "#2D3047",
        "exposed": "#5C7ABF",
    }

    bars1 = ax.bar(
        x - width / 2,
        hidden_means,
        width,
        label="Hidden Preferences",
        color=colors["hidden"],
        edgecolor="white",
    )
    bars2 = ax.bar(
        x + width / 2,
        exposed_means,
        width,
        label="Exposed Preferences",
        color=colors["exposed"],
        edgecolor="white",
    )

    ax.set_ylabel("Assistant Duty of Care Score (%)", fontsize=11)
    ax.set_xlabel("Number of Available Calendar Slots", fontsize=11)
    ax.set_ylim(0, 115)
    ax.set_xticks(x)
    ax.set_xticklabels(all_slots)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f"{int(y)}%"))

    # Add value labels on bars
    for bars in [bars1, bars2]:
        ax.bar_label(bars, fmt="%.0f%%", padding=2, fontsize=8, fontweight="medium")

    # Add count annotations as secondary x-axis labels
    ax.set_xticks(x)
    ax.set_xticklabels([f"{s}\n(n={hidden_counts[i]})" for i, s in enumerate(all_slots)])

    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)
    for spine in ["left", "bottom"]:
        ax.spines[spine].set_linewidth(0.5)
    ax.tick_params(width=0.5)

    # Title, subtitle, and legend below subtitle
    fig.suptitle(
        f"Assistant Duty of Care by Calendar Availability ({MODEL})",
        fontsize=13,
        fontweight="semibold",
        y=1,
    )

    fig.legend(loc="upper center", bbox_to_anchor=(0.5, 0.95), ncol=2, frameon=False)

    plt.tight_layout(rect=[0, 0, 1, 1])
    plt.savefig(output_path, dpi=150, bbox_inches="tight", facecolor="white")
    print(f"Saved plot to {output_path}")


def main():
    if not RESULTS_DIR.exists():
        print(f"Error: Results directory {RESULTS_DIR} does not exist")
        return

    print(f"Loading results from: {RESULTS_DIR}")
    results = load_results_with_slots(RESULTS_DIR, MODEL)

    if not results["hidden"] and not results["exposed"]:
        print(f"Error: No results found for model {MODEL}")
        return

    print(f"\nLoaded {len(results['hidden'])} hidden, {len(results['exposed'])} exposed tasks")

    hidden_by_slots = aggregate_by_slots(results["hidden"])
    exposed_by_slots = aggregate_by_slots(results["exposed"])

    print("\nHidden preferences by slots:")
    for slots in sorted(hidden_by_slots.keys()):
        data = hidden_by_slots[slots]
        print(f"  {slots} slots: {data['mean']:.1f}% (n={data['count']})")

    print("\nExposed preferences by slots:")
    for slots in sorted(exposed_by_slots.keys()):
        data = exposed_by_slots[slots]
        print(f"  {slots} slots: {data['mean']:.1f}% (n={data['count']})")

    plot_results(hidden_by_slots, exposed_by_slots, OUTPUT_PATH)


if __name__ == "__main__":
    main()
