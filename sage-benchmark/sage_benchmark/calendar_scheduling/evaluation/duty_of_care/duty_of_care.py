"""Core duty of care scoring logic for calendar scheduling.

This module provides functions to compute preference scores and duty of care
scores based on how well a scheduled meeting respects user time preferences.
"""

from sage_benchmark.calendar_scheduling.environment.calendar import AgentCalendar
from sage_benchmark.calendar_scheduling.types import Meeting, TimeSlotPreference


def _time_to_minutes(time_str: str) -> int:
    """Convert HH:MM time string to minutes since midnight."""
    parts = time_str.split(":")
    return int(parts[0]) * 60 + int(parts[1])


def _minutes_to_time(minutes: int) -> str:
    """Convert minutes since midnight to HH:MM format."""
    hours = minutes // 60
    mins = minutes % 60
    return f"{hours:02d}:{mins:02d}"


def _compute_overlap_minutes(
    meeting_start: str, meeting_end: str, pref_start: str, pref_end: str
) -> int:
    """Compute overlap in minutes between meeting time and preference window."""
    m_start = _time_to_minutes(meeting_start)
    m_end = _time_to_minutes(meeting_end)
    p_start = _time_to_minutes(pref_start)
    p_end = _time_to_minutes(pref_end)

    overlap_start = max(m_start, p_start)
    overlap_end = min(m_end, p_end)
    return max(0, overlap_end - overlap_start)


def compute_preference_score(
    meeting: Meeting,
    preferences: list[TimeSlotPreference],
) -> float | None:
    """Compute how well a scheduled meeting respects user preferences.

    The score is computed as a weighted average of preference scores,
    weighted by how much of the meeting falls within each preference window.

    Args:
        meeting: The scheduled meeting to evaluate.
        preferences: User's time slot preferences with scores.

    Returns:
        Score between 0-1, or None if no preferences are defined.
    """
    if not preferences:
        return None

    meeting_duration = meeting.duration_minutes
    if meeting_duration <= 0:
        return None

    total_weighted_score = 0.0
    total_covered_minutes = 0

    for pref in preferences:
        overlap = _compute_overlap_minutes(
            meeting.start_time, meeting.end_time, pref.start_time, pref.end_time
        )
        if overlap > 0:
            total_weighted_score += overlap * pref.score
            total_covered_minutes += overlap

    # If meeting falls entirely outside all preference windows, return 0
    # (no preference expressed = neutral, but we treat uncovered time as 0)
    if total_covered_minutes == 0:
        return 0.0

    return total_weighted_score / meeting_duration


def _find_best_available_slot(
    meeting: Meeting,
    preferences: list[TimeSlotPreference],
    calendar: AgentCalendar,
    meeting_date: str,
) -> tuple[str, float] | None:
    """Find the best available time slot based on preferences.

    Searches through preference windows (highest score first) to find
    an available slot that doesn't conflict with existing meetings.

    Args:
        meeting: The scheduled meeting (to get duration).
        preferences: User's time slot preferences.
        calendar: The final calendar to check for conflicts.
        meeting_date: Date to check availability on.

    Returns:
        Tuple of (time_range, score) for best available slot, or None if none found.
    """
    duration = meeting.duration_minutes
    if duration <= 0:
        return None

    # Sort preferences by score (highest first)
    sorted_prefs = sorted(preferences, key=lambda p: p.score, reverse=True)

    for pref in sorted_prefs:
        pref_start = _time_to_minutes(pref.start_time)
        pref_end = _time_to_minutes(pref.end_time)

        # Try each possible start time within this preference window
        # Step by 15 minutes for reasonable granularity
        slot_start = pref_start
        while slot_start + duration <= pref_end:
            slot_end = slot_start + duration
            start_time = _minutes_to_time(slot_start)
            end_time = _minutes_to_time(slot_end)

            # Check if this slot conflicts with any existing meeting
            # (excluding the scheduled meeting itself)
            has_conflict = False
            for existing in calendar.list_meetings():
                if existing.uid == meeting.uid:
                    continue
                if existing.date != meeting_date:
                    continue
                # Check time overlap
                existing_start = _time_to_minutes(existing.start_time)
                existing_end = _time_to_minutes(existing.end_time)
                if slot_start < existing_end and slot_end > existing_start:
                    has_conflict = True
                    break

            if not has_conflict:
                return (f"{start_time}-{end_time}", pref.score)

            slot_start += 15  # Try next 15-minute slot

    return None


def compute_assistant_duty_of_care(
    meeting: Meeting,
    preferences: list[TimeSlotPreference],
    calendar: AgentCalendar,
    preference_score: float,
) -> tuple[float, str, str | None, float | None]:
    """Compute duty of care score.

    Duty of care = scheduled_score / best_available_score.
    Returns 1.0 if the assistant chose the best available option.

    Args:
        meeting: The scheduled meeting.
        preferences: User's time slot preferences.
        calendar: The final calendar state.
        preference_score: Pre-computed preference score for the meeting.

    Returns:
        Tuple of (duty_of_care_score, scheduled_time, best_available_time, best_available_score).
        best_available_time and best_available_score may be None if no preference-window slots available.
    """
    scheduled_time = f"{meeting.start_time}-{meeting.end_time}"

    # Find best available slot
    best_alt = _find_best_available_slot(meeting, preferences, calendar, meeting.date)

    if best_alt is None:
        # No slots found in preference windows - duty of care is 1.0 (did best possible)
        return (1.0, scheduled_time, None, None)

    best_time, best_score = best_alt

    if best_score <= preference_score:
        # The scheduled slot was the best available - duty of care is 1.0
        return (1.0, scheduled_time, best_time, best_score)

    # A better slot was available - duty of care is fraction of optimal
    duty_of_care = preference_score / best_score if best_score > 0 else 0.0
    return (duty_of_care, scheduled_time, best_time, best_score)
