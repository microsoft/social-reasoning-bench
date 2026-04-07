"""Malicious form-filling task generation.

Exports the common API consumed by the ``sagegen malicious`` CLI.
"""

import random
from pathlib import Path

import yaml
from sage_benchmark.benchmarks.form_filling.loader import load_tasks as _load_tasks
from sage_benchmark.benchmarks.form_filling.types import FormTask

from .generate_whimsical import ATTACK_TYPES as WHIMSICAL_ATTACK_TYPES
from .generate_whimsical import _inject as inject_whimsical
from .whimsical.inject import _TASK_DESCRIPTIONS as TASK_DESCRIPTIONS


def load(paths):
    return _load_tasks(paths).all_tasks


def save(tasks: list[FormTask], output_path: Path) -> None:
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
    tasks: list[FormTask],
    attack_type: str,
    limit: int | None,
    rng: random.Random,
) -> list[FormTask]:
    """Sample validation tasks with form-filling-aware prioritisation.

    Attack-type-specific rules:

    * **privacy** — prefer tasks with more secrets (richer leakage surface).
    * **due_diligence** — prefer tasks with ``due_diligence_fields`` and
      ``distractor_scenarios`` so the agent has masked fields to investigate.
    * **duty_of_care** — prefer tasks with ``negative_info`` so the agent
      must decide whether to include harmful information.

    Args:
        tasks: Full list of FormTask objects to sample from.
        attack_type: Attack type key (e.g. ``"privacy"``).
        limit: Maximum number of tasks to return, or *None* for all.
        rng: Seeded random number generator for reproducibility.

    Returns:
        Sampled list of FormTask objects, up to *limit* in length.
    """
    if limit is None or limit >= len(tasks):
        return list(tasks)

    if attack_type == "privacy":
        # Sort by descending number of secrets for richer attack surface.
        scored = sorted(tasks, key=lambda t: len(t.secrets), reverse=True)
    elif attack_type == "due_diligence":
        # Prefer tasks that have due-diligence fields (masked fields with
        # distractors) so the agent's caution can actually be tested.
        scored = sorted(
            tasks,
            key=lambda t: (len(t.due_diligence_fields), len(t.distractor_scenarios)),
            reverse=True,
        )
    elif attack_type == "duty_of_care":
        # Prefer tasks with negative_info so the agent faces advocacy choices.
        scored = sorted(tasks, key=lambda t: len(t.negative_info), reverse=True)
    else:
        scored = list(tasks)

    # Take top-scoring candidates, then randomly sample from them to add
    # variety (pick from the top 2× limit so we don't always get the same set).
    pool_size = min(len(scored), limit * 2)
    pool = scored[:pool_size]
    return rng.sample(pool, min(limit, len(pool)))


__all__ = [
    "WHIMSICAL_ATTACK_TYPES",
    "TASK_DESCRIPTIONS",
    "load",
    "save",
    "inject_whimsical",
    "sample_validation_tasks",
]
