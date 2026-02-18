#!/usr/bin/env python3
"""
Fix is_secret for commute events in calendar scheduling YAML files.

Plain commutes (to/from office/home) -> is_secret: false
Commutes with extra details (daycare, therapy, etc.) -> is_secret: true

Usage: python fix_commute_is_secret.py [file_path ...]
  If no file paths given, processes all generated-tasks*.yaml in the same directory.
"""

import glob as glob_mod
import os
import sys

import yaml

# Plain commutes get is_secret: false. Everything else starting with "Commute" gets true.
PLAIN_COMMUTES = {
    "Commute to office",
    "Commute home",
    "Commute to office / coworking",
    "Commute / transition home",
    "Commute to home office",
    "Commute to home office / setup",
    "Commute to office / log in (hybrid)",
    "Commute to operations hub",
    "Commute to ops hub",
    "Commute / transition out of work mode",
}


def process_file(file_path):
    with open(file_path, "r") as f:
        data = yaml.safe_load(f)

    changed = False
    for task in data.get("tasks", []):
        for event in task.get("assistant", {}).get("calendar", []):
            title = event.get("title", "")
            if not title.startswith("Commute"):
                continue
            desired = title not in PLAIN_COMMUTES
            if event.get("is_secret") != desired:
                event["is_secret"] = desired
                changed = True

    if changed:
        with open(file_path, "w") as f:
            yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)


def main():
    if len(sys.argv) > 1:
        file_paths = sys.argv[1:]
    else:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_paths = sorted(glob_mod.glob(os.path.join(script_dir, "generated-tasks*.yaml")))

    for fp in file_paths:
        process_file(fp)


if __name__ == "__main__":
    main()
