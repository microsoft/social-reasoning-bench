#!/usr/bin/env bash
# Drive eval of Azure-Blob HF checkpoints listed in
# experiments/blob-ckpts/experiment.py.
#
# For each checkpoint:
#   1. azcopy sync HF dir from blob -> $CKPT_CACHE/<short>
#   2. launch vLLM on $PORT (single GPU)
#   3. srbench experiment experiments/blob-ckpts -k <short>
#   4. tear down vLLM, optionally evict checkpoint
#
# Env knobs: GPU, PORT (must match VLLM_BASE_URL in experiment.py),
#            CKPT_CACHE, KEEP_CKPT, VLLM_READY_TIMEOUT.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"
[[ -f .venv/bin/activate ]] && source .venv/bin/activate
[[ -f env.sh ]] && source env.sh

EXP_DIR="experiments/blob-ckpts"

AZ_ACCT="${AZ_ACCT:-aifrontiersplus}"
AZ_CONT="${AZ_CONT:-magentic}"
CKPT_CACHE="${CKPT_CACHE:-$HOME/eval_ckpts}"
PORT="${PORT:-8321}"
GPU="${GPU:-0}"
KEEP_CKPT="${KEEP_CKPT:-0}"
VLLM_READY_TIMEOUT="${VLLM_READY_TIMEOUT:-600}"

mkdir -p "$CKPT_CACHE"

# Pull the (short_name, blob_path) pairs out of experiment.py so this script
# stays the single source of truth for which ckpts to sync/serve.
mapfile -t CKPTS < <(python3 -c "
from experiments.blob_ckpts.experiment import CKPTS
for k, v in CKPTS.items(): print(f'{k}|{v}')
" 2>/dev/null || python3 -c "
import importlib.util, pathlib
spec = importlib.util.spec_from_file_location('exp', pathlib.Path('${EXP_DIR}/experiment.py'))
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
for k, v in m.CKPTS.items(): print(f'{k}|{v}')
")

mint_sas() {
  local expiry; expiry="$(date -u -d "+12 hours" '+%Y-%m-%dT%H:%MZ')"
  az storage container generate-sas \
    --account-name "$AZ_ACCT" --name "$AZ_CONT" \
    --permissions rl --expiry "$expiry" \
    --auth-mode login --as-user -o tsv
}

wait_for_vllm() {
  local pid="$1" deadline=$((SECONDS + VLLM_READY_TIMEOUT))
  while (( SECONDS < deadline )); do
    curl -sf "http://localhost:${PORT}/health" >/dev/null 2>&1 && return 0
    kill -0 "$pid" 2>/dev/null || { echo "  ERROR: vLLM exited before ready" >&2; return 1; }
    sleep 5
  done
  echo "  ERROR: vLLM not ready within ${VLLM_READY_TIMEOUT}s" >&2
  return 1
}

run_one() {
  local short="$1" blob="$2"
  local local_dir="${CKPT_CACHE}/${short}"
  echo
  echo "================ ${short} ================"

  if [[ ! -f "${local_dir}/config.json" ]]; then
    mkdir -p "${local_dir}"
    local sas; sas="$(mint_sas)"
    local src="https://${AZ_ACCT}.blob.core.windows.net/${AZ_CONT}/${blob%/}/?${sas}"
    echo "  syncing from blob ..."
    azcopy sync "$src" "$local_dir" --recursive --log-level=WARNING >/dev/null
  fi
  [[ -f "${local_dir}/config.json" ]] || { echo "  ERROR: missing config.json"; return 1; }

  local vllm_log="/tmp/vllm-${short}.log"
  echo "  launching vLLM (GPU ${GPU}, port ${PORT}) -> ${vllm_log}"
  CUDA_VISIBLE_DEVICES="${GPU}" vllm serve "${local_dir}" \
    --port "${PORT}" \
    --served-model-name "${short}" \
    --dtype bfloat16 \
    --max-model-len 32768 \
    --gpu-memory-utilization 0.85 \
    --enable-auto-tool-choice \
    --tool-call-parser hermes \
    > "${vllm_log}" 2>&1 &
  local vllm_pid=$!
  trap 'kill '"${vllm_pid}"' 2>/dev/null || true; wait '"${vllm_pid}"' 2>/dev/null || true' RETURN

  wait_for_vllm "${vllm_pid}" || { tail -80 "${vllm_log}"; return 1; }
  echo "  vLLM ready, running srbench experiment -k ${short}"

  srbench experiment "${EXP_DIR}" -k "${short}" --logger progress || true

  echo "  stopping vLLM (${vllm_pid})"
  kill "${vllm_pid}" 2>/dev/null || true
  wait "${vllm_pid}" 2>/dev/null || true
  trap - RETURN

  if [[ "${KEEP_CKPT}" != "1" ]]; then
    echo "  removing ${local_dir}"
    rm -rf "${local_dir}"
  fi
}

for entry in "${CKPTS[@]}"; do
  IFS='|' read -r short blob <<<"$entry"
  if ! run_one "$short" "$blob"; then
    echo "================ ${short} FAILED ================" >&2
  fi
done
