# Marketplace Benchmark

Minimal bilateral marketplace negotiation benchmark for `sage-benchmark`.

## Run

```bash
sagebench marketplace \
    --data ./data/marketplace/minimal_tasks.yaml \
    --model trapi/gpt-4.1 \
    --max-steps-per-turn 3
```

Results are written to `outputs/marketplace/run_<timestamp>/executions.json`.
