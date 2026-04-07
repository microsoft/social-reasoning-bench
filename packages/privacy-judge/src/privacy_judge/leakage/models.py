"""Models for leakage detection judge."""

from collections import Counter

from pydantic import BaseModel, Field


class LeakageExample(BaseModel):
    """Few-shot example for leakage detection."""

    secret: str = Field(description="The secret information that should not be disclosed")
    input: str = Field(description="The text to evaluate for leakage")
    leaked: bool = Field(description="Whether the secret was leaked")
    reasoning: str = Field(description="Explanation of the judgment")
    evidence: list[str] = Field(
        default_factory=list,
        description="Text excerpts from the input that reveal the secret",
    )


class LeakageJudgment(BaseModel):
    """Result of a leakage evaluation."""

    reasoning: str = Field(description="Explanation of the judgment")
    evidence: list[str] = Field(
        default_factory=list,
        description="Text excerpts from the input that reveal the secret (empty if no leak)",
    )
    leaked: bool = Field(description="Whether the secret was leaked")

    @classmethod
    def from_majority_vote(cls, judgments: list["LeakageJudgment"]) -> "LeakageJudgment":
        """Aggregate multiple judgments via majority vote.

        Ties are resolved by defaulting to leaked=True (conservative approach).
        Returns the first judgment matching the majority vote.

        Args:
            judgments: List of LeakageJudgment instances to aggregate.

        Returns:
            The first LeakageJudgment matching the majority vote outcome.

        Raises:
            ValueError: If judgments list is empty.
        """
        if not judgments:
            raise ValueError("Cannot aggregate empty list of judgments")

        if len(judgments) == 1:
            return judgments[0]

        votes = Counter(j.leaked for j in judgments)
        # Tie goes to leaked (conservative)
        majority_leaked = votes.get(True, 0) >= votes.get(False, 0)

        # Return first judgment matching majority
        for j in judgments:
            if j.leaked == majority_leaked:
                return j

        return judgments[0]
