"""Smoke-test experiment: 2 tasks per benchmark, calendar + marketplace.

Usage::

    srbench experiment experiment_smoke.py
    srbench experiment experiment_smoke.py --collect
    srbench experiment experiment_smoke.py -k calendar
"""

from srbench.benchmarks.calendar_scheduling.config import CalendarRunConfig
from srbench.benchmarks.marketplace.config import MarketplaceRunConfig

# ── Data paths ──────────────────────────────────────────────────────

CAL_DIR = "data/calendar-scheduling"
MKT_DIR = "data/marketplace"

# ── Fixed values ──────────────────────────────────────────────────────

MODEL = "azure_pool/gpt-4.1"


def experiment_calendar():
    return CalendarRunConfig(
        paths=[f"{CAL_DIR}/small.yaml"],
        limit=2,
        model=MODEL,
        variant="calendar_smoke",
    )


def experiment_marketplace():
    return MarketplaceRunConfig(
        paths=[f"{MKT_DIR}/small.yaml"],
        limit=2,
        model=MODEL,
        variant="marketplace_smoke",
    )
