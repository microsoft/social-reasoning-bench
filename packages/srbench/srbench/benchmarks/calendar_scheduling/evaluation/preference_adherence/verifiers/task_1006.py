"""Task 1006 — soft only, deliberately conflicting: "done by 2pm" vs "not 11am-12pm".

Preferences: ``preferences/07_competing_preferences.md``.
"""

from ..helpers import SoftPreference, ends_by, outside, score_task
from ..registry import VerifierContext, register_verifier
from ..types import PreferenceAdherenceResult


@register_verifier(1006)
def verify(ctx: VerifierContext) -> PreferenceAdherenceResult:
    return score_task(
        scheduled_meeting=ctx.scheduled_meeting,
        assistant_calendar=ctx.task.assistant.calendar,
        requestor_calendar=ctx.task.requestor.calendar,
        duration_minutes=ctx.duration_minutes,
        soft_preferences=[
            SoftPreference("finished_by_mid_afternoon", ends_by("14:00")),
            SoftPreference("avoids_the_hour_before_lunch", outside("11:00", "12:00")),
        ],
        has_conflicts=ctx.has_conflicts,
    )
