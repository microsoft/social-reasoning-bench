"""RQ2: Under attacks, TC stays high but OO collapses.

Slice: prompt=all, all 5 attack conditions. x=attack condition, color=metric (TC/OO),
faceted by domain (rows) and model (columns).
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

CONDITION_ORDER = [
    "normal",
    "hand_crafted_oo",
    "hand_crafted_dd",
    "hand_crafted_privacy",
    "whimsical_oo",
    "whimsical_dd",
    "whimsical_privacy",
]

CONDITION_LABELS = {
    "normal": "Benign",
    "hand_crafted_oo": "HC · OO",
    "hand_crafted_dd": "HC · DD",
    "hand_crafted_privacy": "HC · Priv",
    "whimsical_oo": "Whim · OO",
    "whimsical_dd": "Whim · DD",
    "whimsical_privacy": "Whim · Priv",
}


def get_data() -> pd.DataFrame:
    df = runs_to_df(load_runs())
    df = df[df["prompt"] == "all"].copy()
    df["cond_key"] = df.apply(
        lambda r: "normal"
        if r["attack_style"] == "normal"
        else f"{r['attack_style']}_{r['attack_target']}",
        axis=1,
    )
    df["cond_label"] = df["cond_key"].map(CONDITION_LABELS)
    long = df.melt(
        id_vars=["domain", "model_label", "cond_key", "cond_label"],
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
    label_order = [CONDITION_LABELS[c] for c in CONDITION_ORDER]

    base = alt.Chart(df).encode(
        x=alt.X(
            "cond_label:N",
            title=None,
            sort=label_order,
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
            "cond_label",
            "metric",
            alt.Tooltip("score:Q", format=".1%"),
        ],
    )

    labels = base.mark_text(dy=-6, fontSize=9, color="#333").encode(
        text=alt.Text("score:Q", format=".0%")
    )

    chart = (
        (bars + labels)
        .properties(width=200, height=130)
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
                "RQ2: Task Completion vs. Outcome Optimality Under Attack",
                "All attack conditions · system prompt = all",
            )
        )
    )
    return apply_theme(chart)


def main() -> None:
    render_rq("rq2", get_data, make_plot)


if __name__ == "__main__":
    main()
