"""RQ7: Bubble confusion matrix — binarised OO vs DD for benign tasks.

Each task's Outcome Optimality and Due Diligence are split at 0.5 into
Low / High bins.  The 2×2 grid shows a circle whose area is proportional
to the number of tasks in that cell, faceted by model and domain.
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
    RESULTS_DIR,
    _parse_config,
    apply_theme,
    make_title,
    render_rq,
)
from reasonable_agent import reasonable_score

ALLOWED_MODELS = {
    ("azure_pool-gpt-4-1", "cot"),
    ("azure_pool-gpt-5-4", "high"),
    ("gemini-3-flash-preview", "medium"),
}

OO_ORDER = ["High (≥0.5)", "Low (<0.5)"]
DD_ORDER = ["Low (<0.5)", "High (≥0.5)"]

CELL_COLORS = {
    ("High (≥0.5)", "High (≥0.5)"): "#2E8B57",  # Robust — green
    ("High (≥0.5)", "Low (<0.5)"): "#F0C75E",  # Lucky — yellow
    ("Low (<0.5)", "High (≥0.5)"): "#F0C75E",  # Ineffective — yellow
    ("Low (<0.5)", "Low (<0.5)"): "#C0392B",  # Negligent — red
}


def _model_label(model: str, mode: str) -> str:
    pretty = MODEL_LABELS.get(model, model)
    mode_label = MODE_LABELS.get(mode, mode) if mode else "no_cot"
    return f"{pretty} ({mode_label})"


def get_data() -> pd.DataFrame:
    rows: list[dict] = []
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
        if pc.attack_style != "normal":
            continue

        mlabel = _model_label(pc.model, pc.mode)
        if pc.domain == "marketplace":
            typed = load_marketplace_results(data)
        elif pc.domain == "calendar":
            typed = load_calendar_results(data)
        else:
            continue
        for r in typed:
            oo = r.outcome_optimality
            dd = reasonable_score(r)
            if oo is None or dd is None:
                continue
            rows.append(
                {
                    "domain": DOMAIN_LABELS.get(pc.domain, pc.domain),
                    "model_label": mlabel,
                    "oo_bin": "High (≥0.5)" if oo >= 0.5 else "Low (<0.5)",
                    "dd_bin": "High (≥0.5)" if dd >= 0.5 else "Low (<0.5)",
                }
            )

    df = pd.DataFrame(rows)
    counts = (
        df.groupby(["domain", "model_label", "oo_bin", "dd_bin"], observed=True)
        .size()
        .reset_index(name="count")
    )
    # Ensure all 4 cells exist for every domain×model combination
    idx = pd.MultiIndex.from_product(
        [counts["domain"].unique(), counts["model_label"].unique(), OO_ORDER, DD_ORDER],
        names=["domain", "model_label", "oo_bin", "dd_bin"],
    )
    result = (
        counts.set_index(["domain", "model_label", "oo_bin", "dd_bin"])
        .reindex(idx, fill_value=0)
        .reset_index()
    )
    # Convert to percentage within each domain×model group
    totals = result.groupby(["domain", "model_label"])["count"].transform("sum")
    result["pct"] = (result["count"] / totals * 100).round(1)
    result["pct_label"] = result["pct"].apply(lambda v: f"{v:.0f}%")
    result["cell_color"] = result.apply(lambda r: CELL_COLORS[(r["oo_bin"], r["dd_bin"])], axis=1)
    return result


def make_plot(df: pd.DataFrame) -> alt.Chart:
    color_domain = sorted(df["cell_color"].unique())

    bubbles = (
        alt.Chart(df)
        .mark_circle(opacity=1.0)
        .encode(
            x=alt.X("dd_bin:N", title="Due Diligence", sort=DD_ORDER, axis=alt.Axis(grid=True)),
            y=alt.Y(
                "oo_bin:N", title="Outcome Optimality", sort=OO_ORDER, axis=alt.Axis(grid=True)
            ),
            size=alt.Size(
                "pct:Q",
                scale=alt.Scale(domain=[0, 100], range=[0, 5027]),
                legend=None,
            ),
            color=alt.Color(
                "cell_color:N",
                scale=alt.Scale(domain=color_domain, range=color_domain),
                legend=None,
            ),
            tooltip=["domain:N", "model_label:N", "oo_bin:N", "dd_bin:N", "pct:Q"],
        )
    )

    label_outline = (
        alt.Chart(df)
        .mark_text(fontSize=13, fontWeight="bold", strokeWidth=2)
        .encode(
            x=alt.X("dd_bin:N", sort=DD_ORDER),
            y=alt.Y("oo_bin:N", sort=OO_ORDER),
            text="pct_label:N",
            stroke=alt.Color(
                "cell_color:N",
                scale=alt.Scale(domain=color_domain, range=color_domain),
                legend=None,
            ),
        )
    )

    label_fill = (
        alt.Chart(df)
        .mark_text(fontSize=13, fontWeight="bold", color="white")
        .encode(
            x=alt.X("dd_bin:N", sort=DD_ORDER),
            y=alt.Y("oo_bin:N", sort=OO_ORDER),
            text="pct_label:N",
        )
    )

    chart = (
        (bubbles + label_outline + label_fill)
        .properties(width=160, height=160)
        .facet(
            row=alt.Row(
                "domain:N",
                title=None,
                sort=DOMAIN_ORDER,
                header=alt.Header(labelFontWeight="bold"),
            ),
            column=alt.Column(
                "model_label:N",
                title=None,
                header=alt.Header(labelFontWeight="bold"),
            ),
        )
        .properties(
            title=make_title(
                "RQ7: Outcome Optimality vs Due Diligence (Benign Tasks)",
                "Bubble size = % of tasks · DD = reasonable_agent",
            )
        )
    )
    return apply_theme(chart)


def main() -> None:
    render_rq("rq7", get_data, make_plot)


if __name__ == "__main__":
    main()
