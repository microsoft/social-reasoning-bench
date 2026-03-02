"""Check how many is_secret labels would change based on majority vote from annotators.

Auto-detects full annotation files (all task IDs present) and ignores partial ones.
Outputs a JSON patch file with the label changes.
"""

import json
from collections import Counter
from pathlib import Path

import yaml

ANNOTATIONS_DIR = Path(__file__).parent / "annotations"
DATASET_PATH = (
    Path(__file__).parent.parent / "data" / "calendar-scheduling" / "final" / "small.yaml"
)
PATCH_PATH = Path(__file__).parent / "label_patch.json"


def load_dataset() -> dict[int, dict[str, bool]]:
    with open(DATASET_PATH) as f:
        data = yaml.safe_load(f)

    original_labels = {}
    for task in data["tasks"]:
        task_id = task["id"]
        labels = {}
        for event in task["assistant"]["calendar"]:
            labels[event["uid"]] = event["is_secret"]
        original_labels[task_id] = labels
    return original_labels


def load_full_annotations(expected_task_ids: set[str]) -> dict[str, dict[str, dict[str, bool]]]:
    annotations = {}
    for fpath in sorted(ANNOTATIONS_DIR.glob("*.json")):
        with open(fpath) as f:
            data = json.load(f)
        if set(data.keys()) >= expected_task_ids:
            name = fpath.stem
            annotations[name] = data
            print(f"  Using: {fpath.name} ({len(data)} tasks)")
        else:
            missing = expected_task_ids - set(data.keys())
            print(f"  Skipping: {fpath.name} (missing {len(missing)} tasks)")
    return annotations


def main():
    original_labels = load_dataset()
    expected_task_ids = {str(tid) for tid in original_labels}

    print("Loading annotations...")
    annotations = load_full_annotations(expected_task_ids)
    print(f"  {len(annotations)} full annotation files found\n")

    changes = []
    total_voted = 0

    task_ids = sorted(expected_task_ids, key=int)

    for task_id in task_ids:
        uid_votes: dict[str, list[bool]] = {}
        for ann in annotations.values():
            if task_id not in ann:
                continue
            for uid, vote in ann[task_id].items():
                uid_votes.setdefault(uid, []).append(vote)

        orig = original_labels.get(int(task_id), {})

        for uid, votes in sorted(uid_votes.items()):
            if len(votes) < 2:
                continue
            total_voted += 1

            counts = Counter(votes)
            majority_val, majority_count = counts.most_common(1)[0]

            if majority_count < 2:
                continue

            orig_val = orig.get(uid)
            if orig_val is None:
                continue

            if majority_val != orig_val:
                changes.append(
                    {
                        "task_id": int(task_id),
                        "uid": uid,
                        "old_value": orig_val,
                        "new_value": majority_val,
                        "votes": votes,
                    }
                )

    print(f"Total calendar events with >=2 annotator votes: {total_voted}")
    print(f"Labels where majority agrees with original: {total_voted - len(changes)}")
    print(f"Labels that would be REPLACED: {len(changes)}")
    print()

    if changes:
        print("Details of labels to replace:")
        print("-" * 70)
        for c in changes:
            vote_str = ", ".join(str(v) for v in c["votes"])
            print(
                f"  task {c['task_id']:>3} | {c['uid']:<20} | "
                f"{c['old_value']} -> {c['new_value']}  (votes: {vote_str})"
            )

        patch = [
            {"task_id": c["task_id"], "uid": c["uid"], "new_value": c["new_value"]} for c in changes
        ]
        with open(PATCH_PATH, "w") as f:
            json.dump(patch, f, indent=2)
        print(f"\nPatch saved to {PATCH_PATH}")
    else:
        print("No changes needed — no patch file written.")


if __name__ == "__main__":
    main()
