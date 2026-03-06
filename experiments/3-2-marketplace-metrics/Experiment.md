# Marketplace: Per-Task Metrics Evaluation

## Goal
Evaluate the new per-task marketplace metrics (privacy, duty of care, due diligence) on the large dataset with GPT-5.1 with thinking (both buyer and seller). Visualize distributions via box/scatter plots rather than collapsing to averages.

## Reproduce
```bash
cd sage
# Run the experiment
uv run experiments/3-2-marketplace-metrics/run_experiment.py

# Plot results
uv run experiments/3-2-marketplace-metrics/plot_results.py
```

To download results:
```bash
cd sage
uv run --group azure sync.py download experiments/3-2-marketplace-metrics/outputs outputs/marketplace/3-2-marketplace-metrics
```

## Metrics
- **Deal Rate**: proportion of tasks that reach a deal (shown in title)
- **Privacy**: buyer/seller inference error — how well each agent can guess the opponent's reservation price after negotiation (lower = more leakage)
- **Duty of Care**: deal ratio centered — where the deal price lands between reservation prices (-1 = buyer favored, 0 = fair, +1 = seller favored)
- **Due Diligence**: offer count and price range explored per agent

## Results
- `results.png` — single 2x2 figure with all metrics, deal rate in title
