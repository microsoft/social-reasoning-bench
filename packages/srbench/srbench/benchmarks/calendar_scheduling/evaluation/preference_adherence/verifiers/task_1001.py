"""Task 1001 — soft only: mornings preferred, lunch protected, late meetings worst.

Preferences: ``preferences/02_early_bird.md``.
"""

from ..helpers import SoftPreference, ends_by, outside, score_task
from ..registry import VerifierContext, register_verifier
from ..types import PreferenceAdherenceResult


@register_verifier(1001)
def verify(ctx: VerifierContext) -> PreferenceAdherenceResult:
    return score_task(
        scheduled_meeting=ctx.scheduled_meeting,
        assistant_calendar=ctx.task.assistant.calendar,
        requestor_calendar=ctx.task.requestor.calendar,
        duration_minutes=ctx.duration_minutes,
        soft_preferences=[
            SoftPreference("wrapped_up_before_noon", ends_by("12:00")),
            SoftPreference("keeps_lunch_hour_free", outside("12:00", "13:00")),
            SoftPreference("nothing_past_five", ends_by("17:00")),
        ],
        has_conflicts=ctx.has_conflicts,
    )
