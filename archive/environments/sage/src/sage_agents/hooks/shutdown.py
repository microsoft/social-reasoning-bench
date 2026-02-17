"""Generic hooks for shutdown actions."""

from typing import TypeVar

from magentic_marketplace.platform.shared.models import ActionExecutionResult, BaseAction

from .base import ToolHook

T = TypeVar("T", bound=BaseAction)


class ShutdownHook(ToolHook[T]):
    """Generic hooks that provide shutdown action implementation.

    Stops the agent loop after the server logs the action.
    The server-side handler is a no-op that just records the action.

    Works with any action class that represents a shutdown signal.

    Example:
        from my_protocol.actions import MyShutdownAction

        agent.register_hooks(ShutdownHook(MyShutdownAction))
    """

    def __init__(self, action_class: type[T]):
        """Initialize shutdown hooks with the action class.

        Args:
            action_class: The shutdown action class to handle
        """
        super().__init__(action_class)

    async def after_execute(self, action: T, result: ActionExecutionResult) -> None:
        """Shutdown agent after server logs the action.

        Args:
            action: Shutdown action instance
            result: Marketplace execution result (unused)
        """
        # Try to get reason if the action has one
        reason = getattr(action, "reason", "No reason provided")
        self.agent.logger.info(f"Shutdown signal received: {reason}")
        self.agent.shutdown()
