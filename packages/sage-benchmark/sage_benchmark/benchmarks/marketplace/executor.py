"""Canonical execution pattern for marketplace benchmark.

The executor takes a task and produces a MarketplaceExecutionResult -- the raw
record of what happened, with no judgement.

    execute_task(task, ...) -> MarketplaceExecutionResult

The execution result carries:
    - task: MarketplaceTask (with .hash for checkpoint dedup)
    - outcome: FinalOutcome (deal_reached, deal_price, etc.)
    - messages, offers, action_trace: full negotiation history
    - Execution health (invalid_actions, error)
"""

from __future__ import annotations

import traceback

from sage_llm import SageModelClient

from ...shared.errors import is_fatal_error
from ...shared.logging import BenchmarkLogger, VerboseLogger
from .agents import BuyerAgent, MarketplaceAgent, SellerAgent
from .environment import AgentResources, EndConversation, MarketplaceEnvironment, Wait
from .environment.resources import execute_with_trace
from .types import ActionTrace, MarketplaceExecutionResult, MarketplaceTask


async def _run_agent_turn(
    agent: MarketplaceAgent,
    resources: AgentResources,
    max_steps: int,
    action_trace: list[ActionTrace | dict],
    benchmark_logger: BenchmarkLogger | None = None,
) -> tuple[int, bool]:
    """Run one agent turn until Wait, EndConversation, or max_steps."""
    invalid_actions = 0
    for _ in range(max_steps):
        try:
            action = await agent.generate_tool_call()
        except Exception as e:
            if is_fatal_error(e):
                raise
            action_trace.append(
                {
                    "round": resources.state.current_round,
                    "actor": resources.role,
                    "action_type": "GENERATION_ERROR",
                    "payload": {},
                    "result": traceback.format_exc(),
                    "valid": False,
                }
            )
            return 1, True

        trace, ok = execute_with_trace(resources, action)
        action_trace.append(trace)
        if not ok:
            invalid_actions += 1
        agent.add_tool_call_result(trace.result)

        if isinstance(action, Wait):
            return invalid_actions, False
        if isinstance(action, EndConversation) and ok:
            return invalid_actions, True
        if resources.state.outcome.deal_reached:
            return invalid_actions, True

    return invalid_actions, False


async def execute_task(
    task: MarketplaceTask,
    *,
    buyer_model: str,
    seller_model: str,
    buyer_client: SageModelClient,
    seller_client: SageModelClient,
    max_rounds: int = 20,
    max_steps_per_turn: int = 3,
    explicit_cot: bool = False,
    benchmark_logger: BenchmarkLogger | None = None,
) -> MarketplaceExecutionResult:
    """Execute a single marketplace negotiation task.

    This is the canonical entry point for task execution. It sets up the
    environment, creates buyer/seller agents, and runs the negotiation loop
    until a deal is reached, an agent ends the conversation, or max rounds
    are exhausted.

    Privacy system prompts are read from ``task.buyer.privacy_level`` and
    ``task.seller.privacy_level`` (set during task expansion in load_tasks).

    Args:
        task: The marketplace task to execute, with .hash for checkpointing.
        buyer_model: Model name for the buyer agent.
        seller_model: Model name for the seller agent.
        buyer_client: SageModelClient for the buyer agent.
        seller_client: SageModelClient for the seller agent.
        max_rounds: Maximum conversation rounds.
        max_steps_per_turn: Maximum tool calls per agent turn.
        explicit_cot: Whether to enable explicit chain-of-thought.

    Returns:
        MarketplaceExecutionResult with all execution state.
    """
    from .prompts import get_system_prompt

    env = MarketplaceEnvironment()
    buyer_resources = env.create_agent_resources("buyer")
    seller_resources = env.create_agent_resources("seller")
    buyer_agent = BuyerAgent(
        model=buyer_model,
        model_client=buyer_client,
        instruction_message=task.buyer.instruction_message,
        explicit_cot=explicit_cot,
        system_prompt=get_system_prompt(task.buyer.privacy_level)
        if task.buyer.privacy_level
        else None,
    )
    seller_agent = SellerAgent(
        model=seller_model,
        model_client=seller_client,
        instruction_message=task.seller.instruction_message,
        explicit_cot=explicit_cot,
        system_prompt=get_system_prompt(task.seller.privacy_level)
        if task.seller.privacy_level
        else None,
    )

    if benchmark_logger is None:
        import logging as _logging

        benchmark_logger = VerboseLogger(_logging.getLogger(__name__))

    action_trace = []
    invalid_actions = 0

    for round_num in range(1, max_rounds + 1):
        env.state.current_round = round_num
        benchmark_logger.info("Task %d - Round %d", task.id, round_num)
        for resources, agent in [(buyer_resources, buyer_agent), (seller_resources, seller_agent)]:
            if env.state.outcome.deal_reached or env.state.outcome.end_reason is not None:
                break

            agent.add_turn_marker(current_round=round_num, max_rounds=max_rounds)
            unread_updates = resources.get_unread_updates()
            agent.add_new_messages(unread_updates)
            turn_invalid_actions, agent_ended = await _run_agent_turn(
                agent, resources, max_steps_per_turn, action_trace, benchmark_logger
            )
            invalid_actions += turn_invalid_actions

            # If generation failed, _run_agent_turn returns ended=True but environment isn't ended yet.
            if (
                agent_ended
                and not env.state.outcome.deal_reached
                and env.state.outcome.end_reason is None
            ):
                env.state.outcome.ended_by = resources.role
                env.state.outcome.end_reason = "Agent generation error."
                break

        if env.state.outcome.deal_reached or env.state.outcome.end_reason is not None:
            break

    if not env.state.outcome.deal_reached and env.state.outcome.end_reason is None:
        env.state.outcome.ended_by = "max_rounds"
        env.state.outcome.end_reason = "Reached max rounds without agreement."

    return MarketplaceExecutionResult(
        task=task,
        outcome=env.state.outcome,
        messages=env.state.messages,
        offers=env.state.offers,
        action_trace=action_trace,
        invalid_actions=invalid_actions,
        buyer_context=buyer_agent.messages,
        seller_context=seller_agent.messages,
    )
