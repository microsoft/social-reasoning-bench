from sage_benchmark.benchmarks.calendar_scheduling.loader import load_tasks

from .assemble import _get_free_slot_indices
from .utils import _time_to_minutes


def validate_output(tasks_path: str) -> None:
    loaded = load_tasks([tasks_path])
    tasks = loaded.all_tasks

    assert len(tasks) > 0, "No tasks found"

    for i, task in enumerate(tasks):
        assert task.type == "calendar", f"Task {i}: wrong type '{task.type}'"
        assert task.requestor.is_malicious is False, f"Task {i}: is_malicious should be False"
        assert len(task.assistant.calendar) > 0, f"Task {i}: empty assistant calendar"
        assert len(task.assistant.contacts) > 0, f"Task {i}: empty contacts"
        assert len(task.requestor.calendar) > 0, f"Task {i}: empty requestor calendar"

        # All tasks must be satisfiable
        assert task.satisfiable, f"Task {i}: task is not satisfiable"

        for event in task.assistant.calendar:
            assert len(event.start_time) == 5, f"Task {i}: bad start_time '{event.start_time}'"
            assert len(event.end_time) == 5, f"Task {i}: bad end_time '{event.end_time}'"
            assert event.is_movable is False, f"Task {i}: event '{event.title}' has is_movable=True"

        for event in task.requestor.calendar:
            assert len(event.start_time) == 5, (
                f"Task {i}: bad requestor start_time '{event.start_time}'"
            )
            assert len(event.end_time) == 5, f"Task {i}: bad requestor end_time '{event.end_time}'"

        req = task.requestor.requested_meeting
        req_start = _time_to_minutes(req.start_time)
        req_end = _time_to_minutes(req.end_time)

        has_conflict = any(
            _time_to_minutes(e.start_time) < req_end and req_start < _time_to_minutes(e.end_time)
            for e in task.assistant.calendar
        )
        assert has_conflict, (
            f"Task {i}: requested meeting {req.start_time}-{req.end_time} "
            f"has no conflict with any calendar event"
        )

        # Validate overlap: at least 1 slot free in both calendars
        assistant_free = _get_free_slot_indices(task.assistant.calendar)
        requestor_free = _get_free_slot_indices(task.requestor.calendar)
        overlap = assistant_free & requestor_free
        assert overlap, (
            f"Task {i}: no overlapping free slots "
            f"(assistant free: {sorted(assistant_free)}, "
            f"requestor free: {sorted(requestor_free)})"
        )

    print(f"  Validation passed: {len(tasks)} tasks")
