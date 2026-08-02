#!/usr/bin/env bash
#
# Run the OpenClaw prompt/tool ablation.
#
# The tool profile is written into a Gateway's config when it starts, and the
# Gateway pool outlives any one variant, so that factor cannot be swept inside a
# single srbench process. This walks the tool settings, one process each;
# experiment.py sweeps the SRBench prompt and the preference guidance inside
# each.
#
# Any extra arguments are forwarded to every run, e.g.
#
#     run.sh --set limit=3      # three tasks per cell, for a smoke test
#     run.sh --collect          # list the runs without executing them
#
# ABLATION_REPEATS is how many times each cell runs (default 3).
#
# ABLATION_TOOLS picks the tool settings to walk (default "srbench sandbox"):
#
#   srbench  built-ins removed; only the benchmark's MCP tools
#   sandbox  built-ins kept, but running in a Docker container that cannot
#            see the repository (needs the openclaw-sandbox image; see README)
#   all      built-ins running on the host, as you. Not swept by default: the
#            agent can read the graded ground truth off disk, so its scores
#            cannot be told apart from ones it earned. See README.
#
#     ABLATION_TOOLS="all" run.sh
#
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$HERE/../.." && pwd)"
OUTPUT_BASE="${ABLATION_OUTPUT_BASE:-outputs/openclaw_ablation}"

# Every cell sends a system prompt composed by srbench, which needs a build that
# honours OPENCLAW_SYSTEM_PROMPT_FILE; stock OpenClaw offers no way to replace
# its own system prompt. See README.md.
: "${SRBENCH_OPENCLAW_BIN:?set SRBENCH_OPENCLAW_BIN to the patched OpenClaw build}"

# One Gateway per concurrent task. experiment.py reads the same variable for
# batch size, so the two cannot disagree.
export SRBENCH_OPENCLAW_POOL_SIZE="${SRBENCH_OPENCLAW_POOL_SIZE:-3}"

cd "$ROOT"

# Turns on OpenClaw's cache trace and dumps, per task, the system prompt and
# message array as the provider received them. Without this the stock cells have
# no record of the prompt they ran under, since OpenClaw builds it internally.
export SRBENCH_OPENCLAW_TRACE_DIR="${SRBENCH_OPENCLAW_TRACE_DIR:-$ROOT/$OUTPUT_BASE/openclaw-traces}"
mkdir -p "$SRBENCH_OPENCLAW_TRACE_DIR"

# Repeats are walked here, not inside experiment.py: the collector deduplicates
# configs by content and ignores the variant label, so three identical cells
# yielded from one generator collapse into one. A fresh process resets that.
for rep in $(seq 1 "${ABLATION_REPEATS:-3}"); do
  for tools in ${ABLATION_TOOLS:-srbench sandbox}; do
    export ABLATION_REPEAT="$rep"
    export SRBENCH_OPENCLAW_TOOLS="$tools"
    echo "=== repeat: $rep | tools: $tools ==="
    .venv/bin/srbench experiment "$HERE" --output-base "$OUTPUT_BASE" "$@"
  done
done
