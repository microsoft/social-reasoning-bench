"""Finding 5: Behavior under attack — refusal rate + OO when engaged.

Slice: prompt = all, privacy attacks excluded.  Adversarial = handcrafted +
whimsical attacks merged.  Two metrics × two domains:

* Refusal rate — fraction of tasks where the agent declined to engage.
* OO when engaged — continuous benign OO over engaged tasks.  Tasks that
  hit ``max_rounds`` are counted as engaged with OO=0.

The plot is a 2×2 facet (rows = domain, columns = metric) of grouped bars
comparing benign and adversarial requestors per model.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import altair as alt
import pandas as pd
from srbench.benchmarks.calendar_scheduling.types import (
    CalendarEvaluationResult,
)
from srbench.benchmarks.marketplace.types import MarketplaceEvaluationResult
from utils import loader, plotting

# ── Series definitions ───────────────────────────────────────────


CONDITION_BENIGN = "Benign Counterparty"
CONDITION_ADVERSARIAL = "Adversarial Counterpart"

CONDITION_ORDER: list[str] = [CONDITION_BENIGN, CONDITION_ADVERSARIAL]
CONDITION_COLORS: dict[str, str] = {
    CONDITION_BENIGN: plotting.PALETTE.benign,
    CONDITION_ADVERSARIAL: plotting.PALETTE.adversarial,
}

METRIC_REFUSAL = "Refusal Rate"
METRIC_OO_ENGAGED = "OO When Engaged"

METRIC_ORDER: list[str] = [METRIC_REFUSAL, METRIC_OO_ENGAGED]


# ── Engagement classification ────────────────────────────────────


@dataclass(frozen=True)
class TaskOutcome:
    refused: bool
    engaged_oo: float | None  # None when refused; 0.0 when max_rounds hit


def _classify(result: loader.EvalResult, max_rounds: int) -> TaskOutcome:
    if isinstance(result, MarketplaceEvaluationResult):
        deal_reached = result.execution.outcome.deal_reached
        ended_by = result.execution.outcome.ended_by or ""
        if deal_reached:
            return TaskOutcome(refused=False, engaged_oo=result.outcome_optimality)
        if ended_by == "max_rounds":
            return TaskOutcome(refused=False, engaged_oo=0.0)
        return TaskOutcome(refused=True, engaged_oo=None)

    if isinstance(result, CalendarEvaluationResult):
        if result.scheduled_meeting is not None:
            return TaskOutcome(refused=False, engaged_oo=result.outcome_optimality)
        if result.execution.rounds_completed >= max_rounds:
            return TaskOutcome(refused=False, engaged_oo=0.0)
        return TaskOutcome(refused=True, engaged_oo=None)

    raise TypeError(f"unsupported result type: {type(result).__name__}")


# ── Aggregation ──────────────────────────────────────────────────


@dataclass(frozen=True)
class CellKey:
    domain_label: str
    model_label: str
    condition: str  # CONDITION_BENIGN | CONDITION_ADVERSARIAL


@dataclass
class CellAccumulator:
    n_engaged: int = 0
    n_refused: int = 0
    engaged_oo_values: list[float] = field(default_factory=list)

    def add(self, outcome: TaskOutcome) -> None:
        if outcome.refused:
            self.n_refused += 1
            return
        self.n_engaged += 1
        if outcome.engaged_oo is not None:
            self.engaged_oo_values.append(outcome.engaged_oo)

    @property
    def refusal_rate(self) -> float | None:
        total = self.n_engaged + self.n_refused
        if total == 0:
            return None
        return self.n_refused / total

    @property
    def mean_engaged_oo(self) -> float | None:
        if not self.engaged_oo_values:
            return None
        return sum(self.engaged_oo_values) / len(self.engaged_oo_values)


def _condition_label(run: loader.Run) -> str:
    if run.dims.attack is None:
        return CONDITION_BENIGN
    return CONDITION_ADVERSARIAL


def _accumulate() -> dict[CellKey, CellAccumulator]:
    cells: dict[CellKey, CellAccumulator] = {}

    for run in loader.iter_runs(filters=loader.RunDimsFilter(defense_prompt="all")):
        if run.dims.attack is not None and run.dims.attack.target == "privacy":
            continue

        key = CellKey(
            domain_label=run.dims.domain_label,
            model_label=run.dims.model_label,
            condition=_condition_label(run),
        )
        cell = cells.setdefault(key, CellAccumulator())
        max_rounds = run.config.max_rounds

        for result in run.iter_results():
            cell.add(_classify(result, max_rounds))

    return cells


# ── DataFrame assembly ───────────────────────────────────────────


def _build_dataframe(cells: dict[CellKey, CellAccumulator]) -> pd.DataFrame:
    records: list[dict] = []
    for key, cell in cells.items():
        refusal = cell.refusal_rate
        if refusal is not None:
            records.append(
                {
                    "domain": key.domain_label,
                    "model_label": key.model_label,
                    "condition": key.condition,
                    "metric": METRIC_REFUSAL,
                    "score": refusal,
                }
            )
        mean_oo = cell.mean_engaged_oo
        if mean_oo is not None:
            records.append(
                {
                    "domain": key.domain_label,
                    "model_label": key.model_label,
                    "condition": key.condition,
                    "metric": METRIC_OO_ENGAGED,
                    "score": mean_oo,
                }
            )
    return pd.DataFrame(records)


# ── Plot ─────────────────────────────────────────────────────────


def _make_chart(df: pd.DataFrame) -> alt.FacetChart:
    color_range = [CONDITION_COLORS[name] for name in CONDITION_ORDER]

    base = alt.Chart(df).encode(
        x=alt.X("model_label:N", title=None),
        y=alt.Y(
            "score:Q",
            title=None,
            scale=alt.Scale(domain=[0, 1]),
            axis=alt.Axis(format=".0%"),
        ),
        xOffset=alt.XOffset("condition:N", sort=CONDITION_ORDER),
    )

    bars = base.mark_bar().encode(
        color=alt.Color(
            "condition:N",
            title=None,
            scale=alt.Scale(domain=CONDITION_ORDER, range=color_range),
            legend=alt.Legend(orient="top"),
        ),
        tooltip=[
            "domain",
            "model_label",
            "condition",
            "metric",
            alt.Tooltip("score:Q", format=".1%"),
        ],
    )

    labels = base.mark_text(dy=-6, fontSize=10, color="#333").encode(
        text=alt.Text("score:Q", format=".0%"),
    )

    return (
        (bars + labels)
        .properties(width=340, height=180)
        .facet(
            row=alt.Row(
                "domain:N",
                title=None,
                sort=plotting.DOMAIN_ORDER,
                header=alt.Header(labelFontWeight="bold"),
            ),
            column=alt.Column(
                "metric:N",
                title=None,
                sort=METRIC_ORDER,
                header=alt.Header(labelFontWeight="bold"),
            ),
        )
        .resolve_axis(x="independent")
        .properties(
            title=plotting.make_title(
                "Behavior Under Attack",
                "Adversarial = handcrafted + whimsical (privacy excluded) · prompt = all",
            )
        )
    )


# ── Entry point ──────────────────────────────────────────────────


def main() -> Path:
    cells = _accumulate()
    df = _build_dataframe(cells)
    chart = plotting.apply_theme(_make_chart(df))
    out_path = plotting.save(chart, "finding5")
    print(f"saved {out_path}")
    return out_path


if __name__ == "__main__":
    main()
