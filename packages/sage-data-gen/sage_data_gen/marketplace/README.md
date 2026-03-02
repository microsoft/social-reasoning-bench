# Marketplace Data Generation

Generates marketplace negotiation tasks for `sage-benchmark`.

## Quick Start

```bash
uv run --package sage-data-gen sagegen marketplace \
  --output-dir data/marketplace/final \
  --catalog-model trapi/gpt-4.1 \
  --context-model trapi/gpt-4.1
```

## Outputs

```text
data/marketplace/final/
  large.yaml           # full dataset (default: 280 tasks)
  small.yaml           # stratified subset (default: 21 tasks)
  _pipeline_outputs/   # intermediate step artifacts
```

## What Is LLM vs Deterministic

- LLM-based: catalog generation, buyer/seller context generation.
- Deterministic: task assembly, validation, stats, and overlap-bucket enforcement/fallbacks.

## Key Options

- `--total-tasks` (default: `280`)
- `--small-size` (default: `21`)
- `--catalog-size` (default: `24`)
- `--max-rounds` (default: `6`)
- `--max-concurrency` (default: `12`)
