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

# Canonical scores map directly to agent-visible buckets:
#   0.9 → "Strongly prefer"  (>= 0.8)
#   0.6 → "Prefer"           (>= 0.5)
#   0.4 → "Acceptable"       (>= 0.3)
#   0.2 → "Avoid if possible" (< 0.3)
SCORE_BUCKETS = [0.9, 0.6, 0.4, 0.2]


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
            # Overlapping if event doesn't end before slot starts and doesn't start after slot ends
            if ev_start < we_m and ev_end > ws_m:
                occupied.add(i)

    return set(range(len(windows))) - occupied


def sample_preferences(
    calendar: list[LabeledMeeting] | None = None,
    rng: random.Random | None = None,
    time_windows: list[tuple[str, str]] | None = None,
) -> list[TimeSlotPreference]:
    """Generate random scheduling preferences, weighting free slots higher.

    Free slots (no calendar conflicts) are assigned scores from the top buckets
    (0.9, 0.6) with higher probability. Occupied slots get low scores (0.2, 0.4).
    This ensures preferences naturally reflect calendar availability while still
    being random and varied across tasks.

    Args:
        calendar: The agent's calendar events. If None, all slots are treated as free.
        rng: Random number generator for reproducibility.
        time_windows: Override slot windows (defaults to 11 one-hour working slots).

    Returns:
        List of TimeSlotPreference objects, one per time window.
    """
    rng = rng or random.Random()
    windows = time_windows or DEFAULT_TIME_WINDOWS

    free_indices = (
        get_free_slot_indices(calendar, windows) if calendar else set(range(len(windows)))
    )

    prefs = []
    for i, (start, end) in enumerate(windows):
        if i in free_indices:
            # Free slots: weighted toward high scores
            score = rng.choices(SCORE_BUCKETS, weights=[4, 3, 2, 1])[0]
        else:
            # Occupied slots: always low
            score = rng.choices([0.2, 0.4], weights=[3, 1])[0]
        prefs.append(TimeSlotPreference(start_time=start, end_time=end, score=score))

    return prefs
