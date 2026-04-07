"""Step 5: Deterministic assembly — fullness assignment, meeting placement, calendar trimming.

No LLM calls. All randomness is seeded.
"""

import random

from pydantic import ConfigDict
from sage_benchmark.benchmarks.calendar_scheduling.types import CalendarTask, LabeledMeeting

from .archetypes import NUM_ARCHETYPES
from .generate_calendars import AFTERNOON_SLOT_INDICES, MORNING_SLOT_INDICES
from .generate_preferences import sample_preferences
from .utils import _time_to_minutes

NUM_WORKING_SLOTS = 11


class MutableCalendarTask(CalendarTask):
    """Mutable variant of CalendarTask for use during assembly."""

    model_config = ConfigDict(frozen=False)


def assign_fullness_levels(
    employee_tasks: list[CalendarTask],
    fullness_levels: list[int],
    rng: random.Random,
) -> list[tuple[CalendarTask, int]]:
    """Randomly (seeded) assign each of an employee's 7 tasks to a fullness level.

    Args:
        employee_tasks: The employee's 7 tasks, one per archetype.
        fullness_levels: The 7 fullness levels to assign.
        rng: Seeded random instance for deterministic shuffling.

    Returns:
        List of (task, fullness_level) pairs.
    """
    assert len(employee_tasks) == NUM_ARCHETYPES == len(fullness_levels)
    shuffled_levels = list(fullness_levels)
    rng.shuffle(shuffled_levels)
    return list(zip(employee_tasks, shuffled_levels))


def pick_conflict_slot(task: CalendarTask, rng: random.Random) -> int | None:
    """Pick a conflict slot: randomly select from secret events on the assistant's calendar.

    Args:
        task: The calendar task containing the assistant's calendar.
        rng: Seeded random instance for deterministic selection.

    Returns:
        The working-slot index (0-10) or None if no secret event exists.
    """
    secret_slots = [
        _slot_index_for_time(event.start_time)
        for event in task.assistant.calendar
        if event.is_secret and "sleep" not in event.uid and "personal" not in event.uid
    ]
    if not secret_slots:
        return None
    return rng.choice(secret_slots)


def _slot_index_for_time(start_time: str) -> int:
    """Map a start_time like '09:00' to working slot index 0-10.

    Args:
        start_time: Time string in HH:MM format (e.g. '09:00').

    Returns:
        Integer slot index from 0 (08:00) to 10 (18:00).
    """
    minutes = _time_to_minutes(start_time)
    return (minutes - 8 * 60) // 60


def place_meeting(task: MutableCalendarTask, conflict_slot_index: int) -> None:
    """Set the requested meeting time to the conflict slot.

    Args:
        task: Mutable calendar task whose meeting time will be updated.
        conflict_slot_index: Working-slot index (0-10) for the conflict.
    """
    hour = 8 + conflict_slot_index
    start = f"{hour:02d}:00"
    end = f"{hour + 1:02d}:00"
    task.requestor.requested_meeting.start_time = start
    task.requestor.requested_meeting.end_time = end


def _get_occupied_slot_indices(calendar: list[LabeledMeeting]) -> set[int]:
    """Return the set of working-slot indices (0-10) that have events.

    Args:
        calendar: List of labeled meetings to inspect.

    Returns:
        Set of occupied working-slot indices, excluding sleep and personal blocks.
    """
    occupied: set[int] = set()
    for event in calendar:
        if "sleep" in event.uid or "personal" in event.uid:
            continue
        occupied.add(_slot_index_for_time(event.start_time))
    return occupied


def _get_free_slot_indices(calendar: list[LabeledMeeting]) -> set[int]:
    """Return the set of working-slot indices (0-10) that are free.

    Args:
        calendar: List of labeled meetings to inspect.

    Returns:
        Set of free working-slot indices (complement of occupied slots).
    """
    return set(range(NUM_WORKING_SLOTS)) - _get_occupied_slot_indices(calendar)


def trim_calendar_events(
    calendar: list[LabeledMeeting],
    target_free_slots: int,
    protected_slot_index: int,
    rng: random.Random,
) -> list[LabeledMeeting]:
    """Remove events from a calendar to achieve the target free-slot count.

    Preserves the protected slot (conflict event).

    Args:
        calendar: Full calendar of labeled meetings to trim.
        target_free_slots: Desired number of free working-hour slots.
        protected_slot_index: Slot index that must not be removed (conflict event).
        rng: Seeded random instance for deterministic slot removal.

    Returns:
        Trimmed calendar sorted by start time.
    """
    # Identify working-hour events and non-working events
    working_events: list[tuple[int, LabeledMeeting]] = []
    non_working: list[LabeledMeeting] = []

    for event in calendar:
        if "sleep" in event.uid or "personal" in event.uid:
            non_working.append(event)
        else:
            idx = _slot_index_for_time(event.start_time)
            working_events.append((idx, event))

    # Available slots to remove (not the protected slot)
    removable_indices = [i for i, _ in working_events if i != protected_slot_index]

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

    # Rebuild calendar: non-working + kept working, sorted by time
    all_events = non_working + kept_working
    all_events.sort(key=lambda e: _time_to_minutes(e.start_time))
    return all_events


