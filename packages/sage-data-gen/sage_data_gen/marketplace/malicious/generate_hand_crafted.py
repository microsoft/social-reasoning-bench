"""Generate hand-crafted malicious marketplace tasks.

For each input task, produces two variants: one with the buyer as the
malicious agent and one with the seller as the malicious agent.

Usage:
    python -m sage_data_gen.marketplace.malicious.generate_hand_crafted \
        --input /tmp/sagegen-mkt/small.yaml --attack-type privacy
"""

from pathlib import Path

import yaml
from sage_benchmark.benchmarks.marketplace.loader import load_tasks
from sage_benchmark.benchmarks.marketplace.types import MarketplaceTask

from sage_data_gen.shared.hand_crafted import (
    build_arg_parser,
    resolve_output_path,
)

from .hand_crafted import get_hand_crafted_prompt

ATTACK_TYPES = ["privacy", "duty_of_care", "due_diligence"]


def _load(paths):
    return load_tasks(paths).all_tasks


def _inject_both_roles(task: MarketplaceTask, attack_type: str) -> list[MarketplaceTask]:
    """Inject the malicious prompt into each role, returning two variants."""
    suffix = get_hand_crafted_prompt(attack_type)
    variants: list[MarketplaceTask] = []
    for role in ("buyer", "seller"):
        task_dict = task.model_dump(mode="json")
        task_dict[role]["instruction_message"] += suffix
        task_dict[role]["is_malicious"] = True
        task_dict[role]["malicious_target"] = attack_type
        task_dict[role]["malicious_strategy"] = "hand_crafted"
        task_dict["variant"] = role
        variants.append(MarketplaceTask.model_validate(task_dict))
    return variants


def main() -> None:
    parser = build_arg_parser(
        "Generate hand-crafted malicious marketplace tasks",
        ATTACK_TYPES,
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = resolve_output_path(args)

    print(f"Loading tasks from {input_path}")
    tasks = _load([input_path])
    print(f"Loaded {len(tasks)} tasks")

    print(f"Applying hand-crafted {args.attack_type} attack (both roles)...")
    malicious: list[MarketplaceTask] = []
    for task in tasks:
        malicious.extend(_inject_both_roles(task, args.attack_type))

    print(f"Saving {len(malicious)} tasks to {output_path}")
    tasks_dict = {"tasks": [t.model_dump(mode="json") for t in malicious]}
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
    print("Done!")


if __name__ == "__main__":
    main()
