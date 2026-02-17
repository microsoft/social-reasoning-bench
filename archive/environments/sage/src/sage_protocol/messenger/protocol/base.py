from collections.abc import Sequence

from magentic_marketplace.platform.database.base import BaseDatabaseController
from magentic_marketplace.platform.protocol.base import BaseMarketplaceProtocol
from magentic_marketplace.platform.shared.models import (
    ActionExecutionRequest,
    ActionExecutionResult,
    ActionProtocol,
    AgentProfile,
    BaseAction,
)

from ..actions import (
    ActionTypeAdapter,
    CreateGroup,
    ListContacts,
    ListConversations,
    ReadMessages,
    SendMessageToConversation,
)
from .create_group import handle_create_group
from .list_contacts import handle_list_contacts
from .list_conversations import handle_list_conversations
from .read_messages import handle_read_messages
from .send_message import handle_send_message


class MessengerProtocol(BaseMarketplaceProtocol):
    def __init__(self):
        """Initialize the MessengerProtocol."""
        super().__init__()

    def get_actions(self) -> Sequence[ActionProtocol | type[BaseAction]]:
        actions = [
            SendMessageToConversation,
            ReadMessages,
            ListContacts,
            ListConversations,
            CreateGroup,
        ]

        return actions

    async def execute_action(
        self,
        *,
        agent: AgentProfile,
        action: ActionExecutionRequest,
        database: BaseDatabaseController,
    ) -> ActionExecutionResult:
        request = ActionTypeAdapter.validate_python(action.parameters)

        if isinstance(request, SendMessageToConversation):
            return await handle_send_message(request, agent, database)

        elif isinstance(request, CreateGroup):
            return await handle_create_group(request, agent, database)

        elif isinstance(request, ReadMessages):
            return await handle_read_messages(request, agent, database)

        elif isinstance(request, ListContacts):
            return await handle_list_contacts(request, agent, database)

        elif isinstance(request, ListConversations):
            return await handle_list_conversations(request, agent, database)

        else:
            raise TypeError("Unrecognized action")
