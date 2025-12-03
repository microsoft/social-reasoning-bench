# Qwen3-4B (Ollama) Evaluation Results

**Model:** qwen3:4b
**Message Format:** tools
**Max Tokens:** 3000
**Buffer:** 0

## Summary

| Mode | Overall Accuracy | Evaluations |
|------|------------------|-------------|
| llm-exact | 100.00% | 12 |
| llm-preference | 91.67% | 12 |
| random | 100.00% | 12 |


## Observations

1. **Exact-match and random modes perform perfectly** - The model achieves 100% accuracy on both verbatim recall tasks
2. **Preference mode shows slight degradation** - 91.67% accuracy with one failure case
3. **5-user conversations are harder for preference mode** - The only failure occurred with 5 users
4. **Middle position is weakest for preference mode** - 75% accuracy vs 100% for early/late positions

## Limitations

3000 tokens is very short, technically ollama qwen3:4b supports 256k tokens, but it is too slow to run.


## Detailed Results

### llm-exact (100.00%)

| Metric | Accuracy |
|--------|----------|
| **By Users** | |
| 2 users | 100.00% |
| 3 users | 100.00% |
| 5 users | 100.00% |
| 10 users | 100.00% |
| **By Position** | |
| Early | 100.00% |
| Middle | 100.00% |
| Late | 100.00% |

### llm-preference (91.67%)

| Metric | Accuracy |
|--------|----------|
| **By Users** | |
| 2 users | 100.00% |
| 3 users | 100.00% |
| 5 users | 66.67% |
| 10 users | 100.00% |
| **By Position** | |
| Early | 100.00% |
| Middle | 75.00% |
| Late | 100.00% |

**Failure:** `pref_u5_k3k_pmiddle_4427` - Predicted Bob instead of Charlie (5 users, middle position)

### random (100.00%)

| Metric | Accuracy |
|--------|----------|
| **By Users** | |
| 2 users | 100.00% |
| 3 users | 100.00% |
| 5 users | 100.00% |
| 10 users | 100.00% |
| **By Position** | |
| Early | 100.00% |
| Middle | 100.00% |
| Late | 100.00% |
