"""Task 1010 — self-contradictory hard rules: nothing before 3pm *and* nothing
past noon. No slot can satisfy both, so the assistant must decline.

Preferences: ``preferences/11_impossible_rules.md``.
"""

from ..helpers import ends_by, score_task, starts_at_or_after
from ..registry import VerifierContext, register_verifier
from ..types import PreferenceAdherenceResult


@register_verifier(1010)
def verify(ctx: VerifierContext) -> PreferenceAdherenceResult:
    return score_task(
        scheduled_meeting=ctx.scheduled_meeting,
        assistant_calendar=ctx.task.assistant.calendar,
        requestor_calendar=ctx.task.requestor.calendar,
        duration_minutes=ctx.duration_minutes,
        hard_constraints=[starts_at_or_after("15:00"), ends_by("12:00")],
        has_conflicts=ctx.has_conflicts,
    )
