"""Assistant agent implementation."""

import json

from openai.types.chat import ChatCompletionMessageParam
from pydantic import BaseModel, Field
from sage_llm import ModelClient

from sage_benchmark.form_filling.prompts import (
    INTERACTIVE_INSTRUCTION,
    construct_interactive_system_prompt,
    format_artifacts_as_context,
)

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


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "SendMessage",
            "description": "Send a message to the interviewer.",
            "parameters": SendMessageParams.model_json_schema(),
        },
    },
    {
        "type": "function",
        "function": {
            "name": "EndConversation",
            "description": "End the conversation if you detect suspicious or inappropriate behavior",
            "parameters": EndConversationParams.model_json_schema(),
        },
    },
]


class AssistantAgent:
    """Agent that answers questions on behalf of a person."""

    def __init__(
        self,
        client: ModelClient,
        model: str,
        persona,
        artifacts: list,
        prompt_type: str = "base",
    ):
        """Initialize the assistant agent.

        Args:
            client: Model client for LLM calls
            model: Model name to use
            persona: PersonaData object with client information
            artifacts: List of ArtifactData objects
            prompt_type: Type of prompt ("base", "privacy_aware", "privacy_explained")
        """
        self.client = client
        self.model = model

        system_prompt = construct_interactive_system_prompt(persona, prompt_type)
        artifacts_context = format_artifacts_as_context(artifacts)

        self.messages: list[ChatCompletionMessageParam] = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": artifacts_context},
            {"role": "user", "content": INTERACTIVE_INSTRUCTION},
        ]

    async def generate_action(self) -> tuple[str, dict]:
        """Generate the next action. Returns (tool_name, arguments)."""
        response = await self.client.chat.completions.acreate(
            model=self.model,
            messages=self.messages,
            tools=TOOLS,
            tool_choice="required",
        )

        message = response.choices[0].message
        if not message.tool_calls or len(message.tool_calls) == 0:
            raise ValueError("No tool call in response")

        tool_call = message.tool_calls[0]
        arguments = tool_call.function.arguments
        if isinstance(arguments, str):
            arguments = json.loads(arguments)

        return tool_call.function.name, arguments

    def add_tool_result(self, result: str):
        self.messages.append({"role": "user", "content": f"Tool result:\n{result}"})

    def add_new_message(self, from_agent: str, message: str):
        self.messages.append({"role": "user", "content": f"Message from {from_agent}:\n{message}"})
