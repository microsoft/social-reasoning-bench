"""Interviewer agent implementation."""

from typing import Any

from pydantic import BaseModel, Field

from sage_benchmark.shared.model_clients import AsyncModelClient
from sage_benchmark.shared.schemas import ChatMessage, ToolCall, ToolDefinition

# --- Tool Parameter Schemas ---


class SendMessageParams(BaseModel):
    """Parameters for SendMessage tool."""

    message: str = Field(description="Message to send to the assistant")


class EndInterviewParams(BaseModel):
    """Parameters for EndInterview tool."""

    reason: str = Field(description="Why the interview is ending")


# --- System Prompt ---

INTERVIEWER_SYSTEM_PROMPT = """You are an interviewer conducting an interview to fill out a form.

You have been given a form with specific questions that need to be answered. Your goal is to have a natural conversation with the assistant to gather the information needed to complete the form.

Guidelines:
- Ask questions naturally and conversationally
- You may ask follow-up questions to clarify or get more detail
- Be professional and respectful
- When you have gathered sufficient information, end the interview
- You will fill out the form AFTER the conversation ends

You have two tools available:
- SendMessage: Send a message to the assistant
- EndInterview: End the interview when you have gathered enough information"""


# --- External Context Building Functions ---


class InterviewerAgent:
    """Agent that conducts interviews to fill forms."""

    def __init__(self, client: AsyncModelClient, form_context: str):
        """Initialize interviewer agent.

        Args:
            client: Model client for LLM calls
            form_context: Formatted context describing the form to fill with questions
        """
        self.client = client
        self.messages = [
            ChatMessage(role="system", content=INTERVIEWER_SYSTEM_PROMPT),
            ChatMessage(
                role="user",
                content=f"""You need to conduct an interview to gather all the information needed to fill out this form.

{form_context}

Start the interview by introducing yourself and asking your first question.""",
            ),
        ]

        # Define tools
        self.tools = [
            ToolDefinition(
                name="SendMessage",
                description="Send a message to the assistant",
                parameters_schema=SendMessageParams,
            ),
            ToolDefinition(
                name="EndInterview",
                description="End the interview when you have enough information",
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
        fill_prompt = f"""Based on the conversation you just had, please fill out the form using the SubmitForm tool.

Provide your answers for each question based on what you learned during the conversation.

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
