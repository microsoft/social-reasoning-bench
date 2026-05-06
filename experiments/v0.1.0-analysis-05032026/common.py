"""Shared data loading utilities for v0.1.0 analysis plots."""

import json
import re
import glob
from pathlib import Path
from dataclasses import dataclass, field

import numpy as np

REPO_ROOT = Path(__file__).resolve().parents[2]
RESULTS_DIR = REPO_ROOT / "outputs" / "v0.1.0"
FIGURES_DIR = Path(__file__).resolve().parent / "figures"

# Canonical (model, mode) pairs — matches experiments/v0.1.0/plotting/common.py
TARGET_MODELS: set[tuple[str, str]] = {
    ("gpt-4-1", "cot"),
    ("gpt-5-4", "high"),
    ("gemini", "medium"),
}


def _get_model_key(model_dir: str) -> str | None:
    """Return the short model key for matching against TARGET_MODELS."""
    if "gpt-4-1" in model_dir:
        return "gpt-4-1"
    elif "gpt-5-4" in model_dir:
        return "gpt-5-4"
    elif "gemini" in model_dir:
        return "gemini"
    return None


def _get_mode(model_dir: str) -> str | None:
    """Return the reasoning mode from directory name."""
    if "_cot_" in model_dir:
        return "cot"
    elif "_high_" in model_dir:
        return "high"
    elif "_medium_" in model_dir:
        return "medium"
    elif "_low_" in model_dir:
        return "low"
    return None


def _run_number(path_name: str) -> int:
    """Extract run number from dir name. No suffix = run 1."""
    m = re.search(r"_run(\d+)_", path_name)
    return int(m.group(1)) if m else 1


def is_target_model(model_dir: str) -> bool:
    """Check if this dir matches one of the canonical (model, mode) pairs."""
    model_key = _get_model_key(model_dir)
    mode = _get_mode(model_dir)
    if model_key is None or mode is None:
        return False
    return (model_key, mode) in TARGET_MODELS


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
    """Determine prompt type from directory name. Returns 'all' or 'none' for valid benign dirs."""
    if not is_target_model(model_dir):
        return None
    # Benign dirs have _none_none or no attack suffix
    if "_all_none_none" in model_dir:
        return "all"
    elif "_none_none_none" in model_dir:
        return "none"
    # cot dirs without explicit none_none suffix
    elif "_cot_all_" in model_dir and "handcrafted" not in model_dir and "whimsical" not in model_dir:
        return "all"
    elif "_cot_none_" in model_dir and "handcrafted" not in model_dir and "whimsical" not in model_dir:
        return "none"
    return None


def get_condition_key(model_dir: str) -> str:
    """Return a condition key for deduplication (attack_style + target)."""
    if "handcrafted" in model_dir:
        if "due_diligence" in model_dir:
            return "handcrafted_dd"
        elif "outcome_optimality" in model_dir:
            return "handcrafted_oo"
        elif "privacy" in model_dir:
            return "handcrafted_privacy"
        return "handcrafted_unknown"
    elif "whimsical" in model_dir:
        if "due_diligence" in model_dir:
            return "whimsical_dd"
        elif "outcome_optimality" in model_dir:
            return "whimsical_oo"
        elif "privacy" in model_dir:
            return "whimsical_privacy"
        return "whimsical_unknown"
    else:
        return "none_none"


def get_prompt(model_dir: str) -> str | None:
    """Return 'all' or 'none' for the system prompt variant."""
    if "_all_" in model_dir:
        return "all"
    elif "_none_" in model_dir:
        return "none"
    return None


def is_benign(result: dict, domain: str) -> bool:
    """Correct filter for benign tasks: requestor/seller is_malicious == False."""
    task = result["execution"]["task"]
    if domain == "calendar":
        return task.get("requestor", {}).get("is_malicious", False) is False
    else:  # marketplace
        return task.get("variant") is None


def load_results_dirs(prompt_filter: str | None = None, include_malicious: bool = False) -> list[Path]:
    """Load result directories with TARGET_MODELS filter and deduplication.
    
    Args:
        prompt_filter: 'all', 'none', or None (both)
        include_malicious: if True, include handcrafted/whimsical dirs
    
    Returns:
        Deduplicated list of Path objects sorted by run number.
    """
    seen: set[tuple] = set()
    dirs = []
    
    for d in sorted(RESULTS_DIR.iterdir(), key=lambda p: (_run_number(p.name), p.name)):
        if not d.is_dir():
            continue
        if not (d / "results.json").exists():
            continue
        if not is_target_model(d.name):
            continue
        
        # Domain
        if "calendar" in d.name:
            domain = "calendar"
        elif "marketplace" in d.name:
            domain = "marketplace"
        else:
            continue
        
        # Prompt filter
        prompt = get_prompt(d.name)
        if prompt is None:
            continue
        if prompt_filter and prompt != prompt_filter:
            continue
        
        # Malicious filter
        is_malicious_dir = "handcrafted" in d.name or "whimsical" in d.name
        if not include_malicious and is_malicious_dir:
            continue
        if include_malicious and not is_malicious_dir:
            # When loading malicious, still include benign for comparison
            pass
        
        # Dedup by (domain, model_key, mode, prompt, condition)
        model_key = _get_model_key(d.name)
        mode = _get_mode(d.name)
        condition = get_condition_key(d.name)
        dedup_key = (domain, model_key, mode, prompt, condition)
        if dedup_key in seen:
            continue
        seen.add(dedup_key)
        dirs.append(d)
    
    return dirs


@dataclass
class TaskResult:
    domain: str
    model: str
    prompt: str
    oo: float
    tc: bool


def load_benign_results() -> list[TaskResult]:
    """Load all benign task results across both domains (deduplicated, target models only)."""
    results = []
    for d in load_results_dirs(prompt_filter=None, include_malicious=False):
        domain = "calendar" if "calendar" in d.name else "marketplace"
        model = get_model(d.name)
        prompt = get_prompt(d.name)
        
        data = json.loads((d / "results.json").read_text())
        for r in data.get("results", []):
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
