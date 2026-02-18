from sage_benchmark.calendar_scheduling.types import CalendarTask

from .models import CalendarEvent


def _time_to_minutes(t: str) -> int:
    h, m = t.split(":")
    return int(h) * 60 + int(m)


def compute_stats(
    tasks: list[CalendarTask], employee_calendars: dict[str, list[CalendarEvent]] | None = None
) -> dict:
    total = len(tasks)
    if total == 0:
        return {"total_tasks": 0}

    satisfiable = sum(1 for t in tasks if t.satisfiable)

    fullness_values: list[float] = []
    total_events = 0
    total_secret = 0
    total_movable = 0
    total_potentially_secret = 0
    both_secret = 0  # is_secret=True AND potentially_secret=True
    only_contextual = 0  # is_secret=True but potentially_secret=False
    only_rule_based = 0  # is_secret=False but potentially_secret=True
    unique_assistants: set[str] = set()
    requestor_domains: dict[str, int] = {"same_company": 0, "external": 0}

    for task in tasks:
        unique_assistants.add(task.assistant.email)

        busy_minutes = sum(
            _time_to_minutes(m.end_time) - _time_to_minutes(m.start_time)
            for m in task.assistant.calendar
        )
        fullness_values.append(busy_minutes / (24 * 60))

        for m in task.assistant.calendar:
            total_events += 1
            if m.is_secret:
                total_secret += 1
            if m.is_movable:
                total_movable += 1

            # Privacy label comparison (if employee_calendars provided)
            if employee_calendars:
                # Extract event index from UID: "{email_prefix}-cal-{i}"
                parts = m.uid.rsplit("-", 1)
                if len(parts) == 2 and parts[1].isdigit():
                    event_idx = int(parts[1])
                    calendar_events = employee_calendars.get(task.assistant.email, [])
                    if event_idx < len(calendar_events):
                        event = calendar_events[event_idx]
                        if event.potentially_secret:
                            total_potentially_secret += 1
                        if m.is_secret and event.potentially_secret:
                            both_secret += 1
                        elif m.is_secret and not event.potentially_secret:
                            only_contextual += 1
                        elif not m.is_secret and event.potentially_secret:
                            only_rule_based += 1

        assistant_domain = task.assistant.email.split("@")[1]
        requestor_domain = task.requestor.email.split("@")[1]
        if assistant_domain == requestor_domain:
            requestor_domains["same_company"] += 1
        else:
            requestor_domains["external"] += 1

    result = {
        "total_tasks": total,
        "satisfiable": satisfiable,
        "unsatisfiable": total - satisfiable,
        "unique_assistants": len(unique_assistants),
        "calendar_fullness": {
            "min": round(min(fullness_values), 3),
            "max": round(max(fullness_values), 3),
            "avg": round(sum(fullness_values) / len(fullness_values), 3),
        },
        "events": {
            "total": total_events,
            "secret": total_secret,
            "movable": total_movable,
        },
        "requestor_types": requestor_domains,
    }

    # Add privacy comparison if metadata was available
    if (
        total_potentially_secret > 0
        or both_secret > 0
        or only_contextual > 0
        or only_rule_based > 0
    ):
        result["privacy_labeling"] = {
            "total_potentially_secret": total_potentially_secret,
            "both_secret": both_secret,
            "only_contextual_secret": only_contextual,
            "only_rule_based_secret": only_rule_based,
            "agreement_rate": round(
                (
                    both_secret
                    + (total_events - total_secret - total_potentially_secret + both_secret)
                )
                / total_events,
                3,
            )
            if total_events > 0
            else 0,
        }

    return result


def print_stats(
    tasks: list[CalendarTask], employee_calendars: dict[str, list[CalendarEvent]] | None = None
) -> dict:
    stats = compute_stats(tasks, employee_calendars)
    total = stats["total_tasks"]
    if total == 0:
        print("No tasks generated.")
        return stats

    satisfiable = stats["satisfiable"]
    unsatisfiable = stats["unsatisfiable"]
    fullness = stats["calendar_fullness"]
    events = stats["events"]
    req = stats["requestor_types"]

    print("\n=== Pipeline Summary ===")
    print(f"Total tasks:        {total}")
    print(f"Satisfiable:        {satisfiable} ({satisfiable / total:.0%})")
    print(f"Unsatisfiable:      {unsatisfiable} ({unsatisfiable / total:.0%})")
    print(f"Unique assistants:  {stats['unique_assistants']}")
    print(f"\nCalendar fullness:")
    print(f"  Min: {fullness['min']:.0%}")
    print(f"  Max: {fullness['max']:.0%}")
    print(f"  Avg: {fullness['avg']:.0%}")
    print(f"\nEvents (across all task calendars):")
    print(f"  Total:   {events['total']}")
    print(f"  Secret:  {events['secret']} ({events['secret'] / events['total']:.0%})")
    print(f"  Movable: {events['movable']} ({events['movable'] / events['total']:.0%})")
    print(f"\nRequestor types:")
    print(f"  Same company: {req['same_company']}")
    print(f"  External:     {req['external']}")

    # Print privacy comparison if available
    if "privacy_labeling" in stats:
        privacy = stats["privacy_labeling"]
        print(f"\nPrivacy Labeling (Contextual vs Rule-based):")
        print(f"  Both secret:              {privacy['both_secret']}")
        print(f"  Only contextual secret:   {privacy['only_contextual_secret']}")
        print(f"  Only rule-based secret:   {privacy['only_rule_based_secret']}")
        print(
            f"  Agreement rate:           {privacy['agreement_rate']:.0%} "
            f"({privacy['both_secret']} agree secret, "
            f"{events['total'] - privacy['total_potentially_secret'] - privacy['only_contextual_secret']} agree not secret)"
        )

    return stats
