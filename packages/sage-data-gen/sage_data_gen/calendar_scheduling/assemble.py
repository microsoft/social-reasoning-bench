"""Step 5: Deterministic assembly — fullness assignment, meeting placement, calendar trimming.

No LLM calls. All randomness is seeded.
"""

import random

from pydantic import ConfigDict
from sage_benchmark.benchmarks.calendar_scheduling.types import (
    CalendarTask,
    LabeledMeeting,
    TimeSlotPreference,
)

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
    # Get working-hour occupied slots that are candidates to remove
    occupied_slots = _get_occupied_slot_indices(calendar)
    free_slots = _get_free_slot_indices(calendar)

    # How many occupied slots do we need to free up to meet the target?
    n_deficit_free_slots = target_free_slots - len(free_slots)
    # Need to free up some slots
    if n_deficit_free_slots > 0:
        # Remove the protected slot from the occupied slots so it doesn't get removed
        if protected_slot_index in occupied_slots:
            occupied_slots.remove(protected_slot_index)

        # rng.choice needs a list, not set
        candidate_slots_to_remove = list(occupied_slots)

        slots_to_remove: set[int] = set()
        for _ in range(n_deficit_free_slots):
            slot = rng.choice(candidate_slots_to_remove)
            candidate_slots_to_remove.remove(slot)
            slots_to_remove.add(slot)

        # Remove the events from the calendar
        calendar = [
            event
            for event in calendar
            if _slot_index_for_time(event.start_time) not in slots_to_remove
        ]

    # Ensure chronological
    calendar.sort(key=lambda event: _time_to_minutes(event.start_time))
    return calendar


def trim_requestor_calendar(
    requestor_calendar: list[LabeledMeeting],
    requestor_fullness: int,
    assistant_free_slots: set[int],
    rng: random.Random,
    min_mutual_free_slots: int,
) -> list[LabeledMeeting]:
    """Trim the requestor's calendar ensuring requestor_fullness AND at least min_mutual_free_slots overlapping free slots.

    Args:
        requestor_calendar: The requestor's full calendar of labeled meetings.
        requestor_fullness: Target number of free working-hour slots.
        assistant_free_slots: Set of slot indices already free in the assistant's calendar.
        rng: Seeded random instance for deterministic slot removal.
        min_mutual_free_slots: Minimum number of mutually free slots to guarantee.

    Returns:
        Trimmed requestor calendar sorted by start time.
    """
    # Get the occupied slots on the requestor calendar
    requestor_occupied_slots = _get_occupied_slot_indices(requestor_calendar)

    # Get the free working-hour slots on the requestor calendar
    requestor_free_slots = _get_free_slot_indices(requestor_calendar)

    # Find the slots where the requestor is occupied but the assistant is free.
    # Freeing up these slots on the requestor calendar would increase the number of "mutually free slots"
    requestor_occupied_assistant_free_slots = list(requestor_occupied_slots & assistant_free_slots)

    # Slots where requester and assistant are free
    mutually_free_slots = list(requestor_free_slots & assistant_free_slots)

    # Number of mutually free slots below the target min_mutual_free_slots
    n_deficit_mutually_free_slots = min_mutual_free_slots - len(mutually_free_slots)

    # There is a deficit, we need to remove requestor slots
    if n_deficit_mutually_free_slots > 0:
        # Track the slots we remove
        requestor_slots_to_remove: set[int] = set()

        # Queue n_deficit slots for removal
        for _ in range(n_deficit_mutually_free_slots):
            # Check if there are any more slots to free on the requestor calendar
            if not requestor_occupied_assistant_free_slots:
                raise RuntimeError("Cannot guarantee min_mutual_free_slots")

            # Randomly choose the slot to remove
            slot = rng.choice(requestor_occupied_assistant_free_slots)
            requestor_occupied_assistant_free_slots.remove(slot)

            requestor_slots_to_remove.add(slot)

        # Remove the events from the requestor calendar
        requestor_calendar = [
            event
            for event in requestor_calendar
            if _slot_index_for_time(event.start_time) not in requestor_slots_to_remove
        ]

    # Regardless of min_mutual_free_slots, we want to target a "fullness level" on the requestor calendar.
    requestor_calendar = trim_calendar_events(requestor_calendar, requestor_fullness, -1, rng)

    # Ensure chronological
    requestor_calendar.sort(key=lambda e: _time_to_minutes(e.start_time))
    return requestor_calendar


def assemble_tasks(
    all_employee_tasks: dict[str, list[CalendarTask]],
    fullness_levels: list[int],
    requestor_fullness: int,
    seed: int,
    min_mutual_free_slots: int,
) -> list[CalendarTask]:
    """Step 5: Assign fullness, place meetings, trim both calendars, ensure overlap.

    All fullness levels must be in [1, 10] — no unsatisfiable (0) or fully open (11)
    calendars. The requestor's calendar is trimmed to a fixed fullness level, and at
    least min_mutual_free_slots working-hour slots are guaranteed to be free in both calendars.

    Args:
        all_employee_tasks: Maps employee email to their 7 validated tasks (one per archetype).
        fullness_levels: The 7 fullness levels to distribute (all in [1, 10]).
        requestor_fullness: Fixed number of free slots for all requestor calendars.
        seed: Random seed for deterministic assembly.
        min_mutual_free_slots: Minimum number of mutually free slots to guarantee.

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
                mt.requestor.calendar,
                requestor_fullness,
                assistant_free,
                req_rng,
                min_mutual_free_slots,
            )

            # 5e: Generate preferences based on final trimmed calendars.
            # The mutually-free indices form the ZOPA — pref sampling pins
            # 0.0 and 1.0 there so per-task OO range is always [0, 1].
            asst_pref_rng = random.Random(seed + hash(email) + num_free_slots + 2000)
            requestor_free = _get_free_slot_indices(mt.requestor.calendar)
            assistant_free_post_trim = _get_free_slot_indices(mt.assistant.calendar)
            mutually_free_indices = assistant_free_post_trim & requestor_free
            mt.assistant.preferences = sample_preferences(
                calendar=mt.assistant.calendar,
                mutually_free_indices=mutually_free_indices,
                requested_slot_index=conflict_slot,
                rng=asst_pref_rng,
            )
            # Requestor preferences are the inverse of assistant preferences
            mt.requestor.preferences = [
                TimeSlotPreference(
                    start_time=p.start_time,
                    end_time=p.end_time,
                    score=round(1.0 - p.score, 2),
                )
                for p in mt.assistant.preferences
            ]

            assembled.append(CalendarTask.model_validate(mt))

    return assembled
