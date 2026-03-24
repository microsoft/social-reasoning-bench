#!/usr/bin/env python3
"""Multi-task form filling result viewer.

Generates a single HTML page with a task selector sidebar and detailed
per-task view. All task data is embedded as JSON; rendering happens
client-side via JavaScript.

Usage:
    python -m sage_benchmark.form_filling.visualization_multi <task_results.json>
    python -m sage_benchmark.form_filling.visualization_multi task_results.json --eval eval_results.json --data data/form-filling/tasks
"""

import argparse
import base64
import json
import sys
from pathlib import Path

from sage_benchmark.form_filling.visualization_result import (
    SEARCH_TOOL_NAMES,
    TOOL_ICONS,
    detect_mode,
    extract_system_prompts,
    extract_tool_calls_from_messages,
    load_eval_result,
    load_task_data,
)

# ── Timeline extraction helpers ──


def _parse_content(content) -> str:
    """Normalize message content (may be str or list of dicts) to a string."""
    if isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, dict) and item.get("type") == "text":
                parts.append(item.get("text", ""))
        return "\n".join(parts)
    return str(content) if content else ""


def _parse_tool_args(raw_args) -> dict:
    if isinstance(raw_args, str):
        try:
            return json.loads(raw_args)
        except json.JSONDecodeError:
            return {"_raw": raw_args}
    return raw_args if isinstance(raw_args, dict) else {}


def _extract_timeline(
    context: list[dict],
    conversation: list[dict],
    qa_history: list[dict],
    owner_agent: str,
    incoming_prefix: str,
    incoming_agent: str,
) -> list[dict]:
    """Generic timeline extraction from an agent's context.

    Args:
        context: The agent's message context (assistant_context or interviewer_context).
        conversation: The high-level conversation array for round matching.
        qa_history: The user Q&A history (only relevant for assistant).
        owner_agent: "assistant" or "interviewer" — who owns this context.
        incoming_prefix: Prefix for incoming messages, e.g. "Message from interviewer:".
        incoming_agent: The agent name for incoming messages, e.g. "interviewer".
    """
    if not context:
        return []

    events: list[dict] = []

    # Build tool result lookup
    tool_results: dict[str, str] = {}
    for msg in context:
        if msg.get("role") == "tool":
            tid = msg.get("tool_call_id", "")
            tool_results[tid] = msg.get("content", "")

    conv_idx = 0
    qa_idx = 0

    for msg in context:
        role = msg.get("role", "")
        content = _parse_content(msg.get("content", ""))

        if role == "system":
            continue

        # Incoming messages from the other agent arrive as "user" role with a prefix.
        # In social reasoning mode, ToM intent history may be prepended before the prefix.
        if role == "user" and incoming_prefix in content:
            prefix_pos = content.index(incoming_prefix)
            msg_content = content[prefix_pos + len(incoming_prefix) :].strip()
            round_num = "?"
            if (
                conv_idx < len(conversation)
                and conversation[conv_idx].get("from_agent") == incoming_agent
            ):
                round_num = conversation[conv_idx].get("round", "?")
                conv_idx += 1
            events.append(
                {
                    "type": "conversation",
                    "from_agent": incoming_agent,
                    "content": msg_content,
                    "round": round_num,
                }
            )
            continue

        # Tool calls from this agent
        if role == "assistant" and msg.get("tool_calls"):
            for tc in msg.get("tool_calls", []):
                func = tc.get("function", {})
                tool_name = func.get("name", "")
                args = _parse_tool_args(func.get("arguments", "{}"))
                tid = tc.get("id", "")
                result = tool_results.get(tid, "")

                if tool_name == "SendMessage":
                    send_content = args.get("message", str(args))
                    round_num = "?"
                    if (
                        conv_idx < len(conversation)
                        and conversation[conv_idx].get("from_agent") == owner_agent
                    ):
                        round_num = conversation[conv_idx].get("round", "?")
                        conv_idx += 1
                    ev: dict = {
                        "type": "conversation",
                        "from_agent": owner_agent,
                        "content": send_content,
                        "round": round_num,
                    }
                    for key in ("thinking", "task_related_thinking", "theory_of_mind_thinking"):
                        if args.get(key):
                            ev[key] = args[key]
                    events.append(ev)
                elif tool_name in ("EndConversation", "EndInterview"):
                    events.append(
                        {
                            "type": "end_conversation",
                            "tool_name": tool_name,
                            "arguments": args,
                        }
                    )
                elif tool_name in ("AskUser", "ask_user"):
                    question = args.get("question", str(args))
                    answer = result
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
                elif tool_name in SEARCH_TOOL_NAMES:
                    events.append(
                        {
                            "type": "search",
                            "tool_name": tool_name,
                            "arguments": args,
                            "result": result,
                        }
                    )
            continue

        # Direct assistant content with no tool_calls — this is a message sent
        # by the owner agent (common format where content IS the message, without
        # wrapping in a SendMessage tool call).
        if role == "assistant" and content and not msg.get("tool_calls"):
            round_num = "?"
            if (
                conv_idx < len(conversation)
                and conversation[conv_idx].get("from_agent") == owner_agent
            ):
                round_num = conversation[conv_idx].get("round", "?")
                conv_idx += 1
            ev: dict = {
                "type": "conversation",
                "from_agent": owner_agent,
                "content": content,
                "round": round_num,
            }
            for key in ("thinking", "task_related_thinking", "theory_of_mind_thinking"):
                if msg.get(key):
                    ev[key] = msg[key]
            events.append(ev)
            continue

    return events


def extract_assistant_timeline(execution: dict) -> list[dict]:
    """Extract timeline events from assistant_context."""
    return _extract_timeline(
        context=execution.get("assistant_context", []),
        conversation=execution.get("conversation", []),
        qa_history=execution.get("user_qa_history", []),
        owner_agent="assistant",
        incoming_prefix="Message from interviewer:",
        incoming_agent="interviewer",
    )


def extract_interviewer_timeline(execution: dict) -> list[dict]:
    """Extract timeline events from interviewer_context."""
    return _extract_timeline(
        context=execution.get("interviewer_context", []),
        conversation=execution.get("conversation", []),
        qa_history=[],
        owner_agent="interviewer",
        incoming_prefix="Message from assistant:",
        incoming_agent="assistant",
    )


# ── Data preparation ──


def _extract_eval_summary(eval_data: dict | None) -> dict:
    """Extract top-level metric scores from evaluation data."""
    if not eval_data:
        return {}
    summary: dict = {}

    correctness = eval_data.get("correctness")
    if correctness:
        summary["accuracy"] = correctness.get("accuracy")

    # One-shot has "privacy", interactive has "form_privacy"/"conversation_privacy"
    # For the sidebar, show conversation_privacy for interactive (leakage in conversation
    # is the primary concern), fall back to form_privacy, then one-shot privacy.
    privacy = eval_data.get("privacy")
    form_privacy = eval_data.get("form_privacy")
    conv_privacy = eval_data.get("conversation_privacy")
    if conv_privacy:
        summary["privacy_score"] = conv_privacy.get("privacy_score")
    elif privacy:
        summary["privacy_score"] = privacy.get("privacy_score")
    elif form_privacy:
        summary["privacy_score"] = form_privacy.get("privacy_score")
    if conv_privacy:
        summary["conversation_privacy_score"] = conv_privacy.get("privacy_score")

    dd = eval_data.get("due_diligence")
    if dd:
        summary["due_diligence_accuracy"] = dd.get("masked_field_accuracy")

    doc = eval_data.get("duty_of_care")
    if doc:
        summary["duty_of_care_min_score"] = doc.get("min_score")

    return summary


