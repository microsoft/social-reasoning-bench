#!/bin/bash
# Generate whimsical data files using pre-generated strategies.
#
# Usage:
#     ./experiments/2-25-split-whimsical/generate_data.sh
#
# Prerequisites:
#     Run generate_strategies.py first to create strategy files in strategies/privacy/
#     and strategies/duty_of_care/
#
# This script applies pre-generated strategies to calendar tasks sequentially.
# It does NOT generate new strategies - it only uses existing ones.

set -euo pipefail

EXPERIMENT_DIR="$(cd "$(dirname "$0")" && pwd)"
MODEL="gemini-3-flash-preview"
INPUT="data/calendar-scheduling/final/small.yaml"

cd "$(git rev-parse --show-toplevel)"

# Process each task type (privacy and duty_of_care)
for TASK_TYPE in privacy duty_of_care; do
    STRATEGIES_DIR="$EXPERIMENT_DIR/strategies/$TASK_TYPE"
    DATA_DIR="$EXPERIMENT_DIR/data/$TASK_TYPE"

    if [ ! -d "$STRATEGIES_DIR" ]; then
        echo "WARNING: Strategies directory not found: $STRATEGIES_DIR"
        echo "Run generate_strategies.py --task $TASK_TYPE first."
        continue
    fi

    N=$(ls -1 "$STRATEGIES_DIR"/strategy_*.yaml 2>/dev/null | wc -l | tr -d ' ')
    if [ "$N" -eq 0 ]; then
        echo "WARNING: No strategy files found in $STRATEGIES_DIR"
        echo "Run generate_strategies.py --task $TASK_TYPE first."
        continue
    fi

    mkdir -p "$DATA_DIR"

    echo "=== $TASK_TYPE: Applying $N pre-generated strategies ==="
    echo "Strategies directory: $STRATEGIES_DIR"
    echo "Output directory: $DATA_DIR"
    echo ""

    for i in $(seq 0 $((N-1))); do
        OUTPUT_FILE="$DATA_DIR/strategy_$i.yaml"
        STRATEGY_FILE="$STRATEGIES_DIR/strategy_$i.yaml"

        if [ -f "$OUTPUT_FILE" ]; then
            echo "[$TASK_TYPE $i/$((N-1))] Skipping strategy_$i (already exists)"
            continue
        fi

        if [ ! -f "$STRATEGY_FILE" ]; then
            echo "[$TASK_TYPE $i/$((N-1))] ERROR: Strategy file not found: $STRATEGY_FILE"
            continue
        fi

        echo "[$TASK_TYPE $i/$((N-1))] Applying strategy_$i..."

        uv run --package sage-data-gen python -m sage_data_gen.calendar_scheduling.malicious.whimsical."$TASK_TYPE" \
            "$INPUT" \
            -m "$MODEL" \
            --strategy-assignment single \
            --strategies-file "$STRATEGY_FILE" \
            -o "$OUTPUT_FILE"
    done

    echo ""
    echo "Done with $TASK_TYPE! Generated data files:"
    ls -la "$DATA_DIR/"
    echo ""
done
