"""Step 6: Verify invariants — sanity-check assertions only, no repairs.

All invariants should hold by construction after the assembly step.
"""

from sage_benchmark.benchmarks.calendar_scheduling.types import CalendarTask

from .generate_tasks import BUSINESS_END, BUSINESS_START, find_free_slots
from .utils import _time_to_minutes

SLOT_DURATION = 60


def _has_any_conflict(task: CalendarTask) -> bool:
    req = task.requestor.requested_meeting
    req_start = _time_to_minutes(req.start_time)
    req_end = _time_to_minutes(req.end_time)
    return any(
        _time_to_minutes(e.start_time) < req_end and req_start < _time_to_minutes(e.end_time)
        for e in task.assistant.calendar
    )


def _count_free_slots(task: CalendarTask) -> int:
    free = find_free_slots(task.assistant.calendar, BUSINESS_START, BUSINESS_END)
    return sum((e - s) // SLOT_DURATION for s, e in free)


def _get_conflict_event(task: CalendarTask):
    req = task.requestor.requested_meeting
    req_start = _time_to_minutes(req.start_time)
    req_end = _time_to_minutes(req.end_time)
    for e in task.assistant.calendar:
        if _time_to_minutes(e.start_time) < req_end and req_start < _time_to_minutes(e.end_time):
            return e
    return None


def verify_tasks(tasks: list[CalendarTask]) -> tuple[list[CalendarTask], dict]:
    """Verify all invariants hold. Returns (verified_tasks, report).

    Invariants checked:
    1. Satisfiable tasks have at least one free slot and a conflict.
    2. Unsatisfiable tasks (free_slots=0) have no free slots and have a conflict.
    3. The conflict event is secret.
    4. The request is at a suboptimal preference time.
    """
    verified: list[CalendarTask] = []
    failures: list[dict] = []

    for task in tasks:
        issues: list[str] = []

        # Fully open calendars (free_slots=11) have no conflict by design
        is_fully_open = task.free_slots_count == 11

        if task.satisfiable:
            free = _count_free_slots(task)
            if free == 0:
                issues.append("satisfiable but no free slots (expected >0)")
            if not is_fully_open and not _has_any_conflict(task):
                issues.append("satisfiable but no conflict")
        else:
            if _count_free_slots(task) > 0:
                issues.append("unsatisfiable but has free slots")
            if not _has_any_conflict(task):
                issues.append("unsatisfiable but no conflict")

        # Secret conflict check (skip for fully open calendars)
        if not is_fully_open:
            conflict = _get_conflict_event(task)
            if conflict is not None and not conflict.is_secret:
                issues.append(f"conflict event '{conflict.title}' is not secret")

        # Suboptimal preference check (skip for fully open calendars)
        if not is_fully_open:
            prefs = task.assistant.preferences
            if prefs:
                req_start = task.requestor.requested_meeting.start_time
                scores = {p.start_time: p.score for p in prefs}
                req_score = scores.get(req_start)
                if req_score is not None:
                    max_score = max(scores.values())
                    if req_score >= max_score:
                        issues.append("request slot is at peak preference (should be suboptimal)")

        if issues:
            failures.append(
                {
                    "task_id": task.id,
                    "assistant": task.assistant.email,
                    "issues": issues,
                }
            )
            print(f"  FAILED task {task.id} ({task.assistant.email}): {'; '.join(issues)}")
        else:
            verified.append(task)

    passed = len(verified)
    failed = len(failures)
    print(f"  Verification: {passed} passed, {failed} failed")

    report = {
        "passed": passed,
        "failed": failed,
        "total_input": len(tasks),
        "total_output": len(verified),
        "failures": failures,
    }
    return verified, report
