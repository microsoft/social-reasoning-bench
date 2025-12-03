"""Core entity definitions for calendar_gym.

All entities are Pydantic models that serve dual purposes:
1. Domain objects for representing calendar data
2. LLM structured generation response schemas
"""

from datetime import date
from enum import Enum

from pydantic import AwareDatetime, BaseModel, Field, model_validator

# ============================================================================
# Time Range Model
# ============================================================================


class TimeRange(BaseModel):
    """Represents a date or datetime range."""

    start: AwareDatetime = Field(description="Start of the time range (inclusive)")
    end: AwareDatetime = Field(description="End of the time range (exclusive)")

    def contains_date(self, d: date) -> bool:
        """Check if a date falls within this range."""
        start_date = self.start.date()
        end_date = self.end.date()
        return start_date <= d <= end_date

    def overlaps(self, other: "TimeRange") -> bool:
        """Check if this range overlaps with another range."""
        return self.start <= other.end and other.start <= self.end

    def duration_minutes(self) -> int:
        """Get the duration in minutes."""
        delta = self.end - self.start
        return int(delta.total_seconds() / 60)


# ============================================================================
# Enums
# ============================================================================


class Frequency(str, Enum):
    """Recurrence frequency options."""

    DAILY = "DAILY"
    WEEKLY = "WEEKLY"
    MONTHLY = "MONTHLY"
    YEARLY = "YEARLY"


class DayOfWeek(str, Enum):
    """Days of the week."""

    MONDAY = "MONDAY"
    TUESDAY = "TUESDAY"
    WEDNESDAY = "WEDNESDAY"
    THURSDAY = "THURSDAY"
    FRIDAY = "FRIDAY"
    SATURDAY = "SATURDAY"
    SUNDAY = "SUNDAY"


class Month(int, Enum):
    """Months of the year."""

    JANUARY = 1
    FEBRUARY = 2
    MARCH = 3
    APRIL = 4
    MAY = 5
    JUNE = 6
    JULY = 7
    AUGUST = 8
    SEPTEMBER = 9
    OCTOBER = 10
    NOVEMBER = 11
    DECEMBER = 12


class EndType(str, Enum):
    """How a recurrence pattern ends."""

    NEVER = "NEVER"
    UNTIL_DATE = "UNTIL_DATE"
    COUNT = "COUNT"


# ============================================================================
# Recurrence Models
# ============================================================================


class EndCondition(BaseModel):
    """Defines when a recurring series ends."""

    type: EndType = Field(description="How the recurrence ends")
    until_date: date | None = Field(
        default=None,
        description="End date (inclusive) for UNTIL_DATE type",
    )
    count: int | None = Field(
        default=None,
        description="Number of occurrences for COUNT type",
    )

    @model_validator(mode="after")
    def validate_end_condition(self) -> "EndCondition":
        """Validate end condition after initialization."""
        if self.type == EndType.UNTIL_DATE and self.until_date is None:
            raise ValueError("until_date required for UNTIL_DATE end condition")
        if self.type == EndType.COUNT and self.count is None:
            raise ValueError("count required for COUNT end condition")
        return self


class RecurrenceRule(BaseModel):
    """Defines a recurrence pattern for a series."""

    frequency: Frequency = Field(description="How often the event recurs")
    interval: int = Field(
        default=1,
        description="Repeat every N periods (e.g., every 2 weeks)",
        ge=1,
    )
    by_day: list[DayOfWeek] | None = Field(
        default=None,
        description="Specific days of the week (for WEEKLY frequency)",
    )
    by_month_day: list[int] | None = Field(
        default=None,
        description="Specific days of month (1-31), e.g., [1, 15] for 1st and 15th",
    )
    by_month: list[Month] | None = Field(
        default=None,
        description="Specific months (for YEARLY frequency)",
    )
    by_set_pos: list[int] | None = Field(
        default=None,
        description=(
            "Select specific occurrences within the recurrence set (e.g., [1] for first, [-1] for last, "
            "[2, 4] for 2nd and 4th). Use with by_day for patterns like 'first Monday of month'."
        ),
    )
    end_condition: EndCondition = Field(
        description="When the recurrence ends",
    )

    @model_validator(mode="after")
    def validate_recurrence_fields(self) -> "RecurrenceRule":
        """Validate recurrence rule fields."""
        # Validate by_month_day values
        if self.by_month_day:
            for day in self.by_month_day:
                if not 1 <= day <= 31:
                    raise ValueError(f"by_month_day values must be 1-31, got {day}")

        # Validate by_set_pos values
        if self.by_set_pos:
            for pos in self.by_set_pos:
                if pos == 0 or pos < -366 or pos > 366:
                    raise ValueError(
                        f"by_set_pos values must be -366 to 366 (excluding 0), got {pos}"
                    )

        return self


