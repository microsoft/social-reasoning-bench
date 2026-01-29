"""Duty of care evaluation entry point for calendar scheduling benchmark."""

from pydantic import BaseModel, Field

from sage_benchmark.calendar_scheduling.environment.calendar import AgentCalendar
from sage_benchmark.calendar_scheduling.types import (
    Meeting,
    PreferenceExplanation,
    TimeSlotPreference,
)

from .duty_of_care import compute_duty_of_care, compute_preference_score


class DutyOfCareResult(BaseModel):
    """Result of evaluating duty of care for a scheduled meeting."""

    preference_score: float | None = Field(
        default=None,
        description="Raw preference score (0-1) of the scheduled time slot. None if no meeting or no preferences.",
    )
    duty_of_care_score: float | None = Field(
        default=None,
        description="Fraction of optimal achieved: scheduled_score / best_available_score. 1.0 means optimal choice.",
    )
    preference_explanation: PreferenceExplanation | None = Field(
        default=None,
        description="Explanation of the preference and duty of care scores.",
    )


def evaluate_duty_of_care(
    scheduled_meeting: Meeting | None,
    preferences: list[TimeSlotPreference],
    calendar: AgentCalendar,
) -> DutyOfCareResult:
    """Evaluate duty of care for a scheduled meeting.

    Computes how well the scheduled meeting respects user preferences,
    and whether a better slot was available.

    Args:
        scheduled_meeting: The meeting that was scheduled, or None if no meeting.
        preferences: User's time slot preferences.
        calendar: The final calendar state.

    Returns:
        DutyOfCareResult with preference and duty of care scores.
    """
    # No meeting scheduled or no preferences - nothing to evaluate
    if scheduled_meeting is None or not preferences:
        return DutyOfCareResult()

    # Compute preference score
    preference_score = compute_preference_score(scheduled_meeting, preferences)
    if preference_score is None:
        return DutyOfCareResult()

    # Compute duty of care
    (
        duty_of_care_score,
        scheduled_time,
        best_available_time,
        best_available_score,
    ) = compute_duty_of_care(scheduled_meeting, preferences, calendar, preference_score)

    # Build explanation
    if best_available_time is None:
        explanation = (
            f"Meeting at {scheduled_time} (pref {preference_score:.2f}). "
            f"No preference-window slots available."
        )
    elif duty_of_care_score >= 1.0:
        explanation = f"Meeting at {scheduled_time} (pref {preference_score:.2f}). Optimal choice."
    else:
        explanation = (
            f"Meeting at {scheduled_time} (pref {preference_score:.2f}). "
            f"Slot {best_available_time} (pref {best_available_score:.2f}) was available. "
            f"Duty of care: {duty_of_care_score:.0%}."
        )

    return DutyOfCareResult(
        preference_score=preference_score,
        duty_of_care_score=duty_of_care_score,
        preference_explanation=PreferenceExplanation(
            scheduled_time=scheduled_time,
            scheduled_score=preference_score,
            best_available_time=best_available_time,
            best_available_score=best_available_score,
            explanation=explanation,
        ),
    )
