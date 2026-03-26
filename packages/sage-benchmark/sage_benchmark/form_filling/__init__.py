"""Form filling benchmark package.

This package provides a form filling benchmark using interactive interview Q&A
between an interviewer agent and an assistant agent.

Usage:
    python -m sage_benchmark.form_filling --assistant-model gpt-4o --interviewer-model gpt-4o --data ./data/form-filling/tasks
"""

from .evaluation import (
    evaluate_correctness,
    evaluate_interactive_task,
    evaluate_privacy,
)
from .loader import load_all_form_tasks
from .runner import run_tasks
from .schemas import (
    ConversationMessage,
    ConversationPrivacyEvaluation,
    CorrectnessEvaluation,
    FormTask,
    InteractiveTaskEvaluationResult,
    InteractiveTaskExecutionResult,
    SecretLeakageEvaluation,
)

__all__ = [
    # Loader
    "load_all_form_tasks",
    # Runner
    "run_tasks",
    # Evaluator
    "evaluate_interactive_task",
    "evaluate_correctness",
    "evaluate_privacy",
    # Schemas
    "FormTask",
    "InteractiveTaskExecutionResult",
    "InteractiveTaskEvaluationResult",
    "CorrectnessEvaluation",
    "SecretLeakageEvaluation",
    "ConversationMessage",
    "ConversationPrivacyEvaluation",
]
