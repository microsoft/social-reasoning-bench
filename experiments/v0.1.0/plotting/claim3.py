"""Claim 3: Outcome-Optimality distribution per model and domain.

Each task contributes one dot.  A black tick marks the per-cell mean.

Two figures are produced:

* ``claim3_all`` — all benign tasks
* ``claim3_completed`` — tasks where the agent reported completion (TC=1)
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import altair as alt
import numpy as np
import pandas as pd
from utils import loader, plotting

JITTER_STD: float = 0.08
JITTER_RANGE: tuple[float, float] = (-0.5, 0.5)
JITTER_SEED: int = 0


# ── Per-task collection ──────────────────────────────────────────


@dataclass(frozen=True)
class TaskPoint:
    domain_label: str
    model_label: str
    outcome_optimality: float
    task_completed: bool


def _collect_points() -> list[TaskPoint]:
    points: list[TaskPoint] = []
    for run in loader.iter_runs(filters=loader.RunDimsFilter(include_attacks=False)):
        for result in run.iter_results():
            points.append(
                TaskPoint(
                    domain_label=run.dims.domain_label,
                    model_label=run.dims.model_label,
                    outcome_optimality=result.outcome_optimality,
                    task_completed=bool(result.task_completed),
                )
            )
    return points


def _points_to_df(points: list[TaskPoint]) -> pd.DataFrame:
    records: list[dict] = []
    for point in points:
        records.append(
            {
                "domain": point.domain_label,
                "model_label": point.model_label,
                "oo": point.outcome_optimality,
                "tc": point.task_completed,
            }
        )
    df = pd.DataFrame(records)
    rng = np.random.default_rng(JITTER_SEED)
    df["jitter"] = rng.normal(0.0, JITTER_STD, size=len(df))
    return df


# ── Plot ─────────────────────────────────────────────────────────


def _make_chart(df: pd.DataFrame, title: str, subtitle: str) -> alt.FacetChart:
    model_order = sorted(df["model_label"].unique())
    color_range = plotting.PALETTE.series[: len(model_order)]

    base = alt.Chart(df).transform_joinaggregate(
        mean_oo="mean(oo)",
        groupby=["domain", "model_label"],
    )

    points_layer = base.mark_circle(size=30, opacity=0.4).encode(
        x=alt.X(
            "model_label:N",
            title=None,
            sort=model_order,
        ),
        xOffset=alt.XOffset(
            "jitter:Q",
            scale=alt.Scale(domain=list(JITTER_RANGE)),
        ),
        y=alt.Y(
            "oo:Q",
            title="Outcome Optimality",
            scale=alt.Scale(domain=[-0.05, 1.05]),
            axis=alt.Axis(grid=True, gridColor=plotting.GRAY.g200),
        ),
        color=alt.Color(
            "model_label:N",
            title=None,
            sort=model_order,
            scale=alt.Scale(domain=model_order, range=color_range),
            legend=None,
        ),
        tooltip=[
            "domain",
            "model_label",
            alt.Tooltip("oo:Q", format=".2f"),
        ],
    )

    mean_ticks = base.mark_tick(thickness=3, size=24, color="black").encode(
        x=alt.X("model_label:N", sort=model_order),
        y=alt.Y("mean_oo:Q"),
    )

    mean_labels = base.mark_text(
        align="left",
        dx=14,
        fontSize=10,
        fontWeight="bold",
    ).encode(
        x=alt.X("model_label:N", sort=model_order),
        y=alt.Y("mean_oo:Q"),
        text=alt.Text("mean_oo:Q", format=".2f"),
    )

    layered = alt.layer(points_layer, mean_ticks, mean_labels).properties(
        width=320,
        height=240,
    )

    return (
        layered.facet(
            column=alt.Column(
                "domain:N",
                title=None,
                sort=plotting.DOMAIN_ORDER,
                header=alt.Header(labelFontWeight="bold"),
            ),
        )
        .resolve_axis(x="independent")
        .properties(title=plotting.make_title(title, subtitle))
    )


# ── Entry point ──────────────────────────────────────────────────


def main() -> list[Path]:
    points = _collect_points()
    df_all = _points_to_df(points)
    completed_mask = df_all["tc"].astype(bool)
    df_completed = df_all.loc[completed_mask].copy()

    chart_all = plotting.apply_theme(
        _make_chart(
            df_all,
            "OO Distribution on Benign Tasks",
            "Each dot = one task · black tick = mean",
        )
    )

    out_paths = [
        plotting.save(chart_all, "claim3"),
    ]
    for path in out_paths:
        print(f"saved {path}")
    return out_paths


if __name__ == "__main__":
    main()
