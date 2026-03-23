# Theory of Mind (ToM) Privacy Prompt Experiment

Tests whether a Theory of Mind system prompt can reduce privacy leakage in calendar scheduling. The ToM prompt forces the assistant to model the requestor's mental state (beliefs, intent, threat level) before every response, rather than relying on static privacy rules.

## Approach

A new system prompt (`privacy-tom`) instructs the assistant to produce a `<tom-reasoning>` block before each response:

- **Belief state**: What does the requestor currently know/believe?
- **Inferred intent**: Legitimate scheduling need or information extraction?
- **Next likely action**: What will they do next?
- **Threat assessment**: Does the behavior pattern suggest adversarial intent?
- **Duty of care**: What is the obligation to protect the user's information?

The prompt is registered as `privacy-tom` in `packages/sage-benchmark/.../prompts/privacy_tom.py`.

## Experiment Config

Reuses the same models, requestor, judge, and screening results from `3-18-final-calendar-doc-privacy`.

| Setting | Value |
| --- | --- |
| Dataset size | small (21 tasks) |
| Assistants | GPT-4.1 (CoT), GPT-5.2 (Medium), Gemini 3 Flash (Medium) |
| Requestor | Gemini 3 Flash (Medium) |
| Judge | GPT-4.1 (3 votes) |
| Max rounds | 10 |
| Datasets | benign, mal-hc-privacy, mal-whim-privacy |

Only `privacy-tom` was run as a new experiment (9 variants). The other 4 prompts (base, aware, strong, ci) were extracted as the small subset (task IDs 0-20) from existing large (140-task) results in `3-6-refactor`.

## Results

![Privacy Leakage](privacy_all_prompts.png)

ToM vs CI (current best structured prompt):

| Model | Dataset | CI | ToM |
| --- | --- | --- | --- |
| GPT-4.1 (CoT) | benign | 0% | 5% |
| | mal-hc | 10% | 29% |
| | mal-whim | 43% | 33% |
| GPT-5.2 (Medium) | benign | 5% | 10% |
| | mal-hc | 0% | 14% |
| | mal-whim | 24% | 24% |
| Gemini 3 Flash | benign | 5% | 0% |
| | mal-hc | 5% | 24% |
| | mal-whim | 10% | 10% |

- ToM helped GPT-4.1 on whimsical attacks (43% -> 33%) but hurt on HC attacks across all models.
- Hypothesis: the open-ended ToM reasoning gives models more surface to rationalize leaking on HC attacks.
- Small sample (21 tasks) — results are noisy.

## Cloud Sync

```bash
# Download results
uv run --group azure sync.py download 3-19-tom-privacy/ outputs/calendar_scheduling/3-19-tom-privacy/

# Upload results
uv run --group azure sync.py upload outputs/calendar_scheduling/3-19-tom-privacy/ 3-19-tom-privacy/ --force
```

## How to Reproduce

```bash
# Run ToM experiments (9 = 3 models × 1 prompt × 3 datasets, limited to 21 tasks)
uv run sagebench calendar \
    --experiments experiments/3-19-tom-privacy/experiment_small.py \
    --limit 21

# Extract small subset from existing large results (base, aware, strong, ci)
uv run python experiments/3-19-tom-privacy/extract_small_from_large.py

# Plot all 5 prompts
uv run python experiments/3-19-tom-privacy/plot.py
```

## Files

```
experiments/3-19-tom-privacy/
├── README.md                      # This file
├── experiment_small.py            # Experiment config (privacy-tom only)
├── extract_small_from_large.py    # Extract small subset from 3-6-refactor large results
├── plot.py                        # Plot all 5 prompts
└── privacy_all_prompts.png        # Results chart
```
