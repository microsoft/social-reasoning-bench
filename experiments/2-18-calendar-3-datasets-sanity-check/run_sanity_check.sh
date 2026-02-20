#!/bin/bash
# Sanity check — GPT models over all 3 dataset sizes
#
# Verifies pipeline correctness and establishes baseline numbers.
# Uses default prompt, benign data only, no special settings.
#
# Matrix:
#   2 assistant models × 3 datasets × 2 expose-prefs = 12 runs
set -e
cd "$(dirname "$0")/../.."

# Models 
ASSISTANT_MODELS=(
    "phyagi/gpt-4.1"
    "phyagi/gpt-5.1" 
) 

REQUESTOR_MODEL="phyagi/gpt-5.1"
# REQUESTOR_REASONING="medium"
JUDGE_MODEL="phyagi/gpt-4.1"

# All 3 dataset sizes
declare -A DATASETS
DATASETS["small"]="data/calendar-scheduling/final/small.yaml"
DATASETS["medium"]="data/calendar-scheduling/final/medium.yaml"
DATASETS["large"]="data/calendar-scheduling/final/large.yaml"

DATASET_ORDER=("small" "medium" "large")
# DATASET_ORDER=("small")


OUTPUT_BASE="outputs/calendar_scheduling/2-18-sanity"
BATCH_SIZE=32
MAX_ROUNDS=10


run_benchmark() {
    local assistant_model="$1"
    local data="$2"
    local output_dir="$3"
    local expose_prefs="$4"

    echo "Running: $output_dir"
    mkdir -p "$output_dir"


    sagebench calendar \
        --data "$data" \
        --assistant-model "$assistant_model" \
        --requestor-model "$REQUESTOR_MODEL" \
        --judge-model "$JUDGE_MODEL" \
        --assistant-system-prompt "default" \
        --expose-preferences "$expose_prefs" \
        --explicit-cot false \
        --batch-size "$BATCH_SIZE" \
        --max-rounds "$MAX_ROUNDS" \
        --output-dir "$output_dir"
}

echo "=========================================="
echo "Sanity Check — small / medium / large"
echo "=========================================="

for ASSISTANT_MODEL in "${ASSISTANT_MODELS[@]}"; do
    MODEL_SHORT="${ASSISTANT_MODEL##*/}"
    echo ""
    echo "=== Assistant: $MODEL_SHORT ==="

    for DATASET_NAME in "${DATASET_ORDER[@]}"; do
        DATA="${DATASETS[$DATASET_NAME]}"
        for EXPOSE_PREFS in true false; do
            echo ""
            echo "--- Dataset: $DATASET_NAME | expose-preferences: $EXPOSE_PREFS ---"
            run_benchmark "$ASSISTANT_MODEL" "$DATA" \
                "${OUTPUT_BASE}/${MODEL_SHORT}/${DATASET_NAME}/expose_prefs_${EXPOSE_PREFS}" \
                "$EXPOSE_PREFS"
        done
    done
done

echo ""
echo "=========================================="
echo "Sanity check complete!"
echo "Results in: $OUTPUT_BASE"
echo "=========================================="