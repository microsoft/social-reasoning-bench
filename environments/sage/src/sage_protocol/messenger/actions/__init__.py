from typing import Annotated

from pydantic import Field, TypeAdapter

from .create_group import CreateGroup, GroupInfo
from .list_contacts import Contact, ListContacts, ListContactsResponse
from .list_conversations import (
    ConversationInfo,
    ListConversations,
    ListConversationsResponse,
)
from .read_messages import Message, ReadMessages, ReadMessagesResponse
from .send_message import SendMessageToConversation

ActionType = Annotated[
    (SendMessageToConversation | CreateGroup | ReadMessages | ListContacts | ListConversations),
    Field(discriminator="type"),
]
ActionTypeAdapter = TypeAdapter(ActionType)

__all__ = [
    "SendMessageToConversation",
    "CreateGroup",
    "GroupInfo",
    "ReadMessages",
    "ReadMessagesResponse",
    "Message",
    "ListContacts",
    "Contact",
    "ListContactsResponse",
    "ListConversations",
    "ConversationInfo",
    "ListConversationsResponse",
    "ActionType",
    "ActionTypeAdapter",
]
