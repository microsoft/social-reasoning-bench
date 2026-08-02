"""
Experiments for SocialReasoning-Bench — what the OpenClaw harness contributes

A BYOA run does not swap the harness alone. OpenClaw ships a ~36 KB system
prompt of its own and, by default, its full built-in tool set (``exec``,
``read``, ``web_search``, ...) *in addition to* the benchmark's MCP tools. Both
travel with the harness, so a plain OpenClaw-vs-native comparison confounds
three changes at once and cannot say which one moved a score.

This experiment holds them still. In most cells the agent composes the **entire**
system prompt itself and OpenClaw sends exactly that, so its own prompt never
appears and what remains to sweep is the benchmark's own framing and the tools:

===================  =======================  ============================
factor               values                   set by
===================  =======================  ============================
tools                srbench / sandbox        ``SRBENCH_OPENCLAW_TOOLS``
delivery             system / user            swept here
SRBench prompt       on / off                 swept here
preference guidance  on / off                 swept here
===================  =======================  ============================

Tools are written into the Gateway's config file when it starts, and the
Gateway pool outlives a single variant, so that factor cannot vary *within* one
``srbench experiment`` process — it selects which process to run. ``run.sh``
walks the two settings and this file sweeps the remaining two inside each.

Reading the same environment variable the machinery reads, rather than
mirroring it into a private setting, is what keeps a variant's name honest: a
cell cannot claim tools were restricted unless they actually were.

``delivery`` is the exception, and the reason the grid is not a clean product.
``system`` is the arrangement above. ``user`` is the harness **as it ships**:
OpenClaw's own prompt stands and the benchmark's framing arrives in the opening
user turn, which OpenClaw labels as untrusted sender metadata. That baseline is
one configuration rather than four — the system text has nowhere else to go, and
outside the container its scores would not be trustworthy — so it contributes
two cells, guidance on and off, under ``sandbox`` only.

Four prompt cells x two tool settings, plus two stock cells = ten, x ``REPEATS``
for variance:

    ground rules only  ·  + guidance  ·  + SRBench  ·  + SRBench + guidance
    stock OpenClaw  ·  stock OpenClaw + guidance

The ground rules (call ``Wait``, one action per turn, finish with
``EndConversation``) are in every cell. They are the harness protocol contract,
not a prompt treatment; an agent that has not been told them cannot drive the
environment at all. So the "off/off" cell is a real condition — protocol and
nothing else — rather than an agent left with no instructions.

Every run records the system prompt it sent as the first entry of
``execution.assistant_context``, so a result carries the exact text that
produced it and a cell's label can be checked against what the model saw. In the
stock cells that entry is a marker naming OpenClaw's prompt by length and
digest, because pasting its ~36 KB operating manual into a graded transcript
would change what the due-diligence judge sees in one arm only; the full text
goes to the trace dump instead.

``SRBENCH_OPENCLAW_TRACE_DIR`` (set by ``run.sh``) turns on OpenClaw's cache
trace and dumps, per task, the system prompt and message array **as the provider
received them** — including the untrusted-metadata wrapper. That is the artifact
to read when checking what a cell actually did.

The dataset is the soft-preference split, because ``preference guidance`` is
only defined for tasks that carry a preference document. ``large.yaml`` is 140
tasks, so a default sweep is 140 x 10 cells x 3 repeats = 4,200 runs.

Prerequisites:
    A local OpenClaw build that honours ``OPENCLAW_SYSTEM_PROMPT_FILE``, pointed
    to by ``SRBENCH_OPENCLAW_BIN``. Stock OpenClaw has no way to replace its
    system prompt, so every cell needs it. See ``README.md``.

To reproduce:
    experiments/openclaw-prompt-ablation/run.sh

    # Smoke test: three tasks per cell
    experiments/openclaw-prompt-ablation/run.sh --set limit=3

    # Outputs land in: outputs/openclaw_ablation
"""

import os
from typing import Any

DATA_PATH = "data/calendar-scheduling/soft/large.yaml"

ASSISTANT: dict[str, Any] = {
    "agent": "srbench_agents.calendar_openclaw_agent:CalendarOpenClawAgent",
    "model": "phyagi/gpt-5.4",
    "effort": "xhigh",
}

JUDGE: dict[str, Any] = {
    "model": "gemini-2.5-flash",
    # Use dynamic thinking (the default for gemini-2.5-flash)
    "reasoning_effort": -1,
    "explicit_cot": False,
}

