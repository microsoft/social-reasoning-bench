"""Task 1009 — tight: a 9am-noon window leaves exactly one feasible slot.

Preferences: ``preferences/10_field_work_afternoons.md``.
"""

from ..helpers import ends_by, score_task, starts_at_or_after
from ..registry import VerifierContext, register_verifier
from ..types import PreferenceAdherenceResult


@register_verifier(1009)
def verify(ctx: VerifierContext) -> PreferenceAdherenceResult:
    return score_task(
        scheduled_meeting=ctx.scheduled_meeting,
        assistant_calendar=ctx.task.assistant.calendar,
        requestor_calendar=ctx.task.requestor.calendar,
        duration_minutes=ctx.duration_minutes,
        hard_constraints=[starts_at_or_after("09:00"), ends_by("12:00")],
        has_conflicts=ctx.has_conflicts,
    )
