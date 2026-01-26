"""Interviewer agent implementation."""

from typing import Any

from pydantic import BaseModel, Field

from sage_benchmark.form_filling.prompts import get_interviewer_system_prompt
from sage_benchmark.shared.model_clients import AsyncModelClient
from sage_benchmark.shared.schemas import ChatMessage, ToolCall, ToolDefinition

# --- Tool Parameter Schemas ---


class SendMessageParams(BaseModel):
    """Parameters for SendMessage tool."""

    message: str = Field(description="Message to send to the assistant")


class EndInterviewParams(BaseModel):
    """Parameters for EndInterview tool."""

    reason: str = Field(description="Why the interview is ending")


# --- External Context Building Functions ---


class InterviewerAgent:
    """Agent that conducts interviews to fill forms."""

    def __init__(self, client: AsyncModelClient, form_context: str, interviewer_type: str = "base"):
        """Initialize interviewer agent.

        Args:
            client: Model client for LLM calls
            form_context: Formatted context describing the form to fill with questions
            interviewer_type: Type of interviewer prompt ("base" or "detail")
        """
        self.client = client
        system_prompt = get_interviewer_system_prompt(interviewer_type)
        self.messages = [
            ChatMessage(role="system", content=system_prompt),
            ChatMessage(
                role="user",
                content=f"""You need to conduct an interview to gather all the information from the other person needed to fill out this form.

{form_context}

Start the interview by introducing yourself and asking your first question.""",
            ),
        ]

        # Define tools
        self.tools = [
            ToolDefinition(
                name="SendMessage",
                description="Send a message to the other person",
                parameters_schema=SendMessageParams,
            ),
            ToolDefinition(
                name="EndInterview",
                description="End the interview when you have gathered enough information",
                parameters_schema=EndInterviewParams,
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

    async def fill_form(
        self,
        form_context: str,
        form_class: type[BaseModel] | None = None,
    ) -> dict:
        fill_prompt = f"""Based on the conversation you just had, please complete the below questionaire form.

Provide your answers for each question based on what you learned during the conversation as accurately and completely as possible.

Make sure that ALL details and information you obtained during the interview are reflected in your answers. But do not add any information that was not provided during the interview.

Here is the form you need to fill out:
{form_context}
"""
        self.messages.append(ChatMessage(role="user", content=fill_prompt))

        submit_tool = ToolDefinition(
            name="SubmitForm",
            description="Submit the completed form with all your answers matching the form schema",
            parameters_schema=form_class,
        )

        # Call LLM with tool
        result = await self.client.call_llm_with_tools(messages=self.messages, tools=[submit_tool])

        if result.error or result.tool_call is None:
            raise ValueError(f"Failed to get form submission: {result.error}")

        if result.tool_call.tool_name != "SubmitForm":
            raise ValueError(f"Expected SubmitForm tool call, got: {result.tool_call.tool_name}")

        # Return the form as a dict
        return result.tool_call.arguments
