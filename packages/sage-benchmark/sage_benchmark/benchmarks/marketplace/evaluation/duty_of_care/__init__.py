"""Duty of care evaluation — was behavior appropriate and fair?

MUST be a subpackage (not a flat file). Contains at minimum:
    - ``__init__.py`` — re-exports ``evaluate_duty_of_care``
    - ``evaluate.py`` — the evaluation function
"""

from .evaluate import evaluate_duty_of_care

__all__ = ["evaluate_duty_of_care"]
