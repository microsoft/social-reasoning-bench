"""Static dashboard for cross-benchmark result visualization."""

from importlib.resources import as_file, files
from pathlib import Path


def get_dashboard_path() -> Path:
    """Return a concrete filesystem path to the dashboard HTML file."""
    ref = files(__package__ or __name__).joinpath("index.html")
    # as_file gives a real Path even for zipped packages
    ctx = as_file(ref)
    return ctx.__enter__()  # caller only reads; no cleanup needed
