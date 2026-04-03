"""Assistant agent for interactive form-filling interviews.

Inherits from BaseAgent, which provides tool registry, message history,
response-ID tracking, generate_tool_call(), and add_tool_call_result().

The caller (interactive.py) handles the tool dispatch loop: file-system
tools (SearchFiles, ReadFile) are executed externally via BM25, and the
agent is called again until it produces a conversation tool.
"""

from openai.types.chat.chat_completion_message_tool_call import (
    ChatCompletionMessageToolCall,
    Function,
)
from sage_llm import SageChatCompletionMessage, SageMessage, SageModelClient

from ....shared.agent import BaseAgent
from ..environment.actions import (
    ALL_TOOLS,
    GETMESSAGES_TOOL_NAME,
    ReadFile,
    SearchFiles,
)
from ..prompts import (
    INTERACTIVE_INSTRUCTION,
    construct_system_prompt,
    format_artifacts_as_context,
)


class AssistantAgent(BaseAgent):
    """Agent that answers questions on behalf of a person.

    Inherits tool registry, message history, response-ID tracking,
    ``generate_tool_call()``, and ``add_tool_call_result()`` from
    :class:`BaseAgent`.  No method overrides are needed -- temperature
    and ``tool_choice="required"`` are passed via the base constructor.

    All tool dispatch (including file-system tools) is handled by the
    caller in ``interactive.py``.
    """

    def __init__(
        self,
        client: SageModelClient,
        model: str,
        persona,
        artifacts: list,
        prompt_type: str = "base",
        temperature: float | None = None,
        explicit_cot: bool = False,
    ):
        """Initialize the assistant agent.

        Args:
            client: Model client for LLM calls
            model: Model name to use
            persona: PersonaData object with client information
            artifacts: List of ArtifactData objects
            prompt_type: Privacy level ("none", "simple", "strong", "ci")
            temperature: Sampling temperature for generation
            explicit_cot: If True, generate chain-of-thought reasoning before each tool call
        """
        super().__init__(
            model=model,
            model_client=client,
            tools=list(ALL_TOOLS),
            temperature=temperature,
            tool_choice="required",
            explicit_cot=explicit_cot,
        )

        # Build initial messages
        system_prompt = construct_system_prompt(persona, prompt_type)

        self._messages.append({"role": "system", "content": system_prompt})

        # Inject each artifact as a SearchFiles -> ReadFile tool call sequence
        for i, artifact in enumerate(artifacts):
            artifact_type = artifact.artifact_type
            metadata = artifact.metadata or {}
            label = metadata.get("subject") or metadata.get("title") or f"{artifact_type} {i + 1}"
            file_id = f"{artifact_type}_{i + 1}"

            # SearchFiles call returning a snippet
            snippet = (
                artifact.content[:80] + "..." if len(artifact.content) > 80 else artifact.content
            )
            search_result = (
                f'{{"id": "{file_id}", "type": "{artifact_type}", "snippet": "{snippet}"}}'
            )
            self.add_forced_action(SearchFiles(query=label), f"[{search_result}]")

            # ReadFile call returning full content
            read_result = format_artifacts_as_context([artifact])
            self.add_forced_action(ReadFile(id=file_id), read_result)

        self._messages.append({"role": "user", "content": INTERACTIVE_INSTRUCTION})

    # ------------------------------------------------------------------ #
    # Domain-specific message helpers
    # ------------------------------------------------------------------ #

    def add_new_messages(self, from_agent: str, message: str) -> None:
        """Inject new messages by simulating a GetMessages tool call and response."""
        tool_call_id = str(len(self._messages))
        self._messages.append(
            SageChatCompletionMessage(
                role="assistant",
                tool_calls=[
                    ChatCompletionMessageToolCall(
                        id=tool_call_id,
                        type="function",
                        function=Function(name=GETMESSAGES_TOOL_NAME, arguments="{}"),
                    )
                ],
            )
        )
        content = f"Message from {from_agent}:\n{message}"
        self._messages.append(
            {
                "role": "tool",
                "tool_call_id": tool_call_id,
                "content": content,
            }
        )
