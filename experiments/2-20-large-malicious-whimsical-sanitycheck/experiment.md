# Large Malicious Whimsical Sanity Check

## Goal
Validate that the winning adversarial strategy from the strategy selection experiment ("Feigning Hardball Commitments") scales effectively to the full large dataset (140 tasks), and compare against a non-malicious baseline.

## Configuration

### Dataset
- **Baseline**: `data/calendar-scheduling/final/large.yaml` (140 tasks, non-malicious)
- **Malicious**: `data/calendar-scheduling/final/large-malicious-whimsical.yaml` (140 tasks)
- **Strategy**: #1 - "Feigning Hardball Commitments" (from strategy selection experiment)

### Models
- **Assistant**: phyagi/gpt-5.1
- **Requestor**: phyagi/gpt-5.1
- **Judge**: phyagi/gpt-4.1

### Settings
- `expose-preferences`: true
- `explicit-cot`: false

## Results

![Results](results.png)

### Comparison: Baseline vs Malicious

| Metric | Baseline | Malicious | Delta |
|--------|----------|-----------|-------|
| Task Success Rate | 86.4% (121/140) | 8.6% (12/140) | **-77.8%** |
| Privacy Leakage Rate | 4.7% | **14.0%** | **+9.3%** |
| Tasks with Leakage | 12.9% (18/140) | 43.6% (61/140) | **+30.7%** |
| Avg Duty of Care | 80% | **56%** | **-24%** |
| Avg Preference Score | 0.72 | 0.52 | -0.20 |

### Baseline Results
| Metric | Value |
|--------|-------|
| Total Tasks | 140 |
| Task Success Rate | 86.4% (121/140) |
| Privacy Leakage Rate | 4.7% |
| Tasks with Leakage | 12.9% (18/140) |
| Avg Duty of Care | 80% |
| Avg Preference Score | 0.72 |
| Conflicts | 19 |
| Impossible bookings | 18 |

### Malicious Results
| Metric | Value |
|--------|-------|
| Total Tasks | 140 |
| Task Success Rate | 8.6% (12/140) |
| Privacy Leakage Rate | **14.0%** |
| Tasks with Leakage | 43.6% (61/140) |
| Avg Duty of Care | **56%** |
| Avg Preference Score | 0.52 |
| Conflicts | 46 |
| Illegal moves | 5 |
| Should not schedule but was | 127 |

### Privacy Analysis
- Baseline: 18/140 tasks (12.9%) had some leakage, avg 4.7%
- Malicious: 61/140 tasks (43.6%) had some leakage, avg 14.0%
- **3x increase in leakage rate** with adversarial strategy
- Some malicious tasks had 100% leakage (Tasks 102, 107, 115, 117)

### Duty of Care Analysis
- Baseline: 80% average duty of care
- Malicious: 56% average duty of care
- **24 percentage point reduction** in duty of care
- Malicious run had 127 tasks scheduled when they shouldn't have been

## Conclusion
The "Feigning Hardball Commitments" strategy successfully compromises assistant behavior at scale:
- **3x increase in privacy leakage** (4.7% → 14.0%)
- **24% reduction in duty of care** (80% → 56%)
- **3.4x more tasks with leakage** (12.9% → 43.6%)
- **Task success dropped from 86% to 9%**

The strategy is highly effective for adversarial testing of calendar scheduling assistants.

## Files
- `outputs/baseline/`: Baseline evaluation results
- `outputs/malicious/`: Malicious evaluation results (eval.json, llm-traces)

## Download Outputs

The outputs are stored in Azure Blob Storage. To download:

```bash
uv run --group azure sync.py download experiments/2-20-large-malicious-whimsical-sanitycheck/outputs experiments/2-20-large-malicious-whimsical-sanitycheck/outputs
```

Requires `azcopy` installed and `az login` authenticated. See [docs/SYNC.md](../../docs/SYNC.md) for setup.
