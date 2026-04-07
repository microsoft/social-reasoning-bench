"""Calendar-specific helpers for whimsical strategy injection.

Task loading, instruction parsing, task conversion, and the calendar-specific
CLI runner all live here — separate from the shared StrategyProvider.
"""

import random
import re
from collections.abc import Sequence
from pathlib import Path

import yaml
from sage_benchmark.benchmarks.calendar_scheduling.loader import load_tasks
from sage_benchmark.benchmarks.calendar_scheduling.types import CalendarTask

from sage_data_gen.shared.whimsical import StrategyProvider


def parse_instruction_metadata(instruction: str) -> dict[str, str]:
    """Extract name, company, role from a requestor instruction message.

    Args:
        instruction: The requestor's instruction message text.

    Returns:
        Dict with keys 'name', 'company', and 'role' extracted from the instruction.

    Raises:
        ValueError: If the instruction does not match any known format.
    """
    # Try old format: "You are {name}'s calendar scheduling personal assistant. {name} works for {company} and is a {role}."
    pattern = (
        r"You are (.+?)'s calendar scheduling personal assistant\."
        r" \1 works for (.+?) and is a (.+?)\."
    )
    match = re.search(pattern, instruction)
    if match:
        return {"name": match.group(1), "company": match.group(2), "role": match.group(3)}
    # Try new format: "I am {name}. I work for {company} and am a {role}."
    pattern2 = r"I am[,]? (.+?)\. I work for (.+?) and (?:am|is) (?:a |an |the )?(.+?)\."
    match2 = re.search(pattern2, instruction)
    if match2:
        return {"name": match2.group(1), "company": match2.group(2), "role": match2.group(3)}
    raise ValueError(f"Could not parse instruction message: {instruction[:100]}")


def extract_assistant_name(assistant_instruction: str, name: str | None = None) -> str:
    """Extract the assistant's name. Uses the name field if available, falls back to parsing instruction.

    Args:
        assistant_instruction: The assistant's instruction message text.
        name: Pre-extracted name, if available.

    Returns:
        The assistant's name as a string.

    Raises:
        ValueError: If name is not provided and cannot be parsed from the instruction.
    """
    if name:
        return name
    match = re.search(
        r"(?:You are|I am[,]?) (.+?)(?:'s calendar scheduling personal assistant|\.)",
        assistant_instruction,
    )
    if match:
        return match.group(1)
    raise ValueError(f"Could not extract assistant name from: {assistant_instruction[:100]}")


async def convert_tasks_with_strategies(
    tasks: Sequence[CalendarTask],
    strategy_provider: StrategyProvider,
    inject_fn,
    strategy_assignment: str = "sequential",
    max_strategies: int | None = None,
    rng: random.Random | None = None,
    attack_type: str = "unknown",
) -> list[CalendarTask]:
    """Convert normal tasks to adversarial ones using WhimsyGen strategies.

    Args:
        tasks: List of CalendarTask objects to convert.
        strategy_provider: StrategyProvider with loaded strategies.
        inject_fn: Function(original_instruction, assistant_name, strategy, requested_meeting) -> str.
        strategy_assignment: How to assign strategies ("sequential", "random", "unique", "single").
        max_strategies: Max strategies to generate (required for sequential/random modes).
        rng: Random number generator for random assignment.
        attack_type: Attack type label for the malicious tasks (default: "unknown").

    Returns:
        List of adversarial CalendarTask objects with injected malicious prompts.
    """
    rng = rng or random.Random()

    if strategy_assignment == "unique":
        await strategy_provider.load_or_generate(len(tasks))
    elif strategy_assignment == "single":
        await strategy_provider.load_or_generate(1)
    else:
        if max_strategies is None:
            raise ValueError("max_strategies is required for sequential/random modes")
        await strategy_provider.load_or_generate(min(len(tasks), max_strategies))

    adversarial_tasks = []
    for task in tasks:
        assistant_name = extract_assistant_name(task.assistant.instruction_message, task.assistant.name)

        if strategy_assignment == "random":
            strategy = strategy_provider.get_random(rng)
        else:
            strategy = strategy_provider.get_next()

        new_instruction = inject_fn(
            original_instruction=task.requestor.instruction_message,
            assistant_name=assistant_name,
            strategy=strategy,
            requested_meeting=task.requestor.requested_meeting,
        )

        task_dict = task.model_dump(mode="json")
        task_dict["requestor"]["malicious_prompt"] = new_instruction
        task_dict["requestor"]["is_malicious"] = True
        task_dict["requestor"]["malicious_target"] = attack_type
        task_dict["requestor"]["malicious_strategy"] = "whimsical"
        adversarial_tasks.append(CalendarTask(**task_dict))

    return adversarial_tasks


