"""Utility functions for date/time parsing and formatting."""

import re
from collections.abc import Sequence
from datetime import datetime

from ..types import Email, Meeting


def parse_date(date_str: str) -> str:
    """Parse flexible date formats into ISO format (YYYY-MM-DD).

    Supports:
    - "January 15, 2024"
    - "01-15-2024"
    - "2024-01-15"
    - "1/15/2024"
    - "15 January 2024"

    Args:
        date_str: Date string in any of the supported formats.

    Returns:
        Date in ISO format (YYYY-MM-DD).

    Raises:
        ValueError: If the date string cannot be parsed by any supported format.
    """
    formats = [
        "%B %d, %Y",  # January 15, 2024
        "%b %d, %Y",  # Jan 15, 2024
        "%m-%d-%Y",  # 01-15-2024
        "%Y-%m-%d",  # 2024-01-15
        "%m/%d/%Y",  # 1/15/2024
        "%d %B %Y",  # 15 January 2024
        "%d %b %Y",  # 15 Jan 2024
    ]

    date_str = date_str.strip()
    for fmt in formats:
        try:
            dt = datetime.strptime(date_str, fmt)
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            continue

    raise ValueError(f"Unable to parse date: {date_str}")


def _validate_time(hours: int, minutes: int, original: str) -> str:
    """Validate hours and minutes are in valid range and format result.

    Args:
        hours: Hour value (0-23).
        minutes: Minute value (0-59).
        original: Original time string for error messages.

    Returns:
        Formatted time string in HH:MM format.

    Raises:
        ValueError: If hours or minutes are out of valid range.
    """
    if not (0 <= hours <= 23):
        raise ValueError(f"Invalid hour {hours} in time: {original}")
    if not (0 <= minutes <= 59):
        raise ValueError(f"Invalid minutes {minutes} in time: {original}")
    return f"{hours:02d}:{minutes:02d}"


def parse_time(time_str: str) -> str:
    """Parse flexible time formats into 24-hour format (HH:MM).

    Supports:
    - "2pm", "2PM"
    - "14:00"
    - "2:00pm", "2:00 PM"
    - "1330" (military)

    Args:
        time_str: Time string in any of the supported formats.

    Returns:
        Time in 24-hour format (HH:MM).

    Raises:
        ValueError: If time format is unrecognized or values are out of range.
    """
    original = time_str
    time_str = time_str.strip().lower().replace(" ", "")

    # Handle military time (4 digits)
    if re.match(r"^\d{4}$", time_str):
        hours = int(time_str[:2])
        minutes = int(time_str[2:])
        return _validate_time(hours, minutes, original)

    # Handle 24-hour format (HH:MM)
    match_24h = re.match(r"^(\d{1,2}):(\d{2})$", time_str)
    if match_24h:
        hours = int(match_24h.group(1))
        minutes = int(match_24h.group(2))
        return _validate_time(hours, minutes, original)

    # Handle 12-hour formats (with am/pm)
    am_pm_match = re.match(r"^(\d{1,2})(?::(\d{2}))?(am|pm)$", time_str)
    if am_pm_match:
        hours = int(am_pm_match.group(1))
        minutes = int(am_pm_match.group(2) or 0)
        is_pm = am_pm_match.group(3) == "pm"

        # Validate 12-hour format range
        if not (1 <= hours <= 12):
            raise ValueError(f"Invalid hour {hours} for 12-hour format in time: {original}")

        if is_pm and hours != 12:
            hours += 12
        elif not is_pm and hours == 12:
            hours = 0

        return _validate_time(hours, minutes, original)

    raise ValueError(f"Unable to parse time: {original}")


def time_to_minutes(time_str: str) -> int:
    """Convert HH:MM time string to minutes from midnight.

    Args:
        time_str: Time string in HH:MM format.

    Returns:
        Total minutes from midnight.
    """
    parts = time_str.split(":")
    return int(parts[0]) * 60 + int(parts[1])


