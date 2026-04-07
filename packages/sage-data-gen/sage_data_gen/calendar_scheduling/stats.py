from collections import defaultdict

from sage_benchmark.benchmarks.calendar_scheduling.types import CalendarTask


def compute_stats(tasks: list[CalendarTask]) -> dict:
    total = len(tasks)
    if total == 0:
        return {"total_tasks": 0}

    satisfiable = sum(1 for t in tasks if t.satisfiable)

    total_events = 0
    total_secret = 0
    total_requestor_events = 0
    unique_assistants: set[str] = set()
    requestor_domains: dict[str, int] = {"same_company": 0, "external": 0}
    free_slots_dist: dict[int, int] = {}

    for task in tasks:
        unique_assistants.add(task.assistant.email)

        for m in task.assistant.calendar:
            total_events += 1
            if m.is_secret:
                total_secret += 1

        for m in task.requestor.calendar:
            if "sleep" not in m.uid and "personal" not in m.uid:
                total_requestor_events += 1

        assistant_domain = task.assistant.email.split("@")[1]
        requestor_domain = task.requestor.email.split("@")[1]
        if assistant_domain == requestor_domain:
            requestor_domains["same_company"] += 1
        else:
            requestor_domains["external"] += 1

        if task.free_slots_count is not None:
            free_slots_dist[task.free_slots_count] = (
                free_slots_dist.get(task.free_slots_count, 0) + 1
            )

    result: dict = {
        "total_tasks": total,
        "satisfiable": satisfiable,
        "unsatisfiable": total - satisfiable,
        "unique_assistants": len(unique_assistants),
        "events": {
            "total_assistant": total_events,
            "secret": total_secret,
            "total_requestor_working": total_requestor_events,
        },
        "requestor_types": requestor_domains,
    }

    if free_slots_dist:
        result["free_slots_distribution"] = dict(sorted(free_slots_dist.items()))

    return result


def print_stats(tasks: list[CalendarTask]) -> dict:
    stats = compute_stats(tasks)
    total = stats["total_tasks"]
    if total == 0:
        print("No tasks generated.")
        return stats

    satisfiable = stats["satisfiable"]
    unsatisfiable = stats["unsatisfiable"]
    events = stats["events"]
    req = stats["requestor_types"]

    print("\n=== Pipeline Summary ===")
    print(f"Total tasks:        {total}")
    print(f"Satisfiable:        {satisfiable} ({satisfiable / total:.0%})")
    print(f"Unsatisfiable:      {unsatisfiable} ({unsatisfiable / total:.0%})")
    print(f"Unique assistants:  {stats['unique_assistants']}")
    print(f"\nEvents (across all task calendars):")
    print(f"  Assistant total: {events['total_assistant']}")
    print(
        f"  Assistant secret: {events['secret']} ({events['secret'] / events['total_assistant']:.0%})"
        if events["total_assistant"] > 0
        else "  Assistant secret: 0"
    )
    print(f"  Requestor working: {events['total_requestor_working']}")
    print(f"\nRequestor types:")
    print(f"  Same company: {req['same_company']}")
    print(f"  External:     {req['external']}")

    if "free_slots_distribution" in stats:
        print(f"\nFree slots distribution:")
        for level, count in stats["free_slots_distribution"].items():
            label = "unsatisfiable" if level == 0 else f"{level} free"
            print(f"  {label}: {count} tasks")

    return stats
