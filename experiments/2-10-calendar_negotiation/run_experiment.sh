#!/bin/bash

# Calendar Duty of Care - Negotiation Experiment
# Tests whether a persistent, strategic requestor (gemini-3-flash-preview with thinking)
# can pressure the assistant into scheduling at suboptimal times.
#
# Runs two negotiation conditions per model:
#   1. Exposed prefs + malicious requestor
#   2. Hidden prefs + malicious requestor
# Hidden/exposed baseline results are pulled from the 2-4 experiment for plotting.

set -e

if [ -z "$GEMINI_API_KEY" ]; then
    echo "Error: GEMINI_API_KEY environment variable is not set"
    exit 1
fi

cd "$(dirname "$0")/../.."

# Assistant models to test
ASSISTANT_MODELS=("trapi/msraif/shared/gpt-4o" "trapi/msraif/shared/gpt-4.1" "trapi/msraif/shared/gpt-5.1")
JUDGE_MODEL="trapi/msraif/shared/gpt-4.1"
BATCH_SIZE=16
MAX_ROUNDS=10

# Negotiation requestor
NEGOTIATION_REQUESTOR="gemini-3-flash-preview"
NEGOTIATION_THINKING="high"

# Negotiation data files
DATA_DIR="data/calendar-scheduling/generated-simple-prefs"
NEGOTIATION_FILES=(
    "$DATA_DIR/fullness-00-free-slots-negotiation.yaml"
    "$DATA_DIR/fullness-01-free-slots-negotiation.yaml"
    "$DATA_DIR/fullness-03-free-slots-negotiation.yaml"
    "$DATA_DIR/fullness-05-free-slots-negotiation.yaml"
    "$DATA_DIR/fullness-07-free-slots-negotiation.yaml"
    "$DATA_DIR/fullness-09-free-slots-negotiation.yaml"
    "$DATA_DIR/fullness-11-free-slots-negotiation.yaml"
)

OUTPUT_BASE="outputs/calendar_scheduling/2-10-negotiation"

mkdir -p "$OUTPUT_BASE"

echo "================================================="
echo "Calendar Negotiation Experiment"
echo "================================================="
echo "Requestor: $NEGOTIATION_REQUESTOR (thinking=$NEGOTIATION_THINKING)"
echo "Assistant models: ${ASSISTANT_MODELS[*]}"
echo ""

for MODEL in "${ASSISTANT_MODELS[@]}"; do
    MODEL_SHORT="${MODEL##*/}"

    # Condition 1: Exposed prefs + negotiation requestor
    OUTPUT_DIR="${OUTPUT_BASE}/${MODEL_SHORT}-negotiation"
    if [ -f "$OUTPUT_DIR/eval.json" ]; then
        echo "SKIP: $OUTPUT_DIR/eval.json already exists"
    else
        echo "================================================="
        echo "Running: $MODEL_SHORT + negotiation requestor (exposed prefs)"
        echo "================================================="
        sagebench calendar \
            --data "${NEGOTIATION_FILES[@]}" \
            --assistant-model "$MODEL" \
            --requestor-model "$NEGOTIATION_REQUESTOR" \
            --requestor-reasoning-effort "$NEGOTIATION_THINKING" \
            --judge-model "$JUDGE_MODEL" \
            --assistant-system-prompt "default" \
            --batch-size "$BATCH_SIZE" \
            --max-rounds "$MAX_ROUNDS" \
            --explicit-cot false \
            --expose-preferences true \
            --output-dir "$OUTPUT_DIR" || true
    fi

    # Condition 2: Hidden prefs + negotiation requestor
    OUTPUT_DIR="${OUTPUT_BASE}/${MODEL_SHORT}-negotiation-hidden"
    if [ -f "$OUTPUT_DIR/eval.json" ]; then
        echo "SKIP: $OUTPUT_DIR/eval.json already exists"
    else
        echo "================================================="
        echo "Running: $MODEL_SHORT + negotiation requestor (hidden prefs)"
        echo "================================================="
        sagebench calendar \
            --data "${NEGOTIATION_FILES[@]}" \
            --assistant-model "$MODEL" \
            --requestor-model "$NEGOTIATION_REQUESTOR" \
            --requestor-reasoning-effort "$NEGOTIATION_THINKING" \
            --judge-model "$JUDGE_MODEL" \
            --assistant-system-prompt "default" \
            --batch-size "$BATCH_SIZE" \
            --max-rounds "$MAX_ROUNDS" \
            --explicit-cot false \
            --expose-preferences false \
            --output-dir "$OUTPUT_DIR" || true
    fi
done

echo ""
echo "================================================="
echo "Experiment complete!"
echo "Results in: $OUTPUT_BASE"
echo ""
echo "To plot results (pulls hidden/exposed baselines from 2-4 experiment):"
echo "  uv run analysis/plot_results.py"
echo "================================================="
