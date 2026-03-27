"""Summary computation and printing for marketplace benchmark evaluation results."""

from __future__ import annotations

from .types import (
    MarketplaceBenchmarkSummary,
    TaskEvaluationResult,
    TaskExecutionResult,
)


def _safe_avg(values: list[float | None]) -> float | None:
    """Compute the average of non-None values, or None if empty."""
    filtered = [v for v in values if v is not None]
    if not filtered:
        return None
    return sum(filtered) / len(filtered)


def compute_summary(
    eval_results: list[TaskEvaluationResult],
    exec_results: list[TaskExecutionResult],
) -> MarketplaceBenchmarkSummary:
    """Compute summary statistics from evaluation results.

    Args:
        eval_results: Evaluated task results (may be fewer than exec_results if
            some evaluations were skipped or failed).
        exec_results: All execution results (used for deal counting).

    Returns:
        MarketplaceBenchmarkSummary with aggregate statistics.
    """
    total = len(exec_results)
    deal_count = sum(1 for r in exec_results if r.outcome.deal_reached)
    deal_rate = (deal_count / total) if total else 0.0

    # Task success
    task_success_count = sum(1 for e in eval_results if e.task_success)
    task_success_rate = (task_success_count / len(eval_results)) if eval_results else 0.0

    # Privacy — leakage judge
    avg_buyer_leakage = _safe_avg([e.buyer_leakage_score for e in eval_results])
    avg_seller_leakage = _safe_avg([e.seller_leakage_score for e in eval_results])

    # Privacy — inference error
    avg_buyer_ie = _safe_avg([e.buyer_inference_error for e in eval_results])
    avg_seller_ie = _safe_avg([e.seller_inference_error for e in eval_results])

    # Duty of Care
    avg_buyer_doc = _safe_avg([e.buyer_duty_of_care for e in eval_results])
    avg_seller_doc = _safe_avg([e.seller_duty_of_care for e in eval_results])
    avg_deal_ratio = _safe_avg([e.deal_ratio_centered for e in eval_results])

    # Due Diligence
    avg_buyer_effort = _safe_avg([float(e.buyer_metrics.effort_action_count) for e in eval_results])
    avg_seller_effort = _safe_avg(
        [float(e.seller_metrics.effort_action_count) for e in eval_results]
    )
    avg_buyer_msgs = _safe_avg([float(e.buyer_metrics.message_count) for e in eval_results])
    avg_seller_msgs = _safe_avg([float(e.seller_metrics.message_count) for e in eval_results])
    avg_buyer_offers = _safe_avg([float(e.buyer_metrics.offer_count) for e in eval_results])
    avg_seller_offers = _safe_avg([float(e.seller_metrics.offer_count) for e in eval_results])

    return MarketplaceBenchmarkSummary(
        total_tasks=total,
        deal_count=deal_count,
        deal_rate=deal_rate,
        task_success_count=task_success_count,
        task_success_rate=task_success_rate,
        avg_buyer_leakage_score=avg_buyer_leakage,
        avg_seller_leakage_score=avg_seller_leakage,
        avg_buyer_inference_error=avg_buyer_ie,
        avg_seller_inference_error=avg_seller_ie,
        avg_buyer_duty_of_care=avg_buyer_doc,
        avg_seller_duty_of_care=avg_seller_doc,
        avg_deal_ratio_centered=avg_deal_ratio,
        avg_buyer_effort_actions=avg_buyer_effort,
        avg_seller_effort_actions=avg_seller_effort,
        avg_buyer_messages=avg_buyer_msgs,
        avg_seller_messages=avg_seller_msgs,
        avg_buyer_offers=avg_buyer_offers,
        avg_seller_offers=avg_seller_offers,
    )


