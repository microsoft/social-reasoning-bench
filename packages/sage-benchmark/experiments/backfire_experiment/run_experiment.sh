#!/bin/bash

# Experiment: Backfire effect - do manipulation strategies cause models to
#             leak more private information, or do they backfire?
# Assistant models: GPT-4.1, GPT-4o, GPT-5.1, GPT-5.2, Gemini 2.5 Flash, Qwen2.5-7B-Instruct-CI
# System prompts: default, privacy-ci
# Tasks: 50 malicious calendar-scheduling tasks with manipulation strategies
# Each (model, prompt) pair produces one run

export GEMINI_API_KEY=""
export OPENAI_API_KEY="dummy"

STRATEGIES_TASKS="../../data/calendar-scheduling/generated/generated-tasks-strategies-50.yaml"

REQUESTOR_MODEL="gemini-3-flash-preview"
REASONING_EFFORT="high"
JUDGE_MODEL="trapi/msraif/shared/gpt-4.1"

BATCH_SIZE=32
MAX_ROUNDS=10

# Define assistant models, their short names, and optional base URLs
ASSISTANT_MODELS=(
    "trapi/msraif/shared/gpt-4.1"
    "trapi/msraif/shared/gpt-4o"
    "trapi/msraif/shared/gpt-5.1"
    "trapi/msraif/shared/gpt-5.2"
    "gemini-2.5-flash-preview"
    "openai/huseyinatahaninan/Qwen2.5-7B-Instruct-CI"
)

MODEL_SHORT_NAMES=(
    "gpt-4.1"
    "gpt-4o"
    "gpt-5.1"
    "gpt-5.2"
    "gemini-2.5-flash"
    "qwen"
)

# Base URLs: empty string means no --assistant-base-url flag
MODEL_BASE_URLS=(
    ""
    ""
    ""
    ""
    ""
    "http://localhost:8001/v1"
)


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
        --requestor-model $REQUESTOR_MODEL \
        --requestor-reasoning-effort $REASONING_EFFORT \
        --judge-model $JUDGE_MODEL \
        --assistant-system-prompt $prompt \
        --expose-preferences false \
        --explicit-cot false \
        --batch-size $BATCH_SIZE \
        --max-rounds $MAX_ROUNDS \
        --output-dir $output_dir"

    if [ -n "$ASSISTANT_BASE_URL" ]; then
        cmd="$cmd --assistant-base-url $ASSISTANT_BASE_URL"
    fi

    if [ -n "$limit" ]; then
        cmd="$cmd --limit $limit"
    fi

    eval $cmd

    cp "$output_dir/eval.json" "$result_file"
    echo "Saved: $result_file"
}

# Iterate over all assistant models
for i in "${!ASSISTANT_MODELS[@]}"; do
    ASSISTANT_MODEL="${ASSISTANT_MODELS[$i]}"
    MODEL_NAME="${MODEL_SHORT_NAMES[$i]}"
    ASSISTANT_BASE_URL="${MODEL_BASE_URLS[$i]}"
    BASE_OUTPUT_DIR="../../outputs/calendar_scheduling/${MODEL_NAME}"

    echo ""
    echo "=========================================="
    echo "Running model: $ASSISTANT_MODEL ($MODEL_NAME)"
    echo "=========================================="

    # Strategies + default
    echo ""
    echo "=== Strategies + default ==="
    run_benchmark "$STRATEGIES_TASKS" "default" \
        "${BASE_OUTPUT_DIR}-strategies-default" \
        "${BASE_OUTPUT_DIR}-strategies-default.json" \
        50

    # Strategies + privacy-ci
    echo ""
    echo "=== Strategies + privacy-ci ==="
    run_benchmark "$STRATEGIES_TASKS" "privacy-ci" \
        "${BASE_OUTPUT_DIR}-strategies-privacy-ci" \
        "${BASE_OUTPUT_DIR}-strategies-privacy-ci.json" \
        50
done

# Data analysis: backfire comparison for each model
echo ""
echo "=========================================="
echo "Running data analysis"
echo "=========================================="
for i in "${!ASSISTANT_MODELS[@]}"; do
    MODEL_NAME="${MODEL_SHORT_NAMES[$i]}"
    BASE_OUTPUT_DIR="../../outputs/calendar_scheduling/${MODEL_NAME}"
    DEFAULT_JSON="${BASE_OUTPUT_DIR}-strategies-default.json"
    CI_JSON="${BASE_OUTPUT_DIR}-strategies-privacy-ci.json"

    if [ -f "$DEFAULT_JSON" ] && [ -f "$CI_JSON" ]; then
        echo ""
        echo "=== Analysis: $MODEL_NAME ==="
        python data_analysis.py "$DEFAULT_JSON" "$CI_JSON" "$MODEL_NAME"
    else
        echo "SKIP analysis for $MODEL_NAME: result files not found"
    fi
done

echo ""
echo "=========================================="
echo "All done!"
echo "=========================================="
