# PrivacyLens Evaluation Guideline

## Installation

```bash
uv sync
```

Or with vllm

```bash
uv sync --all-extras
```

## Command to Run

```bash
cd evaluations/privacy
python -m privacy_evals.run_all \
  --model_to_test <model_name> \
  --model_for_secret_extraction <model_name> \
  --model_for_rating <model_name> \
  --number_of_datapoints <num>
```

## Key Arguments

### Required Models
- `--model_to_test`: Model to be evaluated for privacy-preserving behavior (default: `gpt-4.1`)
- `--model_for_secret_extraction`: Model used to identify sensitive information from trajectories (default: `gpt-4.1`)
- `--model_for_rating`: Model used to evaluate leakage and helpfulness (default: `gpt-4.1`)
- vllm support for open-source models: vllm serve 'Qwen/Qwen3-4B-Instruct-2507' --tensor-parallel-size 1 --port 8001

### Dataset Parameters
- `--number_of_datapoints`: Number of datapoints to evaluate (default: 100000)
- `--input_data`: Path to input dataset (default: `../../datasets/privacylens/privacylens.json`)
- `--output_dir`: Directory for output files (default: `output`)

### Optional Flags
- `--eval_only`: Skip action generation and load existing results from file

## Example Usage

Evaluate GPT-4o on 50 datapoints:
```bash
cd evaluations/privacy
python -m privacy_evals.run_all \
  --model_to_test gpt-4o \
  --model_for_secret_extraction gpt-4.1 \
  --model_for_rating gpt-4.1 \
  --number_of_datapoints 50
```

## Evaluation Results

### Leakage Metrics
1. **Datapoints with leaks**: Number and percentage of datapoints with leak_rate > 0
2. **Average leak rate (all)**: Mean leak rate across all datapoints
3. **Average leak rate (leaked only)**: Mean leak rate for datapoints that leaked
4. **Variance of leak rate (all)**: Variance across all datapoints
5. **Variance of leak rate (leaked only)**: Variance across leaked datapoints

### Helpfulness Metrics
1. **Average helpfulness score**: Mean score across all datapoints
2. **Variance helpfulness score**: Variance across all datapoints
3. **Helpfulness by leak status**:
   - Average helpfulness for leaked datapoints
   - Average helpfulness for non-leaked datapoints
   - Variance for each group

## Output Files

Results are saved to `{output_dir}/{dataset_name}/`:
- `{model_name}_final_actions.json`: Generated actions from model_to_test
- `{rating_model}_{test_model}_leakage.json`: Leakage evaluation results
- `{rating_model}_{test_model}_helpfulness.json`: Helpfulness evaluation results


## LLM-as-Judge Prompt Updates

### Privacy Leakage Evaluation Changes
1. Include user instruction as context in leakage evaluation prompts
2. Count partial leakage as leakage (not just full disclosure)
3. Extract secrets from concrete vignette data instead of seed information
4. Use structured output (constraint decoding) for all LLM calls

### Before Change (First 10 Datapoints with 5 runs)

**Per-Model Results:**
| Model | Total Datapoints | Consistent | Inconsistent | Agreement Rate |
|-------|------------------|------------|--------------|----------------|
| gpt-4.1 | 10 | 7 | 3 | 0.7000 |
| gpt-4o | 10 | 9 | 1 | 0.9000 |
| gpt-5 (medium reasoning) | 10 | 7 | 3 | 0.7000 |

**Cross-Model Statistics:**
| Metric | Value |
|--------|-------|
| Total Datapoints (with consensus) | 6 |
| Cross-Model Agreement | 5 |
| Cross-Model Disagreement | 1 |
| Cross-Model Agreement Rate | 0.8333 |

### After Change (First 10 Datapoints)

**Per-Model Results:**
| Model | Total Datapoints | Consistent | Inconsistent | Agreement Rate |
|-------|------------------|------------|--------------|----------------|
| gpt-4.1 | 10 | 10 | 0 | 1.0000 |
| gpt-4o | 10 | 10 | 0 | 1.0000 |
| gpt-5 (medium reasoning) | 10 | 8 | 2 | 0.8000 |

**Cross-Model Statistics:**
| Metric | Value |
|--------|-------|
| Total Datapoints (with consensus) | 8 |
| Cross-Model Agreement | 8 |
| Cross-Model Disagreement | 0 |
| Cross-Model Agreement Rate | 1.0000 |

### Helpfulness Evaluation
- No changes to helpfulness scoring prompts
