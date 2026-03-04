"""GUI mode execution for form filling benchmark using browser automation.

Uses a vision-based LLM agent (e.g., Fara-7B) to fill HTML forms via
Playwright headless browser, then restructures the extracted values into
the Pydantic form schema for evaluation.

Prerequisites:
  pip install playwright
  playwright install
"""

import asyncio
import base64
import functools
import http.server
import json
import logging
import re
import threading
from pathlib import Path

from pydantic import BaseModel
from sage_llm import ModelClient

from sage_benchmark.form_filling.agents.oracle_user import OracleUser
from sage_benchmark.form_filling.environment.bm25_index import BM25Index
from sage_benchmark.form_filling.gui_prompt import build_gui_system_prompt
from sage_benchmark.form_filling.prompts import (
    format_artifacts_as_context,
    get_thinking_prompt,
    translate_persona_to_text,
)
from sage_benchmark.form_filling.schemas import (
    FormFillingAction,
    FormTask,
    TaskExecutionResult,
)

logger = logging.getLogger(__name__)

# ── Config ──
VIEWPORT = {"width": 1428, "height": 896}


# ── Context Construction ──


def construct_gui_context_messages(task: FormTask, prompt_type: str = "base") -> list[dict]:
    """Construct context messages for the GUI vision agent.

    Returns separate messages for instruction, persona, artifacts, and guidance,
    matching the pattern used in one_shot.py for better model comprehension.

    Args:
        task: FormTask with persona and artifacts
        prompt_type: Privacy prompt type ("base", "privacy_aware", etc.)

    Returns:
        List of user messages providing context for the vision agent
    """
    persona_info = translate_persona_to_text(task.persona)
    artifacts_context = format_artifacts_as_context(task.artifacts)
    thinking_prompt = get_thinking_prompt(prompt_type)

    return [
        {
            "role": "user",
            "content": f"{task.instruction}\n\n=== YOUR CLIENT'S INFORMATION ===\n{persona_info}\n\n"
            "Fill in all applicable fields on behalf of your client.\n"
            'When you are done filling in the form, use the terminate action with status "success".',
        },
        {"role": "user", "content": artifacts_context},
        {"role": "user", "content": thinking_prompt},
    ]


# ── HTTP Server ──


