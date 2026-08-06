"""Audit programmatic preference-tool runs for treatment compliance."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from srbench.benchmarks.calendar_scheduling.evaluation.preference_adherence import (
    PreferenceSlotSelector,
)
from srbench.benchmarks.calendar_scheduling.types import CalendarTask

HELPER = "FindNextBestSlot"
REPLY = "ReplyMeeting"
WAIT = "Wait"
PROMPT_MARKER = "Programmatic preference tool"


def _read_results(path: Path) -> dict[str, Any]:
    """Read one final result file."""
    return json.loads(path.read_text())


def _slot(payload: dict[str, Any]) -> tuple[Any, Any, Any]:
    """Return a comparable ``(date, start, end)`` tuple."""
    return payload.get("date"), payload.get("start"), payload.get("end")


def _audit_record(record: dict[str, Any]) -> list[str]:
    """Return treatment-compliance failures for one run."""
    execution = record.get("execution") or {}
    task = execution.get("task") or {}
    task_id = task.get("id", "?")
    assistant_email = (task.get("assistant") or {}).get("email")
    trace = execution.get("action_trace") or []
    failures: list[str] = []
    current_helper: dict[str, Any] | None = None
    helper_calls = 0
    meetings: dict[str, tuple[Any, Any, Any]] = {}
    calendar_task = CalendarTask.model_validate(task)
    preference_file = calendar_task.assistant.preference_file
    if not preference_file:
        return [f"task {task_id}: helper treatment task has no preference document"]
    selector = PreferenceSlotSelector.from_preference(
        preference_file,
        calendar_task.requestor.requested_meeting,
    )

    for entry in trace:
        actor = entry.get("actor")
        action = entry.get("action_type")
        payload = entry.get("payload") or {}
        valid = entry.get("valid", True)

        if action == "RequestMeeting" and valid:
            meetings[payload.get("uid")] = _slot(payload)

        if actor != assistant_email:
            if action == REPLY and payload.get("status") == "COUNTER" and valid:
                meetings[payload.get("meeting_uid")] = _slot(payload)
            continue

        if action == WAIT:
            current_helper = None
        elif action == HELPER:
            helper_calls += 1
            if not valid:
                current_helper = None
                failures.append(f"task {task_id}: helper call was rejected")
                continue
            try:
                current_helper = json.loads(entry.get("result") or "")
            except json.JSONDecodeError:
                current_helper = None
                failures.append(f"task {task_id}: helper returned non-JSON output")
                continue
            expected = json.loads(selector.select(payload.get("blocked_starts") or []))
            if current_helper != expected:
                failures.append(
                    f"task {task_id}: helper returned {current_helper}, expected {expected}"
                )
        elif action == REPLY and payload.get("status") in {
            "ACCEPTED",
            "COUNTER",
            "DECLINED",
        }:
            status = payload["status"]
            if not valid:
                failures.append(f"task {task_id}: {status} ReplyMeeting call was rejected")
            if current_helper is None:
                failures.append(f"task {task_id}: {status} had no fresh successful helper call")
            elif status == "COUNTER":
                if _slot(payload) != _slot(current_helper):
                    failures.append(
                        f"task {task_id}: COUNTER {_slot(payload)} != helper "
                        f"{_slot(current_helper)}"
                    )
            elif status == "ACCEPTED":
                meeting_slot = meetings.get(payload.get("meeting_uid"))
                if meeting_slot != _slot(current_helper):
                    failures.append(
                        f"task {task_id}: ACCEPTED {meeting_slot} != helper {_slot(current_helper)}"
                    )
            elif any(current_helper.get(field) is not None for field in ("date", "start", "end")):
                failures.append(
                    f"task {task_id}: DECLINED despite helper returning {_slot(current_helper)}"
                )
            current_helper = None

        if action == REPLY and payload.get("status") == "COUNTER" and valid:
            meetings[payload.get("meeting_uid")] = _slot(payload)

    if helper_calls == 0:
        failures.append(f"task {task_id}: helper was never called")
    return failures


def main() -> int:
    """Audit every final helper-on result under an output base."""
    parser = argparse.ArgumentParser()
    parser.add_argument("output_base", type=Path)
    parser.add_argument("--expected-runs", type=int)
    parser.add_argument("--expected-traces", type=int)
    args = parser.parse_args()

    result_files = sorted(
        (args.output_base / "openclaw-prompt-ablation").glob("*_preference-tool-on_*/results.json")
    )
    runs = 0
    failures: list[str] = []
    cells: list[str] = []
    for path in result_files:
        document = _read_results(path)
        cells.append(path.parent.name)
        config = document.get("config") or {}
        kwargs = config.get("assistant_agent_kwargs") or {}
        if config.get("programmatic_preference_tool") is not True:
            failures.append(f"{path.parent.name}: config tool flag is not true")
        if kwargs.get("programmatic_preference_tool") is not True:
            failures.append(f"{path.parent.name}: agent tool flag is not true")

        for record in document.get("results") or []:
            runs += 1
            if record.get("error") or (record.get("execution") or {}).get("error"):
                failures.append(
                    f"{path.parent.name}: task "
                    f"{((record.get('execution') or {}).get('task') or {}).get('id', '?')} "
                    "has an execution or evaluation error"
                )
                continue
            names = {
                tool["function"]["name"]
                for tool in (record.get("execution") or {}).get("assistant_tools") or []
            }
            if HELPER not in names:
                failures.append(f"{path.parent.name}: helper schema is absent")
            if len(names) != 8:
                failures.append(
                    f"{path.parent.name}: expected 8 benchmark assistant tools, found {len(names)}"
                )
            requestor_names = {
                tool["function"]["name"]
                for tool in (record.get("execution") or {}).get("requestor_tools") or []
            }
            if HELPER in requestor_names:
                failures.append(f"{path.parent.name}: helper leaked to requestor tools")
            failures.extend(_audit_record(record))

    if args.expected_runs is not None and runs != args.expected_runs:
        failures.append(f"expected {args.expected_runs} runs, found {runs}")

    trace_files = sorted((args.output_base / "openclaw-traces").glob("*.json"))
    trace_shapes: dict[tuple[str, str], int] = {}
    for path in trace_files:
        trace = _read_results(path)
        system = str(trace.get("system") or "")
        messages = trace.get("messages") or []
        opening_user = next(
            (
                json.dumps(message)
                for message in messages
                if isinstance(message, dict) and message.get("role") == "user"
            ),
            "",
        )
        delivery = "user" if trace.get("srbench_system_prompt") is None else "system"
        tools = str(trace.get("tools") or "")
        trace_shapes[(delivery, tools)] = trace_shapes.get((delivery, tools), 0) + 1
        channel_ok = (
            system.count(PROMPT_MARKER) == 1 and PROMPT_MARKER not in opening_user
            if delivery == "system"
            else PROMPT_MARKER not in system and opening_user.count(PROMPT_MARKER) == 1
        )
        if trace.get("model") != "gpt-5.4":
            failures.append(f"{path.name}: unexpected model {trace.get('model')!r}")
        if tools not in {"srbench", "sandbox"}:
            failures.append(f"{path.name}: unexpected tool profile {tools!r}")
        if not channel_ok:
            failures.append(f"{path.name}: helper prompt is in the wrong channel")

    if args.expected_traces is not None and len(trace_files) != args.expected_traces:
        failures.append(f"expected {args.expected_traces} traces, found {len(trace_files)}")

    print(
        f"cells={len(cells)} runs={runs} traces={len(trace_files)} "
        f"trace_shapes={dict(sorted(trace_shapes.items()))} failures={len(failures)}"
    )
    for failure in failures[:50]:
        print(f"- {failure}")
    if len(failures) > 50:
        print(f"- ... {len(failures) - 50} more")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
