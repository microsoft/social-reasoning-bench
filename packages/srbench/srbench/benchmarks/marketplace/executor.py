"""Canonical execution pattern for marketplace benchmark.

The executor takes a task and produces a MarketplaceExecutionResult -- the raw
record of what happened, with no judgement.

    execute_task(task, ...) -> MarketplaceExecutionResult

Each agent owns its run loop and touches the environment only through tools:
``AgentResources.execute`` is the single execution path for every action, and
the executor hands it directly to ``agent.run``, forces the seller's opening
offer, then races both loops against the environment's end signal. ``Wait``
blocks until the counterpart acts and returns the new messages and offers, so
no scheduler injects turns.

The execution result carries:
    - task: MarketplaceTask (with .hash for checkpoint dedup)
    - outcome: FinalOutcome (deal_reached, deal_price, etc.)
    - messages, offers, action_trace: full negotiation history
    - Execution health (invalid_actions, error)
"""

from __future__ import annotations

import logging
import traceback

from srbench_llm import SRBenchModelClient

from ...shared.logging import BenchmarkLogger, VerboseLogger
from ...shared.signals import run_agents_until_end
from .agents import BuyerAgent, SellerAgent
from .environment import AgentResources, MakeOffer, MarketplaceEnvironment
from .types import MarketplaceExecutionResult, MarketplaceTask

logger = logging.getLogger(__name__)


async def _force_initial_seller_offer(
    seller_agent: SellerAgent,
    seller_resources: AgentResources,
    task: MarketplaceTask,
) -> None:
    """Force the seller to make an initial offer at the listed price.

    Lets the agent generate a natural opening message, then creates a
    MakeOffer action with the predetermined listed_price from the task,
    executes it against the environment, and records the forced action on
    the seller's transcript.

    Args:
        seller_agent: The seller agent to record the forced action on.
        seller_resources: The seller's environment resources.
        task: The marketplace task with product.listed_price set.
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
    result = await seller_resources.execute(offer_action)
    seller_agent.add_forced_action(offer_action, result)


async def execute_task(
    task: MarketplaceTask,
    *,
    buyer_model: str,
    seller_model: str,
    buyer_client: SRBenchModelClient,
    seller_client: SRBenchModelClient,
    max_actions_per_agent: int = 50,
    buyer_explicit_cot: bool = False,
    seller_explicit_cot: bool = False,
    system_prompt: str | None = None,
    benchmark_logger: BenchmarkLogger | None = None,
) -> MarketplaceExecutionResult:
    """Execute a single marketplace negotiation task.

    This is the canonical entry point for task execution. It sets up the
    environment, creates buyer/seller agents, and runs their loops
    concurrently until a deal is reached and an agent ends the conversation,
    a budget runs out, or the conversation stalls.

    Args:
        task: The marketplace task to execute, with .hash for checkpointing.
        buyer_model: Model name for the buyer agent.
        seller_model: Model name for the seller agent.
        buyer_client: SRBenchModelClient for the buyer agent.
        seller_client: SRBenchModelClient for the seller agent.
        max_actions_per_agent: Maximum tool calls per agent for the whole conversation.
        buyer_explicit_cot: Whether to enable explicit chain-of-thought for buyer.
        seller_explicit_cot: Whether to enable explicit chain-of-thought for seller.
        system_prompt: Optional resolved system prompt for the buyer (assistant).

    Returns:
        MarketplaceExecutionResult with all execution state.
    """
    env = MarketplaceEnvironment()
    signals = env.signals
    buyer_resources = env.create_agent_resources("buyer")
    seller_resources = env.create_agent_resources("seller")
    buyer_agent = BuyerAgent(
        model=buyer_model,
        model_client=buyer_client,
        instruction_message=task.buyer.instruction_message,
        explicit_cot=buyer_explicit_cot,
        system_prompt=system_prompt,
        max_actions=max_actions_per_agent,
    )
    seller_agent = SellerAgent(
        model=seller_model,
        model_client=seller_client,
        instruction_message=task.seller.instruction_message,
        explicit_cot=seller_explicit_cot,
        malicious_prompt=task.seller.malicious_prompt,
        max_actions=max_actions_per_agent,
    )

    if benchmark_logger is None:
        benchmark_logger = VerboseLogger(logger)

    error: str | None = None
    try:
        if task.product.listed_price is not None:
            # Force the seller's opening offer at the listed price, surface it
            # in the buyer's context before its loop starts (exactly what the
            # turn-based executor did at the start of each turn), and clear
            # the wake signal the offer produced.
            await _force_initial_seller_offer(seller_agent, seller_resources, task)
            buyer_agent.add_new_messages(buyer_resources.get_unread_updates())
            signals.clear("buyer")

        await run_agents_until_end(
            [
                buyer_agent.run(buyer_resources.execute),
                seller_agent.run(seller_resources.execute),
            ],
            signals=signals,
        )
    except Exception as ex:
        logger.exception("Error during execution.")
        benchmark_logger.error("Task %d - Fatal error: %s\n%s", task.id, ex, traceback.format_exc())
        error = str(ex)
        signals.end(reason="error")

    if not env.state.outcome.deal_reached and env.state.outcome.end_reason is None:
        # "max_rounds" is the legacy ended_by value for any harness-stopped
        # run; the free-text end_reason carries the actual cause.
        env.state.outcome.ended_by = "max_rounds"
        env.state.outcome.end_reason = (
            f"Conversation ended without agreement ({signals.end_reason})."
        )

    invalid_actions = sum(1 for trace in env.state.action_trace if not trace.valid)

    return MarketplaceExecutionResult(
        task=task,
        outcome=env.state.outcome,
        messages=env.state.messages,
        offers=env.state.offers,
        action_trace=env.state.action_trace,
        invalid_actions=invalid_actions,
        buyer_context=buyer_agent.messages,
        seller_context=seller_agent.messages,
        error=error,
    )
