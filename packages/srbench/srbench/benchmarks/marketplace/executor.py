"""Canonical execution pattern for marketplace benchmark.

The executor takes a task and produces a MarketplaceExecutionResult -- the raw
record of what happened, with no judgement.

    execute_task(task, ...) -> MarketplaceExecutionResult

Each agent owns its run loop and touches the environment only through tools:
``AgentResources.execute`` is the single execution path for every action, and
the executor hands it directly to ``agent.run``, forces the seller's opening
offer, then races both loops against the environment's end signal. ``Wait``
blocks until the counterpart acts and returns the new messages and offers, so
no scheduler injects turns. The forced opening offer reaches the buyer the
same way, from its first ``Wait``.

The buyer (assistant) side supports "bring your own agent". Pass
``buyer_agent_factory`` (any callable returning a ``BaseAssistantAgent``) to
replace the built-in ``BuyerAgent``.

The execution result carries:
    - task: MarketplaceTask (with .hash for checkpoint dedup)
    - outcome: FinalOutcome (deal_reached, deal_price, etc.)
    - messages, offers, action_trace: full negotiation history
    - Execution health (invalid_actions, error)
"""

from __future__ import annotations

import logging
import traceback
from typing import Callable

from srbench_llm import SRBenchModelClient

from ...shared.agent import BaseAssistantAgent
from ...shared.logging import BenchmarkLogger, VerboseLogger
from ...shared.signals import run_agents_until_end
from .agents import BuyerAgent, SellerAgent
from .environment import AgentResources, MakeOffer, MarketplaceEnvironment
from .environment.actions import MARKETPLACE_TOOLS, EndConversation
from .types import MarketplaceExecutionResult, MarketplaceTask

logger = logging.getLogger(__name__)

# The environment owns each role's tool space and hands it to ``agent.run``.
# Only the buyer may end the conversation.
BUYER_TOOL_SPACE = [t.get_openai_function_tool_param() for t in MARKETPLACE_TOOLS] + [
    EndConversation.get_openai_function_tool_param()
]
SELLER_TOOL_SPACE = [t.get_openai_function_tool_param() for t in MARKETPLACE_TOOLS]


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
    buyer_model: str | None,
    seller_model: str,
    buyer_client: SRBenchModelClient,
    seller_client: SRBenchModelClient,
    max_actions_per_agent: int = 50,
    buyer_explicit_cot: bool = False,
    seller_explicit_cot: bool = False,
    system_prompt: str | None = None,
    benchmark_logger: BenchmarkLogger | None = None,
    buyer_agent_factory: Callable[..., BaseAssistantAgent] | None = None,
) -> MarketplaceExecutionResult:
    """Execute a single marketplace negotiation task.

    This is the canonical entry point for task execution. It sets up the
    environment, creates buyer/seller agents, and runs their loops
    concurrently until a deal is reached and an agent ends the conversation,
    a budget runs out, or the conversation stalls.

    Args:
        task: The marketplace task to execute, with .hash for checkpointing.
        buyer_model: Model name for the built-in buyer agent. May be ``None``
            when ``buyer_agent_factory`` is provided.
        seller_model: Model name for the seller agent.
        buyer_client: SRBenchModelClient for the buyer agent.
        seller_client: SRBenchModelClient for the seller agent.
        max_actions_per_agent: Maximum tool calls per agent for the whole conversation.
        buyer_explicit_cot: Whether to enable explicit chain-of-thought for buyer.
        seller_explicit_cot: Whether to enable explicit chain-of-thought for seller.
        system_prompt: Optional resolved system prompt for the buyer (assistant).
        buyer_agent_factory: Optional factory for a user-provided buyer agent
            (bring your own agent). Called with keyword arguments
            ``instruction_message`` (the buyer's task instructions) and
            ``max_actions``. When provided, the built-in ``BuyerAgent`` and
            its LLM configuration (``buyer_model``, ``system_prompt``,
            ``buyer_explicit_cot``) are not used.

    Returns:
        MarketplaceExecutionResult with all execution state.
    """
    env = MarketplaceEnvironment()
    signals = env.signals
    buyer_resources = env.create_agent_resources("buyer")
    seller_resources = env.create_agent_resources("seller")
    buyer_agent: BaseAssistantAgent
    if buyer_agent_factory is not None:
        buyer_agent = buyer_agent_factory(
            instruction_message=task.buyer.instruction_message,
            max_actions=max_actions_per_agent,
        )
    else:
        if buyer_model is None:
            raise ValueError("buyer_model is required when no buyer_agent_factory is provided")
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
            # Force the seller's opening offer at the listed price. The offer
            # stays unread and the buyer's wake signal stays set, so the
            # buyer's first Wait returns immediately with it. Delivery
            # happens through tools, not by pushing context into the agent.
            await _force_initial_seller_offer(seller_agent, seller_resources, task)

        await run_agents_until_end(
            [
                buyer_agent.run(buyer_resources.execute, BUYER_TOOL_SPACE),
                seller_agent.run(seller_resources.execute, SELLER_TOOL_SPACE),
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
        # Transcripts are debugging artifacts, captured only when the agent
        # exposes them. Evaluation reads the environment's own records.
        buyer_context=list(getattr(buyer_agent, "messages", [])),
        seller_context=seller_agent.messages,
        error=error,
    )
