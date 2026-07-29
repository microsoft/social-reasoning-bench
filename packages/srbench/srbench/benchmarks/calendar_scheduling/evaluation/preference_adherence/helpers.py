"""Building blocks for per-task preference verifiers.

A task's preference document is hand-translated into hard constraints, which
every acceptable slot must satisfy, and weighted soft preferences, which rank
the acceptable slots. This module provides the vocabulary for writing both, and
the search that finds the slots they are evaluated over.

Times are ``"HH:MM"`` strings externally and minutes from midnight internally.
"""

from collections.abc import Callable
from dataclasses import dataclass

from ...types import LabeledMeeting

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


def starts_within(start: str, end: str) -> Predicate:
    """Build a predicate requiring the slot to begin inside ``[start, end)``.

    This constrains only where the meeting begins, unlike :func:`within`, which
    requires the whole meeting to fit. Use it for a preferred time of day that a
    long meeting is allowed to run past, such as "first thing in the morning".
    """
    lower, upper = to_minutes(start), to_minutes(end)
    return lambda slot_start, _slot_end: lower <= slot_start < upper


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
