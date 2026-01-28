"""Assistant agent for iTIP-style calendar scheduling."""

from sage_llm import ModelClient

from ..environment.actions import CALENDAR_TOOLS, EndConversation
from ..types import Artifact, CalendarAssistant, EmailThread, Note
from .calendar_base import CalendarAgent

SYSTEM_PROMPT = """
You are an autonomous calendar scheduling assistant. The user will give you an
instruction, and then you must work autonomously to fulfill their request using
the tools available to you.
""".strip()


def format_artifacts_for_context(artifacts: list[Artifact]) -> str:
    """Format artifacts as a natural context message for the assistant."""
    sections = [
        "Here are some relevant items from your inbox and notes that may help with today's scheduling:\n"
    ]

    for artifact in artifacts:
        if isinstance(artifact, EmailThread):
            sections.append("--- Email Thread ---")
            sections.append(f"Subject: {artifact.subject}")
            sections.append(f"Date: {artifact.date}")
            sections.append("")
            for msg in artifact.messages:
                sections.append(f"From: {msg.sender}")
                sections.append(msg.content)
                sections.append("")
        elif isinstance(artifact, Note):
            sections.append(f"--- Note: {artifact.title} ---")
            sections.append(f"Date: {artifact.date}")
            sections.append(artifact.content)
            sections.append("")

    return "\n".join(sections)


class CalendarAssistantAgent(CalendarAgent):
    """Assistant agent that responds to meeting requests."""

    def __init__(
        self,
        model: str,
        model_client: ModelClient,
        assistant: CalendarAssistant,
        allowed_contacts: list[str],
        artifacts: list[Artifact] | None = None,
    ):
        super().__init__(
            model=model,
            model_client=model_client,
            allowed_contacts=allowed_contacts,
            tools=CALENDAR_TOOLS + [EndConversation],
        )

        system_message = "\n".join([SYSTEM_PROMPT, "", assistant.system_message])
        self._messages.append({"role": "system", "content": system_message})

        # Inject artifacts as context before the instruction message
        if artifacts:
            artifact_content = format_artifacts_for_context(artifacts)
            self._messages.append({"role": "user", "content": artifact_content})

        self._messages.append({"role": "user", "content": assistant.instruction_message})
