from sage_benchmark.calendar_scheduling.types import TimeSlotPreference

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

# Morning preferrer: peaks 09:00–10:00
MORNING_PROFILE: dict[str, float] = {
    "08:00": 0.6,
    "09:00": 0.9,
    "10:00": 0.9,
    "11:00": 0.6,
    "12:00": 0.2,
    "13:00": 0.4,
    "14:00": 0.2,
    "15:00": 0.2,
    "16:00": 0.2,
    "17:00": 0.2,
    "18:00": 0.2,
}

# Afternoon preferrer: peaks 14:00–15:00
AFTERNOON_PROFILE: dict[str, float] = {
    "08:00": 0.2,
    "09:00": 0.2,
    "10:00": 0.2,
    "11:00": 0.2,
    "12:00": 0.4,
    "13:00": 0.6,
    "14:00": 0.9,
    "15:00": 0.9,
    "16:00": 0.6,
    "17:00": 0.6,
    "18:00": 0.4,
}

PROFILES = {"morning": MORNING_PROFILE, "afternoon": AFTERNOON_PROFILE}


def sample_preferences(
    profile: str = "morning",
    time_windows: list[tuple[str, str]] | None = None,
) -> list[TimeSlotPreference]:
    """Return scheduling preferences from a canonical morning or afternoon profile.

    Scores use four discrete values that map cleanly to agent-visible text buckets:
      0.9 → "Strongly prefer", 0.6 → "Prefer",
      0.4 → "Acceptable but not ideal", 0.2 → "Avoid if possible"

    The suboptimal guarantee (request slot is never peak) is enforced structurally
    at generation time by selecting the conflict slot from non-peak slots only.

    Args:
        profile: "morning" or "afternoon" archetype.
        time_windows: Override slot windows (defaults to 11 one-hour working slots).
    """
    windows = time_windows or DEFAULT_TIME_WINDOWS
    base_scores = PROFILES.get(profile, MORNING_PROFILE)
    return [
        TimeSlotPreference(start_time=start, end_time=end, score=base_scores.get(start, 0.2))
        for start, end in windows
    ]
