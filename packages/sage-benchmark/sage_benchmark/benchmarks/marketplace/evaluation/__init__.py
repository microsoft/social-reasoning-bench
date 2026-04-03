"""Evaluation package for the marketplace benchmark.

Every benchmark evaluates task executions across four dimensions,
each in its own SUBPACKAGE (not flat file):

1. **Task completion** -- Was the negotiation outcome correct?
   -> ``evaluation/task_completion/``
2. **Privacy** -- Was private information leaked?
   -> ``evaluation/privacy/``
3. **Due diligence** -- How much effort was expended?
   -> ``evaluation/due_diligence/``
4. **Duty of care** -- Was behavior appropriate and fair?
   -> ``evaluation/duty_of_care/``

The ``evaluator.py`` orchestrator calls each dimension and assembles
the final ``MarketplaceEvaluationResult`` (which embeds the execution result).
"""

from .due_diligence import evaluate_due_diligence
from .duty_of_care import evaluate_duty_of_care
from .evaluator import evaluate_single_task
from .privacy import evaluate_privacy_leakage
from .task_completion import evaluate_task_completion

__all__ = [
    "evaluate_single_task",
    "evaluate_task_completion",
    "evaluate_privacy_leakage",
    "evaluate_due_diligence",
    "evaluate_duty_of_care",
]