def format_meeting_as_attachment(meeting: Meeting) -> str:
    """Format a meeting as a pretty-printed string for email attachment.

    Args:
        meeting: The meeting to format.

    Returns:
        A multi-line formatted string representing the calendar event.
    """
    attendee_list = "\n".join(f"  - {a.email} ({a.status.value})" for a in meeting.attendees)
    return f"""=== CALENDAR EVENT ===
UID: {meeting.uid}
Title: {meeting.title}
Description: {meeting.description}
Date: {meeting.date}
Time: {meeting.start_time} - {meeting.end_time}
Organizer: {meeting.organizer}
Attendees:
{attendee_list}
======================"""


def format_emails(emails: list[Email]) -> str:
    """Format emails for display to agent.

    Args:
        emails: List of Email objects to format.

    Returns:
        Formatted string of emails separated by dividers, or a
        no-unread-emails message if the list is empty.
    """
    if not emails:
        return "No unread emails."

    formatted = []
    for i, email in enumerate(emails, 1):
        entry = f"[{i}] From: {email.from_}\nSubject: {email.subject}\n\n{email.body}"
        if email.event:
            entry += f"\n\n{email.event}"
        formatted.append(entry)

    return "\n\n---\n\n".join(formatted)


def _format_free_block(start: str, end: str) -> str:
    """Format a free time block.

    Args:
        start: Start time in HH:MM format.
        end: End time in HH:MM format.

    Returns:
        A formatted string showing the free time block with duration.
    """
    start_mins = time_to_minutes(start)
    end_mins = time_to_minutes(end)
    duration_mins = end_mins - start_mins
    hours = duration_mins // 60
    mins = duration_mins % 60
    if hours > 0 and mins > 0:
        duration_str = f"{hours} hour{'s' if hours > 1 else ''} {mins} min"
    elif hours > 0:
        duration_str = f"{hours} hour{'s' if hours > 1 else ''}"
    else:
        duration_str = f"{mins} min"
    return f"""=== FREE ===
Time: {start} - {end}
Duration: {duration_str}
============"""


def format_meetings(
    meetings: Sequence[Meeting], business_start: str = "09:00", business_end: str = "17:00"
) -> str:
    """Format meetings for display to agent, including FREE time blocks.

    Shows scheduled meetings and FREE blocks during business hours (default 9:00-17:00).

    Args:
        meetings: Sequence of meetings to format.
        business_start: Start of business hours in HH:MM format.
        business_end: End of business hours in HH:MM format.

    Returns:
        Formatted string of meetings interleaved with free time blocks.
    """
    if not meetings:
        return (
            f"No meetings on your calendar.\n\n{_format_free_block(business_start, business_end)}"
        )

    # Sort meetings by start time
    sorted_meetings = sorted(meetings, key=lambda m: time_to_minutes(m.start_time))

    # Build output with meetings and free blocks
    output_blocks = []
    current_time = business_start
    business_start_mins = time_to_minutes(business_start)
    business_end_mins = time_to_minutes(business_end)

    for meeting in sorted_meetings:
        meeting_start_mins = time_to_minutes(meeting.start_time)
        meeting_end_mins = time_to_minutes(meeting.end_time)
        current_mins = time_to_minutes(current_time)

        # Skip meetings entirely outside business hours
        if meeting_end_mins <= business_start_mins or meeting_start_mins >= business_end_mins:
            output_blocks.append(format_meeting_as_attachment(meeting))
            continue

        # Clamp meeting times to business hours for gap calculation
        effective_start = max(meeting_start_mins, business_start_mins)
        effective_end = min(meeting_end_mins, business_end_mins)

        # Add free block if there's a gap before this meeting
        if current_mins < effective_start:
            free_start = current_time
            free_end = (
                meeting.start_time if meeting_start_mins >= business_start_mins else business_start
            )
            if time_to_minutes(free_start) < time_to_minutes(free_end):
                output_blocks.append(_format_free_block(free_start, free_end))

        # Add the meeting
        output_blocks.append(format_meeting_as_attachment(meeting))

        # Update current time to end of this meeting (clamped to business hours)
        if effective_end > current_mins:
            hours, mins = divmod(effective_end, 60)
            current_time = f"{hours:02d}:{mins:02d}"

    # Add free block at end if there's time remaining
    current_mins = time_to_minutes(current_time)
    if current_mins < business_end_mins:
        output_blocks.append(_format_free_block(current_time, business_end))

    return "\n\n".join(output_blocks)
