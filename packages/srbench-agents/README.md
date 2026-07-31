# srbench-agents

Ready-to-run, LLM-driven **bring-your-own-agent (BYOA)** examples for
[`srbench`](../srbench/). Each agent implements the assistant-side contract
(`srbench.shared.BaseAssistantAgent`): it receives its private task through the
constructor and acts entirely through the `invoke_tool` callable it is handed in
`run(invoke_tool, tools)`. All tool logic and validation live in the srbench
environment; these agents only bridge an LLM's tool calls to that boundary.

Every agent is **generic over the task** — it reads whatever `AssistantTask` it
is given as JSON — so the same class drives the calendar *and* marketplace
benchmarks unchanged.

## Agents

| Agent | Module | Install | Backend |
| --- | --- | --- | --- |
| `ClaudeAgent` | `srbench_agents.claude_agent` | `pip install 'srbench-agents[claude]'` | [Claude Agent SDK](https://code.claude.com/docs/en/agent-sdk/python) (in-process) |
| `OpenClawAgent` | `srbench_agents.openclaw_agent` | `npm install -g openclaw@2026.5.28` | [OpenClaw](https://github.com/openclaw/openclaw) Gateway (WebSocket RPC) |

Each backend is an optional runtime, so install only what you need. The Claude
SDK is a Python extra; OpenClaw is a Node CLI (v2026.5.28, git
`e93216080aa1f425d3ab127014603eba8e365b2d`) that this package runs as a
long-lived Gateway process and version-checks at runtime — there is no Python
`openclaw` package.

## Usage

```bash
pip install 'srbench-agents[claude]'

srbench benchmark calendar \
    --assistant-agent srbench_agents.claude_agent:ClaudeAgent ...
srbench benchmark marketplace \
    --buyer-agent srbench_agents.claude_agent:ClaudeAgent ...
```

```bash
npm install -g openclaw@2026.5.28   # credentials come from the environment

srbench benchmark calendar \
    --assistant-agent srbench_agents.openclaw_agent:OpenClawAgent ...
srbench benchmark marketplace \
    --buyer-agent srbench_agents.openclaw_agent:OpenClawAgent ...
```

Provide the backend's credentials the usual way (e.g. `ANTHROPIC_API_KEY` for
Claude, or an onboarded OpenClaw model provider). Model and reasoning-effort
overrides are read from the environment:

| Agent | Model | Reasoning effort | Other |
| --- | --- | --- | --- |
| `ClaudeAgent` | `SRBENCH_CLAUDE_MODEL` | `SRBENCH_CLAUDE_REASONING_EFFORT` (`low`/`medium`/`high`/`xhigh`/`max`) | — |
| `OpenClawAgent` | `SRBENCH_OPENCLAW_MODEL` (`provider/model`) | `SRBENCH_OPENCLAW_REASONING_EFFORT` (`off`/`minimal`/`low`/`medium`/`high`/`xhigh`/`adaptive`/`max`) | `SRBENCH_OPENCLAW_BIN`, `SRBENCH_OPENCLAW_AGENT` |

Reasoning effort maps to the Claude SDK `effort` option and to OpenClaw's
thinking level respectively. Leave a variable unset to use the backend's own
default.

## How it works

The agents reuse `srbench.mcp.build_server`, which turns the environment's
granted `tools` plus its `invoke_tool` boundary into a standard MCP server. An
in-process agent (Claude) mounts that server directly; OpenClaw runs in a
separate process and reaches it over streamable-HTTP, registered through the
Gateway's `config.patch` RPC. Either way, no per-tool wiring is required and all
tool logic and validation stay in the srbench environment.

Each task holds one Gateway exclusively while it runs. A Gateway registers the
srbench MCP server exactly once, at a fixed loopback port it reserved on
startup; each task then serves *its own* tools at that port and tears the server
down afterwards. OpenClaw rediscovers the tool list on every run, so one task's
tools can never leak into another's. Registration is one-shot because the
Gateway rate-limits control-plane writes (`config.patch` and friends) to three
per minute — a per-task registration would throttle a sweep to a standstill.
Per-task model and thinking level ride on `sessions.create` / `sessions.patch`
instead, which are not rate limited.

The pool is sized by `SRBENCH_OPENCLAW_POOL_SIZE` (default `1`). Because a
Gateway is held exclusively for the duration of a task, raise it to match the
experiment's `batch_size` (the number of tasks run concurrently) — otherwise
concurrent tasks queue behind a single Gateway and run one at a time. Each
Gateway is a Node process, so size it deliberately.
