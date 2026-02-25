#!/bin/bash
# Generate whimsical data files using pre-generated strategies.
#
# Usage:
#     ./experiments/2-20-whimsical-strategy-selection/generate_data.sh
#
# Prerequisites:
#     Run generate_strategies.py first to create strategy files in strategies/
#
# This script applies pre-generated strategies to calendar tasks sequentially.
# It does NOT generate new strategies - it only uses existing ones.

set -euo pipefail

EXPERIMENT_DIR="$(cd "$(dirname "$0")" && pwd)"
MODEL="gemini-3-flash-preview"
INPUT="data/calendar-scheduling/final/small.yaml"

cd "$(git rev-parse --show-toplevel)"

# Create output directory
mkdir -p "$EXPERIMENT_DIR/data"

# Count available strategies
STRATEGIES_DIR="$EXPERIMENT_DIR/strategies"
if [ ! -d "$STRATEGIES_DIR" ]; then
    echo "ERROR: Strategies directory not found: $STRATEGIES_DIR"
    echo "Run generate_strategies.py first to create strategy files."
    exit 1
fi

N=$(ls -1 "$STRATEGIES_DIR"/strategy_*.yaml 2>/dev/null | wc -l | tr -d ' ')
if [ "$N" -eq 0 ]; then
    echo "ERROR: No strategy files found in $STRATEGIES_DIR"
    echo "Run generate_strategies.py first to create strategy files."
    exit 1
fi

echo "Applying $N pre-generated strategies to tasks (sequential)..."
echo "Strategies directory: $STRATEGIES_DIR"
echo ""

for i in $(seq 0 $((N-1))); do
    OUTPUT_FILE="$EXPERIMENT_DIR/data/strategy_$i.yaml"
    STRATEGY_FILE="$STRATEGIES_DIR/strategy_$i.yaml"

    if [ -f "$OUTPUT_FILE" ]; then
        echo "[$i/$((N-1))] Skipping strategy_$i (already exists)"
        continue
    fi

    if [ ! -f "$STRATEGY_FILE" ]; then
        echo "[$i/$((N-1))] ERROR: Strategy file not found: $STRATEGY_FILE"
        continue
    fi

    echo "[$i/$((N-1))] Applying strategy_$i..."

    # Apply pre-generated strategy to tasks (loads from cache, no generation)
    uv run --package sage-benchmark python -m data_gen.calendar_scheduling.malicious.whimsical \
        "$INPUT" \
        -m "$MODEL" \
        --strategy-assignment single \
        --strategies-file "$STRATEGY_FILE" \
        -o "$OUTPUT_FILE"
done

echo ""
echo "Done! Generated data files:"
ls -la "$EXPERIMENT_DIR/data/"
