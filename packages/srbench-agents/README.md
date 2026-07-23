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
| `OpenClawAgent` | `srbench_agents.openclaw_agent` | `npm install -g openclaw@2026.5.28` | [OpenClaw](https://github.com/openclaw/openclaw) CLI (subprocess) |

Each backend is an optional runtime, so install only what you need. The Claude
SDK is a Python extra; OpenClaw is a Node CLI (v2026.5.28, git
`e93216080aa1f425d3ab127014603eba8e365b2d`) that this package shells out to and
version-checks at runtime — there is no Python `openclaw` package.

## Usage

```bash
pip install 'srbench-agents[claude]'

srbench benchmark calendar \
    --assistant-agent srbench_agents.claude_agent:ClaudeAgent ...
srbench benchmark marketplace \
    --buyer-agent srbench_agents.claude_agent:ClaudeAgent ...
```

```bash
npm install -g openclaw@2026.5.28   # onboard it once: `openclaw onboard`

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

Reasoning effort maps to the Claude SDK `effort` option and to the OpenClaw
`agent --thinking <level>` flag respectively. Leave a variable unset to use the
backend's own default.

## How it works

The agents reuse `srbench.mcp.build_server`, which turns the environment's
granted `tools` plus its `invoke_tool` boundary into a standard MCP server. An
in-process agent (Claude) mounts that server directly; an external CLI agent
(OpenClaw) reaches it over streamable-HTTP (`srbench.mcp.serve_http`) and is
pointed at it via `openclaw mcp set`. Either way, no per-tool wiring is
required and all tool logic and validation stay in the srbench environment.
