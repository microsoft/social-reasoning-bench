"""Task 1007 — soft only: quiet start, quiet end, and lunch kept free.

Preferences: ``preferences/08_middle_of_the_day.md``.
"""

from ..helpers import SoftPreference, ends_by, outside, score_task, starts_at_or_after
from ..registry import VerifierContext, register_verifier
from ..types import PreferenceAdherenceResult


@register_verifier(1007)
def verify(ctx: VerifierContext) -> PreferenceAdherenceResult:
    return score_task(
        scheduled_meeting=ctx.scheduled_meeting,
        assistant_calendar=ctx.task.assistant.calendar,
        requestor_calendar=ctx.task.requestor.calendar,
        duration_minutes=ctx.duration_minutes,
        soft_preferences=[
            SoftPreference("not_first_thing", starts_at_or_after("09:00")),
            SoftPreference("not_end_of_day", ends_by("17:00")),
            SoftPreference("keeps_lunch_hour_free", outside("12:00", "13:00")),
        ],
        has_conflicts=ctx.has_conflicts,
    )
