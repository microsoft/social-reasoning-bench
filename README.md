# SocialReasoningBench

[![Docs](https://github.com/microsoft/social-reasoning-bench/actions/workflows/docs.yml/badge.svg?branch=main)](https://github.io/microsoft/social-reasoning-bench)
[![Blog](https://img.shields.io/badge/blog-coming_soon-blueviolet)](https://www.microsoft.com/en-us/research/blog/)

![hero](docs/vitepress/public/hero-light.png)

Evaluate the social reasoning capabilities of LLM agents in multi-agent environments.

## Install

Requires Python 3.11+ and [uv](https://docs.astral.sh/uv/).

```bash
git clone https://github.com/microsoft/social-reasoning-bench.git
cd srbench
uv sync --all-packages --all-groups --all-extras
source .venv/bin/activate
```

Copy `example.env` to `.env` and fill in API keys for whichever providers you'll use (`OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `GEMINI_API_KEY`, or `SRBENCH_AZURE_POOL_PATH`).

## Usage

### Run a benchmark

```bash
srbench benchmark calendar \
    --data data/calendar-scheduling/small.yaml \
    --model azure_pool/gpt-4.1 \
    --limit 2

srbench benchmark marketplace \
    --data data/marketplace/small.yaml \
    --model azure_pool/gpt-4.1 \
    --limit 2
```

For full usage details, checkout the [docs](https://github.io/microsoft/social-reasoning-bench)