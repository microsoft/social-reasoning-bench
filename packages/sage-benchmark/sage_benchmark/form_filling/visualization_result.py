#!/usr/bin/env python3
"""Visualize individual form filling task results as an HTML file.

Reads a task_results.json file and generates an HTML visualization for a single
task result by index. Shows conversation history (if interactive mode), filled
form, artifacts, and secrets.

Usage:
    python -m sage_benchmark.form_filling.visualization_result <path_to_task_results.json> --id <index>

Examples:
    # Visualize the first result (--id 0 or omitted)
    python -m sage_benchmark.form_filling.visualization_result outputs/form_filling/run_gpt-4o_20260122_214813/task_results.json

    # Visualize a specific result by index
    python -m sage_benchmark.form_filling.visualization_result outputs/form_filling/run_20260122_214157_interactive_interviewer_gpt-5.1_assistant_gpt-4o/task_results.json --id 3

    # Specify a custom output path
    python -m sage_benchmark.form_filling.visualization_result task_results.json --id 0 --output my_result.html

    # Provide a data directory to load artifacts/secrets for interactive results
    python -m sage_benchmark.form_filling.visualization_result task_results.json --id 0 --data data/form-filling/tasks
"""

import argparse
import html
import json
import sys
from pathlib import Path


def escape(text: str) -> str:
    """HTML-escape text and convert newlines to <br>."""
    return html.escape(str(text)).replace("\n", "<br>")


def render_form_fields(data: dict, depth: int = 0) -> str:
    """Recursively render form fields as HTML."""
    parts = []
    for key, value in data.items():
        label = key.replace("_", " ").title()
        if isinstance(value, dict):
            parts.append(
                f'<div class="form-section" style="margin-left:{depth * 20}px">'
                f'<div class="form-section-title">{escape(label)}</div>'
            )
            parts.append(render_form_fields(value, depth + 1))
            parts.append("</div>")
        else:
            display = (
                escape(str(value))
                if value not in (None, "")
                else '<span class="empty">empty</span>'
            )
            parts.append(
                f'<div class="form-field" style="margin-left:{depth * 20}px">'
                f'<span class="field-label">{escape(label)}:</span> '
                f'<span class="field-value">{display}</span>'
                f"</div>"
            )
    return "\n".join(parts)


def render_conversation(conversation: list) -> str:
    """Render conversation messages as HTML."""
    parts = []
    for msg in conversation:
        agent = msg.get("from_agent", "unknown")
        content = msg.get("content", "")
        round_num = msg.get("round", "?")
        timestamp = msg.get("timestamp", "")

        css_class = "interviewer" if agent == "interviewer" else "assistant"
        label = "Interviewer" if agent == "interviewer" else "Assistant"
        icon = "&#x1F4CB;" if agent == "interviewer" else "&#x1F464;"

        parts.append(f'<div class="msg {css_class}">')
        parts.append(f'<div class="msg-header">')
        parts.append(f'<span class="msg-icon">{icon}</span>')
        parts.append(f'<span class="msg-label">{label}</span>')
        parts.append(f'<span class="msg-round">Round {round_num}</span>')
        if timestamp:
            parts.append(f'<span class="msg-time">{escape(timestamp)}</span>')
        parts.append("</div>")
        parts.append(f'<div class="msg-content">{escape(content)}</div>')
        parts.append("</div>")

    return "\n".join(parts)


def render_artifacts(artifacts: list) -> str:
    """Render artifacts as HTML cards."""
    parts = []
    for i, art in enumerate(artifacts):
        art_type = art.get("artifact_type", "unknown")
        content = art.get("content", "")
        metadata = art.get("metadata", {})
        contains_secrets = art.get("contains_secrets", [])

        type_icons = {
            "email": "&#x2709;",
            "note": "&#x1F4DD;",
            "calendar": "&#x1F4C5;",
            "text": "&#x1F4C4;",
        }
        icon = type_icons.get(art_type, "&#x1F4CE;")

        # Build metadata line
        meta_parts = []
        if metadata.get("date"):
            meta_parts.append(
                f'<span class="meta-tag">Date: {escape(str(metadata["date"]))}</span>'
            )
        if metadata.get("sender"):
            meta_parts.append(f'<span class="meta-tag">From: {escape(metadata["sender"])}</span>')
        if metadata.get("recipient"):
            meta_parts.append(f'<span class="meta-tag">To: {escape(metadata["recipient"])}</span>')
        if metadata.get("subject"):
            meta_parts.append(
                f'<span class="meta-tag">Subject: {escape(metadata["subject"])}</span>'
            )
        if metadata.get("title"):
            meta_parts.append(f'<span class="meta-tag">Title: {escape(metadata["title"])}</span>')
        if metadata.get("location"):
            meta_parts.append(
                f'<span class="meta-tag">Location: {escape(str(metadata["location"]))}</span>'
            )

        secrets_html = ""
        if contains_secrets:
            secret_tags = " ".join(
                f'<span class="secret-ref">{escape(s)}</span>' for s in contains_secrets
            )
            secrets_html = f'<div class="artifact-secrets">Contains secrets: {secret_tags}</div>'

        parts.append(f'<div class="artifact-card">')
        parts.append(f'<div class="artifact-header">')
        parts.append(f'<span class="artifact-icon">{icon}</span>')
        parts.append(f'<span class="artifact-type">{escape(art_type.title())}</span>')
        parts.append(f'<span class="artifact-index">#{i}</span>')
        parts.append("</div>")
        if meta_parts:
            parts.append(f'<div class="artifact-meta">{"".join(meta_parts)}</div>')
        parts.append(f'<div class="artifact-content">{escape(content)}</div>')
        if secrets_html:
            parts.append(secrets_html)
        parts.append("</div>")

    return "\n".join(parts)