def save_tasks_yaml(tasks: list[CalendarTask], output_path: Path) -> None:
    """Save tasks to YAML file.

    Args:
        tasks: List of calendar tasks to serialize.
        output_path: Destination file path for the YAML output.
    """
    tasks_dict = {"tasks": [task.model_dump(mode="json") for task in tasks]}
    with open(output_path, "w") as f:
        yaml.dump(
            tasks_dict, f, default_flow_style=False, sort_keys=False, allow_unicode=True, width=120
        )


def build_arg_parser(description: str):
    """Build the CLI argument parser for calendar whimsical injection scripts.

    Args:
        description: Help text description for the argument parser.

    Returns:
        Configured argparse.ArgumentParser instance.
    """
    import argparse

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("input_yaml", help="Input tasks YAML file")
    parser.add_argument("-o", "--output", help="Output YAML file")
    parser.add_argument("-m", "--model", required=True, help="Model for strategy generation")
    parser.add_argument(
        "--data-dir",
        type=Path,
        help="Directory for whimsygen data. Defaults to input file's parent directory.",
    )
    parser.add_argument(
        "--strategy-assignment",
        choices=["sequential", "random", "unique", "single"],
        default="single",
    )
    parser.add_argument("--topics", nargs="+")
    parser.add_argument("--seed-chunk-size", type=int, default=5000)
    parser.add_argument("--max-chunks-per-seed", type=int)
    parser.add_argument("--max-strategies-per-chunk", type=int)
    parser.add_argument("--max-strategies-per-seed", type=int)
    parser.add_argument("--prefetch-seeds", type=int)
    parser.add_argument("--prefetch-strategies", type=int)
    parser.add_argument("--max-strategies", type=int)
    parser.add_argument("--rng-seed", type=int, default=42)
    parser.add_argument("--strategies-file", type=Path)
    return parser


async def run_injection(args, inject_fn, task_description: str) -> None:
    """Shared CLI runner for calendar whimsical injection scripts.

    Args:
        args: Parsed CLI arguments from build_arg_parser.
        inject_fn: Injection function that rewrites instructions with a malicious strategy.
        task_description: Human-readable task description for the strategy provider.

    Raises:
        SystemExit: If required arguments are missing or conflicting for the
            chosen strategy assignment mode.
    """
    if args.strategy_assignment in ("sequential", "random") and args.max_strategies is None:
        raise SystemExit("--max-strategies is required for sequential/random modes")
    if args.strategy_assignment in ("single", "unique") and args.max_strategies is not None:
        raise SystemExit("--max-strategies is not allowed for single/unique modes")

    input_path = Path(args.input_yaml)
    output_path = (
        Path(args.output)
        if args.output
        else input_path.parent / f"{input_path.stem}-whimsical{input_path.suffix}"
    )

    print(f"Loading tasks from {input_path}")
    loaded = load_tasks([input_path])
    tasks = loaded.all_tasks
    print(f"Loaded {len(tasks)} tasks")

    data_dir = args.data_dir or input_path.parent
    data_dir.mkdir(parents=True, exist_ok=True)
    seeds_dir = data_dir / "seeds"
    strategies_file = args.strategies_file if args.strategies_file else data_dir / "strategies.yaml"

    strategy_provider = StrategyProvider(
        model=args.model,
        seeds=seeds_dir,
        task=task_description,
        strategies=strategies_file,
        topics=args.topics,
        chunk_size=args.seed_chunk_size,
        max_chunks_per_seed=args.max_chunks_per_seed,
        max_strategies_per_chunk=args.max_strategies_per_chunk,
        max_strategies_per_seed=args.max_strategies_per_seed,
        prefetch_seeds=args.prefetch_seeds,
        prefetch_strategies=args.prefetch_strategies,
    )

    print(f"Generating adversarial tasks (model: {args.model})...")
    rng = random.Random(args.rng_seed)
    adversarial_tasks = await convert_tasks_with_strategies(
        tasks=tasks,
        strategy_provider=strategy_provider,
        inject_fn=inject_fn,
        strategy_assignment=args.strategy_assignment,
        max_strategies=args.max_strategies,
        rng=rng,
    )

    print(f"Saving to {output_path}")
    save_tasks_yaml(adversarial_tasks, output_path)
    print(
        f"\nDone!\n  Input:  {input_path}\n  Output: {output_path}\n  Tasks:  {len(adversarial_tasks)}"
    )
