"""Buyer agent for marketplace negotiation."""

from __future__ import annotations

from srbench_llm import SRBenchModelClient

from ....shared.agent import BaseAgent
from ..environment.actions import MARKETPLACE_TOOLS, EndConversation
from .marketplace_base import build_initial_messages


class BuyerAgent(BaseAgent):
    """Buyer agent (the role under evaluation). Satisfies :class:`Agent`."""

    def __init__(
        self,
        *,
        model: str,
        model_client: SRBenchModelClient,
        instruction_message: str,
        explicit_cot: bool = False,
        system_prompt: str | None = None,
        malicious_prompt: str | None = None,
        max_actions: int = 50,
    ) -> None:
        super().__init__(
            model=model,
            model_client=model_client,
            tools=list(MARKETPLACE_TOOLS) + [EndConversation],
            explicit_cot=explicit_cot,
            prompt_label="mkt_buyer",
            max_actions=max_actions,
        )
        self._messages.extend(
            build_initial_messages(
                system_prompt=system_prompt,
                instruction_message=instruction_message,
                malicious_prompt=malicious_prompt,
            )
        )
