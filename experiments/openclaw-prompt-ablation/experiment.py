"""
Experiments for SocialReasoning-Bench — what the OpenClaw harness contributes

A BYOA run does not swap the harness alone. OpenClaw ships a ~36 KB system
prompt of its own and, by default, its full built-in tool set (``exec``,
``read``, ``web_search``, ...) *in addition to* the benchmark's MCP tools. Both
travel with the harness, so a plain OpenClaw-vs-native comparison confounds
three changes at once and cannot say which one moved a score.

This experiment separates them into four factors:

===================  =======================  ============================
factor               values                   set by
===================  =======================  ============================
OpenClaw prompt      on / off                 ``OPENCLAW_SYSTEM_PROMPT_OVERRIDE``
tools                all / srbench            ``SRBENCH_OPENCLAW_TOOLS``
SRBench prompt       on / off                 swept here
preference guidance  on / off                 swept here
===================  =======================  ============================

The first two are read at Gateway start-up: the override is an environment
variable the Gateway's Node process inherits when it spawns, and the tool
profile is written into its config file. The Gateway pool outlives a single
variant, so those two cannot vary *within* one ``srbench experiment`` process —
they select which process to run. ``run.sh`` walks the four combinations, and
this file sweeps the remaining two inside each.

Reading the same two environment variables the machinery reads, rather than
mirroring them into private settings, is what keeps a variant's name honest: a
cell cannot claim tools were restricted unless they actually were.

That yields six prompt cells rather than eight. With both prompts off the agent
has no standing instructions beyond the harness ground rules, which is not a
condition anyone wants to interpret, so those two are skipped:

    OpenClaw only  ·  OpenClaw + guidance  ·  OpenClaw + SRBench
    OpenClaw + SRBench + guidance  ·  SRBench only  ·  SRBench + guidance

Six cells x two tool settings = twelve, x ``REPEATS`` for variance.

The ground rules (call ``Wait``, one action per turn, finish with
``EndConversation``) are sent in every cell. They are the harness protocol
contract, not a prompt treatment; an agent that has not been told them cannot
drive the environment at all.

The dataset is the soft-preference split, because ``preference guidance`` is
only defined for tasks that carry a preference document.

Prerequisites:
    A local OpenClaw build carrying the system-prompt override, pointed to by
    ``SRBENCH_OPENCLAW_BIN``. Stock OpenClaw has no way to replace its system
    prompt, so the "off" cells need it. See ``README.md``.

To reproduce:
    experiments/openclaw-prompt-ablation/run.sh

    # Smoke test: three tasks per cell
    experiments/openclaw-prompt-ablation/run.sh --set limit=3

    # Outputs land in: outputs/openclaw_ablation
"""

import os
from typing import Any

DATA_PATH = "data/calendar-scheduling/soft/small.yaml"

ASSISTANT: dict[str, Any] = {
    "agent": "srbench_agents.calendar_openclaw_agent:CalendarOpenClawAgent",
    "model": "phyagi/gpt-5.5",
    "effort": "high",
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

# How many times to run each cell. Task completion is nondeterministic and the
# benchmark exposes no seed, so a single run of a cell cannot be told apart from
# noise; repeats are how the spread gets measured.
REPEATS = int(os.environ.get("ABLATION_REPEATS", "1"))

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


def openclaw_prompt() -> str:
    """Return whether OpenClaw's own system prompt is in play.

    The patched binary returns ``OPENCLAW_SYSTEM_PROMPT_OVERRIDE`` verbatim when
    it is set, so an empty string means "no OpenClaw prompt" while an unset
    variable means the stock one.
    """
    return "off" if os.environ.get("OPENCLAW_SYSTEM_PROMPT_OVERRIDE") == "" else "on"


def tools() -> str:
    """Return which tools the agent can reach, as the Gateway will configure them."""
    return "srbench" if os.environ.get("SRBENCH_OPENCLAW_TOOLS", "").lower() == "srbench" else "all"


def prompt_cells():
    """Yield the SRBench-side prompt settings valid for this process.

    With OpenClaw's prompt suppressed, dropping the SRBench prompt too would
    leave the agent nothing but ground rules, so that half of the grid is only
    swept when OpenClaw's prompt is present.
    """
    for srbench in (False, True):
        if not srbench and openclaw_prompt() == "off":
            continue
        for guidance in (False, True):
            yield {"srbench": srbench, "guidance": guidance}


def variant(cell: dict[str, bool], repeat: int) -> str:
    """Name a cell after all four factors, so an output directory is self-describing."""
    return (
        f"calendar_oc-{openclaw_prompt()}"
        f"_srbench-{'on' if cell['srbench'] else 'off'}"
        f"_guidance-{'on' if cell['guidance'] else 'off'}"
        f"_tools-{tools()}"
        f"_rep{repeat}"
    )


# --- Calendar ---


def experiment_calendar():
    from srbench.benchmarks.calendar_scheduling.config import CalendarRunConfig

    for repeat in range(1, REPEATS + 1):
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
                variant=variant(cell, repeat),
            )


# --- Marketplace ---


def experiment_marketplace():
    return
    yield
