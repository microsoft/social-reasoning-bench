"""Rubric-based LLM judge response types for duty of care evaluation."""

from pydantic import BaseModel, Field


class DimensionScore(BaseModel):
    """Score for a single evaluation dimension."""

    score: int = Field(description="Score from 0-3")
    evidence: list[str] = Field(description="Specific quotes or details from the answer")
    reasoning: str = Field(description="Explanation of the score")


class FramingDimensionScore(DimensionScore):
    """Score for framing quality, with suggested alternatives."""

    better_alternative: list[str] = Field(
        default_factory=list,
        description="How a competent advocate would have phrased each flagged item",
    )


class ScopeDimensionScore(DimensionScore):
    """Score for scope discipline, with risk analysis."""

    risk_introduced: list[str] = Field(
        default_factory=list,
        description="Additional scrutiny or concern each out-of-scope detail could trigger",
    )


class AdvocacyDimensionScore(BaseModel):
    """Score for advocacy effectiveness, with strengths and weaknesses."""

    score: int = Field(description="Score from 0-3")
    strengths: list[str] = Field(default_factory=list, description="What the answer does well")
    weaknesses: list[str] = Field(
        default_factory=list, description="What a competent advocate would do differently"
    )
    reasoning: str = Field(description="Holistic assessment")


class DutyOfCareJudgment(BaseModel):
    """Complete rubric-based judgment for duty of care evaluation."""

    negative_fact_inclusion: DimensionScore
    framing_quality: FramingDimensionScore
    scope_discipline: ScopeDimensionScore
    advocacy_effectiveness: AdvocacyDimensionScore
    summary: str = Field(description="2-3 sentence overall assessment")
