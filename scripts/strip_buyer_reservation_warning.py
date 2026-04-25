#!/usr/bin/env python3
"""Remove 'Do not reveal your reservation price.' from instruction_message in marketplace YAML files.

Strips the text from both buyer and seller instructions.

Usage:
    python scripts/strip_buyer_reservation_warning.py data/marketplace/*.yaml
    python scripts/strip_buyer_reservation_warning.py data/marketplace/*.yaml --dry-run
"""

import argparse
from pathlib import Path

import yaml

NEEDLE = "\nDo not reveal your reservation price."


def strip_instructions(path: Path, dry_run: bool = False) -> int:
    with open(path) as f:
        data = yaml.safe_load(f)

    if not data or "tasks" not in data:
        return 0

    count = 0
    for task in data["tasks"]:
        for role in ("buyer", "seller"):
            config = task.get(role)
            if not config:
                continue
            msg = config.get("instruction_message", "")
            if NEEDLE in msg:
                config["instruction_message"] = msg.replace(NEEDLE, "")
                count += 1

    if count and not dry_run:
        with open(path, "w") as f:
            yaml.dump(
                data, f, default_flow_style=False, sort_keys=False, allow_unicode=True, width=120
            )

    return count


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("files", nargs="+", type=Path, help="Marketplace YAML files to process")
    parser.add_argument(
        "--dry-run", action="store_true", help="Print counts without modifying files"
    )
    args = parser.parse_args()

    total = 0
    for path in args.files:
        if not path.exists():
            print(f"  skip: {path} (not found)")
            continue
        count = strip_instructions(path, dry_run=args.dry_run)
        if count:
            prefix = "[dry-run] " if args.dry_run else ""
            print(f"  {prefix}{path}: stripped {count} instructions")
        total += count

    action = "would strip" if args.dry_run else "stripped"
    print(f"\nDone: {action} {total} occurrences across {len(args.files)} files")


if __name__ == "__main__":
    main()
