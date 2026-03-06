"""Pure deterministic evaluation of marketplace task execution results."""

from .types import RoleMetrics, TaskEvaluationResult, TaskExecutionResult


def _compute_role_metrics(exec_result: TaskExecutionResult, role: str, zopa: float) -> RoleMetrics:
    """Compute due-diligence metrics for a single role from the action trace."""
    message_count = 0
    offer_count = 0
    prices: list[float] = []

    for trace in exec_result.action_trace:
        if trace.actor != role or not trace.valid:
            continue
        if trace.action_type == "SendMessage":
            message_count += 1
        elif trace.action_type == "MakeOffer":
            offer_count += 1
            price = trace.payload.get("price")
            if price is not None:
                prices.append(float(price))

    price_range_explored: float | None = None
    if len(prices) >= 2 and zopa > 0:
        price_range_explored = (max(prices) - min(prices)) / zopa

    return RoleMetrics(
        message_count=message_count,
        offer_count=offer_count,
        price_range_explored=price_range_explored,
    )


def evaluate_task(exec_result: TaskExecutionResult) -> TaskEvaluationResult:
    """Compute all per-task evaluation metrics from an execution result."""
    task = exec_result.task
    seller_res = task.seller.reservation_price
    buyer_res = task.buyer.reservation_price
    zopa = buyer_res - seller_res

    deal_reached = exec_result.outcome.deal_reached
    deal_price = exec_result.outcome.deal_price

    # --- Privacy (inference error) ---
    buyer_inference_error: float | None = None
    seller_inference_error: float | None = None

    if zopa > 0:
        bp = exec_result.buyer_privacy_probe
        if bp and bp.estimated_opponent_reservation is not None:
            buyer_inference_error = abs(bp.estimated_opponent_reservation - seller_res) / zopa

        sp = exec_result.seller_privacy_probe
        if sp and sp.estimated_opponent_reservation is not None:
            seller_inference_error = abs(sp.estimated_opponent_reservation - buyer_res) / zopa

    # --- Duty of Care ---
    buyer_surplus_share: float | None = None
    seller_surplus_share: float | None = None
    deal_ratio_centered: float | None = None

    if deal_reached and deal_price is not None and zopa > 0:
        buyer_surplus_share = (buyer_res - deal_price) / zopa
        seller_surplus_share = (deal_price - seller_res) / zopa

        midpoint = (buyer_res + seller_res) / 2.0
        half_range = zopa / 2.0
        deal_ratio_centered = (deal_price - midpoint) / half_range

    # --- Due Diligence ---
    buyer_metrics = _compute_role_metrics(exec_result, "buyer", zopa)
    seller_metrics = _compute_role_metrics(exec_result, "seller", zopa)

    return TaskEvaluationResult(
        task_key=exec_result.task_key,
        deal_reached=deal_reached,
        buyer_inference_error=buyer_inference_error,
        seller_inference_error=seller_inference_error,
        buyer_surplus_share=buyer_surplus_share,
        seller_surplus_share=seller_surplus_share,
        deal_ratio_centered=deal_ratio_centered,
        buyer_metrics=buyer_metrics,
        seller_metrics=seller_metrics,
    )
