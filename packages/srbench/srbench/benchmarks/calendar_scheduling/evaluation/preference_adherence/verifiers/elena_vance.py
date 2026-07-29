"""Verifier for ``preferences/elena_vance.md``.

Each declaration below quotes the sentence it encodes. The prose and these
predicates have to be edited together: changing one without the other grades
the assistant against something it was never told.

Weights are the ranking the document states in words, not calibrated
magnitudes. Each one exceeds the sum of everything below it, so a preference
the document calls more important can never be outvoted by the rest combined.
"""

from ..helpers import (
    Predicate,
    SoftPreference,
    ends_by,
    outside,
    score_task,
    within,
)
from ..registry import VerifierContext, register_verifier
from ..types import PreferenceAdherenceResult

PREFERENCE_FILE = "preferences/elena_vance.md"

HARD_CONSTRAINTS: list[Predicate] = [
    # "User is bookable from 08:00, and never takes a meeting that runs past
    #  17:00 ... she treats that as absolute."
    within("08:00", "17:00"),
]

SOFT_PREFERENCES: list[SoftPreference] = [
    # "The preference User holds above the others is keeping 09:00 to 12:00
    #  clear."
    SoftPreference("deposition prep kept free", outside("09:00", "12:00"), weight=4.0),
    # "Next in importance, meetings work best for User over the middle of the
    #  day, between 12:00 and 14:00 ..."
    SoftPreference("middle of the day", within("12:00", "14:00"), weight=2.0),
    # "Last of the three, she prefers to be done with meetings by 16:00 ..."
    SoftPreference("done by 16:00", ends_by("16:00"), weight=1.0),
]


@register_verifier(PREFERENCE_FILE)
def verify(context: VerifierContext) -> PreferenceAdherenceResult:
    """Grade a run of an Elena Vance task against her preference document."""
    return score_task(
        context.scheduled_meeting,
        context.assistant_calendar,
        context.requestor_calendar,
        context.duration_minutes,
        hard_constraints=HARD_CONSTRAINTS,
        soft_preferences=SOFT_PREFERENCES,
        has_conflicts=context.has_conflicts,
    )
