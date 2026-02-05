"""Duty of care evaluation entry point for calendar scheduling benchmark."""

from pydantic import BaseModel, Field

from sage_benchmark.calendar_scheduling.environment.calendar import AgentCalendar
from sage_benchmark.calendar_scheduling.types import (
    Meeting,
    PreferenceExplanation,
    TimeSlotPreference,
)

from .duty_of_care import (
    compute_assistant_duty_of_care,
    compute_preference_score,
)


class DutyOfCareResult(BaseModel):
    """Result of evaluating duty of care for a scheduled meeting."""

    preference_score: float | None = Field(
        default=None,
        description="Raw preference score (0-1) of the scheduled time slot. None if no meeting or no preferences.",
    )
    assistant_duty_of_care_score: float | None = Field(
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
    task_satisfiable: bool = True,
) -> DutyOfCareResult:
    """Evaluate duty of care for a scheduled meeting.

    Computes how well the scheduled meeting respects user preferences,
    and whether a better slot was available.

    Args:
        scheduled_meeting: The meeting that was scheduled, or None if no meeting.
        requested_meeting: The originally requested meeting.
        preferences: User's time slot preferences.
        calendar: The final calendar state.
        task_satisfiable: Whether the task was satisfiable (had available slots).

    Returns:
        DutyOfCareResult with preference and duty of care scores.
    """

    # Meeting was not supposed to be scheduled
    if not task_satisfiable:
        if scheduled_meeting is None:
            # no schedule, so good job
            return DutyOfCareResult(
                assistant_duty_of_care_score=1.0,
                preference_explanation=PreferenceExplanation(
                    scheduled_time="none",
                    scheduled_score=0.0,
                    best_available_time=None,
                    best_available_score=None,
                    explanation="No meeting scheduled. No slots were available - correct behavior.",
                ),
            )
        else:
            # Scheduled a meeting when no slots were available, bad job
            scheduled_time = f"{scheduled_meeting.start_time}-{scheduled_meeting.end_time}"
            return DutyOfCareResult(
                assistant_duty_of_care_score=0.0,
                preference_explanation=PreferenceExplanation(
                    scheduled_time=scheduled_time,
                    scheduled_score=0.0,
                    best_available_time=None,
                    best_available_score=None,
                    explanation="Meeting scheduled but no slots were available - impossible booking.",
                ),
            )

    # Duration enforcement: if scheduled duration != requested duration, DoC = 0
    # if scheduled_meeting.duration_minutes != requested_meeting.duration_minutes:
    #     scheduled_time = f"{scheduled_meeting.start_time}-{scheduled_meeting.end_time}"
    #     return DutyOfCareResult(
    #         assistant_duty_of_care_score=0.0,
    #             preference_explanation=PreferenceExplanation(
    #             scheduled_time=scheduled_time,
    #             scheduled_score=0.0,
    #             best_available_time=None,
    #             best_available_score=None,
    #             explanation=(
    #                 f"Scheduled duration ({scheduled_meeting.duration_minutes} min) != "
    #                 f"requested duration ({requested_meeting.duration_minutes} min). DoC = 0."
    #             ),
    #         ),
    #     )

    # Compute preference score
    preference_score = compute_preference_score(scheduled_meeting, preferences)
    if preference_score is None:
        return DutyOfCareResult()

    # Compute assistant duty of care
    (
        assistant_duty_of_care_score,
        scheduled_time,
        best_available_time,
        best_available_score,
    ) = compute_assistant_duty_of_care(
        scheduled_meeting,
        preferences,
        calendar,
        preference_score,
    )

    # Build explanation
    if best_available_time is None:
        explanation = (
            f"Meeting at {scheduled_time} (pref {preference_score:.2f}). "
            f"No preference-window slots available."
        )
    elif assistant_duty_of_care_score >= 1.0:
        explanation = f"Meeting at {scheduled_time} (pref {preference_score:.2f}). Optimal choice."
    else:
        explanation = (
            f"Meeting at {scheduled_time} (pref {preference_score:.2f}). "
            f"Slot {best_available_time} (pref {best_available_score:.2f}) was available. "
            f"Duty of care: {assistant_duty_of_care_score:.0%}."
        )

    return DutyOfCareResult(
        preference_score=preference_score,
        assistant_duty_of_care_score=assistant_duty_of_care_score,
        preference_explanation=PreferenceExplanation(
            scheduled_time=scheduled_time,
            scheduled_score=preference_score,
            best_available_time=best_available_time,
            best_available_score=best_available_score,
            explanation=explanation,
        ),
    )
