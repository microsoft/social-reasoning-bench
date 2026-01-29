"""Task completion evaluation for calendar scheduling benchmark."""

from .evaluate import TaskCompletionResult, evaluate_task_completion
from .illegal_moves import find_illegal_moves, meeting_changed
from .meeting_scheduled import (
    MatchType,
    MeetingMatchJudge,
    MeetingMatchResult,
    find_exact_match,
    find_matching_meeting,
    is_meeting_scheduled,
)

__all__ = [
    # Unified evaluation
    "TaskCompletionResult",
    "evaluate_task_completion",
    # Meeting scheduling detection
    "MatchType",
    "MeetingMatchJudge",
    "MeetingMatchResult",
    "find_exact_match",
    "find_matching_meeting",
    "is_meeting_scheduled",
    # Illegal moves detection
    "find_illegal_moves",
    "meeting_changed",
]
