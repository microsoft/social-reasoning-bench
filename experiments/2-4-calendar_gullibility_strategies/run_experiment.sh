#!/bin/bash

# Experiment: Compare baseline vs gullibility strategies for privacy leakage
# Model: Gemini 2.5 Flash
# Prompts: privacy-strong, privacy-ci
# Runs: 100 baselines + 100 strategies per prompt

export GEMINI_API_KEY="${GEMINI_API_KEY:-your-api-key-here}"

BASE_OUTPUT_DIR="../../outputs/calendar_scheduling"
BASELINE="../../datasets/gullibility/privacy_extraction_template.yaml"
STRATEGY_DIR="../../datasets/gullibility/output/config_calendar"

run_experiment() {
    local PROMPT=$1
    local OUTPUT_DIR="$BASE_OUTPUT_DIR/2-4-gullibility_${PROMPT}"
    mkdir -p "$OUTPUT_DIR"

    echo "=============================================="
    echo "Running experiment with prompt: $PROMPT"
    echo "Output dir: $OUTPUT_DIR"
    echo "=============================================="

    # Run 100 strategies
    echo ""
    echo "=== Running 100 strategy files with $PROMPT ==="
    mapfile -t STRATEGIES < <(find "$STRATEGY_DIR" -name "*.yaml" | shuf | head -100)

    i=1
    for strategy in "${STRATEGIES[@]}"; do
        name=$(basename "$strategy" .yaml)
        OUTPUT_FILE="$OUTPUT_DIR/strategy-${name}.json"
        if [ -f "$OUTPUT_FILE" ]; then
            echo "Skipping strategy $i/100: $name (already exists)"
        else
            echo "Running strategy $i/100: $name..."
            sagebench calendar \
                --data "$strategy" \
                --model "gemini-2.5-flash" \
                --judge-model "gemini-2.5-flash" \
                --assistant-system-prompt "$PROMPT" \
                --expose-preferences false \
                --explicit-cot false \
                --max-rounds 10 \
                --output-dir "$OUTPUT_DIR"
            # Rename output file to include strategy name
            mv "$OUTPUT_DIR/${name}.json" "$OUTPUT_FILE" 2>/dev/null || true
        fi
        ((i++))
    done

    # Run 100 baselines
    echo ""
    echo "=== Running 100 baselines with $PROMPT ==="
    for i in {1..100}; do
        OUTPUT_FILE="$OUTPUT_DIR/baseline-run-${i}.json"
        if [ -f "$OUTPUT_FILE" ]; then
            echo "Skipping baseline $i/100 (already exists)"
        else
            echo "Running baseline $i/100..."
            sagebench calendar \
                --data "$BASELINE" \
                --model "gemini-2.5-flash" \
                --judge-model "gemini-2.5-flash" \
                --assistant-system-prompt "$PROMPT" \
                --expose-preferences false \
                --explicit-cot false \
                --max-rounds 10 \
                --output-dir "$OUTPUT_DIR"
            # Rename output file to baseline-run-N
            mv "$OUTPUT_DIR/privacy_extraction_template.json" "$OUTPUT_FILE" 2>/dev/null || true
        fi
    done

    echo ""
    echo "=== Completed $PROMPT ==="
}

# Run both prompts
run_experiment "privacy-strong"
run_experiment "privacy-ci"

echo ""
echo "=============================================="
echo "All experiments completed!"
echo "Results in: $BASE_OUTPUT_DIR/2-4-gullibility_*"
echo "=============================================="
