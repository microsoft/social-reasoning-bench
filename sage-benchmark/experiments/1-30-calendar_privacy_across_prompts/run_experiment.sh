#!/bin/bash

# Usage: ./run_experiment.sh [MODEL]
# Example: ./run_experiment.sh claude-sonnet-4-5
#          ./run_experiment.sh trapi/msraif/shared/gpt-4o

# Model configuration
MAIN_MODEL="${1:-trapi/msraif/shared/gpt-4o}"  # default to gpt-4o if not specified
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
    NORMAL_OUTPUT="${OUTPUT_DIR}/${MODEL_SHORT}-normal-${preset}.json"
    if [ -f "$NORMAL_OUTPUT" ]; then
        echo "Skipping $NORMAL_OUTPUT (already exists)"
    else
        uv run -m sage_benchmark.calendar_scheduling \
            "$NORMAL_DATA" \
            --model "$MAIN_MODEL" \
            --judge-model "$JUDGE_MODEL" \
            --assistant-system-prompt "$preset" \
            --batch-size "$BATCH_SIZE" \
            --max-rounds 10 \
            --output "$NORMAL_OUTPUT"
    fi

    # Malicious data
    MALICIOUS_OUTPUT="${OUTPUT_DIR}/${MODEL_SHORT}-malicious-${preset}.json"
    if [ -f "$MALICIOUS_OUTPUT" ]; then
        echo "Skipping $MALICIOUS_OUTPUT (already exists)"
    else
        uv run -m sage_benchmark.calendar_scheduling \
            "$MALICIOUS_DATA" \
            --model "$MAIN_MODEL" \
            --judge-model "$JUDGE_MODEL" \
            --assistant-system-prompt "$preset" \
            --batch-size "$BATCH_SIZE" \
            --max-rounds 10 \
            --output "$MALICIOUS_OUTPUT"
    fi
done
