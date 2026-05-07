"""Malicious calendar scheduling task generation.

Exports the common API consumed by the ``srbench datagen malicious`` CLI.
"""

import random
from pathlib import Path

import yaml
from srbench.benchmarks.calendar_scheduling.loader import load_tasks as _load_tasks
from srbench.benchmarks.calendar_scheduling.types import CalendarTask

from srbench_data_gen.shared.sampling import (
    compute_tertile_thresholds,
    quantile_bucket,
    stratified_round_robin_sample,
)

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
    """Sample validation tasks via round-robin across (satisfiable, zopa_tertile) buckets.

    Args:
        tasks: Full list of calendar tasks to sample from.
        attack_type: Unused — sampling is attack-type-agnostic.
        limit: Maximum number of tasks to return, or None for all tasks.
        rng: Seeded random instance for reproducible sampling.

    Returns:
        Shuffled list of sampled tasks with broad feature coverage.
    """
    zopa_values = [t.zopa_width() for t in tasks]
    thresholds = compute_tertile_thresholds(zopa_values)

    def feature_fn(t: CalendarTask) -> tuple:
        return (t.satisfiable, quantile_bucket(t.zopa_width(), thresholds))

    return stratified_round_robin_sample(tasks, feature_fn, limit, rng)


__all__ = [
    "WHIMSICAL_ATTACK_TYPES",
    "TASK_DESCRIPTIONS",
    "load",
    "save",
    "inject_whimsical",
    "sample_validation_tasks",
]
