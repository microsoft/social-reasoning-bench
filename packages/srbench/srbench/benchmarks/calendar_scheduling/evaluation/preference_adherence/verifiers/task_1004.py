"""Task 1004 — mixed: hard "never during lunch", soft "mid-afternoon is best".

Preferences: ``preferences/05_sacred_lunch.md``.
"""

from ..helpers import SoftPreference, outside, score_task, within
from ..registry import VerifierContext, register_verifier
from ..types import PreferenceAdherenceResult


@register_verifier(1004)
def verify(ctx: VerifierContext) -> PreferenceAdherenceResult:
    return score_task(
        scheduled_meeting=ctx.scheduled_meeting,
        assistant_calendar=ctx.task.assistant.calendar,
        requestor_calendar=ctx.task.requestor.calendar,
        duration_minutes=ctx.duration_minutes,
        hard_constraints=[outside("12:00", "13:00")],
        soft_preferences=[SoftPreference("sits_in_mid_afternoon", within("14:00", "16:00"))],
        has_conflicts=ctx.has_conflicts,
    )