def render_secrets(secrets: list) -> str:
    """Render secrets as HTML cards."""
    parts = []
    for i, secret in enumerate(secrets):
        detail = secret.get("detail_content", "")
        why_sensitive = secret.get("why_sensitive", "")
        related_question = secret.get("related_question", "")
        question_id = secret.get("question_id", "")
        subtlety = secret.get("subtlety_level", "")
        anchors = secret.get("concrete_anchors", {})

        parts.append(f'<div class="secret-card">')
        parts.append(f'<div class="secret-header">')
        parts.append(f'<span class="secret-icon">&#x1F512;</span>')
        parts.append(f'<span class="secret-title">Secret #{i}</span>')
        if subtlety:
            parts.append(
                f'<span class="subtlety-badge subtlety-{escape(subtlety)}">{escape(subtlety)}</span>'
            )
        parts.append("</div>")

        if related_question:
            parts.append(
                f'<div class="secret-field">Related field: '
                f"<code>{escape(question_id or related_question)}</code></div>"
            )

        parts.append(f'<div class="secret-detail">')
        parts.append(f"<strong>Content:</strong><br>{escape(detail)}")
        parts.append("</div>")

        if why_sensitive:
            parts.append(f'<div class="secret-why">')
            parts.append(f"<strong>Why sensitive:</strong><br>{escape(why_sensitive)}")
            parts.append("</div>")

        if anchors and isinstance(anchors, dict):
            anchor_parts = []
            for anchor_type, values in anchors.items():
                if values:
                    items = ", ".join(escape(str(v)) for v in values)
                    anchor_parts.append(
                        f'<span class="anchor-type">{escape(anchor_type.title())}:</span> {items}'
                    )
            if anchor_parts:
                parts.append(f'<div class="secret-anchors">')
                parts.append(f"<strong>Concrete anchors:</strong><br>")
                parts.append("<br>".join(anchor_parts))
                parts.append("</div>")

        parts.append("</div>")

    return "\n".join(parts)


def load_eval_result(eval_path: Path, task_index: int, form_id: int) -> dict | None:
    """Load evaluation result matching the given task_index and form_id."""
    try:
        with open(eval_path) as f:
            eval_data = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"Warning: Failed to load {eval_path}: {e}", file=sys.stderr)
        return None

    if not isinstance(eval_data, list):
        return None

    for entry in eval_data:
        if entry.get("task_index") == task_index and entry.get("form_id") == form_id:
            return entry.get("evaluation", {})

    # Fallback: match by task_index only
    for entry in eval_data:
        if entry.get("task_index") == task_index:
            return entry.get("evaluation", {})

    return None


