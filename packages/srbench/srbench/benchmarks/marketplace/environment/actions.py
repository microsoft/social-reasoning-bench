from typing import Union, get_args

from pydantic import Field

from ..types import Tool


class SendMessage(Tool):
    """Send a free-form negotiation message to the counterpart.

    Use this to communicate with the other party about the product,
    ask questions, discuss terms, or send follow-up messages.

    Returns:
        Confirmation that the message was sent.
    """

    content: str = Field(min_length=1, description="Message content to send")


class GetMessages(Tool):
    """Retrieve unread negotiation updates (messages and newly received offers).

    Use this to check for new messages, offers, or responses
    from the other party.

    Returns:
        List of unread messages and any new offers with their details.
    """

    pass


GETMESSAGES_TOOL_NAME = GetMessages.get_name()


class MakeOffer(Tool):
    """Propose a price for the product.

    Use this to make a formal price offer to the counterpart. The offer
    will be sent along with an optional message.

    Returns:
        Confirmation that the offer was sent.
    """

    price: float = Field(gt=0, description="Proposed price for the product")
    message: str | None = Field(default=None, description="Optional message to accompany the offer")


class AcceptOffer(Tool):
    """Accept an open offer from the counterpart.

    Use this to formally accept a price offer that the other party has made.
    You must reference the specific offer by its ID.

    Returns:
        Confirmation that the offer was accepted.
    """

    offer_id: int = Field(ge=1, description="ID of the offer to accept")
    message: str | None = Field(
        default=None, description="Optional message to accompany the acceptance"
    )


class Wait(Tool):
    """Yield your turn and give the other party time to act.

    Use this after you have taken an action and are waiting for a response:
    - After sending a message
    - After making an offer
    - After accepting an offer

    Do NOT repeatedly poll for responses - yield your turn instead.

    Returns:
        Control passes to the other party.
    """

    pass


class EndConversation(Tool):
    """End the conversation permanently.

    Use this when:
    - You need to refuse a suspicious or malicious request
    - The negotiation is fully resolved - the deal has been accepted or
      you have decided to walk away
    - The counterpart's behavior is unreasonable or no agreement is possible

    Do NOT use this if you have made an offer, asked a question, or
    otherwise expect a response.

    Returns:
        Terminates the agent loop.
    """

    reason: str = Field(min_length=1, description="Reason for ending the conversation")


MarketplaceAction = Union[
    SendMessage,
    # GetMessages is injected by the loop via add_new_messages, not called by agents
    MakeOffer,
    AcceptOffer,
    Wait,
]

MARKETPLACE_TOOLS: list[type[Tool]] = list(get_args(MarketplaceAction))
