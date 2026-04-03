"""Generate hand-crafted malicious form-filling tasks.

Usage:
    python -m sage_data_gen.form_filling.malicious.generate_hand_crafted \
        --input data/form-filling/small.yaml --attack-type privacy
"""

from sage_benchmark.benchmarks.form_filling.loader import load_tasks
from sage_benchmark.benchmarks.form_filling.types import FormTask

from sage_data_gen.shared.hand_crafted import (
    build_arg_parser,
    inject_and_save,
    resolve_output_path,
)

from .hand_crafted import get_hand_crafted_prompt

ATTACK_TYPES = ["privacy", "duty_of_care", "due_diligence"]


def _load(paths):
    return load_tasks(paths).all_tasks


def _inject(task: FormTask, attack_type: str) -> list[FormTask]:
    prompt = get_hand_crafted_prompt(attack_type)
    task_dict = task.model_dump()
    task_dict["instruction_message"] = prompt
    task_dict["is_malicious"] = True
    task_dict["malicious_target"] = attack_type
    task_dict["malicious_strategy"] = "hand_crafted"
    return [FormTask.model_validate(task_dict)]


def main() -> None:
    parser = build_arg_parser(
        "Generate hand-crafted malicious form-filling tasks",
        ATTACK_TYPES,
    )
    args = parser.parse_args()
    inject_and_save(args.input, resolve_output_path(args), _load, _inject, args.attack_type)


if __name__ == "__main__":
    main()
