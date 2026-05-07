"""Altair theming + save helpers shared by claim plots."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import altair as alt

FIGURES_DIR: Path = Path(__file__).resolve().parents[1] / "figures"


# ── Palette ──────────────────────────────────────────────────────
#
# Sage brand palette plus muted chart accents for cross-series comparisons
# and saturated series colors reserved for the third group-by dimension.


@dataclass(frozen=True)
class Sage:
    s50: str = "#f0f6f1"
    s100: str = "#dceadf"
    s200: str = "#bbd6c1"
    s300: str = "#93bb9d"
    s400: str = "#7db88d"
    s500: str = "#6b9e78"
    s600: str = "#5a8a66"
    s700: str = "#4a7a56"
    s800: str = "#3d6347"
    s900: str = "#33523b"


@dataclass(frozen=True)
class Gray:
    g50: str = "#fafafa"
    g100: str = "#f5f5f5"
    g200: str = "#e5e5e5"
    g300: str = "#d4d4d4"
    g400: str = "#a3a3a3"
    g500: str = "#737373"
    g600: str = "#525252"
    g700: str = "#404040"
    g800: str = "#262626"
    g900: str = "#171717"
    g950: str = "#0a0a0a"


@dataclass(frozen=True)
class Series:
    """Saturated accents — primary chart palette."""

    sage: str = "#6b9e78"
    tile: str = "#3d8aa8"
    apricot: str = "#e08545"
    guard: str = "#d44545"
    shell: str = "#e8b8a8"
    sand: str = "#dcd4a8"
    flare: str = "#f5c518"


SAGE = Sage()
GRAY = Gray()
SERIES = Series()


@dataclass(frozen=True)
class Palette:
    """Semantic colors.

    Data series use saturated :class:`Series` colors throughout.  Grays
    are reserved for neutral baselines (task completion, benign reference).
    """

    # Neutral baselines — same gray everywhere a "reference / non-adversarial"
    # bar appears (task completion in claim1, benign requestor in claim5).
    task_completion: str = SERIES.sand
    benign: str = SERIES.sand

    # Outcome Optimality breakdown — non-semantic series colors
    oo_overall: str = SERIES.sage
    oo_basic: str = SERIES.tile
    oo_defensive: str = SERIES.apricot

    # Adversarial condition
    adversarial: str = SERIES.guard

    # OO×DD bubble cells
    cell_robust: str = SERIES.sage
    cell_mixed: str = SERIES.flare
    cell_negligent: str = SERIES.guard

    series: list[str] = field(
        default_factory=lambda: [
            SERIES.sage,
            SERIES.tile,
            SERIES.apricot,
            SERIES.guard,
            SERIES.shell,
        ]
    )


PALETTE = Palette()


# ── Domain ordering ──────────────────────────────────────────────


DOMAIN_ORDER: list[str] = ["Calendar", "Marketplace"]


# ── Title helper ─────────────────────────────────────────────────


def make_title(text: str, subtitle: str = "") -> alt.TitleParams:
    return alt.TitleParams(text=text, subtitle=subtitle)


# ── Theme ────────────────────────────────────────────────────────


ThemableChart = alt.Chart | alt.LayerChart | alt.HConcatChart | alt.FacetChart


_MULTILINE_LABEL_EXPR = "split(datum.label, '\\n')"


def apply_theme(chart: ThemableChart) -> ThemableChart:
    """Apply consistent typography and axis styling."""
    return (
        chart.configure_view(strokeWidth=0)
        .configure_axis(
            labelFontSize=11,
            titleFontSize=12,
            labelColor="#000",
            titleColor="#000",
            grid=False,
            domainColor="#000",
            tickColor="#000",
        )
        .configure_axisX(
            labelExpr=_MULTILINE_LABEL_EXPR,
            labelAngle=0,
        )
        .configure_axisY(
            labelFontSize=11,
            titleFontSize=12,
            grid=False,
            domain=False,
            ticks=False,
            labelColor="#000",
        )
        .configure_title(
            fontSize=15,
            anchor="middle",
            color="#222",
            fontWeight="bold",
            subtitleFontSize=11,
            subtitleColor="#666",
            subtitleFontWeight="normal",
            offset=12,
            subtitlePadding=6,
        )
        .configure_legend(
            labelFontSize=11,
            titleFontSize=11,
            direction="horizontal",
            titleOrient="left",
            titleAnchor="middle",
            symbolType="square",
            padding=8,
            labelLimit=0,
        )
        .configure_header(
            labelFontSize=12,
            titleFontSize=12,
            labelFontWeight="bold",
            labelExpr=_MULTILINE_LABEL_EXPR,
        )
    )


# ── Saving ───────────────────────────────────────────────────────


def save(chart: ThemableChart, name: str, *, ppi: int = 200) -> Path:
    """Save chart as ``figures/<name>.png`` and return the path."""
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    out_path = FIGURES_DIR / f"{name}.png"
    chart.save(str(out_path), ppi=ppi)
    return out_path
