#!/usr/bin/env bash
# Wave validation script — run between waves to verify benchmarks work end-to-end.
#
# Usage: ./scripts/wave_validation.sh [wave_number]
#
# 1. Generates small datasets for each benchmark
# 2. Runs each benchmark on its generated data
# 3. Produces a validation report
#
set -euo pipefail

WAVE="${1:-0}"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
REPORT_DIR="outputs/wave_validation/wave_${WAVE}_${TIMESTAMP}"
MODEL="trapi/gpt-4.1"
JUDGE_MODEL="trapi/gpt-4.1"

mkdir -p "$REPORT_DIR"

echo "=== Wave $WAVE Validation ==="
echo "Report dir: $REPORT_DIR"
echo "Model: $MODEL"
echo ""

# ─────────────────────────────────────────────
# Step 1: Generate small datasets
# ─────────────────────────────────────────────
echo "──── Step 1: Data Generation ────"

echo "[1/3] Calendar data-gen (small)..."
GEN_CAL_DIR="$REPORT_DIR/datagen/calendar"
uv run sagegen calendar \
  --num-companies 1 \
  --employees-per-company 1 \
  --small-size 1 \
  --medium-size 1 \
  --output-dir "$GEN_CAL_DIR" \
  2>&1 | tee "$REPORT_DIR/datagen_calendar.log" | tail -3
echo ""

echo "[2/3] Marketplace data-gen (small)..."
GEN_MKT_DIR="$REPORT_DIR/datagen/marketplace"
uv run sagegen marketplace \
  --total-tasks 3 \
  --small-size 2 \
  --output-dir "$GEN_MKT_DIR" \
  2>&1 | tee "$REPORT_DIR/datagen_marketplace.log" | tail -3
echo ""

echo "[3/3] Form-filling data-gen (skipped — uses existing tasks)"
# Form-filling generates per-form, not batch. Use existing small set.
FF_DATA="data/form-filling/tasks"
echo ""

# ─────────────────────────────────────────────
# Step 2: Run benchmarks
# ─────────────────────────────────────────────
echo "──── Step 2: Benchmark Runs ────"

echo "[1/3] Calendar benchmark..."
uv run sagebench calendar \
  --data "$GEN_CAL_DIR/small.yaml" \
  --model "$MODEL" \
  --judge-model "$JUDGE_MODEL" \
  --assistant-system-prompt default \
  --expose-preferences true \
  --limit 2 \
  --batch-size 2 \
  --output-dir "$REPORT_DIR/benchmark/calendar" \
  --logger quiet \
  2>&1 | tee "$REPORT_DIR/benchmark_calendar.log" | tail -5
echo ""

echo "[2/3] Marketplace benchmark..."
uv run sagebench marketplace \
  --data "$GEN_MKT_DIR/small.yaml" \
  --model "$MODEL" \
  --judge-model "$JUDGE_MODEL" \
  --limit 2 \
  --output-dir "$REPORT_DIR/benchmark/marketplace" \
  2>&1 | tee "$REPORT_DIR/benchmark_marketplace.log" | tail -5
echo ""

echo "[3/3] Form-filling benchmark (interactive)..."
uv run sagebench forms \
  --data "$FF_DATA" \
  --execution-mode interactive \
  --assistant-model "$MODEL" \
  --interviewer-model "$MODEL" \
  --judge-model "$JUDGE_MODEL" \
  --limit 1 \
  --batch-size 1 \
  --max-rounds 10 \
  --file-system \
  --output-dir "$REPORT_DIR/benchmark/form_filling" \
  2>&1 | tee "$REPORT_DIR/benchmark_formfilling.log" | tail -5
echo ""

# ─────────────────────────────────────────────
# Step 3: Generate report
# ─────────────────────────────────────────────
echo "──── Step 3: Validation Report ────"

uv run python3 - "$REPORT_DIR" <<'PYEOF'
import json, sys, glob
from pathlib import Path

report_dir = Path(sys.argv[1])

