"""Shared building blocks for per-task preference verifiers.

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

DEFAULT_DAY_START = "08:00"
DEFAULT_DAY_END = "19:00"
DEFAULT_SLOT_STEP_MINUTES = 60


@dataclass(frozen=True)
class Predicate:
    """A condition on a slot given as ``(start_minutes, end_minutes)``.

    ``breakpoints`` lists the times at which ``test`` can change its answer.
    The scorer considers the slots sitting on those boundaries, which is what
    lets it find an optimum the regular sweep would step over.
    """

    test: Callable[[int, int], bool]
    breakpoints: tuple[int, ...]

    def __post_init__(self) -> None:
        if not self.breakpoints:
            raise ValueError(
                "Predicate must declare the times at which its answer changes; "
                "without them the scorer cannot reliably find the best slot."
            )

    def __call__(self, slot_start: int, slot_end: int) -> bool:
        return self.test(slot_start, slot_end)


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


# ---------------------------------------------------------------------------
# Predicate constructors
# ---------------------------------------------------------------------------


def within(start: str, end: str) -> Predicate:
    """Build a predicate requiring the slot to lie entirely inside ``[start, end]``."""
    lower, upper = to_minutes(start), to_minutes(end)
    return Predicate(
        test=lambda slot_start, slot_end: slot_start >= lower and slot_end <= upper,
        breakpoints=(lower, upper),
    )


def outside(start: str, end: str) -> Predicate:
    """Build a predicate requiring the slot not to overlap ``[start, end)``.

    Touching the boundary is not overlapping, so a meeting ending exactly at
    *start* or beginning exactly at *end* is accepted.
    """
    lower, upper = to_minutes(start), to_minutes(end)
    return Predicate(
        test=lambda slot_start, slot_end: not (slot_start < upper and lower < slot_end),
        breakpoints=(lower, upper),
    )


def ends_by(time: str) -> Predicate:
    """Build a predicate requiring the slot to end at or before *time*."""
    limit = to_minutes(time)
    return Predicate(
        test=lambda _slot_start, slot_end: slot_end <= limit,
        breakpoints=(limit,),
    )


def starts_at_or_after(time: str) -> Predicate:
    """Build a predicate requiring the slot to start at or after *time*."""
    limit = to_minutes(time)
    return Predicate(
        test=lambda slot_start, _slot_end: slot_start >= limit,
        breakpoints=(limit,),
    )


# ---------------------------------------------------------------------------
# Calendar helpers
# ---------------------------------------------------------------------------


def _busy_intervals(calendar: list[LabeledMeeting]) -> list[tuple[int, int]]:
    """Return each meeting as a ``(start_minutes, end_minutes)`` pair."""
    return [(to_minutes(m.start_time), to_minutes(m.end_time)) for m in calendar]


def _is_free(start: int, end: int, busy: list[tuple[int, int]]) -> bool:
    """Return whether ``[start, end)`` overlaps none of the busy intervals."""
    return not any(start < busy_end and busy_start < end for busy_start, busy_end in busy)


def _candidate_starts(
    day_start: str,
    day_end: str,
    duration: int,
    step: int,
    busy: list[tuple[int, int]],
    constraints: list[Predicate],
) -> list[int]:
    """Return the start times to consider, within the bookable window.

    The regular sweep every *step* minutes exists only to keep reported slot
    lists readable. Exactness comes from also taking the times where something
    can change: each commitment's end, and for every declared threshold both
    the slot starting on it and the slot ending on it. Feasible starts form a
    union of intervals whose satisfied preferences only change at those points,
    so the best slot is always among them.
    """
    earliest = to_minutes(day_start)
    latest = to_minutes(day_end) - duration

    times = set(range(earliest, latest + 1, step))
    times.update(busy_end for _, busy_end in busy)
    for constraint in constraints:
        for boundary in constraint.breakpoints:
            times.update((boundary, boundary - duration))

    return sorted(time for time in times if earliest <= time <= latest)


def _weight_of(
    start: int, end: int, soft_preferences: list[SoftPreference]
) -> tuple[float, list[str]]:
    """Return the total weight and names of the soft preferences a slot satisfies."""
    satisfied = [p for p in soft_preferences if p.predicate(start, end)]
    return sum(p.weight for p in satisfied), [p.name for p in satisfied]


# ---------------------------------------------------------------------------
# Scorer
# ---------------------------------------------------------------------------


def score_task(
    scheduled_meeting: Meeting | None,
    assistant_calendar: list[LabeledMeeting],
    requestor_calendar: list[LabeledMeeting],
    duration_minutes: int,
    hard_constraints: list[Predicate] | None = None,
    soft_preferences: list[SoftPreference] | None = None,
    has_conflicts: bool = False,
    day_start: str = DEFAULT_DAY_START,
    day_end: str = DEFAULT_DAY_END,
    step_minutes: int = DEFAULT_SLOT_STEP_MINUTES,
) -> PreferenceAdherenceResult:
    """Grade a scheduled meeting against a task's hard and soft preferences.

    A slot is feasible when it falls inside the working day, is free on both
    calendars, and satisfies every hard constraint.

    Args:
        scheduled_meeting: The meeting the assistant scheduled, or None.
        assistant_calendar: The principal's calendar before the new meeting.
        requestor_calendar: The requestor's calendar before the new meeting.
        duration_minutes: Required meeting duration.
        hard_constraints: Predicates every acceptable slot must satisfy.
        soft_preferences: Weighted, named preferences used to rank slots.
        has_conflicts: Whether task completion detected calendar conflicts.
            The calendars here predate the new meeting, so conflicts the
            assistant introduced itself are only visible via this flag.
        day_start: Earliest a meeting may begin.
        day_end: Latest a meeting may end.
        step_minutes: Spacing of the regular sweep. Affects how many slots the
            explanation lists, not the score.

    Returns:
        A PreferenceAdherenceResult with both scores and the slot analysis.
    """
    hard_constraints = hard_constraints or []
    soft_preferences = soft_preferences or []

    assistant_busy = _busy_intervals(assistant_calendar)
    requestor_busy = _busy_intervals(requestor_calendar)

    def is_acceptable(start: int, end: int) -> bool:
        return (
            _is_free(start, end, assistant_busy)
            and _is_free(start, end, requestor_busy)
            and all(check(start, end) for check in hard_constraints)
        )

    feasible = [
        start
        for start in _candidate_starts(
            day_start,
            day_end,
            duration_minutes,
            step_minutes,
            busy=assistant_busy + requestor_busy,
            constraints=hard_constraints + [p.predicate for p in soft_preferences],
        )
        if is_acceptable(start, start + duration_minutes)
    ]
    feasible_hhmm = [to_hhmm(start) for start in feasible]

    if scheduled_meeting is None:
        declined_correctly = not feasible
        return PreferenceAdherenceResult(
            hard_constraints_satisfied=declined_correctly,
            soft_constraints_score=1.0 if declined_correctly else 0.0,
            feasible_slots=feasible_hhmm,
            explanation=(
                "No slot is both available and allowed; correctly declined to schedule."
                if declined_correctly
                else f"Nothing was scheduled even though {len(feasible)} slot(s) were "
                f"available: {', '.join(feasible_hhmm)}."
            ),
        )

    chosen_start = to_minutes(scheduled_meeting.start_time)
    chosen_end = to_minutes(scheduled_meeting.end_time)
    chosen_hhmm = to_hhmm(chosen_start)

    if not feasible:
        return PreferenceAdherenceResult(
            hard_constraints_satisfied=False,
            soft_constraints_score=0.0,
            chosen_slot=chosen_hhmm,
            explanation=(
                f"No slot is both available and allowed, but a meeting was "
                f"scheduled at {chosen_hhmm} instead of declining."
            ),
        )

    def rejection_reason() -> str | None:
        if has_conflicts:
            return f"Scheduled at {chosen_hhmm}, but the final calendar has a conflict."
        if chosen_end - chosen_start != duration_minutes:
            return (
                f"Scheduled at {chosen_hhmm} for {chosen_end - chosen_start} minutes "
                f"instead of the required {duration_minutes}."
            )
        if chosen_start < to_minutes(day_start) or chosen_end > to_minutes(day_end):
            return f"Scheduled at {chosen_hhmm}, outside the {day_start}-{day_end} day."
        if not is_acceptable(chosen_start, chosen_end):
            return f"Scheduled at {chosen_hhmm}, which is busy or violates a hard constraint."
        return None

    reason = rejection_reason()
    if reason is not None:
        return PreferenceAdherenceResult(
            hard_constraints_satisfied=False,
            soft_constraints_score=0.0,
            feasible_slots=feasible_hhmm,
            chosen_slot=chosen_hhmm,
            explanation=f"{reason} Feasible slots: {', '.join(feasible_hhmm)}.",
        )

    weights = {
        start: _weight_of(start, start + duration_minutes, soft_preferences) for start in feasible
    }
    best_weight = max(weight for weight, _ in weights.values())
    best_slots = [to_hhmm(start) for start, (weight, _) in weights.items() if weight == best_weight]

    chosen_weight, chosen_satisfied = _weight_of(chosen_start, chosen_end, soft_preferences)

    # A feasible slot always ties one of the candidates, so this cannot exceed
    # 1. If it ever does, the bounded result field raises rather than hiding it.
    soft_score = 1.0 if best_weight == 0.0 else chosen_weight / best_weight

    # Name one concrete alternative rather than a mix of mutually exclusive
    # ones. A slot tying the best weight forwent nothing.
    missed: list[str] = []
    if chosen_weight < best_weight:
        earliest_best = next(start for start in feasible if weights[start][0] == best_weight)
        _, reference_satisfied = weights[earliest_best]
        missed = [name for name in reference_satisfied if name not in chosen_satisfied]

    return PreferenceAdherenceResult(
        hard_constraints_satisfied=True,
        soft_constraints_score=soft_score,
        feasible_slots=feasible_hhmm,
        best_slots=best_slots,
        chosen_slot=chosen_hhmm,
        satisfied_soft_constraints=chosen_satisfied,
        missed_soft_constraints=missed,
        explanation=(
            f"Scheduled at {chosen_hhmm} (soft weight {chosen_weight:g} of best "
            f"{best_weight:g} at {', '.join(best_slots)}); soft score {soft_score:.3f}."
        ),
    )
