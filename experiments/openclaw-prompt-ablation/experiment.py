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
advocacy guidance    off / on                 ``ABLATION_ADVOCACY_GUIDANCE``
preference tool      off / on                 ``ABLATION_PREFERENCE_TOOL``
===================  =======================  ============================

Tools are written into the Gateway's config file when it starts, and the
Gateway pool outlives a single variant, so that factor cannot vary *within* one
``srbench experiment`` process — it selects which process to run. ``run.sh``
walks the two tool settings and this file sweeps the benchmark framing and
preference guidance inside each. Advocacy guidance is held fixed for one output
sweep so the completed historical cells can serve as its ``off`` arm without
being rerun.

Reading the same environment variable the machinery reads, rather than
mirroring it into a private setting, is what keeps a variant's name honest: a
cell cannot claim tools were restricted unless they actually were.

``delivery`` is the exception, and the reason the grid is not a clean product.
``system`` is the arrangement above. ``user`` is the harness **as it ships**:
OpenClaw's own prompt stands and the benchmark's framing arrives in the opening
user turn, which OpenClaw labels as untrusted sender metadata. The benchmark's
system text has nowhere else to go there, so ``srbench-off`` is not a condition
that arm can express and it contributes two cells rather than four. Those two
run under both tool settings, and are skipped only under ``all``, where the
agent could read the graded ground truth off disk.

Four prompt cells x two tool settings, plus two stock cells per tool setting =
twelve, x ``REPEATS`` for variance:

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
tasks, so a default sweep is 140 x 12 cells x 3 repeats = 5,040 runs.

Set ``ABLATION_ADVOCACY_GUIDANCE=on`` and filter to ``srbench-on`` to run the
eight treatment cells. Combined with the existing eight-cell GPT-5.4 baseline,
that produces a balanced 2 x 2 x 2 x 2 design with 6,720 runs.

Set ``ABLATION_PREFERENCE_TOOL=on`` and walk both advocacy settings to run the
16 new helper cells. Combined with the existing 16 helper-off cells, that
produces a balanced five-factor design with 13,440 runs.

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

# The assistant under test. Model and effort are overridable because the harness
# is only half the question — a prompt or tool change that costs one model points
# may cost another none, and that cannot be told apart from a fixed-model sweep.
#
# They are not part of the variant name, so one sweep is one model and different
# models need different ``--output-base`` values. Each run records the model it
# used in its own config, which is what any analysis should read.
ASSISTANT: dict[str, Any] = {
    "agent": "srbench_agents.calendar_openclaw_agent:CalendarOpenClawAgent",
    "model": os.environ.get("ABLATION_ASSISTANT_MODEL", "phyagi/gpt-5.4"),
    "effort": os.environ.get("ABLATION_ASSISTANT_EFFORT", "xhigh"),
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


def advocacy_guidance() -> bool:
    """Return whether the opt-in advocacy policy should be added.

    The historical GPT-5.4 sweep is the ``off`` arm. Keeping that as the
    default preserves its variant names and serialized configs, so those cells
    remain resumable and need not be rerun.

    Raises:
        ValueError: If ``ABLATION_ADVOCACY_GUIDANCE`` is not ``off`` or ``on``.
    """
    setting = os.environ.get("ABLATION_ADVOCACY_GUIDANCE", "off").strip().lower()
    if setting not in ("off", "on"):
        raise ValueError(f"ABLATION_ADVOCACY_GUIDANCE must be 'off' or 'on', got {setting!r}.")
    return setting == "on"


def programmatic_preference_tool() -> bool:
    """Return whether the deterministic next-best-slot tool is enabled.

    The completed GPT-5.4 cells are the ``off`` arm. The false setting is kept
    out of agent kwargs and serialized config so those historical cells retain
    their exact names and configuration shape.

    Raises:
        ValueError: If ``ABLATION_PREFERENCE_TOOL`` is not ``off`` or ``on``.
    """
    setting = os.environ.get("ABLATION_PREFERENCE_TOOL", "off").strip().lower()
    if setting not in ("off", "on"):
        raise ValueError(f"ABLATION_PREFERENCE_TOOL must be 'off' or 'on', got {setting!r}.")
    return setting == "on"


def prompt_cells():
    """Yield the prompt settings to sweep in this process.

    The stock arm varies guidance only. The benchmark's system text has nowhere
    else to go once OpenClaw's own prompt occupies the system slot, so
    ``srbench-off`` is not a condition it can express, and it contributes two
    cells rather than four.

    It is skipped under ``all``, where the built-ins run on the host and the
    agent can read the graded ground truth off disk, making a score
    indistinguishable from one it looked up. That risk is specific to ``all``:
    ``sandbox`` confines the built-ins to a container that cannot see the
    repository, and ``srbench`` removes them outright, leaving nothing that can
    read a file.
    """
    for srbench in (False, True):
        for guidance in (False, True):
            yield {"delivery": "system", "srbench": srbench, "guidance": guidance}
    if tools() != "all":
        for guidance in (False, True):
            yield {"delivery": "user", "srbench": True, "guidance": guidance}


def variant(cell: dict[str, Any], repeat: int) -> str:
    """Name a cell after every factor, so an output directory is self-describing."""
    advocacy = "_advocacy-on" if advocacy_guidance() else ""
    preference_tool = "_preference-tool-on" if programmatic_preference_tool() else ""
    return (
        f"calendar_delivery-{cell['delivery']}"
        f"_srbench-{'on' if cell['srbench'] else 'off'}"
        f"_guidance-{'on' if cell['guidance'] else 'off'}"
        f"_tools-{tools()}"
        f"{advocacy}"
        f"{preference_tool}"
        f"_rep{repeat}"
    )


# --- Calendar ---


def experiment_calendar():
    from srbench.benchmarks.calendar_scheduling.config import CalendarRunConfig

    for cell in prompt_cells():
        agent_kwargs: dict[str, Any] = {
            "srbench_system_prompt": cell["srbench"],
            "preference_guidance": cell["guidance"],
            "prompt_delivery": cell["delivery"],
        }
        if advocacy_guidance():
            agent_kwargs["advocacy_guidance"] = True
        if programmatic_preference_tool():
            agent_kwargs["programmatic_preference_tool"] = True

        yield CalendarRunConfig(
            paths=[DATA_PATH],
            # Assistant (BYOA, OpenClaw)
            assistant_agent=ASSISTANT["agent"],
            assistant_model=ASSISTANT["model"],
            assistant_reasoning_effort=ASSISTANT["effort"],
            assistant_agent_kwargs=agent_kwargs,
            system_prompt="none",
            expose_preferences=True,
            programmatic_preference_tool=programmatic_preference_tool(),
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
