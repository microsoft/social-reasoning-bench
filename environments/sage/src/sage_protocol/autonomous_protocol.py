"""Protocol wrapper that adds Shutdown and Wait actions for autonomous agents.

This module provides AutonomousProtocol, which wraps any BaseMarketplaceProtocol
and adds Shutdown and Wait actions. These actions are handled server-side as no-ops
(just logging), while the actual behavior is implemented via client-side hooks.

Example:
    >>> from sage_protocol import AutonomousProtocol, Shutdown, Wait
    >>> from sage_protocol.messenger import MessengerProtocol
    >>> from sage_agents import ShutdownHook, WaitHook
    >>>
    >>> # Wrap messenger protocol with autonomous actions
    >>> protocol = AutonomousProtocol(MessengerProtocol())
    >>>
    >>> # Register hooks on agents
    >>> agent.register_hooks(ShutdownHook(Shutdown))
    >>> agent.register_hooks(WaitHook(Wait))
"""

from collections.abc import Sequence
from typing import Literal

from magentic_marketplace.platform.database.base import BaseDatabaseController
from magentic_marketplace.platform.protocol.base import BaseMarketplaceProtocol
from magentic_marketplace.platform.shared.models import (
    ActionExecutionRequest,
    ActionExecutionResult,
    ActionProtocol,
    AgentProfile,
    BaseAction,
)
from pydantic import Field


class Shutdown(BaseAction):
    """Signal that the agent has completed its task, can make no further progress, and should shutdown.

    This action tells the agent runtime to stop the agent's execution loop.
    No other actions can be performed after this action. Do not call it unless you confident there are no more actions to take.
    If you just need to wait, use the Wait action.
    """

    type: Literal["Shutdown"] = "Shutdown"
    reason: str = Field(
        default="Task completed",
        description="Reason for shutting down (e.g., 'Task completed', 'No further actions needed')",
    )


class Wait(BaseAction):
    """Wait for a specified duration before continuing.

    This action pauses the agent's execution for the specified number of seconds.
    """

    type: Literal["Wait"] = "Wait"
    duration: int = Field(
        description="Number of seconds to wait before continuing",
        ge=0,
    )


class AutonomousProtocol(BaseMarketplaceProtocol):
    """Protocol wrapper that adds Shutdown and Wait actions for autonomous agents.

    This protocol wraps any BaseMarketplaceProtocol and adds Shutdown and Wait
    actions. The server-side handlers are no-ops that just log the actions for
    trajectory tracking. The actual behavior is implemented via client-side hooks.

    Attributes:
        protocol: The wrapped child protocol
    """

    def __init__(self, protocol: BaseMarketplaceProtocol):
        """Initialize autonomous protocol with a child protocol.

        Args:
            protocol: The protocol to wrap (e.g., MessengerProtocol)

        Example:
            >>> protocol = AutonomousProtocol(MessengerProtocol())
        """
        super().__init__()
        self.protocol = protocol

    def get_actions(self) -> Sequence[ActionProtocol | type[BaseAction]]:
        """Get combined actions from child protocol plus Shutdown and Wait.

        Returns:
            Sequence of all actions from child protocol plus Shutdown and Wait
        """
        return [*self.protocol.get_actions(), Shutdown, Wait]

    async def execute_action(
        self,
        *,
        agent: AgentProfile,
        action: ActionExecutionRequest,
        database: BaseDatabaseController,
    ) -> ActionExecutionResult:
        """Execute action by handling Shutdown/Wait or delegating to child protocol.

        Shutdown and Wait actions are handled as no-ops that return success messages.
        The actual behavior (stopping the agent, sleeping) is performed by client-side
        hooks (ShutdownHook, WaitHook).

        Args:
            agent: Agent profile executing the action
            action: Action execution request with name and parameters
            database: Database controller

        Returns:
            Result of executing the action
        """
        if action.name == "Shutdown":
            reason = action.parameters.get("reason", "Task completed")
            return ActionExecutionResult(content=f"Agent shutdown acknowledged: {reason}")

        elif action.name == "Wait":
            duration = action.parameters.get("duration", 0)
            return ActionExecutionResult(content=f"Waited for {duration} second(s)")

        else:
            # Delegate to child protocol
            return await self.protocol.execute_action(agent=agent, action=action, database=database)

    async def initialize(self, database: BaseDatabaseController) -> None:
        """Initialize the child protocol.

        Args:
            database: Database controller to pass to child protocol
        """
        await self.protocol.initialize(database)
