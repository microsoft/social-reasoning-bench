"""Task completion evaluation — was the negotiation outcome correct?

MUST be a subpackage (not a flat file). Contains at minimum:
    - ``__init__.py`` — re-exports ``evaluate_task_completion``
    - ``evaluate.py`` — the evaluation function
"""

from .evaluate import evaluate_task_completion

__all__ = ["evaluate_task_completion"]