def render_correctness(correctness: dict) -> str:
    """Render correctness evaluation as an HTML table with aggregate scores."""
    parts = []

    # Aggregate scores
    accuracy = correctness.get("accuracy")
    precision = correctness.get("precision")
    recall = correctness.get("recall")
    f1 = correctness.get("f1_score")
    exact = correctness.get("exact_matches", 0)
    semantic = correctness.get("semantic_matches", 0)
    grounded = correctness.get("grounded_matches", 0)
    total = correctness.get("total_fields", 0)
    filled_by_agent = correctness.get("total_filled_by_agent")
    should_fill = correctness.get("total_should_fill")

    score_items = []
    if accuracy is not None:
        score_items.append(
            f'<div class="eval-metric"><span class="metric-label">Accuracy</span>'
            f'<span class="metric-value">{accuracy:.3f}</span></div>'
        )
    if f1 is not None:
        score_items.append(
            f'<div class="eval-metric"><span class="metric-label">F1</span>'
            f'<span class="metric-value">{f1:.3f}</span></div>'
        )
    if precision is not None:
        score_items.append(
            f'<div class="eval-metric"><span class="metric-label">Precision</span>'
            f'<span class="metric-value">{precision:.3f}</span></div>'
        )
    if recall is not None:
        score_items.append(
            f'<div class="eval-metric"><span class="metric-label">Recall</span>'
            f'<span class="metric-value">{recall:.3f}</span></div>'
        )
    score_items.append(
        f'<div class="eval-metric"><span class="metric-label">Exact</span>'
        f'<span class="metric-value">{exact}/{total}</span></div>'
    )
    score_items.append(
        f'<div class="eval-metric"><span class="metric-label">Semantic</span>'
        f'<span class="metric-value">{semantic}/{total}</span></div>'
    )
    if filled_by_agent is not None and should_fill is not None:
        score_items.append(
            f'<div class="eval-metric"><span class="metric-label">Filled/Expected</span>'
            f'<span class="metric-value">{filled_by_agent}/{should_fill}</span></div>'
        )

    parts.append(f'<div class="eval-metrics-bar">{"".join(score_items)}</div>')

    # Per-field table
    field_evals = correctness.get("field_evaluations", [])
    if field_evals:
        parts.append('<table class="eval-table">')
        parts.append(
            "<thead><tr><th>Field</th><th>Expected</th><th>Actual</th>"
            "<th>Correct</th><th>Grounded</th><th>Reason</th></tr></thead>"
        )
        parts.append("<tbody>")
        for fe in field_evals:
            field_id = fe.get("field_id", "")
            expected = escape(str(fe.get("expected_value", "")))
            actual = escape(str(fe.get("actual_value", "")))
            is_correct = fe.get("is_correct", False)
            is_grounded = fe.get("is_grounded", False)
            reason = fe.get("reason") or ""

            correct_icon = (
                '<span class="eval-pass">&#10003;</span>'
                if is_correct
                else '<span class="eval-fail">&#10007;</span>'
            )
            grounded_icon = (
                '<span class="eval-pass">&#10003;</span>'
                if is_grounded
                else '<span class="eval-fail">&#10007;</span>'
            )

            # Truncate long values for the table
            expected_short = expected[:120] + "..." if len(expected) > 120 else expected
            actual_short = actual[:120] + "..." if len(actual) > 120 else actual
            reason_short = escape(reason[:200] + "...") if len(reason) > 200 else escape(reason)

            row_class = "eval-row-pass" if is_correct else "eval-row-fail"
            parts.append(f'<tr class="{row_class}">')
            parts.append(f'<td class="field-id-cell"><code>{escape(field_id)}</code></td>')
            parts.append(f'<td class="eval-val-cell" title="{expected}">{expected_short}</td>')
            parts.append(f'<td class="eval-val-cell" title="{actual}">{actual_short}</td>')
            parts.append(f'<td class="eval-icon-cell">{correct_icon}</td>')
            parts.append(f'<td class="eval-icon-cell">{grounded_icon}</td>')
            parts.append(f'<td class="eval-reason-cell">{reason_short}</td>')
            parts.append("</tr>")
        parts.append("</tbody></table>")

    return "\n".join(parts)


def render_privacy_eval(privacy: dict, label: str) -> str:
    """Render a privacy evaluation section."""
    parts = []

    score = privacy.get("privacy_score")
    secrets_checked = privacy.get("secrets_checked", [])
    secrets_leaked = privacy.get(
        "secrets_leaked", privacy.get("secrets_leaked_in_conversation", [])
    )
    leakage_details = privacy.get("leakage_details", [])

    # Score bar
    score_class = (
        "eval-pass"
        if score is not None and score >= 0.9
        else "eval-warn"
        if score is not None and score >= 0.7
        else "eval-fail"
    )
    score_display = f"{score:.3f}" if score is not None else "N/A"
    parts.append(f'<div class="eval-metrics-bar">')
    parts.append(
        f'<div class="eval-metric"><span class="metric-label">{escape(label)} Score</span>'
        f'<span class="metric-value {score_class}">{score_display}</span></div>'
    )
    parts.append(
        f'<div class="eval-metric"><span class="metric-label">Secrets Checked</span>'
        f'<span class="metric-value">{len(secrets_checked)}</span></div>'
    )
    parts.append(
        f'<div class="eval-metric"><span class="metric-label">Secrets Leaked</span>'
        f'<span class="metric-value {"eval-fail" if secrets_leaked else "eval-pass"}">'
        f"{len(secrets_leaked)}</span></div>"
    )
    parts.append("</div>")

    # Leakage details
    if leakage_details:
        parts.append('<div class="leakage-section">')
        parts.append(f'<h3 class="leakage-title">Leakage Details ({len(leakage_details)})</h3>')
        for i, detail in enumerate(leakage_details):
            severity = detail.get("severity", "unknown")
            evidence = detail.get("evidence", [])
            sensitive_elements = detail.get("sensitive_elements_found", [])
            analysis = detail.get("analysis", "")
            secret_content = detail.get("secret_content", "")

            sev_class = f"severity-{severity}"
            parts.append(f'<div class="leakage-card">')
            parts.append(f'<div class="leakage-header">')
            parts.append(f'<span class="leakage-index">Leak #{i}</span>')
            parts.append(f'<span class="severity-badge {sev_class}">{escape(severity)}</span>')
            parts.append("</div>")

            if secret_content:
                short_secret = (
                    secret_content[:200] + "..." if len(secret_content) > 200 else secret_content
                )
                parts.append(
                    f'<div class="leakage-secret"><strong>Secret:</strong> {escape(short_secret)}</div>'
                )

            if evidence:
                parts.append('<div class="leakage-evidence"><strong>Evidence:</strong><ul>')
                for ev in evidence:
                    parts.append(f"<li>{escape(str(ev))}</li>")
                parts.append("</ul></div>")

            if sensitive_elements:
                parts.append(
                    '<div class="leakage-elements"><strong>Sensitive elements found:</strong><ul>'
                )
                for el in sensitive_elements:
                    parts.append(f"<li>{escape(str(el))}</li>")
                parts.append("</ul></div>")

            if analysis:
                parts.append(
                    f'<details class="leakage-analysis"><summary>Full analysis</summary>'
                    f'<div class="analysis-content">{escape(analysis)}</div></details>'
                )

            parts.append("</div>")
        parts.append("</div>")

    return "\n".join(parts)


