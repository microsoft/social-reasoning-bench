"""Validation sweep for the production geometric-pref PR.

20 variants: 2 conditions (baseline yamls vs new geometric yamls)
  × 2 models (gpt-4.1, gpt-5.4-med)
  × 5 attacks (benign, handcrafted-OO, whimsical-DD, whimsical-OO, whimsical-Privacy)

The baseline yamls are vendored copies (data/baseline/) of the pre-PR
small/whimsical files. The new yamls are loaded from the canonical
data/calendar-scheduling/ paths in the repo root.

To reproduce:
    srbench experiment experiments/v0.1.0-calendar-pref-regen-04302026 \\
        --output-base outputs/v0.1.0-calendar-pref-regen-04302026
"""

from pathlib import Path

from srbench.benchmarks.calendar_scheduling.config import CalendarRunConfig

EXP_DIR = Path(__file__).resolve().parent
REPO_ROOT = EXP_DIR.parent.parent
BASELINE_DIR = EXP_DIR / "data" / "baseline"
NEW_DIR = REPO_ROOT / "data" / "calendar-scheduling"

JUDGE = {"model": "gemini-2.5-flash", "reasoning_effort": "medium"}
COUNTERPARTY = {"model": "gemini-3-flash-preview", "reasoning_effort": "medium"}
CONCURRENCY = {"batch_size": 200, "task_concurrency": 5, "llm_concurrency": 64}
ROUNDS = {"max_rounds": 10, "max_steps_per_turn": 3}


def assistants():
    yield {
        "label": "gpt-4.1",
        "model": "azure_pool/gpt-4.1",
        "explicit_cot": False,
        "reasoning_effort": None,
    }
    yield {
        "label": "gpt-5.4-med",
        "model": "azure_pool/gpt-5.4",
        "explicit_cot": None,
        "reasoning_effort": "medium",
    }


def conditions():
    yield "baseline", BASELINE_DIR
    yield "new", NEW_DIR


def attacks():
    # (attack_label, small_yaml_basename, attack_types)
    yield "benign", "small.yaml", []
    yield "hc_oo", "small.yaml", ["outcome_optimality"]
    yield "whimsical_due_diligence", "small-whimsical-due_diligence.yaml", []
    yield "whimsical_outcome_optimality", "small-whimsical-outcome_optimality.yaml", []
    yield "whimsical_privacy", "small-whimsical-privacy.yaml", []


def variant_name(condition: str, assistant_label: str, attack_label: str) -> str:
    return f"calendar_{condition}_{assistant_label}_{attack_label}"


def experiment_validation():
    for condition, data_dir in conditions():
        for assistant in assistants():
            for attack_label, yaml_name, attack_types in attacks():
                yield CalendarRunConfig(
                    paths=[str(data_dir / yaml_name)],
                    assistant_model=assistant["model"],
                    assistant_explicit_cot=assistant["explicit_cot"],
                    assistant_reasoning_effort=assistant["reasoning_effort"],
                    system_prompt="none",
                    expose_preferences=True,
                    requestor_model=COUNTERPARTY["model"],
                    requestor_reasoning_effort=COUNTERPARTY["reasoning_effort"],
                    attack_types=attack_types,
                    judge_model=JUDGE["model"],
                    judge_reasoning_effort=JUDGE["reasoning_effort"],
                    batch_size=CONCURRENCY["batch_size"],
                    task_concurrency=CONCURRENCY["task_concurrency"],
                    llm_concurrency=CONCURRENCY["llm_concurrency"],
                    max_rounds=ROUNDS["max_rounds"],
                    max_steps_per_turn=ROUNDS["max_steps_per_turn"],
                    variant=variant_name(condition, assistant["label"], attack_label),
                )
