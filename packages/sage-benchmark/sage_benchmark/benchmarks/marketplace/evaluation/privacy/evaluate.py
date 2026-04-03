"""Privacy leakage evaluation for marketplace task execution results."""

from __future__ import annotations

from typing import TYPE_CHECKING

from .leakage import MarketplaceLeakageJudge

if TYPE_CHECKING:
    from sage_llm import SageModelClient

    from ...types import (
        MarketplaceExecutionResult,
        MarketplacePrivacyEvaluation,
    )


def _build_role_messages(exec_result: "MarketplaceExecutionResult", role: str) -> str:
    """Concatenate all messages from a given role into a single string.

    Args:
        exec_result: The task execution result containing messages
        role: The role to filter messages by ("buyer" or "seller")

    Returns:
        All messages from the specified role, joined with newlines
    """
    return "\n".join(msg.content for msg in exec_result.messages if msg.speaker == role)


def _build_conversation_context(exec_result: "MarketplaceExecutionResult") -> str:
    """Build a context string with the full conversation and product info.

    Args:
        exec_result: The task execution result

    Returns:
        Formatted context string with product info and conversation history
    """
    parts = []

    # Product info
    parts.append(f"=== PRODUCT ===")
    parts.append(f"Name: {exec_result.task.product.name}")
    parts.append("")

    # Full conversation
    parts.append("=== CONVERSATION HISTORY ===")
    for msg in exec_result.messages:
        parts.append(f"[{msg.speaker.upper()} | Round {msg.round}]: {msg.content}")

    return "\n".join(parts)


async def evaluate_privacy_leakage(
    exec_result: "MarketplaceExecutionResult",
    model: str,
    model_client: "SageModelClient",
    n_votes: int = 5,
) -> tuple["MarketplacePrivacyEvaluation", "MarketplacePrivacyEvaluation"]:
    """Evaluate privacy leakage for both buyer and seller in a marketplace task.

    Checks whether each party's messages leak their opponent's reservation price.
    - Buyer leakage: checks if buyer messages reveal the buyer's reservation price
      (which is the seller's opponent secret)
    - Seller leakage: checks if seller messages reveal the seller's reservation price
      (which is the buyer's opponent secret)

    Args:
        exec_result: The task execution result containing messages and task info
        model: Model name to use for the judge LLM
        model_client: SageModelClient instance for making LLM calls
        n_votes: Number of parallel judges for majority voting (default: 5)

    Returns:
        Tuple of (buyer_privacy, seller_privacy) as MarketplacePrivacyEvaluation instances.
    """
    from ...types import MarketplacePrivacyEvaluation

    judge = MarketplaceLeakageJudge(
        model=model,
        model_client=model_client,
        n_votes=n_votes,
    )

    task = exec_result.task
    context = _build_conversation_context(exec_result)

    # Evaluate buyer messages for leakage of buyer's reservation price
    buyer_secret = f"Reservation price: ${task.buyer.reservation_price:g}"
    buyer_messages = _build_role_messages(exec_result, "buyer")
    if buyer_messages.strip():
        judgment = await judge.aevaluate(
            input=buyer_messages,
            secret=buyer_secret,
            context=context,
        )
        buyer_privacy = MarketplacePrivacyEvaluation(
            secret=buyer_secret,
            leaked=judgment.leaked,
            reasoning=judgment.reasoning,
            evidence=judgment.evidence,
        )
    else:
        buyer_privacy = MarketplacePrivacyEvaluation(secret=buyer_secret, leaked=False)

    # Evaluate seller messages for leakage of seller's reservation price
    seller_secret = f"Reservation price: ${task.seller.reservation_price:g}"
    seller_messages = _build_role_messages(exec_result, "seller")
    if seller_messages.strip():
        judgment = await judge.aevaluate(
            input=seller_messages,
            secret=seller_secret,
            context=context,
        )
        seller_privacy = MarketplacePrivacyEvaluation(
            secret=seller_secret,
            leaked=judgment.leaked,
            reasoning=judgment.reasoning,
            evidence=judgment.evidence,
        )
    else:
        seller_privacy = MarketplacePrivacyEvaluation(secret=seller_secret, leaked=False)

    return buyer_privacy, seller_privacy
