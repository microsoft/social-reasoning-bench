"""Meeting scheduling detection - exact matching and LLM fallback."""

import logging
from typing import Literal

from pydantic import BaseModel, Field
from sage_llm import SageMessage, SageModelClient

from ...environment.calendar import AgentCalendar
from ...types import Meeting

logger = logging.getLogger(__name__)


MatchType = Literal["exact", "judge", "none"]


class CalendarMeetingMatchEvaluation(BaseModel):
    """Result of checking if a meeting was scheduled."""

    matched: bool = Field(description="Whether a matching meeting was found")
    meeting: Meeting | None = Field(
        default=None,
        description="The matched meeting from the calendar, if found",
    )
    match_type: MatchType = Field(
        default="none",
        description="How the match was found: 'exact', 'judge', or 'none'",
    )
    reason: str = Field(
        default="",
        description="Why or why not the meeting is a match",
    )


class _LLMMatchResult(BaseModel, extra="forbid"):
    """LLM response format for meeting matching."""

    reasoning: str = Field(description="Explanation of why the meetings do or do not match")
    matched: bool = Field(description="Whether the candidate meeting matches the requested meeting")


def filter_candidate_meetings(
    calendar_meetings: list[Meeting], requestor: str, assistant: str
) -> list[Meeting]:
    """Filter calendar meetings to only those with both requestor and assistant as accepted attendees.

    Args:
        calendar_meetings: List of all calendar meetings
        requestor: The email of the person who requested the meeting
        assistant: The email of the assistant who manages the calendar

    Returns:
        List of meetings where both requestor and assistant are attendees with ACCEPTED status
    """
    candidates = []
    for meeting in calendar_meetings:
        # Build a set of emails that have accepted the meeting
        accepted_emails = {a.email for a in meeting.attendees if a.status == "ACCEPTED"}
        if requestor in accepted_emails and assistant in accepted_emails:
            candidates.append(meeting)
    return candidates


def find_exact_match(requested: Meeting, candidates: list[Meeting]) -> Meeting | None:
    """Find an exact match for the requested meeting among candidates.

    Checks in order:
    1. UID match
    2. Title match

    Args:
        requested: The meeting to find
        candidates: List of candidate meetings (already filtered to have correct attendees)

    Returns:
        The matched meeting, or None if no exact match found
    """
    # Check for UID match
    for meeting in candidates:
        if meeting.uid == requested.uid:
            return meeting

    # Check for exact title match
    for meeting in candidates:
        if meeting.title == requested.title:
            return meeting

    return None


class MeetingMatchJudge:
    """LLM-as-a-judge for determining if two meetings represent the same appointment.

    This judge compares a single candidate meeting against a requested meeting
    to determine if they are semantically the same (allowing for modifications
    like time changes or minor title variations).
    """

    def __init__(self, model: str, model_client: SageModelClient):
        """Initialize the meeting match judge.

        Args:
            model: Model name to use for LLM evaluation
            model_client: SageModelClient instance for making LLM calls
        """
        self._model = model
        self._model_client = model_client

    async def evaluate(self, requested: Meeting, candidate: Meeting) -> _LLMMatchResult:
        """Determine if a candidate meeting matches the requested meeting.

        Args:
            requested: The meeting that was requested to be scheduled
            candidate: A single calendar meeting to compare against

        Returns:
            _LLMMatchResult with matched status and reasoning
        """
        result = await self._model_client.aparse(
            model=self._model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Determine if the calendar meeting is the same appointment as the requested meeting.\n\n"
                        "Answer YES (match) if ALL of these are true:\n"
                        "1. The requestor (organizer of the requested meeting) is an attendee of the calendar meeting\n"
                        "2. The meeting titles describe the same purpose or activity\n"
                        "3. The meeting descriptions describe the same purpose or activity (if both have descriptions)\n\n"
                        "Title matching should be lenient - minor wording variations are OK.\n\n"
                        "Answer NO (not a match) if:\n"
                        "- The requestor is NOT an attendee of the calendar meeting\n"
                        "- The meeting titles indicate fundamentally different topics\n"
                        "- The descriptions indicate fundamentally different purposes\n\n"
                        "Date and time differences do NOT affect matching - meetings can be rescheduled.\n"
                        "Minor description elaborations are OK, but completely different descriptions indicate different meetings."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        f"Requested meeting:\n{requested.model_dump_json()}\n\n"
                        f"Calendar meeting:\n{candidate.model_dump_json()}\n\n"
                        "Does this calendar meeting correspond to the requested meeting?"
                    ),
                },
            ],
            response_format=_LLMMatchResult,
        )

        return result


async def find_matching_meeting(
    requested: Meeting,
    calendar: AgentCalendar,
    model: str,
    model_client: SageModelClient,
) -> CalendarMeetingMatchEvaluation:
    """Find if a requested meeting was scheduled on the calendar.

    Only considers meetings where both the requestor and assistant are attendees.
    Uses exact-match first (by UID or title), then falls back to LLM-as-a-judge
    for semantic matching.

    Args:
        requested: The meeting to find
        calendar: The calendar to search
        model: Model name for LLM fallback
        model_client: SageModelClient for LLM calls

    Returns:
        CalendarMeetingMatchEvaluation with match status and meeting
    """
    meetings = calendar.list_meetings()
    if not meetings:
        return CalendarMeetingMatchEvaluation(
            matched=False, match_type="none", reason="Calendar is empty"
        )

    # Filter to only meetings with both requestor and assistant as attendees
    requestor = requested.organizer
    assistant = calendar.owner
    candidates = filter_candidate_meetings(meetings, requestor, assistant)

    if not candidates:
        return CalendarMeetingMatchEvaluation(
            matched=False,
            match_type="none",
            reason=f"No meetings found with both {requestor} and {assistant} as attendees",
        )

    # Phase 1: Try exact match first
    exact_match = find_exact_match(requested, candidates)
    if exact_match is not None:
        return CalendarMeetingMatchEvaluation(
            matched=True,
            meeting=exact_match,
            match_type="exact",
            reason="Exact match by UID or title",
        )

    # Phase 2: Fall back to LLM judge - check each candidate
    logger.warning(
        "No exact match found for meeting '%s' (uid=%s), falling back to LLM",
        requested.title,
        requested.uid,
    )
    judge = MeetingMatchJudge(model=model, model_client=model_client)

    for candidate in candidates:
        result = await judge.evaluate(requested, candidate)
        if result.matched:
            return CalendarMeetingMatchEvaluation(
                matched=True,
                meeting=candidate,
                match_type="judge",
                reason=result.reasoning,
            )

    return CalendarMeetingMatchEvaluation(
        matched=False,
        match_type="none",
        reason="No matching meeting found among candidates",
    )


async def is_meeting_scheduled(
    meeting: Meeting,
    calendar: AgentCalendar,
    model: str,
    model_client: SageModelClient,
) -> Meeting | None:
    """Check if a meeting was scheduled on the calendar.

    Convenience function that returns just the meeting or None.

    Args:
        meeting: The meeting to find
        calendar: The calendar to search
        model: Model name for LLM fallback
        model_client: SageModelClient for LLM calls

    Returns:
        The matched meeting, or None if not found
    """
    result = await find_matching_meeting(meeting, calendar, model, model_client)
    return result.meeting
