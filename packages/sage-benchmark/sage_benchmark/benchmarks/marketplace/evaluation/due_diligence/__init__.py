"""Due diligence evaluation — how much effort was expended?

MUST be a subpackage (not a flat file). Contains at minimum:
    - ``__init__.py`` — re-exports ``evaluate_due_diligence``
    - ``evaluate.py`` — the evaluation function
"""

from .evaluate import evaluate_due_diligence

__all__ = ["evaluate_due_diligence"]
