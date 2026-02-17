"""Base class for action-specific hooks with before/after execution methods."""

from typing import TYPE_CHECKING, Generic, TypeVar, get_args, get_origin

from magentic_marketplace.platform.shared.models import (
    ActionExecutionResult,
    BaseAction,
)

if TYPE_CHECKING:
    from ..agents.base import BaseOpenAIAgent

T = TypeVar("T", bound=BaseAction)


class ToolHook(Generic[T]):
    """Base class for action-specific hooks with before/after execution methods.

    Type parameter T should be a BaseAction subclass.
    The hooks will automatically validate raw dict arguments into T instances.

    Can be used in two ways:

    1. Subclass with type parameter (for custom hook logic):
        class MyCustomHooks(ToolHook[MyAction]):
            async def after_execute(self, action: MyAction, result: ActionExecutionResult):
                # Custom logic here
                pass

    2. Instantiate with action class (for generic hooks like ShutdownHooks):
        hooks = ShutdownHooks(MyShutdownAction)
        agent.register_hooks(hooks)
    """

    def __init__(self, action_class: type[T] | None = None):
        """Initialize the hooks instance.

        Args:
            action_class: Optional action class to use. If not provided,
                          will be extracted from the type parameter.
        """
        self._agent: "BaseOpenAIAgent | None" = None
        self._action_class: type[T] | None = action_class

    @property
    def agent(self) -> "BaseOpenAIAgent":
        """Get the agent instance this hook is registered with.

        Raises:
            RuntimeError: If hooks have not been registered with an agent yet
        """
        if self._agent is None:
            raise RuntimeError(
                f"{self.__class__.__name__} has not been registered with an agent. "
                "Call agent.register_hooks(hooks) first."
            )
        return self._agent

    def get_action_class(self) -> type[BaseAction]:
        """Get the BaseAction type for this hooks instance.

        Returns action class from either:
        1. Instance attribute (if passed to constructor)
        2. Class type parameter (if subclassed with ToolHook[T])

        Returns:
            The BaseAction subclass

        Raises:
            TypeError: If no action class is available
        """
        # First check instance attribute
        if self._action_class is not None:
            return self._action_class

        # Fall back to extracting from type parameter
        return self._get_action_class_from_type_param()

    @classmethod
    def _get_action_class_from_type_param(cls) -> type[BaseAction]:
        """Extract the BaseAction type from ToolHook[T] class definition.

        Returns:
            The BaseAction subclass used as the type parameter

        Raises:
            TypeError: If the class doesn't specify a BaseAction type parameter
        """
        # Look through the class hierarchy for Generic[T] specification
        for base in cls.__orig_bases__:  # type: ignore
            origin = get_origin(base)
            # Check if this base is ToolHook or a Generic type
            if origin is not None and (
                origin is ToolHook or issubclass(origin, ToolHook)  # type: ignore
            ):
                args = get_args(base)
                if args and len(args) > 0:
                    action_class = args[0]
                    # Verify it's actually a BaseAction subclass
                    if isinstance(action_class, type) and issubclass(action_class, BaseAction):
                        return action_class

        raise TypeError(
            f"{cls.__name__} must either be instantiated with an action_class "
            f"or inherit from ToolHook[T] where T is a BaseAction subclass."
        )

    def get_tool_name(self) -> str:
        """Get the tool name from the action class.

        Returns:
            The tool name (e.g., "Wait", "Shutdown")
        """
        return self.get_action_class().get_name()

    async def before_execute(self, action: T) -> None:
        """Called before marketplace execution.

        Override this method to add pre-execution logic such as:
        - Validation (raise exceptions to prevent execution)
        - Rate limiting
        - Caching checks
        - Logging

        Args:
            action: Validated action instance of type T

        Raises:
            Any exception to prevent marketplace execution
        """
        pass

    async def after_execute(self, action: T, result: ActionExecutionResult) -> None:
        """Called after marketplace execution.

        Override this method to add post-execution logic such as:
        - Client-side execution (e.g., actual sleep, shutdown)
        - Modifying result.content to change what the LLM sees
        - Logging
        - Metrics collection
        - State updates

        Args:
            action: Validated action instance of type T
            result: Marketplace execution result (can be modified in-place)

        Note:
            Return value is ignored. To modify what the LLM sees, update
            result.content or result.is_error in-place.
        """
        pass
