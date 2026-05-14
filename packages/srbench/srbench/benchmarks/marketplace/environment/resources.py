"""Marketplace AgentResources: async ``execute`` with blocking inbox semantics."""

from __future__ import annotations

import asyncio
from typing import Literal

from ..types import ActionTrace, MessageRecord, OfferRecord, Tool, ToolError
from .actions import AcceptOffer, EndConversation, GetMessages, MakeOffer, SendMessage
from .state import MarketplaceState


class MarketplaceEnvironment:
    """Shared in-memory state for a bilateral marketplace negotiation.

    Owns the conversation-level ``end_event`` (set by ``EndConversation`` and
    watched by the executor) and a per-role ``new_content_event`` registry so
    blocked ``GetMessages`` calls can be woken up when the counterpart acts.
    """

    def __init__(self) -> None:
        self.state = MarketplaceState()
        self.end_event: asyncio.Event = asyncio.Event()
        self.end_reason: str | None = None
        self._new_content_events: dict[Literal["buyer", "seller"], asyncio.Event] = {}

    def _new_content_event_for(self, role: Literal["buyer", "seller"]) -> asyncio.Event:
        event = self._new_content_events.get(role)
        if event is None:
            event = asyncio.Event()
            self._new_content_events[role] = event
        return event

    def _notify_counterpart_of(self, actor: Literal["buyer", "seller"]) -> None:
        """Wake the role that is NOT the actor (counterpart inbox notification)."""
        counterpart: Literal["buyer", "seller"] = "seller" if actor == "buyer" else "buyer"
        event = self._new_content_events.get(counterpart)
        if event is not None:
            event.set()

    def mark_ended(self, *, reason: str) -> None:
        """Record an end-of-conversation signal and wake up the executor.

        Idempotent: only the first call takes effect.
        """
        if self.end_event.is_set():
            return
        self.end_reason = reason
        self.end_event.set()

    def next_action_index(self) -> int:
        """Return the next monotonic action index (1-based)."""
        self.state.action_count += 1
        return self.state.action_count

    def create_agent_resources(self, role: Literal["buyer", "seller"]) -> "AgentResources":
        new_content_event = self._new_content_event_for(role)
        return AgentResources(
            role=role,
            state=self.state,
            new_content_event=new_content_event,
            env=self,
        )