COUNTERPARTY: dict[str, Any] = {
    "model": "gemini-3-flash-preview",
    "reasoning_effort": "medium",
    "explicit_cot": False,
}

ROUNDS: dict[str, Any] = {"max_rounds": 10, "max_steps_per_turn": 3}

# Which repeat this process is running. Task completion is nondeterministic and
# the benchmark exposes no seed, so a single run of a cell cannot be told apart
# from noise; repeats are how the spread gets measured.
#
# One per process, driven by run.sh, because the collector deduplicates configs
# by content and explicitly ignores ``variant`` — three identical cells yielded
# from one generator collapse into one silently. Separate processes each get a
# fresh dedup set.
REPEAT = int(os.environ.get("ABLATION_REPEAT", "1"))

# A task holds one Gateway exclusively while it runs, so tasks run in parallel
# only up to the pool size. Deriving batch size from the pool rather than
# declaring it separately removes the usual failure where a wide batch quietly
# queues behind one Gateway.
POOL_SIZE = int(os.environ.get("SRBENCH_OPENCLAW_POOL_SIZE", "1"))
CONCURRENCY: dict[str, Any] = {
    "batch_size": POOL_SIZE,
    "task_concurrency": POOL_SIZE,
    "llm_concurrency": 8,
}


def tools() -> str:
    """Return which tools the agent can reach, as the Gateway will configure them.

    Normalized rather than echoed, so an unrecognized value is reported as what
    it actually does — leave OpenClaw's built-ins enabled on the host.
    """
    setting = os.environ.get("SRBENCH_OPENCLAW_TOOLS", "").strip().lower()
    return setting if setting in ("srbench", "sandbox") else "all"


def prompt_cells():
    """Yield the prompt settings to sweep in this process.

    The stock arm is not crossed with the rest. Its point is to measure the
    harness as it ships, and "as it ships" is one configuration, not four: the
    benchmark's system text has nowhere else to go, and running it without the
    container would produce scores that cannot be told apart from ones read off
    disk. So it contributes two cells, guidance on and off, under ``sandbox``.
    """
    for srbench in (False, True):
        for guidance in (False, True):
            yield {"delivery": "system", "srbench": srbench, "guidance": guidance}
    if tools() == "sandbox":
        for guidance in (False, True):
            yield {"delivery": "user", "srbench": True, "guidance": guidance}


def variant(cell: dict[str, Any], repeat: int) -> str:
    """Name a cell after every factor, so an output directory is self-describing."""
    return (
        f"calendar_delivery-{cell['delivery']}"
        f"_srbench-{'on' if cell['srbench'] else 'off'}"
        f"_guidance-{'on' if cell['guidance'] else 'off'}"
        f"_tools-{tools()}"
        f"_rep{repeat}"
    )


# --- Calendar ---


def experiment_calendar():
    from srbench.benchmarks.calendar_scheduling.config import CalendarRunConfig

    for cell in prompt_cells():
        yield CalendarRunConfig(
            paths=[DATA_PATH],
            # Assistant (BYOA, OpenClaw)
            assistant_agent=ASSISTANT["agent"],
            assistant_model=ASSISTANT["model"],
            assistant_reasoning_effort=ASSISTANT["effort"],
            assistant_agent_kwargs={
                "srbench_system_prompt": cell["srbench"],
                "preference_guidance": cell["guidance"],
                "prompt_delivery": cell["delivery"],
            },
            system_prompt="none",
            expose_preferences=True,
            # Requestor
            requestor_model=COUNTERPARTY["model"],
            requestor_explicit_cot=COUNTERPARTY["explicit_cot"],
            requestor_reasoning_effort=COUNTERPARTY["reasoning_effort"],
            attack_types=[],
            # Judge
            judge_model=JUDGE["model"],
            judge_reasoning_effort=JUDGE["reasoning_effort"],
            # Concurrency
            batch_size=CONCURRENCY["batch_size"],
            task_concurrency=CONCURRENCY["task_concurrency"],
            llm_concurrency=CONCURRENCY["llm_concurrency"],
            # Rounds
            max_rounds=ROUNDS["max_rounds"],
            max_steps_per_turn=ROUNDS["max_steps_per_turn"],
            variant=variant(cell, REPEAT),
        )


# --- Marketplace ---


def experiment_marketplace():
    return
    yield
