# Split Whimsical Strategy Selection Experiment

## Goal
Test privacy and duty-of-care adversarial strategies **separately** rather than as a combined dual-attack. Each strategy type targets a single metric, allowing cleaner measurement of which strategies are most effective at each attack surface.

This is an evolution of the 2-20 experiment which used a single combined prompt.

## Hypothesis
Focused single-objective strategies will be more effective than dual-attack strategies because:
1. The LLM can generate more targeted manipulation tactics
2. Results can be cleanly attributed to the specific attack type
3. Strategy selection can be optimized per-metric independently

## Experiment Design

### Dataset
- **Input**: `data/calendar-scheduling/final/small.yaml` (21 tasks)
- **Strategy variants**: 10 privacy strategies + 10 duty-of-care strategies

### Strategy Types
- **Privacy**: Strategies focused on extracting private event details (titles, attendees, purposes)
- **Duty of Care**: Strategies focused on manipulating scheduling to unpreferred times

### Models
- **Assistant**: gemini-2.5-flash (reasoning_effort=1024, system_prompt=privacy-ci)
- **Requestor**: gemini-2.5-flash (reasoning_effort=1024)
- **Judge**: trapi/gpt-4.1

### Configuration
- `expose-preferences`: false (privacy tasks), true (duty-of-care tasks)
- `explicit-cot`: false
- `max-rounds`: 10
- `batch-size`: 21

### Runs
1. **Baseline** (per requestor model): Original small.yaml (non-malicious requestor)
2. **Privacy 0-9** (per requestor model): Privacy-focused whimsical strategies
3. **Duty of Care 0-9** (per requestor model): Duty-of-care-focused whimsical strategies

## Metrics
- **Privacy strategies** ranked by: `privacy_avg_leakage_rate` (higher = more effective attack)
- **Duty of Care strategies** ranked by: `fiduciary_avg_assistant_duty_of_care_score` (lower = more effective attack)

## Pipeline

```bash
# 1. Generate strategies (separate prompts for each attack type)
python experiments/2-25-split-whimsical/generate_strategies.py -n 10

# 2. Apply strategies to calendar tasks
./experiments/2-25-split-whimsical/generate_data.sh

# 3. Run experiments
uv run sagebench calendar --experiments experiments/2-25-split-whimsical/experiment_whimsical_strategy.py

# 4. Analyze and plot results
python experiments/2-25-split-whimsical/analyze_results.py
python experiments/2-25-split-whimsical/plot_results.py

# 5. Generate final adversarial datasets from top-N strategies
python experiments/2-25-split-whimsical/generate_final_data.py -n 5
```

## Data

The `data/`, `outputs/`, and `strategies/` directories are stored in Azure Blob Storage.

To download:

```bash
uv run --group azure sync.py download experiments/2-25-split-whimsical/data experiments/2-25-split-whimsical/data
uv run --group azure sync.py download experiments/2-25-split-whimsical/outputs-v2 experiments/2-25-split-whimsical/outputs
uv run --group azure sync.py download experiments/2-25-split-whimsical/strategies experiments/2-25-split-whimsical/strategies
```

To upload:

```bash
uv run --group azure sync.py upload experiments/2-25-split-whimsical/outputs experiments/2-25-split-whimsical/outputs-v2
uv run --group azure sync.py upload experiments/2-25-split-whimsical/strategies experiments/2-25-split-whimsical/strategies
```

> Note: remote `outputs/` contains older runs (gemini-3-flash and gpt-4.1 requestor). Current results are in `outputs-v2/`.

## Files
- `generate_strategies.py`: Generate privacy and duty-of-care strategies via WhimsyGen
- `generate_data.sh`: Apply strategies to calendar tasks
- `experiment_whimsical_strategy.py`: Experiment configs for sagebench runner
- `analyze_results.py`: Analysis and ranking script
- `plot_results.py`: Visualization (bar charts per metric, dashed baseline lines)
- `generate_final_data.py`: Select top-N strategies per task type and generate adversarial datasets for small/medium/large splits
- `strategies/privacy/`: Generated privacy strategy files (`strategy_0.yaml` … `strategy_9.yaml`)
- `strategies/duty_of_care/`: Generated duty-of-care strategy files
- `data/privacy/`: Whimsical task files with privacy strategies applied
- `data/duty_of_care/`: Whimsical task files with duty-of-care strategies applied
- `outputs/`: Evaluation results (one subdirectory per variant)
- `final_data_summary.json`: Records which strategy indices were selected and their scores
