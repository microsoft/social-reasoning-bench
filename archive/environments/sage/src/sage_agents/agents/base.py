"""Base agent class for OpenAI-powered marketplace agents."""

from abc import abstractmethod
from typing import TYPE_CHECKING, Any, TypeVar

from magentic_marketplace.platform.agent.base import BaseAgent
from magentic_marketplace.platform.shared.models import (
    ActionExecutionRequest,
    AgentProfile,
)
from openai import AsyncOpenAI
from openai.types.chat import ChatCompletionMessageParam
from pydantic import Field
from pydantic_core import to_json

if TYPE_CHECKING:
    from ..hooks.base import ToolHook

T = TypeVar("T", bound="BaseOpenAIAgent")


class OpenAIAgentProfile(AgentProfile):
    """Profile for OpenAI-powered agents."""

    full_name: str
    email_address: str
    messages: list[ChatCompletionMessageParam] = Field(
        description="List of messages to initialize the agent context",
    )

    def get_messages(self) -> list[ChatCompletionMessageParam]:
        """Get messages list for agent initialization.

        Returns:
            List of chat completion messages for agent initialization
        """
        return self.messages


class BaseOpenAIAgent(BaseAgent[OpenAIAgentProfile]):
    """Base class for agents using OpenAI APIs with marketplace tools.

    This abstract base class provides common functionality for agents that use
    OpenAI's APIs (Responses or Chat Completions) to accomplish goals through
    marketplace actions.
    """

    def __init__(
        self,
        profile: OpenAIAgentProfile,
        base_url: str,
        openai_api_key: str | None = None,
        openai_model: str = "",
        max_iterations: int = 50,
    ):
        """Initialize the OpenAI agent.

        Args:
            profile: The agent profile with identity and task
            base_url: The marketplace server URL
            openai_api_key: OpenAI API key (or set OPENAI_API_KEY env var)
            openai_model: The OpenAI model to use
            max_iterations: Maximum number of steps before stopping
        """
        super().__init__(profile, base_url)
        self._openai_client = AsyncOpenAI(api_key=openai_api_key)
        self._model = openai_model
        self._max_iterations = max_iterations
        self._iteration_count = 0
        self._tool_hooks: dict[str, Any] = {}  # Maps tool name -> ToolHook instance

    def _check_max_iterations(self) -> bool:
        """Check if max iterations reached and shutdown if so.

        Returns:
            True if should continue, False if should stop
        """
        self._iteration_count += 1
        if self._iteration_count > self._max_iterations:
            self.logger.info(f"Reached max iterations ({self._max_iterations}), stopping")
            self.shutdown()
            return False
        return True

    def register_hooks(self, hooks: "ToolHook") -> T:  # type: ignore
        """Register tool hooks with this agent.

        This method registers before/after execution hooks for a specific action type.

        Example:
            agent = ChatCompletionsAgent(...)
            agent.register_hooks(WaitHooks())
            agent.register_hooks(ShutdownHooks())

        Args:
            hooks: The ToolHook instance to register

        Returns:
            Self for method chaining

        Raises:
            ValueError: If hooks for the same tool are already registered
        """
        # Runtime import for isinstance check (TYPE_CHECKING import is for type hints only)
        from ..hooks.base import ToolHook as ToolHookClass

        if not isinstance(hooks, ToolHookClass):
            raise TypeError(f"Hooks must be an instance of ToolHook, got {type(hooks)}")

        # Inject agent reference into hooks
        hooks._agent = self

        # Get tool name from hooks instance
        tool_name = hooks.get_tool_name()

        if tool_name in self._tool_hooks:
            raise ValueError(
                f"Hooks for tool '{tool_name}' are already registered. "
                f"Cannot register duplicate hooks."
            )

        self._tool_hooks[tool_name] = hooks

        return self  # type: ignore

    async def execute_tool(self, name: str, arguments: dict) -> str:
        """Execute a tool via marketplace with optional before/after hooks.

        EXECUTION FLOW:
        1. If hooks registered: validate arguments and call before_execute()
        2. Execute action via marketplace API (for server-side trajectory logging)
        3. If hooks registered: call after_execute() with result
        4. Return marketplace result to LLM

        DESIGN RATIONALE:
        - Server execution ensures all actions are logged in agent trajectories
        - Some server handlers are no-ops (Wait, Shutdown) - they just log the action
        - Client hooks do the actual work (asyncio.sleep, agent.shutdown())
        - This separates trajectory logging (server) from execution (client)

        HOOK CAPABILITIES:
        - before_execute: Validation, rate limiting, caching
          (can raise to prevent execution)
        - after_execute: Client-side execution, logging, metrics
          (return value ignored)

        SEPARATION OF CONCERNS:
        - Base agents are environment-agnostic (just LLM + tool calling loop)
        - Hooks are environment-specific (injected by caller, e.g. messenger CLI)
        - Server protocol handlers can be no-ops (just logging)
        - Client hooks do actual work via before/after execution hooks

        Example:
            # Messenger CLI injects environment-specific hooks:
            agent.register_hooks(WaitHooks())      # Performs asyncio.sleep
            agent.register_hooks(ShutdownHooks())  # Calls agent.shutdown()

            # When LLM calls Wait tool:
            # 1. WaitHooks.before_execute() called (validation)
            # 2. Server logs "Wait 5s" (no-op, just records to DB)
            # 3. WaitHooks.after_execute() called: await asyncio.sleep(5)
            # 4. LLM receives: "Waited for 5 seconds"

        Args:
            name: Tool name to execute
            arguments: Tool arguments dict

        Returns:
            Marketplace result as string (for LLM context)

        Raises:
            Exception: If tool execution or hooks fail
        """
        self.logger.info(f"Executing marketplace tool: {name}")
        try:
            # Get hooks if registered
            hooks = self._tool_hooks.get(name)
            validated_action = None

            # Call before_execute hook if registered
            if hooks:
                # Validate arguments into typed action
                action_class = hooks.get_action_class()
                validated_action = action_class.model_validate(arguments)

                self.logger.info(f"Calling before_execute hook for {name}")
                await hooks.before_execute(validated_action)

            # Execute via marketplace (server-side logging)
            action_request = ActionExecutionRequest(
                name=name,
                parameters=arguments,
            )
            result = await self.client.actions.execute_request(action_request)

            # Call after_execute hook if registered
            if hooks:
                # Use already validated action
                if validated_action is None:
                    # Should never happen, but validate again for type safety
                    action_class = hooks.get_action_class()
                    validated_action = action_class.model_validate(arguments)

                self.logger.info(f"Calling after_execute hook for {name}")
                await hooks.after_execute(validated_action, result)

            # Format marketplace result
            result_content = (
                to_json(result.content).decode()
                if not isinstance(result.content, str)
                else result.content
            )

            if result.is_error:
                self.logger.error(f"Tool execution failed: {result.content}")
            else:
                self.logger.info(f"Tool result: {result_content}")

            return result_content

        except Exception as e:
            self.logger.error(f"Error executing tool {name}: {e}")
            error_result = {"error": str(e), "tool": name}
            return to_json(error_result).decode()

    @abstractmethod
    async def on_started(self):
        """Fetch protocol and initialize agent on startup.

        Subclasses must implement this to set up their specific API client.
        """
        pass

    @abstractmethod
    async def step(self):
        """Execute one step of the agent's reasoning and action loop.

        Subclasses must implement this to define their specific interaction pattern.
        """
        pass
