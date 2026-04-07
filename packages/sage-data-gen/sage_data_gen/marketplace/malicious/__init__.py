"""Malicious marketplace task generation.

Exports the common API consumed by the ``sagegen malicious`` CLI.
"""

import random
from pathlib import Path

import yaml
from sage_benchmark.benchmarks.marketplace.loader import load_tasks as _load_tasks
from sage_benchmark.benchmarks.marketplace.types import MarketplaceTask

from .generate_whimsical import ATTACK_TYPES as WHIMSICAL_ATTACK_TYPES
from .generate_whimsical import _inject as inject_whimsical
from .whimsical.inject import _TASK_DESCRIPTIONS as TASK_DESCRIPTIONS


def load(paths):
    return _load_tasks(paths).all_tasks


def save(tasks: list[MarketplaceTask], output_path: Path) -> None:
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
    tasks: list[MarketplaceTask],
    attack_type: str,
    limit: int | None,
    rng: random.Random,
) -> list[MarketplaceTask]:
    """Sample validation tasks with marketplace-aware stratification.

    Attack-type-specific rules:

    * **due_diligence** — favour satisfiable tasks (positive deal zone) so
      the agent has negotiation room to explore or cut short.
    * **duty_of_care** — mix of satisfiable/unsatisfiable; include tasks
      with narrow deal zones where the agent must work harder to protect
      the buyer's surplus.
    * **privacy** — balanced; leakage can happen regardless of deal zone.

    Args:
        tasks: Full list of MarketplaceTask objects to sample from.
        attack_type: Attack type key (e.g. ``"due_diligence"``).
        limit: Maximum number of tasks to return, or *None* for all.
        rng: Seeded random number generator for reproducibility.

    Returns:
        Sampled list of MarketplaceTask objects, up to *limit* in length.
    """
    if limit is None or limit >= len(tasks):
        return list(tasks)

    satisfiable = [t for t in tasks if t.satisfiable]
    unsatisfiable = [t for t in tasks if not t.satisfiable]

    if attack_type == "due_diligence":
        # Need negotiations that actually happen.
        n_sat = max(1, (limit * 2 + 2) // 3)
        n_unsat = limit - n_sat
    elif attack_type == "duty_of_care":
        # Mix; include tight deals where buyer surplus is low.
        n_sat = max(1, limit // 2)
        n_unsat = limit - n_sat
        # Within satisfiable, prefer narrow deal zones (harder to protect).
        satisfiable.sort(key=lambda t: t.buyer.reservation_price - t.seller.reservation_price)
    else:
        n_sat = max(1, limit // 2)
        n_unsat = limit - n_sat

    n_sat = min(n_sat, len(satisfiable))
    n_unsat = min(n_unsat, len(unsatisfiable))
    remaining = limit - n_sat - n_unsat
    if remaining > 0 and len(satisfiable) > n_sat:
        extra = min(remaining, len(satisfiable) - n_sat)
        n_sat += extra
        remaining -= extra
    if remaining > 0 and len(unsatisfiable) > n_unsat:
        n_unsat += min(remaining, len(unsatisfiable) - n_unsat)

    picked_sat = rng.sample(satisfiable, n_sat) if n_sat else []
    picked_unsat = rng.sample(unsatisfiable, n_unsat) if n_unsat else []

    result = picked_sat + picked_unsat
    rng.shuffle(result)
    return result


__all__ = [
    "WHIMSICAL_ATTACK_TYPES",
    "TASK_DESCRIPTIONS",
    "load",
    "save",
    "inject_whimsical",
    "sample_validation_tasks",
]
