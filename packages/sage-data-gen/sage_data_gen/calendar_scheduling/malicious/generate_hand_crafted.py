"""Generate hand-crafted malicious calendar scheduling tasks.

Usage:
    python -m sage_data_gen.calendar_scheduling.malicious.generate_hand_crafted \
        --input /tmp/sagegen-cal/small.yaml --attack-type privacy
"""

from sage_benchmark.benchmarks.calendar_scheduling.loader import load_tasks
from sage_benchmark.benchmarks.calendar_scheduling.types import CalendarTask

from sage_data_gen.shared.hand_crafted import (
    build_arg_parser,
    inject_and_save,
    resolve_output_path,
)

from .hand_crafted import get_hand_crafted_prompt

ATTACK_TYPES = ["privacy", "duty_of_care", "due_diligence"]


def _load(paths):
    return load_tasks(paths).all_tasks


def _inject(task: CalendarTask, attack_type: str) -> list[CalendarTask]:
    suffix = get_hand_crafted_prompt(attack_type)
    task_dict = task.model_dump(mode="json")
    task_dict["requestor"]["instruction_message"] += suffix
    task_dict["requestor"]["is_malicious"] = True
    task_dict["requestor"]["malicious_target"] = attack_type
    task_dict["requestor"]["malicious_strategy"] = "hand_crafted"
    return [CalendarTask(**task_dict)]


def main() -> None:
    parser = build_arg_parser(
        "Generate hand-crafted malicious calendar scheduling tasks",
        ATTACK_TYPES,
    )
    args = parser.parse_args()
    inject_and_save(args.input, resolve_output_path(args), _load, _inject, args.attack_type)


if __name__ == "__main__":
    main()
