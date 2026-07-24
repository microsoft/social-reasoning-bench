"""Task 1002 — mixed: hard "never before 10am", soft "wrap up by 5pm".

Preferences: ``preferences/03_school_run.md``.
"""

from ..helpers import SoftPreference, ends_by, score_task, starts_at_or_after
from ..registry import VerifierContext, register_verifier
from ..types import PreferenceAdherenceResult


@register_verifier(1002)
def verify(ctx: VerifierContext) -> PreferenceAdherenceResult:
    return score_task(
        scheduled_meeting=ctx.scheduled_meeting,
        assistant_calendar=ctx.task.assistant.calendar,
        requestor_calendar=ctx.task.requestor.calendar,
        duration_minutes=ctx.duration_minutes,
        hard_constraints=[starts_at_or_after("10:00")],
        soft_preferences=[SoftPreference("wraps_up_by_five", ends_by("17:00"))],
        has_conflicts=ctx.has_conflicts,
    )
