"""Canonical execution pattern for marketplace benchmark (agent-driven loop).

The executor sets up env + resources, runs the seller's forced opening
offer (the only deterministic harness-driven action), then spawns both
agents' ``run`` loops concurrently and waits for any of:
  - either agent's ``run`` to return,
  - ``env.end_event`` to fire (``EndConversation`` was executed,
    triggering ``MarketplaceEnvironment.mark_ended``),
  - the wall-clock timeout to elapse,
  - the externally-supplied ``cancel_event`` to fire.
"""

from __future__ import annotations

import asyncio
import logging
import traceback

from srbench_llm import SRBenchModelClient

from ...shared.logging import BenchmarkLogger, VerboseLogger
from .agents.buyer import BuyerAgent
from .agents.seller import SellerAgent
from .environment import AgentResources, MakeOffer, MarketplaceEnvironment
from .types import MarketplaceExecutionResult, MarketplaceTask

logger = logging.getLogger(__name__)


async def _force_initial_seller_offer(
    seller_agent: SellerAgent,
    seller_resources: AgentResources,
    task: MarketplaceTask,
) -> None:
    """Drive the deterministic opening MakeOffer at listed_price from the seller.

    The seller agent composes the natural-language body of the message; the
    harness wraps it in a ``MakeOffer(price=listed_price)`` action, executes
    it against the env (which records an ActionTrace + sets buyer's
    ``new_content_event``), and records the forced action on the seller's
    transcript.
    """
    listed_price = task.product.listed_price
    if listed_price is None:
        raise ValueError("listed_price must be set before generating seller opening")

    message = await seller_agent.generate_text(
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
    buyer_explicit_cot: bool = False,
    seller_explicit_cot: bool = False,
    system_prompt: str | None = None,
    max_actions_per_agent: int = 50,
    max_wall_time_seconds: float | None = None,
    cancel_event: asyncio.Event | None = None,
    benchmark_logger: BenchmarkLogger | None = None,
) -> MarketplaceExecutionResult:
    """Execute a single marketplace negotiation task."""
    env = MarketplaceEnvironment()
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
            await _force_initial_seller_offer(seller_agent, seller_resources, task)

        timeout_ctx = (
            asyncio.timeout(max_wall_time_seconds)
            if max_wall_time_seconds is not None
            else _NullAsyncContext()
        )
        try:
            async with timeout_ctx:
                await _race_to_end(
                    env=env,
                    buyer_agent=buyer_agent,
                    buyer_resources=buyer_resources,
                    seller_agent=seller_agent,
                    seller_resources=seller_resources,
                    cancel_event=cancel_event,
                )
        except asyncio.TimeoutError:
            env.mark_ended(reason="max_wall_time")

        if not env.end_event.is_set():
            env.mark_ended(reason="max_actions")

        # If we ended without a deal, label the outcome.
        if not env.state.outcome.deal_reached and env.state.outcome.end_reason is None:
            env.state.outcome.ended_by = "max_rounds"
            env.state.outcome.end_reason = env.end_reason or "Ended without agreement."
    except asyncio.CancelledError:
        env.mark_ended(reason="cancelled")
        raise
    except Exception as ex:
        logger.exception("Error during marketplace execution.")
        error = str(ex)
        env.mark_ended(reason="error")
        env.state.outcome.end_reason = env.state.outcome.end_reason or traceback.format_exc()
    finally:
        await buyer_agent.close()
        await seller_agent.close()

    return MarketplaceExecutionResult(
        task=task,
        outcome=env.state.outcome,
        messages=env.state.messages,
        offers=env.state.offers,
        action_trace=env.state.action_trace,
        invalid_actions=sum(1 for t in env.state.action_trace if not t.valid),
        buyer_context=buyer_agent.messages,
        seller_context=seller_agent.messages,
        total_actions=env.state.action_count,
        end_reason=env.end_reason,
        error=error,
    )


async def _race_to_end(
    *,
    env: MarketplaceEnvironment,
    buyer_agent: BuyerAgent,
    buyer_resources: AgentResources,
    seller_agent: SellerAgent,
    seller_resources: AgentResources,
    cancel_event: asyncio.Event | None,
) -> None:
    t_buyer = asyncio.create_task(buyer_agent.run(buyer_resources.execute))
    t_seller = asyncio.create_task(seller_agent.run(seller_resources.execute))
    t_end = asyncio.create_task(env.end_event.wait())
    watch: set[asyncio.Task] = {t_buyer, t_seller, t_end}
    t_cancel: asyncio.Task | None = None
    if cancel_event is not None:
        t_cancel = asyncio.create_task(cancel_event.wait())
        watch.add(t_cancel)
    try:
        await asyncio.wait(watch, return_when=asyncio.FIRST_COMPLETED)
    finally:
        for t in (t_buyer, t_seller, t_end, t_cancel):
            if t is not None and not t.done():
                t.cancel()
        await asyncio.gather(*[t for t in watch if t is not None], return_exceptions=True)


class _NullAsyncContext:
    async def __aenter__(self) -> None:
        return None

    async def __aexit__(self, *_exc) -> bool:
        return False


__all__ = [
    "execute_task",
    "MarketplaceExecutionResult",
    "MarketplaceTask",
]
