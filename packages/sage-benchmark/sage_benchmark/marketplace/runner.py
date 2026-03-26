"""Minimal marketplace simulation runner (LLM tool-calling agents)."""

import logging
import re
import traceback

from sage_llm import ModelClient

from sage_benchmark.shared.executors import TaskPoolExecutor
from sage_benchmark.shared.logging import BenchmarkLogger

from .agents import BuyerAgent, MarketplaceAgent, SellerAgent
from .environment import AgentResources, EndConversation, MarketplaceEnvironment, Wait
from .environment.resources import execute_with_trace
from .evaluation import evaluate_task, evaluate_task_with_privacy
from .types import (
    ActionTrace,
    KeyedMarketplaceTask,
    PrivacyProbe,
    TaskEvaluationResult,
    TaskExecutionResult,
)

logger = logging.getLogger(__name__)

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
    """Run one agent turn until Wait, EndConversation, or max_steps."""
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
        if isinstance(action, EndConversation) and ok:
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


async def run_and_evaluate_tasks(
    tasks: list[KeyedMarketplaceTask],
    *,
    buyer_model: str,
    seller_model: str,
    buyer_client: ModelClient,
    seller_client: ModelClient,
    max_steps_per_turn: int = 3,
    batch_size: int = 50,
    benchmark_logger: BenchmarkLogger | None = None,
    judge_model: str | None = None,
    judge_client: ModelClient | None = None,
) -> list[tuple[TaskExecutionResult, TaskEvaluationResult]]:
    """Run and evaluate marketplace tasks in a single pass via TaskPoolExecutor.

    Each task is executed then immediately evaluated before the next task starts,
    avoiding a drain-and-restart between execution and evaluation phases.

    Args:
        tasks: List of marketplace tasks to execute.
        buyer_model: Model name for the buyer agent.
        seller_model: Model name for the seller agent.
        buyer_client: ModelClient for the buyer agent.
        seller_client: ModelClient for the seller agent.
        max_steps_per_turn: Maximum tool calls per agent turn.
        batch_size: Maximum number of concurrent tasks.
        benchmark_logger: Optional logger for progress tracking.
        judge_model: Model name for LLM-based privacy judge (None = skip).
        judge_client: ModelClient for the judge.

    Returns:
        List of (TaskExecutionResult, TaskEvaluationResult) tuples.
    """

    async def _run_and_evaluate_single(
        task: KeyedMarketplaceTask,
    ) -> tuple[TaskExecutionResult, TaskEvaluationResult]:
        """Execute a single task then immediately evaluate it."""
        # Execute
        exec_result = await _run_single_task_llm(
            task,
            buyer_model=buyer_model,
            seller_model=seller_model,
            buyer_client=buyer_client,
            seller_client=seller_client,
            max_steps_per_turn=max_steps_per_turn,
        )
        # Evaluate (coupled — no drain between phases)
        if judge_model and judge_client:
            eval_result = await evaluate_task_with_privacy(exec_result, judge_model, judge_client)
        else:
            eval_result = evaluate_task(exec_result)
        return exec_result, eval_result

    if benchmark_logger:
        benchmark_logger.on_phase_start("run+evaluate", len(tasks))

    def on_complete(result: tuple[TaskExecutionResult, TaskEvaluationResult]) -> None:
        exec_result, _ = result
        if benchmark_logger:
            benchmark_logger.on_task_complete(exec_result.task.id, success=True)

    def on_error(error: Exception) -> None:
        if benchmark_logger:
            benchmark_logger.on_task_complete(0, success=False, error=str(error))

    executor = TaskPoolExecutor(
        batch_size=batch_size,
        on_task_complete=on_complete,
        on_task_error=on_error,
        task_logger=logger,
    )

    results = await executor.run(_run_and_evaluate_single(task) for task in tasks)

    if benchmark_logger:
        failed = len(tasks) - len(results)
        benchmark_logger.on_phase_complete("run+evaluate", len(results), failed)

    return results
