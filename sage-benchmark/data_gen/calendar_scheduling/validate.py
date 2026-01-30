from sage_benchmark.calendar_scheduling.loader import load_artifacts, load_calendar_tasks


def _time_to_minutes(t: str) -> int:
    h, m = t.split(":")
    return int(h) * 60 + int(m)


def validate_output(tasks_path: str, artifacts_path: str) -> None:
    tasks = load_calendar_tasks(tasks_path)
    artifacts = load_artifacts(artifacts_path)

    assert len(tasks) > 0, "No tasks found"

    for i, task in enumerate(tasks):
        assert task.type == "calendar", f"Task {i}: wrong type '{task.type}'"
        assert task.requestor.is_malicious is False, f"Task {i}: is_malicious should be False"
        assert len(task.assistant.calendar) > 0, f"Task {i}: empty calendar"
        assert len(task.assistant.contacts) > 0, f"Task {i}: empty contacts"

        # Validate time formats
        for event in task.assistant.calendar:
            assert len(event.start_time) == 5, f"Task {i}: bad start_time '{event.start_time}'"
            assert len(event.end_time) == 5, f"Task {i}: bad end_time '{event.end_time}'"

        # Validate requested meeting conflicts with at least one calendar event
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

    # Verify artifact indices match task indices
    for task_idx in range(len(tasks)):
        assert task_idx in artifacts, f"Missing artifacts for task {task_idx}"

    print(f"  Validation passed: {len(tasks)} tasks, {len(artifacts)} artifact sets")
