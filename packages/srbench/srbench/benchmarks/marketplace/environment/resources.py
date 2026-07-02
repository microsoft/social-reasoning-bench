from typing import Literal

from ....shared.signals import ConversationSignals
from ..types import ActionTrace, MessageRecord, Tool, ToolError
from .actions import AcceptOffer, EndConversation, GetMessages, MakeOffer, SendMessage, Wait
from .state import MarketplaceState


class MarketplaceEnvironment:
    """Shared in-memory state for a bilateral marketplace negotiation.

    Owns the conversation's :class:`ConversationSignals`, keyed by role, so an
    agent blocked on ``Wait`` wakes when its counterpart acts.
    """

    def __init__(self) -> None:
        self.state = MarketplaceState()
        self.signals = ConversationSignals()

    def create_agent_resources(self, role: Literal["buyer", "seller"]) -> "AgentResources":
        self.signals.register(role)
        return AgentResources(role=role, state=self.state, signals=self.signals)


class AgentResources:
    """Executes actions for one role against shared marketplace state.

    ``execute`` is the single execution path for every action. It records an
    ``ActionTrace`` on the shared state for each executed action, wakes the
    counterpart when an action produces content visible to them, blocks on
    ``Wait`` until the counterpart acts, and fires the environment's end
    signal on a successful ``EndConversation``.
    """

    def __init__(
        self,
        role: Literal["buyer", "seller"],
        state: MarketplaceState,
        *,
        signals: ConversationSignals,
    ):
        self.role = role
        self.state = state
        self._seen_message_count = 0
        self._seen_offer_count = 0
        self._signals = signals
        self._counterpart: Literal["buyer", "seller"] = "seller" if role == "buyer" else "buyer"

    async def execute(self, action: Tool) -> str:
        """Execute a tool action, record its trace, and return the result.

        Async because ``Wait`` blocks until the counterpart acts (or the
        negotiation ends); every other action completes immediately.

        Args:
            action: The tool action to execute.

        Returns:
            A string describing the result of the action.

        Raises:
            ToolError: If the action was rejected; recorded as an invalid
                trace entry, then re-raised for the agent's run loop to
                surface as an error-string result.
            ValueError: If the action type is unknown.
        """
        if isinstance(action, Wait) and not await self._signals.wait_for_activity(self.role):
            result = "Negotiation has ended."
            self._record_trace(action, result=result, valid=True)
            return result
        try:
            result = self._dispatch(action)
        except ToolError as e:
            self._record_trace(action, result=f"Error: {e}", valid=False)
            raise
        self._record_trace(action, result=result, valid=True)
        if isinstance(action, (SendMessage, MakeOffer, AcceptOffer)):
            self._signals.notify(self._counterpart)
        if isinstance(action, EndConversation):
            self._signals.end(reason=action.reason)
        return result

    def _record_trace(self, action: Tool, *, result: str, valid: bool) -> None:
        self.state.action_trace.append(
            ActionTrace(
                round=self.state.current_round,
                actor=self.role,
                action_type=type(action).__name__,
                payload=action.model_dump(),
                result=result,
                valid=valid,
            )
        )

    def _dispatch(self, action: Tool) -> str:
        if isinstance(action, SendMessage):
            self.state.messages.append(
                MessageRecord(
                    round=self.state.current_round,
                    speaker=self.role,
                    content=action.content,
                )
            )
            return "Message sent."

        if isinstance(action, GetMessages):
            return self._handle_get_messages()

        if isinstance(action, MakeOffer):
            self.state.expire_offers_from(self.role)
            offer = {
                "id": self.state.next_offer_id,
                "round_created": self.state.current_round,
                "proposer": self.role,
                "price": float(action.price),
                "message": action.message,
                "status": "OPEN",
            }
            self.state.next_offer_id += 1
            from ..types import OfferRecord

            self.state.offers.append(OfferRecord(**offer))
            if action.message:
                self.state.messages.append(
                    MessageRecord(
                        round=self.state.current_round,
                        speaker=self.role,
                        content=action.message,
                    )
                )
            return f"Offer #{offer['id']} created at price {offer['price']:.2f}."

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
                        round=self.state.current_round,
                        speaker=self.role,
                        content=action.message,
                    )
                )
            return f"Accepted offer #{offer.id} at price {offer.price:.2f}."

        if isinstance(action, Wait):
            # The executor blocks the caller until the counterpart acts before
            # executing this action; the result surfaces what arrived.
            return self._handle_get_messages()

        if isinstance(action, EndConversation):
            self.state.outcome.ended_by = self.role
            self.state.outcome.end_reason = action.reason
            return "Negotiation ended."

        raise ValueError(f"Unsupported action type: {type(action).__name__}")

    def get_unread_updates(self) -> list[dict]:
        """Return unread counterpart messages/offers as structured updates and mark read.

        Returns:
            List of update dicts with ``"kind"`` set to ``"message"`` or ``"offer"``
            and associated metadata. Only counterpart updates are included.
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
                    "round": msg.round,
                    "speaker": msg.speaker,
                    "content": msg.content,
                }
            )
        for offer in counterpart_offers:
            updates.append(
                {
                    "kind": "offer",
                    "round": offer.round_created,
                    "offer_id": offer.id,
                    "proposer": offer.proposer,
                    "price": offer.price,
                    "status": offer.status,
                    "message": offer.message,
                }
            )
        return updates

    def _handle_get_messages(self) -> str:
        """Return unread counterpart messages and newly created counterpart offers.

        Returns:
            A human-readable string summarising new messages and offers, or
            ``"No new messages or offers."`` if there are none.
        """
        updates = self.get_unread_updates()

        if not updates:
            return "No new messages or offers."

        lines: list[str] = []
        message_updates = [u for u in updates if u["kind"] == "message"]
        offer_updates = [u for u in updates if u["kind"] == "offer"]
        if message_updates:
            lines.append("New messages:")
            for msg in message_updates:
                lines.append(f"- Round {msg['round']} {msg['speaker']}: {msg['content']}")
        if offer_updates:
            if lines:
                lines.append("")
            lines.append("New offers:")
            for offer in offer_updates:
                msg_suffix = f" | message: {offer['message']}" if offer["message"] else ""
                lines.append(
                    f"- Offer #{offer['offer_id']} from {offer['proposer']}: price={offer['price']:.2f} "
                    f"(round {offer['round']}, status={offer['status']}){msg_suffix}"
                )
        return "\n".join(lines)
