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

This experiment removes (2) in most cells and varies the rest. Where it does,
**SRBench composes the whole system prompt and OpenClaw sends exactly that**, so
OpenClaw's own prompt is not a variable and what remains is the benchmark's own
framing and the tools:

| factor | values | mechanism |
| --- | --- | --- |
| tools | srbench / sandbox | `SRBENCH_OPENCLAW_TOOLS` |
| delivery | system / user | `assistant_agent_kwargs` |
| SRBench system prompt | on / off | `assistant_agent_kwargs` |
| preference guidance | on / off | `assistant_agent_kwargs` |

`delivery` is why the grid is not a clean product. `system` is the arrangement
above. `user` is **OpenClaw as it ships**: its own ~36 KB prompt stands and the
benchmark's framing arrives in the opening user turn, which OpenClaw labels as
untrusted sender metadata. The benchmark's system text has nowhere else to go in
that arm, so `srbench-off` is not a condition it can express and it contributes
two cells, guidance on and off, rather than four.

Those two cells run under both `srbench` and `sandbox`. They are skipped only
under `all`, where the built-ins run on the host and the agent can read the
graded ground truth off disk. That risk belongs to `all` alone: `sandbox`
confines the built-ins to a container that cannot see the repository, and
`srbench` removes them outright, leaving nothing that can read a file.

**Twelve cells**: four prompt combinations times two tool settings, plus two
stock cells per tool setting. `ABLATION_REPEATS` (default 3) runs each cell more
than once. The dataset is `soft/large.yaml`, 140 tasks, so a default sweep is
**5,040 runs**.

The assistant is `phyagi/gpt-5.4` at `xhigh` reasoning effort, against the same
counterparty and judge as the published native runs. Override it with
`ABLATION_ASSISTANT_MODEL` and `ABLATION_ASSISTANT_EFFORT` to ablate the model
as well as the harness — a prompt or tool change that costs one model points may
cost another none, and a fixed-model sweep cannot tell the two apart. The model
is not part of a cell's name, so give each model its own `ABLATION_OUTPUT_BASE`;
every run records the model it used in its own config.

### What the system prompt contains

`CalendarOpenClawAgent` builds it from the same
`build_assistant_messages` the built-in agent uses, so the two harnesses cannot
drift apart:

| piece | when | source |
| --- | --- | --- |
| harness ground rules | always | `srbench_agents.prompts` |
| preset + `You are <name>'s calendar scheduling personal assistant.` | `srbench-on` | `build_assistant_messages` |
| `<user_preference>` explanation | `guidance-on`, soft tasks only | `CALENDAR_PREFERENCE_GUIDANCE` |

The ground rules are in every cell. They are the harness protocol contract
(call `Wait`, one action per turn, finish with `EndConversation`), not a prompt
treatment, and an agent that has not been told them cannot drive the
environment at all. So `srbench-off_guidance-off` is a real condition — protocol
and nothing else — rather than an agent left with no instructions.

In the stock (`delivery-user`) cells this same text is composed identically and
then prepended to the opening user turn instead, since OpenClaw's own prompt
occupies the system slot.

Each run records what it sent as the first entry of
`execution.assistant_context`, so a result carries the exact prompt that
produced it and can be checked against its own label. In the stock (`user`)
cells that entry is a marker naming OpenClaw's prompt by length and digest — its
operating manual is not pasted into a transcript the due-diligence judge reads,
because that would change what the judge sees in one arm only.

### Trace dumps

`run.sh` sets `SRBENCH_OPENCLAW_TRACE_DIR` to `<output base>/openclaw-traces`,
which turns on OpenClaw's cache trace and writes one JSON per task:

| key | what it holds |
| --- | --- |
| `system` | the system prompt as the provider received it, verbatim |
| `messages` | the full message array as sent, including OpenClaw's untrusted-sender wrapper and every tool call and result |
| `srbench_transcript` | the same run as the benchmark recorded it |

That is the only record of what the stock cells ran under, since OpenClaw builds
their prompt internally. Capture happens on cancellation too: the harness
cancels the agent the moment the conversation ends, so that — not a returning
turn — is the ordinary end of a run.

### Tool settings

| value | built-ins | runs on | can read the answer key |
| --- | --- | --- | --- |
| `srbench` | no | — | no |
| `sandbox` | yes | a Docker container | no |
| `all` | yes | the host, as you | **yes** |

The two swept settings ask different questions: `srbench` measures a
deliberately minimal agent, `sandbox` a fully equipped one.

