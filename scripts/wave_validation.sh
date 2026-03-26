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

echo "[3/3] Form-filling data-gen (2 forms)..."
GEN_FF_DIR="$REPORT_DIR/datagen/form_filling/tasks"
# Pick 2 source images from existing tasks
FF_IMAGES=($(ls data/form-filling/tasks/*/image_*.png 2>/dev/null | head -2))
for img in "${FF_IMAGES[@]}"; do
  form_name=$(basename "$(dirname "$img")")
  echo "  Generating from $form_name..."
  uv run --package sage-data-gen sagegen form-filling \
    --image "$img" \
    --output-dir "$GEN_FF_DIR" \
    --filesystem \
    --no-html \
    --mask-fields 3 \
    2>&1 | tee -a "$REPORT_DIR/datagen_formfilling.log" | tail -1
done
FF_DATA="$GEN_FF_DIR"
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
  --explicit-cot false \
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
  --assistant-model "$MODEL" \
  --interviewer-model "$MODEL" \
  --judge-model "$JUDGE_MODEL" \
  --limit 2 \
  --batch-size 2 \
  --max-rounds 10 \
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

# Aligned metrics: Task Completion, Privacy Leakage, Duty of Care, Due Diligence
# (not all benchmarks support all metrics yet — report what's available)

def fmt(val, pct=False):
    if val is None: return "—"
    return f"{val:.0%}" if pct else f"{val:.2f}"

# ── Calendar ──
cal_files = list(report_dir.glob("benchmark/calendar/**/eval.json"))
if cal_files:
    with open(cal_files[0]) as f:
        cal = json.load(f)
    s = cal.get("summary", {})
    print("CALENDAR:")
    print(f"  Tasks: {s.get('valid_tasks', '?')}/{s.get('total_tasks', '?')}")
    print(f"  Task completion:  {fmt(s.get('task_success_rate'), pct=True)}")
    print(f"  Privacy leakage:  {fmt(s.get('privacy_avg_leakage_rate'), pct=True)}")
    print(f"  Duty of care:     {fmt(s.get('fiduciary_avg_assistant_duty_of_care_score'), pct=True)}")
    dd_msg = s.get('due_diligence_avg_message_count')
    dd_prop = s.get('due_diligence_avg_proposal_count')
    print(f"  Due diligence:    msgs={fmt(dd_msg)} proposals={fmt(dd_prop)}")
else:
    print("CALENDAR: No eval.json found")
print()

# ── Marketplace ──
mkt_files = list(report_dir.glob("benchmark/marketplace/**/results.json"))
if mkt_files:
    with open(mkt_files[0]) as f:
        mkt = json.load(f)
    s = mkt.get("summary", {})
    results = mkt.get("results", [])
    evals = [r.get("evaluation", {}) for r in results]
    print("MARKETPLACE:")
    print(f"  Tasks: {s.get('task_count', '?')}")
    print(f"  Task completion:  deal_rate={fmt(s.get('deal_rate'), pct=True)}")
    # Privacy
    buyer_leak = [e.get("buyer_leakage_score") for e in evals if e.get("buyer_leakage_score") is not None]
    seller_leak = [e.get("seller_leakage_score") for e in evals if e.get("seller_leakage_score") is not None]
    if buyer_leak:
        print(f"  Privacy leakage:  buyer={fmt(sum(buyer_leak)/len(buyer_leak))} seller={fmt(sum(seller_leak)/len(seller_leak))}")
    else:
        print(f"  Privacy leakage:  — (no --judge-model)")
    # DoC
    doc_vals = [e.get("deal_ratio_centered") for e in evals if e.get("deal_ratio_centered") is not None]
    if doc_vals:
        print(f"  Duty of care:     avg deal_ratio_centered={fmt(sum(doc_vals)/len(doc_vals))}")
    else:
        print(f"  Duty of care:     — (no deals or no ZOPA)")
    # DD
    offer_counts = [e.get("buyer_metrics", {}).get("offer_count", 0) + e.get("seller_metrics", {}).get("offer_count", 0) for e in evals]
    if offer_counts:
        print(f"  Due diligence:    avg total offers={fmt(sum(offer_counts)/len(offer_counts))}")
else:
    print("MARKETPLACE: No results.json found")
print()

# ── Form-Filling ──
ff_files = list(report_dir.glob("benchmark/form_filling/**/eval_results.json"))
if ff_files:
    with open(ff_files[0]) as f:
        ff = json.load(f)
    if isinstance(ff, list) and ff:
        # Handle nested 'evaluation' key (interactive mode)
        def get_eval(r):
            return r.get("evaluation", r)
        evs = [get_eval(r) for r in ff]
        print("FORM-FILLING:")
        print(f"  Tasks: {len(ff)}")
        # Task completion (correctness)
        acc = [e.get("correctness", {}).get("accuracy") for e in evs if e.get("correctness", {}).get("accuracy") is not None]
        print(f"  Task completion:  accuracy={fmt(sum(acc)/len(acc)) if acc else '—'}")
        # Privacy
        fp = [e.get("form_privacy", e.get("privacy", {})).get("privacy_score") for e in evs]
        fp = [x for x in fp if x is not None]
        cp = [e.get("conversation_privacy", {}).get("privacy_score") for e in evs]
        cp = [x for x in cp if x is not None]
        print(f"  Privacy leakage:  form={fmt(sum(fp)/len(fp)) if fp else '—'} conversation={fmt(sum(cp)/len(cp)) if cp else '—'}")
        # DoC
        doc = [e.get("duty_of_care", {}).get("min_score") for e in evs]
        doc = [x for x in doc if x is not None]
        print(f"  Duty of care:     min_score={fmt(sum(doc)/len(doc)) if doc else '—'}")
        # DD
        dd_acc = [e.get("due_diligence", {}).get("masked_field_accuracy") for e in evs]
        dd_acc = [x for x in dd_acc if x is not None]
        print(f"  Due diligence:    masked_field_accuracy={fmt(sum(dd_acc)/len(dd_acc)) if dd_acc else '—'}")
    else:
        print("FORM-FILLING: No results")
else:
    print("FORM-FILLING: No eval_results.json found")
print()

print(f"{'='*60}")
print(f"Full logs in: {report_dir}/")
print(f"{'='*60}")
PYEOF

# Save report path for easy reference
echo "$REPORT_DIR" > outputs/wave_validation/latest
echo ""
echo "Done. Report at: $REPORT_DIR"
