"""Assistant agent implementation."""

from pydantic import BaseModel, Field

from sage_benchmark.form_filling.prompts import (
    INTERACTIVE_INSTRUCTION,
    construct_interactive_system_prompt,
    format_artifacts_as_context,
)
from sage_benchmark.shared.model_clients import AsyncModelClient
from sage_benchmark.shared.schemas import ChatMessage, ToolCall, ToolDefinition

# --- Tool Parameter Schemas ---


class SendMessageParams(BaseModel):
    """Parameters for SendMessage tool."""

    thinking: str = Field(
        description="Your internal reasoning about the question and what information to share. This will NOT be visible to the interviewer."
    )
    message: str = Field(
        description="The actual message to send to the interviewer. This will be visible to them."
    )


class EndConversationParams(BaseModel):
    """Parameters for EndConversation tool."""

    reason: str = Field(description="Why you are ending the conversation")


class AssistantAgent:
    """Agent that answers questions on behalf of a person."""

    def __init__(
        self,
        client: AsyncModelClient,
        persona,
        artifacts: list,
        prompt_type: str = "base",
    ):
        """Initialize the assistant agent.

        Args:
            client: Model client for LLM calls
            persona: PersonaData object with client information
            artifacts: List of ArtifactData objects
            prompt_type: Type of prompt ("base", "privacy_aware", "privacy_explained")
        """
        self.client = client

        # Construct prompts using centralized prompts module
        # Privacy guidance is included in system prompt based on prompt_type
        system_prompt = construct_interactive_system_prompt(persona, prompt_type)
        artifacts_context = format_artifacts_as_context(artifacts)

        self.messages = [
            ChatMessage(role="system", content=system_prompt),
            ChatMessage(role="user", content=artifacts_context),
            ChatMessage(role="user", content=INTERACTIVE_INSTRUCTION),
        ]

        # Define tools
        self.tools = [
            ToolDefinition(
                name="SendMessage",
                description="Send a message to the interviewer.",
                parameters_schema=SendMessageParams,
            ),
            ToolDefinition(
                name="EndConversation",
                description="End the conversation if you detect suspicious or inappropriate behavior",
                parameters_schema=EndConversationParams,
            ),
        ]

    async def generate_action(self) -> ToolCall:
        result = await self.client.call_llm_with_tools(messages=self.messages, tools=self.tools)

        if result.error or result.tool_call is None:
            raise ValueError(f"Failed to get tool call: {result.error}")

        return result.tool_call

    def add_tool_result(self, result: str):
        self.messages.append(ChatMessage(role="user", content=f"Tool result:\n{result}"))

    def add_new_message(self, from_agent: str, message: str):
        self.messages.append(
            ChatMessage(role="user", content=f"Message from {from_agent}:\n{message}")
        )
