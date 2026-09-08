# srbench

Benchmark runner for evaluating LLM agents on calendar scheduling and marketplace negotiation. Provides parallel execution, checkpointing, resume, and LLM-as-judge evaluation across four dimensions: task completion, privacy, duty of care, and due diligence.

## Install

```bash
uv sync --all-packages
```

## Quick Start

```bash
# Run a single benchmark
srbench benchmark calendar \
    --data ./data/calendar-scheduling/small.yaml \
    --model gpt-4.1 \
    --limit 2

# Run an experiment sweep
srbench experiment experiment_smoke.py
```

## Bring your own assistant agent

The assistant side of each benchmark (the agent under evaluation) can be a class you provide. Implement `BaseAssistantAgent`, which requires only the `run(invoke_tool, tools)` coroutine. Your agent receives its private task through the constructor, and acts by calling `invoke_tool(name, arguments)` — a tool name plus a plain arguments dict — learning everything from the returned result string. All tool logic and validation lives in the environment: `invoke_tool` returns a result string for every expected outcome (success, unknown tool, bad arguments), so you never handle tool exceptions. The counterpart's opening move is waiting in the environment, so your first `Wait` returns it.

```python
# my_pkg/my_mod.py
from srbench.shared import BaseAssistantAgent
from srbench.benchmarks.calendar_scheduling.types import CalendarAssistantTask


class MyAgent(BaseAssistantAgent[CalendarAssistantTask]):
    def __init__(self, *, task):
        self.task = task

    async def run(self, invoke_tool, tools):
        opening = await invoke_tool("Wait", {})
        result = await invoke_tool(
            "ReplyMeeting",
            {"meeting_uid": "sync-001", "status": "ACCEPTED", "message": "Sure!"},
        )
        await invoke_tool("EndConversation", {"reason": "Meeting scheduled."})
```

Point the benchmark at it with an import string.

```bash
srbench benchmark calendar --assistant-agent my_pkg.my_mod:MyAgent ...
srbench benchmark marketplace --buyer-agent my_pkg.my_mod:MyBuyer ...
```

The calendar factory is called with `task=CalendarAssistantTask(...)`; the marketplace factory with `task=MarketplaceBuyerTask(...)`. Each task carries the agent's brief (e.g. the assistant profile or buyer instruction) and `max_actions`. The tool space and `invoke_tool` are delivered separately through `run`. Evaluation reads the environment's own records (emails, offers, action traces), so no transcript reporting is required.

### Worked example: a Claude agent that runs both benchmarks

The companion [`srbench-agents`](../srbench-agents/) package ships ready-to-run, LLM-driven example agents. `srbench_agents.claude_agent:ClaudeAgent` (built on the [Claude Agent SDK](https://code.claude.com/docs/en/agent-sdk/python)) is generic over the task and drives the calendar *and* marketplace benchmarks unchanged:

```bash
pip install 'srbench-agents[claude]'

srbench benchmark calendar --assistant-agent srbench_agents.claude_agent:ClaudeAgent ...
srbench benchmark marketplace --buyer-agent srbench_agents.claude_agent:ClaudeAgent ...
```

See the [`srbench-agents` README](../srbench-agents/README.md) for the full list of example agents and their configuration.

### Serving the environment's tools as an MCP server

If your agent framework speaks the [Model Context Protocol](https://modelcontextprotocol.io/), you don't have to hand-wire each tool. The optional `srbench.mcp` module turns the environment's granted `tools` and its `invoke_tool` boundary into a standard in-process MCP server:

```bash
pip install 'srbench[mcp]'
```

```python
from srbench.mcp import build_server, serve_stdio  # or serve_http for remote clients

async def run(self, invoke_tool, tools):
    server = build_server(tools, invoke_tool, name="srbench")
    # Mount `server` in-process (any MCP-speaking framework), expose it over
    # stdio, or serve it over streamable-HTTP for an out-of-process client:
    await serve_stdio(server)
```

`build_server` returns a raw `mcp.server.lowlevel.Server`; `serve_stdio` and `serve_http` (streamable-HTTP, for a CLI/subprocess client) run it over a transport. All tool logic and validation stay in the environment — the server forwards every call (even malformed ones) to `invoke_tool` and returns its result string verbatim. The example agents in [`srbench-agents`](../srbench-agents/) reuse this bridge (Claude mounts it in-process; OpenClaw reaches it over HTTP), so every framework shares exactly one bridge.

## [Documentation](../../docs/vitepress/)
