"""Finding 1: Task Completion is high while Outcome Optimality is lower.

Slice: benign tasks (attack=normal), both prompts.  Per (domain, model) we
plot four bars:

* Task Completion (averaged across both prompts)
* Outcome Optimality — basic prompt (system_prompt=none)
* Outcome Optimality — defensive prompt (system_prompt=all)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import altair as alt
import pandas as pd
from utils import loader, plotting

# ── Series definitions ───────────────────────────────────────────


METRIC_TC = "Task Completion"
METRIC_OO_BASIC = "Outcome Optimality (Basic Prompt)"
METRIC_OO_DEFENSIVE = "Outcome Optimality (Defensive Prompt)"


METRIC_ORDER: list[str] = [
    METRIC_TC,
    METRIC_OO_BASIC,
    METRIC_OO_DEFENSIVE,
]

METRIC_COLORS: dict[str, str] = {
    METRIC_TC: plotting.PALETTE.task_completion,
    METRIC_OO_BASIC: plotting.PALETTE.oo_basic,
    METRIC_OO_DEFENSIVE: plotting.PALETTE.oo_defensive,
}


# ── Aggregation ──────────────────────────────────────────────────


@dataclass(frozen=True)
class CellKey:
    domain_label: str
    model_label: str


@dataclass
class Samples:
    """Running tally of values across tasks for one metric series."""

    total: float = 0.0
    count: int = 0

    def add(self, value: float) -> None:
        self.total += value
        self.count += 1

    @property
    def mean(self) -> float | None:
        if self.count == 0:
            return None
        return self.total / self.count


@dataclass
class CellAccumulator:
    task_completion: Samples = field(default_factory=Samples)
    oo_basic: Samples = field(default_factory=Samples)
    oo_defensive: Samples = field(default_factory=Samples)

    def add_outcome_optimality(self, value: float, prompt: str) -> None:
        if prompt == "none":
            self.oo_basic.add(value)
        elif prompt == "all":
            self.oo_defensive.add(value)

    def metric_score(self, metric: str) -> float | None:
        if metric == METRIC_TC:
            return self.task_completion.mean
        if metric == METRIC_OO_BASIC:
            return self.oo_basic.mean
        if metric == METRIC_OO_DEFENSIVE:
            return self.oo_defensive.mean
        raise ValueError(f"unknown metric: {metric}")


def _accumulate() -> dict[CellKey, CellAccumulator]:
    cells: dict[CellKey, CellAccumulator] = {}

    for run in loader.iter_runs(filters=loader.RunDimsFilter(include_attacks=False)):
        key = CellKey(
            domain_label=run.dims.domain_label,
            model_label=run.dims.model_label,
        )
        cell = cells.setdefault(key, CellAccumulator())
        for result in run.iter_results():
            cell.task_completion.add(float(result.task_completed))
            cell.add_outcome_optimality(result.outcome_optimality, run.dims.defense_prompt)

    return cells


def _build_dataframe(cells: dict[CellKey, CellAccumulator]) -> pd.DataFrame:
    records: list[dict] = []
    for key, cell in cells.items():
        for metric in METRIC_ORDER:
            score = cell.metric_score(metric)
            if score is None:
                continue
            records.append(
                {
                    "domain": key.domain_label,
                    "model_label": key.model_label,
                    "metric": metric,
                    "score": score,
                }
            )
    return pd.DataFrame(records)


# ── Plot ─────────────────────────────────────────────────────────


def _make_chart(df: pd.DataFrame) -> alt.FacetChart:
    color_range = [METRIC_COLORS[name] for name in METRIC_ORDER]

    base = alt.Chart(df).encode(
        x=plotting.model_x(df["model_label"], title=None),
        y=alt.Y(
            "score:Q",
            title=None,
            scale=alt.Scale(domain=[0, 1]),
            axis=alt.Axis(format=".0%"),
        ),
        xOffset=alt.XOffset("metric:N", sort=METRIC_ORDER),
    )

    bars = base.mark_bar().encode(
        color=alt.Color(
            "metric:N",
            title=None,
            scale=alt.Scale(domain=METRIC_ORDER, range=color_range),
            legend=alt.Legend(orient="top", columns=2),
        ),
        tooltip=[
            "domain",
            "model_label",
            "metric",
            alt.Tooltip("score:Q", format=".1%"),
        ],
    )

    labels = base.mark_text(dy=-6, fontSize=9, color="#333").encode(
        text=alt.Text("score:Q", format=".0%"),
    )

    return (
        (bars + labels)
        .properties(width=320, height=180)
        .facet(
            column=alt.Column(
                "domain:N",
                title=None,
                sort=plotting.DOMAIN_ORDER,
                header=alt.Header(labelFontWeight="bold"),
            ),
        )
        .resolve_axis(x="independent")
        .properties(
            title=plotting.make_title(
                "Task Completion vs. Outcome Optimality",
                "Benign tasks · prompt breakdown shows defensive vs. basic system prompt",
            )
        )
    )


# ── Entry point ──────────────────────────────────────────────────


def main() -> Path:
    cells = _accumulate()
    df = _build_dataframe(cells)
    chart = plotting.apply_theme(_make_chart(df))
    out_path = plotting.save(chart, "finding1")
    print(f"saved {out_path}")
    return out_path


if __name__ == "__main__":
    main()
