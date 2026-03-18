#!/usr/bin/env bash
# Run the full privacy leakage experiment pipeline from the repo root.
set -euo pipefail

# --- Step 1: Generate strategies ---
uv run python experiments/3-18-final-calendar-doc-privacy/privacy/1_generate/generate_strategies.py --count 100

# --- Step 2: Screen strategies ---
# 2a. Prepare screening data (inject strategies into task 20)
uv run python experiments/3-18-final-calendar-doc-privacy/privacy/2_screen/data_gen.py \
    --input data/calendar-scheduling/final/small.yaml \
    --task-ids 20

# 2b. Run screening per model
uv run python experiments/3-18-final-calendar-doc-privacy/privacy/2_screen/run.py \
    --assistant-model phyagi/gpt-4.1 --assistant-explicit-cot

uv run python experiments/3-18-final-calendar-doc-privacy/privacy/2_screen/run.py \
    --assistant-model phyagi/gpt-5.2 --assistant-reasoning-effort medium

uv run python experiments/3-18-final-calendar-doc-privacy/privacy/2_screen/run.py \
    --assistant-model gemini-3-flash-preview --assistant-reasoning-effort medium

# --- Step 3: Run experiments ---
# 3a. Generate experiment data (inject winning strategy into full dataset)
uv run python experiments/3-18-final-calendar-doc-privacy/privacy/3_experiment/data_gen.py \
    --input data/calendar-scheduling/final/large.yaml

# 3b. Run experiment sweep (36 experiments)
uv run sagebench calendar \
    --experiments experiments/3-18-final-calendar-doc-privacy/privacy/3_experiment/experiment_validate.py

# --- Step 4: Analyze ---
uv run python experiments/3-18-final-calendar-doc-privacy/privacy/4_analyze/plot.py
