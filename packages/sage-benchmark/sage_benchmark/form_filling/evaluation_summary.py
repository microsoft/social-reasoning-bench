"""Structured summary computation and printing for the form-filling benchmark.

Mirrors the calendar_scheduling pattern:
  compute_summary()          -> FormFillingBenchmarkSummary
  print_per_task_summary()   -> per-task table to stdout
  print_evaluation_summary() -> aggregate stats to stdout
"""

from __future__ import annotations

from sage_benchmark.form_filling.schemas import (
    FormFillingBenchmarkSummary,
    FormFillingFailedTaskError,
    InteractiveTaskEvaluationResult,
    InteractiveTaskExecutionResult,
)

# ---------------------------------------------------------------------------
# compute_summary
# ---------------------------------------------------------------------------


def compute_summary(
    execution_results: list[InteractiveTaskExecutionResult],
    evaluation_results: list[InteractiveTaskEvaluationResult],
) -> FormFillingBenchmarkSummary:
    """Compute aggregate statistics from execution and evaluation results.

    Args:
        execution_results: All execution results (including failures).
        evaluation_results: Successfully evaluated results.

    Returns:
        A ``FormFillingBenchmarkSummary`` Pydantic model.
    """
    n_total = len(execution_results)
    successful_execs = [r for r in execution_results if r.success]
    n_successful = len(successful_execs)
    n_evals = len(evaluation_results)

    failed_task_errors = [
        FormFillingFailedTaskError(
            form_id=r.form_id,
            task_index=r.task_index,
            error=r.error_message or "unknown error",
        )
        for r in execution_results
        if not r.success
    ]

    if n_evals == 0:
        return FormFillingBenchmarkSummary(
            total_tasks=n_total,
            successful_executions=n_successful,
            evaluated_forms=0,
            failed_tasks=n_total - n_successful,
            failed_task_errors=failed_task_errors,
        )

    # Correctness metrics
    avg_accuracy = sum(e.correctness.accuracy for e in evaluation_results) / n_evals
    avg_precision = sum(e.correctness.precision for e in evaluation_results) / n_evals
    avg_recall = sum(e.correctness.recall for e in evaluation_results) / n_evals
    avg_f1 = sum(e.correctness.f1_score for e in evaluation_results) / n_evals
    perfect_forms = sum(1 for e in evaluation_results if e.correctness.f1_score == 1.0)
    perfect_forms_rate = perfect_forms / n_evals

    # Privacy metrics
    avg_form_privacy = sum(e.form_privacy.privacy_score for e in evaluation_results) / n_evals
    avg_conv_privacy = (
        sum(e.conversation_privacy.privacy_score for e in evaluation_results) / n_evals
    )
    form_leakage_count = sum(
        1 for e in evaluation_results if len(e.form_privacy.secrets_leaked) > 0
    )
    conv_leakage_count = sum(
        1
        for e in evaluation_results
        if len(e.conversation_privacy.secrets_leaked_in_conversation) > 0
    )
    total_secrets = sum(len(e.form_privacy.secrets_checked) for e in evaluation_results)
    total_form_leaked = sum(len(e.form_privacy.secrets_leaked) for e in evaluation_results)
    total_conv_leaked = sum(
        len(e.conversation_privacy.secrets_leaked_in_conversation) for e in evaluation_results
    )

    # CI metrics
    total_form_ci_violations = sum(len(e.form_privacy_ci) for e in evaluation_results)
    total_conv_ci_violations = sum(len(e.conversation_privacy_ci) for e in evaluation_results)
    tasks_with_form_ci = sum(1 for e in evaluation_results if len(e.form_privacy_ci) > 0)
    tasks_with_conv_ci = sum(1 for e in evaluation_results if len(e.conversation_privacy_ci) > 0)

    # Due diligence
    total_dd_fields = sum(e.due_diligence.total_masked_fields for e in evaluation_results)
    avg_mf_accuracy = (
        sum(e.due_diligence.masked_field_accuracy for e in evaluation_results) / n_evals
    )

    # Duty of care
    total_doc_fields = sum(e.duty_of_care.total_fields for e in evaluation_results)
    scored_doc_evals = [e for e in evaluation_results if e.duty_of_care.min_score is not None]
    avg_duty_of_care_score = (
        sum(e.duty_of_care.min_score for e in scored_doc_evals) / len(scored_doc_evals)  # type: ignore[arg-type]
        if scored_doc_evals
        else None
    )

    # Validation
    validation_rate = sum(1 for e in evaluation_results if e.pydantic_validation_passed) / n_evals

    return FormFillingBenchmarkSummary(
        total_tasks=n_total,
        successful_executions=n_successful,
        evaluated_forms=n_evals,
        failed_tasks=n_total - n_successful,
        failed_task_errors=failed_task_errors,
        # Correctness
        avg_accuracy=avg_accuracy,
        avg_precision=avg_precision,
        avg_recall=avg_recall,
        avg_f1_score=avg_f1,
        perfect_forms=perfect_forms,
        perfect_forms_rate=perfect_forms_rate,
        # Privacy
        avg_form_privacy_score=avg_form_privacy,
        avg_conversation_privacy_score=avg_conv_privacy,
        form_leakage_count=form_leakage_count,
        conversation_leakage_count=conv_leakage_count,
        total_secrets=total_secrets,
        total_form_leaked_secrets=total_form_leaked,
        total_conversation_leaked_secrets=total_conv_leaked,
        # CI
        total_form_ci_violations=total_form_ci_violations,
        total_conversation_ci_violations=total_conv_ci_violations,
        tasks_with_form_ci_violations=tasks_with_form_ci,
        tasks_with_conversation_ci_violations=tasks_with_conv_ci,
        # Due diligence
        total_masked_fields=total_dd_fields,
        avg_masked_field_accuracy=avg_mf_accuracy,
        # Duty of care
        total_duty_of_care_fields=total_doc_fields,
        avg_duty_of_care_score=avg_duty_of_care_score,
        # Validation
        validation_rate=validation_rate,
    )


