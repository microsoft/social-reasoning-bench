# Sage-Benchmark

Benchmark your agent's social reasoning ability.

## Setup & Installation

From the root of this repo

```bash
uv sync --all-groups
```

Make sure you have API key environment variables set. The recommended approach is to put a .env file in the `sage-benchmark` folder. It will be loaded automatically.

```bash
export OPENAI_API_KEY="insert-key"
export GEMINI_API_KEY="insert-key"
```

## Run Evals

Run full form evals:

```bash
cd sage-benchmark
uv run -m sage_benchmark.form_filling --data ./data/form-filling/tasks/ --model gpt-4.1  --judge-model gpt-4.1
```

Run calendar scheduling evals:

```bash
cd sage-benchmark
uv run -m sage_benchmark.calendar_scheduling ./data/calendar-scheduling/calendar-tasks.yaml --max-rounds 10 --assistant-model gpt-4.1 --requestor-model gpt-4.1 --judge-model gpt-4.1
```

## Analyze Results

**Forms:**

Each experiment you run will make a folder with outputs in `outputs/form_filling`. The summary of the experiment is in `summary.json`. To aggregate and plot these results, you can run:

```bash
cd sage-benchmark
uv run ./analysis/form_filling/plot_results.py ./outputs/form_filling/
```

## Data Format

For more info on data format, see the [data folder](./data/Data_Format.md).