def start_http_server(directory: str, port: int) -> http.server.HTTPServer:
    """Start a threaded HTTP server serving files from directory."""
    handler = functools.partial(
        http.server.SimpleHTTPRequestHandler,
        directory=directory,
    )
    # Suppress request logs
    handler.log_message = lambda *args, **kwargs: None
    server = http.server.HTTPServer(("localhost", port), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    print(f"HTTP server started at http://localhost:{port} serving {directory}")
    return server


# ── Action parsing ──


def parse_action(text: str) -> tuple[str | None, dict | None]:
    """Parse a tool call from the LLM response text.

    Returns:
        Tuple of (tool_name, arguments_dict). tool_name is None if no tool call
        was found. For computer_use actions, arguments_dict contains the action params.
        For other tools (e.g. file-system tools), arguments_dict contains the tool args.
    """
    match = re.search(r"<tool_call>\s*(\{.*?\})\s*</tool_call>", text, re.DOTALL)
    if match:
        try:
            parsed = json.loads(match.group(1))
            tool_name = parsed.get("name")
            arguments = parsed.get("arguments", parsed)
            return tool_name, arguments
        except json.JSONDecodeError:
            pass
    # Fallback: look for action dicts (computer_use format)
    for m in re.finditer(r'\{[^{}]*"action"\s*:\s*"[^"]+?"[^{}]*\}', text, re.DOTALL):
        try:
            parsed = json.loads(m.group())
            if "action" in parsed:
                return "computer_use", parsed
        except json.JSONDecodeError:
            continue
    return None, None


# ── Screenshot ──


async def screenshot_to_base64(page) -> str:
    """Take a screenshot and return as base64-encoded string."""
    png_bytes = await page.screenshot()
    return base64.b64encode(png_bytes).decode("utf-8")


# ── Action execution ──


async def execute_action(page, action: dict):
    """Execute a browser action. Returns False if the agent terminated."""
    act = action["action"]
    if act == "left_click":
        x, y = action["coordinate"]
        await page.mouse.click(x, y)
    elif act == "type":
        text = action["text"]
        coord = action.get("coordinate")
        if coord:
            await page.mouse.click(coord[0], coord[1])
            await asyncio.sleep(0.3)
        await page.keyboard.type(text)
    elif act == "key":
        keys = action["keys"]
        for k in keys:
            await page.keyboard.down(k)
        for k in reversed(keys):
            await page.keyboard.up(k)
    elif act == "scroll":
        pixels = action.get("pixels", -300)
        await page.mouse.wheel(0, -pixels)
    elif act == "mouse_move":
        x, y = action["coordinate"]
        await page.mouse.move(x, y)
    elif act == "visit_url":
        await page.goto(action["url"], wait_until="domcontentloaded")
    elif act == "web_search":
        await page.goto(
            f"https://www.google.com/search?q={action['query']}",
            wait_until="domcontentloaded",
        )
    elif act == "history_back":
        await page.go_back()
    elif act == "wait":
        await asyncio.sleep(action.get("time", 2))
    elif act == "pause_and_memorize_fact":
        pass
    elif act == "terminate":
        return False
    return True


# ── Extract all form values generically ──


async def extract_form_values(page) -> dict:
    """Extract all input/select/textarea values from the page as a flat dict."""
    return await page.evaluate(
        """() => {
        const data = {};
        // Text inputs, email, tel, url, date, number
        document.querySelectorAll('input[type="text"], input[type="email"], input[type="tel"], input[type="url"], input[type="date"], input[type="number"], input:not([type])').forEach(el => {
            const key = el.id || el.name || '';
            if (key) data[key] = el.value || '';
        });
        // Checkboxes
        document.querySelectorAll('input[type="checkbox"]').forEach(el => {
            const key = el.id || el.name || '';
            if (key) data[key] = el.checked;
        });
        // Radio buttons
        document.querySelectorAll('input[type="radio"]:checked').forEach(el => {
            const key = el.name || el.id || '';
            if (key) data[key] = el.value || '';
        });
        // Selects
        document.querySelectorAll('select').forEach(el => {
            const key = el.id || el.name || '';
            if (key) data[key] = el.value || '';
        });
        // Textareas
        document.querySelectorAll('textarea').forEach(el => {
            const key = el.id || el.name || '';
            if (key) data[key] = el.value || '';
        });
        return data;
    }"""
    )


# ── LLM-based adapter: flat HTML values -> nested Pydantic schema ──


async def restructure_form_values(
    client: ModelClient,
    model: str,
    flat_values: dict,
    form_class: type[BaseModel],
) -> dict:
    """Use the LLM to restructure flat HTML form values into the nested Pydantic schema.

    Args:
        client: ModelClient for the restructuring LLM call
        model: Model name for restructuring
        flat_values: Flat dict of {field_id: value} from HTML extraction
        form_class: Pydantic model class defining the expected nested schema

    Returns:
        Nested dict matching the Pydantic form schema
    """
    schema = form_class.model_json_schema()

    prompt = f"""You are given form field values extracted from an HTML form.
Your task is to map these flat key-value pairs into the correct nested JSON structure
that matches the provided form schema.

Extracted HTML form field values:
{json.dumps(flat_values, indent=2)}

Target form schema:
{json.dumps(schema, indent=2)}

Instructions:
- Map each extracted value to the most appropriate field in the schema based on field names and descriptions.
- For checkbox/boolean fields, use "true" or "false" as string values.
- If a schema field has no matching extracted value, use an empty string "".
- Preserve the exact values from the extraction; do not modify or fabricate data.
- Use the fill_form tool to submit the structured result."""

    tools = [
        {
            "type": "function",
            "function": {
                "name": "fill_form",
                "description": "Submit the restructured form data matching the form schema",
                "parameters": schema,
            },
        },
    ]

    response = await client.chat.completions.acreate(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        tools=tools,
        tool_choice="required",
    )

    message = response.choices[0].message
    if not message.tool_calls or len(message.tool_calls) == 0:
        raise ValueError("LLM did not return a tool call for restructuring")

    tool_args = message.tool_calls[0].function.arguments
    if isinstance(tool_args, str):
        tool_args = json.loads(tool_args)

    validated_form = form_class.model_validate(tool_args)
    return validated_form.model_dump()


# ── Run vision agent on a single form ──


FILE_SYSTEM_TOOL_NAMES = {"search_email", "read_email", "search_calendar", "read_calendar"}


async def run_vision_agent_on_form(
    client: ModelClient,
    model: str,
    browser,
    form_url: str,
    context_messages: list[dict],
    max_steps: int = 30,
    oracle_user: OracleUser | None = None,
    file_system: bool = False,
    bm25_index: BM25Index | None = None,
) -> dict:
    """Run the vision agent on one form.

    Args:
        client: ModelClient for the vision agent
        model: Vision model name
        browser: Playwright browser instance
        form_url: URL of the form to fill
        context_messages: List of user messages with task context (instruction, artifacts, guidance)
        max_steps: Maximum interaction steps
        oracle_user: Optional OracleUser for answering ask_user questions
        file_system: If True, file-system tools are available
        bm25_index: BM25Index for executing file-system tool calls

    Returns dict with steps taken and extracted flat form values.
    """
    # Build system prompt using gui_prompt.py
    system_prompt, (resized_width, resized_height) = build_gui_system_prompt(
        VIEWPORT["width"],
        VIEWPORT["height"],
        file_system=file_system,
    )

    context = await browser.new_context(viewport=VIEWPORT)
    page = await context.new_page()
    await page.goto(form_url, wait_until="domcontentloaded")
    await asyncio.sleep(1)

    messages = [
        {"role": "system", "content": system_prompt},
        *context_messages,
    ]

    steps_log = []
    user_qa_history = []
    terminated = False

    for step in range(max_steps):
        img_b64 = await screenshot_to_base64(page)
        messages.append(
            {
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img_b64}"}},
                    {"type": "text", "text": "What's the next step?"},
                ],
            }
        )

        try:
            response = await client.chat.completions.acreate(
                model=model,
                messages=messages,
                temperature=0,
                max_tokens=1024,
            )
            raw_output = response.choices[0].message.content or ""
        except Exception as e:
            print(f"    LLM error at step {step + 1}: {e}")
            break

        tool_name, action = parse_action(raw_output)
        if not action:
            messages.append({"role": "assistant", "content": raw_output})
            continue

        step_info = {
            "step": step + 1,
            "thought": raw_output.split("<tool_call>")[0].strip(),
            "tool_name": tool_name,
            "action": action,
        }
        steps_log.append(step_info)

        messages.append({"role": "assistant", "content": raw_output})

        # Handle file-system tool calls
        if tool_name in FILE_SYSTEM_TOOL_NAMES and bm25_index is not None:
            print(
                f"    Step {step + 1}: {tool_name}({json.dumps(action)})"
                f"\n      Thought: {step_info['thought']}"
            )
            result_str = bm25_index.execute_tool(tool_name, action)
            print(f"    {tool_name} returned {len(result_str)} chars")
            messages.append(
                {"role": "user", "content": f"<tool_response>\n{result_str}\n</tool_response>"}
            )
            continue

        # From here on, it's a computer_use action with an "action" key
        print(
            f"    Step {step + 1}: {action.get('action', tool_name)} "
            f"{json.dumps({k: v for k, v in action.items() if k != 'action'})}"
            f"\n      Thought: {step_info['thought']}"
        )

        # Handle ask_user action
        if action.get("action") == "ask_user" and oracle_user is not None:
            question = action.get("question", "")
            print(f"    Agent asks user: {question[:80]}...")
            user_answer = await oracle_user.answer_question(question)
            print(f"    User answers: {user_answer[:80]}...")
            user_qa_history.append({"question": question, "answer": user_answer})
            step_info["user_answer"] = user_answer
            messages.append({"role": "user", "content": f"User's answer: {user_answer}"})
            continue

        should_continue = await execute_action(page, action)
        await asyncio.sleep(0.5)

        if not should_continue:
            terminated = True
            break

    # Extract form values
    form_values = await extract_form_values(page)
    await context.close()

    return {
        "steps": steps_log,
        "num_steps": len(steps_log),
        "terminated": terminated,
        "form_values": form_values,
        "user_qa_history": user_qa_history,
    }


