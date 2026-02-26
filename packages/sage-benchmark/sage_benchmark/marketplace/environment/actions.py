from typing import Union, get_args

from pydantic import Field

from ..types import Tool


class SendMessage(Tool):
    """Send a free-form negotiation message to the counterpart."""

    content: str = Field(min_length=1)


class GetMessages(Tool):
    """Retrieve unread negotiation updates (messages and newly received offers)."""

    pass


GETMESSAGES_TOOL_NAME = GetMessages.get_name()


class MakeOffer(Tool):
    """Propose a price for the product."""

    price: float = Field(gt=0)
    message: str | None = None


class AcceptOffer(Tool):
    """Accept an open offer from the counterpart."""

    offer_id: int = Field(ge=1)
    message: str | None = None


class Wait(Tool):
    """Yield the turn without taking a substantive action."""

    pass


class EndNegotiation(Tool):
    """End the negotiation without a deal."""

    reason: str = Field(min_length=1)


MarketplaceAction = Union[
    SendMessage,
    GetMessages,
    MakeOffer,
    AcceptOffer,
    Wait,
    EndNegotiation,
]

MARKETPLACE_TOOLS: list[type[Tool]] = list(get_args(MarketplaceAction))