print(f"\n{'='*60}")
print(f"  WAVE VALIDATION REPORT")
print(f"  {report_dir.name}")
print(f"{'='*60}\n")

# Calendar results
cal_files = list(report_dir.glob("benchmark/calendar/**/eval.json"))
if cal_files:
    with open(cal_files[0]) as f:
        cal = json.load(f)
    summary = cal.get("summary", {})
    print("CALENDAR:")
    print(f"  Tasks: {summary.get('total_tasks', '?')}")
    print(f"  Valid: {summary.get('valid_tasks', '?')}")
    print(f"  Success rate: {summary.get('task_success_rate', '?')}")
    print(f"  Avg leakage: {summary.get('privacy_avg_leakage_rate', '?')}")
    print(f"  Avg DoC: {summary.get('fiduciary_avg_assistant_duty_of_care_score', '?')}")
    print()
else:
    print("CALENDAR: No eval.json found")
    # Try finding any json
    cal_jsons = list(report_dir.glob("benchmark/calendar/**/*.json"))
    if cal_jsons:
        print(f"  Found: {[str(p.relative_to(report_dir)) for p in cal_jsons]}")
    print()

# Marketplace results
mkt_files = list(report_dir.glob("benchmark/marketplace/**/results.json"))
if mkt_files:
    with open(mkt_files[0]) as f:
        mkt = json.load(f)
    summary = mkt.get("summary", {})
    print("MARKETPLACE:")
    print(f"  Tasks: {summary.get('task_count', '?')}")
    print(f"  Deal rate: {summary.get('deal_rate', '?')}")
    # Check for leakage scores
    results = mkt.get("results", [])
    if results:
        evals = [r.get("evaluation", {}) for r in results]
        buyer_leak = [e.get("buyer_leakage_score") for e in evals if e.get("buyer_leakage_score") is not None]
        seller_leak = [e.get("seller_leakage_score") for e in evals if e.get("seller_leakage_score") is not None]
        if buyer_leak:
            print(f"  Avg buyer leakage: {sum(buyer_leak)/len(buyer_leak):.2f}")
            print(f"  Avg seller leakage: {sum(seller_leak)/len(seller_leak):.2f}")
        else:
            print(f"  Leakage scores: not present (no --judge-model?)")
    print()
else:
    print("MARKETPLACE: No results.json found")
    mkt_jsons = list(report_dir.glob("benchmark/marketplace/**/*.json"))
    if mkt_jsons:
        print(f"  Found: {[str(p.relative_to(report_dir)) for p in mkt_jsons]}")
    print()

# Form-filling results
ff_files = list(report_dir.glob("benchmark/form_filling/**/eval_results.json"))
if ff_files:
    with open(ff_files[0]) as f:
        ff = json.load(f)
    if isinstance(ff, list) and ff:
        print("FORM-FILLING:")
        print(f"  Tasks evaluated: {len(ff)}")
        correctness = [r.get("correctness", {}).get("accuracy") for r in ff if r.get("correctness", {}).get("accuracy") is not None]
        privacy = [r.get("form_privacy", r.get("privacy", {})).get("privacy_score") for r in ff if r.get("form_privacy", r.get("privacy", {})).get("privacy_score") is not None]
        if correctness:
            print(f"  Avg correctness: {sum(correctness)/len(correctness):.2f}")
        if privacy:
            print(f"  Avg privacy: {sum(privacy)/len(privacy):.2f}")
    else:
        print(f"FORM-FILLING: eval_results.json is empty or not a list")
    print()
else:
    print("FORM-FILLING: No eval_results.json found")
    ff_jsons = list(report_dir.glob("benchmark/form_filling/**/*.json"))
    if ff_jsons:
        print(f"  Found: {[str(p.relative_to(report_dir)) for p in ff_jsons[:5]]}")
    print()

print(f"{'='*60}")
print(f"Full logs in: {report_dir}/")
print(f"{'='*60}")
PYEOF

# Save report path for easy reference
echo "$REPORT_DIR" > outputs/wave_validation/latest
echo ""
echo "Done. Report at: $REPORT_DIR"
