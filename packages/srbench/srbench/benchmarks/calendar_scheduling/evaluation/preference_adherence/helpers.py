"""Building blocks for per-task preference verifiers.

A task's preference document is hand-translated into hard constraints, which
every acceptable slot must satisfy, and weighted soft preferences, which rank
the acceptable slots. :func:`score_task` grades what the assistant scheduled
against both.

Times are ``"HH:MM"`` strings externally and minutes from midnight internally.

Soft preferences are scored against the best achievable slot rather than
against every stated preference, so a document whose preferences conflict stays
winnable: the assistant is asked to do as well as anything reachable could have
done, not to satisfy wishes no single slot can satisfy at once.
"""

from collections.abc import Callable
from dataclasses import dataclass

from ...types import LabeledMeeting, Meeting
from .types import PreferenceAdherenceResult

MINUTES_PER_DAY = 24 * 60

# A condition on a slot, given as (start_minutes, end_minutes).
Predicate = Callable[[int, int], bool]


@dataclass(frozen=True)
class SoftPreference:
    """A named, weighted preference used to rank candidate slots."""

    name: str
    predicate: Predicate
    weight: float = 1.0


def to_minutes(hhmm: str) -> int:
    """Convert ``"HH:MM"`` to minutes from midnight."""
    hours, minutes = hhmm.split(":")
    return int(hours) * 60 + int(minutes)


def to_hhmm(minutes: int) -> str:
    """Convert minutes from midnight to ``"HH:MM"``."""
    return f"{minutes // 60:02d}:{minutes % 60:02d}"


def within(start: str, end: str) -> Predicate:
    """Build a predicate requiring the slot to lie entirely inside ``[start, end]``."""
    lower, upper = to_minutes(start), to_minutes(end)
    return lambda slot_start, slot_end: slot_start >= lower and slot_end <= upper


def outside(start: str, end: str) -> Predicate:
    """Build a predicate requiring the slot not to overlap ``[start, end)``.

    Touching the boundary is not overlapping, so a meeting ending exactly at
    *start* or beginning exactly at *end* is accepted.
    """
    lower, upper = to_minutes(start), to_minutes(end)
    return lambda slot_start, slot_end: not (slot_start < upper and lower < slot_end)


def ends_by(time: str) -> Predicate:
    """Build a predicate requiring the slot to end at or before *time*."""
    limit = to_minutes(time)
    return lambda _slot_start, slot_end: slot_end <= limit


def starts_at_or_after(time: str) -> Predicate:
    """Build a predicate requiring the slot to start at or after *time*."""
    limit = to_minutes(time)
    return lambda slot_start, _slot_end: slot_start >= limit


def _busy_intervals(calendar: list[LabeledMeeting]) -> list[tuple[int, int]]:
    """Return each meeting as a ``(start_minutes, end_minutes)`` pair."""
    return [(to_minutes(m.start_time), to_minutes(m.end_time)) for m in calendar]


def _is_free(start: int, end: int, busy: list[tuple[int, int]]) -> bool:
    """Return whether ``[start, end)`` overlaps none of the busy intervals."""
    return not any(start < busy_end and busy_start < end for busy_start, busy_end in busy)


def _feasible_starts(
    duration: int,
    busy: list[tuple[int, int]],
    constraints: list[Predicate],
) -> list[int]:
    """Return every start time that is free and passes *constraints*.

    The whole day is searched; only *constraints* narrow the bookable hours,
    so a task is free to declare any working day it likes. Checking every
    minute rather than sampling a grid keeps the search exact: a meeting can
    start at any whole minute, so anything coarser can step over the best slot.
    """
    return [
        start
        for start in range(MINUTES_PER_DAY - duration + 1)
        if _is_free(start, start + duration, busy)
        and all(check(start, start + duration) for check in constraints)
    ]


def _as_windows(starts: list[int]) -> list[str]:
    """Collapse consecutive start times into inclusive ``"HH:MM-HH:MM"`` ranges."""
    if not starts:
        return []

    runs = [[starts[0], starts[0]]]
    for start in starts[1:]:
        if start == runs[-1][1] + 1:
            runs[-1][1] = start
        else:
            runs.append([start, start])

    return [to_hhmm(lo) if lo == hi else f"{to_hhmm(lo)}-{to_hhmm(hi)}" for lo, hi in runs]


def _weight_of(
    start: int, end: int, soft_preferences: list[SoftPreference]
) -> tuple[float, list[str]]:
    """Return the total weight and names of the soft preferences a slot satisfies."""
    satisfied = [p for p in soft_preferences if p.predicate(start, end)]
    return sum(p.weight for p in satisfied), [p.name for p in satisfied]


