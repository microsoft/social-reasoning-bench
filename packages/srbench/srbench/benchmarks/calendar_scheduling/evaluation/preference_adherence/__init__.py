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
    to_hhmm,
    to_minutes,
    within,
)
from .registry import (
    VerifierContext,
    evaluate_preference_adherence,
    register_verifier,
)
from .types import PreferenceAdherenceResult

# Imported for its side effect: registering every persona verifier. Keep this
# last, since the verifier modules import the names defined above.
from . import verifiers  # noqa: E402, F401  (isort: skip)

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
    "within",
    # Scorer
    "score_task",
    # Registry
    "VerifierContext",
    "evaluate_preference_adherence",
    "register_verifier",
    # Time helpers
    "to_hhmm",
    "to_minutes",
]
