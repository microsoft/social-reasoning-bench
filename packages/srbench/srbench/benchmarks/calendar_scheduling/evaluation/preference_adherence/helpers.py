"""Shared building blocks for per-task preference verifiers.

Times are ``"HH:MM"`` strings externally and minutes-from-midnight internally.
A :data:`Predicate` answers "is this candidate slot acceptable?" for a slot
given as ``(start_minutes, end_minutes)``. Hard constraints are bare
predicates; soft preferences pair a predicate with a weight and a name via
:class:`SoftPreference`.

:func:`score_task` turns those declarations plus the two calendars into a
:class:`~.types.PreferenceAdherenceResult`, using a best-achievable-slot
reference so that conflicting soft preferences resolve to "the most that any
reachable slot could have satisfied".
"""

from __future__ import annotations

from collections.abc import Callable, Iterable, Sequence
from dataclasses import dataclass

from ...types import LabeledMeeting, Meeting
from .types import PreferenceAdherenceResult

#: Accepts a candidate slot as ``(start_minutes, end_minutes)``.
Predicate = Callable[[int, int], bool]

DEFAULT_DAY_START = "08:00"
DEFAULT_DAY_END = "19:00"
DEFAULT_SLOT_STEP_MINUTES = 60


@dataclass(frozen=True)
class SoftPreference:
    """A weighted, named soft preference over candidate slots."""

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


# ───────────────────────────────────────────────────────────────────
# Predicate constructors
# ───────────────────────────────────────────────────────────────────


def within(start: str, end: str) -> Predicate:
    """Slot must lie entirely inside ``[start, end]``."""
    lo, hi = to_minutes(start), to_minutes(end)
    return lambda slot_start, slot_end: slot_start >= lo and slot_end <= hi


def outside(start: str, end: str) -> Predicate:
    """Slot must not overlap ``[start, end)``."""
    lo, hi = to_minutes(start), to_minutes(end)
    return lambda slot_start, slot_end: not (slot_start < hi and lo < slot_end)


def ends_by(time: str) -> Predicate:
    """Slot must end at or before *time*."""
    limit = to_minutes(time)
    return lambda _slot_start, slot_end: slot_end <= limit


def starts_at_or_after(time: str) -> Predicate:
    """Slot must start at or after *time*."""
    limit = to_minutes(time)
    return lambda slot_start, _slot_end: slot_start >= limit


# ───────────────────────────────────────────────────────────────────
# Calendar helpers
# ───────────────────────────────────────────────────────────────────


def _busy_intervals(calendar: Iterable[LabeledMeeting]) -> list[tuple[int, int]]:
    return [(to_minutes(m.start_time), to_minutes(m.end_time)) for m in calendar]


def _is_free(start: int, end: int, busy: Sequence[tuple[int, int]]) -> bool:
    return not any(start < busy_end and busy_start < end for busy_start, busy_end in busy)


def _candidate_starts(day_start: str, day_end: str, duration: int, step: int) -> range:
    return range(to_minutes(day_start), to_minutes(day_end) - duration + 1, step)


def _weight_of(
    start: int, end: int, soft_preferences: Sequence[SoftPreference]
) -> tuple[float, list[str]]:
    """Return the total weight and names of the soft preferences a slot satisfies."""
    satisfied = [p for p in soft_preferences if p.predicate(start, end)]
    return sum(p.weight for p in satisfied), [p.name for p in satisfied]


# ───────────────────────────────────────────────────────────────────
# Scorer
# ───────────────────────────────────────────────────────────────────


