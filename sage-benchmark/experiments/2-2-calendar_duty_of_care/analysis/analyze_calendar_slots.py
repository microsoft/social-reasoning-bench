"""Analyze calendar slot availability for duty of care experiment.

Run from the experiment directory (2-2-calendar_duty_of_care):
    uv run python analysis/analyze_calendar_slots.py
"""

import argparse
from collections import Counter
from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt
import yaml

DEFAULT_DATA_PATH = "../../data/calendar-scheduling/generated/generated-tasks.yaml"
DEFAULT_OUTPUT_PATH = "analysis/slot_distribution.png"


def parse_time(time_str: str) -> datetime:
    """Parse time string to datetime object."""
    time_str = str(time_str).zfill(5)
    return datetime.strptime(time_str, "%H:%M")


def get_meeting_duration_minutes(meeting: dict) -> int:
    """Get meeting duration in minutes."""
    start = parse_time(meeting["start_time"])
    end = parse_time(meeting["end_time"])
    return int((end - start).total_seconds() / 60)


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


def main():
    parser = argparse.ArgumentParser(description="Analyze calendar slot availability")
    parser.add_argument(
        "--data",
        "-d",
        default=DEFAULT_DATA_PATH,
        help=f"Path to tasks YAML file (default: {DEFAULT_DATA_PATH})",
    )
    parser.add_argument(
        "--output",
        "-o",
        default=DEFAULT_OUTPUT_PATH,
        help=f"Output path for plot (default: {DEFAULT_OUTPUT_PATH})",
    )
    args = parser.parse_args()

    with open(args.data) as f:
        data = yaml.safe_load(f)

    tasks = data["tasks"]

    # Analyze each task
    results = []
    for task in tasks:
        satisfiable = task["satisfiable"]
        meeting = task["requestor"]["requested_meeting"]
        calendar = task["assistant"]["calendar"]

        duration = get_meeting_duration_minutes(meeting)
        free_slots = find_free_slots(calendar)
        num_fitting_slots = count_fitting_slots(free_slots, duration)

        results.append(
            {
                "id": task["id"],
                "satisfiable": satisfiable,
                "duration_minutes": duration,
                "num_fitting_slots": num_fitting_slots,
            }
        )

    # Summary statistics
    total_tasks = len(results)
    unsatisfiable = [r for r in results if not r["satisfiable"]]
    satisfiable = [r for r in results if r["satisfiable"]]

    print(f"Total tasks: {total_tasks}")
    print(f"Unsatisfiable tasks: {len(unsatisfiable)}")
    print(f"Satisfiable tasks: {len(satisfiable)}")
    print()

    # Check unsatisfiable tasks
    unsatisfiable_with_slots = [r for r in unsatisfiable if r["num_fitting_slots"] > 0]
    print(f"Unsatisfiable tasks with >0 fitting slots: {len(unsatisfiable_with_slots)}")
    if unsatisfiable_with_slots:
        print("  (These may have slots but other constraints make them unsatisfiable)")
    print()

    # Investigate satisfiable tasks with 0 slots
    satisfiable_zero_slots = [r for r in satisfiable if r["num_fitting_slots"] == 0]
    if satisfiable_zero_slots:
        print(f"Satisfiable tasks with 0 slots: {len(satisfiable_zero_slots)}")
        for r in satisfiable_zero_slots[:3]:
            task = next(t for t in tasks if t["id"] == r["id"])
            print(f"  Task {r['id']}: duration={r['duration_minutes']}min")
            movable = [e for e in task["assistant"]["calendar"] if e.get("is_movable", False)]
            print(f"    Movable events: {len(movable)}")
        print()

    # Statistics for satisfiable tasks
    satisfiable_slots = [r["num_fitting_slots"] for r in satisfiable]
    if satisfiable_slots:
        avg_slots = sum(satisfiable_slots) / len(satisfiable_slots)
        min_slots = min(satisfiable_slots)
        max_slots = max(satisfiable_slots)
        print("Satisfiable tasks - slots available:")
        print(f"  Average: {avg_slots:.2f}")
        print(f"  Min: {min_slots}")
        print(f"  Max: {max_slots}")

        slot_counts = Counter(satisfiable_slots)
        print("\nSlot distribution for satisfiable tasks:")
        for slots in sorted(slot_counts.keys()):
            print(f"  {slots} slots: {slot_counts[slots]} tasks")

    # Create bar chart
    _, ax = plt.subplots(figsize=(10, 3))

    satisfiable_slots = [r["num_fitting_slots"] for r in satisfiable]
    slot_counts = Counter(satisfiable_slots)

    x_values = list(range(min(satisfiable_slots), max(satisfiable_slots) + 1))
    counts = [slot_counts.get(x, 0) for x in x_values]

    bars = ax.bar(x_values, counts, color="#6b6b6b", width=0.7)

    for bar, count in zip(bars, counts):
        if count > 0:
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.4,
                str(count),
                ha="center",
                va="bottom",
                fontsize=10,
            )

    ax.set_xlabel("Number of Available Slots")
    ax.set_ylabel("Number of Tasks")
    ax.set_title("Distribution of Available Calendar Slots (Satisfiable Tasks)")
    ax.set_xticks(x_values)
    ax.set_ylim(0, max(counts) + 3)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.tick_params(left=False)

    plt.tight_layout()

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=150, bbox_inches="tight", facecolor="white")
    print(f"\nPlot saved to: {output_path}")


if __name__ == "__main__":
    main()
