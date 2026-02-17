"""Generation-specific entity definitions.

These models are used exclusively by the generation system and are separate
from the core calendar entities in sage_protocol.calendar.
"""

from pydantic import AwareDatetime, BaseModel, Field, model_validator
from sage_protocol.calendar.entities import ParticipantProfile, TimeRange

# ============================================================================
# Goal Event Model
# ============================================================================


class GoalEvent(BaseModel):
    """The goal event that participants need to coordinate.

    This event has a specific scheduled time, and conflicts are generated
    to block this exact slot.
    """

    title: str = Field(description="Goal event title")
    description: str = Field(description="Goal event description and purpose")
    scheduled_start: AwareDatetime = Field(
        description="The specific scheduled start time for the goal event"
    )
    scheduled_end: AwareDatetime = Field(
        description="The specific scheduled end time for the goal event"
    )
    organizer_id: str = Field(description="ID of the organizing participant")
    required_attendees: list[str] = Field(
        description="Participant IDs who must attend",
        min_length=2,
    )

    @property
    def duration_minutes(self) -> int:
        """Calculate duration from scheduled times."""
        delta = self.scheduled_end - self.scheduled_start
        return int(delta.total_seconds() / 60)


# ============================================================================
# Scenario Model
# ============================================================================


class Scenario(BaseModel):
    """Complete scenario definition with participants and goal.

    This is the top-level object produced by the generation system.
    """

    description: str = Field(
        description="High-level scenario description and context",
    )
    participants: list[ParticipantProfile] = Field(
        description="All participants in the scenario",
        min_length=2,
    )
    goal_event: GoalEvent = Field(
        description="The event to be scheduled",
    )
    organizer_id: str = Field(
        description="ID of the participant organizing the goal event",
    )

    def get_participant(self, participant_id: str) -> ParticipantProfile | None:
        """Get a participant by ID."""
        for p in self.participants:
            if p.id == participant_id:
                return p
        return None

    def get_organizer(self) -> ParticipantProfile | None:
        """Get the organizer participant."""
        return self.get_participant(self.organizer_id)


# ============================================================================
# Generation Parameters
# ============================================================================


class LLMConfig(BaseModel):
    """Configuration for LLM-based generation."""

    model: str = Field(
        default="gpt-4-turbo-preview",
        description="OpenAI model to use",
    )
    temperature: float | None = Field(
        default=None,
        description="Sampling temperature",
        ge=0.0,
        le=2.0,
    )
    max_tokens: int | None = Field(
        default=None,
        description="Maximum tokens in response",
    )
    api_key: str | None = Field(
        default=None,
        description="OpenAI API key (defaults to OPENAI_API_KEY env var)",
    )


class GenerationParams(BaseModel):
    """Parameters for scenario generation."""

    num_participants: int = Field(
        description="Number of participants to generate",
        ge=2,
        le=10,
    )
    timezone_distribution: dict[str, int] = Field(
        description="Map of timezone to number of participants (e.g., {'America/New_York': 2, 'Europe/London': 1})",
    )
    seed_days: int = Field(
        description="Number of days to pre-generate in calendars",
        ge=1,
        le=90,
    )
    goal_event_size: int = Field(
        description="Number of required attendees for goal event",
        ge=2,
    )
    scenario_hint: str | None = Field(
        default=None,
        description="Optional hint/theme for scenario generation",
    )
    llm_config: LLMConfig = Field(
        default_factory=LLMConfig,
        description="LLM configuration",
    )
    seed: int | None = Field(
        default=None,
        description="Random seed for reproducibility",
    )

    @model_validator(mode="after")
    def validate_parameters(self) -> "GenerationParams":
        """Validate parameters after initialization."""
        # Check timezone distribution sums to num_participants
        total = sum(self.timezone_distribution.values())
        if total != self.num_participants:
            raise ValueError(
                f"timezone_distribution sum ({total}) must equal num_participants ({self.num_participants})"
            )

        # Check goal_event_size doesn't exceed participants
        if self.goal_event_size > self.num_participants:
            raise ValueError(
                f"goal_event_size ({self.goal_event_size}) cannot exceed num_participants ({self.num_participants})"
            )

        return self
