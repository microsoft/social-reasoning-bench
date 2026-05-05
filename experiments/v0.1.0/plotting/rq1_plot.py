"""RQ1: On benign tasks, TC is high while OO is lower.

Slice: prompt=all, attack=normal. Bars: TC vs OO per model, faceted by domain.
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


def get_data() -> pd.DataFrame:
    df = runs_to_df(load_runs())
    df = df[(df["prompt"] == "all") & (df["attack_style"] == "normal")].copy()
    long = df.melt(
        id_vars=["domain", "model_label"],
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
        x=alt.X("model_label:N", title=None, axis=alt.Axis(labelAngle=-30)),
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
        tooltip=["domain", "model_label", "metric", alt.Tooltip("score:Q", format=".1%")],
    )

    labels = base.mark_text(dy=-6, fontSize=10, color="#333").encode(
        text=alt.Text("score:Q", format=".0%")
    )

    is_combined = df["domain"].nunique() > 1
    facet_kwargs = (
        {"column": alt.Column("domain:N", title=None, sort=DOMAIN_ORDER, header=alt.Header(labelFontWeight="bold"))}
        if is_combined
        else {"row": alt.Row("domain:N", title=None, sort=DOMAIN_ORDER, header=alt.Header(labelFontWeight="bold"))}
    )
    width = 280 if is_combined else 520
    chart = (
        (bars + labels)
        .properties(width=width, height=160)
        .facet(**facet_kwargs)
        .resolve_axis(x="independent")
        .properties(
            title=make_title(
                "RQ1: Task Completion vs. Outcome Optimality",
                "Benign tasks · system prompt = all",
            )
        )
    )
    return apply_theme(chart)


def main() -> None:
    render_rq("rq1", get_data, make_plot)


if __name__ == "__main__":
    main()
