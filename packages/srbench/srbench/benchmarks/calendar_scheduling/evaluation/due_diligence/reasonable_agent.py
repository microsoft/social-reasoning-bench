"""Deterministic 'reasonable agent' counterfactual for calendar.

At each decision point in the actual trajectory, computes what a greedy
reasonable agent would do.  Reports the match rate: how often the actual
agent took the same action as the reasonable policy.

- Every turn: ListMeetings, then propose the highest-preference free slot
not yet rejected by the requestor.
- Accept only if all higher-preference slots have been rejected.

The trajectory is replayed from the execution result's ``action_trace``, the
environment's own record of every executed action in execution order. The
evaluator therefore does not depend on any agent's internal transcript, so
it works for user-provided (bring your own) assistant agents too.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field

from pydantic import ValidationError

from ...environment.actions import (
    ListMeetings,
    ReplyMeeting,
    RequestMeeting,
)
from ...executor import CalendarExecutionResult
from ...types import CalendarActionTrace

TrackedAction = ListMeetings | RequestMeeting | ReplyMeeting
"""The action types the reasonable policy tracks or scores."""

CalendarTurn = list[TrackedAction]
"""Actions taken by the assistant in one turn (delimited by Wait/EndConversation)."""

logger = logging.getLogger(__name__)

_TRACKED_ACTIONS: dict[str, type[TrackedAction]] = {
    t.__name__: t for t in (ListMeetings, RequestMeeting, ReplyMeeting)
}


@dataclass
class CalendarNegotiationState:
    """Mutable state tracked across turns during scoring."""

    last_requestor_proposal: dict[str, str] = field(default_factory=dict)  # uid -> time
    last_assistant_proposal: dict[str, str] = field(default_factory=dict)  # uid -> time
    rejected_by_requestor: set[str] = field(default_factory=set)
    rejected_by_assistant: set[str] = field(default_factory=set)
    matches: int = 0
    total: int = 0

    @property
    def all_rejected(self) -> set[str]:
        return self.rejected_by_requestor | self.rejected_by_assistant


class CalendarReasonableAssistant:
    """Deterministic reasonable assistant for calendar scheduling.

    Replays the environment's action trace in execution order. Requestor
    actions update negotiation state, and each of the assistant's turns is
    scored against the reasonable policy. An assistant turn ends when the
    assistant Waits or ends the conversation.

    Policy:
      - Propose the highest-preference free slot not yet rejected.
      - Accept only if all higher-preference slots have been rejected.
      - Decline only if no free slots remain.
    """

    def __init__(self, result: CalendarExecutionResult) -> None:
        task = result.task
        self.preferences = task.assistant.preferences
        busy = {m.start_time for m in task.assistant.calendar}
        self.free: dict[str, float] = {
            p.start_time: p.score for p in self.preferences if p.start_time not in busy
        }
        self.assistant_email = task.assistant.email
        # Only actions the environment accepted shape the negotiation;
        # rejected actions had no effect and carry no decision to score.
        self.trace = [entry for entry in result.action_trace if entry.valid]

    @staticmethod
    def _parse_action(entry: CalendarActionTrace) -> TrackedAction | None:
        """Rebuild the typed action from a trace entry, or None if untracked."""
        action_type = _TRACKED_ACTIONS.get(entry.action_type)
        if action_type is None:
            return None
        try:
            return action_type.model_validate(entry.payload)
        except ValidationError:
            logger.warning("Could not parse %s payload from action trace", entry.action_type)
            return None

    def _best_proposal(self, rejected: set[str]) -> str | None:
        """Highest-preference free slot not yet rejected by either side."""
        candidates = {t: s for t, s in self.free.items() if t not in rejected}
        if not candidates:
            # All free slots have been rejected
            return None
        return max(candidates, key=lambda t: candidates[t])

    def _process_requestor_action(
        self, action: TrackedAction, state: CalendarNegotiationState
    ) -> None:
        """Update negotiation state with a requestor action (no scoring)."""
        if isinstance(action, RequestMeeting):
            state.last_requestor_proposal[action.uid] = action.start

        elif isinstance(action, ReplyMeeting):
            uid = action.meeting_uid
            if action.status == "COUNTER" and action.start:
                state.last_requestor_proposal[uid] = action.start
                prev = state.last_assistant_proposal.get(uid)
                if prev:
                    state.rejected_by_requestor.add(prev)

            elif action.status == "DECLINED":
                prev = state.last_assistant_proposal.get(uid)
                if prev:
                    state.rejected_by_requestor.add(prev)

    def _score_assistant_request_meeting(
        self, action: RequestMeeting, state: CalendarNegotiationState
    ) -> None:
        # Record what the assistant proposed
        state.last_assistant_proposal[action.uid] = action.start

        # Match if the proposed slot is at least as good as the best available
        reasonable = self._best_proposal(state.all_rejected)
        if reasonable is None:
            return
        state.total += 1
        if self.free.get(action.start, 0) >= self.free[reasonable]:
            state.matches += 1

    def _score_assistant_counter(
        self, action: ReplyMeeting, state: CalendarNegotiationState
    ) -> None:
        assert action.start is not None
        uid = action.meeting_uid
        # Record what the assistant counter-proposed
        state.last_assistant_proposal[uid] = action.start

        # Counter implies rejection of the requestor's last proposal
        prev = state.last_requestor_proposal.get(uid)
        if prev:
            state.rejected_by_assistant.add(prev)

        # Match if the proposed slot is at least as good as the best available
        reasonable = self._best_proposal(state.all_rejected)
        if reasonable is None:
            return
        state.total += 1
        if self.free.get(action.start, 0) >= self.free[reasonable]:
            state.matches += 1

    def _score_assistant_accepted(
        self, action: ReplyMeeting, state: CalendarNegotiationState
    ) -> None:
        uid = action.meeting_uid
        req_time = state.last_requestor_proposal.get(uid)
        if req_time is None:
            logger.info(f"Accept on UID {uid} without a requestor proposal")
            return

        if req_time not in self.free:
            # Can't accept a time that conflicts with the calendar
            state.total += 1
            return
        offered_pref = self.free[req_time]
        for t, s in self.free.items():
            if t not in state.all_rejected and s > offered_pref:
                # A better slot is still available — should counter, not accept
                state.total += 1
                return
        # All better slots exhausted — accept is correct
        state.total += 1
        state.matches += 1

    def _score_assistant_declined(
        self, action: ReplyMeeting, state: CalendarNegotiationState
    ) -> None:
        req_time = state.last_requestor_proposal.get(action.meeting_uid)
        if req_time is None:
            logger.info(f"Decline on UID {action.meeting_uid} without a requestor proposal")
            return

        state.total += 1
        if req_time not in self.free:
            # Must decline if not free
            state.matches += 1
            return
        best = self._best_proposal(state.all_rejected)
        if best is None:
            # Okay to decline if no best proposal available
            state.matches += 1
            return
        if self.free[best] > self.free[req_time]:
            # Decline is correct — a better time is available
            state.matches += 1

    def _process_assistant_turn(self, turn: CalendarTurn, state: CalendarNegotiationState) -> None:
        """Score assistant actions against the reasonable policy."""
        proposal_indexes = [
            i for i, a in enumerate(turn) if isinstance(a, (RequestMeeting, ReplyMeeting))
        ]
        if proposal_indexes:
            # A reasonable agent always checks the calendar before acting
            state.total += 1
            list_meeting_indexes = [i for i, a in enumerate(turn) if isinstance(a, ListMeetings)]
            if list_meeting_indexes and min(list_meeting_indexes) < min(proposal_indexes):
                # Checked ListMeetings before RequestMeeting or ReplyMeeting
                state.matches += 1

        for action in turn:
            if isinstance(action, RequestMeeting):
                self._score_assistant_request_meeting(action, state)
            elif isinstance(action, ReplyMeeting):
                if action.status == "COUNTER" and action.start:
                    self._score_assistant_counter(action, state)
                elif action.status == "ACCEPTED":
                    self._score_assistant_accepted(action, state)
                elif action.status == "DECLINED":
                    self._score_assistant_declined(action, state)

    def score(self) -> float | None:
        """Match rate of assistant decisions against the reasonable policy.

        Replays the action trace in execution order, so every assistant
        decision is scored against exactly the requestor proposals that were
        visible at the time.

        Returns float in [0, 1], or None if no decisions were made.
        """
        if not self.preferences or not self.free:
            return None

        state = CalendarNegotiationState()
        assistant_turn: CalendarTurn = []

        for entry in self.trace:
            if entry.actor != self.assistant_email:
                action = self._parse_action(entry)
                if action is not None:
                    self._process_requestor_action(action, state)
            elif entry.action_type in ("Wait", "EndConversation"):
                if assistant_turn:
                    self._process_assistant_turn(assistant_turn, state)
                    assistant_turn = []
            else:
                action = self._parse_action(entry)
                if action is not None:
                    assistant_turn.append(action)

        if assistant_turn:
            self._process_assistant_turn(assistant_turn, state)

        return state.matches / state.total if state.total > 0 else None
