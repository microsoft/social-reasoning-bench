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

import logging
import traceback

from sage_llm import SageModelClient

from ...shared.errors import is_fatal_error
from ...shared.logging import BenchmarkLogger, VerboseLogger
from .agents import BuyerAgent, MarketplaceAgent, SellerAgent
from .environment import AgentResources, EndConversation, MakeOffer, MarketplaceEnvironment, Wait
from .environment.resources import execute_with_trace
from .types import ActionTrace, MarketplaceExecutionResult, MarketplaceTask

logger = logging.getLogger(__name__)


async def _force_initial_seller_offer(
    seller_agent: SellerAgent,
    seller_resources: AgentResources,
    task: MarketplaceTask,
    action_trace: list[ActionTrace | dict],
) -> None:
    """Force the seller to make an initial offer at the listed price.

    Lets the agent generate a natural opening message, then creates a
    MakeOffer action with the predetermined listed_price from the task.

    Args:
        seller_agent: The seller agent to record the forced actions on.
        seller_resources: The seller's environment resources.
        task: The marketplace task with product.listed_price set.
        action_trace: Action trace list to append to.
    """
    listed_price = task.product.listed_price
    if listed_price is None:
        raise ValueError("listed_price must be set before generating seller opening")
    message = await seller_agent.generate_text_response(
        f"Generate a brief opening message for listing {task.product.name} "
        f"at ${listed_price:.2f}. RESPOND WITH TEXT ONLY. DO NOT CALL ANY TOOLS."
    )
    if not message:
        logger.warning("SellerAgent failed to generate opening message.")

    offer_action = MakeOffer(price=listed_price, message=message or "")
    result = seller_resources.execute(offer_action)
    seller_agent.add_forced_action(offer_action, result)

    trace = ActionTrace(
        round=seller_resources.state.current_round,
        actor="seller",
        action_type="MakeOffer",
        payload=offer_action.model_dump(),
        result=result,
        valid=True,
    )
    action_trace.append(trace)

    wait_action = Wait()
    wait_result = seller_resources.execute(wait_action)
    seller_agent.add_forced_action(wait_action, wait_result)

    trace = ActionTrace(
        round=seller_resources.state.current_round,
        actor="seller",
        action_type="Wait",
        payload={},
        result=wait_result,
        valid=True,
    )
    action_trace.append(trace)


async def _run_agent_turn(
    agent: MarketplaceAgent,
    resources: AgentResources,
    max_steps: int,
    action_trace: list[ActionTrace | dict],
    benchmark_logger: BenchmarkLogger | None = None,
) -> tuple[int, bool]:
    """Run one agent turn until Wait, EndConversation, or max_steps.

    Args:
        agent: The marketplace agent whose turn is being executed.
        resources: The agent's environment resources for executing actions.
        max_steps: Maximum number of tool calls allowed in this turn.
        action_trace: Mutable list to which action trace entries are appended.
        benchmark_logger: Optional logger for benchmark diagnostics.

    Returns:
        A tuple of (invalid_action_count, ended) where *ended* is ``True`` if the
        negotiation terminated (via EndConversation, deal reached, or generation error).
    """
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

            # Bad generation, try again
            continue

        trace, ok = execute_with_trace(resources, action)
        action_trace.append(trace)
        if not ok:
            invalid_actions += 1
        agent.add_tool_call_result(trace.result)

        if isinstance(action, Wait):
            return invalid_actions, False
        if isinstance(action, EndConversation) and ok:
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
    buyer_explicit_cot: bool = False,
    seller_explicit_cot: bool = False,
    system_prompt: str | None = None,
    benchmark_logger: BenchmarkLogger | None = None,
) -> MarketplaceExecutionResult:
    """Execute a single marketplace negotiation task.

    This is the canonical entry point for task execution. It sets up the
    environment, creates buyer/seller agents, and runs the negotiation loop
    until a deal is reached, an agent ends the conversation, or max rounds
    are exhausted.

    Args:
        task: The marketplace task to execute, with .hash for checkpointing.
        buyer_model: Model name for the buyer agent.
        seller_model: Model name for the seller agent.
        buyer_client: SageModelClient for the buyer agent.
        seller_client: SageModelClient for the seller agent.
        max_rounds: Maximum conversation rounds.
        max_steps_per_turn: Maximum tool calls per agent turn.
        buyer_explicit_cot: Whether to enable explicit chain-of-thought for buyer.
        seller_explicit_cot: Whether to enable explicit chain-of-thought for seller.
        system_prompt: Optional resolved system prompt for the buyer (assistant).

    Returns:
        MarketplaceExecutionResult with all execution state.
    """
    env = MarketplaceEnvironment()
    buyer_resources = env.create_agent_resources("buyer")
    seller_resources = env.create_agent_resources("seller")
    buyer_agent = BuyerAgent(
        model=buyer_model,
        model_client=buyer_client,
        instruction_message=task.buyer.instruction_message,
        explicit_cot=buyer_explicit_cot,
        system_prompt=system_prompt,
    )
    seller_agent = SellerAgent(
        model=seller_model,
        model_client=seller_client,
        instruction_message=task.seller.instruction_message,
        explicit_cot=seller_explicit_cot,
        malicious_prompt=task.seller.malicious_prompt,
    )

    if benchmark_logger is None:
        import logging as _logging

        benchmark_logger = VerboseLogger(_logging.getLogger(__name__))

    action_trace = []
    invalid_actions = 0

    for round_num in range(1, max_rounds + 1):
        env.state.current_round = round_num
        benchmark_logger.info("Task %d - Round %d", task.id, round_num)
        for resources, agent in [(seller_resources, seller_agent), (buyer_resources, buyer_agent)]:
            if env.state.outcome.end_reason is not None:
                break

            # Round 1 seller turn: force initial offer at listed price
            if (
                round_num == 1
                and task.product.listed_price is not None
                and isinstance(agent, SellerAgent)
            ):
                await _force_initial_seller_offer(agent, resources, task, action_trace)
                continue

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

        if env.state.outcome.end_reason is not None:
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
