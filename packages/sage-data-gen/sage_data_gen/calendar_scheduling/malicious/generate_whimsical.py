"""Generate whimsical malicious calendar scheduling tasks.

Usage:
    python -m sage_data_gen.calendar_scheduling.malicious.generate_whimsical \
        --input /tmp/sagegen-cal/small.yaml --attack-type privacy \
        -m gemini-2.5-flash
"""

import asyncio
from pathlib import Path

import yaml
from sage_benchmark.benchmarks.calendar_scheduling.loader import load_tasks
from sage_benchmark.benchmarks.calendar_scheduling.types import CalendarTask

from sage_data_gen.shared.whimsical import build_injection_arg_parser, run_injection

from .whimsical.inject import _TASK_DESCRIPTIONS

ATTACK_TYPES = list(_TASK_DESCRIPTIONS.keys())


def _load(paths):
    return load_tasks(paths).all_tasks


def _inject(task: CalendarTask, attack_type: str, strategy: str) -> list[CalendarTask]:
    task_desc = _TASK_DESCRIPTIONS[attack_type]
    malicious_prompt = f"{task_desc}\n\n### STRATEGY TO USE\n{strategy}\n"
    task_dict = task.model_dump(mode="json")
    task_dict["requestor"]["malicious_prompt"] = malicious_prompt
    task_dict["requestor"]["is_malicious"] = True
    task_dict["requestor"]["malicious_target"] = attack_type
    task_dict["requestor"]["malicious_strategy"] = "whimsical"
    return [CalendarTask(**task_dict)]


def _save(tasks: list[CalendarTask], output_path: Path) -> None:
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
        "Generate whimsical malicious calendar scheduling tasks",
        ATTACK_TYPES,
    )
    args = parser.parse_args()
    task_desc = _TASK_DESCRIPTIONS[args.attack_type]
    asyncio.run(run_injection(args, task_desc, _load, _inject, _save, benchmark_name="calendar"))


if __name__ == "__main__":
    main()
