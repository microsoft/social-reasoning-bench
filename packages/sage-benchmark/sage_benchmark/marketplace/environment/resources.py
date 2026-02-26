from ..types import ActionTrace, MessageRecord, Tool, ToolError
from .actions import AcceptOffer, EndNegotiation, GetMessages, MakeOffer, SendMessage, Wait
from .state import MarketplaceState


class MarketplaceEnvironment:
    """Shared in-memory state for a bilateral marketplace negotiation."""

    def __init__(self) -> None:
        self.state = MarketplaceState()

    def create_agent_resources(self, role: str) -> "AgentResources":
        return AgentResources(role=role, state=self.state)


class AgentResources:
    """Executes actions for one role against shared marketplace state."""

    def __init__(self, role: str, state: MarketplaceState):
        if role not in {"buyer", "seller"}:
            raise ValueError(f"Unsupported role: {role}")
        self.role = role
        self.state = state
        self._seen_message_count = 0
        self._seen_offer_count = 0

    def execute(self, action: Tool) -> str:
        if isinstance(action, SendMessage):
            self.state.messages.append(
                MessageRecord(
                    round=self.state.current_round,
                    speaker=self.role,  # type: ignore[arg-type]
                    content=action.content,
                )
            )
            return "Message sent."

        if isinstance(action, GetMessages):
            return self._handle_get_messages()

        if isinstance(action, MakeOffer):
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
                        speaker=self.role,  # type: ignore[arg-type]
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
            if offer.round_created != self.state.current_round:
                raise ToolError("Offer expired (only current-round offers can be accepted).")

            offer.status = "ACCEPTED"
            self.state.outcome.deal_reached = True
            self.state.outcome.deal_price = offer.price
            self.state.outcome.accepted_offer_id = offer.id
            if action.message:
                self.state.messages.append(
                    MessageRecord(
                        round=self.state.current_round,
                        speaker=self.role,  # type: ignore[arg-type]
                        content=action.message,
                    )
                )
            return f"Accepted offer #{offer.id} at price {offer.price:.2f}."

        if isinstance(action, Wait):
            return "Waited."

        if isinstance(action, EndNegotiation):
            self.state.outcome.ended_by = self.role  # type: ignore[assignment]
            self.state.outcome.end_reason = action.reason
            return "Negotiation ended."

        raise ValueError(f"Unsupported action type: {type(action).__name__}")

    def get_unread_updates(self) -> list[dict]:
        """Return unread counterpart messages/offers as structured updates and mark read."""
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
        """Return unread counterpart messages and newly created counterpart offers."""
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


def execute_with_trace(
    resources: AgentResources,
    action: Tool,
) -> tuple[ActionTrace, bool]:
    try:
        result = resources.execute(action)
        trace = ActionTrace(
            round=resources.state.current_round,
            actor=resources.role,  # type: ignore[arg-type]
            action_type=type(action).__name__,
            payload=action.model_dump(),
            result=result,
            valid=True,
        )
        return trace, True
    except ToolError as e:
        trace = ActionTrace(
            round=resources.state.current_round,
            actor=resources.role,  # type: ignore[arg-type]
            action_type=type(action).__name__,
            payload=action.model_dump(),
            result=f"Error: {e}",
            valid=False,
        )
        return trace, False
