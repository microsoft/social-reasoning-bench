"""Form filling benchmark package.

This package provides a form filling benchmark supporting two execution modes:
- one-shot: Single structured output from an agent to fill a form
- interactive: Interview Q&A between an interviewer agent and an assistant agent

Usage:
    python -m sage_benchmark.form_filling --execution-mode one-shot --model gpt-4o --data ./data/form-filling/tasks
    python -m sage_benchmark.form_filling --execution-mode interactive --model gpt-4o --interviewer-model gpt-4o --data ./data/form-filling/tasks
"""

from .evaluation import (
    evaluate_correctness,
    evaluate_interactive_task,
    evaluate_privacy,
    evaluate_task,
)
from .loader import load_all_form_tasks
from .runner import run_tasks
from .schemas import (
    ConversationMessage,
    ConversationPrivacyEvaluation,
    CorrectnessEvaluation,
    FormTask,
    FormTaskEvaluationResult,
    InteractiveTaskEvaluationResult,
    InteractiveTaskExecutionResult,
    SecretLeakageEvaluation,
    TaskExecutionResult,
)

__all__ = [
    # Loader
    "load_all_form_tasks",
    # Runner
    "run_tasks",
    # Evaluator
    "evaluate_task",
    "evaluate_interactive_task",
    "evaluate_correctness",
    "evaluate_privacy",
    # Schemas
    "FormTask",
    "TaskExecutionResult",
    "FormTaskEvaluationResult",
    "InteractiveTaskExecutionResult",
    "InteractiveTaskEvaluationResult",
    "CorrectnessEvaluation",
    "SecretLeakageEvaluation",
    "ConversationMessage",
    "ConversationPrivacyEvaluation",
]
