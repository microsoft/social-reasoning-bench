#!/bin/bash
set -e

EXPERIMENT_DIR="$(cd "$(dirname "$0")" && pwd)"
MODEL="trapi/gpt-4.1"
INPUT="data/calendar-scheduling/final/small.yaml"
N=10

cd "$(git rev-parse --show-toplevel)"

mkdir -p "$EXPERIMENT_DIR/strategies"
mkdir -p "$EXPERIMENT_DIR/outputs"

# Phase 1: Run baseline (non-malicious)
echo "=== Running baseline evaluation ==="
uv run sagebench calendar \
  --data "$INPUT" \
  --assistant-model "$MODEL" \
  --requestor-model "$MODEL" \
  --judge-model "$MODEL" \
  --assistant-system-prompt default \
  --expose-preferences true \
  --explicit-cot false \
  --batch-size 21 \
  --max-rounds 10 \
  --output-dir "$EXPERIMENT_DIR/outputs/baseline"

# Phase 2: Generate and evaluate N strategies
for i in $(seq 0 $((N-1))); do
  echo ""
  echo "========================================"
  echo "=== Strategy $i of $((N-1)) ==="
  echo "========================================"

  STRATEGY_DIR="$EXPERIMENT_DIR/strategies/strategy_$i"
  mkdir -p "$STRATEGY_DIR"

  # Generate whimsical tasks with unique strategy
  echo "Generating whimsical tasks..."
  uv run --package sage-benchmark python -m data_gen.calendar_scheduling.malicious.whimsical \
    "$INPUT" \
    -m "$MODEL" \
    --strategy-assignment single \
    --data-dir "$STRATEGY_DIR" \
    -o "$STRATEGY_DIR/small-whimsical.yaml" \
    --rng-seed "$i"

  # Evaluate
  echo "Running evaluation..."
  uv run sagebench calendar \
    --data "$STRATEGY_DIR/small-whimsical.yaml" \
    --assistant-model "$MODEL" \
    --requestor-model "$MODEL" \
    --judge-model "$MODEL" \
    --assistant-system-prompt default \
    --expose-preferences true \
    --explicit-cot false \
    --batch-size 21 \
    --max-rounds 10 \
    --output-dir "$EXPERIMENT_DIR/outputs/strategy_$i"
done

# Phase 3: Analyze results
echo ""
echo "========================================"
echo "=== Analyzing results ==="
echo "========================================"
uv run python "$EXPERIMENT_DIR/analyze_results.py"
