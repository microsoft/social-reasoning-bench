#!/usr/bin/env python3
"""Remove form-filling tasks that exceed complexity limits.

Filters a form-filling tasks.yaml file by max fields, max secrets, and
min open-ended fields, writing the result to a new file (or in-place
with --in-place).

These limits control evaluation cost: form-filling privacy evaluation
creates (fields × secrets × judge_votes) LLM calls per task, so capping
fields and secrets prevents outlier tasks from dominating eval time.

Uses the same defaults as FormFillingConfig so the script stays in sync
with the datagen rejection-sampling guards.

Usage:
    # Dry-run (print what would be removed):
    python scripts/filter_form_filling_tasks.py data/form-filling/tasks.yaml

    # Write filtered output to a new file:
    python scripts/filter_form_filling_tasks.py data/form-filling/tasks.yaml -o data/form-filling/tasks-filtered.yaml

    # Filter in-place:
    python scripts/filter_form_filling_tasks.py data/form-filling/tasks.yaml --in-place

    # Custom limits:
    python scripts/filter_form_filling_tasks.py data/form-filling/tasks.yaml --max-fields 8 --max-secrets 12 -o out.yaml
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml


def _count_fields(task: dict) -> int:
    """Count ground-truth fields (proxy for form model leaf fields).

    Args:
        task: A task dictionary containing a ``ground_truth`` list.

    Returns:
        The number of ground-truth field entries.
    """
    return len(task.get("ground_truth", []))


def _count_secrets(task: dict) -> int:
    return len(task.get("secrets", []))


def _count_open_ended(task: dict) -> int:
    return sum(1 for g in task.get("ground_truth", []) if g.get("is_open_ended"))


def filter_tasks(
    tasks: list[dict],
    *,
    max_fields: int,
    max_secrets: int,
    min_open_ended: int,
) -> tuple[list[dict], list[dict]]:
    """Split tasks into (kept, removed) based on complexity limits.

    Args:
        tasks: List of task dictionaries to filter.
        max_fields: Maximum number of ground-truth fields allowed.
        max_secrets: Maximum number of secrets allowed.
        min_open_ended: Minimum number of open-ended fields required.

    Returns:
        A tuple of (kept, removed) task lists. Removed tasks have a
        ``_removal_reasons`` key listing why they were filtered out.
    """
    kept, removed = [], []
    for task in tasks:
        n_fields = _count_fields(task)
        n_secrets = _count_secrets(task)
        n_open_ended = _count_open_ended(task)

        reasons = []
        if n_fields > max_fields:
            reasons.append(f"fields={n_fields}>{max_fields}")
        if n_secrets > max_secrets:
            reasons.append(f"secrets={n_secrets}>{max_secrets}")
        if n_open_ended < min_open_ended:
            reasons.append(f"open_ended={n_open_ended}<{min_open_ended}")

        if reasons:
            task["_removal_reasons"] = reasons
            removed.append(task)
        else:
            kept.append(task)

    return kept, removed


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Filter form-filling tasks by complexity limits.",
    )
    parser.add_argument("input", type=Path, help="Path to form-filling tasks.yaml")
    parser.add_argument("-o", "--output", type=Path, help="Output path (default: dry-run)")
    parser.add_argument("--in-place", action="store_true", help="Overwrite input file")
    parser.add_argument("--max-fields", type=int, default=10)
    parser.add_argument("--max-secrets", type=int, default=15)
    parser.add_argument("--min-open-ended", type=int, default=1)
    args = parser.parse_args()

    if args.in_place and args.output:
        parser.error("--in-place and -o/--output are mutually exclusive")

    data = yaml.safe_load(args.input.read_text())
    tasks = data.get("tasks", data if isinstance(data, list) else [])
    print(f"Loaded {len(tasks)} tasks from {args.input}")

    kept, removed = filter_tasks(
        tasks,
        max_fields=args.max_fields,
        max_secrets=args.max_secrets,
        min_open_ended=args.min_open_ended,
    )

    print(
        f"\nLimits: max_fields={args.max_fields}, max_secrets={args.max_secrets}, "
        f"min_open_ended={args.min_open_ended}"
    )
    print(f"Kept:    {len(kept)}")
    print(f"Removed: {len(removed)}")

    if removed:
        print(f"\nRemoved tasks:")
        for task in removed:
            tid = task.get("id", "?")
            reasons = task.pop("_removal_reasons", [])
            n_f = _count_fields(task)
            n_s = _count_secrets(task)
            n_oe = _count_open_ended(task)
            print(
                f"  Task {tid:>6}: fields={n_f}, secrets={n_s}, "
                f"open_ended={n_oe}  ({', '.join(reasons)})"
            )

    output_path = args.input if args.in_place else args.output
    if output_path:
        out_data = {"tasks": kept} if isinstance(data, dict) else kept
        output_path.write_text(
            yaml.dump(out_data, default_flow_style=False, allow_unicode=True, sort_keys=False),
        )
        print(f"\nWrote {len(kept)} tasks to {output_path}")
    else:
        print(f"\nDry-run — no file written. Use -o or --in-place to write.")


if __name__ == "__main__":
    main()
