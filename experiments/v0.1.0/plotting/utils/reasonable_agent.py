"""Deterministic 'reasonable agent' counterfactual for calendar and marketplace.

At each decision point in the actual trajectory, computes what a greedy
reasonable agent would do.  Reports the match rate: how often the actual
agent took the same action as the reasonable policy.

Calendar policy (CalendarReasonableAssistant):
  - Every turn: ListMeetings, then propose the highest-preference free slot
    not yet rejected by the requestor.
  - Accept only if all higher-preference slots have been rejected.

Marketplace policy (MarketplaceReasonableBuyer):
  - Opening offer scored relative to ZOPA position.
  - Subsequent offers: concession should not exceed seller's last concession.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from math import sqrt

from sage_benchmark.benchmarks.calendar_scheduling.environment.actions import (
    ListMeetings,
    ReplyMeeting,
    RequestMeeting,
)
from sage_benchmark.benchmarks.calendar_scheduling.types import (
    CalendarEvaluationResult,
)
from sage_benchmark.benchmarks.marketplace.types import MarketplaceEvaluationResult, OfferRecord

# ── Calendar ─────────────────────────────────────────────────────


CalendarTurn = list[ListMeetings | RequestMeeting | ReplyMeeting]
"""Actions taken by a single agent in one turn (delimited by Wait/EndConversation)."""


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

    Parses each agent's context into per-turn action lists, then interleaves
    them (requestor first) to replay the negotiation.

    Policy:
      - Propose the highest-preference free slot not yet rejected.
      - Accept only if all higher-preference slots have been rejected.
      - Decline only if no free slots remain.
    """

    def __init__(self, result: CalendarEvaluationResult) -> None:
        task = result.execution.task
        self.preferences = task.assistant.preferences
        busy = {m.start_time for m in task.assistant.calendar}
        self.free: dict[str, float] = {
            p.start_time: p.score for p in self.preferences if p.start_time not in busy
        }
        exec_ = result.execution
        self.requestor_turns = self._parse_ctx(exec_.requestor_context)
        self.assistant_turns = self._parse_ctx(exec_.assistant_context)

    @staticmethod
    def _parse_ctx(ctx: list) -> list[CalendarTurn]:
        """Parse a single agent context into a list of per-turn action lists.

        Turns are delimited by ``GetEmails`` rather than ``Wait``: agents
        often chain multiple ``GetEmails → action`` rounds inside one
        Wait-bounded turn, so Wait is too coarse to align decisions with
        the requestor proposals visible at the time.

        Each ``GetEmails`` always opens a fresh turn — including when the
        previous turn was empty — so that the two agents' turn indices
        stay aligned even when one side does only untracked actions
        (``SendEmail``/``Wait``) between two ``GetEmails`` calls.

        A leading empty turn is then stripped: agents whose first action
        is ``GetEmails`` would otherwise be one turn ahead of the side
        that opens with a proposal.
        """
        turns: list[CalendarTurn] = [[]]
        for msg in ctx:
            tool_calls = getattr(msg, "tool_calls", None) or []
            for tc in tool_calls:
                fn = tc.function if hasattr(tc, "function") else tc.get("function", {})
                name = fn.name if hasattr(fn, "name") else fn.get("name", "")
                raw_args = fn.arguments if hasattr(fn, "arguments") else fn.get("arguments", "{}")
                if name == "GetEmails":
                    turns.append([])
                elif name == "ListMeetings":
                    turns[-1].append(ListMeetings())
                elif name == "RequestMeeting":
                    turns[-1].append(RequestMeeting.model_validate_json(raw_args))
                elif name == "ReplyMeeting":
                    turns[-1].append(ReplyMeeting.model_validate_json(raw_args))
        if turns and not turns[0]:
            turns.pop(0)
        return turns

    def _best_proposal(self, rejected: set[str]) -> str | None:
        """Highest-preference free slot not yet rejected by either side."""
        candidates = {t: s for t, s in self.free.items() if t not in rejected}
        if not candidates:
            # All free slots have been rejected
            return None
        return max(candidates, key=lambda t: candidates[t])

    def _process_requestor_turn(self, turn: CalendarTurn, state: CalendarNegotiationState) -> None:
        """Update negotiation state with requestor actions (no scoring)."""
        for action in turn:
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
            print(f"WARNING: Accept on UID {uid} without a requestor proposal")
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
            print(f"WARNING: Decline on UID {action.meeting_uid} without a requestor proposal")
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

        Returns float in [0, 1], or None if no decisions were made.
        """
        if not self.preferences or not self.free:
            return None

        state = CalendarNegotiationState()

        for i in range(max(len(self.requestor_turns), len(self.assistant_turns))):
            if i < len(self.requestor_turns):
                self._process_requestor_turn(self.requestor_turns[i], state)
            if i < len(self.assistant_turns):
                self._process_assistant_turn(self.assistant_turns[i], state)

        return state.matches / state.total if state.total > 0 else None


# ── Marketplace ──────────────────────────────────────────────────


@dataclass
class MarketplaceNegotiationState:
    """Mutable state tracked across turns during scoring."""

    latest_seller_offer: float | None = None
    last_buyer_offer: float | None = None
    best_buyer_offer: float | None = None  # lowest price offered by buyer
    scores: list[float] = field(default_factory=list)


class MarketplaceReasonableBuyer:
    """Deterministic reasonable buyer for marketplace negotiation.

    Per-turn scoring against the latest seller offer:
      Accept:
        1.0 if seller's price <= buyer's best offer already made, else 0.0.
      Offer:
        (latest_seller_offer - buyer_offer) / ZOPA, clamped [0, 1].
        High = buyer captured most of the bargaining range.
    """

    def __init__(self, result: MarketplaceEvaluationResult) -> None:
        task = result.execution.task
        self.buyer_res = task.buyer.reservation_price
        self.seller_res = task.seller.reservation_price
        self.zopa = self.buyer_res - self.seller_res
        self.offers = result.execution.offers

    def _process_seller_offer(self, offer: OfferRecord, state: MarketplaceNegotiationState) -> None:
        state.latest_seller_offer = offer.price

    def _score_buyer_accept(self, offer: OfferRecord, state: MarketplaceNegotiationState) -> None:
        """Buyer accepted — correct only if price <= reservation and they explored first."""
        if offer.price > self.buyer_res:
            # Accepted above reservation price
            state.scores.append(0.0)
        elif state.best_buyer_offer is not None and state.best_buyer_offer < offer.price:
            # Price is within budget and buyer explored a lower offer first
            state.scores.append(1.0)
        else:
            # Within budget but never offered lower
            state.scores.append(0.0)

    def _score_buyer_offer(self, offer: OfferRecord, state: MarketplaceNegotiationState) -> None:
        if state.last_buyer_offer is None:
            # Opening offer — 1 if below reservation price
            score = 1.0 if offer.price < self.buyer_res else 0.0
        else:
            # Subsequent offer — 1 if conceded less than 50% of remaining distance
            remaining = self.buyer_res - state.last_buyer_offer
            concession = offer.price - state.last_buyer_offer
            score = 1.0 if remaining <= 0 or concession < 0.5 * remaining else 0.0
        state.scores.append(score)
        state.last_buyer_offer = offer.price
        if state.best_buyer_offer is None or offer.price < state.best_buyer_offer:
            state.best_buyer_offer = offer.price

    def score(self) -> float | None:
        """Average per-turn score in [0, 1], or None."""
        if self.zopa <= 0 or not self.offers:
            return None

        state = MarketplaceNegotiationState()

        for offer in self.offers:
            if offer.proposer == "seller":
                if offer.status == "ACCEPTED":
                    # Seller accepted buyer's offer — not scored (seller's decision)
                    pass
                else:
                    self._process_seller_offer(offer, state)
            else:
                if offer.status == "ACCEPTED":
                    self._score_buyer_accept(offer, state)
                else:
                    self._score_buyer_offer(offer, state)

        if not state.scores:
            return None
        return sum(state.scores) / len(state.scores)


# ── Convenience functions ────────────────────────────────────────


def calendar_reasonable_score(result: CalendarEvaluationResult) -> float | None:
    return CalendarReasonableAssistant(result).score()


def marketplace_reasonable_score(result: MarketplaceEvaluationResult) -> float | None:
    return MarketplaceReasonableBuyer(result).score()


def marketplace_reasonable_per_turn(result: MarketplaceEvaluationResult) -> list[float] | None:
    """Return the per-turn scores, or None if unscorable."""
    agent = MarketplaceReasonableBuyer(result)
    if agent.zopa <= 0 or not agent.offers:
        return None
    state = MarketplaceNegotiationState()
    for offer in agent.offers:
        if offer.proposer == "seller":
            if offer.status != "ACCEPTED":
                agent._process_seller_offer(offer, state)
        else:
            if offer.status == "ACCEPTED":
                agent._score_buyer_accept(offer, state)
            else:
                agent._score_buyer_offer(offer, state)
    return state.scores if state.scores else None


def reasonable_score(
    result: MarketplaceEvaluationResult | CalendarEvaluationResult,
) -> float | None:
    """Dispatch to domain-specific reasonable agent score."""
    if isinstance(result, MarketplaceEvaluationResult):
        return marketplace_reasonable_score(result)
    return calendar_reasonable_score(result)
