"""Composite client for combining multiple marketplace clients.

This module provides CompositeClient, which allows combining multiple
MarketplaceClient instances into a single unified client interface.

Example:
    >>> from sage_agents.utils import CompositeClient
    >>> from magentic_marketplace.platform.client import MarketplaceClient
    >>>
    >>> client = CompositeClient(
    ...     MarketplaceClient("http://localhost:8000"),
    ...     MarketplaceClient("http://localhost:8001"),
    ... )
    >>>
    >>> # Fetch combined protocol from all clients
    >>> protocol = await client.actions.get_protocol()
    >>>
    >>> # Execute actions - routed to appropriate client
    >>> result = await client.actions.execute_request(request)
"""

from magentic_marketplace.platform.client import MarketplaceClient
from magentic_marketplace.platform.shared.models import (
    ActionExecutionRequest,
    ActionExecutionResult,
    ActionProtocol,
)


class CompositeActionsResource:
    """Actions resource that combines actions from multiple clients.

    Routes action execution to the appropriate underlying client based
    on which client provides that action.
    """

    def __init__(self, clients: tuple[MarketplaceClient, ...]):
        """Initialize with multiple clients.

        Args:
            clients: Tuple of MarketplaceClient instances to combine
        """
        self._clients = clients
        self._action_to_client: dict[str, MarketplaceClient] = {}
        self._cached_actions: list[ActionProtocol] = []

    async def get_protocol(self):
        """Get combined protocol from all clients.

        Merges action protocols from all clients and detects name collisions.
        Builds internal mapping for action routing.

        Returns:
            Combined ActionProtocolResponse with all actions

        Raises:
            ValueError: If multiple clients define actions with the same name
        """
        self._action_to_client.clear()
        self._cached_actions.clear()

        for client in self._clients:
            protocol_response = await client.actions.get_protocol()

            for action in protocol_response.actions:
                action_name = action.name

                # Check for collisions
                if action_name in self._action_to_client:
                    raise ValueError(
                        f"Action name collision: '{action_name}' is defined in multiple clients. "
                        f"Each action name must be unique across all clients."
                    )

                # Register action
                self._action_to_client[action_name] = client
                self._cached_actions.append(action)

        # Return a protocol-like response
        return _CompositeProtocolResponse(actions=self._cached_actions)

    async def execute_request(self, request: ActionExecutionRequest) -> ActionExecutionResult:
        """Execute action by routing to the appropriate client.

        Args:
            request: Action execution request with name and parameters

        Returns:
            Result of executing the action

        Raises:
            ValueError: If action name is not recognized
        """
        # Ensure protocol has been fetched
        if not self._action_to_client:
            await self.get_protocol()

        # Look up which client owns this action
        client = self._action_to_client.get(request.name)

        if client is None:
            return ActionExecutionResult(
                content=f"Unknown action: '{request.name}'. "
                f"This action is not registered in any of the composite clients.",
                is_error=True,
            )

        # Delegate to the appropriate client
        return await client.actions.execute_request(request)


class _CompositeProtocolResponse:
    """Simple response object for combined protocol."""

    def __init__(self, actions: list[ActionProtocol]):
        self.actions = actions


class CompositeClient:
    """Composite client that combines multiple MarketplaceClients into one.

    This client merges actions from multiple clients and delegates
    execution to the appropriate client based on action name. It detects
    and fails fast on action name collisions between clients.

    Attributes:
        clients: Tuple of child clients to combine
        actions: Combined actions resource for protocol and execution
    """

    def __init__(self, *clients: MarketplaceClient):
        """Initialize composite client with child clients.

        Args:
            *clients: Variable number of MarketplaceClient instances to combine

        Example:
            >>> client = CompositeClient(
            ...     MarketplaceClient("http://localhost:8000"),
            ...     MarketplaceClient("http://localhost:8001"),
            ... )
        """
        self.clients = clients
        self.actions = CompositeActionsResource(clients)
        self._agent_id: str | None = None

    def set_agent_id(self, agent_id: str) -> None:
        """Set agent ID on all underlying clients.

        Args:
            agent_id: The agent ID to set
        """
        self._agent_id = agent_id
        for client in self.clients:
            client.set_agent_id(agent_id)

    async def connect(self) -> None:
        """Connect all underlying clients."""
        for client in self.clients:
            await client.connect()

    async def close(self) -> None:
        """Close all underlying clients."""
        for client in self.clients:
            await client.close()

    async def __aenter__(self) -> "CompositeClient":
        """Async context manager entry."""
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Async context manager exit."""
        await self.close()
