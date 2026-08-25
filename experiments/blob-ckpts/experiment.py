"""SRBench eval matrix for Azure-Blob HF checkpoints served via local vLLM.

The companion ``scripts/eval_blob_checkpoints.sh`` iterates over the
checkpoints in ``CKPTS``, syncs each from Azure Blob to local disk, launches
vLLM on ``VLLM_PORT``, then runs:

    srbench experiment experiments/blob-ckpts -k <short_name>

so only that one checkpoint's configs fire while vLLM is up.

To reproduce manually (with vLLM already serving on the expected port):
    srbench experiment experiments/blob-ckpts -k ppo-dnd-step209
"""

from __future__ import annotations

from typing import Any

from srbench.benchmarks.calendar_scheduling.config import CalendarRunConfig
from srbench.benchmarks.marketplace.config import MarketplaceRunConfig

# short_name -> blob_path (under the magentic container)
CKPTS: dict[str, str] = {
    "ppo-dnd-step209": "sage-train/checkpoints/wenyuehua-p0-ppo-dnd-2026-05-18_01-30-15_3N/global_step_209/actor/huggingface",
    "sft-dnd-step270": "sage-train/checkpoints/sft_2026_05_16/Qwen3-4B-Instruct_global_step_270_hf_merged",
    "multienv-ppo-step320": "sage-train/checkpoints/multienv_ppo_uniform_2026_05_19/global_step_320/actor/huggingface",
    "ppo-dnd-echo-step200": "sage-train/checkpoints/wenyuehua-p0-ppo-dnd-oppsft-0-1-2026-05-19_13-10-30_3N/global_step_200",
}

VLLM_BASE_URL = "http://localhost:8321/v1"

CALENDAR_DATA = "data/calendar-scheduling/small.yaml"
MARKETPLACE_DATA = "data/marketplace/medium.yaml"

DEFENSES = ("none", "all")

COUNTERPARTY = "gemini/gemini-2.5-flash"
JUDGE: dict[str, Any] = {"model": "gemini/gemini-2.5-flash", "votes": 3}

CONCURRENCY: dict[str, Any] = {"batch_size": 32}
ROUNDS: dict[str, Any] = {"max_rounds": 20}


def _variant(bench: str, short: str, defense: str) -> str:
    return f"{bench}_{short}_{defense}"


def experiment_calendar():
    for short in CKPTS:
        model = f"openai/{short}"
        for defense in DEFENSES:
            yield CalendarRunConfig(
                paths=[CALENDAR_DATA],
                assistant_model=model,
                assistant_base_url=VLLM_BASE_URL,
                expose_preferences=True,
                requestor_model=COUNTERPARTY,
                judge_model=JUDGE["model"],
                judge_votes=JUDGE["votes"],
                system_prompt=defense,
                max_rounds=ROUNDS["max_rounds"],
                batch_size=CONCURRENCY["batch_size"],
                variant=_variant("calendar", short, defense),
            )


def experiment_marketplace():
    for short in CKPTS:
        model = f"openai/{short}"
        for defense in DEFENSES:
            yield MarketplaceRunConfig(
                paths=[MARKETPLACE_DATA],
                buyer_model=model,
                buyer_base_url=VLLM_BASE_URL,
                seller_model=COUNTERPARTY,
                judge_model=JUDGE["model"],
                judge_votes=JUDGE["votes"],
                system_prompt=defense,
                max_rounds=ROUNDS["max_rounds"],
                batch_size=CONCURRENCY["batch_size"],
                variant=_variant("marketplace", short, defense),
            )
