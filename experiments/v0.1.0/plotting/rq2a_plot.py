"""RQ2a: Same as RQ2, but averages TC/OO across attack targets per attack style.

Slice: prompt=all. Three bars per model per metric: Benign, Hand-Crafted (avg
across oo/dd/privacy), Whimsical (avg across oo/dd/privacy).
"""


import altair as alt
import pandas as pd
from common import (
    DOMAIN_ORDER,
    PALETTE,
    apply_theme,
    load_runs,
    make_title,
    render_rq,
    runs_to_df,
)

STYLE_ORDER = ["Benign", "Hand-Crafted", "Whimsical"]
STYLE_LABELS = {"normal": "Benign", "hand_crafted": "Hand-Crafted", "whimsical": "Whimsical"}


def get_data() -> pd.DataFrame:
    df = runs_to_df(load_runs())
    df = df[df["prompt"] == "all"].copy()
    grouped = (
        df.groupby(["domain", "model_label", "attack_style"], as_index=False)[
            ["task_completion", "outcome_optimality"]
        ]
        .mean()
    )
    grouped["attack_style_label"] = grouped["attack_style"].map(STYLE_LABELS)
    long = grouped.melt(
        id_vars=["domain", "model_label", "attack_style", "attack_style_label"],
        value_vars=["task_completion", "outcome_optimality"],
        var_name="metric",
        value_name="score",
    )
    long["metric"] = long["metric"].map(
        {"task_completion": "Task Completion", "outcome_optimality": "Outcome Optimality"}
    )
    return long


def make_plot(df: pd.DataFrame) -> alt.Chart:
    metric_domain = ["Task Completion", "Outcome Optimality"]
    metric_range = [PALETTE["task_completion"], PALETTE["outcome_optimality"]]

    base = alt.Chart(df).encode(
        x=alt.X(
            "attack_style_label:N",
            title=None,
            sort=STYLE_ORDER,
            axis=alt.Axis(labelAngle=-30),
        ),
        y=alt.Y(
            "score:Q",
            title=None,
            scale=alt.Scale(domain=[0, 1]),
            axis=alt.Axis(format=".0%"),
        ),
        xOffset=alt.XOffset("metric:N", sort=metric_domain),
    )

    bars = base.mark_bar().encode(
        color=alt.Color(
            "metric:N",
            title=None,
            scale=alt.Scale(domain=metric_domain, range=metric_range),
            legend=alt.Legend(orient="top"),
        ),
        tooltip=[
            "domain",
            "model_label",
            "attack_style_label",
            "metric",
            alt.Tooltip("score:Q", format=".1%"),
        ],
    )

    labels = base.mark_text(dy=-6, fontSize=9, color="#333").encode(
        text=alt.Text("score:Q", format=".0%")
    )

    chart = (
        (bars + labels)
        .properties(width=180, height=140)
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
                "RQ2a: TC vs. OO Under Attack (averaged across attack targets)",
                "System prompt = all · attack styles averaged over oo/dd/privacy",
            )
        )
    )
    return apply_theme(chart)


def main() -> None:
    render_rq("rq2a", get_data, make_plot)


if __name__ == "__main__":
    main()
