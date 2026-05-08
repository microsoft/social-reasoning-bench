# Installation

## Prerequisites

- **Python** 3.11 or newer
- **[uv](https://docs.astral.sh/uv/)**

## Install

```bash
git clone https://github.com/microsoft/social-reasoning-bench.git srbench
cd srbench
uv sync --all-packages --all-groups --all-extras
source .venv/bin/activate
```

## Configure a model provider

Copy the example environment file and fill in keys for whichever provider(s) you use:

```bash
cp example.env .env
```

| Provider   | Environment variable        |
|------------|-----------------------------|
| OpenAI     | `OPENAI_API_KEY`            |
| Anthropic  | `ANTHROPIC_API_KEY`         |
| Gemini     | `GEMINI_API_KEY`            |
| Azure pool | `SRBENCH_AZURE_POOL_PATH`   |

You only need a key for the providers you actually plan to use. See [LLMs](/llm) for the full provider setup, model name formats, and the Azure pool.

## Verify

Run the smoke experiment to confirm everything works end-to-end:

```bash
# Assuming you set OPENAI_API_KEY
srbench experiment experiments/smoke --set model=openai/gpt-4.1
```

This runs two tasks each from the calendar and marketplace benchmarks. Results land in `outputs/`.

For long sweeps, see [LLMs › Concurrency](/llm#concurrency) for tuning per-provider rate limits.
