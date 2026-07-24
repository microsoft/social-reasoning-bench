"""Result type for programmatic preference-adherence evaluation."""

from __future__ import annotations

from pydantic import BaseModel, Field


class PreferenceAdherenceResult(BaseModel):
    """Outcome of grading a scheduled meeting against a task's preferences."""

    hard_constraints_satisfied: bool = Field(
        description=(
            "True iff the meeting landed on a slot that is free for both parties and "
            "respects every hard constraint, or the task admits no such slot and the "
            "assistant correctly declined to schedule."
        )
    )
    soft_constraints_score: float = Field(
        ge=0.0,
        le=1.0,
        description=(
            "Soft-preference adherence in [0, 1]: the weight of soft preferences met "
            "by the chosen slot divided by the best weight achievable on any feasible "
            "slot. 0.0 whenever a hard constraint is violated."
        ),
    )
    feasible_slots: list[str] = Field(
        default_factory=list,
        description="Start times (HH:MM) free for both parties that satisfy all hard constraints.",
    )
    best_slots: list[str] = Field(
        default_factory=list,
        description="Feasible start times achieving the maximum soft-preference weight.",
    )
    chosen_slot: str | None = Field(
        default=None, description="Start time (HH:MM) of the meeting the assistant scheduled."
    )
    satisfied_soft_constraints: list[str] = Field(
        default_factory=list,
        description="Names of the soft preferences honoured by the chosen slot.",
    )
    missed_soft_constraints: list[str] = Field(
        default_factory=list,
        description="Names of the soft preferences a better feasible slot would have honoured.",
    )
    explanation: str = Field(default="", description="Human-readable summary of the grading.")
