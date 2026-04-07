"""Malicious calendar scheduling task generation.

Exports the common API consumed by the ``sagegen malicious`` CLI.
"""

import random
from pathlib import Path

import yaml
from sage_benchmark.benchmarks.calendar_scheduling.loader import load_tasks as _load_tasks
from sage_benchmark.benchmarks.calendar_scheduling.types import CalendarTask

from .generate_whimsical import ATTACK_TYPES as WHIMSICAL_ATTACK_TYPES
from .generate_whimsical import _inject as inject_whimsical
from .whimsical.inject import _TASK_DESCRIPTIONS as TASK_DESCRIPTIONS


def load(paths):
    return _load_tasks(paths).all_tasks


def save(tasks: list[CalendarTask], output_path: Path) -> None:
    tasks_dict = {"tasks": [t.model_dump(mode="json") for t in tasks]}
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        yaml.dump(
            tasks_dict,
            f,
            default_flow_style=False,
            sort_keys=False,
            allow_unicode=True,
            width=120,
        )


def sample_validation_tasks(
    tasks: list[CalendarTask],
    attack_type: str,
    limit: int | None,
    rng: random.Random,
) -> list[CalendarTask]:
    """Sample validation tasks with calendar-aware stratification.

    Ensures the sample contains a mix of satisfiable and unsatisfiable tasks,
    stratified by ``free_slots_count`` buckets.  Attack-type-specific rules:

    * **due_diligence / duty_of_care** — at least 2/3 of the sample should be
      satisfiable so the agent has scheduling options to explore or protect.
    * **privacy** — balanced mix; leakage can happen regardless of satisfiability.

    Args:
        tasks: Full list of calendar tasks to sample from.
        attack_type: Attack category (e.g. 'due_diligence', 'privacy') controlling
            the satisfiable/unsatisfiable ratio.
        limit: Maximum number of tasks to return, or None for all tasks.
        rng: Seeded random instance for reproducible sampling.

    Returns:
        Shuffled list of sampled tasks, stratified by satisfiability and fullness.
    """
    if limit is None or limit >= len(tasks):
        return list(tasks)

    satisfiable = [t for t in tasks if t.satisfiable]
    unsatisfiable = [t for t in tasks if not t.satisfiable]

    if attack_type in ("due_diligence", "duty_of_care"):
        # Favour satisfiable tasks so strategies have room to exploit.
        n_sat = max(1, (limit * 2 + 2) // 3)  # ceil(2/3 * limit)
        n_unsat = limit - n_sat
    else:
        # Privacy: balanced split.
        n_sat = max(1, limit // 2)
        n_unsat = limit - n_sat

    # Clamp to available counts and redistribute overflow.
    n_sat = min(n_sat, len(satisfiable))
    n_unsat = min(n_unsat, len(unsatisfiable))
    remaining = limit - n_sat - n_unsat
    if remaining > 0 and len(satisfiable) > n_sat:
        extra = min(remaining, len(satisfiable) - n_sat)
        n_sat += extra
        remaining -= extra
    if remaining > 0 and len(unsatisfiable) > n_unsat:
        n_unsat += min(remaining, len(unsatisfiable) - n_unsat)

    # Stratified pick within each group by free_slots_count buckets.
    picked_sat = _stratified_pick(satisfiable, n_sat, rng)
    picked_unsat = _stratified_pick(unsatisfiable, n_unsat, rng)

    result = picked_sat + picked_unsat
    rng.shuffle(result)
    return result


def _stratified_pick(
    tasks: list[CalendarTask],
    n: int,
    rng: random.Random,
) -> list[CalendarTask]:
    """Pick *n* tasks spread across ``free_slots_count`` buckets.

    Args:
        tasks: Pool of calendar tasks to pick from.
        n: Number of tasks to select.
        rng: Seeded random instance for shuffling within buckets.

    Returns:
        List of up to *n* tasks distributed across free_slots_count buckets
        via round-robin.
    """
    if n <= 0 or not tasks:
        return []
    if n >= len(tasks):
        return list(tasks)

    # Group by free_slots_count.
    buckets: dict[int | None, list[CalendarTask]] = {}
    for t in tasks:
        buckets.setdefault(t.free_slots_count, []).append(t)

    # Round-robin one from each bucket until we reach n.
    picked: list[CalendarTask] = []
    bucket_keys = sorted(buckets.keys(), key=lambda k: (k is None, k))
    # Shuffle within each bucket for randomness.
    for k in bucket_keys:
        rng.shuffle(buckets[k])
    idx = {k: 0 for k in bucket_keys}

    while len(picked) < n:
        added_this_round = False
        for k in bucket_keys:
            if len(picked) >= n:
                break
            if idx[k] < len(buckets[k]):
                picked.append(buckets[k][idx[k]])
                idx[k] += 1
                added_this_round = True
        if not added_this_round:
            break

    return picked


__all__ = [
    "WHIMSICAL_ATTACK_TYPES",
    "TASK_DESCRIPTIONS",
    "load",
    "save",
    "inject_whimsical",
    "sample_validation_tasks",
]
