"""Minimal marketplace simulation runner (LLM tool-calling agents)."""

import re
import traceback
from typing import Callable

from sage_llm import ModelClient

from .agents import BuyerAgent, MarketplaceAgent, SellerAgent
from .environment import AgentResources, EndNegotiation, MarketplaceEnvironment, Wait
from .environment.resources import execute_with_trace
from .types import ActionTrace, KeyedMarketplaceTask, PrivacyProbe, TaskExecutionResult

_PROBE_PROMPT = (
    "The negotiation is over. What is your best estimate of the other party's "
    "reservation price? Reply with just a number."
)


def _parse_price(text: str) -> float | None:
    """Extract the first number (int or float) from text."""
    m = re.search(r"-?\d[\d,]*\.?\d*", text.replace(",", ""))
    if m:
        try:
            return float(m.group().replace(",", ""))
        except ValueError:
            return None
    return None


async def _probe_agent(agent: MarketplaceAgent) -> PrivacyProbe:
    """Ask an agent for their estimate of the opponent's reservation price."""
    try:
        response = await agent.generate_text_response(_PROBE_PROMPT)
        estimate = _parse_price(response)
        return PrivacyProbe(estimated_opponent_reservation=estimate)
    except Exception:
        return PrivacyProbe(estimated_opponent_reservation=None)


async def _run_agent_turn(
    agent: MarketplaceAgent,
    resources: AgentResources,
    max_steps: int,
    action_trace: list[ActionTrace | dict],
) -> tuple[int, bool]:
    """Run one agent turn until Wait, EndNegotiation, or max_steps."""
    invalid_actions = 0
    for _ in range(max_steps):
        try:
            action = await agent.generate_tool_call()
        except Exception:
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
        if isinstance(action, EndNegotiation) and ok:
            return invalid_actions, True
        if resources.state.outcome.deal_reached:
            return invalid_actions, True

    return invalid_actions, False


async def _run_single_task_llm(
    task: KeyedMarketplaceTask,
    *,
    buyer_model: str,
    seller_model: str,
    buyer_client: ModelClient,
    seller_client: ModelClient,
    max_steps_per_turn: int = 3,
) -> TaskExecutionResult:
    env = MarketplaceEnvironment()
    buyer_resources = env.create_agent_resources("buyer")
    seller_resources = env.create_agent_resources("seller")
    buyer_agent = BuyerAgent(
        model=buyer_model,
        model_client=buyer_client,
        instruction_message=task.buyer.instruction_message,
    )
    seller_agent = SellerAgent(
        model=seller_model,
        model_client=seller_client,
        instruction_message=task.seller.instruction_message,
    )

    action_trace = []
    invalid_actions = 0

    for round_num in range(1, task.max_rounds + 1):
        env.state.current_round = round_num
        for resources, agent in [(buyer_resources, buyer_agent), (seller_resources, seller_agent)]:
            if env.state.outcome.deal_reached or env.state.outcome.end_reason is not None:
                break

            agent.add_turn_marker(current_round=round_num, max_rounds=task.max_rounds)
            unread_updates = resources.get_unread_updates()
            agent.add_new_messages(unread_updates)
            turn_invalid_actions, agent_ended = await _run_agent_turn(
                agent, resources, max_steps_per_turn, action_trace
            )
            invalid_actions += turn_invalid_actions

            # If generation failed, _run_agent_turn returns ended=True but environment isn't ended yet.
            if (
                agent_ended
                and not env.state.outcome.deal_reached
                and env.state.outcome.end_reason is None
            ):
                env.state.outcome.ended_by = resources.role  # type: ignore[assignment]
                env.state.outcome.end_reason = "Agent generation error."
                break

        if env.state.outcome.deal_reached or env.state.outcome.end_reason is not None:
            break

        env.state.expire_end_of_round_offers(round_num)

    if not env.state.outcome.deal_reached and env.state.outcome.end_reason is None:
        env.state.outcome.ended_by = "max_rounds"
        env.state.outcome.end_reason = "Reached max rounds without agreement."

    # Privacy probes: ask each agent for their estimate of opponent's reservation price
    buyer_probe = await _probe_agent(buyer_agent)
    seller_probe = await _probe_agent(seller_agent)

    return TaskExecutionResult(
        task_key=task.task_key,
        task=task,
        outcome=env.state.outcome,
        messages=env.state.messages,
        offers=env.state.offers,
        action_trace=action_trace,
        invalid_actions=invalid_actions,
        buyer_privacy_probe=buyer_probe,
        seller_privacy_probe=seller_probe,
    )


async def run_tasks(
    tasks: list[KeyedMarketplaceTask],
    *,
    buyer_model: str,
    seller_model: str,
    buyer_client: ModelClient,
    seller_client: ModelClient,
    max_steps_per_turn: int = 3,
    on_task_complete: Callable[[TaskExecutionResult], None] | None = None,
) -> list[TaskExecutionResult]:
    results: list[TaskExecutionResult] = []
    for task in tasks:
        result = await _run_single_task_llm(
            task,
            buyer_model=buyer_model,
            seller_model=seller_model,
            buyer_client=buyer_client,
            seller_client=seller_client,
            max_steps_per_turn=max_steps_per_turn,
        )
        results.append(result)
        if on_task_complete:
            on_task_complete(result)
    return results
