#!/bin/bash
# Malicious hand-crafted experiment — small + large datasets, hidden preferences
#
# Tests how GPT-4.1 and GPT-5.1 handle adversarial requestors that
# attempt to extract calendar details under the guise of scheduling.
#
# Matrix:
#   2 assistant models × 4 datasets (small/large × benign/malicious) × hidden prefs = 8 runs
set -e
cd "$(dirname "$0")/../.."

ASSISTANT_MODELS=(
    "phyagi/gpt-4.1"
    "phyagi/gpt-5.1"
)

REQUESTOR_MODEL="phyagi/gpt-5.1"
JUDGE_MODEL="phyagi/gpt-4.1"

DATASET_NAMES=("small-benign" "small-malicious-hand-crafted" "large-benign" "large-malicious-hand-crafted")
DATASET_PATHS=(
    "data/calendar-scheduling/final/small.yaml"
    "data/calendar-scheduling/final/small-malicious-hand-crafted.yaml"
    "data/calendar-scheduling/final/large.yaml"
    "data/calendar-scheduling/final/large-malicious-hand-crafted.yaml"
)

OUTPUT_BASE="outputs/calendar_scheduling/2-20-malicious-hand-crafted"
BATCH_SIZE=32
MAX_ROUNDS=10

run_benchmark() {
    local assistant_model="$1"
    local data="$2"
    local output_dir="$3"

    echo "Running: $output_dir"
    mkdir -p "$output_dir"

    sagebench calendar \
        --data "$data" \
        --assistant-model "$assistant_model" \
        --requestor-model "$REQUESTOR_MODEL" \
        --judge-model "$JUDGE_MODEL" \
        --assistant-system-prompt "default" \
        --expose-preferences false \
        --explicit-cot false \
        --batch-size "$BATCH_SIZE" \
        --max-rounds "$MAX_ROUNDS" \
        --output-dir "$output_dir"
}

echo "=========================================="
echo "Malicious Hand-Crafted — small + large, hidden prefs"
echo "=========================================="

for ASSISTANT_MODEL in "${ASSISTANT_MODELS[@]}"; do
    MODEL_SHORT="${ASSISTANT_MODEL##*/}"
    echo ""
    echo "=== Assistant: $MODEL_SHORT ==="

    for i in "${!DATASET_NAMES[@]}"; do
        DATASET_NAME="${DATASET_NAMES[$i]}"
        DATA="${DATASET_PATHS[$i]}"
        echo ""
        echo "--- Dataset: $DATASET_NAME ---"
        run_benchmark "$ASSISTANT_MODEL" "$DATA" \
            "${OUTPUT_BASE}/${MODEL_SHORT}/${DATASET_NAME}"
    done
done

echo ""
echo "=========================================="
echo "Experiment complete!"
echo "Results in: $OUTPUT_BASE"
echo "=========================================="