class AgentResources:
    """Executes actions for one role against shared marketplace state."""

    def __init__(
        self,
        role: Literal["buyer", "seller"],
        state: MarketplaceState,
        new_content_event: asyncio.Event | None = None,
        env: MarketplaceEnvironment | None = None,
    ):
        self.role = role
        self.state = state
        self._seen_message_count = 0
        self._seen_offer_count = 0
        self._new_content_event: asyncio.Event = new_content_event or asyncio.Event()
        self._env: MarketplaceEnvironment | None = env

    async def execute(self, action: Tool) -> str:
        """Execute a tool action against marketplace state.

        Records an ``ActionTrace`` on the env (formerly the responsibility of
        ``execute_with_trace``) and assigns a monotonic ``action_index``.
        Wakes the counterpart's ``new_content_event`` for mutating actions and
        blocks on inbox reads when the agent has nothing new.

        Raises:
            ToolError: For invalid input (e.g. accepting a non-existent
                offer). The caller (``invoke_tool``) formats it into the
                result string.
        """
        action_index = self._env.next_action_index() if self._env else 0
        try:
            result = await self._dispatch(action)
            valid = True
        except ToolError as e:
            self._record_trace(action, action_index, result=f"Error: {e}", valid=False)
            raise

        self._record_trace(action, action_index, result=result, valid=valid)
        return result

    async def _dispatch(self, action: Tool) -> str:
        if isinstance(action, SendMessage):
            self.state.messages.append(
                MessageRecord(
                    round=0,
                    action_index=self._env.state.action_count if self._env else 0,
                    speaker=self.role,
                    content=action.content,
                )
            )
            if self._env is not None:
                self._env._notify_counterpart_of(self.role)
            return "Message sent."

        if isinstance(action, GetMessages):
            return await self._handle_get_messages()

        if isinstance(action, MakeOffer):
            self.state.expire_offers_from(self.role)
            offer = OfferRecord(
                id=self.state.next_offer_id,
                round_created=0,
                action_index=self._env.state.action_count if self._env else 0,
                proposer=self.role,
                price=float(action.price),
                message=action.message,
                status="OPEN",
            )
            self.state.next_offer_id += 1
            self.state.offers.append(offer)
            if action.message:
                self.state.messages.append(
                    MessageRecord(
                        round=0,
                        action_index=self._env.state.action_count if self._env else 0,
                        speaker=self.role,
                        content=action.message,
                    )
                )
            if self._env is not None:
                self._env._notify_counterpart_of(self.role)
            return f"Offer #{offer.id} created at price {offer.price:.2f}."

        if isinstance(action, AcceptOffer):
            offer = self.state.get_offer(action.offer_id)
            if offer is None:
                raise ToolError(f"Offer #{action.offer_id} does not exist.")
            if offer.status != "OPEN":
                raise ToolError(f"Offer #{action.offer_id} is not open (status={offer.status}).")
            if offer.proposer == self.role:
                raise ToolError("Cannot accept your own offer.")

            offer.status = "ACCEPTED"
            self.state.outcome.deal_reached = True
            self.state.outcome.deal_price = offer.price
            self.state.outcome.accepted_offer_id = offer.id
            if action.message:
                self.state.messages.append(
                    MessageRecord(
                        round=0,
                        action_index=self._env.state.action_count if self._env else 0,
                        speaker=self.role,
                        content=action.message,
                    )
                )
            if self._env is not None:
                self._env._notify_counterpart_of(self.role)
            return f"Accepted offer #{offer.id} at price {offer.price:.2f}."

        if isinstance(action, EndConversation):
            self.state.outcome.ended_by = self.role
            self.state.outcome.end_reason = action.reason
            if self._env is not None:
                self._env.mark_ended(reason=action.reason)
            return "Negotiation ended."

        raise ValueError(f"Unsupported action type: {type(action).__name__}")

    async def _handle_get_messages(self) -> str:
        """Return new counterpart messages/offers, blocking if there are none.

        Clear-then-check-then-await — same pattern as calendar's GetEmails.
        """
        self._new_content_event.clear()
        updates = self.get_unread_updates()
        if not updates:
            await self._new_content_event.wait()
            self._new_content_event.clear()
            updates = self.get_unread_updates()
        if not updates:
            return "No new messages or offers."

        lines: list[str] = []
        message_updates = [u for u in updates if u["kind"] == "message"]
        offer_updates = [u for u in updates if u["kind"] == "offer"]
        if message_updates:
            lines.append("New messages:")
            for msg in message_updates:
                lines.append(f"- {msg['speaker']}: {msg['content']}")
        if offer_updates:
            if lines:
                lines.append("")
            lines.append("New offers:")
            for offer in offer_updates:
                msg_suffix = f" | message: {offer['message']}" if offer["message"] else ""
                lines.append(
                    f"- Offer #{offer['offer_id']} from {offer['proposer']}: "
                    f"price={offer['price']:.2f} (status={offer['status']}){msg_suffix}"
                )
        return "\n".join(lines)

    def get_unread_updates(self) -> list[dict]:
        """Return unread counterpart messages/offers as structured updates and mark read.

        Returns:
            List of update dicts with ``"kind"`` set to ``"message"`` or
            ``"offer"`` and associated metadata. Only counterpart updates are
            included.
        """
        new_messages = self.state.messages[self._seen_message_count :]
        new_offers = self.state.offers[self._seen_offer_count :]
        self._seen_message_count = len(self.state.messages)
        self._seen_offer_count = len(self.state.offers)

        counterpart_messages = [m for m in new_messages if m.speaker != self.role]
        counterpart_offers = [o for o in new_offers if o.proposer != self.role]

        updates: list[dict] = []
        for msg in counterpart_messages:
            updates.append(
                {
                    "kind": "message",
                    "action_index": msg.action_index,
                    "speaker": msg.speaker,
                    "content": msg.content,
                }
            )
        for offer in counterpart_offers:
            updates.append(
                {
                    "kind": "offer",
                    "action_index": offer.action_index,
                    "offer_id": offer.id,
                    "proposer": offer.proposer,
                    "price": offer.price,
                    "status": offer.status,
                    "message": offer.message,
                }
            )
        return updates

    def _record_trace(
        self,
        action: Tool,
        action_index: int,
        *,
        result: str,
        valid: bool,
    ) -> None:
        self.state.action_trace.append(
            ActionTrace(
                round=0,
                action_index=action_index,
                actor=self.role,
                action_type=type(action).__name__,
                payload=action.model_dump(),
                result=result,
                valid=valid,
            )
        )
