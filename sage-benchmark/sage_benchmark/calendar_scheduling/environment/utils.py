"""Utility functions for date/time parsing and formatting."""

import re
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
    """Validate hours and minutes are in valid range and format result."""
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
    """Convert HH:MM time string to minutes from midnight."""
    parts = time_str.split(":")
    return int(parts[0]) * 60 + int(parts[1])


def format_meeting_as_attachment(meeting: Meeting) -> str:
    """Format a meeting as a pretty-printed string for email attachment."""
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
    """Format emails for display to agent."""
    if not emails:
        return "No unread emails."

    formatted = []
    for i, email in enumerate(emails, 1):
        entry = f"[{i}] From: {email.from_}\nSubject: {email.subject}\n\n{email.body}"
        if email.event:
            entry += f"\n\n{email.event}"
        formatted.append(entry)

    return "\n\n---\n\n".join(formatted)


def format_meetings(meetings: list[Meeting]) -> str:
    """Format meetings for display to agent."""
    if not meetings:
        return "No meetings on your calendar."

    return "\n\n".join(format_meeting_as_attachment(m) for m in meetings)
