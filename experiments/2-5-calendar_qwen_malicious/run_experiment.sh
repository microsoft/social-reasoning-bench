#!/bin/bash

# Experiment: Compare baseline vs gullibility strategies for privacy leakage
# Model: Qwen 2.5 7B Instruct CI (with Gemini 3 Flash as requestor)
# Prompts: privacy-strong, privacy-ci
# Runs: 50 baselines + 50 strategies per prompt

export GEMINI_API_KEY=""
export OPENAI_API_KEY="dummy"

BASE_OUTPUT_DIR="../../outputs/calendar_scheduling/qwen"

NORMAL_TASKS="../../data/calendar-scheduling/generated/generated-tasks.yaml"
MALICIOUS_TASKS="../../data/calendar-scheduling/generated/generated-tasks-malicious-extraction.yaml"
STRATEGIES_TASKS="../../data/calendar-scheduling/generated/generated-tasks-malicious-with-strategies-authoritarian-50.yaml"

ASSISTANT_MODEL="openai/huseyinatahaninan/Qwen2.5-7B-Instruct-CI"
REQUESTOR_MODEL="gemini-3-flash-preview"
REASONING_EFFORT="high"
JUDGE_MODEL="trapi/msraif/shared/gpt-4.1"
ASSISTANT_BASE_URL="http://localhost:8001/v1"

BATCH_SIZE=32
MAX_ROUNDS=10


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
        --assistant-model $ASSISTANT_MODEL \
        --assistant-base-url $ASSISTANT_BASE_URL \
        --requestor-model $REQUESTOR_MODEL \
        --requestor-reasoning-effort $REASONING_EFFORT \
        --judge-model $JUDGE_MODEL \
        --assistant-system-prompt $prompt \
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


# 1. Normal + default
echo ""
echo "=== 1/6: Normal + default ==="
run_benchmark "$NORMAL_TASKS" "default" \
    "${BASE_OUTPUT_DIR}-normal-default" \
    "${BASE_OUTPUT_DIR}-normal-default.json" \
    50

# 2. Normal + privacy-ci
echo ""
echo "=== 2/6: Normal + privacy-ci ==="
run_benchmark "$NORMAL_TASKS" "privacy-ci" \
    "${BASE_OUTPUT_DIR}-normal-privacy-ci" \
    "${BASE_OUTPUT_DIR}-normal-privacy-ci.json" \
    50

# 3. Malicious + default
echo ""
echo "=== 3/6: Malicious + default ==="
run_benchmark "$MALICIOUS_TASKS" "default" \
    "${BASE_OUTPUT_DIR}-malicious-default" \
    "${BASE_OUTPUT_DIR}-malicious-default.json" \
    50

# 4. Malicious + privacy-ci
echo ""
echo "=== 4/6: Malicious + privacy-ci ==="
run_benchmark "$MALICIOUS_TASKS" "privacy-ci" \
    "${BASE_OUTPUT_DIR}-malicious-privacy-ci" \
    "${BASE_OUTPUT_DIR}-malicious-privacy-ci.json" \
    50

# 5. Strategies + default
echo ""
echo "=== 5/6: Strategies + default ==="
run_benchmark "$STRATEGIES_TASKS" "default" \
    "${BASE_OUTPUT_DIR}-strategies-default" \
    "${BASE_OUTPUT_DIR}-strategies-default.json" \
    50

# 6. Strategies + privacy-ci
echo ""
echo "=== 6/6: Strategies + privacy-ci ==="
run_benchmark "$STRATEGIES_TASKS" "privacy-ci" \
    "${BASE_OUTPUT_DIR}-strategies-privacy-ci" \
    "${BASE_OUTPUT_DIR}-strategies-privacy-ci.json" \
    50

echo ""
echo "=========================================="
echo "All done!"
echo "=========================================="
echo "All done!"
echo "=========================================="