# ---------------------------------------------------------------------------
# print_per_task_summary
# ---------------------------------------------------------------------------


def print_per_task_summary(eval_results: list[InteractiveTaskEvaluationResult]) -> None:
    """Print a per-task summary table to stdout."""
    if not eval_results:
        return

    # Define columns: (header, width, getter)
    task_col = (
        "Task",
        30,
        lambda r: r.form_id[:30],
    )
    correctness_cols = [
        ("Prec", 6, lambda r: f"{r.correctness.precision:.0%}"),
        ("Rec", 6, lambda r: f"{r.correctness.recall:.0%}"),
        ("F1", 6, lambda r: f"{r.correctness.f1_score:.0%}"),
    ]
    privacy_cols = [
        ("FrmPrv", 6, lambda r: f"{r.form_privacy.privacy_score:.0%}"),
        ("CnvPrv", 6, lambda r: f"{r.conversation_privacy.privacy_score:.0%}"),
    ]
    dd_cols = [
        ("MFAcc", 6, lambda r: f"{r.due_diligence.masked_field_accuracy:.0%}"),
    ]
    doc_cols = [
        (
            "DoC",
            5,
            lambda r: (
                f"{r.duty_of_care.min_score:.2f}" if r.duty_of_care.min_score is not None else "N/A"
            ),
        ),
    ]
    val_cols = [
        ("Valid", 5, lambda r: "yes" if r.pydantic_validation_passed else "no"),
    ]
    all_cols = [task_col] + correctness_cols + privacy_cols + dd_cols + doc_cols + val_cols

    # Group headers
    corr_width = sum(c[1] for c in correctness_cols) + 3 * (len(correctness_cols) - 1)
    priv_width = sum(c[1] for c in privacy_cols) + 3 * (len(privacy_cols) - 1)

    def make_header(label: str, width: int) -> str:
        pad_total = width - len(label)
        pad_left = pad_total // 2
        pad_right = pad_total - pad_left
        return "-" * pad_left + label + "-" * pad_right

    separator = "-+-".join("-" * col[1] for col in all_cols)

    group_header = (
        " " * task_col[1]
        + " | "
        + make_header(" Correctness ", corr_width)
        + " | "
        + make_header(" Privacy ", priv_width)
        + " | "
        + "DD".center(dd_cols[0][1])
        + " | "
        + "DoC".center(doc_cols[0][1])
        + " | "
        + "Val".center(val_cols[0][1])
    )

    header = " | ".join(col[0].ljust(col[1]) for col in all_cols)

    print(f"\n{'=' * len(separator)}")
    print("PER-TASK RESULTS")
    print(f"{'=' * len(separator)}")
    print(group_header)
    print(header)
    print(separator)

    for result in sorted(eval_results, key=lambda r: r.form_id):
        row = " | ".join(col[2](result).ljust(col[1]) for col in all_cols)
        print(row)

    print(f"{'=' * len(separator)}")


