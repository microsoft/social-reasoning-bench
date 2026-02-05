#!/bin/bash

# Simple Calendar Duty of Care Experiment

# Model configuration
MODELS=("trapi/msraif/shared/gpt-4o" "trapi/msraif/shared/gpt-4.1" "trapi/msraif/shared/gpt-5.1")
JUDGE_MODEL="trapi/msraif/shared/gpt-4.1"
BATCH_SIZE=50

# Paths (relative to this script's directory)
DATA_DIR="../../data/calendar-scheduling/generated-simple-prefs"
OUTPUT_BASE="../../outputs/calendar_scheduling/2-4-simple-prefs"

mkdir -p "$OUTPUT_BASE"

echo "========================================"
echo "Simple Calendar Duty of Care Experiment"
echo "========================================"
echo "Data directory: $DATA_DIR"
echo "Output base: $OUTPUT_BASE"
echo "Models: ${MODELS[*]}"
echo "" 

for MODEL in "${MODELS[@]}"; do
    MODEL_SHORT="${MODEL##*/}"
    echo "========================================"
    echo "Running with model: $MODEL_SHORT"
    echo "========================================"

    # Run without exposed preferences
    echo ""
    echo ">>> Hidden preferences..."
    uv run -m sage_benchmark.calendar_scheduling \
        "$DATA_DIR" \
        --assistant-model "$MODEL" \
        --requestor-model "$MODEL" \
        --judge-model "$JUDGE_MODEL" \
        --assistant-system-prompt "default" \
        --batch-size "$BATCH_SIZE" \
        --max-rounds 10 \
        --explicit-cot false \
        --expose-preferences false \
        --output-dir "${OUTPUT_BASE}/${MODEL_SHORT}-hidden-prefs"

    # Run with exposed preferences
    echo ""
    echo ">>> Exposed preferences..."
    uv run -m sage_benchmark.calendar_scheduling \
        "$DATA_DIR" \
        --assistant-model "$MODEL" \
        --requestor-model "$MODEL" \
        --judge-model "$JUDGE_MODEL" \
        --assistant-system-prompt "default" \
        --batch-size "$BATCH_SIZE" \
        --max-rounds 10 \
        --explicit-cot false \
        --expose-preferences true \
        --output-dir "${OUTPUT_BASE}/${MODEL_SHORT}-exposed-prefs"
done

echo ""
echo "========================================"
echo "Experiment complete!"
echo "Results in: $OUTPUT_BASE"
echo "========================================"
