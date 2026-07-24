"""Programmatic preference-adherence evaluation for calendar scheduling.

Replaces the numeric ZOPA-based outcome-optimality metric: tasks now express
the principal's preferences in natural language and are graded by a per-task
Python verifier that returns a hard-constraint verdict and a soft-preference
score.
"""

from . import verifiers as _verifiers  # noqa: F401  (imported for registration side effects)
from .helpers import (
    SoftPreference,
    ends_by,
    outside,
    score_task,
    starts_at_or_after,
    within,
)
from .registry import (
    VERIFIER_REGISTRY,
    VerifierContext,
    evaluate_preference_adherence,
    register_verifier,
)
from .types import PreferenceAdherenceResult

__all__ = [
    "PreferenceAdherenceResult",
    "SoftPreference",
    "VERIFIER_REGISTRY",
    "VerifierContext",
    "ends_by",
    "evaluate_preference_adherence",
    "outside",
    "register_verifier",
    "score_task",
    "starts_at_or_after",
    "within",
]
