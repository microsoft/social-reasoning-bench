"""iCalendar (.ics) file import support."""

import logging
import uuid
from dataclasses import dataclass
from datetime import date, datetime, time
from pathlib import Path

import icalendar

from ..entities import (
    DayOfWeek,
    EndCondition,
    EndType,
    Event,
    Frequency,
    Modification,
    Month,
    RecurrenceRule,
)
from ..utils.dates import ensure_timezone_aware

logger = logging.getLogger(__name__)


class ICSImportError(Exception):
    """Base exception for .ics import errors."""

    pass


class ICSParseError(ICSImportError):
    """Error parsing .ics file format."""

    pass


class ICSMappingError(ICSImportError):
    """Error mapping .ics data to calendar_gym entities."""

    pass


@dataclass
class ICSImportConfig:
    """Configuration for .ics file import."""

    participant_map: dict[str, str]  # email → participant_id
    default_timezone: str = "UTC"
    default_organizer_id: str | None = None
    preserve_uids: bool = True  # Use .ics UIDs or generate new ones
    skip_unknown_attendees: bool = True  # Skip events with unmapped attendees


class ICSImporter:
    """Imports iCalendar (.ics) files into calendar_gym entities."""

    def __init__(self, config: ICSImportConfig):
        """
        Initialize the ICS importer.

        Args:
            config: Import configuration
        """
        self.config = config

    def import_from_file(
        self,
        ics_path: str | Path,
    ) -> list[Event]:
        """
        Import .ics file into calendar Event entities.

        Args:
            ics_path: Path to .ics file

        Returns:
            List of Event objects (both standalone and recurring)

        Raises:
            ICSParseError: If file parsing fails
            ICSMappingError: If entity mapping fails
        """
        logger.info(f"Importing iCalendar file: {ics_path}")

        # Read and parse .ics file
        try:
            ics_data = Path(ics_path).read_text()
            calendar = icalendar.Calendar.from_ical(ics_data)
        except Exception as e:
            raise ICSParseError(f"Failed to parse .ics file: {e}") from e

        # Track events by UID for handling RECURRENCE-ID
        event_map: dict[str, Event] = {}
        errors: list[dict] = []

        # Process all VEVENT components
        for component in calendar.walk("VEVENT"):
            try:
                result = self._convert_vevent(component, event_map)
                if result:
                    event_map[result.id] = result
            except Exception as e:
                uid = component.get("UID", "unknown")
                errors.append({"uid": uid, "error": str(e)})
                logger.warning(f"Failed to import event {uid}: {e}")

        events = list(event_map.values())

        logger.info(
            f"Imported {len(events)} events ({sum(1 for e in events if e.is_recurring)} recurring)"
        )
        if errors:
            logger.warning(f"Encountered {len(errors)} errors during import")

        return events

    def _convert_vevent(
        self,
        vevent: icalendar.cal.Component,
        event_map: dict[str, Event],
    ) -> Event | None:
        """
        Convert iCalendar VEVENT to Event (standalone or recurring).

        Args:
            vevent: iCalendar event component
            event_map: Map of UIDs to Events (for handling RECURRENCE-ID)

        Returns:
            Event or None if should be skipped
        """
        uid = str(vevent.get("UID", uuid.uuid4()))

        # Check if this is a recurrence instance modification
        recurrence_id = vevent.get("RECURRENCE-ID")
        if recurrence_id:
            # This is a modification of a recurring event instance
            self._handle_recurrence_id(vevent, event_map, uid)
            return None

        # Extract basic fields
        summary = str(vevent.get("SUMMARY", "Untitled Event"))
        description = str(vevent.get("DESCRIPTION", ""))

        # Extract organizer
        organizer_id = self._extract_organizer(vevent)
        if not organizer_id:
            if not self.config.default_organizer_id:
                logger.warning(f"No organizer for event {uid}, skipping")
                return None
            organizer_id = self.config.default_organizer_id

        # Extract participants
        participants = self._extract_participants(vevent, organizer_id)

        # Extract dates/times
        dtstart = vevent.get("DTSTART")
        dtend = vevent.get("DTEND")

        if not dtstart:
            logger.warning(f"Event {uid} has no DTSTART, skipping")
            return None

        # Get datetime objects (icalendar handles timezone conversion)
        start_dt = dtstart.dt
        end_dt = dtend.dt if dtend else None

        # Handle all-day events (date-only)
        if isinstance(start_dt, date) and not isinstance(start_dt, datetime):
            # All-day event - convert to datetime with timezone
            start_dt = datetime.combine(start_dt, time(0, 0))
            start_dt = ensure_timezone_aware(start_dt, self.config.default_timezone)
            if end_dt and isinstance(end_dt, date):
                end_dt = datetime.combine(end_dt, time(23, 59))
                end_dt = ensure_timezone_aware(end_dt, self.config.default_timezone)

        # Ensure timezone-aware using utility function
        start_dt = ensure_timezone_aware(start_dt, self.config.default_timezone)

        if end_dt:
            end_dt = ensure_timezone_aware(end_dt, self.config.default_timezone)

        # If no end time, default to 1 hour
        if not end_dt:
            from datetime import timedelta

            end_dt = start_dt + timedelta(hours=1)

        # Check if this is a recurring event
        rrule = vevent.get("RRULE")
        event_id = uid if self.config.preserve_uids else str(uuid.uuid4())

        if rrule:
            # Create recurring Event
            recurrence_rule = self._parse_rrule(rrule, start_dt)

            event = Event(
                id=event_id,
                recurrence_rule=recurrence_rule,
                organizer_id=organizer_id,
                start_datetime=start_dt,
                end_datetime=end_dt,
                title=summary,
                description=description,
                participants=participants,
                instance_modifications=None,
            )

            return event
        else:
            # Create standalone Event
            event = Event(
                id=event_id,
                recurrence_rule=None,
                organizer_id=organizer_id,
                start_datetime=start_dt,
                end_datetime=end_dt,
                title=summary,
                description=description,
                participants=participants,
            )

            return event

    def _parse_rrule(
        self,
        rrule: dict,
        dtstart: datetime,
    ) -> RecurrenceRule:
        """
        Parse iCalendar RRULE to RecurrenceRule.

        Args:
            rrule: RRULE dictionary from icalendar
            dtstart: Start datetime for context

        Returns:
            RecurrenceRule object
        """
        # Map frequency
        freq_map = {
            "DAILY": Frequency.DAILY,
            "WEEKLY": Frequency.WEEKLY,
            "MONTHLY": Frequency.MONTHLY,
            "YEARLY": Frequency.YEARLY,
        }

        freq_str = rrule.get("FREQ", ["DAILY"])[0]
        frequency = freq_map.get(freq_str, Frequency.DAILY)

        # Get interval
        interval = int(rrule.get("INTERVAL", [1])[0])

        # Parse BYDAY
        by_day = None
        if "BYDAY" in rrule:
            day_map = {
                "MO": DayOfWeek.MONDAY,
                "TU": DayOfWeek.TUESDAY,
                "WE": DayOfWeek.WEDNESDAY,
                "TH": DayOfWeek.THURSDAY,
                "FR": DayOfWeek.FRIDAY,
                "SA": DayOfWeek.SATURDAY,
                "SU": DayOfWeek.SUNDAY,
            }
            byday_values = rrule["BYDAY"]
            if not isinstance(byday_values, list):
                byday_values = [byday_values]

            by_day = []
            for day_str in byday_values:
                # Remove numeric prefix if present (e.g., "2MO" → "MO")
                day_code = str(day_str).lstrip("-0123456789")
                if day_code in day_map:
                    by_day.append(day_map[day_code])

        # Parse BYMONTHDAY (now supports list)
        by_month_day = None
        if "BYMONTHDAY" in rrule:
            monthday_values = rrule["BYMONTHDAY"]
            if not isinstance(monthday_values, list):
                monthday_values = [monthday_values]
            by_month_day = [int(d) for d in monthday_values]

        # Parse BYMONTH
        by_month = None
        if "BYMONTH" in rrule:
            bymonth_values = rrule["BYMONTH"]
            if not isinstance(bymonth_values, list):
                bymonth_values = [bymonth_values]
            by_month = [Month(int(m)) for m in bymonth_values]

        # Parse BYSETPOS
        by_set_pos = None
        if "BYSETPOS" in rrule:
            setpos_values = rrule["BYSETPOS"]
            if not isinstance(setpos_values, list):
                setpos_values = [setpos_values]
            by_set_pos = [int(p) for p in setpos_values]

        # Parse end condition
        if "UNTIL" in rrule:
            until_value = rrule["UNTIL"][0]
            # icalendar returns datetime or date
            until_date = until_value.date() if isinstance(until_value, datetime) else until_value

            end_condition = EndCondition(
                type=EndType.UNTIL_DATE,
                until_date=until_date,
            )
        elif "COUNT" in rrule:
            count = int(rrule["COUNT"][0])
            end_condition = EndCondition(
                type=EndType.COUNT,
                count=count,
            )
        else:
            end_condition = EndCondition(type=EndType.NEVER)

        return RecurrenceRule(
            frequency=frequency,
            interval=interval,
            by_day=by_day,
            by_month_day=by_month_day,
            by_month=by_month,
            by_set_pos=by_set_pos,
            end_condition=end_condition,
        )

    def _handle_recurrence_id(
        self,
        vevent: icalendar.cal.Component,
        event_map: dict[str, Event],
        uid: str,
    ) -> None:
        """
        Handle RECURRENCE-ID (instance modification).

        Args:
            vevent: Modified instance VEVENT
            event_map: Map of UIDs to Events
            uid: Event UID
        """
        if uid not in event_map:
            logger.warning(f"RECURRENCE-ID for unknown recurring event {uid}, skipping")
            return

        parent_event = event_map[uid]

        if not parent_event.is_recurring:
            logger.warning(f"RECURRENCE-ID for non-recurring event {uid}, skipping")
            return

        recurrence_id = vevent.get("RECURRENCE-ID")
        recurrence_dt = recurrence_id.dt

        # Get the date of the modified instance
        instance_date = (
            recurrence_dt.date() if isinstance(recurrence_dt, datetime) else recurrence_dt
        )

        # Extract modified properties
        dtstart = vevent.get("DTSTART")
        dtend = vevent.get("DTEND")
        new_start = dtstart.dt if dtstart else None
        new_end = dtend.dt if dtend else None

        # Ensure timezone-aware using utility function
        if new_start and isinstance(new_start, datetime):
            new_start = ensure_timezone_aware(new_start, self.config.default_timezone)

        if new_end and isinstance(new_end, datetime):
            new_end = ensure_timezone_aware(new_end, self.config.default_timezone)

        # Create modification
        modification = Modification(
            is_cancelled=False,
            new_start=new_start if isinstance(new_start, datetime) else None,
            new_end=new_end if isinstance(new_end, datetime) else None,
            title_override=str(vevent.get("SUMMARY")) if "SUMMARY" in vevent else None,
            description_override=(
                str(vevent.get("DESCRIPTION")) if "DESCRIPTION" in vevent else None
            ),
            participants_override=None,  # Could extract if needed
        )

        # Add to parent event modifications
        parent_event.set_modification(instance_date, modification)

    def _extract_organizer(self, vevent: icalendar.cal.Component) -> str | None:
        """
        Extract organizer participant ID from ORGANIZER field.

        Args:
            vevent: iCalendar event

        Returns:
            Participant ID or None if not found
        """
        from ..utils.participant_mapper import ParticipantMapper

        organizer = vevent.get("ORGANIZER")
        if not organizer:
            return None

        # Normalize email using ParticipantMapper
        email = ParticipantMapper.normalize_email(str(organizer))

        # Look up in participant map
        return self.config.participant_map.get(email)

    def _extract_participants(
        self,
        vevent: icalendar.cal.Component,
        organizer_id: str,
    ) -> list[str]:
        """
        Extract participant IDs from ATTENDEE fields.

        Args:
            vevent: iCalendar event
            organizer_id: ID of the organizer (always included)

        Returns:
            List of participant IDs
        """
        from ..utils.participant_mapper import ParticipantMapper

        participants = [organizer_id]  # Always include organizer

        attendees = vevent.get("ATTENDEE", [])
        if not isinstance(attendees, list):
            attendees = [attendees]

        for attendee in attendees:
            # Normalize email using ParticipantMapper
            email = ParticipantMapper.normalize_email(str(attendee))

            # Look up in participant map
            participant_id = self.config.participant_map.get(email)
            if participant_id and participant_id not in participants:
                participants.append(participant_id)
            elif not participant_id and not self.config.skip_unknown_attendees:
                logger.warning(f"Unknown attendee: {email}")

        return participants
