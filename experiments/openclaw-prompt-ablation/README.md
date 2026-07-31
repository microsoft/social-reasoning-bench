# OpenClaw prompt and tool ablation

Running the calendar benchmark under the OpenClaw harness changes three things
at once, not one:

1. **The harness** — OpenClaw drives the agent loop instead of `LLMAgent`.
2. **The system prompt** — OpenClaw injects ~36 KB of its own standing
   instructions (heartbeats, group chats, memory, red lines) that the benchmark
   never sees and cannot override through config.
3. **The tools** — by default the benchmark's MCP tools are *added* to
   OpenClaw's built-ins rather than replacing them, so the agent can also
   `exec` a shell and `read` files. It will: a probe run had the model read
   `data/calendar-scheduling/soft/large.yaml`, the graded ground truth.

This experiment holds the harness fixed and varies the other two, alongside the
two SRBench prompt pieces, so each contribution can be read off separately.

| factor | values | mechanism |
| --- | --- | --- |
| OpenClaw system prompt | on / off | `OPENCLAW_SYSTEM_PROMPT_OVERRIDE` |
| tools | all / srbench | `SRBENCH_OPENCLAW_TOOLS` |
| SRBench system prompt | on / off | `assistant_agent_kwargs` |
| preference guidance | on / off | `assistant_agent_kwargs` |

Twelve cells: six prompt combinations (the two with *both* prompts off are
skipped — the agent would have no standing instructions to interpret) times two
tool settings. `ABLATION_REPEATS` runs each cell more than once.

## Setup

The "off" cells need an OpenClaw build that can have its system prompt
replaced. Stock OpenClaw cannot: `sessions.create` accepts only a key and a
model, `agents.defaults` has no system-prompt field, and the one config value
that suppresses the prompt (`promptMode: "none"`) also disables tools. So build
it from source with a six-line override, pinned to the version the agent
asserts at runtime:

```bash
git clone https://github.com/openclaw/openclaw ~/openclaw          # if needed
cd ~/openclaw && git worktree add ~/openclaw-pinned e932160        # v2026.5.28
```

Add this at the top of `buildAgentSystemPrompt` in
`~/openclaw-pinned/src/agents/system-prompt.ts`:

```ts
const promptOverride = process.env.OPENCLAW_SYSTEM_PROMPT_OVERRIDE;
if (promptOverride !== undefined) {
  return promptOverride;
}
```

Then build it (about five minutes) and point the benchmark at it:

```bash
cd ~/openclaw-pinned && pnpm install --frozen-lockfile && pnpm build
export SRBENCH_OPENCLAW_BIN=~/openclaw-pinned/openclaw.mjs
```

## Running

```bash
cd ~/social-reasoning-bench && set -a && source ~/.env && set +a
export SRBENCH_OPENCLAW_BIN=~/openclaw-pinned/openclaw.mjs

experiments/openclaw-prompt-ablation/run.sh --set limit=3   # smoke test
experiments/openclaw-prompt-ablation/run.sh                 # full 21-task run
```

`run.sh` walks the four Gateway-level combinations one process at a time,
because OpenClaw reads both its prompt override and its tool profile when a
Gateway starts and the pool outlives a single variant.

Each cell's four factors are in its output directory name, e.g.
`calendar_oc-on_srbench-off_guidance-on_tools-srbench_rep1`.
