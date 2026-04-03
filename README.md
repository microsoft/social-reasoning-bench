# SAGE Benchmark

Evaluating social reasoning capabilities of LLM agents in multi-agent settings. SAGE measures task completion, privacy leakage, duty of care, and due diligence across three benchmarks: calendar scheduling, form filling, and marketplace negotiation.

## Install

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
git clone https://github.com/microsoft/sage.git
cd sage
uv sync --all-packages
```

## Quick Start

```bash
sagebench benchmark calendar \
    --data ./data/calendar-scheduling/final/small.yaml \
    --model gpt-4.1 \
    --limit 2
```

## [Documentation](docs/vitepress/)