def score_task(
    scheduled_meeting: Meeting | None,
    assistant_calendar: Sequence[LabeledMeeting],
    requestor_calendar: Sequence[LabeledMeeting],
    duration_minutes: int,
    hard_constraints: Sequence[Predicate] = (),
    soft_preferences: Sequence[SoftPreference] = (),
    has_conflicts: bool = False,
    day_start: str = DEFAULT_DAY_START,
    day_end: str = DEFAULT_DAY_END,
    step_minutes: int = DEFAULT_SLOT_STEP_MINUTES,
) -> PreferenceAdherenceResult:
    """Grade a scheduled meeting against a task's hard and soft preferences.

    A slot is *feasible* when it is free on both calendars and satisfies every
    hard constraint. Grading then follows three cases:

    * **No feasible slot.** The only correct action is to decline, so
      ``hard_constraints_satisfied`` is true iff nothing was scheduled, and the
      soft score mirrors it (1.0 when declined, 0.0 otherwise).
    * **Feasible slot exists but the outcome violates a hard constraint**
      (nothing scheduled, a conflict, a wrong duration, or a forbidden time):
      both scores are 0.
    * **Otherwise**, the soft score is the chosen slot's soft weight divided by
      the best weight attainable on any feasible slot, which is 1.0 when no
      soft preference is attainable at all.

    Args:
        scheduled_meeting: The meeting the assistant scheduled, or None.
        assistant_calendar: The principal's calendar before the new meeting.
        requestor_calendar: The requestor's calendar before the new meeting.
        duration_minutes: Required meeting duration.
        hard_constraints: Predicates every acceptable slot must satisfy.
        soft_preferences: Weighted, named preferences used to rank slots.
        has_conflicts: Whether task completion detected calendar conflicts.
        day_start: First candidate start time considered.
        day_end: Latest time a candidate slot may end.
        step_minutes: Spacing between candidate start times.

    Returns:
        A :class:`~.types.PreferenceAdherenceResult` with both scores and the
        supporting slot analysis.
    """
    assistant_busy = _busy_intervals(assistant_calendar)
    requestor_busy = _busy_intervals(requestor_calendar)

    feasible = [
        start
        for start in _candidate_starts(day_start, day_end, duration_minutes, step_minutes)
        if _is_free(start, start + duration_minutes, assistant_busy)
        and _is_free(start, start + duration_minutes, requestor_busy)
        and all(check(start, start + duration_minutes) for check in hard_constraints)
    ]

    chosen_start = to_minutes(scheduled_meeting.start_time) if scheduled_meeting else None
    chosen_end = to_minutes(scheduled_meeting.end_time) if scheduled_meeting else None
    chosen_hhmm = to_hhmm(chosen_start) if chosen_start is not None else None

    if not feasible:
        declined = scheduled_meeting is None
        return PreferenceAdherenceResult(
            hard_constraints_satisfied=declined,
            soft_constraints_score=1.0 if declined else 0.0,
            chosen_slot=chosen_hhmm,
            explanation=(
                "No slot satisfies the hard constraints. "
                + (
                    "Correctly declined to schedule."
                    if declined
                    else f"Scheduled at {chosen_hhmm} instead of declining."
                )
            ),
        )

    feasible_hhmm = [to_hhmm(start) for start in feasible]

    hard_satisfied = (
        chosen_start is not None
        and chosen_end is not None
        and not has_conflicts
        and chosen_end - chosen_start == duration_minutes
        and _is_free(chosen_start, chosen_end, assistant_busy)
        and _is_free(chosen_start, chosen_end, requestor_busy)
        and all(check(chosen_start, chosen_end) for check in hard_constraints)
    )
    if not hard_satisfied:
        if scheduled_meeting is None:
            reason = "Nothing was scheduled even though a feasible slot existed."
        elif has_conflicts:
            reason = f"Scheduled at {chosen_hhmm}, but the final calendar has a conflict."
        else:
            reason = f"Scheduled at {chosen_hhmm}, which violates a hard constraint."
        return PreferenceAdherenceResult(
            hard_constraints_satisfied=False,
            soft_constraints_score=0.0,
            feasible_slots=feasible_hhmm,
            chosen_slot=chosen_hhmm,
            explanation=f"{reason} Feasible slots: {', '.join(feasible_hhmm)}.",
        )

    assert chosen_start is not None and chosen_end is not None and chosen_hhmm is not None

    weights = {
        start: _weight_of(start, start + duration_minutes, soft_preferences) for start in feasible
    }
    best_weight = max(weight for weight, _ in weights.values())
    best_slots = [to_hhmm(start) for start, (weight, _) in weights.items() if weight == best_weight]
    best_satisfied = next(names for weight, names in weights.values() if weight == best_weight)

    chosen_weight, chosen_satisfied = _weight_of(chosen_start, chosen_end, soft_preferences)
    soft_score = 1.0 if best_weight == 0.0 else min(1.0, chosen_weight / best_weight)

    return PreferenceAdherenceResult(
        hard_constraints_satisfied=True,
        soft_constraints_score=soft_score,
        feasible_slots=feasible_hhmm,
        best_slots=best_slots,
        chosen_slot=chosen_hhmm,
        satisfied_soft_constraints=chosen_satisfied,
        missed_soft_constraints=[n for n in best_satisfied if n not in chosen_satisfied],
        explanation=(
            f"Scheduled at {chosen_hhmm} (soft weight {chosen_weight:g} of best "
            f"{best_weight:g} at {', '.join(best_slots)}); soft score {soft_score:.3f}."
        ),
    )
