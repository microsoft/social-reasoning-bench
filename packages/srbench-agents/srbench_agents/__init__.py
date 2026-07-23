"""Example "bring your own agent" (BYOA) implementations for srbench.

These modules demonstrate the assistant-side agent contract
(:class:`srbench.shared.BaseAssistantAgent`): an agent receives its private
task through its constructor and does everything else through the
``invoke_tool`` callable it is handed in :meth:`run`, learning about the world
only from the tool result strings the environment returns.

Each agent lives in its own module and depends on an optional third-party
runtime, so nothing is imported here eagerly:

- :mod:`srbench_agents.claude_agent` — :class:`ClaudeAgent`, built on the
  Claude Agent SDK (install with ``pip install 'srbench-agents[claude]'``).
- :mod:`srbench_agents.openclaw_agent` — :class:`OpenClawAgent`, which drives
  the OpenClaw CLI (``npm install -g openclaw@2026.5.28``) as a subprocess.

Every agent is *generic over the task*: it reads whatever
:class:`srbench.shared.AssistantTask` it is handed as JSON and therefore drives
*both* the calendar and marketplace benchmarks unchanged. Point a benchmark at
one with the CLI, e.g.::

    srbench benchmark calendar \\
        --assistant-agent srbench_agents.claude_agent:ClaudeAgent ...

    srbench benchmark marketplace \\
        --buyer-agent srbench_agents.claude_agent:ClaudeAgent ...
"""
