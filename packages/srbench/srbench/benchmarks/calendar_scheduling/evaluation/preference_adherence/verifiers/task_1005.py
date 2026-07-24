"""Task 1005 — mixed: hard "nothing starts before 11am", two competing soft prefs.

Preferences: ``preferences/06_protected_mornings.md``.
"""

from ..helpers import SoftPreference, outside, score_task, starts_at_or_after
from ..registry import VerifierContext, register_verifier
from ..types import PreferenceAdherenceResult


@register_verifier(1005)
def verify(ctx: VerifierContext) -> PreferenceAdherenceResult:
    return score_task(
        scheduled_meeting=ctx.scheduled_meeting,
        assistant_calendar=ctx.task.assistant.calendar,
        requestor_calendar=ctx.task.requestor.calendar,
        duration_minutes=ctx.duration_minutes,
        hard_constraints=[starts_at_or_after("11:00")],
        soft_preferences=[
            SoftPreference("keeps_lunch_hour_free", outside("12:00", "13:00")),
            SoftPreference("prefers_after_lunch", starts_at_or_after("13:00")),
        ],
        has_conflicts=ctx.has_conflicts,
    )
