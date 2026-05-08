# LLMs

`srbench` talks to OpenAI, Anthropic, Gemini, and Azure through a single client. This page covers everything you need to point it at the right provider.

## Provider keys

Set the API key for whichever providers you plan to use in your `.env`:

| Provider   | Environment variable        | Sign up |
|------------|-----------------------------|---------|
| OpenAI     | `OPENAI_API_KEY`            | [platform.openai.com](https://platform.openai.com/) |
| Anthropic  | `ANTHROPIC_API_KEY`         | [console.anthropic.com](https://console.anthropic.com/) |
| Gemini     | `GEMINI_API_KEY`            | [aistudio.google.com](https://aistudio.google.com/) |
| Azure pool | `SRBENCH_AZURE_POOL_PATH`   | See [Azure pool](#azure-pool) below |

You only need keys for the providers you actually plan to use.

## Model name format

The CLI flag is the same in every case — the prefix tells `srbench` which provider to route to:

| Provider   | Format                              | Example                  |
|------------|-------------------------------------|--------------------------|
| OpenAI     | `gpt-*` or `openai/gpt-*`           | `gpt-4.1`                |
| Anthropic  | `claude-*` or `anthropic/claude-*`  | `claude-sonnet-4-5`      |
| Gemini     | `gemini-*` or `gemini/gemini-*`     | `gemini-2.5-flash`       |
| Azure pool | `azure_pool/<deployment>`           | `azure_pool/gpt-4.1`     |

```bash
srbench benchmark calendar --model claude-sonnet-4-5 ...
srbench benchmark calendar --model azure_pool/gpt-4.1 ...
```

## Bring your own model

Any OpenAI-compatible server — vLLM, Ollama, LM Studio, a private gateway — works through the OpenAI provider. Two pieces:

1. Use the `openai/<your-model-name>` prefix so `srbench` routes through the OpenAI client without trying to match it against known `gpt-*` aliases.
2. Pass `--base-url` to point that client at your server.

```bash
srbench benchmark calendar \
    --model openai/meta-llama/Llama-3.1-70B-Instruct \
    --base-url http://localhost:8000/v1 \
    --data data/calendar-scheduling/small.yaml \
    --limit 2
```

`OPENAI_API_KEY` must still be set — most local servers ignore the value, so any non-empty string (e.g. `OPENAI_API_KEY=dummy`) is fine.

If you want different roles to hit different endpoints (e.g. an assistant model on vLLM and a judge on hosted OpenAI), use the per-role variants instead of the global `--base-url`: `--assistant-base-url`, `--requestor-base-url`, `--judge-base-url` for calendar; `--buyer-base-url`, `--seller-base-url`, `--judge-base-url` for marketplace.

## Azure pool

The Azure pool provider load-balances requests across multiple Azure OpenAI deployments — useful when one deployment's quota isn't enough for a long sweep.

Populate the pool config from your Azure subscription:

```bash
srbench llm azure-pool populate --output-dir configs/azure_pool
```

Then point `SRBENCH_AZURE_POOL_PATH` at the output directory in `.env`:

```bash
SRBENCH_AZURE_POOL_PATH=configs/azure_pool
```

After that, any model name prefixed with `azure_pool/` (e.g. `azure_pool/gpt-4.1`) will be routed across all populated deployments for that model.

## Concurrency

`srbench` enforces per-provider concurrency limits to avoid hammering rate limits. There are two knobs:

| Variable                  | What it controls                                      |
|---------------------------|-------------------------------------------------------|
| `SRBENCH_LLM_SIZE`        | Max concurrent calls per provider, total              |
| `SRBENCH_LLM_TASK_SIZE`   | Max concurrent calls per task                         |

Set defaults in `.env`:

```bash
SRBENCH_LLM_SIZE=64
SRBENCH_LLM_TASK_SIZE=5
```

Or override per run on the command line — these flags work on both `srbench benchmark` and `srbench experiment`:

```bash
srbench experiment experiments/v0.1.0 \
    --batch-size 200 \
    --task-concurrency 5 \
    --llm-concurrency 64
```

| Flag                  | What it maps to                          |
|-----------------------|------------------------------------------|
| `--llm-concurrency`   | `SRBENCH_LLM_SIZE`                       |
| `--task-concurrency`  | `SRBENCH_LLM_TASK_SIZE`                  |
| `--batch-size`        | Tasks executing in parallel              |

### Per-provider overrides

You can override either limit for a specific provider with a suffix:

```bash
SRBENCH_LLM_SIZE_OPENAI=128
SRBENCH_LLM_SIZE_ANTHROPIC=20
SRBENCH_LLM_TASK_SIZE_AZURE=3
```

Provider keys: `openai`, `anthropic`, `google`, `azure`.

### Tuning rule of thumb

- Start with whatever rate limit your provider enforces. Set `SRBENCH_LLM_SIZE` a little under it.
- If you see lots of timeouts or 429s, lower it.
- If utilization looks low and the provider isn't rate-limiting you, raise it.
- `SRBENCH_LLM_TASK_SIZE` only matters when each task makes many parallel LLM calls (e.g. with high judge vote counts). Leave it unset if unsure.
