"""RQ7c: Duty of Care stacked bars using true OO × Reasonableness.

Like RQ7iii but uses the original OO scores (binary 0/1 for malicious tasks)
instead of benign re-scoring.  Includes all conditions as separate bars.
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
from reasonable_agent import reasonable_score

ALLOWED_MODELS = {
    ("azure_pool-gpt-4-1", "cot"),
    ("azure_pool-gpt-5-4", "high"),
    ("gemini-3-flash-preview", "medium"),
}

ARCHETYPE_ORDER = ["Robust", "Lucky", "Ineffective", "Negligent"]
ARCHETYPE_COLORS = ["#2E8B57", "#F0C75E", "#E6740C", "#C0392B"]

STYLE_ORDER = ["Benign", "Hand-Crafted", "Whimsical"]
STYLE_LABELS = {
    "normal": "Benign",
    "hand_crafted": "Hand-Crafted",
    "whimsical": "Whimsical",
}


def _archetype(oo_high: bool, dd_high: bool) -> str:
    if oo_high and dd_high:
        return "Robust"
    if oo_high and not dd_high:
        return "Lucky"
    if not oo_high and dd_high:
        return "Ineffective"
    return "Negligent"


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
        if (pc.model, pc.mode) not in ALLOWED_MODELS:
            continue

        if pc.domain == "marketplace":
            typed = load_marketplace_results(data)
        elif pc.domain == "calendar":
            typed = load_calendar_results(data)
        else:
            continue

        mlabel = _model_label(pc.model, pc.mode)
        style_label = STYLE_LABELS.get(pc.attack_style, pc.attack_style)
        for r in typed:
            oo = r.outcome_optimality
            dd = reasonable_score(r)
            if oo is None or dd is None:
                continue
            rows.append(
                {
                    "domain": DOMAIN_LABELS.get(pc.domain, pc.domain),
                    "model_label": mlabel,
                    "style_label": style_label,
                    "archetype": _archetype(oo >= 0.5, dd >= 0.5),
                }
            )

    df = pd.DataFrame(rows)
    counts = (
        df.groupby(["domain", "model_label", "style_label", "archetype"], observed=True)
        .size()
        .reset_index(name="count")  # ty: ignore[no-matching-overload]
    )
    idx = pd.MultiIndex.from_product(
        [counts["domain"].unique(), counts["model_label"].unique(), STYLE_ORDER, ARCHETYPE_ORDER],
        names=["domain", "model_label", "style_label", "archetype"],
    )
    counts = (
        counts.set_index(["domain", "model_label", "style_label", "archetype"])
        .reindex(idx, fill_value=0)
        .reset_index()
    )
    totals = counts.groupby(["domain", "model_label", "style_label"])["count"].transform("sum")
    counts["pct"] = counts["count"] / totals
    return counts


def make_plot(df: pd.DataFrame) -> alt.Chart:
    sort_map = {"Negligent": 0, "Ineffective": 1, "Lucky": 2, "Robust": 3}
    df = df.copy()
    df["sort_key"] = df["archetype"].map(sort_map)

    bars = (
        alt.Chart(df)
        .mark_bar()
        .encode(
            x=alt.X("style_label:N", title=None, sort=STYLE_ORDER, axis=alt.Axis(labelAngle=-30)),
            y=alt.Y(
                "pct:Q",
                title=None,
                stack="zero",
                scale=alt.Scale(domain=[0, 1]),
                axis=alt.Axis(format=".0%"),
            ),
            color=alt.Color(
                "archetype:N",
                title=None,
                scale=alt.Scale(domain=ARCHETYPE_ORDER, range=ARCHETYPE_COLORS),
                legend=alt.Legend(orient="top"),
            ),
            order=alt.Order("sort_key:Q"),
            tooltip=[
                "domain:N",
                "model_label:N",
                "style_label:N",
                "archetype:N",
                alt.Tooltip("pct:Q", format=".1%"),
            ],
        )
    )

    chart = (
        bars.properties(width=150, height=200)
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
        .resolve_axis(x="independent")
        .properties(
            title=make_title(
                "RQ7c: Duty of Care by Condition (True OO)",
                "Stacked by archetype (True OO) · DD = reasonable_agent",
            )
        )
    )
    return apply_theme(chart)


def main() -> None:
    render_rq("rq7c", get_data, make_plot)


if __name__ == "__main__":
    main()
