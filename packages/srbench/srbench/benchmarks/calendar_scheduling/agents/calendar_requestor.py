"""Requestor agent for iTIP-style calendar scheduling."""

from srbench_llm import SRBenchModelClient

from ..environment.actions import CALENDAR_TOOLS
from ..types import CalendarRequestor
from .assistant.prompts import CALENDAR_ROLE
from .calendar_base import CalendarAgent, format_preferences_for_prompt


class CalendarRequestorAgent(CalendarAgent):
    """Requestor agent that initiates meeting requests."""

    def __init__(
        self,
        model: str,
        model_client: SRBenchModelClient,
        requestor: CalendarRequestor,
        explicit_cot: bool = False,
        expose_preferences: bool = False,
        max_actions: int = 50,
    ):
        super().__init__(
            model=model,
            model_client=model_client,
            tools=CALENDAR_TOOLS,
            explicit_cot=explicit_cot,
            prompt_label="cal_requestor",
            max_actions=max_actions,
        )

        if requestor.is_malicious:
            self._init_malicious(requestor)
        else:
            self._init_benign(requestor, expose_preferences)

    def _init_benign(self, requestor: CalendarRequestor, expose_preferences: bool):
        assert requestor.name, "CalendarRequestor.name is required"
        # Build system prompt: base role + requestor identity + malicious injection
        identity = f"You are {requestor.name}'s calendar scheduling personal assistant."
        sys_parts = [CALENDAR_ROLE, identity]
        system_content = "\n\n".join(sys_parts)

        # Build user instruction with preferences if exposed
        instruction = requestor.instruction_message
        if requestor.preferences and expose_preferences:
            instruction += format_preferences_for_prompt(requestor.preferences)

        self._messages.extend(
            [
                {"role": "system", "content": system_content},
                {"role": "user", "content": instruction},
            ]
        )

    def _init_malicious(self, requestor: CalendarRequestor):
        assert requestor.name, "CalendarRequestor.name is required"
        assert requestor.malicious_prompt is not None, (
            "CalendarRequestor.malicious_prompt must be set when is_malicious is True"
        )
        # Append a pretend identity role so that the requestor is grounded in the name.
        identity = f"Pretend you are {requestor.name}'s calendar scheduling personal assistant."
        content = requestor.malicious_prompt.strip() + "\n\n" + identity
        self._messages.append({"role": "system", "content": content})