# ── Single task execution (matches one_shot.py pattern) ──


async def run_single_task(
    task: FormTask,
    task_index: int,
    client: ModelClient,
    model: str,
    restructure_client: ModelClient,
    restructure_model: str,
    browser,
    http_port: int,
    data_path: str,
    prompt_type: str = "base",
    max_steps: int = 30,
    oracle_user: OracleUser | None = None,
    file_system: bool = False,
) -> TaskExecutionResult:
    """Execute GUI form filling for a single task.

    Args:
        task: FormTask with persona, artifacts, form info
        task_index: Task index for tracking
        client: ModelClient for the vision agent
        model: Vision model name (e.g., "microsoft/Fara-7B")
        restructure_client: ModelClient for restructuring flat values
        restructure_model: Model name for restructuring
        browser: Playwright browser instance
        http_port: Port for the local HTTP server
        data_path: Root directory containing task subdirectories with HTML form files
        prompt_type: Privacy prompt type
        max_steps: Maximum interaction steps
        oracle_user: Optional OracleUser for answering ask_user questions
        file_system: If True, enable file-system tools (search/read email/calendar)

    Returns:
        TaskExecutionResult compatible with evaluate_task()
    """
    form_filename = f"form_{task.form_id}.html"
    form_path = Path(data_path) / f"form_{task.form_id}" / form_filename
    if not form_path.exists():
        return TaskExecutionResult(
            task_index=task_index,
            task=task,
            action=None,
            llm_calls=[],
            success=False,
            error_message=f"HTML form not found: {form_path}",
        )

    form_url = f"http://localhost:{http_port}/form_{task.form_id}/{form_filename}"

    # Construct context messages from benchmark data (separate messages for clarity)
    context_messages = construct_gui_context_messages(task, prompt_type)

    # Initialize BM25 index for file-system mode
    bm25_index: BM25Index | None = None
    if file_system and task.filesystem_artifacts:
        bm25_index = BM25Index([a.model_dump() for a in task.filesystem_artifacts])

    print(f"[Task {task_index}] Running GUI agent on form_{task.form_id}...")

    try:
        # Run the vision agent
        result = await run_vision_agent_on_form(
            client,
            model,
            browser,
            form_url,
            context_messages,
            max_steps,
            oracle_user=oracle_user,
            file_system=file_system,
            bm25_index=bm25_index,
        )

        flat_values = result["form_values"]
        has_content = any(
            v for v in flat_values.values() if v and str(v).strip() and str(v).strip() != "false"
        )

        if not has_content:
            print(f"[Task {task_index}] No form values extracted")
            return TaskExecutionResult(
                task_index=task_index,
                task=task,
                action=None,
                llm_calls=[],
                success=False,
                error_message=f"No form values extracted (steps={result['num_steps']}, terminated={result['terminated']})",
            )

        # Restructure flat values into nested Pydantic schema
        print(f"[Task {task_index}] Restructuring form values...")
        nested_values = await restructure_form_values(
            restructure_client, restructure_model, flat_values, task.form_class
        )

        action = FormFillingAction(
            action_type="fill",
            fill_responses=nested_values,
        )

        print(f"[Task {task_index}] Success! ({result['num_steps']} steps)")
        return TaskExecutionResult(
            task_index=task_index,
            task=task,
            action=action,
            llm_calls=[],
            success=True,
        )

    except Exception as e:
        logger.error(f"Task {task_index} failed: {e}")
        return TaskExecutionResult(
            task_index=task_index,
            task=task,
            action=None,
            llm_calls=[],
            success=False,
            error_message=str(e),
        )
