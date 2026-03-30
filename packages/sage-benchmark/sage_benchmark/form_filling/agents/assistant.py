"""Assistant agent for interactive form-filling interviews.

Inherits from BaseAgent, which provides tool registry, message history,
response-ID tracking, generate_tool_call(), and add_tool_call_result().

The caller (interactive.py) handles the tool dispatch loop: file-system
tools (SearchFiles, ReadFile) are executed externally via BM25, and the
agent is called again until it produces a conversation tool.
"""

from openai.types.chat import (
    ChatCompletionAssistantMessageParam,
    ChatCompletionMessageToolCallParam,
    ChatCompletionToolMessageParam,
)
from sage_llm import ModelClient

from sage_benchmark.form_filling.environment.actions import ALL_TOOLS, GETMESSAGES_TOOL_NAME
from sage_benchmark.form_filling.prompts import (
    INTERACTIVE_INSTRUCTION,
    construct_interactive_system_prompt,
    format_artifacts_as_context,
)
from sage_benchmark.shared.agent import BaseAgent


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
        client: ModelClient,
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
        system_prompt = construct_interactive_system_prompt(persona, prompt_type)
        artifacts_context = format_artifacts_as_context(artifacts)

        self._messages.extend(
            [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": artifacts_context},
                {"role": "user", "content": INTERACTIVE_INSTRUCTION},
            ]
        )

    # ------------------------------------------------------------------ #
    # Domain-specific message helpers
    # ------------------------------------------------------------------ #

    def add_new_messages(self, from_agent: str, message: str) -> None:
        """Inject new messages by simulating a GetMessages tool call and response."""
        tool_call_id = str(len(self._messages))
        self._messages.append(
            ChatCompletionAssistantMessageParam(
                role="assistant",
                tool_calls=[
                    ChatCompletionMessageToolCallParam(
                        id=tool_call_id,
                        type="function",
                        function={"name": GETMESSAGES_TOOL_NAME, "arguments": "{}"},
                    )
                ],
            )
        )
        content = f"Message from {from_agent}:\n{message}"
        self._messages.append(
            ChatCompletionToolMessageParam(
                role="tool",
                tool_call_id=tool_call_id,
                content=content,
            )
        )
