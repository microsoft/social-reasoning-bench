# Privacy Leakage Sweep (3-6-refactor)

Evaluates how well different LLM assistants protect private calendar information
under benign, hand-crafted (HC), and whimsical (auto-generated) attack strategies.

## Cloud sync

```bash
# Download outputs
uv run --group azure sync.py download 3-6-refactor/ outputs/calendar_scheduling/3-6-refactor/

# Upload outputs
uv run --group azure sync.py upload outputs/calendar_scheduling/3-6-refactor/ 3-6-refactor/ --force
```

## Pipeline

Five scripts in two phases:

### Phase 1: Screen (per model)

#### `screen/data_gen.py` — Generate screening data

Filters base tasks to specific IDs, then injects each strategy into the task's requestor instructions (pure string templating, no LLM calls).

We require explicit task IDs because not all tasks are good screening candidates — some are unsatisfiable (e.g. task 0 has a fully packed calendar with no movable events), and others may not be representative of the broader dataset. Pick tasks that are satisfiable and representative. Task 20 is a good default (satisfiable, used in 3-5 screening).

```bash
uv run python experiments/3-6-refactor/screen/data_gen.py \
    --input data/calendar-scheduling/final/small.yaml \
    --task-ids 20
```

#### `screen/run.py` — Screen strategies and pick winner

Runs each strategy on the screening task(s) for N rounds. Selects the strategy with the highest leak rate. **Raises an error if no strategy leaks** (instead of silently picking a 0% "winner").

Screening is per-model: different models may be vulnerable to different strategies. Results are saved as `results/screening_results_<model-slug>.json`.

```bash
# Screen GPT-4.1 (with explicit CoT)
uv run python experiments/3-6-refactor/screen/run.py \
    --assistant-model phyagi/gpt-4.1 --assistant-explicit-cot

# Screen GPT-5.2
uv run python experiments/3-6-refactor/screen/run.py \
    --assistant-model phyagi/gpt-5.2 --assistant-reasoning-effort medium

# Screen Gemini 3 Flash
uv run python experiments/3-6-refactor/screen/run.py \
    --assistant-model gemini-3-flash-preview --assistant-reasoning-effort medium
```

Generation results:

| Model                   | Benign       | Mal-HC         | Mal-Whim       | Screening winner        |
| ----------------------- | ------------ | -------------- | -------------- | ----------------------- |
| GPT-4.1 (CoT)           | 0/140 (0.0%) | 10/140 (7.1%)  | 61/140 (43.6%) | strategy_61 (3/3, 100%) |
| GPT-5.2 (Medium)        | 1/140 (0.7%) | 7/140 (5.0%)   | 43/140 (30.7%) | strategy_40 (1/3, 33%)  |
| Gemini 3 Flash (Medium) | 7/140 (5.0%) | 45/140 (32.1%) | 76/140 (54.3%) | strategy_15 (3/3, 100%) |

### Phase 2: Validate

#### `experiment/data_gen.py` — Generate validation data

Injects the winning strategy into all tasks in the full dataset.

```bash
# Uses winner from screening results automatically
uv run python experiments/3-6-refactor/experiment/data_gen.py \
    --input data/calendar-scheduling/final/large.yaml

# Or force a specific strategy
uv run python experiments/3-6-refactor/experiment/data_gen.py \
    --input data/calendar-scheduling/final/large.yaml \
    --force-strategy strategy_40
```

#### `experiment/experiment_validate.py` — Privacy leakage sweep

Sweeps models × datasets × prompt strategies using the `sagebench calendar --experiments` runner.
Already-completed experiments are automatically skipped on re-run.

The sweep dimensions are configured at the top of the file:

- **`ASSISTANT_MODELS`**: which models to test (3 by default)
- **`PROMPTS`**: which prompt strategies to sweep (4 by default)
- **`DATASETS`**: benign, mal-hc-privacy, mal-whim-privacy

Use `-k` to filter to a subset:

```bash
# Run all 36 experiments (3 models × 3 datasets × 4 prompts = 36)
uv run sagebench calendar \
    --experiments experiments/3-6-refactor/experiment/experiment_validate.py

# Run CI-only: 9 experiments (3 models × 3 datasets × 1 prompt)
uv run sagebench calendar \
    --experiments experiments/3-6-refactor/experiment/experiment_validate.py \
    -k privacy-ci

# Run a single model, all datasets, CI only (3 experiments)
uv run sagebench calendar \
    --experiments experiments/3-6-refactor/experiment/experiment_validate.py \
    -k gpt5.2-medium_privacy-ci

# Run with a small task limit for testing
uv run sagebench calendar \
    --experiments experiments/3-6-refactor/experiment/experiment_validate.py \
    -k privacy-ci --limit 2

# List all experiments without running
uv run sagebench calendar \
    --experiments experiments/3-6-refactor/experiment/experiment_validate.py \
    --collect-only

# Override whimsical strategy winner
FORCE_STRATEGY=strategy_40 uv run sagebench calendar \
    --experiments experiments/3-6-refactor/experiment/experiment_validate.py
```

### Plot

```bash
uv run python experiments/3-6-refactor/plot.py

# Custom output path
uv run python experiments/3-6-refactor/plot.py --output results.png
```

# Full Experiment Sweep Results

Privacy

![privacy.png](privacy.png)