def load_task_data(form_id: int, data_dir: Path) -> dict | None:
    """Load task data (artifacts, secrets) from the data directory."""
    task_dir = data_dir / f"form_{form_id}"
    if not task_dir.is_dir():
        return None

    result = {}
    artifacts_path = task_dir / "artifacts.json"
    if artifacts_path.exists():
        with open(artifacts_path) as f:
            arts_data = json.load(f)
        if isinstance(arts_data, dict):
            result["artifacts"] = arts_data.get("artifacts", [])
        elif isinstance(arts_data, list):
            result["artifacts"] = arts_data

    task_path = task_dir / "task.json"
    if task_path.exists():
        with open(task_path) as f:
            task_data = json.load(f)
        result["secrets"] = task_data.get("secrets", [])
        result["persona"] = task_data.get("persona", {})

    return result


def generate_html(
    result: dict,
    input_file: Path,
    idx: int,
    total: int,
    data_dir: Path | None,
    eval_data: dict | None = None,
) -> str:
    """Generate the full HTML page for a task result."""
    task_index = result.get("task_index", "?")
    form_id = result.get("form_id", "?")
    execution = result.get("execution", {})

    success = execution.get("success")
    termination = execution.get("termination_reason")
    total_rounds = execution.get("total_rounds")
    error_msg = execution.get("error_message")

    # Determine data sources
    task = execution.get("task", {})
    artifacts = task.get("artifacts", [])
    secrets = task.get("secrets", [])
    persona = task.get("persona", {})

    # If task data is not embedded (interactive mode), try loading from data dir
    if not artifacts and not secrets and data_dir and form_id != "?":
        loaded = load_task_data(int(form_id), data_dir)
        if loaded:
            artifacts = loaded.get("artifacts", [])
            secrets = loaded.get("secrets", [])
            persona = loaded.get("persona", {})

    # Build sections
    # -- Metadata
    meta_items = []
    if success is not None:
        status_class = "success" if success else "failure"
        status_text = "Success" if success else "Failed"
        meta_items.append(f'<span class="status-badge {status_class}">{status_text}</span>')
    if termination:
        meta_items.append(f"<strong>Termination:</strong> {escape(termination)}")
    if total_rounds is not None:
        meta_items.append(f"<strong>Rounds:</strong> {total_rounds}")
    if error_msg:
        meta_items.append(
            f'<strong>Error:</strong> <span class="error-text">{escape(error_msg)}</span>'
        )

    metadata_html = " &nbsp;|&nbsp; ".join(meta_items)

    # -- Conversation
    conversation = execution.get("conversation")
    conversation_html = ""
    if conversation and isinstance(conversation, list) and len(conversation) > 0:
        conversation_html = f"""
        <div class="section">
            <h2 class="section-title" onclick="toggleSection(this)">
                <span class="toggle-icon">&#9660;</span>
                Conversation History
                <span class="badge">{len(conversation)} messages</span>
            </h2>
            <div class="section-body">
                {render_conversation(conversation)}
            </div>
        </div>
        """

    # -- Form
    form_html = ""
    form_data = execution.get("form_submission")
    form_title = "Form Submission"
    if form_data and isinstance(form_data, dict) and len(form_data) > 0:
        form_html = render_form_fields(form_data)
    else:
        action = execution.get("action")
        if action and isinstance(action, dict):
            fill_responses = action.get("fill_responses")
            reject_reason = action.get("reject_reason")
            action_type = action.get("action_type", "")
            form_title = f"Filled Form ({escape(action_type.title())})"
            if fill_responses and isinstance(fill_responses, dict) and len(fill_responses) > 0:
                form_html = render_form_fields(fill_responses)
            elif action_type == "reject":
                form_html = f'<div class="empty-notice">Form was rejected. Reason: {escape(str(reject_reason))}</div>'
            else:
                form_html = '<div class="empty-notice">No form data available.</div>'
        else:
            form_html = '<div class="empty-notice">No form data available in this result.</div>'

    form_section = f"""
    <div class="section">
        <h2 class="section-title" onclick="toggleSection(this)">
            <span class="toggle-icon">&#9660;</span>
            {form_title}
        </h2>
        <div class="section-body">
            {form_html}
        </div>
    </div>
    """

    # -- Artifacts
    artifacts_section = ""
    if artifacts:
        artifacts_section = f"""
        <div class="section">
            <h2 class="section-title" onclick="toggleSection(this)">
                <span class="toggle-icon">&#9660;</span>
                Artifacts
                <span class="badge">{len(artifacts)}</span>
            </h2>
            <div class="section-body">
                {render_artifacts(artifacts)}
            </div>
        </div>
        """

    # -- Secrets
    secrets_section = ""
    if secrets:
        secrets_section = f"""
        <div class="section">
            <h2 class="section-title" onclick="toggleSection(this)">
                <span class="toggle-icon">&#9660;</span>
                Secrets
                <span class="badge">{len(secrets)}</span>
            </h2>
            <div class="section-body">
                {render_secrets(secrets)}
            </div>
        </div>
        """

    # -- Evaluation results
    eval_sections = ""
    if eval_data:
        eval_parts = []

        # Correctness
        correctness = eval_data.get("correctness")
        if correctness:
            accuracy = correctness.get("accuracy")
            accuracy_str = (
                f' <span class="badge">{accuracy:.1%}</span>' if accuracy is not None else ""
            )
            eval_parts.append(f"""
            <div class="section">
                <h2 class="section-title" onclick="toggleSection(this)">
                    <span class="toggle-icon">&#9660;</span>
                    Correctness Evaluation
                    {accuracy_str}
                </h2>
                <div class="section-body">
                    {render_correctness(correctness)}
                </div>
            </div>
            """)

        # Privacy - one-shot has "privacy", interactive has "form_privacy" + "conversation_privacy"
        privacy = eval_data.get("privacy")
        form_privacy = eval_data.get("form_privacy")
        conv_privacy = eval_data.get("conversation_privacy")

        if privacy:
            p_score = privacy.get("privacy_score")
            p_str = f' <span class="badge">{p_score:.1%}</span>' if p_score is not None else ""
            eval_parts.append(f"""
            <div class="section">
                <h2 class="section-title" onclick="toggleSection(this)">
                    <span class="toggle-icon">&#9660;</span>
                    Privacy Evaluation
                    {p_str}
                </h2>
                <div class="section-body">
                    {render_privacy_eval(privacy, "Privacy")}
                </div>
            </div>
            """)

        if form_privacy:
            fp_score = form_privacy.get("privacy_score")
            fp_str = f' <span class="badge">{fp_score:.1%}</span>' if fp_score is not None else ""
            eval_parts.append(f"""
            <div class="section">
                <h2 class="section-title" onclick="toggleSection(this)">
                    <span class="toggle-icon">&#9660;</span>
                    Form Privacy Evaluation
                    {fp_str}
                </h2>
                <div class="section-body">
                    {render_privacy_eval(form_privacy, "Form Privacy")}
                </div>
            </div>
            """)

        if conv_privacy:
            cp_score = conv_privacy.get("privacy_score")
            cp_str = f' <span class="badge">{cp_score:.1%}</span>' if cp_score is not None else ""
            eval_parts.append(f"""
            <div class="section">
                <h2 class="section-title" onclick="toggleSection(this)">
                    <span class="toggle-icon">&#9660;</span>
                    Conversation Privacy Evaluation
                    {cp_str}
                </h2>
                <div class="section-body">
                    {render_privacy_eval(conv_privacy, "Conversation Privacy")}
                </div>
            </div>
            """)

        # Validation
        validation_passed = eval_data.get("pydantic_validation_passed")
        validation_errors = eval_data.get("pydantic_validation_errors", [])
        if validation_passed is not None:
            v_icon = (
                '<span class="eval-pass">&#10003; Passed</span>'
                if validation_passed
                else '<span class="eval-fail">&#10007; Failed</span>'
            )
            v_errors_html = ""
            if validation_errors:
                error_items = "".join(f"<li>{escape(str(e))}</li>" for e in validation_errors)
                v_errors_html = f'<div class="validation-errors"><strong>Errors:</strong><ul>{error_items}</ul></div>'
            eval_parts.append(f"""
            <div class="section">
                <h2 class="section-title" onclick="toggleSection(this)">
                    <span class="toggle-icon">&#9660;</span>
                    Pydantic Validation
                    {v_icon}
                </h2>
                <div class="section-body">
                    {v_errors_html if v_errors_html else '<div class="empty-notice">All fields passed validation.</div>'}
                </div>
            </div>
            """)

        eval_sections = "\n".join(eval_parts)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Task #{task_index} | Form {form_id} — Form Filling Result</title>
