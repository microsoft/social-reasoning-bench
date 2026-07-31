#!/usr/bin/env bash
#
# Run the OpenClaw prompt/tool ablation.
#
# OpenClaw's system prompt and its tool profile are both read when a Gateway
# starts, and the Gateway pool outlives any one variant, so those two factors
# cannot be swept inside a single srbench process. This walks the four
# combinations, one process each; experiment.py sweeps the SRBench prompt and
# the preference guidance inside each.
#
# Any extra arguments are forwarded to every run, e.g.
#
#     run.sh --set limit=3      # three tasks per cell, for a smoke test
#     run.sh --collect          # list the runs without executing them
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

# The "off" cells need a build that honours OPENCLAW_SYSTEM_PROMPT_OVERRIDE;
# stock OpenClaw offers no way to replace its system prompt. See README.md.
: "${SRBENCH_OPENCLAW_BIN:?set SRBENCH_OPENCLAW_BIN to the patched OpenClaw build}"

# One Gateway per concurrent task. experiment.py reads the same variable for
# batch size, so the two cannot disagree.
export SRBENCH_OPENCLAW_POOL_SIZE="${SRBENCH_OPENCLAW_POOL_SIZE:-3}"

cd "$ROOT"

for tools in ${ABLATION_TOOLS:-srbench sandbox}; do
  for prompt in on off; do
    export SRBENCH_OPENCLAW_TOOLS="$tools"
    if [[ "$prompt" == "off" ]]; then
      export OPENCLAW_SYSTEM_PROMPT_OVERRIDE=""
    else
      unset OPENCLAW_SYSTEM_PROMPT_OVERRIDE
    fi

    echo "=== openclaw prompt: $prompt | tools: $tools ==="
    .venv/bin/srbench experiment "$HERE" --output-base "$OUTPUT_BASE" "$@"
  done
done
