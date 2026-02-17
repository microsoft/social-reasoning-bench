"""Composite protocol for combining multiple marketplace protocols.

This module provides CompositeProtocol, which allows combining multiple
protocol implementations (e.g., EmailProtocol + MessengerProtocol) into
a single unified protocol.

Example:
    >>> from mm_environments import CompositeProtocol, EmailProtocol, MessengerProtocol
    >>>
    >>> protocol = CompositeProtocol(
    ...     EmailProtocol(),
    ...     MessengerProtocol(enable_groups=True)
    ... )
    >>>
    >>> # Agents can now use actions from both protocols
    >>> # - Email: SendEmail, CheckEmails, SearchContacts, etc.
    >>> # - Messenger: SendMessage, ListContacts, CreateGroup, etc.
"""

from collections.abc import Sequence

from magentic_marketplace.platform.database.base import BaseDatabaseController
from magentic_marketplace.platform.protocol.base import BaseMarketplaceProtocol
from magentic_marketplace.platform.shared.models import (
    ActionExecutionRequest,
    ActionExecutionResult,
    ActionProtocol,
    BaseAction,
)


class CompositeProtocol(BaseMarketplaceProtocol):
    """Composite protocol that combines multiple protocols into one.

    This protocol merges actions from multiple child protocols and delegates
    execution to the appropriate protocol based on action name. It detects
    and fails fast on action name collisions between protocols.

    Attributes:
        protocols: Tuple of child protocols to combine
    """

    def __init__(self, *protocols: BaseMarketplaceProtocol):
        """Initialize composite protocol with child protocols.

        Args:
            *protocols: Variable number of protocol instances to combine

        Example:
            >>> protocol = CompositeProtocol(
            ...     EmailProtocol(),
            ...     MessengerProtocol(enable_groups=True)
            ... )
        """
        super().__init__()
        self.protocols = protocols
        self._action_to_protocol: dict[str, BaseMarketplaceProtocol] = {}
        self.get_actions()

    def get_actions(self) -> Sequence[ActionProtocol | type[BaseAction]]:
        """Get combined actions from all child protocols.

        Merges actions from all protocols and detects name collisions.
        Builds internal mapping for action routing.

        Returns:
            Sequence of all actions from all protocols

        Raises:
            ValueError: If multiple protocols define actions with the same name
        """
        all_actions: list[ActionProtocol | type[BaseAction]] = []
        self._action_to_protocol.clear()

        for protocol in self.protocols:
            protocol_name = protocol.__class__.__name__

            for action in protocol.get_actions():
                # Get action name
                action_name = (
                    action.name if isinstance(action, ActionProtocol) else action.get_name()
                )

                # Check for collisions
                if action_name in self._action_to_protocol:
                    existing_protocol_name = self._action_to_protocol[
                        action_name
                    ].__class__.__name__
                    raise ValueError(
                        f"Action name collision: '{action_name}' is defined in both "
                        f"{existing_protocol_name} and {protocol_name}. "
                        f"Each action name must be unique across all protocols."
                    )

                # Register action
                self._action_to_protocol[action_name] = protocol
                all_actions.append(action)

        return all_actions

    async def execute_action(
        self,
        *,
        agent,
        action: ActionExecutionRequest,
        database: BaseDatabaseController,
    ) -> ActionExecutionResult:
        """Execute action by delegating to the appropriate child protocol.

        Routes the action to the protocol that registered it.

        Args:
            agent: Agent profile executing the action
            action: Action execution request with name and parameters
            database: Database controller

        Returns:
            Result of executing the action

        Raises:
            ValueError: If action name is not recognized
        """
        if not self._action_to_protocol:
            self.get_actions()

        # Look up which protocol owns this action
        protocol = self._action_to_protocol.get(action.name)

        if protocol is None:
            return ActionExecutionResult(
                content=f"Unknown action: '{action.name}'. "
                f"This action is not registered in any of the composite protocols.",
                is_error=True,
            )

        # Delegate to child protocol
        return await protocol.execute_action(agent=agent, action=action, database=database)

    async def initialize(self, database: BaseDatabaseController) -> None:
        """Initialize all child protocols.

        Calls initialize() on each child protocol in sequence.

        Args:
            database: Database controller to pass to child protocols
        """
        for protocol in self.protocols:
            await protocol.initialize(database)
