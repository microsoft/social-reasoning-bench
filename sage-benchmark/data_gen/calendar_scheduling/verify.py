import random

from sage_benchmark.calendar_scheduling.types import CalendarTask

from .generate_tasks import BUSINESS_END, BUSINESS_START, find_free_slots


def _time_to_minutes(t: str) -> int:
    h, m = t.split(":")
    return int(h) * 60 + int(m)


def _minutes_to_time(m: int) -> str:
    return f"{m // 60:02d}:{m % 60:02d}"


def _has_any_conflict(task: CalendarTask) -> bool:
    """Check if the requested meeting conflicts with at least one calendar event."""
    req = task.requestor.requested_meeting
    req_start = _time_to_minutes(req.start_time)
    req_end = _time_to_minutes(req.end_time)

    return any(
        _time_to_minutes(e.start_time) < req_end and req_start < _time_to_minutes(e.end_time)
        for e in task.assistant.calendar
    )


def _verify_satisfiable(task: CalendarTask) -> bool:
    """A satisfiable task must have a free gap available and conflict with something.

    The requested meeting can conflict with any event (movable or immovable).
    The key is that a free gap exists (considering only immovable events) where
    the meeting can be rescheduled.
    """
    if not _has_any_conflict(task):
        return False

    requested = task.requestor.requested_meeting
    duration = requested.duration_minutes

    # Check that a free gap exists (immovable-only) that fits the duration
    immovable = [m for m in task.assistant.calendar if not m.is_movable]
    free_slots = find_free_slots(immovable, BUSINESS_START, BUSINESS_END)

    for slot_start, slot_end in free_slots:
        if (slot_end - slot_start) >= duration:
            return True

    return False


def _verify_unsatisfiable(task: CalendarTask) -> bool:
    """An unsatisfiable task must have a conflict and no gap big enough for the duration."""
    if not _has_any_conflict(task):
        return False

    requested = task.requestor.requested_meeting
    duration = requested.duration_minutes

    immovable = [m for m in task.assistant.calendar if not m.is_movable]
    free_slots = find_free_slots(immovable, BUSINESS_START, BUSINESS_END)

    for slot_start, slot_end in free_slots:
        if (slot_end - slot_start) >= duration:
            return False
    return True


def _try_repair_satisfiable(task: CalendarTask) -> bool:
    """Repair a satisfiable task: ensure free gap exists and meeting conflicts with something."""
    requested = task.requestor.requested_meeting
    duration = requested.duration_minutes
    calendar = list(task.assistant.calendar)

    # Find free slots considering only immovable events
    immovable = [m for m in calendar if not m.is_movable]
    free_slots = find_free_slots(immovable, BUSINESS_START, BUSINESS_END)

    fitting_slots = [(s, e) for s, e in free_slots if (e - s) >= duration]
    if not fitting_slots:
        return False

    # Find a time that conflicts with at least one event
    bh_events = [
        m
        for m in calendar
        if _time_to_minutes(m.end_time) > BUSINESS_START
        and _time_to_minutes(m.start_time) < BUSINESS_END
    ]

    if not bh_events:
        # No events to conflict with, just use a free slot
        slot_start, _ = random.choice(fitting_slots)
        requested.start_time = _minutes_to_time(slot_start)
        requested.end_time = _minutes_to_time(slot_start + duration)
        return True

    random.shuffle(bh_events)
    for target in bh_events:
        ts = _time_to_minutes(target.start_time)
        meeting_end = ts + duration

        if meeting_end > BUSINESS_END:
            continue

        requested.start_time = _minutes_to_time(ts)
        requested.end_time = _minutes_to_time(meeting_end)
        return True

    return False


def _try_repair_unsatisfiable(task: CalendarTask) -> bool:
    """Adjust duration and placement so the task is truly unsatisfiable with a conflict."""
    immovable = [m for m in task.assistant.calendar if not m.is_movable]
    free_slots = find_free_slots(immovable, BUSINESS_START, BUSINESS_END)

    if not free_slots:
        return _has_any_conflict(task)

    max_gap = max(e - s for s, e in free_slots)
    new_duration = ((max_gap // 30) + 1) * 30
    if new_duration > 180:
        return False

    # Place overlapping an immovable event to guarantee conflict
    immovable_bh = [
        m
        for m in task.assistant.calendar
        if not m.is_movable
        and _time_to_minutes(m.end_time) > BUSINESS_START
        and _time_to_minutes(m.start_time) < BUSINESS_END
    ]
    if not immovable_bh:
        return False

    target = random.choice(immovable_bh)
    req_start = max(_time_to_minutes(target.start_time), BUSINESS_START)
    new_end = req_start + new_duration
    if new_end > BUSINESS_END:
        req_start = max(BUSINESS_START, BUSINESS_END - new_duration)
        new_end = req_start + new_duration
    if new_end > BUSINESS_END:
        return False

    requested = task.requestor.requested_meeting
    requested.start_time = _minutes_to_time(req_start)
    requested.end_time = _minutes_to_time(new_end)
    return True


def verify_and_repair(tasks: list[CalendarTask]) -> tuple[list[CalendarTask], dict]:
    verified: list[CalendarTask] = []
    repairs = 0
    drops = 0
    details: list[dict] = []

    for i, task in enumerate(tasks):
        if task.satisfiable:
            if _verify_satisfiable(task):
                verified.append(task)
                details.append({"task_id": i, "satisfiable": True, "action": "passed"})
            elif _try_repair_satisfiable(task):
                repairs += 1
                verified.append(task)
                details.append({"task_id": i, "satisfiable": True, "action": "repaired"})
            else:
                drops += 1
                details.append(
                    {
                        "task_id": i,
                        "satisfiable": True,
                        "action": "dropped",
                        "reason": "no movable event to conflict with",
                    }
                )
                print(f"  Dropped satisfiable task {i}: no movable event to conflict with")
        else:
            if _verify_unsatisfiable(task):
                verified.append(task)
                details.append({"task_id": i, "satisfiable": False, "action": "passed"})
            elif _try_repair_unsatisfiable(task):
                if _verify_unsatisfiable(task):
                    repairs += 1
                    verified.append(task)
                    details.append({"task_id": i, "satisfiable": False, "action": "repaired"})
                else:
                    drops += 1
                    details.append(
                        {
                            "task_id": i,
                            "satisfiable": False,
                            "action": "dropped",
                            "reason": "could not make truly unsatisfiable",
                        }
                    )
                    print(f"  Dropped unsatisfiable task {i}: could not make truly unsatisfiable")
            else:
                drops += 1
                details.append(
                    {
                        "task_id": i,
                        "satisfiable": False,
                        "action": "dropped",
                        "reason": "gap too large to block",
                    }
                )
                print(f"  Dropped unsatisfiable task {i}: gap too large to block")

    direct_pass = len(verified) - repairs
    print(f"  Verification: {direct_pass} passed, {repairs} repaired, {drops} dropped")

    report = {
        "passed": direct_pass,
        "repaired": repairs,
        "dropped": drops,
        "total_input": len(tasks),
        "total_output": len(verified),
        "details": details,
    }
    return verified, report
