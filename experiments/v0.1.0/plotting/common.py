"""Shared loading + theme for blog plots."""

import json
import re
from dataclasses import dataclass
from pathlib import Path

import altair as alt
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[3]
RESULTS_DIR = REPO_ROOT / "outputs" / "v0.1.0"
FIGURES_DIR = Path(__file__).resolve().parent / "figures"

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
        pretty = MODEL_LABELS.get(self.model, self.model)
        mode = MODE_LABELS.get(self.mode, self.mode) if self.mode else "no_cot"
        return f"{pretty} ({mode})"


MODEL_LABELS = {
    "azure_pool-gpt-4-1": "GPT-4.1",
    "azure_pool-gpt-5-4": "GPT-5.4",
    "gemini-3-flash-preview": "Gemini 3 Flash",
    "claude-sonnet-4-6": "Claude Sonnet 4.6",
}

# Only include these (model, mode) pairs in plots.
TARGET_MODELS: set[tuple[str, str]] = {
    ("azure_pool-gpt-4-1", "cot"),
    ("azure_pool-gpt-5-4", "high"),
    ("gemini-3-flash-preview", "medium"),
}

MODE_LABELS = {
    "cot": "cot",
    "medium": "think_med",
    "high": "think_high",
    "low": "think_low",
}


def _short_target(target: str) -> str:
    return {"outcome_optimality": "oo", "due_diligence": "dd"}.get(target, target)


def _normalize_model(model: str) -> str:
    return model.replace("/", "-").replace(".", "-")


@dataclass(frozen=True)
class ParsedConfig:
    domain: str
    model: str
    mode: str
    prompt: str
    attack_style: str
    attack_target: str
    condition: str


def _parse_config(cfg: dict) -> ParsedConfig:
    """Extract experiment dimensions from a results.json config."""
    if "assistant_model" in cfg:
        domain = "calendar"
        model_raw = cfg["assistant_model"]
        effort = cfg.get("assistant_reasoning_effort")
        cot = cfg.get("assistant_explicit_cot")
    elif "buyer_model" in cfg:
        domain = "marketplace"
        model_raw = cfg["buyer_model"]
        effort = cfg.get("buyer_reasoning_effort")
        cot = cfg.get("buyer_explicit_cot")
    else:
        raise ValueError(f"cannot infer domain from config: keys={list(cfg)[:10]}")

    model = _normalize_model(model_raw)
    if cot is True:
        mode = "cot"
    elif effort is not None:
        mode = str(effort)
    else:
        mode = ""

    prompt = cfg.get("system_prompt") or "none"

    attack_types = cfg.get("attack_types") or []
    paths = cfg.get("paths") or []
    path = paths[0] if paths else ""
    if "whimsical" in path:
        attack_style = "whimsical"
        # filename pattern: {size}-whimsical-{target}.yaml
        target = Path(path).stem.split("-whimsical-", 1)[1]
        attack_target = _short_target(target)
        condition = f"whimsical_{target}"
    elif attack_types:
        attack_style = "hand_crafted"
        target = attack_types[0]
        attack_target = _short_target(target)
        condition = f"handcrafted_{target}"
    else:
        attack_style = "normal"
        attack_target = "none"
        condition = "none_none"

    return ParsedConfig(domain, model, mode, prompt, attack_style, attack_target, condition)


def _compute_metrics(results: list) -> dict[str, float]:
    """Average per-task scores across all results, ignoring None.

    The pre-aggregated `evaluation` block in results.json drops tasks where
    `finished_successfully` is False (notably tasks that hit max_rounds), which
    can shift averages substantially under attack conditions. Recomputing from
    raw per-task scores includes every task and gives an honest picture.
    """

    def _avg(key: str, source: str = "task") -> float | None:
        if source == "task":
            vals = [r.get(key) for r in results]
        else:
            vals = [(r.get("execution") or {}).get(key) for r in results]
        vals = [v for v in vals if v is not None]
        if not vals:
            return None
        # Booleans (e.g., task_completed) average as 0/1.
        return sum(float(v) for v in vals) / len(vals)

    return {
        "avg_task_completion": _avg("task_completed"),
        "avg_outcome_optimality": _avg("outcome_optimality"),
        "avg_due_diligence": _avg("due_diligence"),
        "avg_duty_of_care": _avg("duty_of_care"),
        "avg_leakage_rate": _avg("leakage_rate"),
    }


def _run_sort_key(path: Path) -> tuple[int, str]:
    """Sort dirs so that the lowest-numbered run wins dedup.

    Base dir (no `_runN_`) is treated as run 1. `_run2_`, `_run3_`, ... follow.
    """
    m = re.search(r"_run(\d+)_", path.name)
    run_num = int(m.group(1)) if m else 1
    return (run_num, path.name)


def load_runs(results_dir: Path = RESULTS_DIR) -> list[Run]:
    runs: list[Run] = []
    seen: set[tuple] = set()
    for variant_dir in sorted(results_dir.iterdir(), key=_run_sort_key):
        results_file = variant_dir / "results.json"
        if not results_file.is_file():
            continue
        data = json.loads(results_file.read_text())
        cfg = data.get("config") or {}
        if "assistant_model" not in cfg and "buyer_model" not in cfg:
            continue
        pc = _parse_config(cfg)
        if (pc.model, pc.mode) not in TARGET_MODELS:
            continue
        # Skip duplicate runs (same domain/model/mode/prompt/condition).
        key = (pc.domain, pc.model, pc.mode, pc.prompt, pc.condition)
        if key in seen:
            continue
        seen.add(key)
        runs.append(
            Run(
                domain=pc.domain,
                model=pc.model,
                mode=pc.mode,
                prompt=pc.prompt,
                attack_style=pc.attack_style,
                attack_target=pc.attack_target,
                condition=pc.condition,
                metrics=_compute_metrics(data["results"]),
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


def save(chart: alt.Chart, name: str, subdir: str = "") -> Path:
    out_dir = FIGURES_DIR / subdir if subdir else FIGURES_DIR
    out_dir.mkdir(parents=True, exist_ok=True)
    out_png = out_dir / f"{name}.png"
    chart.save(str(out_png), ppi=200)
    return out_png


def render_rq(name, get_data, make_plot):
    """Render three PNGs per RQ into combined/, calendar/, marketplace/ subdirs."""
    df = get_data()
    for subdir, sub in (
        ("combined", df),
        ("calendar", df[df["domain"] == DOMAIN_LABELS["calendar"]]),
        ("marketplace", df[df["domain"] == DOMAIN_LABELS["marketplace"]]),
    ):
        if sub.empty:
            continue
        out = save(make_plot(sub), name, subdir=subdir)
        print(f"saved {out}")
