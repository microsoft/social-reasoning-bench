"""Shared CLI utilities for argument parsing."""

import argparse
from typing import Literal

ReasoningEffort = Literal["none", "minimal", "low", "medium", "high", "xhigh", "default"]
REASONING_EFFORT_CHOICES = ("none", "minimal", "low", "medium", "high", "xhigh", "default")


def parse_reasoning_effort(value: str) -> ReasoningEffort | int:
    """Parse reasoning effort: either a known string or an integer budget.

    Args:
        value: The reasoning effort value from CLI

    Returns:
        The original string if it's a known choice, or an integer if parseable

    Raises:
        argparse.ArgumentTypeError: If value is neither a known choice nor an integer
    """
    if value in REASONING_EFFORT_CHOICES:
        return value
    try:
        return int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(
            f"Invalid reasoning effort '{value}'. "
            f"Use one of {REASONING_EFFORT_CHOICES} or an integer budget."
        )
