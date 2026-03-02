"""Apply the label patch to all experiment YAML files in calendar-scheduling/final.

Reads label_patch.json and updates is_secret values in-place for matching
task_id + calendar uid pairs across all YAML files.
"""

import json
from pathlib import Path

import yaml

PATCH_PATH = Path(__file__).parent / "label_patch.json"
DATASET_DIR = Path(__file__).parent.parent / "data" / "calendar-scheduling" / "final"


def load_patch() -> dict[int, dict[str, bool]]:
    with open(PATCH_PATH) as f:
        raw = json.load(f)

    patch = {}
    for entry in raw:
        tid = entry["task_id"]
        patch.setdefault(tid, {})[entry["uid"]] = entry["new_value"]
    return patch


def apply_patch_to_file(fpath: Path, patch: dict[int, dict[str, bool]]) -> int:
    with open(fpath) as f:
        data = yaml.safe_load(f)

    updates = 0
    for task in data["tasks"]:
        tid = task["id"]
        if tid not in patch:
            continue
        uid_map = patch[tid]
        for event in task["assistant"]["calendar"]:
            if event["uid"] in uid_map:
                old = event["is_secret"]
                new = uid_map[event["uid"]]
                if old != new:
                    event["is_secret"] = new
                    updates += 1

    if updates > 0:
        with open(fpath, "w") as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

    return updates


def main():
    patch = load_patch()
    total_patches = sum(len(v) for v in patch.values())
    print(f"Loaded patch: {total_patches} label changes across {len(patch)} tasks\n")

    yaml_files = sorted(DATASET_DIR.glob("*.yaml"))
    print(f"Found {len(yaml_files)} YAML files in {DATASET_DIR}\n")

    total_updates = 0
    for fpath in yaml_files:
        updates = apply_patch_to_file(fpath, patch)
        status = f"{updates} labels updated" if updates > 0 else "no matching tasks"
        print(f"  {fpath.name}: {status}")
        total_updates += updates

    print(f"\nTotal updates across all files: {total_updates}")


if __name__ == "__main__":
    main()
