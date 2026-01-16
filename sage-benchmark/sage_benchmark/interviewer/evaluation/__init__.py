"""Evaluation module for interviewer tasks.

Public API:
    evaluate_task: Main dispatcher for evaluating YAML or form tasks
"""

from .evaluation import evaluate_task

__all__ = ["evaluate_task"]
