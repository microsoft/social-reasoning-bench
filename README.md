# SAGE Benchmark

Evaluating social reasoning capabilities of LLM agents in multi-agent settings. SAGE measures **task completion**, **privacy leakage**, **duty of care**, and **due diligence** across three benchmarks:

- **Calendar scheduling** — an assistant protects private calendar events while negotiating meeting times with a requestor.
- **Form filling** — an assistant fills out forms from sensitive digital artifacts while an interviewer probes for information.
- **Marketplace negotiation** — a buyer and seller negotiate price while each hides a secret reservation price.

Each benchmark includes adversarial (hand-crafted and whimsical) variants that stress-test agent robustness across privacy, duty of care, and due diligence dimensions.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Environment Variables](#environment-variables)
- [Setting Up Azure Pool](#setting-up-azure-pool)
- [Concurrency and Throughput](#concurrency-and-throughput)
- [Generating Data](#generating-data)
- [Generating Malicious Data](#generating-malicious-data)
- [Running Experiments](#running-experiments)
- [Dashboard](#dashboard)
- [Development](#development)
- [Links](#links)

## Prerequisites

### Required

- **Python** >= 3.11
- **[uv](https://docs.astral.sh/uv/)** — fast Python package manager

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Optional

- **[Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli)** — needed for Azure pool setup (`az login` must succeed)
- **Node.js** — needed for local docs dev server

## Installation

```bash
git clone https://github.com/microsoft/sage.git
cd sage
uv sync --all-packages --all-groups --all-extras
# Prefer sourcing over using `uv run`
source .venv/bin/activate
```

This installs all five workspace packages, their dependencies, dev tools (ruff, pytest, ty, poe), and optional extras.

### Monorepo Structure

```
sage/
  packages/
    sage-benchmark/    # Benchmark runner, CLI, evaluation
    sage-data-gen/     # Data generation pipelines
    sage-llm/          # Multi-provider LLM client + Azure pool CLI
    whimsygen/         # Adversarial strategy generation
    privacy-judge/     # Privacy evaluation judges
  experiments/         # Experiment sweep definitions
  data/                # Benchmark task data
  scripts/             # Utility scripts (Azure pool, etc.)
  docs/vitepress/      # Full documentation site
```

## Environment Variables

Create a `.env` file at the repo root with API keys for your model provider(s) (see [`example.env`](example.env)):

| Provider | Variable |
|----------|----------|
| OpenAI | `OPENAI_API_KEY` |
| Anthropic | `ANTHROPIC_API_KEY` |
| Gemini | `GEMINI_API_KEY` |
| Azure pool | `SAGE_AZURE_POOL_PATH` |
| TRAPI | _(Azure AD auth — uses `az login`, no env var needed)_ |

Model name formats: `gpt-4.1`, `claude-sonnet-4`, `gemini-2.5-flash`, `trapi/gpt-4.1`, `azure_pool/gpt-5.4`. **`azure_pool/` is the recommended provider** — it load-balances across all Azure OpenAI deployments discovered by `sage-azure-pool`. See [sage-llm](packages/sage-llm/) for full details.

## Setting Up Azure Pool

The Azure Pool LLM provider discovers all Azure OpenAI deployments across your subscription and writes per-model JSON config files for load balancing.

```bash
# Prerequisites: log in and verify subscription access
az login --scope https://cognitiveservices.azure.com/.default

# Discover all deployments and write configs (default: configs/azure_pool/)
sage-azure-pool

# Specific models only
sage-azure-pool --models gpt-5.2 gpt-4.1

# Preview without writing files
sage-azure-pool --dry-run

# Custom account prefix or subscription
sage-azure-pool --prefix my-openai- --subscription <id>
```

Then add the pool path to your `.env`:

```
SAGE_AZURE_POOL_PATH=configs/azure_pool
```

Use pool models with the `azure_pool/` prefix: `--model azure_pool/gpt-4.1`.

## Concurrency and Throughput

SAGE uses a three-level concurrency model to maximize throughput, especially across Azure pool endpoints with many deployments:

| Level | Flag | Description | Suggested Default |
|-------|------|-------------|-------------------|
| **Batch** | `--batch-size` | Max parallel benchmark tasks | `200` |
| **Task** | `--task-concurrency` | Max concurrent LLM calls *within a single task* per provider | `5`–`10` |
| **LLM** | `--llm-concurrency` | Max total concurrent LLM calls per (provider, model) pair | `64` |

### How the levels interact

**Batch size** controls how many tasks run simultaneously. Each task involves a multi-turn agent conversation with multiple LLM calls.

**Task concurrency** prevents any single task from monopolizing the LLM pool. Without it, a task with many parallel judge calls or tool invocations could starve other tasks. Setting `--task-concurrency 5` means each task can have at most 5 in-flight LLM calls to a given provider, ensuring fair distribution across all tasks in the batch.

**LLM concurrency** is the global cap on concurrent API calls per (provider, model) pair. This is the starting point for the AIMD (Additive Increase / Multiplicative Decrease) controller, which automatically adjusts concurrency at runtime: it ramps up when calls succeed and backs off when rate limits or errors are hit. With Azure pool endpoints that spread load across many deployments, you can set this high (64+) and let AIMD find the optimal level.

### Maximizing throughput on Azure pool

For large runs across Azure pool endpoints:

```bash
sagebench experiment experiments/experiment_full.py \
    --batch-size 200 \
    --task-concurrency 5 \
    --llm-concurrency 64
```

The AIMD controller will automatically discover the throughput ceiling of your pool. Watch the periodic metrics log to see real-time throughput, concurrency levels, and in-flight counts per model.

### Per-provider tuning

Concurrency limits can also be set per-provider via environment variables:

```bash
SAGE_LLM_SIZE=64                  # default global LLM concurrency
SAGE_LLM_SIZE_OPENAI=30           # override for OpenAI
SAGE_LLM_SIZE_ANTHROPIC=10        # override for Anthropic
SAGE_LLM_TASK_SIZE=5              # default per-task limit
SAGE_LLM_TASK_SIZE_ANTHROPIC=3    # per-provider per-task override
```

### Monitoring throughput

Set `SAGE_METRICS_INTERVAL` to control how often (in seconds) throughput metrics are logged:

```bash
SAGE_METRICS_INTERVAL=60   # log every 60s (default: 120)
```

The metrics log reports per-model throughput (tok/s with 1m and 5m EMAs), average call duration, in-flight EMA, AIMD concurrency state, parallelism factor, and per-label token breakdowns (assistant, interviewer, judge, etc.). Set to `0` to disable.

## Generating Data

The `sagegen` CLI generates benchmark task data for all three domains.

### Calendar Scheduling

```bash
sagegen calendar --model azure_pool/gpt-4.1 --output-dir data/calendar-scheduling/
```

Produces `large.yaml`, `medium.yaml`, and `small.yaml` with tasks stratified by calendar fullness level (1–10 free slots). The pipeline generates companies, employees, calendars, and meeting requests through a 7-step process combining LLM generation with deterministic assembly.

| Option | Default | Description |
|--------|---------|-------------|
| `--model` | _(required)_ | Model for generation |
| `--output-dir` | `data/calendar-scheduling` | Output directory |
| `--num-companies` | `4` | Number of companies to generate |
| `--employees-per-company` | `5` | Employees per company |
| `--calendar-date` | `2026-02-20` | Base calendar date |
| `--fullness-levels` | `1,2,3,5,7,9,10` | Comma-separated free slot counts |
| `--medium-size` | `10` | Tasks per fullness level in medium dataset |
| `--small-size` | `3` | Tasks per fullness level in small dataset |
| `--judge-models` | `--model` | Comma-separated models for majority-vote privacy labeling |
| `--requestor-fullness` | `5` | Fixed free slots in requestor calendars |
| `--task-retry-limit` | `3` | Max retries per task on validation failure |
| `--seed` | `42` | Random seed |

### Form Filling

```bash
sagegen form-filling --output-dir data/form-filling -m azure_pool/gpt-4.1
```

Takes a form image, runs a multi-stage LLM pipeline (parse → generate ground truth → mask fields → generate scenario → create artifacts → validate → generate HTML form), and produces a complete evaluation task.

| Option | Default | Description |
|--------|---------|-------------|
| `--image` | — | Path to a single form image (PNG/JPEG) |
| `--batch` | _(bundled JSONL)_ | Path to `common_forms.jsonl` for batch generation |
| `-m, --model` | — | Default model for all roles |
| `--output-dir` | `.` | Output directory |
| `--form-id` | _(from filename)_ | Form ID (single-image mode only) |
| `--mask-fields` | `5` | Close-ended fields to mask |
| `--seed` | `42` | Random seed |
| `--parsing-model` | `-m` | Override model for form parsing |
| `--generation-model` | `-m` | Override model for data generation |
| `--validation-model` | `-m` | Override model for validation |
| `--vision-model` | `-m` | Override model for vision/OCR |
| `--no-html` | `false` | Skip HTML form generation |
| `--open-ended-only` | `false` | Keep only open-ended and masked due-diligence fields |
| `--secrets-per-field` | `2,5` | Min,max secrets per open-ended field |
| `--start` | `0` | Start index for batch processing |
| `--limit` | _(all)_ | Max forms to process in batch mode |
| `--concurrency` | `8` | Max concurrent forms for batch |

### Marketplace

```bash
sagegen marketplace --catalog-model azure_pool/gpt-4.1 --context-model azure_pool/gpt-4.1 --output-dir data/marketplace
```

Produces `large.yaml` and `small.yaml` with buyer-seller negotiation tasks. The pipeline generates product catalogs and reservation contexts with hidden price limits.

| Option | Default | Description |
|--------|---------|-------------|
| `--catalog-model` | _(required)_ | Model for catalog generation |
| `--context-model` | _(required)_ | Model for context generation |
| `--output-dir` | `data/marketplace` | Output directory |
| `--total-tasks` | `280` | Total tasks to generate |
| `--small-size` | `21` | Tasks in small dataset |
| `--max-rounds` | `6` | Maximum negotiation rounds |
| `--catalog-size` | `24` | Number of products in catalog |
| `--max-concurrency` | `12` | Parallel generation workers |
| `--max-retries-per-item` | `3` | Max retries for item generation |
| `--seed` | `42` | Random seed |

See the [full data generation docs](docs/vitepress/generating-data.md) for all CLI options and pipeline details.

## Generating Malicious Data

Each benchmark supports adversarial variants across three attack dimensions: `privacy`, `duty_of_care`, and `due_diligence`. Variants are generated using [WhimsyGen](docs/vitepress/whimsygen.md), which extracts creative adversarial strategies from Wikipedia articles.

```bash
sagegen malicious calendar \
    --input data/calendar-scheduling/small.yaml \
    -m azure_pool/gpt-4.1 \
    --batch-size 200 \
    --task-concurrency 5 \
    --llm-concurrency 64
```

| Option | Default | Description |
|--------|---------|-------------|
| `--attack-type` | _(all)_ | `privacy`, `duty_of_care`, or `due_diligence` (omit for all) |
| `-m, --model` | _(required)_ | LLM for strategy generation |
| `-n, --count` | `1` | Number of strategies to generate |
| `--strategy-assignment` | `single` | `sequential`, `random`, `unique`, or `single` |

### Validated Generation

Use `--validate` to automatically benchmark candidate strategies on a validation set and select the most effective one:

```bash
sagegen malicious calendar \
    --input data/calendar-scheduling/small.yaml \
    -m azure_pool/gpt-4.1 \
    --validate \
    --n-strategies 10 \
    --val-tasks-data data/calendar-scheduling/small.yaml \
    --val-tasks-limit 5 \
    --assistant-model azure_pool/gpt-4.1 \
    --judge-model azure_pool/gpt-4.1 \
    --batch-size 200 \
    --task-concurrency 5 \
    --llm-concurrency 64 \
    --logger progress \
    --log-level warning
```

This generates N candidate strategies, runs each against the validation tasks, and injects the best-performing strategy into the full task set.

| Option | Default | Description |
|--------|---------|-------------|
| `--validate` | off | Enable generate → benchmark → select pipeline |
| `--n-strategies` | _(required)_ | Number of candidate strategies to generate |
| `--val-tasks-data` | _(required)_ | Validation task YAML |
| `--val-tasks-limit` | _(all)_ | Max validation tasks per strategy |
| `--assistant-model` | `-m` | Model for the agent under test |
| `--assistant-reasoning-effort` | _(none)_ | Reasoning effort for assistant |
| `--assistant-explicit-cot` | `false` | Enable chain-of-thought for assistant |
| `--counterparty-model` | _(none)_ | Model for the counterparty agent |
| `--counterparty-reasoning-effort` | _(none)_ | Reasoning effort for counterparty |
| `--counterparty-explicit-cot` | `false` | Enable chain-of-thought for counterparty |
| `--judge-model` | `-m` | Model for the evaluation judge |
| `--judge-reasoning-effort` | _(none)_ | Reasoning effort for judge |
| `--val-output-dir` | _(auto)_ | Output directory for validation results |
| `--logger` | `progress` | `verbose`, `progress`, `quiet` |
| `--log-level` | `warning` | `debug`, `info`, `warning`, `error` |

## Running Experiments

### Single Benchmark

```bash
# Calendar scheduling
sagebench benchmark calendar \
    --data ./data/calendar-scheduling/small.yaml \
    --model azure_pool/gpt-4.1 \
    --batch-size 200 \
    --task-concurrency 5 \
    --llm-concurrency 64 \
    --limit 2

# Form filling
sagebench benchmark form_filling \
    --data ./data/form-filling/tasks.yaml \
    --model azure_pool/gpt-4.1 \
    --batch-size 200 \
    --task-concurrency 5 \
    --llm-concurrency 64 \
    --limit 2

# Marketplace
sagebench benchmark marketplace \
    --data ./data/marketplace/small.yaml \
    --model azure_pool/gpt-4.1 \
    --batch-size 200 \
    --task-concurrency 5 \
    --llm-concurrency 64 \
    --limit 2
```

#### Shared Options

These flags work across all three benchmarks:

| Option | Default | Description |
|--------|---------|-------------|
| `--data` | _(required)_ | YAML files or directories containing tasks |
| `--model` | _(required)_ | Default model for all agents |
| `--limit` | _(all)_ | Maximum number of tasks to run |
| `--batch-size` | `32` | Concurrent task count |
| `--max-rounds` | `20` | Maximum conversation rounds per task |
| `--max-steps-per-turn` | `20` | Maximum tool calls per agent turn |
| `--judge-model` | `--model` | Model for LLM-as-judge evaluation |
| `--judge-votes` | `3` | Majority vote count for judge |
| `--judge-reasoning-effort` | — | Reasoning effort for judge |
| `--system-prompt` | `none` | System prompt preset: `none`, `privacy`, `dd_info_gathering`, `dd_advocacy`, `oo` |
| `--reasoning-effort` | — | Reasoning effort for agent |
| `--explicit-cot` | — | Enable explicit chain-of-thought (`true`/`false`) |
| `--attack-types` | — | Hand-crafted attack types to inject at runtime |
| `--output-dir` | `outputs/` | Output directory |
| `--logger` | `progress` | Logging style: `verbose`, `progress`, `quiet` |
| `--log-level` | `warning` | `debug`, `info`, `warning`, `error` |

#### Calendar-Specific Options

| Option | Default | Description |
|--------|---------|-------------|
| `--assistant-model` | `--model` | Model for calendar assistant |
| `--requestor-model` | `--model` | Model for meeting requestor |
| `--assistant-reasoning-effort` | `--reasoning-effort` | Reasoning effort for assistant |
| `--requestor-reasoning-effort` | `--reasoning-effort` | Reasoning effort for requestor |
| `--assistant-explicit-cot` | `--explicit-cot` | Chain-of-thought for assistant |
| `--requestor-explicit-cot` | `--explicit-cot` | Chain-of-thought for requestor |
| `--expose-preferences` | `true` | Share scheduling preferences with assistant |

#### Form Filling-Specific Options

| Option | Default | Description |
|--------|---------|-------------|
| `--assistant-model` | `--model` | Model for form-filling assistant |
| `--interviewer-model` | `--model` | Model for interviewer |
| `--assistant-reasoning-effort` | `--reasoning-effort` | Reasoning effort for assistant |
| `--interviewer-reasoning-effort` | `--reasoning-effort` | Reasoning effort for interviewer |
| `--single-field-mode` | `false` | Fill one field at a time |
| `--eval-batch-size` | `0` (auto) | Concurrent evaluation work items per task. 0 = unlimited |

#### Marketplace-Specific Options

| Option | Default | Description |
|--------|---------|-------------|
| `--buyer-model` | `--model` | Model for buyer agent |
| `--seller-model` | `--model` | Model for seller agent |
| `--buyer-reasoning-effort` | `--reasoning-effort` | Reasoning effort for buyer |
| `--seller-reasoning-effort` | `--reasoning-effort` | Reasoning effort for seller |

### Experiment Sweeps

Experiment files define multiple benchmark runs. The runner pools tasks across all experiments for efficient execution.

```bash
# Run a smoke test (2 tasks per benchmark)
sagebench experiment experiments/experiment_smoke.py \
    --batch-size 200 --task-concurrency 5 --llm-concurrency 64

# Run the full sweep (benchmarks × attacks × system prompts × models)
sagebench experiment experiments/experiment_full.py \
    --batch-size 200 --task-concurrency 5 --llm-concurrency 64

# Preview without running
sagebench experiment experiments/experiment_full.py --collect

# Filter by pattern
sagebench experiment experiments/experiment_full.py -k calendar \
    --batch-size 200 --task-concurrency 5 --llm-concurrency 64

# Override models from the command line
sagebench experiment experiments/experiment_full.py --set model=azure_pool/gpt-5.4 \
    --batch-size 200 --task-concurrency 5 --llm-concurrency 64

# Cross-product across multiple models
sagebench experiment experiments/experiment_full.py \
    --set model=azure_pool/gpt-4.1 \
    --and \
    --set model=azure_pool/gpt-5.4 \
    --batch-size 200 --task-concurrency 5 --llm-concurrency 64
```

See [New Experiments](docs/vitepress/new-experiments.md) for how to write your own experiment files.

#### Experiment Options

| Option | Default | Description |
|--------|---------|-------------|
| `path` | _(required)_ | Path to experiment file or directory |
| `--collect` | off | List experiments without running |
| `-k` | — | Only run experiments matching this pattern |
| `--set key=value` | — | Override config fields across all experiments |
| `--and` | — | Separate override groups for cross-product |
| `--batch-size` | `100` | Concurrent tasks |
| `--task-concurrency` | _(unlimited)_ | Max concurrent LLM calls per task per provider |
| `--llm-concurrency` | _(unlimited)_ | Max total concurrent LLM calls per provider |
| `--output-base` | — | Base directory for outputs |
| `--restart-exec` | off | Re-run execution, ignore checkpoints |
| `--restart-eval` | off | Re-run evaluation, ignore checkpoints |
| `--logger` | `progress` | `verbose`, `progress`, `quiet` |
| `--log-level` | `warning` | `debug`, `info`, `warning`, `error` |

### Output

Each run produces an output directory under `--output-base` (default: `outputs/`):

```
# Single benchmark (sagebench benchmark)
outputs/{timestamp}-{variant}/
  results.json        # Config, evaluation, per-task results

# Experiment sweep (sagebench experiment)
outputs/{group_name}/{experiment_name}/
  results.json
outputs/{group_name}/sweep_metadata_{timestamp}.json
```

## Dashboard

After running experiments, launch the interactive dashboard to compare results:

```bash
sagebench dashboard
```

This opens an HTML dashboard in your browser. Load one or more `results.json` files to explore four visualization modes:

- **Radar charts** — all four metrics on a single chart per experiment
- **Bar charts** — individual metrics across experiments
- **Heatmaps** — color-coded grid of experiments vs. metrics
- **Distributions** — per-task score spreads within each experiment

Drag and reorder pivot chips to group data by model, variant, benchmark, or other dimensions.

## Development

```bash
# Check formatting, linting, and types
poe check

# Auto-fix formatting and lint issues
poe fix

# Run tests
pytest

# Local docs dev server (requires Node.js)
poe docs-dev
```

CI runs `poe check` on every push and PR to `main` (see `.github/workflows/check.yml`).

## Links

- **[Full Documentation](docs/vitepress/)** — VitePress site with architecture deep-dives, benchmark internals, and API reference
- **[License](LICENSE)** — MIT
- **[Security](SECURITY.md)** — Microsoft security reporting policy
