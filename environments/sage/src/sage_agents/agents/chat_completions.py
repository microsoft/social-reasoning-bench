"""Agent implementation using OpenAI's Chat Completions API with marketplace tools."""

from magentic_marketplace.platform.shared.models import ActionProtocol
from openai.types.chat import ChatCompletionMessageParam, ChatCompletionToolParam
from openai.types.chat.chat_completion_message_tool_call import (
    ChatCompletionMessageToolCallUnion,
)
from pydantic_core import from_json

from .base import BaseOpenAIAgent, OpenAIAgentProfile


class ChatCompletionsAgent(BaseOpenAIAgent):
    """A tool-calling agent that uses OpenAI's Chat Completions API.

    This agent:
    - Fetches available tools from the marketplace protocol on startup
    - Manages conversation history manually as a message list
    - Executes marketplace actions as tools to accomplish its goal
    """

    def __init__(
        self,
        profile: OpenAIAgentProfile,
        base_url: str,
        openai_api_key: str | None = None,
        openai_model: str = "",
        max_iterations: int = 50,
    ):
        """Initialize the chat completions agent.

        Args:
            profile: The agent profile with identity and goal
            base_url: The marketplace server URL
            openai_api_key: OpenAI API key (or set OPENAI_API_KEY env var)
            openai_model: The OpenAI model to use
            max_iterations: Maximum number of steps before stopping
        """
        super().__init__(profile, base_url, openai_api_key, openai_model, max_iterations)

        # Will be populated on startup
        self._messages: list[ChatCompletionMessageParam] = []
        self._tools: list[ChatCompletionToolParam] = []

    async def on_started(self):
        """Fetch protocol and initialize conversation on agent startup."""
        await super().on_started()

        # Fetch available actions from marketplace
        protocol = await self.get_protocol()

        # Convert ActionProtocol objects to OpenAI function definitions
        # Convert all protocol actions (including Wait and Stop) to chat tools
        self._tools = [self._action_protocol_to_chat_tool(action) for action in protocol.actions]

        # Initialize message history from profile
        # Profile provides messages list (either directly or converted from
        # legacy fields)
        self._messages = self.profile.get_messages().copy()

        self.logger.info(f"Chat initialized with {len(self._tools)} tools")

    def _action_protocol_to_chat_tool(self, action: ActionProtocol) -> ChatCompletionToolParam:
        """Convert an ActionProtocol to OpenAI Chat Completions tool format.

        Args:
            action: The marketplace action protocol

        Returns:
            OpenAI chat completion tool definition
        """
        return {
            "type": "function",
            "function": {
                "name": action.name,
                "description": action.description,
                "parameters": action.parameters,
            },
        }

    async def step(self):
        """Execute one step of the agent's reasoning and action loop."""
        if not self._check_max_iterations():
            return

        try:
            # Get completion from the model with available tools
            completion = await self._openai_client.chat.completions.create(
                model=self._model,
                messages=self._messages,
                tools=self._tools,
                tool_choice="required",
            )

            # Get the assistant's response
            message = completion.choices[0].message

            # Add assistant message to history
            assistant_message: ChatCompletionMessageParam = {
                "role": "assistant",
                "content": message.content,
            }
            if message.tool_calls:
                assistant_message["tool_calls"] = message.tool_calls  # type: ignore
            self._messages.append(assistant_message)

            # Log any text content
            if message.content:
                self.logger.info(f"Agent: {message.content}")

            # Handle tool calls if present
            if message.tool_calls:
                for tool_call in message.tool_calls:
                    await self._handle_tool_call(tool_call)

        except Exception as e:
            self.logger.error(f"Error in step: {e}")
            raise

    async def _handle_tool_call(self, tool_call: ChatCompletionMessageToolCallUnion):
        """Execute a tool call from the model.

        Args:
            tool_call: The tool call from OpenAI Chat Completions API
        """
        # Only handle function tool calls, skip custom tool calls
        if tool_call.type != "function":
            self.logger.warning(f"Skipping non-function tool call of type: {tool_call.type}")
            return

        function_name = tool_call.function.name
        arguments = from_json(tool_call.function.arguments)

        self.logger.info(f"Executing tool: {function_name} with args: {arguments}")

        try:
            # Ensure type field is present for Pydantic discriminator
            if isinstance(arguments, dict) and "type" not in arguments:
                arguments["type"] = function_name

            # Execute tool via base class (handles hooks if registered)
            result_content = await self.execute_tool(function_name, arguments)

            # Add the function result back to the conversation
            self._messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result_content,
                }
            )

        except Exception as e:
            self.logger.error(f"Error executing tool {function_name}: {e}")
            # Report error back to the conversation
            self._messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": f"Error executing tool: {str(e)}",
                }
            )
