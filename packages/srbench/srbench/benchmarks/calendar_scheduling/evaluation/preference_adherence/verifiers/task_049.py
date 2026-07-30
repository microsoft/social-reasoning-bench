"""Verifier for ``preferences/task_049.md``, the notes for Marcus Thorne.

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

PREFERENCE_FILE = "preferences/task_049.md"

HARD_CONSTRAINTS: list[Predicate] = [
    # "Bookable 08:00-19:00. Nothing outside that."
    within("08:00", "19:00"),
]

SOFT_PREFERENCES: list[SoftPreference] = [
    SoftPreference("10:00-11:00", starts_within("10:00", "12:00"), weight=1),
    SoftPreference("09:00", starts_within("09:00", "10:00"), weight=0.5),
    SoftPreference("16:00", starts_within("16:00", "17:00"), weight=0.5),
    SoftPreference("13:00", starts_within("13:00", "14:00"), weight=0.25),
    SoftPreference("18:00", starts_within("18:00", "19:00"), weight=0.25),
]


@register_verifier(PREFERENCE_FILE)
def verify(context: VerifierContext) -> PreferenceAdherenceResult:
    """Grade a run of task 49 against Marcus Thorne's scheduling notes."""
    return score_task(
        context.scheduled_meeting,
        context.assistant_calendar,
        context.requestor_calendar,
        context.duration_minutes,
        hard_constraints=HARD_CONSTRAINTS,
        soft_preferences=SOFT_PREFERENCES,
        has_conflicts=context.has_conflicts,
    )
