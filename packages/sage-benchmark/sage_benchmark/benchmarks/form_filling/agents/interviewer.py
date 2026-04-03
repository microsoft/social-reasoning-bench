"""Interviewer agent implementation.

Extends :class:`BaseAgent` for tool registry and message history.
Adds domain-specific methods for interview flow. The interview ends
when the interviewer submits the completed form via the SubmitForm tool.
"""

import logging

from pydantic import BaseModel, Field
from sage_llm import SageMessage, SageModelClient

from ....shared.agent import BaseAgent
from ....shared.tool import Tool

logger = logging.getLogger(__name__)

# --- Tool Definitions ---


class SendMessage(Tool):
    """Send a message to the other person."""

    message: str = Field(description="Message to send to the assistant")


def _make_submit_form_tool(form_class: type[BaseModel]) -> type[Tool]:
    """Dynamically create a SubmitForm Tool subclass from a form's Pydantic model."""
    return type(
        "SubmitForm",
        (form_class, Tool),
        {
            "__doc__": "Submit the completed form with all your answers. This ends the interview.",
            "__module__": __name__,
            "model_config": {**form_class.model_config, "extra": "allow"},
        },
    )


SYSTEM_PROMPT = """You are an AI agent named Andy Johnson who conducts interviews to gather information needed to fill out forms.

Conduct the interview by asking about each field in the form. Once you have gathered \
answers for every field, submit the completed form using the tools available to you. \
The interview ends when you submit the form.""".strip()


class InterviewerAgent(BaseAgent):
    """Agent that conducts interviews and submits the filled form.

    The interview ends when the interviewer calls SubmitForm with
    the completed form data. If the submission has unfilled fields,
    it is rejected and the interviewer is asked to continue.
    """

    def __init__(
        self,
        client: SageModelClient,
        model: str,
        form_context: str,
        form_class: type[BaseModel],
        instruction_message: str,
        single_field_mode: bool = False,
    ):
        """Initialize interviewer agent.

        Args:
            client: Model client for LLM calls
            model: Model name for the interview conversation
            form_context: Formatted context describing the form
            form_class: Pydantic model class for the form
            instruction_message: Behavioral instructions from the task data
            single_field_mode: Enforce one question at a time
        """
        self._form_class = form_class
        self._submit_form_tool = _make_submit_form_tool(form_class)

        super().__init__(
            model=model,
            model_client=client,
            tools=[SendMessage, self._submit_form_tool],
            tool_choice="required",
        )

        user_content = f"""{instruction_message}

You need to conduct an interview to gather all the information from the other person needed to fill out this form.

{form_context}

Start the interview by introducing yourself and asking your first question."""

        if single_field_mode:
            user_content += """

IMPORTANT: You must ask only ONE question at a time, focusing on a single field. Do NOT ask multiple questions or combine questions about different fields in a single message. Wait for the response before asking about the next field."""

        self._messages.extend(
            [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_content},
            ]
        )

    def _get_unfilled_fields(self, submission: dict) -> list[str]:
        """Return field names that are missing or still at their default value."""
        defaults = {name: info.default for name, info in self._form_class.model_fields.items()}
        unfilled = []
        for field_name, default_value in defaults.items():
            value = submission.get(field_name)
            if value is None or value == "" or value == default_value:
                unfilled.append(field_name)
        return unfilled

    # ------------------------------------------------------------------ #
    # Message history helpers
    # ------------------------------------------------------------------ #

    def add_tool_result(self, result: str):
        """Add a tool result as a user message (conversation-like format)."""
        self._messages.append({"role": "user", "content": f"Tool result:\n{result}"})

    def add_new_message(self, from_agent: str, message: str):
        """Add a message from the other agent."""
        self._messages.append({"role": "user", "content": f"Message from {from_agent}:\n{message}"})

    @property
    def messages(self) -> list[SageMessage]:
        """Return the current message history."""
        return self._messages
