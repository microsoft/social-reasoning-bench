# Distribution of Duty of Care

## Motivation

Previous analyses report duty of care as a single average per condition. Averages can mask the underlying shape of the data — a mean of 0.50 could come from a uniform spread, or from scores clustered at 0 and 1 with nothing in between.

We plot the **distribution** of per-sample duty of care scores to understand:
- Is duty of care a continuous spectrum, or does it behave more like a binary outcome (fail hard or succeed)?
- Does exposing preferences or enabling negotiation change the *shape* of the distribution, or just shift its center?

## Datasets

Download the two datasets:

```bash
uv run sync.py download 2-4-simple-prefs outputs/calendar_scheduling/2-4-simple-prefs/

uv run sync.py download 2-10-negotiation outputs/calendar_scheduling/2-10-negotiation/
```

- **2-4-simple-prefs**: Baseline scheduling without negotiation (hidden and exposed preferences)
- **2-10-negotiation**: Scheduling with a malicious negotiation requestor (hidden and exposed preferences)

## Command to Run

```bash
uv run experiments/2-18-distribution_of_dutyofcare/plot_doc_distribution.py \
    outputs/calendar_scheduling/2-4-simple-prefs \
    outputs/calendar_scheduling/2-10-negotiation

# With per-model breakdown:
uv run experiments/2-18-distribution_of_dutyofcare/plot_doc_distribution.py \
    outputs/calendar_scheduling/2-4-simple-prefs \
    outputs/calendar_scheduling/2-10-negotiation \
    --per-model
```

## Results

![Distribution of Duty of Care](doc_distribution.png)

| Condition | N | Mean | Median | Std | BC |
|-----------|---|------|--------|-----|-----|
| Hidden Prefs | 105 | 0.50 | 0.28 | 0.36 | 0.771 * |
| Exposed Prefs | 105 | 0.82 | 1.00 | 0.34 | 0.893 * |
| Hidden + Negotiation | 105 | 0.34 | 0.17 | 0.41 | 0.812 * |
| Exposed + Negotiation | 105 | 0.28 | 0.22 | 0.33 | 0.768 * |

\* BC (bimodality coefficient) > 0.555 suggests bimodal distribution.

## Takeaways

1. **Duty of care is bimodal across all conditions.** Every condition has BC > 0.555. Scores cluster at the extremes — models either schedule optimally (near 1.0) or fail hard (near 0.0), with very little middle ground. This is consistent across all three models (gpt-4.1, gpt-4o, gpt-5.1).

2. **Exposing preferences does not change the bimodal shape — it simply shifts mass toward success.** The Hidden Prefs distribution has weight at both ends; the Exposed Prefs distribution has the same bimodal shape but with the overwhelming majority of mass at 1.0. Exposed preferences make success far more likely, but when the model still fails, it fails just as badly.

3. **Negotiation shifts mass toward failure and makes the bimodal split more pronounced.** Both negotiation conditions pile up near 0.0, but they still retain a tail at 1.0 — the gap in between widens. The bad outcomes get worse (median drops from 0.28 → 0.17 for hidden, 1.00 → 0.22 for exposed), while the few successes that survive negotiation still land near 1.0. The malicious requestor doesn't just lower the average — it polarizes outcomes further. Notably, exposed + negotiation performs *worse* than hidden + negotiation — the requestor exploits known preferences to push scheduling into the worst slots.

4. **The middle of the score range is mostly empty.** Across all conditions, the 0.4–0.8 range has very few samples. Duty of care behaves as a near-binary outcome: the model either finds a good slot or gets stuck with a bad one. There is no "partial credit" — scheduling outcomes are win-or-lose.
