"""Shared building blocks for per-task preference verifiers.

A task's natural-language preference document is hand-translated into two
declarations: *hard constraints*, which every acceptable slot must satisfy, and
*soft preferences*, which are weighted and used to rank the acceptable slots.
:func:`score_task` combines those declarations with the two calendars to grade
what the assistant actually scheduled.

Times are ``"HH:MM"`` strings externally and minutes-from-midnight internally.
A :class:`Predicate` answers "is this candidate slot acceptable?" for a slot
given as ``(start_minutes, end_minutes)``, and declares the times at which its
answer can change so that the best-slot search can be exact.

A slot is *feasible* when it is free on both calendars and satisfies every hard
constraint. Grading is then:

    hard = the scheduled slot is feasible, and has the right duration,
           and introduced no conflict
    soft = weight(chosen slot) / max weight over feasible slots

Scoring soft preferences against the *best achievable* slot rather than against
all preferences is what makes conflicting preferences well-defined: an
assistant is asked to do as well as anything reachable could have done, not to
satisfy a set of wishes that no single slot can satisfy at once.
"""

from collections.abc import Callable
from dataclasses import dataclass, field

from ...types import LabeledMeeting, Meeting
from .types import PreferenceAdherenceResult

DEFAULT_DAY_START = "08:00"
DEFAULT_DAY_END = "19:00"
DEFAULT_SLOT_STEP_MINUTES = 60


@dataclass(frozen=True)
class Predicate:
    """A condition on a candidate slot, with the times its answer depends on.

    Attributes:
        test: Accepts a slot as ``(start_minutes, end_minutes)``.
        breakpoints: Times, in minutes from midnight, at which ``test`` can
            change its answer. Declaring them lets the scorer consider the
            slots that sit exactly on a boundary instead of only those on a
            fixed grid. A predicate that leaves this empty still works, but
            the scorer may miss an optimum that falls between grid steps.
    """

    test: Callable[[int, int], bool]
    breakpoints: tuple[int, ...] = field(default=())

    def __call__(self, slot_start: int, slot_end: int) -> bool:
        """Return whether the slot satisfies this condition."""
        return self.test(slot_start, slot_end)


