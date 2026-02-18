#!/bin/bash
# Gemini 2.5 Flash (thinking=high) - Full 3x2 experiment
# 3 task types: normal, malicious, strategies
# 2 system prompts: default, privacy-ci
set -e

# Requires GEMINI_API_KEY to be set in environment
if [ -z "$GEMINI_API_KEY" ]; then
    echo "Error: GEMINI_API_KEY environment variable is not set"
    exit 1
fi

cd "$(dirname "$0")/../.."

MODEL="gemini-2.5-flash"
JUDGE="trapi/msraif/shared/gpt-4.1"
BATCH_SIZE=16
MAX_ROUNDS=10
THINKING="high"

NORMAL_TASKS="data/calendar-scheduling/generated/generated-tasks.yaml"
MALICIOUS_TASKS="data/calendar-scheduling/generated/generated-tasks-malicious-extraction.yaml"
STRATEGIES_TASKS="data/calendar-scheduling/generated/generated-tasks-malicious-with-strategies-50.yaml"

OUTPUT_BASE="outputs/calendar_scheduling/gemini25-flash-high"

run_benchmark() {
    local tasks="$1"
    local prompt="$2"
    local output_dir="$3"
    local result_file="$4"
    local limit="$5"

    if [ -f "$result_file" ]; then
        echo "SKIP: $result_file already exists"
        return 0
    fi

    echo "Running: $result_file"
    mkdir -p "$output_dir"

    local cmd="sagebench calendar --data $tasks \
        --model $MODEL \
        --judge-model $JUDGE \
        --assistant-system-prompt $prompt \
        --assistant-reasoning-effort $THINKING \
        --expose-preferences false \
        --explicit-cot false \
        --batch-size $BATCH_SIZE \
        --max-rounds $MAX_ROUNDS \
        --output-dir $output_dir"

    if [ -n "$limit" ]; then
        cmd="$cmd --limit $limit"
    fi

    eval $cmd

    cp "$output_dir/eval.json" "$result_file"
    echo "Saved: $result_file"
}

echo "=========================================="
echo "Gemini 2.5 Flash (thinking=high) - 3x2 Matrix"
echo "=========================================="

# 1. Normal + default
echo ""
echo "=== 1/6: Normal + default ==="
run_benchmark "$NORMAL_TASKS" "default" \
    "${OUTPUT_BASE}-normal-default" \
    "${OUTPUT_BASE}-normal-default.json" \
    50

# 2. Normal + privacy-ci
echo ""
echo "=== 2/6: Normal + privacy-ci ==="
run_benchmark "$NORMAL_TASKS" "privacy-ci" \
    "${OUTPUT_BASE}-normal-privacy-ci" \
    "${OUTPUT_BASE}-normal-privacy-ci.json" \
    50

# 3. Malicious + default
echo ""
echo "=== 3/6: Malicious + default ==="
run_benchmark "$MALICIOUS_TASKS" "default" \
    "${OUTPUT_BASE}-malicious-default" \
    "${OUTPUT_BASE}-malicious-default.json" \
    50

# 4. Malicious + privacy-ci
echo ""
echo "=== 4/6: Malicious + privacy-ci ==="
run_benchmark "$MALICIOUS_TASKS" "privacy-ci" \
    "${OUTPUT_BASE}-malicious-privacy-ci" \
    "${OUTPUT_BASE}-malicious-privacy-ci.json" \
    50

# 5. Strategies + default
echo ""
echo "=== 5/6: Strategies + default ==="
run_benchmark "$STRATEGIES_TASKS" "default" \
    "${OUTPUT_BASE}-strategies-default" \
    "${OUTPUT_BASE}-strategies-default.json" \
    ""

# 6. Strategies + privacy-ci (SKIP - already done)
echo ""
echo "=== 6/6: Strategies + privacy-ci ==="
run_benchmark "$STRATEGIES_TASKS" "privacy-ci" \
    "${OUTPUT_BASE}-strategies-privacy-ci" \
    "${OUTPUT_BASE}-strategies-privacy-ci.json" \
    ""

echo ""
echo "=========================================="
echo "All done!"
echo "=========================================="
