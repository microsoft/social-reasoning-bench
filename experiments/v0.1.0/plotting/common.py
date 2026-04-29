"""Shared loading + theme for blog plots."""

import json
from dataclasses import dataclass
from pathlib import Path

import altair as alt
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[3]
RESULTS_DIR = REPO_ROOT / "outputs" / "v0.1.0"
FIGURES_DIR = Path(__file__).resolve().parent / "figures"

PROMPT_TOKENS = {"none", "all"}

PALETTE = {
    "task_completion": "#B8B8B8",
    "outcome_optimality": "#5a8a66",
    "duty_of_care": "#5a8a66",
    "due_diligence": "#B279A2",
    "none": "#B8B8B8",
    "all": "#2E5C8A",
    "normal": "#B8B8B8",
    "hand_crafted": "#E6740C",
    "whimsical": "#A50F15",
}

DOMAIN_ORDER = ["Calendar", "Marketplace"]
DOMAIN_LABELS = {"calendar": "Calendar", "marketplace": "Marketplace"}

METRIC_LABELS = {
    "avg_task_completion": "Task Completion",
    "avg_outcome_optimality": "Outcome Optimality",
    "avg_duty_of_care": "Duty of Care",
    "avg_due_diligence": "Due Diligence",
}


@dataclass(frozen=True)
class Run:
    domain: str
    model: str
    mode: str
    prompt: str
    attack_style: str
    attack_target: str
    condition: str
    metrics: dict[str, float]

    @property
    def model_label(self) -> str:
        pretty = self.model.replace("gpt", "GPT")
        return f"{pretty} ({self.mode})"


def _parse_variant(name: str) -> tuple[str, str, str, str, str]:
    parts = name.split("_")
    domain = parts[0]
    prompt_idx = next(i for i, p in enumerate(parts) if p in PROMPT_TOKENS)
    model_full = "_".join(parts[1:prompt_idx])
    if "_" in model_full:
        model, mode = model_full.split("_", 1)
    else:
        model, mode = model_full, ""
    prompt = parts[prompt_idx]
    condition = "_".join(parts[prompt_idx + 1 :])
    return domain, model, mode, prompt, condition


def _parse_condition(condition: str) -> tuple[str, str]:
    if condition == "normal":
        return "normal", "none"
    if condition.startswith("hand_crafted_"):
        target = condition.removeprefix("hand_crafted_")
        return "hand_crafted", _short_target(target)
    if condition.startswith("whimsical_"):
        target = condition.removeprefix("whimsical_")
        return "whimsical", _short_target(target)
    raise ValueError(f"unknown condition: {condition}")


def _short_target(target: str) -> str:
    return {"outcome_optimality": "oo", "due_diligence": "dd"}.get(target, target)


def load_runs(results_dir: Path = RESULTS_DIR) -> list[Run]:
    runs: list[Run] = []
    for variant_dir in sorted(results_dir.iterdir()):
        results_file = variant_dir / "results.json"
        if not results_file.is_file():
            continue
        data = json.loads(results_file.read_text())
        domain, model, mode, prompt, condition = _parse_variant(variant_dir.name)
        attack_style, attack_target = _parse_condition(condition)
        runs.append(
            Run(
                domain=domain,
                model=model,
                mode=mode,
                prompt=prompt,
                attack_style=attack_style,
                attack_target=attack_target,
                condition=condition,
                metrics=data["evaluation"],
            )
        )
    return runs


def runs_to_df(runs: list[Run]) -> pd.DataFrame:
    rows = []
    for r in runs:
        rows.append(
            {
                "domain": DOMAIN_LABELS.get(r.domain, r.domain),
                "model": r.model,
                "mode": r.mode,
                "model_label": r.model_label,
                "prompt": r.prompt,
                "attack_style": r.attack_style,
                "attack_target": r.attack_target,
                "condition": r.condition,
                "task_completion": r.metrics.get("avg_task_completion"),
                "outcome_optimality": r.metrics.get("avg_outcome_optimality"),
                "duty_of_care": r.metrics.get("avg_duty_of_care"),
                "due_diligence": r.metrics.get("avg_due_diligence"),
                "leakage_rate": r.metrics.get("avg_leakage_rate"),
            }
        )
    return pd.DataFrame(rows)


def apply_theme(chart: alt.Chart | alt.LayerChart | alt.HConcatChart) -> alt.Chart:
    return (
        chart.configure_view(strokeWidth=0)
        .configure_axis(
            labelFontSize=11,
            titleFontSize=12,
            labelColor="#000",
            titleColor="#000",
            grid=False,
            domainColor="#000",
            tickColor="#000",
        )
        .configure_axisY(
            labelFontSize=11,
            titleFontSize=12,
            grid=False,
            domain=False,
            ticks=False,
            labelColor="#000",
        )
        .configure_title(
            fontSize=15,
            anchor="middle",
            color="#222",
            fontWeight="bold",
            subtitleFontSize=11,
            subtitleColor="#666",
            subtitleFontWeight="normal",
            offset=12,
            subtitlePadding=6,
        )
        .configure_legend(
            labelFontSize=11,
            titleFontSize=11,
            direction="horizontal",
            titleOrient="left",
            titleAnchor="middle",
            symbolType="square",
            padding=8,
        )
        .configure_header(
            labelFontSize=12,
            titleFontSize=12,
            labelFontWeight="bold",
        )
    )


def make_title(text: str, subtitle: str | None = None) -> alt.TitleParams:
    return alt.TitleParams(text=text, subtitle=subtitle or "")


def save(chart: alt.Chart, name: str) -> Path:
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    out_png = FIGURES_DIR / f"{name}.png"
    chart.save(str(out_png), ppi=200)
    return out_png
