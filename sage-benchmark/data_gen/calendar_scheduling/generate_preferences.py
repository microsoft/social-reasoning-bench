"""Utility to sample scheduling preferences and generate YAML variants."""

import argparse
import copy
import random
from pathlib import Path

import yaml
from sage_benchmark.calendar_scheduling.types import TimeSlotPreference

# Default time windows covering typical working hours
DEFAULT_TIME_WINDOWS = [
    ("08:00", "10:00"),  # Early morning
    ("10:00", "12:00"),  # Late morning
    ("12:00", "13:00"),  # Lunch
    ("13:00", "15:00"),  # Early afternoon
    ("15:00", "17:00"),  # Late afternoon
    ("17:00", "19:00"),  # Evening
]


def sample_preferences(
    rng: random.Random,
    time_windows: list[tuple[str, str]] | None = None,
) -> list[TimeSlotPreference]:
    """Sample scheduling preferences from a reasonable default distribution.

    The distribution biases toward:
    - Higher scores for afternoon slots
    - Lower scores for early morning and lunch
    - Some randomness to create variety

    Args:
        rng: Random number generator for reproducibility
        time_windows: Optional custom time windows, defaults to working hours

    Returns:
        List of TimeSlotPreference objects
    """
    windows = time_windows or DEFAULT_TIME_WINDOWS

    # Base scores with realistic bias (can be overridden by randomness)
    base_scores = {
        "08:00": 0.3,  # Early morning - most people less enthusiastic
        "10:00": 0.6,  # Late morning - decent
        "12:00": 0.2,  # Lunch - usually avoid
        "13:00": 0.7,  # Early afternoon - good
        "15:00": 0.8,  # Late afternoon - often preferred
        "17:00": 0.5,  # Evening - depends on person
    }

    preferences = []
    for start, end in windows:
        # Start with base score, add noise, clamp to [0.1, 1.0]
        base = base_scores.get(start, 0.5)
        noise = rng.gauss(0, 0.25)
        score = max(0.1, min(1.0, base + noise))
        score = round(score, 2)

        preferences.append(TimeSlotPreference(start_time=start, end_time=end, score=score))

    return preferences


def augment_task_with_preferences(
    task: dict,
    preferences: list[TimeSlotPreference],
) -> dict:
    """Add preferences to a task's assistant configuration.

    Args:
        task: Task dictionary from YAML
        preferences: Preferences to add

    Returns:
        Modified task dictionary (deep copy)
    """
    task = copy.deepcopy(task)
    assistant = task.get("assistant", {})

    if assistant.get("preferences"):
        raise ValueError(
            f"Task already has preferences defined. "
            f"Assistant email: {assistant.get('email', 'unknown')}"
        )

    assistant["preferences"] = [
        {"start_time": p.start_time, "end_time": p.end_time, "score": p.score} for p in preferences
    ]
    task["assistant"] = assistant

    return task


def generate_preference_variants(
    input_path: Path,
    output_dir: Path,
    seed: int = 42,
) -> Path:
    """Generate a YAML file with sampled preferences added to each task.

    Note: This function is now simplified - it only generates preferences without
    the expose_preferences field. Use the --expose-preferences CLI flag at runtime
    to control whether preferences are shown to the agent.

    Args:
        input_path: Path to source YAML file
        output_dir: Directory to write output files
        seed: Random seed for reproducibility

    Returns:
        Path to output file with preferences
    """
    with open(input_path) as f:
        data = yaml.safe_load(f)

    tasks = data.get("tasks", [])
    if not tasks:
        raise ValueError(f"No tasks found in {input_path}")

    # Check for existing preferences before modifying anything
    for i, task in enumerate(tasks):
        assistant = task.get("assistant", {})
        if assistant.get("preferences"):
            raise ValueError(
                f"Task {i} already has preferences. Assistant: {assistant.get('email', 'unknown')}"
            )

    rng = random.Random(seed)

    # Generate preferences for all tasks
    output_data = copy.deepcopy(data)

    for i, task in enumerate(tasks):
        # Sample fresh preferences for each task
        preferences = sample_preferences(rng)
        output_data["tasks"][i] = augment_task_with_preferences(task, preferences)

    # Write output file
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    stem = input_path.stem
    output_path = output_dir / f"{stem}-with-prefs.yaml"

    with open(output_path, "w") as f:
        yaml.dump(output_data, f, default_flow_style=False, sort_keys=False)

    return output_path


def main():
    parser = argparse.ArgumentParser(
        description="Generate YAML file with sampled scheduling preferences"
    )
    parser.add_argument("input", type=Path, help="Input YAML file")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Output directory (defaults to input file's directory)",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed for reproducibility",
    )

    args = parser.parse_args()

    output_dir = args.output_dir or args.input.parent

    output_path = generate_preference_variants(args.input, output_dir, args.seed)

    print(f"Generated:")
    print(f"  {output_path}")
    print(f"\nUse --expose-preferences flag when running the benchmark to include")
    print(f"preferences in the assistant agent's prompt.")


if __name__ == "__main__":
    main()
