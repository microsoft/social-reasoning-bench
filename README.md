# SocialReasoningBench

Evaluate the social reasoning capabilities of LLM agents in multi-agent environments.

## Install

Requires Python 3.11+ and [uv](https://docs.astral.sh/uv/).

```bash
git clone https://github.com/microsoft/srbench.git
cd srbench
uv sync --all-packages --all-groups --all-extras
source .venv/bin/activate
```

Copy `example.env` to `.env` and fill in API keys for whichever providers you'll use (`OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `GEMINI_API_KEY`, or `SRBENCH_AZURE_POOL_PATH`).

## Usage

Everything goes through the unified `srbench` CLI:

```bash
srbench {benchmark,experiment,datagen,llm,dashboard} ...
```

### Run a benchmark

```bash
srbench benchmark calendar    --data data/calendar-scheduling/small.yaml --model azure_pool/gpt-4.1 --limit 2
srbench benchmark marketplace --data data/marketplace/small.yaml         --model azure_pool/gpt-4.1 --limit 2
```

### Run an experiment sweep

Experiment files define multiple runs and pool tasks across them.

```bash
srbench experiment experiments/experiment_smoke.py
srbench experiment experiments/experiment_full.py --batch-size 200 --task-concurrency 5 --llm-concurrency 64

srbench experiment experiments/experiment_full.py --collect              # preview without running
srbench experiment experiments/experiment_full.py -k calendar            # filter by pattern
srbench experiment experiments/experiment_full.py --set model=azure_pool/gpt-5.4
```

### Generate data

```bash
srbench datagen calendar    --model azure_pool/gpt-4.1 --output-dir data/calendar-scheduling/
srbench datagen marketplace --catalog-model azure_pool/gpt-4.1 --context-model azure_pool/gpt-4.1 --output-dir data/marketplace/

# Adversarial variants
srbench datagen malicious calendar --input data/calendar-scheduling/small.yaml -m azure_pool/gpt-4.1
```

### Populate Azure pool

Discovers Azure OpenAI deployments via `az` CLI and writes per-model JSON configs for load-balanced inference.

```bash
az login --scope https://cognitiveservices.azure.com/.default
srbench llm azure-pool populate                              # default: configs/azure_pool/
srbench llm azure-pool populate --models gpt-5.2 gpt-4.1
srbench llm azure-pool populate --dry-run
```

Then point `SRBENCH_AZURE_POOL_PATH=configs/azure_pool` in `.env` and use models with the `azure_pool/` prefix.

### Open the dashboard

```bash
srbench dashboard
```

Load one or more `results.json` files in your browser for radar/bar/heatmap/distribution comparisons.
