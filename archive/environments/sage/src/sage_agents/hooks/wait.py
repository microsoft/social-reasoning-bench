"""Generic hooks for wait actions."""

import asyncio
from typing import TypeVar

from magentic_marketplace.platform.shared.models import ActionExecutionResult, BaseAction

from .base import ToolHook

T = TypeVar("T", bound=BaseAction)


class WaitHook(ToolHook[T]):
    """Generic hooks that provide wait action implementation.

    Performs actual client-side sleep after the server logs the action.
    The server-side handler is a no-op that just records the action.

    Works with any action class that has a 'duration' field.

    Example:
        from my_protocol.actions import MyWaitAction

        agent.register_hooks(WaitHook(MyWaitAction))
    """

    def __init__(self, action_class: type[T]):
        """Initialize wait hooks with the action class.

        Args:
            action_class: The wait action class to handle (must have 'duration' field)
        """
        super().__init__(action_class)

    async def after_execute(self, action: T, result: ActionExecutionResult) -> None:
        """Perform actual client-side sleep after server logs the action.

        Args:
            action: Wait action with duration field
            result: Marketplace execution result (unused)
        """
        duration = getattr(action, "duration", 0)
        self.agent.logger.info(f"Waiting for {duration} second(s)")
        await asyncio.sleep(duration)