def trim_requestor_calendar(
    requestor_calendar: list[LabeledMeeting],
    requestor_fullness: int,
    assistant_free_slots: set[int],
    rng: random.Random,
) -> list[LabeledMeeting]:
    """Trim the requestor's calendar ensuring at least 1 overlapping free slot.

    Guarantees that after trimming, at least one working-hour slot is free in
    both the requestor's and assistant's calendars.

    Args:
        requestor_calendar: The requestor's full calendar of labeled meetings.
        requestor_fullness: Target number of free working-hour slots.
        assistant_free_slots: Set of slot indices already free in the assistant's calendar.
        rng: Seeded random instance for deterministic slot removal.

    Returns:
        Trimmed requestor calendar sorted by start time.
    """
    occupied = _get_occupied_slot_indices(requestor_calendar)

    # Find slots that are occupied in the requestor's calendar AND free in the assistant's.
    # Freeing one of these creates an overlap.
    overlap_candidates = list(occupied & assistant_free_slots)

    # If there's already an overlap (requestor slot free where assistant is also free),
    # just do a normal trim with no protected slot.
    current_requestor_free = set(range(NUM_WORKING_SLOTS)) - occupied
    existing_overlap = current_requestor_free & assistant_free_slots
    if existing_overlap or not overlap_candidates:
        # Either overlap already exists, or we can't force one (shouldn't happen
        # since assistant_free_slots is non-empty and requestor is fully packed)
        return trim_calendar_events(requestor_calendar, requestor_fullness, -1, rng)

    # Force one overlap: pick a slot that's occupied in requestor but free in assistant.
    # We'll ensure this slot gets freed by marking it for removal first,
    # then trimming the rest normally.
    forced_slot = rng.choice(overlap_candidates)

    # Remove the forced slot event and then trim remaining to target
    remaining_to_free = requestor_fullness - 1
    if remaining_to_free <= 0:
        # Only need to free 1 slot — the forced one
        return trim_calendar_events(requestor_calendar, 1, -1, rng)

    # Remove the forced slot, then trim the rest (protecting nothing else)
    working_events: list[tuple[int, LabeledMeeting]] = []
    non_working: list[LabeledMeeting] = []
    for event in requestor_calendar:
        if "sleep" in event.uid or "personal" in event.uid:
            non_working.append(event)
        else:
            idx = _slot_index_for_time(event.start_time)
            working_events.append((idx, event))

    # Remove the forced slot plus additional random slots
    removable_indices = [i for i, _ in working_events if i != forced_slot]
    morning_removable = [i for i in removable_indices if i in MORNING_SLOT_INDICES]
    afternoon_removable = [i for i in removable_indices if i in AFTERNOON_SLOT_INDICES]

    morning_free = round(
        remaining_to_free * len(morning_removable) / max(len(removable_indices), 1)
    )
    afternoon_free = remaining_to_free - morning_free
    morning_free = min(morning_free, len(morning_removable))
    afternoon_free = min(afternoon_free, len(afternoon_removable))

    while morning_free + afternoon_free < remaining_to_free:
        if afternoon_free < len(afternoon_removable):
            afternoon_free += 1
        elif morning_free < len(morning_removable):
            morning_free += 1
        else:
            break
    while morning_free + afternoon_free > remaining_to_free:
        if morning_free > 0:
            morning_free -= 1
        elif afternoon_free > 0:
            afternoon_free -= 1

    slots_to_remove: set[int] = {forced_slot}
    if morning_free > 0:
        slots_to_remove.update(rng.sample(morning_removable, morning_free))
    if afternoon_free > 0:
        slots_to_remove.update(rng.sample(afternoon_removable, afternoon_free))

    kept_working = [event for idx, event in working_events if idx not in slots_to_remove]
    all_events = non_working + kept_working
    all_events.sort(key=lambda e: _time_to_minutes(e.start_time))
    return all_events


def assemble_tasks(
    all_employee_tasks: dict[str, list[CalendarTask]],
    fullness_levels: list[int],
    requestor_fullness: int,
    seed: int,
) -> list[CalendarTask]:
    """Step 5: Assign fullness, place meetings, trim both calendars, ensure overlap.

    All fullness levels must be in [1, 10] — no unsatisfiable (0) or fully open (11)
    calendars. The requestor's calendar is trimmed to a fixed fullness level, and at
    least 1 working-hour slot is guaranteed to be free in both calendars.

    Args:
        all_employee_tasks: Maps employee email to their 7 validated tasks (one per archetype).
        fullness_levels: The 7 fullness levels to distribute (all in [1, 10]).
        requestor_fullness: Fixed number of free slots for all requestor calendars.
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
            mt = MutableCalendarTask.model_validate(task.model_dump(mode="json"))
            mt.free_slots_count = num_free_slots
            mt.satisfiable = True

            # 5b: Pick conflict slot and place meeting
            conflict_rng = random.Random(seed + hash(email) + num_free_slots + 4000)
            conflict_slot = pick_conflict_slot(mt, conflict_rng)
            if conflict_slot is None:
                print(f"  Warning: no valid conflict slot for {email}, skipping task")
                continue

            place_meeting(mt, conflict_slot)

            # 5c: Trim assistant calendar
            level_rng = random.Random(seed + hash(email) + num_free_slots)
            mt.assistant.calendar = trim_calendar_events(
                mt.assistant.calendar, num_free_slots, conflict_slot, level_rng
            )

            # 5d: Trim requestor calendar with overlap guarantee
            assistant_free = _get_free_slot_indices(mt.assistant.calendar)
            req_rng = random.Random(seed + hash(email) + num_free_slots + 1000)
            mt.requestor.calendar = trim_requestor_calendar(
                mt.requestor.calendar, requestor_fullness, assistant_free, req_rng
            )

            # 5e: Generate preferences based on final trimmed calendars
            asst_pref_rng = random.Random(seed + hash(email) + num_free_slots + 2000)
            mt.assistant.preferences = sample_preferences(
                calendar=mt.assistant.calendar, rng=asst_pref_rng
            )
            req_pref_rng = random.Random(seed + hash(email) + num_free_slots + 3000)
            mt.requestor.preferences = sample_preferences(
                calendar=mt.requestor.calendar, rng=req_pref_rng
            )

            assembled.append(CalendarTask.model_validate(mt))

    return assembled
