"""Shared data loading utilities for v0.1.0 analysis plots."""

import json
import glob
from pathlib import Path
from dataclasses import dataclass, field

import numpy as np

REPO_ROOT = Path(__file__).resolve().parents[2]
RESULTS_DIR = REPO_ROOT / "outputs" / "v0.1.0"
FIGURES_DIR = Path(__file__).resolve().parent / "figures"


def get_model(model_dir: str) -> str | None:
    if "gpt-4-1" in model_dir:
        return "GPT-4.1"
    elif "gpt-5-4" in model_dir:
        return "GPT-5.4"
    elif "gemini" in model_dir:
        return "Gemini"
    return None


def has_reasoning(model_dir: str) -> bool:
    """Check if the run used chain-of-thought or thinking (medium/high)."""
    return "_cot_" in model_dir or "_medium_" in model_dir or "_high_" in model_dir


def get_prompt_type(model_dir: str) -> str | None:
    """Determine prompt type from directory name. Only includes reasoning runs."""
    if not has_reasoning(model_dir):
        return None
    if "_all_none_none" in model_dir or "_cot_all_" in model_dir:
        return "all"
    elif "_none_none_none" in model_dir or "_cot_none_" in model_dir:
        return "none"
    return None


def is_benign(result: dict, domain: str) -> bool:
    """Correct filter for benign tasks: requestor/seller is_malicious == False."""
    task = result["execution"]["task"]
    if domain == "calendar":
        return task.get("requestor", {}).get("is_malicious", False) is False
    else:  # marketplace
        return task.get("variant") is None


@dataclass
class TaskResult:
    domain: str
    model: str
    prompt: str
    oo: float
    tc: bool


def load_benign_results() -> list[TaskResult]:
    """Load all benign task results across both domains."""
    results = []
    for domain in ["calendar", "marketplace"]:
        for rpath in sorted(glob.glob(str(RESULTS_DIR / f"{domain}_*" / "results.json"))):
            model_dir = Path(rpath).parent.name
            model = get_model(model_dir)
            if not model:
                continue
            prompt = get_prompt_type(model_dir)
            if not prompt:
                continue

            with open(rpath) as f:
                data = json.load(f)["results"]

            for r in data:
                oo = r.get("outcome_optimality")
                if oo is None:
                    continue
                if not is_benign(r, domain):
                    continue
                tc = r.get("task_completed", False)
                results.append(TaskResult(
                    domain=domain, model=model, prompt=prompt, oo=oo, tc=tc
                ))
    return results
