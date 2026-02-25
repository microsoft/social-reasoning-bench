"""Large Malicious Whimsical Sanity Check experiments.

Validates that the winning adversarial strategy ("Feigning Hardball Commitments")
scales effectively to the full large dataset (140 tasks), compared against a
non-malicious baseline.
"""

from sage_benchmark.calendar_scheduling.experiments import ExperimentConfig

# Shared configuration
MODEL = "phyagi/gpt-5.1"
JUDGE_MODEL = "phyagi/gpt-4.1"


def experiment_baseline():
    """Non-malicious baseline on the large dataset."""
    return ExperimentConfig(
        paths=["data/calendar-scheduling/final/large.yaml"],
        model=MODEL,
        judge_model=JUDGE_MODEL,
        assistant_system_prompt="default",
        expose_preferences=True,
        explicit_cot=False,
        variant="baseline",
    )


def experiment_malicious():
    """Malicious whimsical strategy on the large dataset."""
    return ExperimentConfig(
        paths=["data/calendar-scheduling/final/large-malicious-whimsical.yaml"],
        model=MODEL,
        judge_model=JUDGE_MODEL,
        assistant_system_prompt="default",
        expose_preferences=True,
        explicit_cot=False,
        variant="malicious",
    )
