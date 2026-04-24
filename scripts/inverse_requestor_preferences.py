"""Set requestor preferences = 1 - assistant preferences in calendar task YAML files.

Usage:
    python scripts/fix_requestor_preferences.py data/calendar-scheduling/*.yaml
"""

import sys
from pathlib import Path

import yaml

from sage_benchmark.benchmarks.calendar_scheduling.types import CalendarTask, TimeSlotPreference


def fix_requestor_preferences(path: Path) -> int:
    """Rewrite requestor preferences in-place. Returns number of tasks modified."""
    with open(path) as f:
        data = yaml.safe_load(f)

    tasks = [CalendarTask.model_validate(d) for d in data["tasks"]]

    for task in tasks:
        task.requestor.preferences = [
            TimeSlotPreference(
                start_time=p.start_time,
                end_time=p.end_time,
                score=round(1.0 - p.score, 1),
            )
            for p in task.assistant.preferences
        ]

    data["tasks"] = [task.model_dump(mode="json") for task in tasks]
    with open(path, "w") as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

    return len(tasks)


def main() -> None:
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <yaml_file> [yaml_file ...]", file=sys.stderr)
        sys.exit(1)

    for arg in sys.argv[1:]:
        path = Path(arg)
        n = fix_requestor_preferences(path)
        print(f"{path}: updated {n} tasks")


if __name__ == "__main__":
    main()
