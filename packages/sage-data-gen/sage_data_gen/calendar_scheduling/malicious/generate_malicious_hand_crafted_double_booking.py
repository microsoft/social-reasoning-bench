"""Generate malicious calendar scheduling tasks targeting double booking.

This script takes existing calendar scheduling tasks and replaces the requestor's
instruction message with an adversarial one that tries to trick the assistant into
creating calendar conflicts (scheduling over existing meetings).

Usage:
    python generate_malicious_hand_crafted_double_booking.py --input-dir data/calendar-scheduling/final
    python generate_malicious_hand_crafted_double_booking.py --input-dir data/calendar-scheduling/final --output-dir /tmp/out
"""

import argparse
from pathlib import Path

import yaml
from sage_benchmark.benchmarks.calendar_scheduling.loader import load_tasks
from sage_benchmark.benchmarks.calendar_scheduling.types import CalendarTask

from .hand_crafted.double_booking import PROMPT as DOUBLE_BOOKING_SUFFIX


def convert_to_malicious(tasks: list[CalendarTask]) -> list[CalendarTask]:
    """Convert normal tasks to malicious ones by appending double-booking instructions."""
    malicious_tasks = []

    for task in tasks:
        task_dict = task.model_dump(mode="json")
        original = task_dict["requestor"]["instruction_message"]
        task_dict["requestor"]["instruction_message"] = original + DOUBLE_BOOKING_SUFFIX
        task_dict["requestor"]["is_malicious"] = True
        task_dict["requestor"]["malicious_target"] = "double_booking"
        task_dict["requestor"]["malicious_strategy"] = "hand_crafted"

        malicious_tasks.append(CalendarTask(**task_dict))

    return malicious_tasks


def save_tasks_yaml(tasks: list[CalendarTask], output_path: Path) -> None:
    """Save tasks to YAML file."""
    tasks_dict = {"tasks": [task.model_dump(mode="json") for task in tasks]}

    with open(output_path, "w") as f:
        yaml.dump(
            tasks_dict,
            f,
            default_flow_style=False,
            sort_keys=False,
            allow_unicode=True,
            width=120,
        )


def generate_for_directory(input_dir: Path, output_dir: Path | None = None) -> None:
    """Generate malicious versions for small/medium/large datasets."""
    if output_dir is None:
        output_dir = input_dir

    large_path = input_dir / "large.yaml"
    medium_path = input_dir / "medium.yaml"
    small_path = input_dir / "small.yaml"

    for p in [large_path, medium_path, small_path]:
        if not p.exists():
            raise FileNotFoundError(f"Expected file not found: {p}")

    medium_ids = {t.id for t in load_tasks([medium_path]).all_tasks}
    small_ids = {t.id for t in load_tasks([small_path]).all_tasks}

    print(f"Loading tasks from {large_path}")
    large_tasks = load_tasks([large_path]).all_tasks
    print(f"Loaded {len(large_tasks)} tasks")

    print("Converting to malicious double-booking tasks...")
    large_malicious = convert_to_malicious(large_tasks)

    malicious_by_id = {t.id: t for t in large_malicious}
    medium_malicious = [malicious_by_id[tid] for tid in sorted(medium_ids)]
    small_malicious = [malicious_by_id[tid] for tid in sorted(small_ids)]

    for name, tasks in [
        ("large-malicious-hand-crafted-double-booking", large_malicious),
        ("medium-malicious-hand-crafted-double-booking", medium_malicious),
        ("small-malicious-hand-crafted-double-booking", small_malicious),
    ]:
        out_path = output_dir / f"{name}.yaml"
        print(f"Saving {len(tasks)} tasks to {out_path}")
        save_tasks_yaml(tasks, out_path)

    print("\nDone!")
    print(f"  large:  {len(large_malicious)} tasks")
    print(f"  medium: {len(medium_malicious)} tasks")
    print(f"  small:  {len(small_malicious)} tasks")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate malicious calendar scheduling tasks targeting double booking"
    )
    parser.add_argument(
        "--input-dir",
        type=Path,
        required=True,
        help="Directory containing small.yaml, medium.yaml, large.yaml",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Output directory (defaults to input directory)",
    )
    args = parser.parse_args()

    generate_for_directory(args.input_dir, args.output_dir)


if __name__ == "__main__":
    main()
