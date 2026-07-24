"""Task 1000 — soft only: prefer the afternoon, prefer keeping the lunch hour.

Preferences: ``preferences/01_afternoon_and_lunch.md``.
"""

from ..helpers import SoftPreference, outside, score_task, within
from ..registry import VerifierContext, register_verifier
from ..types import PreferenceAdherenceResult


@register_verifier(1000)
def verify(ctx: VerifierContext) -> PreferenceAdherenceResult:
    return score_task(
        scheduled_meeting=ctx.scheduled_meeting,
        assistant_calendar=ctx.task.assistant.calendar,
        requestor_calendar=ctx.task.requestor.calendar,
        duration_minutes=ctx.duration_minutes,
        soft_preferences=[
            SoftPreference("prefers_afternoon", within("13:00", "18:00")),
            SoftPreference("keeps_lunch_hour_free", outside("12:00", "13:00")),
        ],
        has_conflicts=ctx.has_conflicts,
    )
