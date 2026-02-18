#!/bin/bash

# Model configuration
MODELS=("trapi/msraif/shared/gpt-4o" "trapi/msraif/shared/gpt-4.1")
JUDGE_MODEL="trapi/msraif/shared/gpt-4.1"
BATCH_SIZE=32

# Output directory
OUTPUT_DIR="../../outputs/calendar_scheduling/2-2-calendar_duty_of_care"
mkdir -p "$OUTPUT_DIR"

# Data file
DATA="../../data/calendar-scheduling/generated/generated-tasks.yaml"

for MODEL in "${MODELS[@]}"; do
    MODEL_SHORT="${MODEL##*/}"
    echo "Running experiments with model: $MODEL_SHORT (assistant and requestor)"

    # Run without exposed preferences
    uv run -m sage_benchmark.calendar_scheduling \
        "$DATA" \
        --assistant-model "$MODEL" \
        --requestor-model "$MODEL" \
        --judge-model "$JUDGE_MODEL" \
        --assistant-system-prompt "default" \
        --batch-size "$BATCH_SIZE" \
        --max-rounds 10 \
        --explicit-cot false \
        --expose-preferences false \
        --output-dir "${OUTPUT_DIR}/${MODEL_SHORT}-no-exposed-preferences"

    # Run with exposed preferences
    uv run -m sage_benchmark.calendar_scheduling \
        "$DATA" \
        --assistant-model "$MODEL" \
        --requestor-model "$MODEL" \
        --judge-model "$JUDGE_MODEL" \
        --assistant-system-prompt "default" \
        --batch-size "$BATCH_SIZE" \
        --max-rounds 10 \
        --explicit-cot false \
        --expose-preferences true \
        --output-dir "${OUTPUT_DIR}/${MODEL_SHORT}-exposed-preferences"
done
