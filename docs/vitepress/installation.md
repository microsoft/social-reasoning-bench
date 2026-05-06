# Installation

## Prerequisites

- **Python** >= 3.11
- **[uv](https://docs.astral.sh/uv/)** is a fast Python package manager

```bash
# Install uv if you don't have it
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Clone and Install

```bash
git clone https://github.com/microsoft/srbench.git
cd srbench
uv sync --all-packages
```

This installs all five workspace packages (`srbench`, `srbench-data-gen`, `srbench-llm`, `whimsygen`, `privacy-judge`) and their dependencies.

## Environment Variables

Set the API key for your model provider in a `.env` file at the repo root:

| Provider | Environment Variable | Example |
|----------|---------------------|---------|
| OpenAI | `OPENAI_API_KEY` | `export OPENAI_API_KEY="sk-..."` |
| Anthropic | `ANTHROPIC_API_KEY` | `export ANTHROPIC_API_KEY="sk-ant-..."` |
| Gemini | `GEMINI_API_KEY` | `export GEMINI_API_KEY="..."` |

## Model Name Formats

All CLI tools accept model names in these formats:

| Provider | Format | Example |
|----------|--------|---------|
| OpenAI | `{model}` or `openai/{model}` | `gpt-4.1` |
| Anthropic | `claude-*` or `anthropic/claude-*` | `claude-sonnet-4` |
| Gemini | `gemini-*` or `gemini/gemini-*` | `gemini-2.5-flash` |

See the [srbench-llm README](https://github.com/microsoft/srbench/tree/main/packages/srbench-llm) for full details on model routing.

## Verify Installation

Run a quick smoke test to confirm everything works:

```bash
srbench experiment experiment_smoke.py -k calendar --collect
```

This should list the calendar smoke experiment without executing it. To actually run it:

```bash
srbench experiment experiment_smoke.py -k calendar
```

## Development

```bash
# Check formatting and linting
uv run poe check-all

# Auto-fix issues
uv run poe fix-all
```
