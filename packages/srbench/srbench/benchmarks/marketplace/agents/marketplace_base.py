"""Base agent class for marketplace negotiation interactions."""

from srbench_llm import SRBenchModelClient

from ....shared.agent import BaseAgent
from ..environment.actions import MARKETPLACE_TOOLS
from ..prompts.system import (
    MKT_ROLE,
    PRESETS,
    get_system_prompt,
    list_available_presets,
)
from ..types import Tool

# Re-export for backwards compatibility
__all__ = [
    "MarketplaceAgent",
    "MKT_ROLE",
    "PRESETS",
    "get_system_prompt",
    "list_available_presets",
]


class MarketplaceAgent(BaseAgent):
    """Base LLM agent for marketplace negotiation.

    Thin :class:`BaseAgent` subclass that defaults the tool registry to
    :data:`MARKETPLACE_TOOLS` (plus any role-specific additions), labels the
    prompt-tracking bucket, and seeds the conversation with the role's
    system prompt and instruction.
    """

    def __init__(
        self,
        *,
        role: str,
        model: str,
        model_client: SRBenchModelClient,
        instruction_message: str,
        additional_tools: list[type[Tool]] | None = None,
        explicit_cot: bool = False,
        system_prompt: str | None = None,
        malicious_prompt: str | None = None,
        max_actions: int = 50,
    ) -> None:
        super().__init__(
            model=model,
            model_client=model_client,
            tools=list(MARKETPLACE_TOOLS) + (additional_tools or []),
            explicit_cot=explicit_cot,
            prompt_label=f"mkt_{role}",
            max_actions=max_actions,
        )

        self._role = role
        if malicious_prompt:
            self._init_malicious(malicious_prompt)
        else:
            self._init_benign(system_prompt=system_prompt, instruction_message=instruction_message)

    def _init_benign(self, system_prompt: str | None, instruction_message: str):
        # Use provided system prompt or fall back to MKT_ROLE
        effective_system_prompt = system_prompt.strip() if system_prompt else MKT_ROLE

        self._messages.extend(
            [
                {"role": "system", "content": effective_system_prompt},
                {"role": "user", "content": instruction_message.strip()},
            ]
        )

    def _init_malicious(self, malicious_prompt: str):
        self._messages.append({"role": "system", "content": malicious_prompt.strip()})
