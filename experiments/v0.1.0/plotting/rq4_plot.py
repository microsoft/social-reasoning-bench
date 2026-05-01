"""RQ4: Most models perform poorly on DoC; prompting helps but doesn't close the gap.

Slice: attack=normal, prompt in {none, all}. y=DoC, x=model, color=prompt, facet=domain.
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
    df = df[df["attack_style"] == "normal"].copy()
    return df[["domain", "model_label", "prompt", "duty_of_care"]]


def make_plot(df: pd.DataFrame) -> alt.Chart:
    prompt_order = ["none", "all"]
    prompt_range = [PALETTE["none"], PALETTE["all"]]

    base = alt.Chart(df).encode(
        x=alt.X("model_label:N", title=None, axis=alt.Axis(labelAngle=-30)),
        y=alt.Y(
            "duty_of_care:Q",
            title=None,
            scale=alt.Scale(domain=[0, 1]),
            axis=alt.Axis(format=".0%"),
        ),
        xOffset=alt.XOffset("prompt:N", sort=prompt_order),
    )

    bars = base.mark_bar().encode(
        color=alt.Color(
            "prompt:N",
            title="System prompt",
            scale=alt.Scale(domain=prompt_order, range=prompt_range),
            legend=alt.Legend(orient="top"),
        ),
        tooltip=[
            "domain",
            "model_label",
            "prompt",
            alt.Tooltip("duty_of_care:Q", format=".1%"),
        ],
    )

    labels = base.mark_text(dy=-6, fontSize=10, color="#333").encode(
        text=alt.Text("duty_of_care:Q", format=".0%")
    )

    chart = (
        (bars + labels)
        .properties(width=520, height=160)
        .facet(
            row=alt.Row(
                "domain:N",
                title=None,
                sort=DOMAIN_ORDER,
                header=alt.Header(labelFontWeight="bold"),
            )
        )
        .resolve_axis(x="independent")
        .properties(
            title=make_title(
                "RQ4: Duty of Care by Model and System Prompt",
                "Benign tasks · system prompt ∈ {none, all}",
            )
        )
    )
    return apply_theme(chart)


def main() -> None:
    render_rq("rq4", get_data, make_plot)


if __name__ == "__main__":
    main()
