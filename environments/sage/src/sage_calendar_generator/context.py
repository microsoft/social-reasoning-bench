"""Context classes for propagating information through the generation pipeline.

Each context class represents the information available to a generator at a
specific phase of the pipeline. Context flows downward, with each phase adding
more information for subsequent phases.
"""

from typing import Any

from pydantic import BaseModel, Field
from sage_protocol.calendar.entities import Event, ParticipantProfile, TimeRange

from .entities import GoalEvent, Scenario


class ScenarioContext(BaseModel):
    """Context for scenario generation (Phase 1).

    This is the initial context with just the generation parameters.
    """

    num_participants: int = Field(description="Number of participants to generate")
    scenario_hint: str | None = Field(
        default=None,
        description="Optional theme/hint for scenario",
    )
    seed: int | None = Field(default=None, description="Random seed")


class ParticipantContext(BaseModel):
    """Context for participant generation (Phase 2).

    Includes scenario description and existing participants for coherence.
    """

    scenario_description: str = Field(description="The scenario being generated")
    num_participants: int = Field(description="Total participants to generate")
    existing_participants: list[ParticipantProfile] = Field(
        default_factory=list,
        description="Participants already generated",
    )
    timezone_hint: str = Field(
        description="Timezone this participant should use",
    )
    participant_index: int = Field(
        description="Index of this participant (0-based)",
    )
    has_goal: bool = Field(
        default=False,
        description="Whether this participant has a goal related to the scenario",
    )
    email_hint: str | None = Field(
        default=None,
        description="Email address hint for generating participant details",
    )


class GoalEventContext(BaseModel):
    """Context for goal event generation (Phase 3).

    Includes complete scenario and designated organizer/attendees.
    """

    scenario_description: str = Field(description="The scenario description")
    organizer: ParticipantProfile = Field(description="The organizing participant")
    required_attendees: list[ParticipantProfile] = Field(
        description="Participants who must attend",
    )
    duration_minutes: int = Field(description="Expected event duration")
    seed_range: TimeRange = Field(
        description="Date range for potential scheduling",
    )


class BlockingEventContext(BaseModel):
    """Context for generating blocking events (Phase 4).

    Creates conflicts that overlap with the goal event's scheduled time.
    """

    scenario_description: str = Field(description="The scenario description")
    participant: ParticipantProfile = Field(
        description="Participant whose calendar is being populated",
    )
    goal_event: GoalEvent = Field(
        description="The goal event with scheduled time - conflicts must overlap this"
    )
    date_range: TimeRange = Field(
        description="Range to generate blocking events in",
    )
    num_blocking_events: int = Field(
        description="Number of blocking events to create",
        ge=1,
    )


class BaselineCalendarContext(BaseModel):
    """Context for baseline calendar generation (Phase 5).

    Populates calendars with realistic recurring series and standalone events.
    """

    scenario_description: str = Field(description="The scenario description")
    participant: ParticipantProfile = Field(
        description="Participant whose calendar is being populated",
    )
    existing_events: list[Event] = Field(
        default_factory=list,
        description="Events already on this participant's calendar (e.g., blocking events)",
    )
    date_range: TimeRange = Field(
        description="Range to populate with events",
    )
    target_series_count: int = Field(
        description="Target number of recurring series to create",
        ge=3,
        le=7,
    )
    target_event_density: float = Field(
        description="Target percentage of work hours filled (0.0-1.0)",
        ge=0.1,
        le=0.9,
    )


class GenerationContext(BaseModel):
    """Root context that persists throughout the entire generation process.

    Stores shared state like LLM messages and intermediate results.
    """

    messages: list[dict[str, Any]] = Field(
        default_factory=list,
        description="Shared LLM conversation history",
    )
    scenario: Scenario | None = Field(
        default=None,
        description="Scenario being generated (populated incrementally)",
    )
    seed_range: TimeRange | None = Field(
        default=None,
        description="Date range for seed data",
    )
    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Additional generation metadata",
    )
