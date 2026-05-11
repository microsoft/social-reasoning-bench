# SocialReasoningBench

[![Docs](https://github.com/microsoft/social-reasoning-bench/actions/workflows/docs.yml/badge.svg)](https://github.io/microsoft/social-reasoning-bench)
[![Blog](https://img.shields.io/badge/Blog-coming_soon-blueviolet)](https://www.microsoft.com/en-us/research/blog/)

![hero](docs/vitepress/public/hero-light.png)

Evaluate the social reasoning capabilities of LLM agents in multi-party environments.

## Install

Requires Python 3.11+ and [uv](https://docs.astral.sh/uv/).

```bash
git clone https://github.com/microsoft/social-reasoning-bench.git
cd srbench
uv sync --all-packages --all-groups --all-extras
source .venv/bin/activate
```

## Usage

Evaluate the social reasoning ability of your own LLM. For example's sake, we'll assume your LLM is served as `my-model` via an OpenAI compatible endpoint at http://localhost:8000.

```bash
# To reproduce our results use Gemini as the counterparty.
GEMINI_API_KEY=<your api key>

# 3. Run the v0.1.0 experiment sweep with your model as the assistant
srbench experiment experiments/v0.1.0 \
    --output-base outputs/my-model
    --assistant-model openai/my-model \
    --assistant-base-url http://localhost:8000/v1 \
    --assistant-api-key none
    # To just test a few examples per experiment in the sweep
    # --set limit=10

# 4. View the results
srbench dashboard outputs/my-model
```

See [Installation](/installation), [Experiments](/experiments.md), and [LLMs](/llm.md) for detailed instructions.