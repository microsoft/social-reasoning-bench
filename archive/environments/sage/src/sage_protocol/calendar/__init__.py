"""Calendar Gym: LLM-driven calendar scheduling scenarios for multi-agent systems."""

from .entities import (
    DayOfWeek,
    EndCondition,
    EndType,
    Event,
    Frequency,
    Modification,
    Month,
    ParticipantProfile,
    RecurrenceRule,
    TimeRange,
)

__version__ = "0.1.0"

__all__ = [
    # Core entities
    "Event",
    "Modification",
    "RecurrenceRule",
    "EndCondition",
    "ParticipantProfile",
    # Enums
    "Frequency",
    "DayOfWeek",
    "Month",
    "EndType",
    # Utilities
    "TimeRange",
]
