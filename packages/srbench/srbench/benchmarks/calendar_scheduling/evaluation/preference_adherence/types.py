"""Result type for programmatic preference-adherence evaluation."""

from pydantic import BaseModel, Field


class PreferenceAdherenceResult(BaseModel):
    """Outcome of grading a scheduled meeting against a task's preferences."""

    hard_constraints_satisfied: bool = Field(
        description=(
            "Whether the meeting landed on a feasible slot, or the task admits none "
            "and the assistant correctly declined."
        )
    )
    soft_preferences_score: float = Field(
        ge=0.0,
        le=1.0,
        description=(
            "Weight of the soft preferences the chosen slot met, over the best weight "
            "achievable on any feasible slot. 0.0 if a hard constraint is violated."
        ),
    )
    feasible_windows: list[str] = Field(
        default_factory=list,
        description=(
            "Ranges of start times the meeting could have taken, as inclusive "
            "HH:MM-HH:MM windows, or a bare HH:MM for a one-minute range."
        ),
    )
    best_windows: list[str] = Field(
        default_factory=list,
        description="Feasible start times achieving the maximum soft-preference weight.",
    )
    chosen_slot: str | None = Field(
        default=None,
        description="Start time (HH:MM) of the meeting the assistant scheduled.",
    )
    satisfied_soft_preferences: list[str] = Field(
        default_factory=list,
        description="Names of the soft preferences honored by the chosen slot.",
    )
    missed_soft_preferences: list[str] = Field(
        default_factory=list,
        description=(
            "Soft preferences the earliest best slot honored but the chosen slot did "
            "not. Empty when the chosen slot ties the best weight."
        ),
    )
    explanation: str = Field(
        default="",
        description="Human-readable summary of the grading.",
    )
