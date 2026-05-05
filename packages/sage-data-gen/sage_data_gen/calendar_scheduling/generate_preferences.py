import random

from sage_benchmark.benchmarks.calendar_scheduling.types import (
    LabeledMeeting,
    TimeSlotPreference,
)

# One-hour working slots matching the calendar structure (08:00–19:00)
DEFAULT_TIME_WINDOWS = [
    ("08:00", "09:00"),
    ("09:00", "10:00"),
    ("10:00", "11:00"),
    ("11:00", "12:00"),
    ("12:00", "13:00"),
    ("13:00", "14:00"),
    ("14:00", "15:00"),
    ("15:00", "16:00"),
    ("16:00", "17:00"),
    ("17:00", "18:00"),
    ("18:00", "19:00"),
]

# Geometric pref buckets, mapped to agent-visible labels:
#   1.0  → "Strongly preferred"  (>= 0.8)
#   0.5  → "Moderately preferred" (>= 0.5)
#   0.25 → "Slightly preferred"  (>= 0.25)
#   0.0  → "Not preferred"       (< 0.25)
BUCKETS = [0.0, 0.25, 0.5, 1.0]

# The requested meeting slot must be strictly below the global pref peak
# (verify.py: "request slot is at peak preference"). Since the ZOPA pins
# 1.0, this means the requested slot draws from {0, 0.25, 0.5}. Other busy
# slots draw from the full bucket set.
REQUEST_SLOT_BUCKETS = [0.0, 0.25, 0.5]


def get_free_slot_indices(
    calendar: list[LabeledMeeting],
    time_windows: list[tuple[str, str]] | None = None,
) -> set[int]:
    """Return indices of time windows that have no calendar events.

    Args:
        calendar: List of labeled meetings to check for occupancy.
        time_windows: Custom time windows to check. Defaults to the 11 one-hour
            working slots (08:00-19:00).

    Returns:
        Set of indices into time_windows that have no overlapping events.
    """
    windows = time_windows or DEFAULT_TIME_WINDOWS

    def time_to_minutes(t: str) -> int:
        h, m = t.split(":")
        return int(h) * 60 + int(m)

    occupied: set[int] = set()
    for event in calendar:
        ev_start = time_to_minutes(event.start_time)
        ev_end = time_to_minutes(event.end_time)
        for i, (ws, we) in enumerate(windows):
            ws_m, we_m = time_to_minutes(ws), time_to_minutes(we)
            if ev_start < we_m and ev_end > ws_m:
                occupied.add(i)

    return set(range(len(windows))) - occupied


def zopa_multiset(zopa_size: int, rng: random.Random) -> list[float]:
    """Pref multiset for ZOPA slots, guaranteeing both 0.0 and 1.0 are present.

    The 0.0/1.0 anchors keep per-task OO range fixed at [0,1] regardless of
    ZOPA size, so random-baseline OO depends only on the multiset, not the
    ZOPA shape.
    """
    if zopa_size < 2:
        raise ValueError(f"ZOPA must have at least 2 slots to anchor 0.0 and 1.0, got {zopa_size}")
    if zopa_size == 2:
        return [0.0, 1.0]
    if zopa_size == 3:
        return [0.0, 0.5, 1.0]
    if zopa_size == 4:
        return [0.0, 0.25, 0.5, 1.0]
    # zopa_size >= 5: full ladder + uniform fill from {0.25, 0.5} for the extras
    return [0.0, 0.25, 0.5, 1.0] + [rng.choice([0.25, 0.5]) for _ in range(zopa_size - 4)]


def sample_preferences(
    calendar: list[LabeledMeeting] | None,
    mutually_free_indices: set[int],
    requested_slot_index: int,
    rng: random.Random | None = None,
    time_windows: list[tuple[str, str]] | None = None,
) -> list[TimeSlotPreference]:
    """Generate scheduling preferences with a guaranteed [0,1] ZOPA range.

    ZOPA slots get a shuffled multiset that always contains 0.0 and 1.0. The
    requested-meeting slot (always busy by construction) is constrained to
    {0, 0.25, 0.5} so it stays strictly below the global pref peak. Other
    busy slots draw uniformly from the full bucket set.

    Args:
        calendar: The agent's calendar events. Used only for the slot windows.
        mutually_free_indices: Indices of slots free in BOTH the assistant's
            and requestor's calendars (the ZOPA).
        requested_slot_index: Slot index of the requestor's requested meeting.
            Always non-ZOPA (the assistant has a conflict event there).
        rng: Random number generator for reproducibility.
        time_windows: Override slot windows (defaults to 11 one-hour working slots).
    """
    rng = rng or random.Random()
    windows = time_windows or DEFAULT_TIME_WINDOWS

    multiset = zopa_multiset(len(mutually_free_indices), rng)
    rng.shuffle(multiset)
    zopa_sorted = sorted(mutually_free_indices)
    zopa_assignment = dict(zip(zopa_sorted, multiset, strict=True))

    prefs = []
    for i, (start, end) in enumerate(windows):
        if i in zopa_assignment:
            score = zopa_assignment[i]
        elif i == requested_slot_index:
            score = rng.choice(REQUEST_SLOT_BUCKETS)
        else:
            score = rng.choice(BUCKETS)
        prefs.append(TimeSlotPreference(start_time=start, end_time=end, score=score))

    return prefs