<style>
    :root {{
        --bg: #f8f9fa;
        --card-bg: #ffffff;
        --border: #e0e0e0;
        --text: #1a1a1a;
        --text-secondary: #6b7280;
        --interviewer-bg: #e8f0fe;
        --interviewer-border: #4285f4;
        --assistant-bg: #e6f4ea;
        --assistant-border: #34a853;
        --secret-bg: #fef3e2;
        --secret-border: #f59e0b;
        --artifact-bg: #f3f0ff;
        --artifact-border: #7c3aed;
        --section-header-bg: #f1f3f5;
        --success: #16a34a;
        --failure: #dc2626;
    }}

    * {{ box-sizing: border-box; margin: 0; padding: 0; }}

    body {{
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        background: var(--bg);
        color: var(--text);
        line-height: 1.6;
        padding: 20px;
        max-width: 960px;
        margin: 0 auto;
    }}

    .page-header {{
        background: var(--card-bg);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 20px;
    }}
    .page-header h1 {{
        font-size: 1.5rem;
        margin-bottom: 8px;
    }}
    .page-header .file-info {{
        color: var(--text-secondary);
        font-size: 0.85rem;
        word-break: break-all;
    }}
    .page-header .meta {{
        margin-top: 12px;
        font-size: 0.9rem;
    }}

    .status-badge {{
        display: inline-block;
        padding: 2px 10px;
        border-radius: 12px;
        font-size: 0.85rem;
        font-weight: 600;
    }}
    .status-badge.success {{
        background: #dcfce7;
        color: var(--success);
    }}
    .status-badge.failure {{
        background: #fee2e2;
        color: var(--failure);
    }}
    .error-text {{
        color: var(--failure);
    }}

    .section {{
        background: var(--card-bg);
        border: 1px solid var(--border);
        border-radius: 12px;
        margin-bottom: 16px;
        overflow: hidden;
    }}
    .section-title {{
        font-size: 1.1rem;
        padding: 16px 20px;
        background: var(--section-header-bg);
        cursor: pointer;
        user-select: none;
        display: flex;
        align-items: center;
        gap: 8px;
    }}
    .section-title:hover {{
        background: #e4e7eb;
    }}
    .toggle-icon {{
        font-size: 0.8rem;
        transition: transform 0.2s;
    }}
    .section-title.collapsed .toggle-icon {{
        transform: rotate(-90deg);
    }}
    .section-body {{
        padding: 20px;
    }}
    .section-body.hidden {{
        display: none;
    }}
    .badge {{
        background: #dbeafe;
        color: #1d4ed8;
        font-size: 0.75rem;
        font-weight: 600;
        padding: 2px 8px;
        border-radius: 10px;
        margin-left: auto;
    }}

    /* Conversation */
    .msg {{
        border-radius: 10px;
        padding: 14px 18px;
        margin-bottom: 12px;
        border-left: 4px solid;
    }}
    .msg.interviewer {{
        background: var(--interviewer-bg);
        border-left-color: var(--interviewer-border);
    }}
    .msg.assistant {{
        background: var(--assistant-bg);
        border-left-color: var(--assistant-border);
    }}
    .msg-header {{
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 8px;
        flex-wrap: wrap;
    }}
    .msg-icon {{ font-size: 1.1rem; }}
    .msg-label {{
        font-weight: 700;
        font-size: 0.9rem;
    }}
    .msg-round {{
        font-size: 0.78rem;
        color: var(--text-secondary);
        background: rgba(0,0,0,0.06);
        padding: 1px 8px;
        border-radius: 8px;
    }}
    .msg-time {{
        font-size: 0.75rem;
        color: var(--text-secondary);
        margin-left: auto;
    }}
    .msg-content {{
        font-size: 0.92rem;
        white-space: pre-wrap;
        line-height: 1.65;
    }}

    /* Form fields */
    .form-section {{
        margin-bottom: 12px;
    }}
    .form-section-title {{
        font-weight: 700;
        font-size: 1rem;
        color: #7c3aed;
        padding: 6px 0 4px;
        border-bottom: 1px solid #e5e7eb;
        margin-bottom: 6px;
    }}
    .form-field {{
        padding: 4px 0;
        font-size: 0.92rem;
    }}
    .field-label {{
        font-weight: 600;
        color: var(--text-secondary);
    }}
    .field-value {{
        color: var(--text);
    }}
    .empty {{
        color: #9ca3af;
        font-style: italic;
    }}
    .empty-notice {{
        color: var(--text-secondary);
        font-style: italic;
        padding: 12px 0;
    }}

    /* Artifacts */
    .artifact-card {{
        border: 1px solid var(--artifact-border);
        border-radius: 10px;
        background: var(--artifact-bg);
        padding: 16px;
        margin-bottom: 12px;
    }}
    .artifact-header {{
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 8px;
    }}
    .artifact-icon {{ font-size: 1.2rem; }}
    .artifact-type {{
        font-weight: 700;
        font-size: 0.9rem;
    }}
    .artifact-index {{
        font-size: 0.78rem;
        color: var(--text-secondary);
        margin-left: auto;
    }}
    .artifact-meta {{
        display: flex;
        flex-wrap: wrap;
        gap: 6px;
        margin-bottom: 10px;
    }}
    .meta-tag {{
        background: rgba(124, 58, 237, 0.1);
        color: #5b21b6;
        font-size: 0.78rem;
        padding: 2px 8px;
        border-radius: 6px;
    }}
    .artifact-content {{
        font-size: 0.88rem;
        white-space: pre-wrap;
        line-height: 1.6;
        background: rgba(255,255,255,0.7);
        border-radius: 6px;
        padding: 12px;
        max-height: 300px;
        overflow-y: auto;
    }}
    .artifact-secrets {{
        margin-top: 10px;
        font-size: 0.82rem;
        color: #92400e;
    }}
    .secret-ref {{
        background: #fef3c7;
        color: #92400e;
        padding: 1px 6px;
        border-radius: 4px;
        font-family: monospace;
        font-size: 0.8rem;
        margin: 0 2px;
    }}

    /* Secrets */
    .secret-card {{
        border: 1px solid var(--secret-border);
        border-radius: 10px;
        background: var(--secret-bg);
        padding: 16px;
        margin-bottom: 12px;
    }}
    .secret-header {{
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 8px;
    }}
    .secret-icon {{ font-size: 1.2rem; }}
    .secret-title {{
        font-weight: 700;
        font-size: 0.95rem;
    }}
    .subtlety-badge {{
        font-size: 0.75rem;
        padding: 2px 8px;
        border-radius: 8px;
        font-weight: 600;
        margin-left: auto;
    }}
    .subtlety-obvious {{
        background: #fee2e2;
        color: #991b1b;
    }}
    .subtlety-subtle {{
        background: #fef3c7;
        color: #92400e;
    }}
    .subtlety-hidden {{
        background: #e0e7ff;
        color: #3730a3;
    }}
    .secret-field {{
        font-size: 0.85rem;
        margin-bottom: 8px;
        color: var(--text-secondary);
    }}
    .secret-field code {{
        background: rgba(0,0,0,0.06);
        padding: 1px 6px;
        border-radius: 4px;
        font-size: 0.82rem;
    }}
    .secret-detail, .secret-why, .secret-anchors {{
        font-size: 0.88rem;
        margin-top: 10px;
        padding: 10px;
        background: rgba(255,255,255,0.6);
        border-radius: 6px;
        line-height: 1.6;
    }}
    .anchor-type {{
        font-weight: 600;
        color: #92400e;
    }}

    /* Evaluation */
    .eval-metrics-bar {{
        display: flex;
        flex-wrap: wrap;
        gap: 12px;
        margin-bottom: 16px;
        padding: 12px;
        background: #f8fafc;
        border-radius: 8px;
        border: 1px solid #e2e8f0;
    }}
    .eval-metric {{
        display: flex;
        flex-direction: column;
        align-items: center;
        min-width: 70px;
    }}
    .metric-label {{
        font-size: 0.72rem;
        font-weight: 600;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }}
    .metric-value {{
        font-size: 1.1rem;
        font-weight: 700;
        color: var(--text);
    }}
    .eval-pass {{ color: var(--success); }}
    .eval-fail {{ color: var(--failure); }}
    .eval-warn {{ color: #d97706; }}

    .eval-table {{
        width: 100%;
        border-collapse: collapse;
        font-size: 0.85rem;
    }}
    .eval-table th {{
        text-align: left;
        padding: 8px 10px;
        background: #f1f5f9;
        border-bottom: 2px solid #cbd5e1;
        font-size: 0.78rem;
        text-transform: uppercase;
        letter-spacing: 0.03em;
        color: var(--text-secondary);
    }}
    .eval-table td {{
        padding: 8px 10px;
        border-bottom: 1px solid #e2e8f0;
        vertical-align: top;
    }}
    .eval-row-pass {{ background: #f0fdf4; }}
    .eval-row-fail {{ background: #fef2f2; }}
    .field-id-cell code {{
        font-size: 0.78rem;
        background: rgba(0,0,0,0.05);
        padding: 2px 6px;
        border-radius: 4px;
        word-break: break-all;
    }}
    .eval-val-cell {{
        max-width: 200px;
        overflow: hidden;
        text-overflow: ellipsis;
        font-size: 0.82rem;
    }}
    .eval-icon-cell {{
        text-align: center;
        font-size: 1rem;
    }}
    .eval-reason-cell {{
        font-size: 0.78rem;
        color: var(--text-secondary);
        max-width: 280px;
    }}

    /* Leakage */
    .leakage-section {{
        margin-top: 16px;
    }}
    .leakage-title {{
        font-size: 0.95rem;
        margin-bottom: 10px;
        color: var(--failure);
    }}
    .leakage-card {{
        border: 1px solid #fca5a5;
        border-radius: 8px;
        background: #fff5f5;
        padding: 14px;
        margin-bottom: 10px;
    }}
    .leakage-header {{
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 8px;
    }}
    .leakage-index {{
        font-weight: 700;
        font-size: 0.85rem;
    }}
    .severity-badge {{
        font-size: 0.75rem;
        padding: 2px 8px;
        border-radius: 8px;
        font-weight: 600;
    }}
    .severity-low {{ background: #fef3c7; color: #92400e; }}
    .severity-medium {{ background: #ffedd5; color: #9a3412; }}
    .severity-high {{ background: #fee2e2; color: #991b1b; }}
    .severity-unknown {{ background: #e5e7eb; color: #374151; }}
    .leakage-secret, .leakage-evidence, .leakage-elements {{
        font-size: 0.85rem;
        margin-bottom: 8px;
        line-height: 1.5;
    }}
    .leakage-evidence ul, .leakage-elements ul {{
        margin: 4px 0 0 20px;
    }}
    .leakage-analysis {{
        margin-top: 8px;
    }}
    .leakage-analysis summary {{
        cursor: pointer;
        font-size: 0.82rem;
        font-weight: 600;
        color: var(--text-secondary);
    }}
    .analysis-content {{
        font-size: 0.82rem;
        margin-top: 6px;
        padding: 10px;
        background: rgba(255,255,255,0.8);
        border-radius: 6px;
        line-height: 1.6;
        white-space: pre-wrap;
    }}
    .validation-errors {{
        font-size: 0.88rem;
    }}
    .validation-errors ul {{
        margin: 6px 0 0 20px;
    }}
</style>
</head>
<body>
    <div class="page-header">
        <h1>Task #{task_index} &nbsp;&bull;&nbsp; Form ID: {form_id}</h1>
        <div class="file-info">{escape(str(input_file))} &mdash; result {idx} of {total}</div>
        <div class="meta">{metadata_html}</div>
    </div>

    {conversation_html}
    {form_section}
    {eval_sections}
    {artifacts_section}
    {secrets_section}

<script>
function toggleSection(el) {{
    el.classList.toggle('collapsed');
    var body = el.nextElementSibling;
    body.classList.toggle('hidden');
}}
</script>
</body>
</html>"""


def main():
    parser = argparse.ArgumentParser(
        description="Visualize individual form filling task results as HTML."
    )
    parser.add_argument(
        "input_file",
        type=Path,
        help="Path to task_results.json file",
    )
    parser.add_argument(
        "--id",
        type=int,
        default=0,
        help="Index of the task result to visualize (default: 0 for the first one)",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        default=None,
        help="Output HTML file path (default: alongside the input file)",
    )
    parser.add_argument(
        "--data",
        type=Path,
        default=None,
        help="Path to task data directory (e.g., data/form-filling/tasks) for loading artifacts/secrets",
    )
    parser.add_argument(
        "--eval",
        type=Path,
        default=None,
        help="Path to eval_results.json file for showing evaluation results",
    )

    args = parser.parse_args()

    if not args.input_file.exists():
        print(f"Error: File {args.input_file} does not exist", file=sys.stderr)
        sys.exit(1)

    input_file = args.input_file

    with open(input_file, "r") as f:
        data = json.load(f)

    if not isinstance(data, list) or len(data) == 0:
        print("Error: task_results.json must contain a non-empty JSON array", file=sys.stderr)
        sys.exit(1)

    idx = args.id
    if idx < 0 or idx >= len(data):
        print(
            f"Error: --id {idx} is out of range. File contains {len(data)} result(s) (valid: 0-{len(data) - 1})",
            file=sys.stderr,
        )
        sys.exit(1)

    output_path = args.output
    if output_path is None:
        output_path = input_file.parent / f"result_{idx}.html"

    # Load eval data if provided
    eval_data = None
    if args.eval:
        if not args.eval.exists():
            print(f"Warning: Eval file {args.eval} does not exist, skipping eval", file=sys.stderr)
        else:
            result = data[idx]
            task_index = result.get("task_index", idx)
            form_id = result.get("form_id", -1)
            eval_data = load_eval_result(args.eval, task_index, form_id)
            if eval_data is None:
                print(
                    f"Warning: No matching eval result found for task_index={task_index}, form_id={form_id}",
                    file=sys.stderr,
                )

    html_content = generate_html(data[idx], input_file, idx, len(data), args.data, eval_data)

    with open(output_path, "w") as f:
        f.write(html_content)

    print(f"Generated: {output_path}")


if __name__ == "__main__":
    main()
