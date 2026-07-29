"""Programmatic preference-adherence evaluation for calendar scheduling.

Provides the vocabulary a task's natural-language preference document is
hand-translated into: hard constraints every acceptable slot must satisfy, and
weighted soft preferences that rank the acceptable slots.
"""

from .helpers import (
    Predicate,
    SoftPreference,
    ends_by,
    outside,
    starts_at_or_after,
    to_hhmm,
    to_minutes,
    within,
)

__all__ = [
    # Declarations
    "Predicate",
    "SoftPreference",
    # Predicate constructors
    "ends_by",
    "outside",
    "starts_at_or_after",
    "within",
    # Time helpers
    "to_hhmm",
    "to_minutes",
]