`all` is what OpenClaw does when nothing is configured, and it is not swept.
Verified: unsandboxed, the model ran `hostname` and got the host, then read
`soft/large.yaml` — so a good score there might have been read off disk rather
than reasoned out, and nothing in the results distinguishes the two. Sandboxed,
`exec` still works but reports a container ID and the read is denied. Ask for it
with `ABLATION_TOOLS="all"` if the unrestricted default is itself the object of
study; do not compare its scores with the others.

The container's only mount is the Gateway's own scratch directory, writable so
the agent has somewhere to work — no repository, no Gateway config, no API key
in its environment. Note it is a plain debian-bookworm-slim box with bash, curl,
git, jq, python3, and ripgrep, so it is a different machine from the host rather
than a walled-off copy of it.

OpenClaw creates one container per task and prunes them on an idle timer
measured in hours, so a sweep would leave hundreds running. Gateway teardown
removes the ones it created, matched by their mount path.

## Setup

The eight `delivery-system` cells need an OpenClaw build that can have its
system prompt replaced. Stock OpenClaw cannot: `sessions.create` accepts only a
key and a model, `agents.defaults` has no system-prompt field, and the one
config value that suppresses the prompt (`promptMode: "none"`) also disables
tools. So build it from source with a small patch, pinned to the version the
agent asserts at runtime:

```bash
git clone https://github.com/openclaw/openclaw ~/openclaw          # if needed
cd ~/openclaw && git worktree add ~/openclaw-pinned e932160        # v2026.5.28
```

In `~/openclaw-pinned/src/agents/system-prompt.ts`, add a reader:

```ts
import { existsSync, readFileSync } from "node:fs";

function readSystemPromptOverride(): string | undefined {
  const path = process.env.OPENCLAW_SYSTEM_PROMPT_FILE;
  if (!path || !existsSync(path)) {
    return undefined;
  }
  return readFileSync(path, "utf8");
}
```

then return it at the top of `buildAgentSystemPrompt`:

```ts
const promptOverride = readSystemPromptOverride();
if (promptOverride !== undefined) {
  return promptOverride;
}
```

and short-circuit `appendModelIdentitySystemPrompt`, which runs *after*
`buildAgentSystemPrompt` and would otherwise append a `Current model identity:`
line the benchmark never wrote:

```ts
if (readSystemPromptOverride() !== undefined) {
  return params.systemPrompt;
}
```

A file rather than an environment variable because the prompt names the
principal and so differs per task, while a Node process's environment is fixed
at spawn. The Gateway writes it to its own state directory and the patch
re-reads it on every prompt build; a missing file means stock behavior, so an
unpatched or unconfigured run is unaffected.

Then build it (about five minutes) and point the benchmark at it:

```bash
cd ~/openclaw-pinned && pnpm install --frozen-lockfile && pnpm build
export SRBENCH_OPENCLAW_BIN=~/openclaw-pinned/openclaw.mjs
```

The `sandbox` cells need the sandbox image, built once:

```bash
cd ~/openclaw-pinned
docker build -t openclaw-sandbox:bookworm-slim -f scripts/docker/sandbox/Dockerfile scripts/docker/sandbox/
```

## Running

```bash
cd ~/social-reasoning-bench && set -a && source ~/.env && set +a
export SRBENCH_OPENCLAW_BIN=~/openclaw-pinned/openclaw.mjs

# smoke test: 3 tasks, one repeat, all twelve cells
ABLATION_REPEATS=1 experiments/openclaw-prompt-ablation/run.sh --set limit=3

# full run: 140 tasks x 12 cells x 3 repeats
experiments/openclaw-prompt-ablation/run.sh

# the unrestricted default, whose scores are not comparable
ABLATION_TOOLS="all" experiments/openclaw-prompt-ablation/run.sh

# a second model, into its own output base; -k srbench-on drops the
# ground_rules probe and leaves the eight cells that are a full 2x2x2
ABLATION_ASSISTANT_MODEL=phyagi/gpt-5.5 \
  ABLATION_OUTPUT_BASE=outputs/oc_gpt55_8cell \
  experiments/openclaw-prompt-ablation/run.sh -k srbench-on
```

`run.sh` walks the tool settings one process at a time, because the profile is
written into a Gateway's config when it starts and the pool outlives a single
variant. The prompt factors are swept inside each process.

Repeats are walked by `run.sh` as well, one process each. The collector
deduplicates configs by content and ignores the variant label, so three
identical cells yielded from one generator would silently collapse into one.

Each cell's factors are in its output directory name, e.g.
`calendar_delivery-system_srbench-off_guidance-on_tools-srbench_rep1`.
