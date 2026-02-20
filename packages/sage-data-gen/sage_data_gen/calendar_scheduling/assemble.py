"""Step 5: Deterministic assembly — fullness assignment, meeting placement, calendar trimming.

No LLM calls. All randomness is seeded.
"""

import random

from sage_benchmark.calendar_scheduling.types import CalendarTask, LabeledMeeting

from .archetypes import NUM_ARCHETYPES
from .generate_calendars import AFTERNOON_SLOT_INDICES, MORNING_SLOT_INDICES
from .generate_preferences import PROFILES
from .utils import _time_to_minutes


def assign_fullness_levels(
    employee_tasks: list[CalendarTask],
    fullness_levels: list[int],
    rng: random.Random,
) -> list[tuple[CalendarTask, int]]:
    """Randomly (seeded) assign each of an employee's 7 tasks to a fullness level.

    Returns list of (task, fullness_level) pairs.
    """
    assert len(employee_tasks) == NUM_ARCHETYPES == len(fullness_levels)
    shuffled_levels = list(fullness_levels)
    rng.shuffle(shuffled_levels)
    return list(zip(employee_tasks, shuffled_levels))


def pick_conflict_slot(task: CalendarTask) -> int | None:
    """Pick a conflict slot: a secret event at a suboptimal preference time.

    Returns the working-slot index (0-10) or None if no valid slot exists.
    """
    prefs = task.assistant.preferences
    if not prefs:
        return None

    scores = {p.start_time: p.score for p in prefs}
    peak_score = max(scores.values())

    # Walk the working-hour events in the calendar (skip sleep/personal)
    for event in task.assistant.calendar:
        if "sleep" in event.uid or "personal" in event.uid:
            continue
        if not event.is_secret:
            continue
        slot_score = scores.get(event.start_time, 0)
        if slot_score < peak_score:
            return _slot_index_for_time(event.start_time)

    return None


def _slot_index_for_time(start_time: str) -> int:
    """Map a start_time like '09:00' to working slot index 0-10."""
    minutes = _time_to_minutes(start_time)
    return (minutes - 8 * 60) // 60


def pick_suboptimal_slot(task: CalendarTask, rng: random.Random) -> int:
    """Pick any working-hour slot that is NOT at peak preference score.

    Used for fullness=11 tasks where there are no calendar events to conflict with,
    but the meeting must still be placed at a suboptimal time.
    """
    prefs = task.assistant.preferences
    if not prefs:
        return 0

    scores = {p.start_time: p.score for p in prefs}
    peak_score = max(scores.values())

    suboptimal_indices = []
    for i in range(11):
        hour = 8 + i
        start = f"{hour:02d}:00"
        if scores.get(start, 0) < peak_score:
            suboptimal_indices.append(i)

    if not suboptimal_indices:
        return 0

    return rng.choice(suboptimal_indices)


def place_meeting(task: CalendarTask, conflict_slot_index: int) -> None:
    """Set the requested meeting time to the conflict slot."""
    hour = 8 + conflict_slot_index
    start = f"{hour:02d}:00"
    end = f"{hour + 1:02d}:00"
    task.requestor.requested_meeting.start_time = start
    task.requestor.requested_meeting.end_time = end


def trim_calendar(
    task: CalendarTask,
    target_free_slots: int,
    conflict_slot_index: int,
    rng: random.Random,
) -> None:
    """Remove events to achieve the target free-slot count. Preserves conflict event."""
    if target_free_slots == 0:
        return

    if target_free_slots == 11:
        task.assistant.calendar = [
            e for e in task.assistant.calendar if "sleep" in e.uid or "personal" in e.uid
        ]
        return

    # Identify working-hour events and which to keep
    working_events: list[tuple[int, LabeledMeeting]] = []
    non_working: list[LabeledMeeting] = []

    for event in task.assistant.calendar:
        if "sleep" in event.uid or "personal" in event.uid:
            non_working.append(event)
        else:
            idx = _slot_index_for_time(event.start_time)
            working_events.append((idx, event))

    # Available slots to remove (not the conflict slot)
    removable_indices = [i for i, _ in working_events if i != conflict_slot_index]

    # Proportional morning/afternoon distribution
    morning_removable = [i for i in removable_indices if i in MORNING_SLOT_INDICES]
    afternoon_removable = [i for i in removable_indices if i in AFTERNOON_SLOT_INDICES]

    morning_free = round(
        target_free_slots * len(morning_removable) / max(len(removable_indices), 1)
    )
    afternoon_free = target_free_slots - morning_free

    morning_free = min(morning_free, len(morning_removable))
    afternoon_free = min(afternoon_free, len(afternoon_removable))

    while morning_free + afternoon_free < target_free_slots:
        if afternoon_free < len(afternoon_removable):
            afternoon_free += 1
        elif morning_free < len(morning_removable):
            morning_free += 1
        else:
            break
    while morning_free + afternoon_free > target_free_slots:
        if morning_free > 0:
            morning_free -= 1
        elif afternoon_free > 0:
            afternoon_free -= 1

    slots_to_remove: set[int] = set()
    if morning_free > 0:
        slots_to_remove.update(rng.sample(morning_removable, morning_free))
    if afternoon_free > 0:
        slots_to_remove.update(rng.sample(afternoon_removable, afternoon_free))

    kept_working = [event for idx, event in working_events if idx not in slots_to_remove]

    # Rebuild calendar: sleep + kept working + personal, sorted by time
    all_events = non_working + kept_working
    all_events.sort(key=lambda e: _time_to_minutes(e.start_time))
    task.assistant.calendar = all_events


def assemble_tasks(
    all_employee_tasks: dict[str, list[CalendarTask]],
    fullness_levels: list[int],
    seed: int,
) -> list[CalendarTask]:
    """Step 5: Assign fullness, place meetings, trim calendars.

    Args:
        all_employee_tasks: Maps employee email to their 7 validated tasks (one per archetype).
        fullness_levels: The 7 fullness levels to distribute.
        seed: Random seed for deterministic assembly.

    Returns:
        All assembled tasks, ready for verification.
    """
    assembled: list[CalendarTask] = []

    for email, tasks in all_employee_tasks.items():
        rng = random.Random(seed + hash(email))

        # 5a: Assign fullness levels
        task_level_pairs = assign_fullness_levels(tasks, fullness_levels, rng)

        for task, num_free_slots in task_level_pairs:
            task.free_slots_count = num_free_slots
            task.satisfiable = num_free_slots > 0

            if num_free_slots == 11:
                # Fully open calendar: no conflict, just place at a suboptimal time
                level_rng = random.Random(seed + hash(email) + num_free_slots)
                suboptimal_slot = pick_suboptimal_slot(task, level_rng)
                place_meeting(task, suboptimal_slot)
                trim_calendar(task, num_free_slots, -1, level_rng)
                assembled.append(task)
                continue

            # 5b: Pick conflict slot and place meeting
            conflict_slot = pick_conflict_slot(task)
            if conflict_slot is None:
                print(f"  Warning: no valid conflict slot for {email}, skipping task")
                continue

            place_meeting(task, conflict_slot)

            # 5c: Trim calendar
            level_rng = random.Random(seed + hash(email) + num_free_slots)
            trim_calendar(task, num_free_slots, conflict_slot, level_rng)

            assembled.append(task)

    return assembled
