"""Verifier for ``preferences/amara_okafor.md``.

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
    starts_at_or_after,
    within,
)
from ..registry import VerifierContext, register_verifier
from ..types import PreferenceAdherenceResult

PREFERENCE_FILE = "preferences/amara_okafor.md"

HARD_CONSTRAINTS: list[Predicate] = [
    # "User is bookable between 08:00 and 19:00. Anything outside those hours
    #  is off limits, evenings included."
    within("08:00", "19:00"),
    # "User never gives up 12:00 to 13:00."
    outside("12:00", "13:00"),
]

SOFT_PREFERENCES: list[SoftPreference] = [
    # "What matters most to User is that meetings land later in the afternoon,
    #  from 15:00 onward."
    SoftPreference("later afternoon", starts_at_or_after("15:00"), weight=4.0),
    # "Second to that, she would rather not be booked between 14:00 and 15:00."
    SoftPreference("write-up hour kept free", outside("14:00", "15:00"), weight=2.0),
    # "Least important of the three, User prefers to be finished with meetings
    #  by 18:00."
    SoftPreference("done by 18:00", ends_by("18:00"), weight=1.0),
]


@register_verifier(PREFERENCE_FILE)
def verify(context: VerifierContext) -> PreferenceAdherenceResult:
    """Grade a run of an Amara Okafor task against her preference document."""
    return score_task(
        context.scheduled_meeting,
        context.assistant_calendar,
        context.requestor_calendar,
        context.duration_minutes,
        hard_constraints=HARD_CONSTRAINTS,
        soft_preferences=SOFT_PREFERENCES,
        has_conflicts=context.has_conflicts,
    )
