"""Shared utilities for hand-crafted malicious task injection.

Each benchmark provides a thin CLI wrapper that calls :func:`inject_and_save`
with the appropriate loader, task type, and injection function.
"""

import argparse
from collections.abc import Callable, Sequence
from pathlib import Path
from typing import TypeVar

import yaml
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


def inject_and_save(
    input_path: Path,
    output_path: Path,
    load_fn: Callable[[Sequence[Path]], list[T]],
    inject_fn: Callable[[T, str], list[T]],
    attack_type: str,
) -> None:
    """Load tasks, apply hand-crafted injection, and write output YAML.

    Args:
        input_path: Path to input tasks YAML.
        output_path: Path to write output YAML.
        load_fn: Callable that takes a list of paths and returns tasks.
        inject_fn: Callable(task, attack_type) -> list of modified tasks.
        attack_type: The attack type to apply.
    """
    print(f"Loading tasks from {input_path}")
    tasks = load_fn([input_path])
    print(f"Loaded {len(tasks)} tasks")

    print(f"Applying hand-crafted {attack_type} attack...")
    malicious = [t for task in tasks for t in inject_fn(task, attack_type)]

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


def build_arg_parser(
    description: str,
    attack_types: list[str],
) -> argparse.ArgumentParser:
    """Build a standard CLI parser for hand-crafted injection scripts."""
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        "--input",
        type=Path,
        required=True,
        help="Input tasks YAML file",
    )
    parser.add_argument(
        "--attack-type",
        choices=attack_types,
        required=True,
        help="Attack type to apply",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=None,
        help="Output YAML (default: <stem>-malicious-hand-crafted-<attack>.yaml)",
    )
    return parser


def resolve_output_path(args: argparse.Namespace) -> Path:
    """Derive output path from args if not explicitly provided."""
    if args.output:
        return args.output
    input_path = Path(args.input)
    return input_path.parent / f"{input_path.stem}-malicious-hand-crafted-{args.attack_type}.yaml"