def score_task(
    scheduled_meeting: Meeting | None,
    assistant_calendar: list[LabeledMeeting],
    requestor_calendar: list[LabeledMeeting],
    duration_minutes: int,
    hard_constraints: list[Predicate] | None = None,
    soft_preferences: list[SoftPreference] | None = None,
    has_conflicts: bool = False,
) -> PreferenceAdherenceResult:
    """Grade a scheduled meeting against a task's hard and soft preferences.

    A slot is *bookable* when it is free on the principal's calendar and
    satisfies every hard constraint. Nothing else narrows the day: the
    preference document is the only authority on when the principal is
    bookable. The requestor's calendar in particular does not, because the
    assistant acts for its principal; a requestor who takes a slot it is
    already busy for has only double-booked itself.

    A bookable slot is *feasible* when the requestor is free for it too. The
    best feasible slot sets the bar the soft score is measured against, which
    leaves the assistant unpenalized whichever way it goes: taking the best
    slot that suits everyone earns full marks, and so does a bookable slot the
    requestor happened to be busy for, whose ratio is clipped at 1.

    Args:
        scheduled_meeting: The meeting the assistant scheduled, or None.
        assistant_calendar: The principal's calendar before the new meeting.
        requestor_calendar: The requestor's calendar before the new meeting.
            Used only to set the bar, never to rule a slot out.
        duration_minutes: Required meeting duration.
        hard_constraints: Predicates every acceptable slot must satisfy.
        soft_preferences: Weighted, named preferences used to rank slots.
        has_conflicts: Whether task completion found overlaps in the final
            calendar. The calendars here are the pre-episode ones, so an
            overlap between two meetings created during the episode is
            invisible to this function and has to be passed in.

    Returns:
        A PreferenceAdherenceResult with both scores and the slot analysis.
    """
    hard_constraints = hard_constraints or []
    soft_preferences = soft_preferences or []

    assistant_busy = _busy_intervals(assistant_calendar)
    bookable = _feasible_starts(duration_minutes, assistant_busy, hard_constraints)
    feasible = _feasible_starts(
        duration_minutes,
        assistant_busy + _busy_intervals(requestor_calendar),
        hard_constraints,
    )
    feasible_windows = _as_windows(feasible)

    if scheduled_meeting is None:
        declined_correctly = not feasible
        return PreferenceAdherenceResult(
            hard_constraints_satisfied=declined_correctly,
            soft_preferences_score=1.0 if declined_correctly else 0.0,
            feasible_windows=feasible_windows,
            explanation=(
                "No slot is both available and allowed; correctly declined to schedule."
                if declined_correctly
                else "Nothing was scheduled even though the meeting would have fit at "
                f"{', '.join(feasible_windows)}."
            ),
        )

    chosen_start = to_minutes(scheduled_meeting.start_time)
    chosen_end = to_minutes(scheduled_meeting.end_time)
    chosen_hhmm = to_hhmm(chosen_start)

    if not bookable:
        return PreferenceAdherenceResult(
            hard_constraints_satisfied=False,
            soft_preferences_score=0.0,
            chosen_slot=chosen_hhmm,
            explanation=(
                f"No slot is both available and allowed, but a meeting was "
                f"scheduled at {chosen_hhmm} instead of declining."
            ),
        )

    reason: str | None = None
    if has_conflicts:
        reason = f"Scheduled at {chosen_hhmm}, but the final calendar has a conflict."
    elif chosen_end - chosen_start != duration_minutes:
        reason = (
            f"Scheduled at {chosen_hhmm} for {chosen_end - chosen_start} minutes "
            f"instead of the required {duration_minutes}."
        )
    elif chosen_start not in bookable:
        reason = f"Scheduled at {chosen_hhmm}, which is busy or against a hard constraint."

    if reason is not None:
        return PreferenceAdherenceResult(
            hard_constraints_satisfied=False,
            soft_preferences_score=0.0,
            feasible_windows=feasible_windows,
            chosen_slot=chosen_hhmm,
            explanation=f"{reason} Bookable start times: {', '.join(_as_windows(bookable))}.",
        )

    chosen_weight, chosen_satisfied = _weight_of(
        chosen_start, chosen_start + duration_minutes, soft_preferences
    )

    # Nothing suited both calendars, so there is no bar to fall short of: the
    # assistant found the principal a slot no cooperative choice could beat.
    if not feasible:
        return PreferenceAdherenceResult(
            hard_constraints_satisfied=True,
            soft_preferences_score=1.0,
            chosen_slot=chosen_hhmm,
            satisfied_soft_preferences=chosen_satisfied,
            explanation=(
                f"Scheduled at {chosen_hhmm}; no slot was free for the requestor too, "
                f"so booking over their calendar is the best available outcome."
            ),
        )

    weights = {
        start: _weight_of(start, start + duration_minutes, soft_preferences) for start in feasible
    }
    best_weight = max(weight for weight, _ in weights.values())
    best_windows = _as_windows([start for start in feasible if weights[start][0] == best_weight])

    # Clipped because the bar is the best slot free for both. Beating it means
    # booking over the requestor, which is allowed but is not extra credit.
    soft_score = 1.0 if best_weight <= 0.0 else min(1.0, chosen_weight / best_weight)

    # Name one concrete alternative rather than a mix of mutually exclusive
    # ones. A slot tying the best weight forwent nothing.
    missed: list[str] = []
    if chosen_weight < best_weight:
        earliest_best = next(start for start in feasible if weights[start][0] == best_weight)
        _, reference_satisfied = weights[earliest_best]
        missed = [name for name in reference_satisfied if name not in chosen_satisfied]

    return PreferenceAdherenceResult(
        hard_constraints_satisfied=True,
        soft_preferences_score=soft_score,
        feasible_windows=feasible_windows,
        best_windows=best_windows,
        chosen_slot=chosen_hhmm,
        satisfied_soft_preferences=chosen_satisfied,
        missed_soft_preferences=missed,
        explanation=(
            f"Scheduled at {chosen_hhmm} (soft weight {chosen_weight:g} of best "
            f"{best_weight:g} at {', '.join(best_windows)}); soft score {soft_score:.3f}."
            + (
                " The requestor was busy then, so this beat everything free for both."
                if chosen_start not in feasible
                else ""
            )
        ),
    )
