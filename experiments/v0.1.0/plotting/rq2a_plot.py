"""RQ2a: Task Completion stays high under attack.

Slice: prompt=all, three bars per model: Benign / Hand-Crafted / Whimsical.
Faceted by domain (rows) and model (columns).
"""

import json

import altair as alt
import pandas as pd
from benign_oo import (
    load_calendar_results,
    load_marketplace_results,
)
from common import (
    DOMAIN_LABELS,
    DOMAIN_ORDER,
    MODE_LABELS,
    MODEL_LABELS,
    PALETTE,
    RESULTS_DIR,
    _parse_config,
    apply_theme,
    make_title,
    render_rq,
)

ALLOWED_MODELS = {
    ("azure_pool-gpt-4-1", "cot"),
    ("azure_pool-gpt-5-4", "high"),
    ("gemini-3-flash-preview", "medium"),
}

STYLE_ORDER = ["normal", "hand_crafted", "whimsical"]

STYLE_LABELS = {
    "normal": "Benign",
    "hand_crafted": "Hand-Crafted",
    "whimsical": "Whimsical",
}


def _model_label(model: str, mode: str) -> str:
    pretty = MODEL_LABELS.get(model, model)
    mode_label = MODE_LABELS.get(mode, mode) if mode else "no_cot"
    return f"{pretty} ({mode_label})"


def get_data() -> pd.DataFrame:
    groups: dict[tuple[str, str, str], list[float]] = {}

    for variant_dir in sorted(RESULTS_DIR.iterdir()):
        results_file = variant_dir / "results.json"
        if not results_file.is_file():
            continue
        data = json.loads(results_file.read_text())
        cfg = data.get("config") or {}
        if "assistant_model" not in cfg and "buyer_model" not in cfg:
            continue
        pc = _parse_config(cfg)
        if pc.prompt != "all":
            continue
        if (pc.model, pc.mode) not in ALLOWED_MODELS:
            continue

        if pc.domain == "marketplace":
            typed = load_marketplace_results(data)
        elif pc.domain == "calendar":
            typed = load_calendar_results(data)
        else:
            continue

        key = (
            DOMAIN_LABELS.get(pc.domain, pc.domain),
            _model_label(pc.model, pc.mode),
            pc.attack_style,
        )
        if key not in groups:
            groups[key] = []

        for r in typed:
            groups[key].append(float(r.task_completed))

    rows = []
    for (domain, model_label, style), vals in groups.items():
        rows.append(
            {
                "domain": domain,
                "model_label": model_label,
                "style": style,
                "style_label": STYLE_LABELS.get(style, style),
                "task_completion": sum(vals) / len(vals) if vals else None,
            }
        )

    return pd.DataFrame(rows)


def make_plot(df: pd.DataFrame) -> alt.Chart:
    domains_in_slice = set(df["domain"].unique())
    complete_models = [
        m
        for m in df["model_label"].unique()
        if set(df.loc[df["model_label"] == m, "domain"].unique()) == domains_in_slice
    ]
    df = df[df["model_label"].isin(complete_models)].copy()

    label_order = [STYLE_LABELS[s] for s in STYLE_ORDER]
    style_range = [PALETTE["normal"], PALETTE["hand_crafted"], PALETTE["whimsical"]]

    base = alt.Chart(df).encode(
        x=alt.X(
            "style_label:N",
            title=None,
            sort=label_order,
            axis=alt.Axis(labelAngle=-30),
        ),
        y=alt.Y(
            "task_completion:Q",
            title=None,
            scale=alt.Scale(domain=[0, 1]),
            axis=alt.Axis(format=".0%"),
        ),
    )

    bars = base.mark_bar().encode(
        color=alt.Color(
            "style_label:N",
            title="Condition",
            scale=alt.Scale(domain=label_order, range=style_range),
            legend=alt.Legend(orient="top"),
        ),
        tooltip=[
            "domain",
            "model_label",
            "style_label",
            alt.Tooltip("task_completion:Q", format=".1%"),
        ],
    )

    labels = base.mark_text(dy=-6, fontSize=9, color="#333").encode(
        text=alt.Text("task_completion:Q", format=".0%")
    )

    chart = (
        (bars + labels)
        .properties(width=200, height=150)
        .facet(
            row=alt.Row(
                "domain:N",
                title=None,
                sort=DOMAIN_ORDER,
                header=alt.Header(labelFontWeight="bold"),
            ),
            column=alt.Column(
                "model_label:N", title=None, header=alt.Header(labelFontWeight="bold")
            ),
        )
        .resolve_axis(x="independent")
        .properties(
            title=make_title(
                "RQ2a: Task Completion Under Attack",
                "Averaged across attack targets · system prompt = all",
            )
        )
    )
    return apply_theme(chart)


def main() -> None:
    render_rq("rq2a", get_data, make_plot)


if __name__ == "__main__":
    main()
