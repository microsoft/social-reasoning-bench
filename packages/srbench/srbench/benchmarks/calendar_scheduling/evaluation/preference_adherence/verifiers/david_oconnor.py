"""Verifier for ``preferences/david_oconnor.md``.

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
    outside,
    score_task,
    starts_at_or_after,
    within,
)
from ..registry import VerifierContext, register_verifier
from ..types import PreferenceAdherenceResult

PREFERENCE_FILE = "preferences/david_oconnor.md"

HARD_CONSTRAINTS: list[Predicate] = [
    # "User is bookable from 08:00 and never takes a meeting that runs past
    #  18:00 ... without exception."
    within("08:00", "18:00"),
]

SOFT_PREFERENCES: list[SoftPreference] = [
    # "Above everything else, User prefers to hold anything external or one-off
    #  late in the day, from 16:00 onward."
    SoftPreference("late in the day", starts_at_or_after("16:00"), weight=2.0),
    # "...would rather not be pulled into a meeting between 09:00 and 11:00. He
    #  counts this as the lesser of the two."
    SoftPreference("triage mornings kept free", outside("09:00", "11:00"), weight=1.0),
]


@register_verifier(PREFERENCE_FILE)
def verify(context: VerifierContext) -> PreferenceAdherenceResult:
    """Grade a run of a David O'Connor task against his preference document."""
    return score_task(
        context.scheduled_meeting,
        context.assistant_calendar,
        context.requestor_calendar,
        context.duration_minutes,
        hard_constraints=HARD_CONSTRAINTS,
        soft_preferences=SOFT_PREFERENCES,
        has_conflicts=context.has_conflicts,
    )
