"""Programmatic preference-adherence evaluation for calendar scheduling.

Grades a scheduled meeting against hard constraints and weighted soft
preferences hand-translated from a task's natural-language preference document.
"""

from .helpers import (
    Predicate,
    SoftPreference,
    ends_by,
    outside,
    score_task,
    starts_at_or_after,
    starts_within,
    to_hhmm,
    to_minutes,
    within,
)
from .types import PreferenceAdherenceResult

__all__ = [
    # Result type
    "PreferenceAdherenceResult",
    # Declarations
    "Predicate",
    "SoftPreference",
    # Predicate constructors
    "ends_by",
    "outside",
    "starts_at_or_after",
    "starts_within",
    "within",
    # Scorer
    "score_task",
    # Time helpers
    "to_hhmm",
    "to_minutes",
]
