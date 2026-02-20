"""
Privacy Judge - Evaluates information disclosure using multiple approaches.

Provides two judges:
- LeakageJudge: Binary leak detection with majority voting
- CIJudge: Contextual Integrity flow analysis (exhaustive)
"""

from .ci import (
    CIExample,
    CIFlowAnalysis,
    CIFlowExample,
    CIJudge,
    CIJudgment,
    CIVerdict,
    CIVerdictExample,
    NoMoreFlows,
    ReportCIFlow,
)
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
    # CI Judge
    "CIJudge",
    "CIJudgment",
    "CIFlowAnalysis",
    "CIExample",
    "CIFlowExample",
    "CIVerdictExample",
    "CIVerdict",
    "ReportCIFlow",
    "NoMoreFlows",
]
