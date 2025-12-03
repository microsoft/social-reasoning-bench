"""Date and time utility functions for calendar operations."""

from __future__ import annotations

from datetime import date, datetime, time, timedelta
from zoneinfo import ZoneInfo

from dateutil.rrule import DAILY, MONTHLY, WEEKLY, YEARLY, rrule

from ..entities import RecurrenceRule, TimeRange


def parse_time(time_str: str, timezone_str: str) -> time:
    """
    Parse a time string with timezone information.

    Args:
        time_str: Time string in format "HH:MM" or "HH:MM:SS"
        timezone_str: Timezone string (e.g., "America/New_York")

    Returns:
        time object with timezone info
    """
    # Parse the time components
    parts = time_str.split(":")
    hour = int(parts[0])
    minute = int(parts[1])
    second = int(parts[2]) if len(parts) > 2 else 0

    # Create timezone-aware time
    tz = ZoneInfo(timezone_str)
    # Note: time objects in Python don't directly support tzinfo in a straightforward way
    # We return a time object and handle timezone separately
    return time(hour, minute, second, tzinfo=tz)


def ensure_timezone_aware(dt: datetime, default_tz: str = "UTC") -> datetime:
    """
    Ensure a datetime is timezone-aware.

    If the datetime is naive (no timezone info), applies the default timezone.
    If already aware, returns unchanged.

    Args:
        dt: Datetime to check/convert
        default_tz: Default timezone to apply if naive (default: "UTC")

    Returns:
        Timezone-aware datetime

    Examples:
        >>> from datetime import datetime
        >>> naive_dt = datetime(2024, 1, 15, 10, 30)
        >>> aware_dt = ensure_timezone_aware(naive_dt, "America/New_York")
        >>> aware_dt.tzinfo is not None
        True

        >>> from zoneinfo import ZoneInfo
        >>> already_aware = datetime(2024, 1, 15, 10, 30, tzinfo=ZoneInfo("UTC"))
        >>> result = ensure_timezone_aware(already_aware, "America/New_York")
        >>> result.tzinfo == ZoneInfo("UTC")  # Original timezone preserved
        True
    """
    if dt.tzinfo is None:
        # Naive datetime - apply default timezone
        tz = ZoneInfo(default_tz)
        return dt.replace(tzinfo=tz)
    else:
        # Already timezone-aware - return as-is
        return dt


def combine_date_and_time(d: date, t: time, timezone_str: str | None = None) -> datetime:
    """
    Combine a date and time into a timezone-aware datetime.

    Args:
        d: Date component
        t: Time component
        timezone_str: Optional timezone override

    Returns:
        Timezone-aware datetime
    """
    if timezone_str:
        # Explicit timezone override
        dt = datetime.combine(d, t.replace(tzinfo=None))
        return ensure_timezone_aware(dt, timezone_str)
    elif t.tzinfo:
        # Use the time's timezone - directly attach it rather than converting to string
        # This preserves the timezone object whether it's a ZoneInfo or a fixed offset
        dt = datetime.combine(d, t)
        return dt
    else:
        # No timezone information - use UTC as default
        dt = datetime.combine(d, t)
        return ensure_timezone_aware(dt, "UTC")


def expand_recurrence(
    start_date: date,
    recurrence_rule: RecurrenceRule,
    date_range: TimeRange,
    limit: int | None = None,
) -> list[date]:
    """
    Expand a recurrence rule into concrete dates within a range.

    Args:
        start_date: First occurrence date
        recurrence_rule: Recurrence pattern
        date_range: Date range to expand into
        limit: Maximum number of occurrences to generate

    Returns:
        List of dates matching the recurrence pattern
    """
    from ..entities import EndType, Frequency

    # Map our Frequency enum to dateutil's constants
    freq_map = {
        Frequency.DAILY: DAILY,
        Frequency.WEEKLY: WEEKLY,
        Frequency.MONTHLY: MONTHLY,
        Frequency.YEARLY: YEARLY,
    }

    # Build rrule kwargs
    kwargs = {
        "freq": freq_map[recurrence_rule.frequency],
        "interval": recurrence_rule.interval,
        "dtstart": datetime.combine(start_date, time(0, 0)),
    }

    # Handle by_day (weekdays)
    if recurrence_rule.by_day:
        # Map our DayOfWeek enum to dateutil's constants (MO, TU, etc.)
        from dateutil.rrule import FR, MO, SA, SU, TH, TU, WE

        day_map = {
            "MONDAY": MO,
            "TUESDAY": TU,
            "WEDNESDAY": WE,
            "THURSDAY": TH,
            "FRIDAY": FR,
            "SATURDAY": SA,
            "SUNDAY": SU,
        }
        kwargs["byweekday"] = [day_map[day.value] for day in recurrence_rule.by_day]

    # Handle by_month_day
    if recurrence_rule.by_month_day:
        kwargs["bymonthday"] = recurrence_rule.by_month_day

    # Handle by_month
    if recurrence_rule.by_month:
        kwargs["bymonth"] = [m.value for m in recurrence_rule.by_month]

    # Handle by_set_pos
    if recurrence_rule.by_set_pos:
        kwargs["bysetpos"] = recurrence_rule.by_set_pos

    # Handle end condition
    if recurrence_rule.end_condition.type == EndType.UNTIL_DATE:
        assert recurrence_rule.end_condition.until_date is not None
        kwargs["until"] = datetime.combine(
            recurrence_rule.end_condition.until_date,
            time(23, 59, 59),
        )
    elif recurrence_rule.end_condition.type == EndType.COUNT:
        assert recurrence_rule.end_condition.count is not None
        kwargs["count"] = recurrence_rule.end_condition.count

    # Generate occurrences
    rule = rrule(**kwargs)

    # Filter to date range and convert to dates
    results = []
    for dt in rule:
        d = dt.date()
        if d >= date_range.end.date():
            break
        if d >= date_range.start.date():
            results.append(d)
            if limit and len(results) >= limit:
                break

    return results


def get_next_occurrence(
    current_date: date,
    recurrence_rule: RecurrenceRule,
) -> date | None:
    """
    Get the next occurrence after a given date.

    Args:
        current_date: Current date
        recurrence_rule: Recurrence pattern

    Returns:
        Next occurrence date, or None if no more occurrences
    """
    # Create a range starting from the next day
    start = datetime.combine(current_date + timedelta(days=1), time(0, 0))
    # Look ahead up to 2 years
    end = start + timedelta(days=730)

    range_obj = TimeRange(start=start, end=end)

    occurrences = expand_recurrence(current_date, recurrence_rule, range_obj, limit=1)

    return occurrences[0] if occurrences else None


def events_overlap(
    start1: datetime,
    end1: datetime,
    start2: datetime,
    end2: datetime,
) -> bool:
    """
    Check if two events overlap in time.

    Args:
        start1: Start time of first event
        end1: End time of first event
        start2: Start time of second event
        end2: End time of second event

    Returns:
        True if events overlap
    """
    return start1 < end2 and start2 < end1
