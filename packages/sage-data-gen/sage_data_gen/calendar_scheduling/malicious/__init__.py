"""Malicious calendar scheduling task generation.

Exports the common API consumed by the ``sagegen malicious`` CLI.
"""

from pathlib import Path

import yaml
from sage_benchmark.benchmarks.calendar_scheduling.loader import load_tasks as _load_tasks
from sage_benchmark.benchmarks.calendar_scheduling.types import CalendarTask

from .generate_hand_crafted import ATTACK_TYPES as HANDCRAFTED_ATTACK_TYPES
from .generate_hand_crafted import _inject as inject_handcrafted
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


__all__ = [
    "HANDCRAFTED_ATTACK_TYPES",
    "WHIMSICAL_ATTACK_TYPES",
    "TASK_DESCRIPTIONS",
    "load",
    "save",
    "inject_handcrafted",
    "inject_whimsical",
]
