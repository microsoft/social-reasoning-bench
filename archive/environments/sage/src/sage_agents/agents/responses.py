"""Agent implementation using OpenAI's Responses API with marketplace tools."""

from magentic_marketplace.platform.shared.models import (
    ActionExecutionRequest,
    ActionProtocol,
)
from openai.types.responses.function_tool_param import FunctionToolParam
from openai.types.responses.response_function_tool_call import (
    ResponseFunctionToolCall,
)
from pydantic_core import from_json, to_json

from .base import BaseOpenAIAgent, OpenAIAgentProfile


class ResponsesAgent(BaseOpenAIAgent):
    """A tool-calling agent that uses OpenAI's Responses API.

    This agent:
    - Fetches available tools from the marketplace protocol on startup
    - Uses OpenAI's Conversation API to maintain context across steps
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
        """Initialize the responses agent.

        Args:
            profile: The agent profile with identity and goal
            base_url: The marketplace server URL
            openai_api_key: OpenAI API key (or set OPENAI_API_KEY env var)
            openai_model: The OpenAI model to use
            max_iterations: Maximum number of steps before stopping
        """
        super().__init__(profile, base_url, openai_api_key, openai_model, max_iterations)

        # Will be populated on startup
        self._conversation_id: str | None = None
        self._tools: list[FunctionToolParam] = []

    async def on_started(self):
        """Fetch protocol and create conversation on agent startup."""
        await super().on_started()

        # Fetch available actions from marketplace
        protocol = await self.get_protocol()

        # Convert ActionProtocol objects to OpenAI function definitions
        # Convert all protocol actions (including Wait and Shutdown) to OpenAI tools
        self._tools = [self._action_protocol_to_openai_tool(action) for action in protocol.actions]

        # Get messages from profile and convert to Responses API format
        profile_messages = self.profile.get_messages()

        # Convert ChatCompletionMessageParam to Responses API items format
        conversation_items = []
        for msg in profile_messages:
            if msg["role"] == "system":
                conversation_items.append(
                    {
                        "type": "message",
                        "role": "system",
                        "content": [{"type": "input_text", "text": msg["content"]}],
                    }
                )
            elif msg["role"] == "user":
                conversation_items.append(
                    {
                        "type": "message",
                        "role": "user",
                        "content": [{"type": "input_text", "text": msg["content"]}],
                    }
                )
            elif msg["role"] == "assistant":
                # Handle assistant messages if present
                conversation_items.append(
                    {
                        "type": "message",
                        "role": "assistant",
                        "content": [{"type": "output_text", "text": msg.get("content", "")}],
                    }
                )

        # Create conversation with initial messages
        conversation = await self._openai_client.conversations.create(items=conversation_items)

        self._conversation_id = conversation.id
        self.logger.info(f"Conversation created: {self._conversation_id}")
        self.logger.info(f"Loaded {len(self._tools)} tools from marketplace")

    def _action_protocol_to_openai_tool(self, action: ActionProtocol) -> FunctionToolParam:
        """Convert an ActionProtocol to OpenAI Responses API tool format.

        Args:
            action: The marketplace action protocol

        Returns:
            OpenAI Responses API function tool definition (flat structure)
        """
        return {
            "type": "function",
            "name": action.name,
            "description": action.description,
            "parameters": action.parameters,
            "strict": None,
        }

    async def step(self):
        """Execute one step of the agent's reasoning and action loop."""
        if not self._check_max_iterations():
            return

        if not self._conversation_id:
            raise RuntimeError("Conversation not initialized. Call on_started() first.")

        try:
            # Get response from the model with available tools
            # Pass conversation ID as input for responses API
            response = await self._openai_client.responses.create(
                conversation=self._conversation_id,
                model=self._model,
                tools=self._tools,
                tool_choice="required",
                input="Take your next action.",
            )

            # Process the response
            if response.output:
                for output_item in response.output:
                    if output_item.type == "reasoning":
                        # Agent is reasoning (extended thinking)
                        content = output_item.content
                        if isinstance(content, list):
                            for content_item in content:
                                if content_item.type == "output_text":
                                    self.logger.info(f"Reasoning: {content_item.text}")

                    elif output_item.type == "message":
                        # Agent's message output
                        content = output_item.content

                        if isinstance(content, list):
                            for content_item in content:
                                if content_item.type == "output_text":
                                    self.logger.info(f"Agent: {content_item.text}")
                        elif isinstance(content, str):
                            self.logger.info(f"Agent: {content}")

                    elif output_item.type == "function_call":
                        # Agent wants to execute a tool
                        await self._handle_function_call(output_item)

        except Exception as e:
            self.logger.error(f"Error in step: {e}")
            raise

    async def _handle_function_call(self, function_call: ResponseFunctionToolCall):
        """Execute a function call from the model.

        Args:
            function_call: The function call output from OpenAI Responses API
        """
        if not self._conversation_id:
            raise RuntimeError("Conversation not initialized.")

        function_name = function_call.name
        arguments = (
            from_json(function_call.arguments)
            if isinstance(function_call.arguments, str)
            else function_call.arguments
        )

        self.logger.info(f"Executing tool: {function_name} with args: {arguments}")

        try:
            # Ensure type field is present for Pydantic discriminator
            if isinstance(arguments, dict) and "type" not in arguments:
                arguments["type"] = function_name

            # Create action execution request
            action_request = ActionExecutionRequest(
                name=function_name,
                parameters=arguments,
            )

            # Execute the action through the marketplace
            result = await self.client.actions.execute_request(action_request)

            # Prepare result content
            result_content = (
                to_json(result.content).decode()
                if not isinstance(result.content, str)
                else result.content
            )

            # Add the function result back to the conversation
            await self._openai_client.conversations.items.create(
                conversation_id=self._conversation_id,
                items=[
                    {
                        "type": "function_call_output",
                        "call_id": function_call.call_id,
                        "output": result_content,
                    }
                ],
            )

            if result.is_error:
                self.logger.error(f"Tool execution failed: {result.content}")
            else:
                self.logger.info(f"Tool result: {result.content}")

        except Exception as e:
            self.logger.error(f"Error executing tool {function_name}: {e}")
            # Report error back to the conversation
            await self._openai_client.conversations.items.create(
                conversation_id=self._conversation_id,
                items=[
                    {
                        "type": "function_call_output",
                        "call_id": function_call.call_id,
                        "output": f"Error executing tool: {str(e)}",
                    }
                ],
            )