def print_per_task_summary(
    eval_results: list[TaskEvaluationResult],
    exec_results: list[TaskExecutionResult],
) -> None:
    """Print a per-task summary table for marketplace results."""
    if not eval_results:
        return

    # Build a lookup from task_key -> exec_result for deal/price info
    exec_by_key: dict[str, TaskExecutionResult] = {r.task_key: r for r in exec_results}

    def task_description(e: TaskEvaluationResult) -> str:
        ex = exec_by_key.get(e.task_key)
        task_id = ex.task.id if ex else "?"
        malicious_parts = []
        if ex:
            if ex.task.buyer.is_malicious:
                malicious_parts.append("buyer-mal")
            if ex.task.seller.is_malicious:
                malicious_parts.append("seller-mal")
        mal_str = ", ".join(malicious_parts) if malicious_parts else "normal"
        return f"Task {task_id}: {mal_str}"

    # Define columns: (header, width, getter)
    task_col = ("Task", 28, task_description)
    outcome_cols = [
        ("Deal", 4, lambda e: "yes" if e.deal_reached else "no"),
        (
            "Price",
            8,
            lambda e: (
                f"${exec_by_key[e.task_key].outcome.deal_price:.0f}"
                if e.task_key in exec_by_key
                and exec_by_key[e.task_key].outcome.deal_price is not None
                else "N/A"
            ),
        ),
        ("Success", 7, lambda e: "YES" if e.task_success else "NO"),
    ]
    privacy_cols = [
        (
            "BLeak",
            5,
            lambda e: (
                f"{e.buyer_leakage_score:.2f}" if e.buyer_leakage_score is not None else "N/A"
            ),
        ),
        (
            "SLeak",
            5,
            lambda e: (
                f"{e.seller_leakage_score:.2f}" if e.seller_leakage_score is not None else "N/A"
            ),
        ),
    ]
    doc_cols = [
        (
            "BDoC",
            5,
            lambda e: f"{e.buyer_duty_of_care:.2f}" if e.buyer_duty_of_care is not None else "N/A",
        ),
        (
            "SDoC",
            5,
            lambda e: (
                f"{e.seller_duty_of_care:.2f}" if e.seller_duty_of_care is not None else "N/A"
            ),
        ),
    ]
    dd_cols = [
        ("BEff", 4, lambda e: str(e.buyer_metrics.effort_action_count)),
        ("SEff", 4, lambda e: str(e.seller_metrics.effort_action_count)),
    ]
    all_cols = [task_col] + outcome_cols + privacy_cols + doc_cols + dd_cols

    # Group headers
    outcome_width = sum(c[1] for c in outcome_cols) + 3 * (len(outcome_cols) - 1)
    privacy_width = sum(c[1] for c in privacy_cols) + 3 * (len(privacy_cols) - 1)
    doc_width = sum(c[1] for c in doc_cols) + 3 * (len(doc_cols) - 1)
    dd_width = sum(c[1] for c in dd_cols) + 3 * (len(dd_cols) - 1)

    separator = "-+-".join("-" * col[1] for col in all_cols)

    group_header = (
        " " * task_col[1]
        + " | "
        + "Outcome".center(outcome_width)
        + " | "
        + "Privacy".center(privacy_width)
        + " | "
        + "Duty of Care".center(doc_width)
        + " | "
        + "Due Diligence".center(dd_width)
    )

    header = " | ".join(col[0].ljust(col[1]) for col in all_cols)

    print(f"\n{'=' * len(separator)}")
    print("PER-TASK RESULTS")
    print(f"{'=' * len(separator)}")
    print(group_header)
    print(header)
    print(separator)

    # Sort by task id when available
    def sort_key(e: TaskEvaluationResult) -> int:
        ex = exec_by_key.get(e.task_key)
        return ex.task.id if ex else 0

    for result in sorted(eval_results, key=sort_key):
        row = " | ".join(col[2](result).ljust(col[1]) for col in all_cols)
        print(row)

    print(f"{'=' * len(separator)}")


def print_evaluation_summary(summary: MarketplaceBenchmarkSummary) -> None:
    """Print summary statistics from a pre-computed MarketplaceBenchmarkSummary."""
    if summary.total_tasks == 0:
        print("No results to summarize.")
        return

    print(f"\n{'=' * 40}")
    print("EVALUATION SUMMARY")
    print(f"{'=' * 40}")
    print(f"Total tasks:                    {summary.total_tasks}")
    print(
        f"Deals reached:                  {summary.deal_count}/{summary.total_tasks} "
        f"({summary.deal_rate:.1%})"
    )
    print(
        f"Task success rate:              {summary.task_success_count}/{summary.total_tasks} "
        f"({summary.task_success_rate:.1%})"
    )

    # Privacy
    has_privacy = (
        summary.avg_buyer_leakage_score is not None or summary.avg_seller_leakage_score is not None
    )
    if has_privacy:
        print("\nPrivacy (leakage judge):")
        if summary.avg_buyer_leakage_score is not None:
            print(f"  Avg buyer leakage score:      {summary.avg_buyer_leakage_score:.3f}")
        if summary.avg_seller_leakage_score is not None:
            print(f"  Avg seller leakage score:     {summary.avg_seller_leakage_score:.3f}")

    has_inference = (
        summary.avg_buyer_inference_error is not None
        or summary.avg_seller_inference_error is not None
    )
    if has_inference:
        print("\nPrivacy (inference error):")
        if summary.avg_buyer_inference_error is not None:
            print(f"  Avg buyer inference error:     {summary.avg_buyer_inference_error:.3f}")
        if summary.avg_seller_inference_error is not None:
            print(f"  Avg seller inference error:    {summary.avg_seller_inference_error:.3f}")

    # Duty of Care
    has_doc = (
        summary.avg_buyer_duty_of_care is not None or summary.avg_seller_duty_of_care is not None
    )
    if has_doc:
        print("\nDuty of Care:")
        if summary.avg_buyer_duty_of_care is not None:
            print(f"  Avg buyer duty of care:       {summary.avg_buyer_duty_of_care:.3f}")
        if summary.avg_seller_duty_of_care is not None:
            print(f"  Avg seller duty of care:      {summary.avg_seller_duty_of_care:.3f}")
        if summary.avg_deal_ratio_centered is not None:
            print(f"  Avg deal ratio (centered):    {summary.avg_deal_ratio_centered:.3f}")

    # Due Diligence
    has_dd = (
        summary.avg_buyer_effort_actions is not None
        or summary.avg_seller_effort_actions is not None
    )
    if has_dd:
        print("\nDue Diligence:")
        if summary.avg_buyer_effort_actions is not None:
            print(f"  Avg buyer effort actions:     {summary.avg_buyer_effort_actions:.1f}")
        if summary.avg_seller_effort_actions is not None:
            print(f"  Avg seller effort actions:    {summary.avg_seller_effort_actions:.1f}")
        if summary.avg_buyer_messages is not None:
            print(f"  Avg buyer messages:           {summary.avg_buyer_messages:.1f}")
        if summary.avg_seller_messages is not None:
            print(f"  Avg seller messages:          {summary.avg_seller_messages:.1f}")
        if summary.avg_buyer_offers is not None:
            print(f"  Avg buyer offers:             {summary.avg_buyer_offers:.1f}")
        if summary.avg_seller_offers is not None:
            print(f"  Avg seller offers:            {summary.avg_seller_offers:.1f}")

    print(f"{'=' * 40}")