def prepare_task_data(
    results: list[dict],
    eval_path: Path | None,
    data_dir: Path | None,
) -> list[dict]:
    """Prepare all task data for JSON embedding."""
    tasks = []

    for idx, result in enumerate(results):
        task_index = result.get("task_index", idx)
        form_id = result.get("form_id", "?")
        execution = result.get("execution", {})

        mode = detect_mode(execution)
        prompts = extract_system_prompts(execution, mode)

        # Timelines
        assistant_timeline: list[dict] = []
        interviewer_timeline: list[dict] = []
        one_shot_steps: list[dict] = []

        if mode == "interactive":
            assistant_timeline = extract_assistant_timeline(execution)
            interviewer_timeline = extract_interviewer_timeline(execution)
        elif mode == "one_shot":
            llm_calls = execution.get("llm_calls", [])
            if llm_calls:
                best_call = None
                for call in reversed(llm_calls):
                    if call.get("parsed_action") is not None:
                        best_call = call
                        break
                if best_call is None:
                    best_call = llm_calls[-1]
                one_shot_steps = extract_tool_calls_from_messages(best_call.get("messages", []))
                # Append final action
                parsed = best_call.get("parsed_action") or {}
                action_type = parsed.get("action_type", "")
                if action_type == "fill":
                    one_shot_steps.append(
                        {
                            "step_number": len(one_shot_steps) + 1,
                            "tool_name": "fill_form",
                            "arguments": parsed.get("fill_responses", {}),
                            "result": "",
                        }
                    )
                elif action_type == "reject":
                    one_shot_steps.append(
                        {
                            "step_number": len(one_shot_steps) + 1,
                            "tool_name": "reject_form",
                            "arguments": {"reason": parsed.get("reject_reason", "")},
                            "result": "",
                        }
                    )

        # Form submission
        form_submission = execution.get("form_submission")
        if not form_submission:
            action = execution.get("action", {})
            if action:
                form_submission = action.get("fill_responses")

        # Conversation
        conversation = execution.get("conversation", [])

        # Eval data
        eval_data = None
        if eval_path:
            eval_data = load_eval_result(
                eval_path, task_index, int(form_id) if form_id != "?" else -1
            )

        eval_summary = _extract_eval_summary(eval_data)

        # Task data (artifacts, secrets)
        task_info = execution.get("task", {})
        artifacts = task_info.get("artifacts", [])
        secrets = task_info.get("secrets", [])
        if not artifacts and not secrets and data_dir and form_id != "?":
            loaded = load_task_data(int(form_id), data_dir)
            if loaded:
                artifacts = loaded.get("artifacts", [])
                secrets = loaded.get("secrets", [])

        # Form image — always base64-embed by default so HTML is portable
        form_image_data = None
        if data_dir and form_id != "?":
            img_path = data_dir / f"form_{form_id}" / f"image_{form_id}.png"
            if img_path.exists():
                with open(img_path, "rb") as f:
                    b64 = base64.b64encode(f.read()).decode("ascii")
                form_image_data = f"data:image/png;base64,{b64}"

        tasks.append(
            {
                "task_index": task_index,
                "form_id": form_id,
                "mode": mode,
                "success": execution.get("success"),
                "termination_reason": execution.get("termination_reason"),
                "total_rounds": execution.get("total_rounds"),
                "error_message": execution.get("error_message"),
                "prompts": prompts,
                "assistant_timeline": assistant_timeline,
                "interviewer_timeline": interviewer_timeline,
                "one_shot_steps": one_shot_steps,
                "form_submission": form_submission,
                "conversation": conversation,
                "eval_summary": eval_summary,
                "eval_detail": eval_data,
                "form_image": form_image_data,
                "artifacts": artifacts,
                "secrets": secrets,
            }
        )

    return tasks


# ── HTML generation ──

TOOL_ICONS_JS = json.dumps(TOOL_ICONS)


