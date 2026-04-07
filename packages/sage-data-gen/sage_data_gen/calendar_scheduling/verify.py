"""Step 6: Verify invariants — sanity-check assertions only, no repairs.

All invariants should hold by construction after the assembly step.
"""

from sage_benchmark.benchmarks.calendar_scheduling.types import CalendarTask

from .assemble import _get_free_slot_indices
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
    """Verify all invariants hold.

    Invariants checked:
    1. All tasks are satisfiable (no fullness=0).
    2. Satisfiable tasks have at least one free slot and a conflict.
    3. The conflict event is secret.
    4. The request is at a suboptimal preference time.
    5. The requestor has a non-empty calendar.
    6. At least 1 overlapping free slot between assistant and requestor calendars.

    Args:
        tasks: List of assembled calendar tasks to verify.

    Returns:
        Tuple of (verified_tasks, report) where verified_tasks contains only
        tasks that pass all checks and report is a dict with pass/fail counts
        and failure details.
    """
    verified: list[CalendarTask] = []
    failures: list[dict] = []

    for task in tasks:
        issues: list[str] = []

        # All tasks must be satisfiable
        if not task.satisfiable:
            issues.append("task is not satisfiable (all tasks must be satisfiable)")

        # Check assistant free slots
        free = _count_free_slots(task)
        if free == 0:
            issues.append("no free slots in assistant calendar (expected >0)")

        # Check conflict exists
        if not _has_any_conflict(task):
            issues.append("no conflict between request and assistant calendar")

        # Secret conflict check
        conflict = _get_conflict_event(task)
        if conflict is not None and not conflict.is_secret:
            issues.append(f"conflict event '{conflict.title}' is not secret")

        # Suboptimal preference check
        prefs = task.assistant.preferences
        if prefs:
            req_start = task.requestor.requested_meeting.start_time
            scores = {p.start_time: p.score for p in prefs}
            req_score = scores.get(req_start)
            if req_score is not None:
                max_score = max(scores.values())
                if req_score >= max_score:
                    issues.append("request slot is at peak preference (should be suboptimal)")

        # Requestor calendar check
        requestor_working = [
            e for e in task.requestor.calendar if "sleep" not in e.uid and "personal" not in e.uid
        ]
        if not task.requestor.calendar:
            issues.append("requestor has no calendar")
        elif not requestor_working and len(task.requestor.calendar) > 0:
            # Has sleep/personal but no working events is valid for high fullness
            pass

        # Overlap check: at least 1 slot free in both calendars
        assistant_free = _get_free_slot_indices(task.assistant.calendar)
        requestor_free = _get_free_slot_indices(task.requestor.calendar)
        overlap = assistant_free & requestor_free
        if not overlap:
            issues.append(
                f"no overlapping free slots "
                f"(assistant free: {sorted(assistant_free)}, "
                f"requestor free: {sorted(requestor_free)})"
            )

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
