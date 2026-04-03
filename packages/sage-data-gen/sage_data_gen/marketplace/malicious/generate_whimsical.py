"""Generate whimsical malicious marketplace tasks.

For each input task, produces two variants: one with the buyer as the
malicious agent and one with the seller as the malicious agent.

Usage:
    python -m sage_data_gen.marketplace.malicious.generate_whimsical \
        --input /tmp/sagegen-mkt/small.yaml --attack-type privacy \
        -m gemini-2.5-flash
"""

import asyncio
from pathlib import Path

import yaml
from sage_benchmark.benchmarks.marketplace.loader import load_tasks
from sage_benchmark.benchmarks.marketplace.types import MarketplaceTask

from sage_data_gen.shared.whimsical import build_injection_arg_parser, run_injection

from .whimsical.inject import _TASK_DESCRIPTIONS

ATTACK_TYPES = list(_TASK_DESCRIPTIONS.keys())


def _load(paths):
    return load_tasks(paths).all_tasks


def _inject_both_roles(
    task: MarketplaceTask, attack_type: str, strategy: str
) -> list[MarketplaceTask]:
    """Inject the malicious prompt into each role, returning two variants."""
    task_desc = _TASK_DESCRIPTIONS[attack_type]
    suffix = f"\n\n{task_desc}\n\n### STRATEGY TO USE\n{strategy}\n"
    variants: list[MarketplaceTask] = []
    for role in ("buyer", "seller"):
        task_dict = task.model_dump(mode="json")
        task_dict[role]["instruction_message"] += suffix
        task_dict[role]["is_malicious"] = True
        task_dict[role]["malicious_target"] = attack_type
        task_dict[role]["malicious_strategy"] = "whimsical"
        task_dict["variant"] = role
        variants.append(MarketplaceTask.model_validate(task_dict))
    return variants


def _save(tasks: list[MarketplaceTask], output_path: Path) -> None:
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


def main() -> None:
    parser = build_injection_arg_parser(
        "Generate whimsical malicious marketplace tasks",
        ATTACK_TYPES,
    )
    args = parser.parse_args()
    task_desc = _TASK_DESCRIPTIONS[args.attack_type]
    asyncio.run(
        run_injection(
            args, task_desc, _load, _inject_both_roles, _save, benchmark_name="marketplace"
        )
    )


if __name__ == "__main__":
    main()