def generate_multi_html(
    tasks_data: list[dict], input_file: Path, run_meta: dict | None = None
) -> str:
    """Generate a single-page multi-task viewer HTML."""
    run_meta = run_meta or {}
    tasks_json = json.dumps(tasks_data, ensure_ascii=False, default=str)

    # Build metadata badges
    meta_badges = ""
    if run_meta.get("assistant_model"):
        model = run_meta["assistant_model"]
        meta_badges += f'<span class="px-1.5 py-0.5 text-xs rounded bg-green-100 text-green-700">{model}</span>'
    mode = run_meta.get("execution_mode", "")
    if mode:
        mode_label = "One-Shot" if mode == "one-shot" else "Interactive"
        meta_badges += f'<span class="px-1.5 py-0.5 text-xs rounded bg-blue-100 text-blue-700">{mode_label}</span>'
    if run_meta.get("is_malicious"):
        meta_badges += (
            '<span class="px-1.5 py-0.5 text-xs rounded bg-red-100 text-red-700">Malicious</span>'
        )
    if run_meta.get("is_social"):
        meta_badges += '<span class="px-1.5 py-0.5 text-xs rounded bg-purple-100 text-purple-700">Social Reasoning</span>'
    meta_html = f'<div class="mt-1 flex flex-wrap gap-1">{meta_badges}</div>' if meta_badges else ""

    return f"""<!DOCTYPE html>
<html lang="en" class="light">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Form Filling Benchmark Viewer</title>
<script src="https://cdn.tailwindcss.com"></script>
<script>tailwind.config = {{ darkMode: 'class' }}</script>
<style>
    /* Custom styles for timeline, messages, eval */
    .timeline-connector {{ position: relative; padding-left: 28px; }}
    .timeline-connector::before {{
        content: ''; position: absolute; left: 12px; top: 0; bottom: 0;
        width: 2px; background: #d1d5db;
    }}
    .timeline-event {{ position: relative; margin-bottom: 12px; }}
    .timeline-event::before {{
        content: ''; position: absolute; left: -22px; top: 8px;
        width: 10px; height: 10px; border-radius: 50%; background: #9ca3af;
        border: 2px solid white; z-index: 1;
    }}
    .timeline-event.msg-assistant::before {{ background: #34a853; }}
    .timeline-event.msg-interviewer::before {{ background: #4285f4; }}
    .timeline-event.search-event::before {{ background: #7c3aed; }}
    .timeline-event.ask-user-event::before {{ background: #f59e0b; }}
    .timeline-event.end-event::before {{ background: #dc2626; }}

    .task-row {{ cursor: pointer; transition: background 0.1s; }}
    .task-row:hover {{ background: rgba(59, 130, 246, 0.08); }}
    .task-row.selected {{ background: rgba(59, 130, 246, 0.15); font-weight: 600; }}

    .metric-pill {{
        display: inline-block; padding: 1px 6px; border-radius: 8px;
        font-size: 0.7rem; font-weight: 600; min-width: 36px; text-align: center;
    }}
    .metric-green {{ background: #dcfce7; color: #16a34a; }}
    .metric-yellow {{ background: #fef9c3; color: #a16207; }}
    .metric-red {{ background: #fee2e2; color: #dc2626; }}
    .metric-gray {{ background: #f3f4f6; color: #9ca3af; }}

    .eval-table {{ width: 100%; border-collapse: collapse; font-size: 0.85rem; }}
    .eval-table th {{ text-align: left; padding: 6px 8px; background: #f9fafb; border-bottom: 2px solid #e5e7eb; }}
    .eval-table td {{ padding: 6px 8px; border-bottom: 1px solid #f3f4f6; }}
    .eval-table tr.pass {{ background: #f0fdf4; }}
    .eval-table tr.fail {{ background: #fef2f2; }}

    details > summary {{ cursor: pointer; }}
    details > summary::-webkit-details-marker {{ display: none; }}
    details > summary::before {{ content: '\\25B6 '; font-size: 0.7rem; margin-right: 4px; }}
    details[open] > summary::before {{ content: '\\25BC '; }}

    .secret-card {{ border-left: 3px solid #f59e0b; background: #fffbeb; }}
    .artifact-card {{ border-left: 3px solid #7c3aed; background: #faf5ff; }}

    .section-card {{ background: white; border: 1px solid #e5e7eb; border-radius: 8px; overflow: hidden; }}
    .section-header {{
        padding: 10px 16px; background: #f9fafb; cursor: pointer;
        display: flex; align-items: center; gap: 8px; font-weight: 600;
        user-select: none; font-size: 0.95rem;
    }}
    .section-header:hover {{ background: #f3f4f6; }}
    .section-body {{ padding: 16px; }}
    .section-body.collapsed {{ display: none; }}

    .msg-bubble {{
        padding: 8px 12px; border-radius: 8px; margin-bottom: 6px;
        font-size: 0.9rem; white-space: pre-wrap; word-break: break-word;
    }}
    .msg-bubble.assistant {{ background: #e6f4ea; border-left: 3px solid #34a853; }}
    .msg-bubble.interviewer {{ background: #e8f0fe; border-left: 3px solid #4285f4; }}

    #sidebar {{ scrollbar-width: thin; }}
    .thinking-block {{ font-size: 0.8rem; color: #6b7280; margin-top: 4px; padding: 4px 8px; background: #f9fafb; border-radius: 4px; }}
    .tom-block {{ font-size: 0.8rem; color: #7c3aed; margin-top: 4px; padding: 4px 8px; background: #f5f3ff; border-radius: 4px; }}
</style>
</head>
<body class="bg-gray-50 text-gray-900 min-h-screen flex">

<!-- Sidebar -->
<aside id="sidebar" class="w-80 bg-white border-r border-gray-200 fixed left-0 top-0 h-screen flex flex-col z-10">
    <div class="p-4 border-b border-gray-200">
        <h1 class="text-lg font-bold">Form Filling Viewer</h1>
        <div class="text-xs text-gray-500 mt-1 truncate" title="{input_file}">{input_file.name}</div>
        {meta_html}
        <div id="stats-bar" class="mt-2 text-xs text-gray-600"></div>
    </div>
    <div class="px-3 py-2 border-b border-gray-100">
        <input id="filter-input" type="text" placeholder="Filter by form ID..."
               class="w-full px-2 py-1 text-sm border border-gray-300 rounded focus:outline-none focus:ring-1 focus:ring-blue-400">
    </div>
    <div id="task-table-wrap" class="flex-1 overflow-y-auto">
        <table class="w-full text-xs">
            <thead class="sticky top-0 bg-gray-50 z-10">
                <tr>
                    <th class="text-left px-2 py-1.5 font-semibold">#</th>
                    <th class="text-left px-2 py-1.5 font-semibold">Form</th>
                    <th class="text-center px-1 py-1.5 font-semibold" title="Correctness">Acc</th>
                    <th class="text-center px-1 py-1.5 font-semibold" title="Privacy">Prv</th>
                    <th class="text-center px-1 py-1.5 font-semibold" title="Due Diligence">DD</th>
                    <th class="text-center px-1 py-1.5 font-semibold" title="Duty of Care">DoC</th>
                </tr>
            </thead>
            <tbody id="task-table-body"></tbody>
        </table>
    </div>
</aside>

<!-- Main content -->
<main id="main-content" class="ml-80 flex-1 p-6 space-y-5 max-w-6xl">
    <div id="no-task-msg" class="text-center text-gray-400 mt-20">Select a task from the sidebar</div>

    <!-- Task header -->
    <div id="task-header" class="hidden">
        <div class="flex items-center gap-3 mb-2">
            <h2 id="task-title" class="text-xl font-bold"></h2>
            <span id="mode-badge" class="px-2 py-0.5 rounded-full text-xs font-semibold"></span>
            <span id="status-badge" class="px-2 py-0.5 rounded-full text-xs font-semibold"></span>
        </div>
        <div id="task-meta" class="text-sm text-gray-600"></div>
    </div>

    <!-- Task Overview: prompts side by side -->
    <div id="overview-section" class="hidden">
        <div class="section-card">
            <div class="section-header" onclick="toggleSectionBody(this)">
                <span class="toggle-arrow">&#9660;</span> Task Overview
            </div>
            <div class="section-body">
                <div id="prompts-grid" class="grid md:grid-cols-2 gap-4"></div>
                <div id="form-image-wrap" class="mt-4"></div>
            </div>
        </div>
    </div>

    <!-- Trajectories -->
    <div id="trajectories-section" class="hidden">
        <div class="section-card">
            <div class="section-header" onclick="toggleSectionBody(this)">
                <span class="toggle-arrow">&#9660;</span> Trajectories
                <span id="traj-badge" class="ml-auto text-xs bg-blue-100 text-blue-700 px-2 py-0.5 rounded-full"></span>
            </div>
            <div class="section-body p-0">
                <div id="traj-aligned" class="max-h-[800px] overflow-y-auto p-4">
                    <div class="grid grid-cols-2 gap-0 mb-2 sticky top-0 bg-white z-10 pb-2 border-b">
                        <h3 class="font-semibold text-sm text-green-700">&#x1F464; Assistant</h3>
                        <h3 class="font-semibold text-sm text-blue-700">&#x1F4CB; Interviewer</h3>
                    </div>
                    <div id="traj-rounds"></div>
                </div>
            </div>
        </div>
    </div>

    <!-- One-shot timeline (full width) -->
    <div id="oneshot-section" class="hidden">
        <div class="section-card">
            <div class="section-header" onclick="toggleSectionBody(this)">
                <span class="toggle-arrow">&#9660;</span> Action Sequence
                <span id="oneshot-badge" class="ml-auto text-xs bg-blue-100 text-blue-700 px-2 py-0.5 rounded-full"></span>
            </div>
            <div class="section-body">
                <div id="oneshot-timeline" class="timeline-connector max-h-[600px] overflow-y-auto pr-2"></div>
            </div>
        </div>
    </div>

    <!-- Form Submission -->
    <div id="form-section" class="hidden">
        <div class="section-card">
            <div class="section-header" onclick="toggleSectionBody(this)">
                <span class="toggle-arrow">&#9660;</span> Form Submission
            </div>
            <div class="section-body">
                <div id="form-fields"></div>
            </div>
        </div>
    </div>

    <!-- Artifacts & Secrets -->
    <div id="artifacts-section" class="hidden">
        <div class="section-card">
            <div class="section-header" onclick="toggleSectionBody(this)">
                <span class="toggle-arrow">&#9660;</span> Artifacts
                <span id="artifacts-badge" class="ml-auto text-xs bg-purple-100 text-purple-700 px-2 py-0.5 rounded-full"></span>
            </div>
            <div class="section-body collapsed">
                <div id="artifacts-content"></div>
            </div>
        </div>
    </div>

    <div id="secrets-section" class="hidden">
        <div class="section-card">
            <div class="section-header" onclick="toggleSectionBody(this)">
                <span class="toggle-arrow">&#9660;</span> Secrets
                <span id="secrets-badge" class="ml-auto text-xs bg-yellow-100 text-yellow-700 px-2 py-0.5 rounded-full"></span>
            </div>
            <div class="section-body collapsed">
                <div id="secrets-content"></div>
            </div>
        </div>
    </div>

    <!-- Eval sections -->
    <div id="eval-section" class="hidden space-y-4">
        <div id="eval-correctness" class="section-card hidden">
            <div class="section-header" onclick="toggleSectionBody(this)">
                <span class="toggle-arrow">&#9660;</span> Correctness Evaluation
                <span id="eval-acc-badge" class="ml-auto text-xs bg-blue-100 text-blue-700 px-2 py-0.5 rounded-full"></span>
            </div>
            <div class="section-body collapsed"><div id="eval-correctness-body"></div></div>
        </div>
        <div id="eval-privacy" class="section-card hidden">
            <div class="section-header" onclick="toggleSectionBody(this)">
                <span class="toggle-arrow">&#9660;</span> Privacy Evaluation
                <span id="eval-prv-badge" class="ml-auto text-xs bg-blue-100 text-blue-700 px-2 py-0.5 rounded-full"></span>
            </div>
            <div class="section-body collapsed"><div id="eval-privacy-body"></div></div>
        </div>
        <div id="eval-dd" class="section-card hidden">
            <div class="section-header" onclick="toggleSectionBody(this)">
                <span class="toggle-arrow">&#9660;</span> Due Diligence
                <span id="eval-dd-badge" class="ml-auto text-xs bg-blue-100 text-blue-700 px-2 py-0.5 rounded-full"></span>
            </div>
            <div class="section-body collapsed"><div id="eval-dd-body"></div></div>
        </div>
        <div id="eval-doc" class="section-card hidden">
            <div class="section-header" onclick="toggleSectionBody(this)">
                <span class="toggle-arrow">&#9660;</span> Duty of Care
                <span id="eval-doc-badge" class="ml-auto text-xs bg-blue-100 text-blue-700 px-2 py-0.5 rounded-full"></span>
            </div>
            <div class="section-body collapsed"><div id="eval-doc-body"></div></div>
        </div>
    </div>
</main>

<script>
// ── Data ──
const TASKS = {tasks_json};
const TOOL_ICONS = {TOOL_ICONS_JS};
let currentIdx = -1;

// ── Utilities ──
function esc(text) {{
    if (text == null) return '';
    const d = document.createElement('div');
    d.textContent = String(text);
    return d.innerHTML.replace(/\\n/g, '<br>');
}}

function metricPill(value, label, strict) {{
    if (value == null || value === undefined) return `<span class="metric-pill metric-gray" title="${{label}}">—</span>`;
    const v = typeof value === 'number' ? value : parseFloat(value);
    if (isNaN(v)) return `<span class="metric-pill metric-gray" title="${{label}}">—</span>`;
    // strict mode (privacy): only 100% is green, any leakage is bad
    const cls = strict
        ? (v >= 1.0 ? 'metric-green' : v >= 0.8 ? 'metric-yellow' : 'metric-red')
        : (v >= 0.8 ? 'metric-green' : v >= 0.5 ? 'metric-yellow' : 'metric-red');
    return `<span class="metric-pill ${{cls}}" title="${{label}}: ${{(v*100).toFixed(1)}}%">${{(v*100).toFixed(0)}}%</span>`;
}}

function toggleSectionBody(header) {{
    const body = header.nextElementSibling;
    const arrow = header.querySelector('.toggle-arrow');
    if (body.classList.contains('collapsed')) {{
        body.classList.remove('collapsed');
        if (arrow) arrow.innerHTML = '&#9660;';
    }} else {{
        body.classList.add('collapsed');
        if (arrow) arrow.innerHTML = '&#9654;';
    }}
}}

function show(id) {{ document.getElementById(id).classList.remove('hidden'); }}
function hide(id) {{ document.getElementById(id).classList.add('hidden'); }}

// ── Populate sidebar ──
function populateTaskTable() {{
    const tbody = document.getElementById('task-table-body');
    let html = '';
    TASKS.forEach((t, i) => {{
        const es = t.eval_summary || {{}};
        html += `<tr class="task-row border-b border-gray-100" data-index="${{i}}" data-form="${{t.form_id}}">
            <td class="px-2 py-1.5">${{i}}</td>
            <td class="px-2 py-1.5">${{t.form_id}}</td>
            <td class="px-1 py-1.5 text-center">${{metricPill(es.accuracy, 'Accuracy')}}</td>
            <td class="px-1 py-1.5 text-center">${{metricPill(es.privacy_score, 'Privacy', true)}}</td>
            <td class="px-1 py-1.5 text-center">${{metricPill(es.due_diligence_accuracy, 'Due Diligence')}}</td>
            <td class="px-1 py-1.5 text-center">${{metricPill(es.duty_of_care_min_score, 'Duty of Care')}}</td>
        </tr>`;
    }});
    tbody.innerHTML = html;

    // Stats
    const modes = {{}};
    TASKS.forEach(t => {{ modes[t.mode] = (modes[t.mode] || 0) + 1; }});
    const modeStr = Object.entries(modes).map(([m,c]) => `${{c}} ${{m}}`).join(', ');
    document.getElementById('stats-bar').textContent = `${{TASKS.length}} tasks (${{modeStr}})`;

    // Click handler
    tbody.addEventListener('click', e => {{
        const row = e.target.closest('.task-row');
        if (row) renderTask(parseInt(row.dataset.index));
    }});

    // Filter
    document.getElementById('filter-input').addEventListener('input', e => {{
        const q = e.target.value.toLowerCase();
        tbody.querySelectorAll('.task-row').forEach(row => {{
            const form = row.dataset.form.toLowerCase();
            row.style.display = form.includes(q) || q === '' ? '' : 'none';
        }});
    }});
}}

// ── Render task ──
function renderTask(idx) {{
    if (idx < 0 || idx >= TASKS.length) return;
    currentIdx = idx;
    const t = TASKS[idx];

    // Update sidebar selection
    document.querySelectorAll('.task-row').forEach(r => r.classList.remove('selected'));
    const row = document.querySelector(`.task-row[data-index="${{idx}}"]`);
    if (row) {{
        row.classList.add('selected');
        row.scrollIntoView({{ block: 'nearest' }});
    }}

    hide('no-task-msg');
    show('task-header');
    show('overview-section');

    // Header
    document.getElementById('task-title').textContent = `Task #${{t.task_index}} — Form ${{t.form_id}}`;
    const mb = document.getElementById('mode-badge');
    mb.textContent = t.mode === 'one_shot' ? 'One-Shot' : t.mode === 'interactive' ? 'Interactive' : 'GUI';
    mb.className = 'px-2 py-0.5 rounded-full text-xs font-semibold ' +
        (t.mode === 'interactive' ? 'bg-green-100 text-green-700' :
         t.mode === 'one_shot' ? 'bg-blue-100 text-blue-700' : 'bg-purple-100 text-purple-700');

    const sb = document.getElementById('status-badge');
    if (t.success !== null && t.success !== undefined) {{
        sb.textContent = t.success ? 'Success' : 'Failed';
        sb.className = 'px-2 py-0.5 rounded-full text-xs font-semibold ' +
            (t.success ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700');
        sb.classList.remove('hidden');
    }} else {{
        sb.classList.add('hidden');
    }}

    const metaParts = [];
    if (t.total_rounds != null) metaParts.push(`Rounds: ${{t.total_rounds}}`);
    if (t.termination_reason) metaParts.push(`Termination: ${{t.termination_reason}}`);
    if (t.error_message) metaParts.push(`<span class="text-red-600">Error: ${{esc(t.error_message)}}</span>`);
    document.getElementById('task-meta').innerHTML = metaParts.join(' &nbsp;|&nbsp; ');

    // Overview: prompts side by side
    renderPrompts(t);

    // Form image
    renderFormImage(t);

    // Trajectories
    if (t.mode === 'interactive') {{
        show('trajectories-section');
        hide('oneshot-section');
        renderInteractiveTrajectories(t);
    }} else if (t.mode === 'one_shot') {{
        hide('trajectories-section');
        show('oneshot-section');
        renderOneShotTimeline(t);
    }} else {{
        hide('trajectories-section');
        hide('oneshot-section');
    }}

    // Form submission
    if (t.form_submission && Object.keys(t.form_submission).length > 0) {{
        show('form-section');
        document.getElementById('form-fields').innerHTML = renderFormFields(t.form_submission);
    }} else {{
        hide('form-section');
    }}

    // Artifacts & secrets
    if (t.artifacts && t.artifacts.length > 0) {{
        show('artifacts-section');
        document.getElementById('artifacts-badge').textContent = `${{t.artifacts.length}}`;
        document.getElementById('artifacts-content').innerHTML = renderArtifacts(t.artifacts);
    }} else {{
        hide('artifacts-section');
    }}

    if (t.secrets && t.secrets.length > 0) {{
        show('secrets-section');
        document.getElementById('secrets-badge').textContent = `${{t.secrets.length}}`;
        document.getElementById('secrets-content').innerHTML = renderSecrets(t.secrets);
    }} else {{
        hide('secrets-section');
    }}

    // Eval
    renderEval(t);
}}

// ── Prompts side by side ──
function renderPrompts(t) {{
    const grid = document.getElementById('prompts-grid');
    const p = t.prompts || {{}};

    if (p.system) {{
        // One-shot: single prompt full width
        grid.className = 'grid grid-cols-1 gap-4';
        grid.innerHTML = `<details>
            <summary class="font-semibold text-sm text-gray-700">System Prompt</summary>
            <div class="mt-2 p-3 bg-gray-50 rounded text-xs max-h-60 overflow-y-auto whitespace-pre-wrap">${{esc(p.system)}}</div>
        </details>`;
    }} else {{
        grid.className = 'grid md:grid-cols-2 gap-4';
        let html = '';
        if (p.assistant) {{
            html += `<details>
                <summary class="font-semibold text-sm text-green-700">&#x1F464; Assistant Prompt</summary>
                <div class="mt-2 p-3 bg-green-50 rounded text-xs max-h-60 overflow-y-auto whitespace-pre-wrap">${{esc(p.assistant)}}</div>
            </details>`;
        }}
        if (p.interviewer) {{
            html += `<details>
                <summary class="font-semibold text-sm text-blue-700">&#x1F4CB; Interviewer Prompt</summary>
                <div class="mt-2 p-3 bg-blue-50 rounded text-xs max-h-60 overflow-y-auto whitespace-pre-wrap">${{esc(p.interviewer)}}</div>
            </details>`;
        }}
        grid.innerHTML = html || '<div class="text-gray-400 text-sm">No prompts available</div>';
    }}
}}

// ── Form image ──
function renderFormImage(t) {{
    const wrap = document.getElementById('form-image-wrap');
    if (t.form_image) {{
        wrap.innerHTML = `<details>
            <summary class="font-semibold text-sm text-gray-700">Form Screenshot</summary>
            <div class="mt-2"><img src="${{esc(t.form_image)}}" alt="Form ${{t.form_id}}"
                class="max-h-96 rounded shadow border border-gray-200"
                onerror="this.parentElement.innerHTML='<span class=\\'text-gray-400 text-sm\\'>Image failed to load</span>'"></div>
        </details>`;
    }} else {{
        wrap.innerHTML = '';
    }}
}}

// ── Timeline event rendering ──
function renderTimelineEvent(ev, stepNum) {{
    let cls = '';
    let html = '';

    if (ev.type === 'conversation') {{
        const isAssistant = ev.from_agent === 'assistant';
        cls = isAssistant ? 'msg-assistant' : 'msg-interviewer';
        const label = isAssistant ? 'Assistant' : 'Interviewer';
        const bubbleCls = isAssistant ? 'assistant' : 'interviewer';
        html = `<div class="flex items-center gap-2 mb-1">
            <span class="text-xs font-semibold text-gray-500">#${{stepNum}}</span>
            <span class="text-xs font-semibold">${{label}}</span>
            <span class="text-xs text-gray-400">Round ${{ev.round != null && ev.round !== '?' ? Number(ev.round) + 1 : '?'}}</span>
        </div>`;
        if (ev.thinking) {{
            html += `<details class="thinking-block mb-1"><summary class="text-xs">Thinking</summary><div class="text-xs whitespace-pre-wrap">${{esc(ev.thinking)}}</div></details>`;
        }}
        if (ev.task_related_thinking) {{
            html += `<details class="thinking-block mb-1"><summary class="text-xs">Task Reasoning</summary><div class="text-xs whitespace-pre-wrap">${{esc(ev.task_related_thinking)}}</div></details>`;
        }}
        if (ev.theory_of_mind_thinking) {{
            html += `<details class="tom-block mb-1"><summary class="text-xs">Theory of Mind</summary><div class="text-xs whitespace-pre-wrap">${{esc(ev.theory_of_mind_thinking)}}</div></details>`;
        }}
        html += `<div class="msg-bubble ${{bubbleCls}}">${{esc(ev.content)}}</div>`;

    }} else if (ev.type === 'search') {{
        cls = 'search-event';
        const icon = TOOL_ICONS[ev.tool_name] || '&#x1F527;';
        const argsStr = JSON.stringify(ev.arguments || {{}}, null, 2);
        const resultStr = String(ev.result || '');
        html = `<div class="flex items-center gap-2 mb-1">
            <span class="text-xs font-semibold text-gray-500">#${{stepNum}}</span>
            <span>${{icon}}</span>
            <span class="text-xs font-semibold text-purple-700">${{esc(ev.tool_name)}}</span>
        </div>
        <div class="text-xs bg-gray-50 p-2 rounded mb-1"><code>${{esc(argsStr.length > 300 ? argsStr.slice(0,300) + '...' : argsStr)}}</code></div>`;
        if (resultStr) {{
            html += `<details class="text-xs"><summary>Result (${{resultStr.length}} chars)</summary>
                <div class="bg-gray-50 p-2 rounded mt-1 max-h-40 overflow-y-auto whitespace-pre-wrap">${{esc(resultStr)}}</div></details>`;
        }}

    }} else if (ev.type === 'ask_user') {{
        cls = 'ask-user-event';
        html = `<div class="flex items-center gap-2 mb-1">
            <span class="text-xs font-semibold text-gray-500">#${{stepNum}}</span>
            <span>&#x2753;</span>
            <span class="text-xs font-semibold text-yellow-700">AskUser</span>
        </div>
        <div class="text-sm"><span class="font-semibold">Q:</span> ${{esc(ev.question)}}</div>`;
        if (ev.answer) {{
            html += `<div class="text-sm text-green-800"><span class="font-semibold">A:</span> ${{esc(ev.answer)}}</div>`;
        }}

    }} else if (ev.type === 'end_conversation') {{
        cls = 'end-event';
        const icon = TOOL_ICONS[ev.tool_name] || '&#x1F6D1;';
        html = `<div class="flex items-center gap-2">
            <span class="text-xs font-semibold text-gray-500">#${{stepNum}}</span>
            <span>${{icon}}</span>
            <span class="text-xs font-semibold text-red-600">${{esc(ev.tool_name || 'EndConversation')}}</span>
        </div>`;
        if (ev.arguments) {{
            html += `<div class="text-xs bg-gray-50 p-2 rounded mt-1"><code>${{esc(JSON.stringify(ev.arguments, null, 2))}}</code></div>`;
        }}
    }}

    return `<div class="timeline-event ${{cls}}">${{html}}</div>`;
}}

function renderTimeline(events) {{
    if (!events || events.length === 0) return '<div class="text-gray-400 text-sm">No events</div>';
    return events.map((ev, i) => renderTimelineEvent(ev, i + 1)).join('');
}}

// ── Interactive trajectories (round-aligned) ──
function renderInteractiveTrajectories(t) {{
    const aEvents = (t.assistant_timeline || []).filter(e =>
        e.type !== 'conversation' || e.from_agent === 'assistant');
    const iEvents = (t.interviewer_timeline || []).filter(e =>
        e.type !== 'conversation' || e.from_agent === 'interviewer');
    document.getElementById('traj-badge').textContent = `${{aEvents.length}} asst / ${{iEvents.length}} intv events`;

    // Group events by round. Non-conversation events attach to the last seen round.
    function groupByRound(events) {{
        const groups = {{}};
        let lastRound = 0;
        for (const ev of events) {{
            let r = (ev.type === 'conversation' && ev.round != null && ev.round !== '?')
                ? Number(ev.round) + 1 : lastRound;
            if (ev.type === 'conversation') lastRound = r;
            if (!groups[r]) groups[r] = [];
            groups[r].push(ev);
        }}
        return groups;
    }}
    const aGroups = groupByRound(aEvents);
    const iGroups = groupByRound(iEvents);
    const allRounds = [...new Set([...Object.keys(aGroups), ...Object.keys(iGroups)])]
        .map(Number).sort((a, b) => a - b);

    let html = '';
    for (const r of allRounds) {{
        const aHtml = (aGroups[r] || []).map((ev, i) => renderTimelineEvent(ev, i + 1)).join('');
        const iHtml = (iGroups[r] || []).map((ev, i) => renderTimelineEvent(ev, i + 1)).join('');
        html += `<div class="grid grid-cols-2 gap-4 mb-3 pb-3 border-b border-gray-100">
            <div class="timeline-connector">${{aHtml || '<div class="text-gray-300 text-xs italic">—</div>'}}</div>
            <div class="timeline-connector">${{iHtml || '<div class="text-gray-300 text-xs italic">—</div>'}}</div>
        </div>`;
    }}
    document.getElementById('traj-rounds').innerHTML = html || '<div class="text-gray-400 text-sm">No events</div>';
}}

// ── One-shot timeline ──
function renderOneShotTimeline(t) {{
    const steps = t.one_shot_steps || [];
    document.getElementById('oneshot-badge').textContent = `${{steps.length}} steps`;
    if (steps.length === 0) {{
        document.getElementById('oneshot-timeline').innerHTML = '<div class="text-gray-400 text-sm">No steps recorded</div>';
        return;
    }}
    let html = '';
    steps.forEach((s, i) => {{
        const icon = TOOL_ICONS[s.tool_name] || '&#x1F527;';
        const isTerminal = s.tool_name === 'fill_form' || s.tool_name === 'reject_form';
        const cls = isTerminal ? 'end-event' : (TOOL_ICONS[s.tool_name] ? 'search-event' : '');
        const argsStr = typeof s.arguments === 'object' ? JSON.stringify(s.arguments, null, 2) : String(s.arguments || '');
        const resultStr = String(s.result || '');

        let inner = `<div class="flex items-center gap-2 mb-1">
            <span class="text-xs font-semibold text-gray-500">#${{s.step_number || i+1}}</span>
            <span>${{icon}}</span>
            <span class="text-xs font-semibold">${{esc(s.tool_name)}}</span>
        </div>`;
        if (argsStr && argsStr !== '{{}}' && argsStr !== '""') {{
            inner += `<div class="text-xs bg-gray-50 p-2 rounded mb-1"><code>${{esc(argsStr.length > 500 ? argsStr.slice(0,500) + '...' : argsStr)}}</code></div>`;
        }}
        if (resultStr) {{
            inner += `<details class="text-xs"><summary>Result (${{resultStr.length}} chars)</summary>
                <div class="bg-gray-50 p-2 rounded mt-1 max-h-40 overflow-y-auto whitespace-pre-wrap">${{esc(resultStr)}}</div></details>`;
        }}
        html += `<div class="timeline-event ${{cls}}">${{inner}}</div>`;
    }});
    document.getElementById('oneshot-timeline').innerHTML = html;
}}

// ── Form fields rendering ──
function renderFormFields(data, depth) {{
    depth = depth || 0;
    if (!data || typeof data !== 'object') return '';
    let html = '';
    for (const [key, value] of Object.entries(data)) {{
        const label = key.replace(/_/g, ' ').replace(/\\b\\w/g, c => c.toUpperCase());
        if (value && typeof value === 'object' && !Array.isArray(value)) {{
            html += `<div style="margin-left:${{depth*20}}px" class="mt-2">
                <div class="font-semibold text-sm text-gray-700">${{esc(label)}}</div>
                ${{renderFormFields(value, depth+1)}}
            </div>`;
        }} else {{
            const display = (value != null && value !== '') ? esc(String(value)) : '<span class="text-gray-400 italic">empty</span>';
            html += `<div style="margin-left:${{depth*20}}px" class="py-0.5 text-sm">
                <span class="text-gray-600 font-medium">${{esc(label)}}:</span> <span>${{display}}</span>
            </div>`;
        }}
    }}
    return html;
}}

// ── Artifacts ──
function renderArtifacts(artifacts) {{
    return artifacts.map((art, i) => {{
        const typeIcons = {{ email: '&#x2709;', note: '&#x1F4DD;', calendar: '&#x1F4C5;', text: '&#x1F4C4;' }};
        const icon = typeIcons[art.artifact_type] || '&#x1F4CE;';
        const meta = art.metadata || {{}};
        const metaParts = [];
        if (meta.date) metaParts.push(`Date: ${{esc(meta.date)}}`);
        if (meta.sender) metaParts.push(`From: ${{esc(meta.sender)}}`);
        if (meta.recipient) metaParts.push(`To: ${{esc(meta.recipient)}}`);
        if (meta.subject) metaParts.push(`Subject: ${{esc(meta.subject)}}`);
        if (meta.title) metaParts.push(`Title: ${{esc(meta.title)}}`);

        return `<div class="artifact-card p-3 rounded mb-2">
            <div class="flex items-center gap-2 mb-1">
                <span>${{icon}}</span>
                <span class="font-semibold text-sm">${{esc((art.artifact_type||'').charAt(0).toUpperCase() + (art.artifact_type||'').slice(1))}}</span>
                <span class="text-xs text-gray-400">#${{i}}</span>
            </div>
            ${{metaParts.length ? `<div class="text-xs text-gray-500 mb-1">${{metaParts.join(' &middot; ')}}</div>` : ''}}
            <details class="text-xs"><summary>Content</summary>
                <div class="whitespace-pre-wrap mt-1 bg-white p-2 rounded max-h-40 overflow-y-auto">${{esc(art.content)}}</div>
            </details>
        </div>`;
    }}).join('');
}}

// ── Secrets ──
function renderSecrets(secrets) {{
    return secrets.map((s, i) => {{
        return `<div class="secret-card p-3 rounded mb-2">
            <div class="flex items-center gap-2 mb-1">
                <span>&#x1F512;</span>
                <span class="font-semibold text-sm">Secret #${{i}}</span>
                ${{s.subtlety_level ? `<span class="text-xs bg-yellow-100 text-yellow-700 px-1 rounded">${{esc(s.subtlety_level)}}</span>` : ''}}
            </div>
            ${{s.question_id ? `<div class="text-xs text-gray-500 mb-1">Field: <code>${{esc(s.question_id)}}</code></div>` : ''}}
            <div class="text-sm">${{esc(s.detail_content)}}</div>
            ${{s.why_sensitive ? `<div class="text-xs text-gray-500 mt-1"><strong>Why sensitive:</strong> ${{esc(s.why_sensitive)}}</div>` : ''}}
        </div>`;
    }}).join('');
}}

// ── Eval rendering ──
function renderEval(t) {{
    const ed = t.eval_detail;
    if (!ed) {{
        hide('eval-section');
        return;
    }}
    show('eval-section');

    // Correctness
    const corr = ed.correctness;
    if (corr) {{
        show('eval-correctness');
        const acc = corr.accuracy;
        document.getElementById('eval-acc-badge').textContent = acc != null ? (acc*100).toFixed(1) + '%' : '';
        let html = `<div class="grid grid-cols-4 gap-3 mb-4 text-center">
            <div><div class="text-lg font-bold">${{corr.exact_matches ?? '—'}}</div><div class="text-xs text-gray-500">Exact</div></div>
            <div><div class="text-lg font-bold">${{corr.semantic_matches ?? '—'}}</div><div class="text-xs text-gray-500">Semantic</div></div>
            <div><div class="text-lg font-bold">${{corr.grounded_matches ?? '—'}}</div><div class="text-xs text-gray-500">Grounded</div></div>
            <div><div class="text-lg font-bold">${{corr.total_fields ?? '—'}}</div><div class="text-xs text-gray-500">Total</div></div>
        </div>`;
        if (corr.field_evaluations && corr.field_evaluations.length > 0) {{
            html += `<table class="eval-table"><thead><tr>
                <th>Field</th><th>Expected</th><th>Actual</th><th>EM</th><th>Sem</th><th>Grnd</th>
            </tr></thead><tbody>`;
            corr.field_evaluations.forEach(fe => {{
                const cls = (fe.exact_match || fe.semantic_match || fe.is_grounded) ? 'pass' : 'fail';
                html += `<tr class="${{cls}}">
                    <td class="font-medium">${{esc(fe.field_id)}}</td>
                    <td class="max-w-[200px] truncate" title="${{esc(fe.expected_value)}}">${{esc(fe.expected_value)}}</td>
                    <td class="max-w-[200px] truncate" title="${{esc(fe.actual_value)}}">${{esc(fe.actual_value)}}</td>
                    <td>${{fe.exact_match ? '&#10003;' : '&#10007;'}}</td>
                    <td>${{fe.semantic_match ? '&#10003;' : '&#10007;'}}</td>
                    <td>${{fe.is_grounded ? '&#10003;' : '&#10007;'}}</td>
                </tr>`;
            }});
            html += '</tbody></table>';
        }}
        document.getElementById('eval-correctness-body').innerHTML = html;
    }} else {{
        hide('eval-correctness');
    }}

    // Privacy
    const prv = ed.privacy || ed.form_privacy;
    const convPrv = ed.conversation_privacy;
    if (prv || convPrv) {{
        show('eval-privacy');
        const score = (prv || convPrv || {{}}).privacy_score;
        document.getElementById('eval-prv-badge').textContent = score != null ? (score*100).toFixed(1) + '%' : '';
        let html = '';

        [['Form Privacy', prv || ed.privacy], ['Conversation Privacy', convPrv]].forEach(([label, p]) => {{
            if (!p) return;
            html += `<div class="mb-3"><div class="font-semibold text-sm mb-1">${{label}}</div>`;
            html += `<div class="grid grid-cols-3 gap-3 mb-2 text-center text-sm">
                <div><span class="font-bold">${{p.privacy_score != null ? (p.privacy_score*100).toFixed(1)+'%' : '—'}}</span><div class="text-xs text-gray-500">Score</div></div>
                <div><span class="font-bold">${{(p.secrets_checked || []).length}}</span><div class="text-xs text-gray-500">Checked</div></div>
                <div><span class="font-bold text-red-600">${{(p.secrets_leaked || p.secrets_leaked_in_conversation || []).length}}</span><div class="text-xs text-gray-500">Leaked</div></div>
            </div>`;
            if (p.leakage_details && p.leakage_details.length > 0) {{
                html += '<div class="space-y-2">';
                p.leakage_details.forEach((ld, i) => {{
                    const secretText = ld.secret_content || '';
                    const preview = secretText.length > 150 ? secretText.slice(0, 150) + '...' : secretText;
                    html += `<div class="text-xs p-2 bg-red-50 rounded">
                        <div class="font-semibold mb-1">Leak #${{i}}</div>
                        <div class="mb-1"><strong>Secret:</strong> ${{esc(preview)}}</div>
                        ${{ld.reasoning ? `<details><summary>Reasoning</summary><div class="mt-1 whitespace-pre-wrap">${{esc(ld.reasoning)}}</div></details>` : ''}}
                        ${{ld.evidence ? `<details><summary>Evidence</summary><div class="mt-1 whitespace-pre-wrap">${{esc(typeof ld.evidence === 'string' ? ld.evidence : JSON.stringify(ld.evidence, null, 2))}}</div></details>` : ''}}
                    </div>`;
                }});
                html += '</div>';
            }}
            html += '</div>';
        }});
        document.getElementById('eval-privacy-body').innerHTML = html;
    }} else {{
        hide('eval-privacy');
    }}

    // Due Diligence
    const dd = ed.due_diligence;
    if (dd) {{
        show('eval-dd');
        const ddAcc = dd.masked_field_accuracy;
        document.getElementById('eval-dd-badge').textContent = ddAcc != null ? (ddAcc*100).toFixed(1) + '%' : '';
        let html = `<div class="grid grid-cols-4 gap-3 mb-4 text-center text-sm">
            <div><span class="font-bold">${{dd.total_masked_fields ?? '—'}}</span><div class="text-xs text-gray-500">Masked</div></div>
            <div><span class="font-bold">${{dd.total_findable ?? '—'}}</span><div class="text-xs text-gray-500">Findable</div></div>
            <div><span class="font-bold">${{dd.total_unfindable ?? '—'}}</span><div class="text-xs text-gray-500">Unfindable</div></div>
            <div><span class="font-bold">${{dd.total_ask_user_calls ?? '—'}}</span><div class="text-xs text-gray-500">Ask User</div></div>
        </div>`;
        if (dd.ask_user_precision != null) {{
            html += `<div class="grid grid-cols-3 gap-3 mb-4 text-center text-sm">
                <div><span class="font-bold">${{(dd.ask_user_precision*100).toFixed(1)}}%</span><div class="text-xs text-gray-500">Precision</div></div>
                <div><span class="font-bold">${{(dd.ask_user_recall*100).toFixed(1)}}%</span><div class="text-xs text-gray-500">Recall</div></div>
                <div><span class="font-bold">${{(dd.ask_user_f1*100).toFixed(1)}}%</span><div class="text-xs text-gray-500">F1</div></div>
            </div>`;
        }}
        if (dd.masked_field_evals && dd.masked_field_evals.length > 0) {{
            html += `<table class="eval-table"><thead><tr>
                <th>Field</th><th>Findability</th><th>Asked User</th><th>Correct</th>
            </tr></thead><tbody>`;
            dd.masked_field_evals.forEach(mfe => {{
                const cls = mfe.answer_correct ? 'pass' : 'fail';
                html += `<tr class="${{cls}}">
                    <td class="font-medium">${{esc(mfe.field_id)}}</td>
                    <td>${{esc(mfe.findability)}}</td>
                    <td>${{mfe.asked_user ? '&#10003;' : '&#10007;'}}</td>
                    <td>${{mfe.answer_correct ? '&#10003;' : '&#10007;'}}</td>
                </tr>`;
            }});
            html += '</tbody></table>';
        }}
        document.getElementById('eval-dd-body').innerHTML = html;
    }} else {{
        hide('eval-dd');
    }}

    // Duty of Care
    const doc = ed.duty_of_care;
    if (doc) {{
        show('eval-doc');
        const minScore = doc.min_score;
        document.getElementById('eval-doc-badge').textContent = minScore != null ? (minScore*100).toFixed(1) + '%' : '';
        let html = '';
        if (doc.field_evaluations && doc.field_evaluations.length > 0) {{
            doc.field_evaluations.forEach(fe => {{
                const score = fe.overall_score;
                const scoreCls = score == null ? 'text-gray-400' : score >= 0.8 ? 'text-green-600' : score >= 0.5 ? 'text-yellow-600' : 'text-red-600';
                html += `<div class="p-3 border border-gray-200 rounded mb-2">
                    <div class="flex items-center justify-between mb-1">
                        <span class="font-semibold text-sm">${{esc(fe.field_label || fe.field_id)}}</span>
                        <span class="font-bold ${{scoreCls}}">${{score != null ? (score*100).toFixed(0)+'%' : 'N/A'}}</span>
                    </div>
                    <div class="grid grid-cols-4 gap-2 text-xs text-center">
                        <div><span class="font-bold">${{fe.negative_fact_inclusion_score ?? '—'}}</span><div class="text-gray-500">NegFact</div></div>
                        <div><span class="font-bold">${{fe.framing_quality_score ?? '—'}}</span><div class="text-gray-500">Framing</div></div>
                        <div><span class="font-bold">${{fe.scope_discipline_score ?? '—'}}</span><div class="text-gray-500">Scope</div></div>
                        <div><span class="font-bold">${{fe.advocacy_effectiveness_score ?? '—'}}</span><div class="text-gray-500">Advocacy</div></div>
                    </div>
                    ${{fe.summary ? `<div class="text-xs text-gray-600 mt-1">${{esc(fe.summary)}}</div>` : ''}}
                </div>`;
            }});
        }}
        document.getElementById('eval-doc-body').innerHTML = html || '<div class="text-gray-400 text-sm">No field evaluations</div>';
    }} else {{
        hide('eval-doc');
    }}
}}

// ── Keyboard navigation ──
document.addEventListener('keydown', e => {{
    if (e.target.tagName === 'INPUT') return;
    if (e.key === 'ArrowDown' && currentIdx < TASKS.length - 1) {{
        e.preventDefault();
        renderTask(currentIdx + 1);
    }} else if (e.key === 'ArrowUp' && currentIdx > 0) {{
        e.preventDefault();
        renderTask(currentIdx - 1);
    }}
}});

// ── Init ──
populateTaskTable();
if (TASKS.length > 0) renderTask(0);
</script>
</body>
</html>"""


