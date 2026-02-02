#!/bin/bash

# Model configuration
MAIN_MODEL="trapi/msraif/shared/gpt-4o"
JUDGE_MODEL="trapi/msraif/shared/gpt-4.1"
MODEL_SHORT="${MAIN_MODEL##*/}"  # extracts model name from full path

# Test limit
BATCH_SIZE=32

# Output directory
OUTPUT_DIR="../../outputs/calendar_scheduling/1-30-privacy_across_prompts"
mkdir -p "$OUTPUT_DIR"

# Data files
NORMAL_DATA="../../data/calendar-scheduling/generated/generated-tasks.yaml"
MALICIOUS_DATA="../../data/calendar-scheduling/generated/generated-tasks-malicious-extraction.yaml"

for preset in 'default' 'privacy-simple' 'privacy-strong' 'privacy-ci'; do
    # Normal data
    uv run -m sage_benchmark.calendar_scheduling \
        "$NORMAL_DATA" \
        --model "$MAIN_MODEL" \
        --judge-model "$JUDGE_MODEL" \
        --assistant-system-prompt "$preset" \
        --batch-size "$BATCH_SIZE" \
        --max-rounds 10 \
        --output "${OUTPUT_DIR}/${MODEL_SHORT}-normal-${preset}.json"

    # Malicious data
    uv run -m sage_benchmark.calendar_scheduling \
        "$MALICIOUS_DATA" \
        --model "$MAIN_MODEL" \
        --judge-model "$JUDGE_MODEL" \
        --assistant-system-prompt "$preset" \
        --batch-size "$BATCH_SIZE" \
        --max-rounds 10 \
        --output "${OUTPUT_DIR}/${MODEL_SHORT}-malicious-${preset}.json"
done