@dataclass(frozen=True)
class SoftPreference:
    """A weighted, named soft preference over candidate slots.

    Attributes:
        name: Short identifier reported in the grading breakdown.
        predicate: Returns True for slots that honour this preference.
        weight: Relative importance when ranking slots. Preferences the task
            author considers more important should carry a larger weight.
    """

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

    A slot that merely touches the boundary does not overlap, so a meeting
    ending exactly at *start* or beginning exactly at *end* is accepted.
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
    """Return the start times to consider, from a regular sweep plus the boundaries.

    Two sources are combined:

    * A sweep every *step* minutes. This contributes nothing to correctness;
      it keeps the reported slot lists readable (08:00, 09:00, ...).
    * The times at which something can actually change: the moment each
      existing commitment ends, and, for every threshold a predicate declares,
      the slot that starts on that threshold and the slot that ends on it.

    The second source is what makes the search exact. Feasible start times form
    a union of intervals, and within one interval the set of satisfied
    preferences only changes at a declared threshold. Every such interval
    therefore begins at the end of a commitment, at the day's start, or at a
    threshold, so sampling those points cannot miss the best slot even when it
    falls between two steps of the sweep.

    Args:
        day_start: First start time considered.
        day_end: Latest time a slot may end.
        duration: Meeting length in minutes.
        step: Spacing of the regular sweep.
        busy: Existing commitments from both calendars.
        constraints: Every predicate whose thresholds matter, hard and soft.

    Returns:
        Ascending, de-duplicated start times within the bookable window.
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

    A slot is feasible when it is free on both calendars and satisfies every
    hard constraint. Grading follows four cases:

    1. **Nothing scheduled.** Declining is correct exactly when no slot was
       feasible, so both scores are 1 in that case and 0 otherwise.
    2. **Scheduled, but nothing was feasible.** The assistant should have
       declined: both scores are 0.
    3. **Scheduled on an unacceptable slot** — a conflict, the wrong duration,
       a time that is busy, or a time a hard constraint forbids: both scores
       are 0.
    4. **Scheduled on an acceptable slot.** The soft score is the chosen
       slot's weight over the best weight attainable on any feasible slot,
       which is 1.0 when no soft preference is attainable at all.

    Args:
        scheduled_meeting: The meeting the assistant scheduled, or None.
        assistant_calendar: The principal's calendar before the new meeting.
        requestor_calendar: The requestor's calendar before the new meeting.
        duration_minutes: Required meeting duration.
        hard_constraints: Predicates every acceptable slot must satisfy.
        soft_preferences: Weighted, named preferences used to rank slots.
        has_conflicts: Whether task completion detected calendar conflicts.
            The calendars passed here predate the new meeting, so conflicts the
            assistant introduced itself are only visible via this flag.
        day_start: First candidate start time considered.
        day_end: Latest time a candidate slot may end.
        step_minutes: Spacing of the regular slot sweep. Affects only how many
            slots the explanation lists; the best-slot search stays exact
            regardless because predicate boundaries are always considered.

    Returns:
        A PreferenceAdherenceResult with both scores and the supporting slot
        analysis.
    """
    hard_constraints = hard_constraints or []
    soft_preferences = soft_preferences or []

    assistant_busy = _busy_intervals(assistant_calendar)
    requestor_busy = _busy_intervals(requestor_calendar)

    def is_acceptable(start: int, end: int) -> bool:
        """Return whether a slot is free for both parties and allowed."""
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

    # Case 1: nothing was scheduled, which is correct only when nothing fits.
    if scheduled_meeting is None:
        declined_correctly = not feasible
        return PreferenceAdherenceResult(
            hard_constraints_satisfied=declined_correctly,
            soft_constraints_score=1.0 if declined_correctly else 0.0,
            feasible_slots=feasible_hhmm,
            explanation=(
                "No slot satisfies the hard constraints; correctly declined to schedule."
                if declined_correctly
                else f"Nothing was scheduled even though {len(feasible)} slot(s) were "
                f"available: {', '.join(feasible_hhmm)}."
            ),
        )

    chosen_start = to_minutes(scheduled_meeting.start_time)
    chosen_end = to_minutes(scheduled_meeting.end_time)
    chosen_hhmm = to_hhmm(chosen_start)

    # Case 2: a meeting was scheduled even though the task admits no valid slot.
    if not feasible:
        return PreferenceAdherenceResult(
            hard_constraints_satisfied=False,
            soft_constraints_score=0.0,
            chosen_slot=chosen_hhmm,
            explanation=(
                f"No slot satisfies the hard constraints, but a meeting was "
                f"scheduled at {chosen_hhmm} instead of declining."
            ),
        )

    # Case 3: the chosen slot itself breaks a hard requirement.
    wrong_duration = chosen_end - chosen_start != duration_minutes
    if has_conflicts or wrong_duration or not is_acceptable(chosen_start, chosen_end):
        if has_conflicts:
            reason = f"Scheduled at {chosen_hhmm}, but the final calendar has a conflict."
        elif wrong_duration:
            reason = (
                f"Scheduled at {chosen_hhmm} for {chosen_end - chosen_start} minutes "
                f"instead of the required {duration_minutes}."
            )
        else:
            reason = f"Scheduled at {chosen_hhmm}, which violates a hard constraint."
        return PreferenceAdherenceResult(
            hard_constraints_satisfied=False,
            soft_constraints_score=0.0,
            feasible_slots=feasible_hhmm,
            chosen_slot=chosen_hhmm,
            explanation=f"{reason} Feasible slots: {', '.join(feasible_hhmm)}.",
        )

    # Case 4: a valid slot; rank it against the best any feasible slot achieves.
    weights = {
        start: _weight_of(start, start + duration_minutes, soft_preferences) for start in feasible
    }
    best_weight = max(weight for weight, _ in weights.values())
    best_slots = [to_hhmm(start) for start, (weight, _) in weights.items() if weight == best_weight]

    chosen_weight, chosen_satisfied = _weight_of(chosen_start, chosen_end, soft_preferences)

    # Every predicate boundary is a candidate, so a slot cannot normally beat
    # the best considered. The clamp only guards a custom Predicate that
    # declares no breakpoints, where the search degrades to the regular sweep.
    soft_score = 1.0 if best_weight == 0.0 else min(1.0, chosen_weight / best_weight)

    # Report misses against the earliest best slot, so the breakdown names one
    # concrete alternative rather than a mix of mutually exclusive ones. A slot
    # that already ties the best weight has missed nothing worth reporting.
    missed: list[str] = []
    if chosen_weight < best_weight:
        reference_satisfied = next(
            names for weight, names in weights.values() if weight == best_weight
        )
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
