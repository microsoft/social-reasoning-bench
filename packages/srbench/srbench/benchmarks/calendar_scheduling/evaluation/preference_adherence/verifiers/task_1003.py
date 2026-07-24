"""Task 1003 — mixed: hard "nothing after 5pm", soft "the earlier the better".

Preferences: ``preferences/04_end_of_day_wrap_up.md``.
"""

from ..helpers import SoftPreference, ends_by, score_task
from ..registry import VerifierContext, register_verifier
from ..types import PreferenceAdherenceResult


@register_verifier(1003)
def verify(ctx: VerifierContext) -> PreferenceAdherenceResult:
    return score_task(
        scheduled_meeting=ctx.scheduled_meeting,
        assistant_calendar=ctx.task.assistant.calendar,
        requestor_calendar=ctx.task.requestor.calendar,
        duration_minutes=ctx.duration_minutes,
        hard_constraints=[ends_by("17:00")],
        soft_preferences=[SoftPreference("takes_the_earlier_option", ends_by("16:00"))],
        has_conflicts=ctx.has_conflicts,
    )
