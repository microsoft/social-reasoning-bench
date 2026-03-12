#!/usr/bin/env python3
"""Visualize individual form filling task results as an HTML file.

Reads a task_results.json file and generates an HTML visualization for a single
task result by index. Renders mode-specific views:
- One-shot: tool call timeline + expandable message log + final form
- Interactive: conversation history + user Q&A + final form
- GUI: final form only

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


def detect_mode(execution: dict) -> str:
    """Detect visualization mode from execution data.

    Returns: "interactive", "one_shot", or "gui"
    """
    conversation = execution.get("conversation")
    if conversation and isinstance(conversation, list) and len(conversation) > 0:
        return "interactive"

    llm_calls = execution.get("llm_calls", [])
    if llm_calls and isinstance(llm_calls, list) and len(llm_calls) > 0:
        return "one_shot"

    return "gui"


# ── Tool call extraction (one-shot) ──

TOOL_ICONS = {
    "ask_user": "&#x2753;",
    "AskUser": "&#x2753;",
    "SearchEmail": "&#x1F50D;",
    "search_email": "&#x1F50D;",
    "ReadEmail": "&#x2709;",
    "read_email": "&#x2709;",
    "SearchCalendar": "&#x1F4C5;",
    "search_calendar": "&#x1F4C5;",
    "ReadCalendar": "&#x1F4C5;",
    "read_calendar": "&#x1F4C5;",
    "SendMessage": "&#x1F4AC;",
    "EndConversation": "&#x1F6D1;",
    "EndInterview": "&#x1F6D1;",
    "fill_form": "&#x2705;",
    "reject_form": "&#x274C;",
}

SEARCH_TOOL_NAMES = {
    "SearchEmail",
    "search_email",
    "ReadEmail",
    "read_email",
    "SearchCalendar",
    "search_calendar",
    "ReadCalendar",
    "read_calendar",
}


def extract_tool_calls_from_messages(messages: list) -> list[dict]:
    """Extract ordered tool call steps from an LLM message history.

    Returns list of dicts: {step_number, tool_name, arguments, result}.
    """
    steps = []
    step_num = 0

    # Build a lookup of tool results by tool_call_id
    tool_results: dict[str, str] = {}
    for msg in messages:
        if msg.get("role") == "tool":
            tid = msg.get("tool_call_id", "")
            tool_results[tid] = msg.get("content", "")

    # Walk through messages finding assistant tool_calls
    for msg in messages:
        if msg.get("role") != "assistant":
            continue
        tool_calls = msg.get("tool_calls")
        if not tool_calls:
            continue
        for tc in tool_calls:
            func = tc.get("function", {})
            tool_name = func.get("name", "unknown")
            raw_args = func.get("arguments", "{}")
            if isinstance(raw_args, str):
                try:
                    arguments = json.loads(raw_args)
                except json.JSONDecodeError:
                    arguments = {"_raw": raw_args}
            else:
                arguments = raw_args

            tid = tc.get("id", "")
            result = tool_results.get(tid, "")

            step_num += 1
            steps.append(
                {
                    "step_number": step_num,
                    "tool_name": tool_name,
                    "arguments": arguments,
                    "result": result,
                }
            )

    return steps


# ── System prompt extraction ──


def extract_system_prompts(execution: dict, mode: str) -> dict[str, str]:
    """Extract system prompt(s) from execution data.

    Returns dict with keys like 'system', 'assistant', 'interviewer'.
    """
    prompts: dict[str, str] = {}

    if mode == "one_shot":
        llm_calls = execution.get("llm_calls", [])
        if llm_calls:
            messages = llm_calls[0].get("messages", [])
            for msg in messages:
                if msg.get("role") == "system":
                    content = msg.get("content", "")
                    if isinstance(content, list):
                        content = "\n".join(
                            item.get("text", "") for item in content if isinstance(item, dict)
                        )
                    if content:
                        prompts["system"] = str(content)
                    break

    elif mode == "interactive":
        # Assistant system prompt
        assistant_ctx = execution.get("assistant_context", [])
        if assistant_ctx:
            for msg in assistant_ctx:
                if msg.get("role") == "system":
                    content = msg.get("content", "")
                    if isinstance(content, list):
                        content = "\n".join(
                            item.get("text", "") for item in content if isinstance(item, dict)
                        )
                    if content:
                        prompts["assistant"] = str(content)
                    break

        # Interviewer system prompt
        interviewer_ctx = execution.get("interviewer_context", [])
        if interviewer_ctx:
            for msg in interviewer_ctx:
                if msg.get("role") == "system":
                    content = msg.get("content", "")
                    if isinstance(content, list):
                        content = "\n".join(
                            item.get("text", "") for item in content if isinstance(item, dict)
                        )
                    if content:
                        prompts["interviewer"] = str(content)
                    break

    return prompts


def render_system_prompt(prompts: dict[str, str]) -> str:
    """Render system prompt(s) as HTML."""
    if not prompts:
        return '<div class="empty-notice">No system prompt found.</div>'

    parts = []
    if "system" in prompts:
        # One-shot mode: single prompt
        parts.append(f'<div class="system-prompt-content">{escape(prompts["system"])}</div>')
    else:
        # Interactive mode: assistant + interviewer prompts
        if "assistant" in prompts:
            parts.append(
                f'<details open><summary class="system-prompt-label">Assistant System Prompt</summary>'
                f'<div class="system-prompt-content">{escape(prompts["assistant"])}</div>'
                f"</details>"
            )
        if "interviewer" in prompts:
            parts.append(
                f'<details><summary class="system-prompt-label">Interviewer System Prompt</summary>'
                f'<div class="system-prompt-content">{escape(prompts["interviewer"])}</div>'
                f"</details>"
            )

    return "\n".join(parts)


# ── Search action helpers ──


def count_search_actions(execution: dict, mode: str) -> int:
    """Count search tool calls from execution data."""
    count = 0
    if mode == "one_shot":
        llm_calls = execution.get("llm_calls", [])
        for call in llm_calls:
            for msg in call.get("messages", []):
                if msg.get("role") == "assistant":
                    for tc in msg.get("tool_calls", []):
                        if tc.get("function", {}).get("name", "") in SEARCH_TOOL_NAMES:
                            count += 1
    elif mode == "interactive":
        for msg in execution.get("assistant_context", []):
            if msg.get("role") == "assistant":
                for tc in msg.get("tool_calls", []):
                    if tc.get("function", {}).get("name", "") in SEARCH_TOOL_NAMES:
                        count += 1
    return count


def extract_search_queries(execution: dict, mode: str) -> list[dict]:
    """Extract search tool calls with queries and results."""
    queries = []

    def _extract_from_messages(messages: list) -> None:
        tool_results: dict[str, str] = {}
        for msg in messages:
            if msg.get("role") == "tool":
                tid = msg.get("tool_call_id", "")
                tool_results[tid] = msg.get("content", "")
        for msg in messages:
            if msg.get("role") != "assistant":
                continue
            for tc in msg.get("tool_calls", []):
                func = tc.get("function", {})
                tool_name = func.get("name", "")
                if tool_name not in SEARCH_TOOL_NAMES:
                    continue
                raw_args = func.get("arguments", "{}")
                if isinstance(raw_args, str):
                    try:
                        args = json.loads(raw_args)
                    except json.JSONDecodeError:
                        args = {"_raw": raw_args}
                else:
                    args = raw_args
                tid = tc.get("id", "")
                result = tool_results.get(tid, "")
                queries.append({"tool_name": tool_name, "arguments": args, "result": result})

    if mode == "one_shot":
        for call in execution.get("llm_calls", []):
            _extract_from_messages(call.get("messages", []))
    elif mode == "interactive":
        _extract_from_messages(execution.get("assistant_context", []))

    return queries


def render_search_log(queries: list[dict]) -> str:
    """Render a collapsible log of search actions."""
    if not queries:
        return ""
    parts = [
        f'<details class="search-log"><summary>Search Actions Log ({len(queries)} calls)</summary>'
    ]
    parts.append('<div class="search-log-content">')
    for i, q in enumerate(queries):
        tool_name = q["tool_name"]
        icon = TOOL_ICONS.get(tool_name, "&#x1F527;")
        args_str = json.dumps(q["arguments"], ensure_ascii=False, indent=2)
        result_str = str(q.get("result", ""))
        parts.append(f'<div class="search-log-item">')
        parts.append(
            f'<div class="search-log-header">'
            f'<span class="step-icon">{icon}</span>'
            f'<span class="step-tool-name">{escape(tool_name)}</span>'
            f'<span class="search-log-index">#{i + 1}</span>'
            f"</div>"
        )
        parts.append(f'<div class="step-args"><code>{escape(args_str)}</code></div>')
        if result_str:
            result_preview = result_str[:200] + "..." if len(result_str) > 200 else result_str
            parts.append(
                f'<details class="step-result">'
                f"<summary>Result ({len(result_str)} chars)</summary>"
                f'<div class="step-result-content">{escape(result_str)}</div>'
                f"</details>"
            )
        parts.append("</div>")
    parts.append("</div></details>")
    return "\n".join(parts)


# ── Interactive timeline extraction ──


def extract_interactive_timeline(execution: dict) -> list[dict]:
    """Extract a unified timeline of events from interactive mode assistant_context.

    Returns ordered list of events with types: conversation, search, ask_user.
    """
    assistant_ctx = execution.get("assistant_context", [])
    conversation = execution.get("conversation", [])
    qa_history = execution.get("user_qa_history", [])

    if not assistant_ctx:
        return []

    events: list[dict] = []

    # Build tool result lookup
    tool_results: dict[str, str] = {}
    for msg in assistant_ctx:
        if msg.get("role") == "tool":
            tid = msg.get("tool_call_id", "")
            tool_results[tid] = msg.get("content", "")

    # Track conversation message index for matching round info
    conv_idx = 0
    qa_idx = 0

    # Walk through assistant_context sequentially
    for msg in assistant_ctx:
        role = msg.get("role", "")
        content = msg.get("content", "")

        # Handle content that may be a list
        if isinstance(content, list):
            text_parts = []
            for item in content:
                if isinstance(item, dict) and item.get("type") == "text":
                    text_parts.append(item.get("text", ""))
            content = "\n".join(text_parts)

        # Skip system messages and setup
        if role == "system":
            continue

        # Interviewer messages arrive as user messages with "Message from interviewer:"
        if (
            role == "user"
            and isinstance(content, str)
            and content.startswith("Message from interviewer:")
        ):
            msg_content = content[len("Message from interviewer:") :].strip()
            # Match with conversation list for round info
            round_num = "?"
            if (
                conv_idx < len(conversation)
                and conversation[conv_idx].get("from_agent") == "interviewer"
            ):
                round_num = conversation[conv_idx].get("round", "?")
                conv_idx += 1
            events.append(
                {
                    "type": "conversation",
                    "from_agent": "interviewer",
                    "content": msg_content,
                    "round": round_num,
                }
            )
            continue

        # Assistant tool calls
        if role == "assistant" and msg.get("tool_calls"):
            for tc in msg.get("tool_calls", []):
                func = tc.get("function", {})
                tool_name = func.get("name", "")
                raw_args = func.get("arguments", "{}")
                if isinstance(raw_args, str):
                    try:
                        args = json.loads(raw_args)
                    except json.JSONDecodeError:
                        args = {"_raw": raw_args}
                else:
                    args = raw_args

                tid = tc.get("id", "")
                result = tool_results.get(tid, "")

                if tool_name in SEARCH_TOOL_NAMES:
                    events.append(
                        {
                            "type": "search",
                            "tool_name": tool_name,
                            "arguments": args,
                            "result": result,
                        }
                    )
                elif tool_name in ("AskUser", "ask_user"):
                    question = args.get("question", str(args))
                    answer = result
                    # Also try to match with qa_history
                    if qa_idx < len(qa_history):
                        answer = qa_history[qa_idx].get("answer", result)
                        qa_idx += 1
                    events.append(
                        {
                            "type": "ask_user",
                            "question": question,
                            "answer": answer,
                        }
                    )
                elif tool_name == "SendMessage":
                    send_content = args.get("message", str(args))
                    thinking = args.get("thinking", "")
                    # Match with conversation list for round info
                    round_num = "?"
                    if (
                        conv_idx < len(conversation)
                        and conversation[conv_idx].get("from_agent") == "assistant"
                    ):
                        round_num = conversation[conv_idx].get("round", "?")
                        conv_idx += 1
                    events.append(
                        {
                            "type": "conversation",
                            "from_agent": "assistant",
                            "content": send_content,
                            "thinking": thinking,
                            "round": round_num,
                        }
                    )
                elif tool_name in ("EndConversation", "EndInterview"):
                    events.append(
                        {
                            "type": "end_conversation",
                            "tool_name": tool_name,
                            "arguments": args,
                        }
                    )
            continue

    return events


def render_interactive_timeline(events: list[dict]) -> str:
    """Render a unified interactive timeline as HTML."""
    if not events:
        return '<div class="empty-notice">No events found in assistant context.</div>'

    parts = ['<div class="action-timeline interactive-timeline">']
    step_num = 0

    for event in events:
        step_num += 1
        event_type = event["type"]

        if event_type == "conversation":
            agent = event["from_agent"]
            content = event["content"]
            round_num = event.get("round", "?")
            thinking = event.get("thinking", "")
            css_class = "interviewer" if agent == "interviewer" else "assistant"
            label = "Interviewer" if agent == "interviewer" else "Assistant"
            icon = "&#x1F4CB;" if agent == "interviewer" else "&#x1F464;"

            parts.append(f'<div class="timeline-step timeline-msg-step">')
            parts.append(f'<div class="msg {css_class}" style="margin:0">')
            parts.append(f'<div class="msg-header">')
            parts.append(f'<span class="step-number">{step_num}</span>')
            parts.append(f'<span class="msg-icon">{icon}</span>')
            parts.append(f'<span class="msg-label">{label}</span>')
            parts.append(f'<span class="msg-round">Round {round_num}</span>')
            parts.append("</div>")
            if thinking:
                parts.append(
                    f'<details class="thinking-block"><summary>Thinking</summary>'
                    f'<div class="thinking-content">{escape(thinking)}</div></details>'
                )
            parts.append(f'<div class="msg-content">{escape(content)}</div>')
            parts.append("</div>")
            parts.append("</div>")

        elif event_type == "search":
            tool_name = event["tool_name"]
            icon = TOOL_ICONS.get(tool_name, "&#x1F527;")
            args = event["arguments"]
            result = event.get("result", "")

            args_str = json.dumps(args, ensure_ascii=False, indent=2)
            args_short = args_str[:300] + "..." if len(args_str) > 300 else args_str
            result_str = str(result)

            parts.append(f'<div class="timeline-step search-step">')
            parts.append(f'<div class="step-header">')
            parts.append(f'<span class="step-number">{step_num}</span>')
            parts.append(f'<span class="step-icon">{icon}</span>')
            parts.append(f'<span class="step-tool-name">{escape(tool_name)}</span>')
            parts.append("</div>")
            parts.append(f'<div class="step-args"><code>{escape(args_short)}</code></div>')
            if result_str:
                parts.append(
                    f'<details class="step-result">'
                    f"<summary>Result ({len(result_str)} chars)</summary>"
                    f'<div class="step-result-content">{escape(result_str)}</div>'
                    f"</details>"
                )
            parts.append("</div>")

        elif event_type == "ask_user":
            question = event["question"]
            answer = event.get("answer", "")

            parts.append(f'<div class="timeline-step ask-user">')
            parts.append(f'<div class="step-header">')
            parts.append(f'<span class="step-number">{step_num}</span>')
            parts.append(f'<span class="step-icon">&#x2753;</span>')
            parts.append(f'<span class="step-tool-name">AskUser</span>')
            parts.append("</div>")
            parts.append(
                f'<div class="qa-question" style="margin-top:6px">'
                f'<span class="qa-label">Q:</span>'
                f'<span class="qa-content">{escape(question)}</span>'
                f"</div>"
            )
            if answer:
                parts.append(
                    f'<div class="qa-answer">'
                    f'<span class="qa-label">A:</span>'
                    f'<span class="qa-content">{escape(answer)}</span>'
                    f"</div>"
                )
            parts.append("</div>")

        elif event_type == "end_conversation":
            tool_name = event.get("tool_name", "EndConversation")
            icon = TOOL_ICONS.get(tool_name, "&#x1F6D1;")
            args = event.get("arguments", {})
            args_str = json.dumps(args, ensure_ascii=False, indent=2) if args else ""

            parts.append(f'<div class="timeline-step terminal">')
            parts.append(f'<div class="step-header">')
            parts.append(f'<span class="step-number">{step_num}</span>')
            parts.append(f'<span class="step-icon">{icon}</span>')
            parts.append(f'<span class="step-tool-name">{escape(tool_name)}</span>')
            parts.append("</div>")
            if args_str:
                parts.append(f'<div class="step-args"><code>{escape(args_str)}</code></div>')
            parts.append("</div>")

    parts.append("</div>")
    return "\n".join(parts)


# ── Rendering helpers ──


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


def render_action_sequence(llm_calls: list) -> str:
    """Render tool call timeline from one-shot LLM calls as HTML."""
    # Find the best llm_call entry (last one with parsed_action, or just the last)
    best_call = None
    for call in reversed(llm_calls):
        if call.get("parsed_action") is not None:
            best_call = call
            break
    if best_call is None and llm_calls:
        best_call = llm_calls[-1]
    if best_call is None:
        return '<div class="empty-notice">No LLM calls recorded.</div>'

    messages = best_call.get("messages", [])
    steps = extract_tool_calls_from_messages(messages)

    # Append the final action from parsed_action if not already in steps
    parsed_action = best_call.get("parsed_action")
    if parsed_action and isinstance(parsed_action, dict):
        action_type = parsed_action.get("action_type", "")
        # Check if the last step is already the terminal action
        last_tool = steps[-1]["tool_name"] if steps else ""
        if last_tool not in ("fill_form", "reject_form"):
            final_tool = "fill_form" if action_type == "fill" else "reject_form"
            final_args = {}
            if action_type == "fill":
                final_args = parsed_action.get("fill_responses", {})
            elif action_type == "reject":
                final_args = {"reason": parsed_action.get("reject_reason", "")}
            step_num = (steps[-1]["step_number"] + 1) if steps else 1
            steps.append(
                {
                    "step_number": step_num,
                    "tool_name": final_tool,
                    "arguments": final_args,
                    "result": "",
                }
            )

    if not steps:
        return '<div class="empty-notice">No tool calls found in message history.</div>'

    parts = ['<div class="action-timeline">']
    for step in steps:
        tool_name = step["tool_name"]
        icon = TOOL_ICONS.get(tool_name, "&#x1F527;")
        args = step["arguments"]
        result = step["result"]

        # Determine step CSS class
        if tool_name in ("fill_form", "reject_form"):
            step_class = "terminal"
        elif tool_name == "ask_user":
            step_class = "ask-user"
        else:
            step_class = ""

        # Format arguments for display
        args_str = json.dumps(args, ensure_ascii=False, indent=2)
        args_short = args_str[:300] + "..." if len(args_str) > 300 else args_str

        # Format result for display
        result_str = str(result)
        result_len = len(result_str)

        parts.append(f'<div class="timeline-step {step_class}">')
        parts.append(f'<div class="step-header">')
        parts.append(f'<span class="step-number">{step["step_number"]}</span>')
        parts.append(f'<span class="step-icon">{icon}</span>')
        parts.append(f'<span class="step-tool-name">{escape(tool_name)}</span>')
        parts.append("</div>")

        # Arguments
        parts.append(f'<div class="step-args"><code>{escape(args_short)}</code></div>')

        # Result (expandable)
        if result_str:
            result_preview = result_str
            parts.append(
                f'<details class="step-result">'
                f"<summary>Result ({result_len} chars)</summary>"
                f'<div class="step-result-content">{escape(result_str)}</div>'
                f"</details>"
            )

        parts.append("</div>")

    parts.append("</div>")
    return "\n".join(parts)


def render_llm_message_log(llm_calls: list) -> str:
    """Render full LLM message history as expandable message bubbles."""
    # Use the last llm_call with parsed_action, or the very last one
    best_call = None
    for call in reversed(llm_calls):
        if call.get("parsed_action") is not None:
            best_call = call
            break
    if best_call is None and llm_calls:
        best_call = llm_calls[-1]
    if best_call is None:
        return '<div class="empty-notice">No LLM calls recorded.</div>'

    messages = best_call.get("messages", [])
    if not messages:
        return '<div class="empty-notice">No messages in LLM call.</div>'

    parts = ['<div class="llm-message-log">']
    for i, msg in enumerate(messages):
        role = msg.get("role", "unknown")
        content = msg.get("content") or ""
        tool_calls = msg.get("tool_calls")

        # Map role to CSS class
        role_class = {
            "system": "system",
            "user": "user",
            "assistant": "assistant-msg",
            "tool": "tool-result",
        }.get(role, "user")

        role_label = role.upper()

        # Handle content that may be a list (multimodal messages)
        if isinstance(content, list):
            text_parts = []
            for item in content:
                if isinstance(item, dict) and item.get("type") == "text":
                    text_parts.append(item.get("text", ""))
                elif isinstance(item, dict) and item.get("type") == "image_url":
                    text_parts.append("[Image]")
            content = "\n".join(text_parts)

        # Truncate long content
        content_str = str(content)
        is_long = len(content_str) > 500
        display_content = content_str[:500] + "..." if is_long else content_str

        parts.append(f'<div class="llm-msg {role_class}">')
        parts.append(f'<div class="llm-msg-role">{role_label}</div>')

        if is_long:
            parts.append(
                f"<details>"
                f"<summary><div class='llm-msg-content'>{escape(display_content)}</div></summary>"
                f"<div class='llm-msg-content'>{escape(content_str)}</div>"
                f"</details>"
            )
        else:
            parts.append(f'<div class="llm-msg-content">{escape(display_content)}</div>')

        # Show tool calls if present
        if tool_calls:
            for tc in tool_calls:
                func = tc.get("function", {})
                tc_name = func.get("name", "?")
                tc_args = func.get("arguments", "")
                if isinstance(tc_args, str) and len(tc_args) > 200:
                    tc_args = tc_args[:200] + "..."
                parts.append(
                    f'<div class="llm-msg-tool-call">'
                    f"<strong>Tool call:</strong> <code>{escape(tc_name)}</code>"
                    f'<div class="llm-msg-tool-args"><code>{escape(str(tc_args))}</code></div>'
                    f"</div>"
                )

        parts.append("</div>")

    parts.append("</div>")
    return "\n".join(parts)


def render_user_qa_history(qa_history: list) -> str:
    """Render oracle user Q&A exchanges as HTML cards."""
    parts = ['<div class="qa-list">']
    for i, qa in enumerate(qa_history):
        question = qa.get("question", "")
        answer = qa.get("answer", "")

        parts.append(f'<div class="qa-item">')
        parts.append(
            f'<div class="qa-question">'
            f'<span class="qa-icon">&#x2753;</span>'
            f'<span class="qa-label">Q{i + 1}:</span>'
            f'<span class="qa-content">{escape(question)}</span>'
            f"</div>"
        )
        parts.append(
            f'<div class="qa-answer">'
            f'<span class="qa-icon">&#x1F4AC;</span>'
            f'<span class="qa-label">A{i + 1}:</span>'
            f'<span class="qa-content">{escape(answer)}</span>'
            f"</div>"
        )
        parts.append("</div>")

    parts.append("</div>")
    return "\n".join(parts)


# ── Evaluation rendering ──


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
            actual_short = actual
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


# ── Data loading ──


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


# ── Section compositors (mode-specific) ──


def _make_section(title: str, body: str, badge: str = "", collapsed: bool = False) -> str:
    """Helper to wrap content in a collapsible section."""
    collapsed_class = " collapsed" if collapsed else ""
    hidden_class = " hidden" if collapsed else ""
    return f"""
    <div class="section">
        <h2 class="section-title{collapsed_class}" onclick="toggleSection(this)">
            <span class="toggle-icon">&#9660;</span>
            {title}
            {badge}
        </h2>
        <div class="section-body{hidden_class}">
            {body}
        </div>
    </div>
    """


def render_form_section(execution: dict) -> str:
    """Render the final form section from execution data."""
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

    return _make_section(form_title, form_html)


def render_one_shot_sections(execution: dict, artifacts: list, secrets: list) -> str:
    """Compose all sections for one-shot mode."""
    parts = []

    # 0. System Prompt
    prompts = extract_system_prompts(execution, "one_shot")
    if prompts:
        parts.append(_make_section("System Prompt", render_system_prompt(prompts), collapsed=True))

    # 1. Tool Call Timeline
    llm_calls = execution.get("llm_calls", [])
    if llm_calls:
        timeline_html = render_action_sequence(llm_calls)
        # Count steps by looking at rendered timeline step divs
        step_count = timeline_html.count('class="timeline-step')
        badge = f'<span class="badge">{step_count} steps</span>' if step_count else ""
        parts.append(_make_section("Action Sequence", timeline_html, badge))

    # 2. User Q&A History (collapsed, shown in action sequence already)
    qa_history = execution.get("user_qa_history", [])
    if qa_history:
        qa_html = render_user_qa_history(qa_history)
        badge = f'<span class="badge">{len(qa_history)} exchanges</span>'
        parts.append(_make_section("User Q&A", qa_html, badge, collapsed=True))

    # 3. Full Message Log (collapsed by default)
    if llm_calls:
        msg_html = render_llm_message_log(llm_calls)
        parts.append(_make_section("Full Message Log", msg_html, collapsed=True))

    # 4. Final Form
    parts.append(render_form_section(execution))

    # 5. Artifacts
    if artifacts:
        badge = f'<span class="badge">{len(artifacts)}</span>'
        parts.append(_make_section("Artifacts", render_artifacts(artifacts), badge))

    # 6. Secrets
    if secrets:
        badge = f'<span class="badge">{len(secrets)}</span>'
        parts.append(_make_section("Secrets", render_secrets(secrets), badge))

    return "\n".join(parts)


def render_interactive_sections(execution: dict, artifacts: list, secrets: list) -> str:
    """Compose all sections for interactive mode."""
    parts = []

    # 0. System Prompt
    prompts = extract_system_prompts(execution, "interactive")
    if prompts:
        parts.append(_make_section("System Prompt", render_system_prompt(prompts), collapsed=True))

    # 1. Unified Action Sequence (conversation + search + ask_user interleaved)
    timeline_events = extract_interactive_timeline(execution)
    if timeline_events:
        search_count = sum(1 for e in timeline_events if e["type"] == "search")
        ask_count = sum(1 for e in timeline_events if e["type"] == "ask_user")
        badge = f'<span class="badge">{len(timeline_events)} events</span>'
        if search_count:
            badge += f' <span class="badge">{search_count} searches</span>'
        if ask_count:
            badge += f' <span class="badge">{ask_count} ask_user</span>'
        parts.append(
            _make_section("Action Sequence", render_interactive_timeline(timeline_events), badge)
        )

    # 2. Conversation (collapsed, for reference)
    conversation = execution.get("conversation", [])
    if conversation:
        conv_html = render_conversation(conversation)
        badge = f'<span class="badge">{len(conversation)} messages</span>'
        parts.append(_make_section("Conversation History", conv_html, badge, collapsed=True))

    # 3. User Q&A History (collapsed, for reference)
    qa_history = execution.get("user_qa_history", [])
    if qa_history:
        qa_html = render_user_qa_history(qa_history)
        badge = f'<span class="badge">{len(qa_history)} exchanges</span>'
        parts.append(_make_section("User Q&A (Oracle)", qa_html, badge, collapsed=True))

    # 4. Final Form
    parts.append(render_form_section(execution))

    # 5. Artifacts
    if artifacts:
        badge = f'<span class="badge">{len(artifacts)}</span>'
        parts.append(_make_section("Artifacts", render_artifacts(artifacts), badge))

    # 6. Secrets
    if secrets:
        badge = f'<span class="badge">{len(secrets)}</span>'
        parts.append(_make_section("Secrets", render_secrets(secrets), badge))

    return "\n".join(parts)


def render_gui_sections(execution: dict) -> str:
    """Compose sections for GUI mode -- only the final form."""
    return render_form_section(execution)


def render_due_diligence(
    dd: dict, search_count: int = 0, search_queries: list[dict] | None = None
) -> str:
    """Render due diligence evaluation as metrics bar + per-field table."""
    parts = []

    accuracy = dd.get("masked_field_accuracy", 0)
    precision = dd.get("ask_user_precision", 0)
    recall = dd.get("ask_user_recall", 0)
    f1 = dd.get("ask_user_f1", 0)
    total = dd.get("total_masked_fields", 0)
    findable = dd.get("total_findable", 0)
    unfindable = dd.get("total_unfindable", 0)
    ask_calls = dd.get("total_ask_user_calls", 0)

    # Metrics bar
    parts.append('<div class="eval-metrics-bar">')
    parts.append(
        f'<div class="eval-metric"><span class="metric-label">Accuracy</span>'
        f'<span class="metric-value">{accuracy:.3f}</span></div>'
    )
    parts.append(
        f'<div class="eval-metric"><span class="metric-label">Ask Precision</span>'
        f'<span class="metric-value">{precision:.3f}</span></div>'
    )
    parts.append(
        f'<div class="eval-metric"><span class="metric-label">Ask Recall</span>'
        f'<span class="metric-value">{recall:.3f}</span></div>'
    )
    parts.append(
        f'<div class="eval-metric"><span class="metric-label">Ask F1</span>'
        f'<span class="metric-value">{f1:.3f}</span></div>'
    )
    parts.append(
        f'<div class="eval-metric"><span class="metric-label">Fields</span>'
        f'<span class="metric-value">{total}</span></div>'
    )
    parts.append(
        f'<div class="eval-metric"><span class="metric-label">Findable</span>'
        f'<span class="metric-value">{findable}</span></div>'
    )
    parts.append(
        f'<div class="eval-metric"><span class="metric-label">Unfindable</span>'
        f'<span class="metric-value">{unfindable}</span></div>'
    )
    parts.append(
        f'<div class="eval-metric"><span class="metric-label">Ask Calls</span>'
        f'<span class="metric-value">{ask_calls}</span></div>'
    )
    parts.append(
        f'<div class="eval-metric"><span class="metric-label">Search Actions</span>'
        f'<span class="metric-value">{search_count}</span></div>'
    )
    parts.append("</div>")

    # Search actions log (collapsed)
    if search_queries:
        parts.append(render_search_log(search_queries))

    # Per-field table
    field_evals = dd.get("masked_field_evals", [])
    if field_evals:
        parts.append('<table class="eval-table">')
        parts.append(
            "<thead><tr><th>Field</th><th>Findability</th><th>Asked User</th>"
            "<th>Correct</th><th>Agent Answer</th><th>Expected</th></tr></thead>"
        )
        parts.append("<tbody>")
        for fe in field_evals:
            field_id = fe.get("field_id", "")
            findability = fe.get("findability", "")
            asked = fe.get("asked_user", False)
            correct = fe.get("answer_correct", False)
            agent_ans = escape(str(fe.get("agent_answer", "")))
            expected = escape(str(fe.get("expected_answer", "")))

            correct_icon = (
                '<span class="eval-pass">&#10003;</span>'
                if correct
                else '<span class="eval-fail">&#10007;</span>'
            )
            asked_icon = (
                '<span class="eval-pass">&#10003;</span>'
                if asked
                else '<span class="eval-fail">&#10007;</span>'
            )
            find_class = "eval-pass" if findability == "findable" else "eval-warn"

            agent_short = agent_ans[:120] + "..." if len(agent_ans) > 120 else agent_ans
            expected_short = expected[:120] + "..." if len(expected) > 120 else expected

            row_class = "eval-row-pass" if correct else "eval-row-fail"
            parts.append(f'<tr class="{row_class}">')
            parts.append(f'<td class="field-id-cell"><code>{escape(field_id)}</code></td>')
            parts.append(
                f'<td class="eval-icon-cell"><span class="{find_class}">{escape(findability)}</span></td>'
            )
            parts.append(f'<td class="eval-icon-cell">{asked_icon}</td>')
            parts.append(f'<td class="eval-icon-cell">{correct_icon}</td>')
            parts.append(f'<td class="eval-val-cell" title="{agent_ans}">{agent_short}</td>')
            parts.append(f'<td class="eval-val-cell" title="{expected}">{expected_short}</td>')
            parts.append("</tr>")
        parts.append("</tbody></table>")

    return "\n".join(parts)


def render_duty_of_care(dc: dict) -> str:
    """Render duty of care evaluation as metrics bar + per-field cards."""
    parts = []

    min_score = dc.get("min_score")
    total_fields = dc.get("total_fields", 0)

    # Metrics bar
    if min_score is not None:
        score_class = (
            "eval-pass" if min_score >= 0.75 else "eval-warn" if min_score >= 0.5 else "eval-fail"
        )
        score_display = f"{min_score:.3f}"
    else:
        score_class = ""
        score_display = "N/A"
    parts.append('<div class="eval-metrics-bar">')
    parts.append(
        f'<div class="eval-metric"><span class="metric-label">Min Score</span>'
        f'<span class="metric-value {score_class}">{score_display}</span></div>'
    )
    parts.append(
        f'<div class="eval-metric"><span class="metric-label">Fields Evaluated</span>'
        f'<span class="metric-value">{total_fields}</span></div>'
    )
    parts.append("</div>")

    # Per-field cards
    field_evals = dc.get("field_evaluations", [])
    for fe in field_evals:
        field_id = fe.get("field_id", "")
        field_label = fe.get("field_label", field_id)
        overall = fe.get("overall_score")
        neg_fact = fe.get("negative_fact_inclusion_score")
        framing = fe.get("framing_quality_score")
        scope = fe.get("scope_discipline_score")
        advocacy = fe.get("advocacy_effectiveness_score")
        summary = fe.get("summary", "")
        agent_answer = fe.get("agent_answer", "")

        if overall is not None:
            card_class = (
                "eval-pass" if overall >= 0.75 else "eval-warn" if overall >= 0.5 else "eval-fail"
            )
            overall_display = f"{overall:.2f}"
        else:
            card_class = ""
            overall_display = "N/A"

        agent_short = agent_answer[:300] + "..." if len(agent_answer) > 300 else agent_answer

        parts.append(f'<div class="doc-card">')
        parts.append(f'<div class="doc-card-header">')
        parts.append(f"<code>{escape(field_id)}</code>")
        parts.append(
            f'<span class="metric-value {card_class}" style="margin-left:auto">{overall_display}</span>'
        )
        parts.append("</div>")
        parts.append(f'<div class="doc-card-label">{escape(field_label)}</div>')

        # Dimension scores
        parts.append('<div class="doc-dimensions">')
        for dim_name, dim_val in [
            ("Neg. Facts", neg_fact),
            ("Framing", framing),
            ("Scope", scope),
            ("Advocacy", advocacy),
        ]:
            if dim_val is not None:
                dim_class = (
                    "eval-pass" if dim_val == 3 else "eval-warn" if dim_val == 2 else "eval-fail"
                )
                dim_display = f"{dim_val}/3"
            else:
                dim_class = ""
                dim_display = "N/A"
            parts.append(
                f'<span class="doc-dim"><span class="doc-dim-label">{dim_name}</span>'
                f'<span class="doc-dim-value {dim_class}">{dim_display}</span></span>'
            )
        parts.append("</div>")

        if summary:
            parts.append(f'<div class="doc-summary">{escape(summary)}</div>')

        if agent_answer:
            parts.append(
                f'<details class="doc-answer"><summary>Agent answer</summary>'
                f'<div class="doc-answer-content">{escape(agent_short)}</div></details>'
            )

        parts.append("</div>")

    return "\n".join(parts)


def render_eval_sections(eval_data: dict | None, execution: dict | None = None) -> str:
    """Render evaluation sections (correctness, privacy, validation, due diligence, duty of care)."""
    if not eval_data:
        return ""

    eval_parts = []

    # Correctness
    correctness = eval_data.get("correctness")
    if correctness:
        accuracy = correctness.get("accuracy")
        accuracy_str = f' <span class="badge">{accuracy:.1%}</span>' if accuracy is not None else ""
        eval_parts.append(
            _make_section(
                f"Correctness Evaluation{accuracy_str}",
                render_correctness(correctness),
            )
        )

    # Privacy -- one-shot has "privacy", interactive has "form_privacy" + "conversation_privacy"
    privacy = eval_data.get("privacy")
    form_privacy = eval_data.get("form_privacy")
    conv_privacy = eval_data.get("conversation_privacy")

    if privacy:
        p_score = privacy.get("privacy_score")
        p_str = f' <span class="badge">{p_score:.1%}</span>' if p_score is not None else ""
        eval_parts.append(
            _make_section(
                f"Privacy Evaluation{p_str}",
                render_privacy_eval(privacy, "Privacy"),
            )
        )

    if form_privacy:
        fp_score = form_privacy.get("privacy_score")
        fp_str = f' <span class="badge">{fp_score:.1%}</span>' if fp_score is not None else ""
        eval_parts.append(
            _make_section(
                f"Form Privacy Evaluation{fp_str}",
                render_privacy_eval(form_privacy, "Form Privacy"),
            )
        )

    if conv_privacy:
        cp_score = conv_privacy.get("privacy_score")
        cp_str = f' <span class="badge">{cp_score:.1%}</span>' if cp_score is not None else ""
        eval_parts.append(
            _make_section(
                f"Conversation Privacy Evaluation{cp_str}",
                render_privacy_eval(conv_privacy, "Conversation Privacy"),
            )
        )

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
        body = (
            v_errors_html
            if v_errors_html
            else '<div class="empty-notice">All fields passed validation.</div>'
        )
        eval_parts.append(_make_section(f"Pydantic Validation {v_icon}", body))

    # Due Diligence
    due_diligence = eval_data.get("due_diligence")
    if due_diligence:
        dd_acc = due_diligence.get("masked_field_accuracy")
        dd_str = f' <span class="badge">{dd_acc:.1%}</span>' if dd_acc is not None else ""
        search_count = 0
        search_queries: list[dict] = []
        if execution:
            mode = detect_mode(execution)
            search_count = count_search_actions(execution, mode)
            search_queries = extract_search_queries(execution, mode)
        eval_parts.append(
            _make_section(
                f"Due Diligence{dd_str}",
                render_due_diligence(
                    due_diligence,
                    search_count=search_count,
                    search_queries=search_queries,
                ),
            )
        )

    # Duty of Care
    duty_of_care = eval_data.get("duty_of_care")
    if duty_of_care:
        dc_min = duty_of_care.get("min_score")
        dc_str = f' <span class="badge">{dc_min:.1%}</span>' if dc_min is not None else ""
        eval_parts.append(
            _make_section(
                f"Duty of Care{dc_str}",
                render_duty_of_care(duty_of_care),
            )
        )

    return "\n".join(eval_parts)


# ── Main HTML generation ──


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

    # Detect mode
    mode = detect_mode(execution)
    mode_labels = {"one_shot": "One-Shot", "interactive": "Interactive", "gui": "GUI"}
    mode_css = {"one_shot": "one-shot", "interactive": "interactive", "gui": "gui"}

    # Load artifacts/secrets
    task = execution.get("task", {})
    artifacts = task.get("artifacts", [])
    secrets = task.get("secrets", [])

    if not artifacts and not secrets and data_dir and form_id != "?":
        loaded = load_task_data(int(form_id), data_dir)
        if loaded:
            artifacts = loaded.get("artifacts", [])
            secrets = loaded.get("secrets", [])

    # Build metadata header
    meta_items = [f'<span class="mode-badge {mode_css[mode]}">{mode_labels[mode]}</span>']
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

    # Mode-specific sections
    if mode == "one_shot":
        mode_html = render_one_shot_sections(execution, artifacts, secrets)
    elif mode == "interactive":
        mode_html = render_interactive_sections(execution, artifacts, secrets)
    else:
        mode_html = render_gui_sections(execution)

    # Evaluation sections
    eval_html = render_eval_sections(eval_data, execution)

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

    /* Mode badge */
    .mode-badge {{
        display: inline-block;
        padding: 2px 10px;
        border-radius: 12px;
        font-size: 0.85rem;
        font-weight: 600;
    }}
    .mode-badge.one-shot {{ background: #dbeafe; color: #1d4ed8; }}
    .mode-badge.interactive {{ background: #dcfce7; color: #16a34a; }}
    .mode-badge.gui {{ background: #f3e8ff; color: #7c3aed; }}

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

    /* Action Timeline (one-shot) */
    .action-timeline {{
        position: relative;
        padding-left: 30px;
    }}
    .action-timeline::before {{
        content: '';
        position: absolute;
        left: 15px;
        top: 0;
        bottom: 0;
        width: 2px;
        background: var(--border);
    }}
    .timeline-step {{
        position: relative;
        margin-bottom: 16px;
        padding: 12px 16px;
        background: var(--card-bg);
        border: 1px solid var(--border);
        border-radius: 8px;
    }}
    .timeline-step::before {{
        content: '';
        position: absolute;
        left: -23px;
        top: 18px;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        background: #4285f4;
        border: 2px solid white;
    }}
    .timeline-step.terminal::before {{
        background: #34a853;
    }}
    .timeline-step.ask-user::before {{
        background: #f59e0b;
    }}
    .step-header {{
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 6px;
    }}
    .step-number {{
        background: #e8f0fe;
        color: #1d4ed8;
        font-weight: 700;
        font-size: 0.75rem;
        width: 24px;
        height: 24px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
    }}
    .step-icon {{ font-size: 1.1rem; }}
    .step-tool-name {{
        font-weight: 700;
        font-size: 0.9rem;
        font-family: monospace;
    }}
    .step-args {{
        font-size: 0.82rem;
        padding: 6px 10px;
        background: #f8fafc;
        border-radius: 6px;
        margin-bottom: 6px;
        word-break: break-all;
        overflow-x: auto;
    }}
    .step-args code {{
        font-size: 0.8rem;
        white-space: pre-wrap;
    }}
    .step-result summary {{
        cursor: pointer;
        font-size: 0.82rem;
        font-weight: 600;
        color: var(--text-secondary);
    }}
    .step-result-content {{
        font-size: 0.82rem;
        padding: 10px;
        background: #f8fafc;
        border-radius: 6px;
        margin-top: 6px;
        max-height: 300px;
        overflow-y: auto;
        white-space: pre-wrap;
        line-height: 1.5;
    }}

    /* LLM Message Log */
    .llm-message-log {{
        max-height: 600px;
        overflow-y: auto;
    }}
    .llm-msg {{
        border-radius: 8px;
        padding: 10px 14px;
        margin-bottom: 8px;
        font-size: 0.85rem;
    }}
    .llm-msg.system {{ background: #f1f3f5; border-left: 3px solid #9ca3af; }}
    .llm-msg.user {{ background: #e8f0fe; border-left: 3px solid #4285f4; }}
    .llm-msg.assistant-msg {{ background: #e6f4ea; border-left: 3px solid #34a853; }}
    .llm-msg.tool-result {{ background: #f3f0ff; border-left: 3px solid #7c3aed; }}
    .llm-msg-role {{
        font-weight: 700;
        font-size: 0.78rem;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        margin-bottom: 4px;
        color: var(--text-secondary);
    }}
    .llm-msg-content {{
        white-space: pre-wrap;
        line-height: 1.5;
        word-break: break-word;
    }}
    .llm-msg-tool-call {{
        margin-top: 8px;
        padding: 6px 10px;
        background: rgba(0,0,0,0.04);
        border-radius: 6px;
        font-size: 0.82rem;
    }}
    .llm-msg-tool-args {{
        margin-top: 4px;
        max-height: 150px;
        overflow-y: auto;
    }}
    .llm-msg-tool-args code {{
        font-size: 0.78rem;
        white-space: pre-wrap;
        word-break: break-all;
    }}

    /* User Q&A History */
    .qa-list {{ }}
    .qa-item {{
        margin-bottom: 12px;
        padding: 12px;
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        background: #fffbeb;
    }}
    .qa-question, .qa-answer {{
        display: flex;
        gap: 8px;
        margin-bottom: 6px;
        font-size: 0.9rem;
        line-height: 1.5;
    }}
    .qa-icon {{ font-size: 1rem; flex-shrink: 0; }}
    .qa-label {{
        font-weight: 700;
        min-width: 32px;
        flex-shrink: 0;
    }}
    .qa-content {{ flex: 1; white-space: pre-wrap; }}

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

    /* Duty of Care cards */
    .doc-card {{
        border: 1px solid var(--border);
        border-radius: 8px;
        padding: 14px;
        margin-bottom: 12px;
        background: #fafbfc;
    }}
    .doc-card-header {{
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 6px;
    }}
    .doc-card-header code {{
        font-size: 0.82rem;
        background: rgba(0,0,0,0.05);
        padding: 2px 6px;
        border-radius: 4px;
    }}
    .doc-card-label {{
        font-weight: 600;
        font-size: 0.9rem;
        margin-bottom: 8px;
        color: var(--text-secondary);
    }}
    .doc-dimensions {{
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        margin-bottom: 10px;
    }}
    .doc-dim {{
        display: flex;
        flex-direction: column;
        align-items: center;
        min-width: 60px;
        padding: 4px 8px;
        background: #f1f5f9;
        border-radius: 6px;
    }}
    .doc-dim-label {{
        font-size: 0.7rem;
        font-weight: 600;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 0.03em;
    }}
    .doc-dim-value {{
        font-size: 0.9rem;
        font-weight: 700;
    }}
    .doc-summary {{
        font-size: 0.85rem;
        line-height: 1.5;
        margin-bottom: 8px;
        padding: 8px;
        background: rgba(255,255,255,0.8);
        border-radius: 6px;
    }}
    .doc-answer summary {{
        cursor: pointer;
        font-size: 0.82rem;
        font-weight: 600;
        color: var(--text-secondary);
    }}
    .doc-answer-content {{
        font-size: 0.82rem;
        padding: 10px;
        background: rgba(255,255,255,0.8);
        border-radius: 6px;
        margin-top: 6px;
        white-space: pre-wrap;
        line-height: 1.5;
        max-height: 200px;
        overflow-y: auto;
    }}

    /* System Prompt */
    .system-prompt-content {{
        font-family: 'SF Mono', 'Consolas', 'Monaco', monospace;
        font-size: 0.82rem;
        background: #f1f3f5;
        border: 1px solid #d1d5db;
        border-radius: 8px;
        padding: 16px;
        white-space: pre-wrap;
        line-height: 1.6;
        max-height: 500px;
        overflow-y: auto;
        word-break: break-word;
    }}
    .system-prompt-label {{
        cursor: pointer;
        font-weight: 700;
        font-size: 0.9rem;
        color: var(--text-secondary);
        padding: 8px 0;
    }}

    /* Interactive Timeline */
    .interactive-timeline .timeline-msg-step {{
        border: none;
        padding: 0;
        background: transparent;
    }}
    .interactive-timeline .timeline-msg-step::before {{
        background: #9ca3af;
    }}
    .interactive-timeline .timeline-msg-step .msg {{
        border-radius: 8px;
    }}
    .search-step::before {{
        background: #7c3aed !important;
    }}
    .thinking-block {{
        margin-bottom: 8px;
    }}
    .thinking-block summary {{
        cursor: pointer;
        font-size: 0.82rem;
        font-weight: 600;
        color: var(--text-secondary);
    }}
    .thinking-content {{
        font-size: 0.82rem;
        padding: 10px;
        background: rgba(0,0,0,0.04);
        border-radius: 6px;
        margin-top: 4px;
        white-space: pre-wrap;
        line-height: 1.5;
        max-height: 200px;
        overflow-y: auto;
    }}

    /* Search Log */
    .search-log {{
        margin-top: 16px;
    }}
    .search-log > summary {{
        cursor: pointer;
        font-size: 0.9rem;
        font-weight: 600;
        color: var(--text-secondary);
        padding: 8px 0;
    }}
    .search-log-content {{
        padding-top: 8px;
    }}
    .search-log-item {{
        border: 1px solid var(--border);
        border-radius: 8px;
        padding: 10px 14px;
        margin-bottom: 8px;
        background: #fafbfc;
    }}
    .search-log-header {{
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 6px;
    }}
    .search-log-index {{
        font-size: 0.75rem;
        color: var(--text-secondary);
        margin-left: auto;
    }}
</style>
</head>
<body>
    <div class="page-header">
        <h1>Task #{task_index} &nbsp;&bull;&nbsp; Form ID: {form_id}</h1>
        <div class="file-info">{escape(str(input_file))} &mdash; result {idx} of {total}</div>
        <div class="meta">{metadata_html}</div>
    </div>

    {mode_html}
    {eval_html}

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
    parser.add_argument(
        "--all",
        action="store_true",
        help="Generate HTML for all results and save to a visuals/ subfolder",
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

    # Resolve eval path once (auto-detect or explicit)
    eval_path = args.eval
    if eval_path is None:
        auto_eval = input_file.parent / "eval_results.json"
        if auto_eval.exists():
            eval_path = auto_eval
    if eval_path and not eval_path.exists():
        print(f"Warning: Eval file {eval_path} does not exist, skipping eval", file=sys.stderr)
        eval_path = None

    if args.all:
        # Generate HTML for all results
        visuals_dir = input_file.parent / "visuals"
        visuals_dir.mkdir(exist_ok=True)

        for idx in range(len(data)):
            eval_data = None
            if eval_path:
                result = data[idx]
                task_index = result.get("task_index", idx)
                form_id = result.get("form_id", -1)
                eval_data = load_eval_result(eval_path, task_index, form_id)

            html_content = generate_html(
                data[idx], input_file, idx, len(data), args.data, eval_data
            )
            out = visuals_dir / f"result_{idx}.html"
            with open(out, "w") as f:
                f.write(html_content)

        print(f"Generated {len(data)} files in {visuals_dir}/")
    else:
        # Single result mode
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

        eval_data = None
        if eval_path:
            result = data[idx]
            task_index = result.get("task_index", idx)
            form_id = result.get("form_id", -1)
            eval_data = load_eval_result(eval_path, task_index, form_id)
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
