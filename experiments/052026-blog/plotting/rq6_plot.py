"""RQ6: Whimsical attacks do more damage than hand-crafted.

Slice: prompt=all, attack_style in {normal, hand_crafted, whimsical}. Compare
resulting OO across the benign baseline and the two attack styles, faceted by
domain (rows) and attack target (columns). The benign baseline is duplicated
across both target columns for visual reference.
"""


import altair as alt
import pandas as pd
from common import (
    DOMAIN_ORDER,
    PALETTE,
    apply_theme,
    load_runs,
    make_title,
    runs_to_df,
    save,
)

TARGET_LABELS = {"oo": "Outcome Optimality", "dd": "Due Diligence"}
STYLE_LABELS = {
    "normal": "Benign",
    "hand_crafted": "Hand-Crafted",
    "whimsical": "Whimsical",
}


def get_data() -> pd.DataFrame:
    df = runs_to_df(load_runs())
    df = df[df["prompt"] == "all"].copy()

    normal = df[df["attack_style"] == "normal"]
    benign_oo = normal.assign(attack_target="oo")
    benign_dd = normal.assign(attack_target="dd")
    attacks = df[df["attack_style"].isin(["hand_crafted", "whimsical"])]

    out = pd.concat([benign_oo, benign_dd, attacks], ignore_index=True)
    out["attack_target_label"] = out["attack_target"].map(TARGET_LABELS)
    out["attack_style_label"] = out["attack_style"].map(STYLE_LABELS)
    return out[
        [
            "domain",
            "model_label",
            "attack_style",
            "attack_style_label",
            "attack_target_label",
            "outcome_optimality",
        ]
    ]


def make_plot(df: pd.DataFrame) -> alt.Chart:
    style_order = ["Benign", "Hand-Crafted", "Whimsical"]
    style_range = [PALETTE["normal"], PALETTE["hand_crafted"], PALETTE["whimsical"]]

    base = alt.Chart(df).encode(
        x=alt.X("model_label:N", title=None, axis=alt.Axis(labelAngle=0)),
        y=alt.Y(
            "outcome_optimality:Q",
            title=None,
            scale=alt.Scale(domain=[0, 1]),
            axis=alt.Axis(format=".0%"),
        ),
        xOffset=alt.XOffset("attack_style_label:N", sort=style_order),
    )

    bars = base.mark_bar().encode(
        color=alt.Color(
            "attack_style_label:N",
            title="Condition",
            scale=alt.Scale(domain=style_order, range=style_range),
            legend=alt.Legend(orient="top"),
        ),
        tooltip=[
            "domain",
            "model_label",
            "attack_style_label",
            "attack_target_label",
            alt.Tooltip("outcome_optimality:Q", format=".1%"),
        ],
    )

    labels = base.mark_text(dy=-6, fontSize=10, color="#333").encode(
        text=alt.Text("outcome_optimality:Q", format=".0%")
    )

    chart = (
        (bars + labels)
        .properties(width=240, height=100)
        .facet(
            row=alt.Row(
                "domain:N",
                title=None,
                sort=DOMAIN_ORDER,
                header=alt.Header(labelFontWeight="bold"),
            ),
            column=alt.Column(
                "attack_target_label:N",
                title="Attack Target",
                header=alt.Header(labelFontWeight="bold"),
            ),
        )
        .resolve_axis(x="independent")
        .properties(
            title=make_title(
                "RQ6: Whimsical vs. Hand-Crafted Attacks on Outcome Optimality",
                "System prompt = all · benign baseline shown in grey",
            )
        )
    )
    return apply_theme(chart)


def main() -> None:
    df = get_data()
    chart = make_plot(df)
    out = save(chart, "rq6")
    print(f"saved {out}")


if __name__ == "__main__":
    main()
