"""
Privacy Judge - Evaluates information disclosure using multiple approaches.

Provides two judges:
- LeakageJudge: Binary leak detection with majority voting
"""

from .leakage import (
    EvidenceValidationError,
    LeakageExample,
    LeakageJudge,
    LeakageJudgment,
    ReportLeakage,
)

__all__ = [
    # Leakage Judge
    "LeakageJudge",
    "LeakageJudgment",
    "LeakageExample",
    "ReportLeakage",
    "EvidenceValidationError",
]
