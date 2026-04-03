"""Smoke-test experiment: 2 tasks per benchmark, all three domains.

Usage::

    sagebench experiment experiment_smoke.py
    sagebench experiment experiment_smoke.py --collect
    sagebench experiment experiment_smoke.py -k calendar
"""

from sage_benchmark.benchmarks.calendar_scheduling.config import CalendarRunConfig
from sage_benchmark.benchmarks.form_filling.config import FormFillingRunConfig
from sage_benchmark.benchmarks.marketplace.config import MarketplaceRunConfig


def experiment_calendar():
    return CalendarRunConfig(
        paths=["data/calendar-scheduling/small.yaml"],
        limit=2,
        model="trapi/gpt-4.1",
        variant="calendar_smoke",
    )


def experiment_marketplace():
    return MarketplaceRunConfig(
        paths=["data/marketplace/small.yaml"],
        limit=2,
        model="trapi/gpt-4.1",
        variant="marketplace_smoke",
    )


def experiment_form_filling():
    return FormFillingRunConfig(
        paths=["data/form-filling/open_ended_only/simple_forms/fs/tasks.yaml"],
        limit=2,
        model="trapi/gpt-4.1",
        variant="form_filling_smoke",
    )
