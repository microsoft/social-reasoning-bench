#!/bin/bash
# Run benchmark matrix: models x benchmarks
# Runs 1 task per benchmark for each model
#
# Usage: bash run_benchmark_matrix.sh > matrix.log 2>&1 && echo "All tests passed!" || echo "Some tests failed!"

LIMIT=1

# Track passed and failed commands
PASSED=()
FAILED=()

MODELS=(
    "trapi/msraif/shared/gpt-5.2_2025-12-11"
    "gpt-5.2"
    "gemini/gemini-2.5-flash"
)


echo "=========================================="
echo "Running benchmark matrix with limit=$LIMIT"
echo "=========================================="

for MODEL in "${MODELS[@]}"; do
    echo ""
    echo "=========================================="
    echo "Model: $MODEL"
    echo "=========================================="

    # Build model-specific args
    MODEL_ARGS="--model $MODEL"
    
    # Calendar Scheduling
    echo ""
    echo "--- Calendar Scheduling ---"
    if uv run -m sage_benchmark.calendar_scheduling \
        ./data/calendar-scheduling/calendar-tasks.yaml \
        $MODEL_ARGS \
        --limit "$LIMIT"; then
        PASSED+=("Calendar Scheduling ($MODEL)")
    else
        FAILED+=("Calendar Scheduling ($MODEL)")
    fi

    # Form Filling
    echo ""
    echo "--- Form Filling ---"
    if uv run -m sage_benchmark.form_filling \
        --data ./data/form-filling/tasks \
        $MODEL_ARGS \
        --limit "$LIMIT"; then
        PASSED+=("Form Filling ($MODEL)")
    else
        FAILED+=("Form Filling ($MODEL)")
    fi

    # Interviewer
    echo ""
    echo "--- Interviewer ---"
    if uv run -m sage_benchmark.interviewer \
        --data ./data/interviewer/tasks.yaml \
        --interviewer-model "$MODEL" \
        --assistant-model "$MODEL" \
        ${MODEL_ARGS/--model $MODEL/} \
        --limit "$LIMIT"; then
        PASSED+=("Interviewer ($MODEL)")
    else
        FAILED+=("Interviewer ($MODEL)")
    fi

done

echo ""
echo "=========================================="
echo "Benchmark matrix complete!"
echo "=========================================="
echo ""
echo "PASSED (${#PASSED[@]}):"
for item in "${PASSED[@]}"; do
    echo "  ✓ $item"
done
echo ""
echo "FAILED (${#FAILED[@]}):"
if [ ${#FAILED[@]} -eq 0 ]; then
    echo "  (none)"
else
    for item in "${FAILED[@]}"; do
        echo "  ✗ $item"
    done
fi
echo ""

if [ ${#FAILED[@]} -eq 0 ]; then
    echo "All tests passed!"
    exit 0
else
    echo "Some tests failed."
    exit 1
fi