# ============================================================================
# Modification Model
# ============================================================================


class Modification(BaseModel):
    """Represents instance-level modifications to a recurring series.

    Stored in Series.instance_modifications keyed by date.
    """

    is_cancelled: bool = Field(
        default=False,
        description="Whether this instance is cancelled",
    )
    new_start: AwareDatetime | None = Field(
        default=None,
        description="Override start time for this instance",
    )
    new_end: AwareDatetime | None = Field(
        default=None,
        description="Override end time for this instance",
    )
    title_override: str | None = Field(
        default=None,
        description="Override title for this instance",
    )
    description_override: str | None = Field(
        default=None,
        description="Override description for this instance",
    )
    participants_override: list[str] | None = Field(
        default=None,
        description="Override participant IDs for this instance",
    )


# ============================================================================
# Participant Model
# ============================================================================


class ParticipantProfile(BaseModel):
    """Profile for a calendar participant.

    Extends the concept of AgentProfile from magentic-marketplace.
    """

    id: str = Field(description="Unique participant identifier")
    name: str = Field(description="Participant's display name")
    description: str = Field(
        description="Role, responsibilities, and personality traits",
    )
    goal: str | None = Field(
        default=None,
        description="Participant's goal related to the scenario",
    )
    timezone: str = Field(
        description="IANA timezone (e.g., 'America/New_York')",
    )


# ============================================================================
# Calendar Event Models
# ============================================================================


class Event(BaseModel):
    """A calendar event (standalone, series parent, or series instance).

    Event Types:
    - Standalone: recurrence_rule=None, id={uuid}
    - Series parent: recurrence_rule=<rule>, id={uuid}
    - Series instance: recurrence_rule=None, id={parent_id}_{YYYY-MM-DD}
    """

    id: str = Field(description="Unique event identifier")
    recurrence_rule: RecurrenceRule | None = Field(
        default=None,
        description="Recurrence pattern if this is a series parent, None otherwise",
    )
    start_datetime: AwareDatetime = Field(description="Event start time (timezone-aware)")
    end_datetime: AwareDatetime = Field(description="Event end time (timezone-aware)")
    title: str = Field(description="Event title")
    description: str = Field(description="Event description")
    organizer_id: str = Field(description="ID of the participant who organized/created this event")
    participants: list[str] = Field(
        description="List of participant IDs (attendees/invitees, including organizer)",
        default_factory=list,
    )
    instance_modifications: dict[str, Modification] | None = Field(
        default=None,
        description="Instance-level modifications keyed by date (ISO format), only for series parents",
    )

    @property
    def event_date(self) -> date:
        """Event date derived from start_datetime."""
        return self.start_datetime.date()

    @property
    def duration_minutes(self) -> int:
        """Calculate event duration in minutes."""
        delta = self.end_datetime - self.start_datetime
        return int(delta.total_seconds() / 60)

    @property
    def is_recurring(self) -> bool:
        """Check if this is a recurring series parent."""
        return self.recurrence_rule is not None

    @property
    def is_series_instance(self) -> bool:
        """Check if this is an instance of a series (ID format: parent_id_YYYY-MM-DD)."""
        from .utils.event_utils import parse_instance_id

        return parse_instance_id(self.id) is not None

    @property
    def parent_id(self) -> str | None:
        """Get the parent event ID if this is a series instance."""
        from .utils.event_utils import parse_instance_id

        parsed = parse_instance_id(self.id)
        return parsed[0] if parsed else None

    def get_modification(self, d: date) -> Modification | None:
        """Get modification for a specific date if it exists (for series parents)."""
        if self.instance_modifications is None:
            return None
        return self.instance_modifications.get(d.isoformat())

    def set_modification(self, d: date, modification: Modification) -> None:
        """Set modification for a specific date (for series parents)."""
        if self.instance_modifications is None:
            self.instance_modifications = {}
        self.instance_modifications[d.isoformat()] = modification

    def is_cancelled(self, d: date) -> bool:
        """Check if a specific instance is cancelled (for series parents)."""
        mod = self.get_modification(d)
        return mod.is_cancelled if mod else False

    def overlaps(self, other: "Event") -> bool:
        """Check if this event overlaps with another event."""
        from .utils.dates import events_overlap

        return events_overlap(
            self.start_datetime,
            self.end_datetime,
            other.start_datetime,
            other.end_datetime,
        )