# ---------------------------------------------------------------------------
# print_evaluation_summary
# ---------------------------------------------------------------------------


def print_evaluation_summary(summary: FormFillingBenchmarkSummary) -> None:
    """Print summary statistics from a pre-computed FormFillingBenchmarkSummary."""
    # Warn about failures
    if summary.failed_tasks > 0:
        print(f"\n{'=' * 60}")
        print(
            f"WARNING: {summary.failed_tasks} task(s) excluded from statistics due to execution errors:"
        )
        print(f"{'=' * 60}")
        for error in summary.failed_task_errors:
            print(f"  {error.form_id} (idx {error.task_index}): {error.error}")
        print(f"{'=' * 60}\n")

    if summary.evaluated_forms == 0:
        print("No evaluated results to summarize.")
        return

    n = summary.evaluated_forms

    print(f"\n{'=' * 60}")
    print("EVALUATION SUMMARY")
    print(f"{'=' * 60}")
    print(f"Total tasks:                       {summary.total_tasks}")
    print(f"Successful executions:             {summary.successful_executions}")
    print(f"Evaluated forms:                   {summary.evaluated_forms}")
    print(f"Failed tasks (execution errors):   {summary.failed_tasks}")

    print(f"\nCorrectness Metrics:")
    print(f"  Average precision:               {summary.avg_precision:.2%}")
    print(f"  Average recall:                  {summary.avg_recall:.2%}")
    print(f"  Average F1 score:                {summary.avg_f1_score:.2%}")
    print(
        f"  Perfect forms (F1=1.0):          {summary.perfect_forms}/{n} ({summary.perfect_forms_rate:.1%})"
    )

    print(f"\nPrivacy Metrics:")
    print(f"  Average form privacy score:      {summary.avg_form_privacy_score:.2%}")
    print(f"  Average conversation privacy:    {summary.avg_conversation_privacy_score:.2%}")
    print(
        f"  Form leakage rate:               {summary.form_leakage_count}/{n} ({summary.form_leakage_count / n:.1%})"
    )
    print(
        f"  Conversation leakage rate:       {summary.conversation_leakage_count}/{n} ({summary.conversation_leakage_count / n:.1%})"
    )
    print(f"  Total secrets:                   {summary.total_secrets}")
    print(f"  Total form leaked:               {summary.total_form_leaked_secrets}")
    print(f"  Total conversation leaked:       {summary.total_conversation_leaked_secrets}")

    print(f"\nContextual Integrity (CI) Metrics:")
    print(
        f"  Form CI violations:              {summary.total_form_ci_violations} (tasks: {summary.tasks_with_form_ci_violations}/{n})"
    )
    print(
        f"  Conversation CI violations:      {summary.total_conversation_ci_violations} (tasks: {summary.tasks_with_conversation_ci_violations}/{n})"
    )

    print(f"\nDue Diligence Metrics:")
    print(f"  Total masked fields:             {summary.total_masked_fields}")
    print(f"  Average masked field accuracy:   {summary.avg_masked_field_accuracy:.2%}")

    print(f"\nDuty of Care Metrics:")
    print(f"  Total fields evaluated:          {summary.total_duty_of_care_fields}")
    doc_display = (
        f"{summary.avg_duty_of_care_score:.2f}"
        if summary.avg_duty_of_care_score is not None
        else "N/A"
    )
    print(f"  Average min duty of care score:  {doc_display}")

    print(f"\nValidation rate:                   {summary.validation_rate:.1%}")
    print(f"{'=' * 60}")
