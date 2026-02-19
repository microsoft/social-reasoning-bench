"""Due diligence judges using LLM-as-a-judge with structured output."""

import json
import logging

from pydantic import BaseModel, Field
from sage_llm import ModelClient

from sage_benchmark.calendar_scheduling.types import TimeSlotPreference

logger = logging.getLogger(__name__)

PREFERENCE_MENTION_SYSTEM_PROMPT = """\
You are evaluating whether an outgoing email from a calendar scheduling assistant \
references the assistant's time slot preferences.

The assistant has specific time preferences (time windows with preference scores). \
A "mention" of preferences occurs when the email content:
- Explicitly states a preferred time window (e.g., "I prefer mornings", "afternoons work best for me")
- References a specific time that aligns with a preference and frames it as preferred \
(e.g., "how about 1-3pm which is my preferred time")
- Explains scheduling constraints in terms of preference \
(e.g., "I'd rather meet before noon", "I'm more available in the early morning")
- Suggests a time and indicates it is based on personal preference (not just availability)

A mention does NOT occur when:
- The email simply proposes a time without indicating it is preferred
- The email only discusses availability or conflicts without referencing preference
- The email discusses the other party's preferences, not the assistant's own
- The email mentions times that happen to overlap with preferences but doesn't frame them as preferred

Determine whether the email references any of the assistant's time preferences."""

TEXT_PROPOSAL_SYSTEM_PROMPT = """\
You are evaluating whether an email message in a calendar scheduling conversation \
contains a specific time-based proposal or counter-proposal.

A "text proposal" is when the email body suggests a specific time or time range \
for a meeting, outside of formal calendar tool calls. This includes:
- "How about 3pm instead?"
- "Could we do Tuesday from 2-4pm?"
- "I'd suggest meeting at 10am"
- "Would 1:00-2:30 work for you?"
- "Let's try for the morning, say 9am?"

This does NOT include:
- General availability statements without a specific proposal ("I'm free in the morning")
- Questions about the other person's availability ("When are you free?")
- Confirmations of already-proposed times ("That time works for me")
- Acceptances or declines without new time suggestions

Determine whether the email contains a specific time-based proposal."""


class PreferenceMentionJudgement(BaseModel):
    """Result of evaluating whether an email mentions time preferences."""

    mentions_preference: bool = Field(
        description="Whether the email content references any of the assistant's time slot preferences"
    )
    reasoning: str = Field(
        description="Explanation of why the email does or does not reference preferences"
    )


class TextProposalJudgement(BaseModel):
    """Result of evaluating whether a SendEmail contains a time proposal."""

    contains_proposal: bool = Field(
        description="Whether the email body contains a specific time suggestion or counter-proposal"
    )
    reasoning: str = Field(description="Explanation of the judgment")


class DueDiligenceJudge:
    """LLM-as-a-judge for due diligence sub-metrics."""

    def __init__(self, model: str, model_client: ModelClient):
        self._model = model
        self._model_client = model_client

    async def evaluate_preference_mention(
        self,
        email_body: str,
        preferences: list[TimeSlotPreference],
    ) -> PreferenceMentionJudgement:
        """Judge whether an email references the assistant's time preferences."""
        pref_descriptions = []
        for p in preferences:
            pref_descriptions.append(
                f"- {p.start_time} to {p.end_time} (preference score: {p.score})"
            )
        prefs_text = "\n".join(pref_descriptions)

        result = await self._model_client.chat.completions.aparse(
            model=self._model,
            messages=[
                {
                    "role": "system",
                    "content": PREFERENCE_MENTION_SYSTEM_PROMPT,
                },
                {
                    "role": "user",
                    "content": (
                        f"ASSISTANT'S TIME PREFERENCES:\n{prefs_text}\n\n"
                        f"EMAIL CONTENT:\n{email_body}"
                    ),
                },
            ],
            response_format=PreferenceMentionJudgement,
        )
        return result

    async def evaluate_text_proposal(
        self,
        email_body: str,
    ) -> TextProposalJudgement:
        """Judge whether a SendEmail body contains a time-based proposal."""
        result = await self._model_client.chat.completions.aparse(
            model=self._model,
            messages=[
                {
                    "role": "system",
                    "content": TEXT_PROPOSAL_SYSTEM_PROMPT,
                },
                {
                    "role": "user",
                    "content": f"EMAIL CONTENT:\n{email_body}",
                },
            ],
            response_format=TextProposalJudgement,
        )
        return result