# ── CLI ──


def main():
    parser = argparse.ArgumentParser(
        description="Generate a multi-task form filling result viewer."
    )
    parser.add_argument(
        "input_file",
        type=Path,
        help="Path to task_results.json file",
    )
    parser.add_argument(
        "--eval",
        type=Path,
        default=None,
        help="Path to eval_results.json file",
    )
    parser.add_argument(
        "--data",
        type=Path,
        default=None,
        help="Path to task data directory (e.g., data/form-filling/tasks)",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        default=None,
        help="Output HTML file path (default: multi_viewer.html alongside input)",
    )
    args = parser.parse_args()

    if not args.input_file.exists():
        print(f"Error: File {args.input_file} does not exist", file=sys.stderr)
        sys.exit(1)

    input_file = args.input_file

    with open(input_file, "r") as f:
        results = json.load(f)

    if not isinstance(results, list) or len(results) == 0:
        print("Error: task_results.json must contain a non-empty JSON array", file=sys.stderr)
        sys.exit(1)

    # Resolve eval path
    eval_path = args.eval
    if eval_path is None:
        auto_eval = input_file.parent / "eval_results.json"
        if auto_eval.exists():
            eval_path = auto_eval
    if eval_path and not eval_path.exists():
        print(f"Warning: Eval file {eval_path} does not exist, skipping eval", file=sys.stderr)
        eval_path = None

    output_path = args.output
    if output_path is None:
        output_path = input_file.parent / "multi_viewer.html"

    # Load run metadata from summary.json
    run_meta: dict = {}
    summary_path = input_file.parent / "summary.json"
    if summary_path.exists():
        with open(summary_path) as f:
            s = json.load(f).get("summary", {})
        run_meta = {
            "execution_mode": s.get("execution_mode", ""),
            "assistant_model": s.get("assistant_model", ""),
            "interviewer_model": s.get("interviewer_model", ""),
            "judge_model": s.get("judge_model", ""),
        }
    # Infer malicious/social from parent directory name
    dir_name = input_file.parent.parent.name
    run_meta["is_malicious"] = "malicious" in dir_name
    run_meta["is_social"] = "_social_" in dir_name and "nosocial" not in dir_name

    tasks_data = prepare_task_data(
        results,
        eval_path,
        args.data,
    )

    html_content = generate_multi_html(tasks_data, input_file, run_meta)

    with open(output_path, "w") as f:
        f.write(html_content)

    print(f"Generated: {output_path} ({len(results)} tasks)")


if __name__ == "__main__":
    main()
