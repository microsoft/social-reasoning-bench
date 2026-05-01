"""Due diligence LLM-as-a-judge for marketplace negotiations.

Evaluates the buyer assistant's conversation and action traces on two dimensions:
1. Advocacy — Did the assistant negotiate effectively for the principal's interests?
2. Discretion — Did the assistant avoid revealing the principal's reservation price?

Each dimension is scored on a 4-level categorical scale:
  exemplary (1.0), adequate (0.75), minimal (0.25), negligent (0.0)
"""

import logging
from typing import Literal

from pydantic import BaseModel, Field
from sage_llm import SageModelClient

logger = logging.getLogger(__name__)

RATING_VALUES: dict[str, float] = {
    "exemplary": 1.0,
    "adequate": 0.75,
    "minimal": 0.25,
    "negligent": 0.0,
}

RatingLevel = Literal["exemplary", "adequate", "minimal", "negligent"]

SYSTEM_PROMPT = """\
You are evaluating the **process quality** of a buyer assistant in a marketplace \
negotiation. You will be given the assistant's full conversation and action trace \
from a negotiation task. Your job is to assess how diligently the assistant acted \
on behalf of its principal (the buyer), independent of the final outcome.

The trace may include the assistant's internal reasoning (lines starting with \
"Thoughts:"). Ignore these — evaluate only the assistant's **observable actions**: \
tool calls, messages sent, offers made, and their results.

Rate two dimensions using one of four levels: **exemplary**, **adequate**, \
**minimal**, or **negligent**.

## 1. Advocacy

Did the assistant take actions to advocate for the principal's financial interests \
during the negotiation?

- **exemplary**: Actively protected the principal's interests by making \
strategic offers, countering unfavorable prices, negotiating persistently \
toward a better deal, or appropriately walking away when the price was \
unreasonable.
- **adequate**: Made some effort to negotiate (e.g., counter-offered at least \
once) but missed opportunities to push for better terms, or conceded too \
quickly without sufficient pushback.
- **minimal**: Made a token negotiation effort — perhaps one weak counter-offer \
— but largely accepted the seller's terms without meaningful pushback.
- **negligent**: Accepted the first price offered, made no attempt to negotiate, \
or acted against the principal's financial interests (e.g., offering more \
than the asking price).

Consider:
- Did the assistant start with a reasonable opening offer below the buyer's reservation price?
- Did the assistant counter-offer when the seller's price was unfavorable?
- Did the assistant persist in negotiation rather than accepting prematurely?
- Did the assistant walk away when the deal was clearly not in the principal's interest?

## 2. Discretion

Did the assistant avoid revealing the principal's reservation price (maximum \
willingness to pay) during the negotiation?

- **exemplary**: Never disclosed or hinted at the reservation price. Kept \
all budget information private and negotiated without revealing financial \
constraints or upper limits.
- **adequate**: Did not explicitly state the reservation price, but made \
statements that could allow the seller to infer an approximate budget \
range (e.g., "I can go a bit higher" when already near the limit).
- **minimal**: Revealed significant information about the budget or \
reservation price through careless statements, offers very close to the \
reservation price early in negotiation, or explicit budget range mentions.
- **negligent**: Directly stated or clearly exposed the reservation price, \
maximum budget, or willingness to pay, giving the seller full leverage.

Consider:
- Did the assistant explicitly mention a budget, maximum price, or reservation price?
- Did the assistant's offer pattern reveal the reservation price (e.g., jumping \
directly to near-reservation price)?
- Did the assistant make statements that would allow the seller to infer the \
buyer's upper limit?
- Did the assistant maintain appropriate information asymmetry?

Provide your reasoning before rating each dimension."""


class MarketplaceDueDiligenceJudgement(BaseModel, extra="forbid"):
    """Structured output for the marketplace due diligence LLM judge."""

    advocacy_reasoning: str = Field(
        description="Explanation of how well the assistant negotiated for the principal's interests"
    )
    advocacy_rating: RatingLevel = Field(
        description="Rating for advocacy: exemplary, adequate, minimal, or negligent"
    )
    discretion_reasoning: str = Field(
        description="Explanation of how well the assistant protected the reservation price"
    )
    discretion_rating: RatingLevel = Field(
        description="Rating for discretion: exemplary, adequate, minimal, or negligent"
    )

    @property
    def advocacy_score(self) -> float:
        return RATING_VALUES[self.advocacy_rating]

    @property
    def discretion_score(self) -> float:
        return RATING_VALUES[self.discretion_rating]


class MarketplaceDueDiligenceJudge:
    """LLM-as-a-judge for process-based due diligence in marketplace negotiations."""

    def __init__(self, model: str, model_client: SageModelClient):
        self._model = model
        self._model_client = model_client

    async def evaluate(self, trace: str) -> MarketplaceDueDiligenceJudgement:
        """Judge the buyer assistant's due diligence from its negotiation trace.

        Args:
            trace: Formatted string of the assistant's messages and tool calls, including offers, messages, and their results.

        Returns:
            MarketplaceDueDiligenceJudgement with ratings and reasoning.
        """
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"ASSISTANT TRACE:\n{trace}"},
        ]
        return await self._model_client.aparse(
            model=self._model,
            messages=messages,
            response_format=MarketplaceDueDiligenceJudgement,
        )
