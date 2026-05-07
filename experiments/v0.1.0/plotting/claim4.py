"""Claim 4: Bubble matrix of binarised Outcome Optimality vs. Due Diligence.

For benign tasks (prompt = all), each task's OO and DD are split at 0.5 into
Low / High bins.  Within each (domain, model) cell we compute the percentage
of tasks falling in each of the four (OO, DD) corners and draw a bubble
whose area is proportional to that percentage.

Cell colours:

* High OO + High DD → robust (green)
* High OO + Low DD or Low OO + High DD → mixed (yellow)
* Low OO + Low DD → negligent (red)

Due Diligence is computed by the deterministic ``reasonable_agent`` policy
counterfactual rather than the LLM judge score.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import altair as alt
import pandas as pd
from utils import loader, plotting

# ── Bin labels and palette ───────────────────────────────────────


OO_HIGH = "High (≥0.5)"
OO_LOW = "Low (<0.5)"
DD_HIGH = "High (≥0.5)"
DD_LOW = "Low (<0.5)"

OO_ORDER: list[str] = [OO_HIGH, OO_LOW]
DD_ORDER: list[str] = [DD_LOW, DD_HIGH]


@dataclass(frozen=True)
class CellLabel:
    oo_bin: str
    dd_bin: str


CELL_COLORS: dict[CellLabel, str] = {
    CellLabel(OO_HIGH, DD_HIGH): plotting.PALETTE.cell_robust,
    CellLabel(OO_HIGH, DD_LOW): plotting.PALETTE.cell_mixed,
    CellLabel(OO_LOW, DD_HIGH): plotting.PALETTE.cell_mixed,
    CellLabel(OO_LOW, DD_LOW): plotting.PALETTE.cell_negligent,
}


def _bin(score: float, *, high_label: str, low_label: str) -> str:
    return high_label if score >= 0.5 else low_label


# ── Per-task collection ──────────────────────────────────────────


@dataclass(frozen=True)
class BinnedTask:
    domain_label: str
    model_label: str
    oo_bin: str
    dd_bin: str


def _collect_binned_tasks() -> list[BinnedTask]:
    binned: list[BinnedTask] = []

    benign_all_prompt = loader.RunDimsFilter(defense_prompt="all", include_attacks=False)
    for run in loader.iter_runs(filters=benign_all_prompt):
        for result in run.iter_results():
            binned.append(
                BinnedTask(
                    domain_label=run.dims.domain_label,
                    model_label=run.dims.model_label,
                    oo_bin=_bin(result.outcome_optimality, high_label=OO_HIGH, low_label=OO_LOW),
                    dd_bin=_bin(result.due_diligence, high_label=DD_HIGH, low_label=DD_LOW),
                )
            )

    return binned


# ── DataFrame assembly ───────────────────────────────────────────


def _full_grid_index(df: pd.DataFrame) -> pd.MultiIndex:
    return pd.MultiIndex.from_product(
        [
            df["domain"].unique(),
            df["model_label"].unique(),
            OO_ORDER,
            DD_ORDER,
        ],
        names=["domain", "model_label", "oo_bin", "dd_bin"],
    )


def _build_dataframe(tasks: list[BinnedTask]) -> pd.DataFrame:
    records: list[dict] = []
    for task in tasks:
        records.append(
            {
                "domain": task.domain_label,
                "model_label": task.model_label,
                "oo_bin": task.oo_bin,
                "dd_bin": task.dd_bin,
            }
        )
    raw = pd.DataFrame(records)
    grid_keys = ["domain", "model_label", "oo_bin", "dd_bin"]
    counts = raw.groupby(grid_keys).size().to_frame("count").reset_index()

    full_grid = (
        counts.set_index(grid_keys).reindex(_full_grid_index(counts), fill_value=0).reset_index()
    )

    totals = full_grid.groupby(["domain", "model_label"])["count"].transform("sum")
    full_grid["pct"] = (full_grid["count"] / totals * 100).round(1)
    full_grid["pct_label"] = full_grid["pct"].map(lambda value: f"{value:.0f}%")

    cell_colors: list[str] = []
    for oo_bin, dd_bin in zip(full_grid["oo_bin"], full_grid["dd_bin"]):
        cell_colors.append(CELL_COLORS[CellLabel(str(oo_bin), str(dd_bin))])
    full_grid["cell_color"] = cell_colors
    return full_grid


# ── Plot ─────────────────────────────────────────────────────────


def _make_chart(df: pd.DataFrame) -> alt.FacetChart:
    color_domain = sorted(df["cell_color"].unique())

    bubbles = (
        alt.Chart(df)
        .mark_circle(opacity=1.0)
        .encode(
            x=alt.X(
                "dd_bin:N",
                title="Due Diligence",
                sort=DD_ORDER,
                axis=alt.Axis(grid=True),
            ),
            y=alt.Y(
                "oo_bin:N",
                title="Outcome Optimality",
                sort=OO_ORDER,
                axis=alt.Axis(grid=True),
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
            tooltip=[
                "domain:N",
                "model_label:N",
                "oo_bin:N",
                "dd_bin:N",
                alt.Tooltip("pct:Q", format=".1f"),
            ],
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

    return (
        (bubbles + label_outline + label_fill)
        .properties(width=160, height=160)
        .facet(
            row=alt.Row(
                "domain:N",
                title=None,
                sort=plotting.DOMAIN_ORDER,
                header=alt.Header(labelFontWeight="bold"),
            ),
            column=alt.Column(
                "model_label:N",
                title=None,
                header=alt.Header(labelFontWeight="bold"),
            ),
        )
        .properties(
            title=plotting.make_title(
                "Outcome Optimality vs. Due Diligence (Benign Tasks)",
                "Bubble size = % of tasks · DD = reasonable-agent counterfactual",
            )
        )
    )


# ── Entry point ──────────────────────────────────────────────────


def main() -> Path:
    tasks = _collect_binned_tasks()
    df = _build_dataframe(tasks)
    chart = plotting.apply_theme(_make_chart(df))
    out_path = plotting.save(chart, "claim4")
    print(f"saved {out_path}")
    return out_path


if __name__ == "__main__":
    main()
