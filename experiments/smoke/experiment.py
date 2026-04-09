"""Smoke-test experiment: 2 tasks per benchmark, all three domains.

Usage::

    sagebench experiment experiment_smoke.py
    sagebench experiment experiment_smoke.py --collect
    sagebench experiment experiment_smoke.py -k calendar
"""

from sage_benchmark.benchmarks.calendar_scheduling.config import CalendarRunConfig
from sage_benchmark.benchmarks.form_filling.config import FormFillingRunConfig
from sage_benchmark.benchmarks.marketplace.config import MarketplaceRunConfig

# ── Data paths ──────────────────────────────────────────────────────

CAL_DIR = "data/calendar-scheduling"
MKT_DIR = "data/marketplace"
FF_DIR = "data/form-filling"

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


def experiment_form_filling():
    return FormFillingRunConfig(
        paths=[f"{FF_DIR}/open_ended_only/simple_forms/fs/tasks.yaml"],
        limit=2,
        model=MODEL,
        variant="form_filling_smoke",
    )
