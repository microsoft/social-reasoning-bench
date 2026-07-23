# BYOA Experiments

A clone of the [`v0.1.0`](../v0.1.0/) experiment where the **assistant side** is
driven by *bring-your-own-agent* (BYOA) implementations from the
[`srbench-agents`](../../packages/srbench-agents/) package instead of the
built-in model-driven assistant. The counterparty, judge, attacks, defenses, and
data all mirror v0.1.0 so results are directly comparable.

Agents under test (a **model × reasoning-effort grid** per agent):

| Agent | Backend | Default sweep |
| --- | --- | --- |
| `srbench_agents.claude_agent:ClaudeAgent` | [Claude Agent SDK](https://code.claude.com/docs/en/agent-sdk/python) (in-process) | `claude-sonnet-4-6` × {low, medium, high} |
| `srbench_agents.openclaw_agent:OpenClawAgent` | [OpenClaw](https://github.com/openclaw/openclaw) CLI v2026.5.28 (subprocess) | `openai/gpt-5.4` × {low, medium, high} |

## Setup

```bash
# Claude agent (Python extra) + credentials
pip install 'srbench-agents[claude]'
export ANTHROPIC_API_KEY=...

# OpenClaw agent (Node CLI, pinned) + onboarding
npm install -g openclaw@2026.5.28
openclaw onboard          # configure a model provider
```

## Run

```bash
# Re-run experiments
srbench experiment experiments/byoa

# Outputs land in: outputs/byoa/<variant>

# Filter to one agent or benchmark with -k (substring match):
srbench experiment experiments/byoa -k claude
srbench experiment experiments/byoa -k marketplace_openclaw
```

## Model & reasoning effort

Unlike v0.1.0 (which sweeps built-in models via `assistant_model`), BYOA agents
receive their **model** and **reasoning effort per variant** through
`assistant_agent_kwargs` / `buyer_agent_kwargs`, which the harness forwards to
the agent constructor. The sweep is a **model × effort grid per agent**, defined
by the `AGENTS` list in [`experiment.py`](experiment.py) — add models or efforts
to any agent to widen it:

```python
AGENTS = [
    {
        "name": "claude",
        "agent": "srbench_agents.claude_agent:ClaudeAgent",
        "models": ["claude-sonnet-4-6"],
        "efforts": ["low", "medium", "high"],
    },
    {
        "name": "openclaw",
        "agent": "srbench_agents.openclaw_agent:OpenClawAgent",
        "models": ["openai/gpt-5.4"],           # provider/model; must be onboarded
        "efforts": ["low", "medium", "high"],
    },
]
```

- Claude `reasoning_effort` → SDK `effort` (`low`/`medium`/`high`/`xhigh`/`max`).
- OpenClaw `reasoning_effort` → CLI `agent --thinking <level>`
  (`off`/`minimal`/`low`/`medium`/`high`/`xhigh`/`adaptive`/`max`).

With the defaults this is 2 agents × 1 model × 3 efforts = **6 assistants**,
which — across the same attacks/styles/defenses as v0.1.0 and both benchmarks —
expands to **120 variants**.

The same per-variant override also works from the CLI for one-off runs:

```bash
srbench benchmark calendar \
    --assistant-agent srbench_agents.claude_agent:ClaudeAgent \
    --assistant-agent-kwargs '{"model": "claude-sonnet-4-6", "reasoning_effort": "high"}'
```

## Notes

- `DATA_SIZE` defaults to `"small"` because BYOA runs are heavier than
  model-only runs (OpenClaw spawns a Node subprocess and a local MCP server per
  task). Set it to `"large"` to match the v0.1.0 sweep exactly.
- `CONCURRENCY` is kept modest for the same reason; raise it if your machine and
  rate limits allow.
- Plots: the [v0.1.0 plotting scripts](../v0.1.0/plotting/) can be pointed at
  `outputs/byoa` to regenerate the same figures.
