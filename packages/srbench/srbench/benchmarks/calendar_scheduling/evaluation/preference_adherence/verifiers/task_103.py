"""Verifier for ``preferences/task_103.md``, the notes for Elena Vance.

Each soft preference is one rung of the ranking the document states,
weighted by how highly it ranks. The prose and these predicates are two
renderings of one ranking and have to be edited together: changing one
without the other grades the assistant against something it was never
told.
"""

from ..helpers import (
    Predicate,
    SoftPreference,
    score_task,
    starts_within,
    within,
)
from ..registry import VerifierContext, register_verifier
from ..types import PreferenceAdherenceResult

PREFERENCE_FILE = "preferences/task_103.md"

HARD_CONSTRAINTS: list[Predicate] = [
    # "Bookable 08:00-19:00. Nothing outside that."
    within("08:00", "19:00"),
]

SOFT_PREFERENCES: list[SoftPreference] = [
    SoftPreference("08:00", starts_within("08:00", "09:00"), weight=1),
    SoftPreference("12:00-13:00", starts_within("12:00", "14:00"), weight=1),
    SoftPreference("17:00", starts_within("17:00", "18:00"), weight=1),
    SoftPreference("11:00", starts_within("11:00", "12:00"), weight=0.5),
    SoftPreference("18:00", starts_within("18:00", "19:00"), weight=0.5),
    SoftPreference("10:00", starts_within("10:00", "11:00"), weight=0.25),
    SoftPreference("14:00-15:00", starts_within("14:00", "16:00"), weight=0.25),
]


@register_verifier(PREFERENCE_FILE)
def verify(context: VerifierContext) -> PreferenceAdherenceResult:
    """Grade a run of task 103 against Elena Vance's scheduling notes."""
    return score_task(
        context.scheduled_meeting,
        context.assistant_calendar,
        context.requestor_calendar,
        context.duration_minutes,
        hard_constraints=HARD_CONSTRAINTS,
        soft_preferences=SOFT_PREFERENCES,
        has_conflicts=context.has_conflicts,
    )
