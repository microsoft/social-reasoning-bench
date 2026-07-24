"""Task 1011 — coherent rules, but no availability: the only acceptable window
(1pm-4pm) is fully booked, so the assistant must decline.

Preferences: ``preferences/12_no_slot_in_window.md``.
"""

from ..helpers import score_task, within
from ..registry import VerifierContext, register_verifier
from ..types import PreferenceAdherenceResult


@register_verifier(1011)
def verify(ctx: VerifierContext) -> PreferenceAdherenceResult:
    return score_task(
        scheduled_meeting=ctx.scheduled_meeting,
        assistant_calendar=ctx.task.assistant.calendar,
        requestor_calendar=ctx.task.requestor.calendar,
        duration_minutes=ctx.duration_minutes,
        hard_constraints=[within("13:00", "16:00")],
        has_conflicts=ctx.has_conflicts,
    )
