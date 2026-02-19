# Dev Setup

## Install

```bash
# Install uv if not used before
curl -LsSf https://astral.sh/uv/install.sh | sh

# clone and install
git clone https://github.com/microsoft/sage.git
cd sage
uv sync --packages
```

## Checks

Need to pass before PR.

```bash
# check formatting
uv run poe check-all

# try to auto-fix
uv run poe fix-all
```

## Running experiments with different models

**OpenAI models:**

Add `export OPENAI_API_KEY="..."` to your `.env` file at the root, then:

```bash
sagebench calendar \
    --model gpt-5.1 \
    # rest of required args...
```

**TRAPI models:**

```bash
--model trapi/msraif/shared/gpt-4.1
```

**PhyAGI models:**

Go to [https://playground.phyagi.net/login](https://playground.phyagi.net/login) and generate an API key. Add it to `.env` as `export PHYAGI_API_KEY="..."`.

```bash
--model phyagi/gpt-5.1
```

**Geimini models:**

Add `export GEMINI_API_KEY="..."` to your `.env` at root, then:

```bash
--model gemini-2.5-flash
```

**Anthropic models:**

Add `export ANTHROPIC_API_KEY="..."` to your `.env` at root, then:

```bash
--model claude-opus-4-5
```

The [sage-llm readme](../packages/sage-llm/README.md) has more details on other aliases you can use for model names.
