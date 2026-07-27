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
    soft_constraints_score: float = Field(
        ge=0.0,
        le=1.0,
        description=(
            "Weight of the soft preferences the chosen slot met, over the best weight "
            "achievable on any feasible slot. 0.0 if a hard constraint is violated."
        ),
    )
    feasible_slots: list[str] = Field(
        default_factory=list,
        description=(
            "Representative feasible start times (HH:MM), including every time at which "
            "feasibility or soft-preference adherence can change."
        ),
    )
    best_slots: list[str] = Field(
        default_factory=list,
        description="Feasible start times achieving the maximum soft-preference weight.",
    )
    chosen_slot: str | None = Field(
        default=None,
        description="Start time (HH:MM) of the meeting the assistant scheduled.",
    )
    satisfied_soft_constraints: list[str] = Field(
        default_factory=list,
        description="Names of the soft preferences honoured by the chosen slot.",
    )
    missed_soft_constraints: list[str] = Field(
        default_factory=list,
        description=(
            "Soft preferences the earliest best slot honoured but the chosen slot did "
            "not. Empty when the chosen slot ties the best weight."
        ),
    )
    explanation: str = Field(
        default="",
        description="Human-readable summary of the grading.",
    )
